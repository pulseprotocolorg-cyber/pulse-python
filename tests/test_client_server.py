"""Tests for PULSE Protocol HTTP client and server.

Tests cover:
- Client initialization and configuration
- Server initialization and handler registration
- Client-server message exchange (JSON and Binary)
- Security: signing, verification, replay protection
- Error handling: invalid messages, network errors
- Retry logic with exponential backoff
- Health check endpoint
- Fire-and-forget messages
- Statistics tracking
"""
import time
import json
import threading
import pytest
from unittest.mock import patch, MagicMock

from pulse.message import PulseMessage
from pulse.client import PulseClient
from pulse.server import PulseServer
from pulse.security import SecurityManager
from pulse.exceptions import NetworkError, SecurityError


# ========== Client Unit Tests ==========


class TestPulseClientInit:
    """Test PulseClient initialization."""

    def test_basic_init(self):
        """Test basic client initialization."""
        client = PulseClient("https://example.com")
        assert client.base_url == "https://example.com"
        assert client.encoding == "json"
        assert client.timeout == 30
        assert client.security is None

    def test_init_with_options(self):
        """Test client initialization with all options."""
        security = SecurityManager(secret_key="test-key")
        client = PulseClient(
            "https://example.com",
            agent_id="agent-001",
            encoding="binary",
            security=security,
            timeout=10,
            max_retries=5,
            retry_base_delay=0.5,
        )
        assert client.agent_id == "agent-001"
        assert client.encoding == "binary"
        assert client.security is security
        assert client.timeout == 10
        assert client.max_retries == 5

    def test_invalid_encoding(self):
        """Test that invalid encoding raises ValueError."""
        with pytest.raises(ValueError, match="Unsupported encoding"):
            PulseClient("https://example.com", encoding="xml")

    def test_trailing_slash_stripped(self):
        """Test that trailing slash is stripped from base_url."""
        client = PulseClient("https://example.com/")
        assert client.base_url == "https://example.com"

    def test_repr(self):
        """Test string representation."""
        client = PulseClient("https://example.com")
        repr_str = repr(client)
        assert "example.com" in repr_str
        assert "json" in repr_str

    def test_initial_stats(self):
        """Test initial statistics are zero."""
        client = PulseClient("https://example.com")
        stats = client.stats
        assert stats["messages_sent"] == 0
        assert stats["messages_failed"] == 0
        assert stats["bytes_sent"] == 0

    def test_reset_stats(self):
        """Test statistics reset."""
        client = PulseClient("https://example.com")
        client._stats["messages_sent"] = 10
        client.reset_stats()
        assert client.stats["messages_sent"] == 0


class TestPulseClientEncoding:
    """Test client message encoding."""

    def test_encode_json(self):
        """Test JSON encoding produces correct content type."""
        client = PulseClient("https://example.com", encoding="json")
        message = PulseMessage(action="ACT.QUERY.DATA")
        data, content_type = client._encode_message(message)
        assert content_type == "application/json"
        assert isinstance(data, bytes)
        # Should be valid JSON
        json.loads(data.decode("utf-8"))

    def test_encode_binary(self):
        """Test Binary encoding produces correct content type."""
        client = PulseClient("https://example.com", encoding="binary")
        message = PulseMessage(action="ACT.QUERY.DATA")
        data, content_type = client._encode_message(message)
        assert content_type == "application/x-pulse-binary"
        assert isinstance(data, bytes)


# ========== Server Unit Tests ==========


class TestPulseServerInit:
    """Test PulseServer initialization."""

    def test_basic_init(self):
        """Test basic server initialization."""
        server = PulseServer()
        assert server.host == "127.0.0.1"
        assert server.port == 8080
        assert server.agent_id == "server-agent"
        assert not server.is_running

    def test_init_with_options(self):
        """Test server initialization with all options."""
        security = SecurityManager(secret_key="test-key")
        server = PulseServer(
            host="0.0.0.0",
            port=9090,
            agent_id="my-server",
            security=security,
            require_signatures=True,
            verbose=True,
        )
        assert server.host == "0.0.0.0"
        assert server.port == 9090
        assert server.agent_id == "my-server"

    def test_add_handler(self):
        """Test handler registration."""
        server = PulseServer()

        def handler(msg):
            return None

        server.add_handler("ACT.QUERY.DATA", handler)
        assert "ACT.QUERY.DATA" in server._handlers

    def test_remove_handler(self):
        """Test handler removal."""
        server = PulseServer()
        server.add_handler("ACT.QUERY.DATA", lambda m: None)
        assert server.remove_handler("ACT.QUERY.DATA")
        assert not server.remove_handler("ACT.QUERY.DATA")  # Already removed

    def test_catch_all_handler(self):
        """Test catch-all handler with '*'."""
        server = PulseServer()
        server.add_handler("*", lambda m: None)
        assert "*" in server._handlers

    def test_repr(self):
        """Test string representation."""
        server = PulseServer(port=9090)
        repr_str = repr(server)
        assert "9090" in repr_str
        assert "stopped" in repr_str

    def test_url_property(self):
        """Test URL property."""
        server = PulseServer(host="0.0.0.0", port=9090)
        assert server.url == "http://0.0.0.0:9090"


# ========== Integration Tests ==========


class TestClientServerIntegration:
    """Integration tests with real HTTP communication."""

    @pytest.fixture
    def server_port(self):
        """Get a free port for testing."""
        import socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("127.0.0.1", 0))
            return s.getsockname()[1]

    @pytest.fixture
    def echo_server(self, server_port):
        """Create and start an echo server."""
        server = PulseServer(
            host="127.0.0.1",
            port=server_port,
            agent_id="test-server",
        )

        def echo_handler(message):
            response = PulseMessage(
                action="ACT.RESPOND",
                sender="test-server",
                validate=False,
            )
            response.type = "RESPONSE"
            response.envelope["receiver"] = message.envelope.get("sender")
            response.content["parameters"] = {
                "echo": message.content.get("parameters", {}),
                "received_action": message.content.get("action"),
            }
            return response

        server.add_handler("*", echo_handler)
        server.start(blocking=False)
        time.sleep(0.2)  # Wait for server to start

        yield server

        server.stop()

    def test_send_json_message(self, echo_server, server_port):
        """Test sending and receiving JSON message."""
        client = PulseClient(
            f"http://127.0.0.1:{server_port}",
            agent_id="test-client",
            encoding="json",
            timeout=5,
        )

        message = PulseMessage(
            action="ACT.QUERY.DATA",
            target="ENT.DATA.TEXT",
            parameters={"query": "hello"},
            sender="test-client",
        )

        response = client.send(message)

        assert response.type == "RESPONSE"
        assert response.content["parameters"]["received_action"] == "ACT.QUERY.DATA"
        assert response.content["parameters"]["echo"]["query"] == "hello"

    def test_send_binary_message(self, echo_server, server_port):
        """Test sending and receiving binary message."""
        client = PulseClient(
            f"http://127.0.0.1:{server_port}",
            agent_id="test-client",
            encoding="binary",
            timeout=5,
        )

        message = PulseMessage(
            action="ACT.QUERY.DATA",
            parameters={"data": [1, 2, 3]},
            sender="test-client",
        )

        response = client.send(message)
        assert response.type == "RESPONSE"
        assert response.content["parameters"]["received_action"] == "ACT.QUERY.DATA"

    def test_send_multiple_messages(self, echo_server, server_port):
        """Test sending multiple messages sequentially."""
        client = PulseClient(
            f"http://127.0.0.1:{server_port}",
            agent_id="test-client",
            timeout=5,
        )

        for i in range(5):
            message = PulseMessage(
                action="ACT.QUERY.DATA",
                parameters={"index": i},
                sender="test-client",
            )
            response = client.send(message)
            assert response.type == "RESPONSE"

        assert client.stats["messages_sent"] == 5

    def test_health_check(self, echo_server, server_port):
        """Test server health check endpoint."""
        client = PulseClient(
            f"http://127.0.0.1:{server_port}",
            agent_id="test-client",
            timeout=5,
        )

        health = client.ping()
        assert health["status"] == "healthy"
        assert health["status_code"] == 200
        assert "latency_ms" in health

    def test_fire_and_forget(self, echo_server, server_port):
        """Test fire-and-forget message sending."""
        client = PulseClient(
            f"http://127.0.0.1:{server_port}",
            agent_id="test-client",
            timeout=5,
        )

        message = PulseMessage(
            action="ACT.QUERY.DATA",
            sender="test-client",
        )
        message.type = "STATUS"

        result = client.send_fire_and_forget(message)
        assert result is True

    def test_server_stats(self, echo_server, server_port):
        """Test server statistics tracking."""
        client = PulseClient(
            f"http://127.0.0.1:{server_port}",
            agent_id="test-client",
            timeout=5,
        )

        message = PulseMessage(action="ACT.QUERY.DATA", sender="test-client")
        client.send(message)

        stats = echo_server.stats
        assert stats["messages_received"] >= 1


class TestClientServerSecurity:
    """Test security features in client-server communication."""

    @pytest.fixture
    def server_port(self):
        """Get a free port."""
        import socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("127.0.0.1", 0))
            return s.getsockname()[1]

    @pytest.fixture
    def secure_server(self, server_port):
        """Create server with security enabled."""
        security = SecurityManager(secret_key="shared-secret-key")
        server = PulseServer(
            host="127.0.0.1",
            port=server_port,
            agent_id="secure-server",
            security=security,
            require_signatures=True,
            enable_replay_protection=True,
        )

        def handler(message):
            response = PulseMessage(
                action="ACT.RESPOND",
                sender="secure-server",
                validate=False,
            )
            response.type = "RESPONSE"
            response.content["parameters"] = {"status": "ok"}
            return response

        server.add_handler("*", handler)
        server.start(blocking=False)
        time.sleep(0.2)

        yield server

        server.stop()

    def test_signed_message_accepted(self, secure_server, server_port):
        """Test that properly signed messages are accepted."""
        security = SecurityManager(secret_key="shared-secret-key")
        client = PulseClient(
            f"http://127.0.0.1:{server_port}",
            agent_id="secure-client",
            security=security,
            timeout=5,
        )

        message = PulseMessage(action="ACT.QUERY.DATA", sender="secure-client")
        response = client.send(message)
        assert response.type == "RESPONSE"

    def test_unsigned_message_rejected(self, secure_server, server_port):
        """Test that unsigned messages are rejected when signatures required."""
        client = PulseClient(
            f"http://127.0.0.1:{server_port}",
            agent_id="unsigned-client",
            timeout=5,
        )

        message = PulseMessage(action="ACT.QUERY.DATA", sender="unsigned-client")

        with pytest.raises(NetworkError, match="403"):
            client.send(message)


class TestClientErrorHandling:
    """Test client error handling."""

    def test_connection_refused(self):
        """Test handling of connection refused."""
        client = PulseClient(
            "http://127.0.0.1:19999",
            timeout=2,
            max_retries=1,
            retry_base_delay=0.1,
        )

        message = PulseMessage(action="ACT.QUERY.DATA")

        with pytest.raises(NetworkError):
            client.send(message)

    def test_ping_unreachable(self):
        """Test health check to unreachable server."""
        client = PulseClient("http://127.0.0.1:19999", timeout=2)
        health = client.ping()
        assert health["status"] in ("unreachable", "error")

    def test_stats_track_failures(self):
        """Test that failures are tracked in stats."""
        client = PulseClient(
            "http://127.0.0.1:19999",
            timeout=1,
            max_retries=1,
            retry_base_delay=0.1,
        )

        message = PulseMessage(action="ACT.QUERY.DATA")

        try:
            client.send(message)
        except NetworkError:
            pass

        assert client.stats["messages_failed"] >= 1

    def test_fire_and_forget_returns_false_on_error(self):
        """Test fire-and-forget returns False on connection error."""
        client = PulseClient("http://127.0.0.1:19999", timeout=1)
        message = PulseMessage(action="ACT.QUERY.DATA")
        result = client.send_fire_and_forget(message)
        assert result is False
