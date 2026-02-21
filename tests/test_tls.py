"""Tests for PULSE TLS transport layer.

Tests cover:
- Self-signed certificate generation
- TLSConfig creation and validation
- Server SSL context creation
- Client SSL context creation
- HTTPS server/client communication
- mTLS (mutual TLS) support
- TLS version enforcement
- Error handling (missing certs, invalid configs)
"""
import os
import ssl
import time
import tempfile
import threading
import pytest

from pulse.tls import TLSConfig, generate_self_signed_cert
from pulse.message import PulseMessage
from pulse.client import PulseClient
from pulse.server import PulseServer
from pulse.security import SecurityManager


class TestCertificateGeneration:
    """Test self-signed certificate generation."""

    def test_generate_default_cert(self):
        """Test generating a default self-signed certificate."""
        cert_path, key_path = generate_self_signed_cert()
        assert os.path.isfile(cert_path)
        assert os.path.isfile(key_path)

        # Check PEM format
        with open(cert_path, "r") as f:
            cert_content = f.read()
        assert "BEGIN CERTIFICATE" in cert_content

        with open(key_path, "r") as f:
            key_content = f.read()
        assert "BEGIN" in key_content and "KEY" in key_content

    def test_generate_cert_custom_hostname(self):
        """Test generating cert with custom hostname."""
        cert_path, key_path = generate_self_signed_cert(
            hostname="agent.example.com"
        )
        assert os.path.isfile(cert_path)
        assert os.path.isfile(key_path)

    def test_generate_cert_custom_output_dir(self):
        """Test generating cert in custom directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            cert_path, key_path = generate_self_signed_cert(
                output_dir=tmpdir
            )
            assert cert_path.startswith(tmpdir)
            assert key_path.startswith(tmpdir)
            assert os.path.isfile(cert_path)
            assert os.path.isfile(key_path)

    def test_generate_cert_creates_output_dir(self):
        """Test that output dir is created if it doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            subdir = os.path.join(tmpdir, "certs", "dev")
            cert_path, key_path = generate_self_signed_cert(
                output_dir=subdir
            )
            assert os.path.isdir(subdir)
            assert os.path.isfile(cert_path)

    def test_generate_cert_custom_validity(self):
        """Test generating cert with custom validity period."""
        cert_path, key_path = generate_self_signed_cert(days_valid=30)
        assert os.path.isfile(cert_path)

    def test_generate_cert_custom_key_size(self):
        """Test generating cert with custom key size."""
        cert_path, key_path = generate_self_signed_cert(key_size=4096)
        assert os.path.isfile(cert_path)


class TestTLSConfig:
    """Test TLSConfig dataclass."""

    def test_default_config(self):
        """Test default TLSConfig values."""
        config = TLSConfig()
        assert config.certfile == ""
        assert config.keyfile == ""
        assert config.cafile is None
        assert config.require_client_cert is False
        assert config.min_version == ssl.TLSVersion.TLSv1_2
        assert config.ciphers is None

    def test_config_with_cert_paths(self):
        """Test TLSConfig with certificate paths."""
        config = TLSConfig(
            certfile="/path/to/cert.pem",
            keyfile="/path/to/key.pem"
        )
        assert config.certfile == "/path/to/cert.pem"
        assert config.keyfile == "/path/to/key.pem"

    def test_config_with_mtls(self):
        """Test TLSConfig with mutual TLS settings."""
        config = TLSConfig(
            certfile="/path/to/cert.pem",
            keyfile="/path/to/key.pem",
            cafile="/path/to/ca.pem",
            require_client_cert=True,
        )
        assert config.require_client_cert is True
        assert config.cafile == "/path/to/ca.pem"


class TestTLSServerContext:
    """Test server SSL context creation."""

    def test_create_server_context(self):
        """Test creating server SSL context with valid certs."""
        cert_path, key_path = generate_self_signed_cert()
        config = TLSConfig(certfile=cert_path, keyfile=key_path)
        ctx = config.create_server_context()
        assert isinstance(ctx, ssl.SSLContext)

    def test_server_context_missing_certfile(self):
        """Test server context fails without certfile."""
        config = TLSConfig(keyfile="/some/key.pem")
        with pytest.raises(ValueError, match="certfile is required"):
            config.create_server_context()

    def test_server_context_missing_keyfile(self):
        """Test server context fails without keyfile."""
        config = TLSConfig(certfile="/some/cert.pem")
        with pytest.raises(ValueError, match="keyfile is required"):
            config.create_server_context()

    def test_server_context_nonexistent_certfile(self):
        """Test server context fails with non-existent cert file."""
        config = TLSConfig(
            certfile="/nonexistent/cert.pem",
            keyfile="/nonexistent/key.pem"
        )
        with pytest.raises(FileNotFoundError, match="Certificate file"):
            config.create_server_context()

    def test_server_context_nonexistent_keyfile(self):
        """Test server context fails with non-existent key file."""
        cert_path, _ = generate_self_signed_cert()
        config = TLSConfig(
            certfile=cert_path,
            keyfile="/nonexistent/key.pem"
        )
        with pytest.raises(FileNotFoundError, match="Key file"):
            config.create_server_context()

    def test_server_context_no_client_cert_required(self):
        """Test server context without client cert requirement."""
        cert_path, key_path = generate_self_signed_cert()
        config = TLSConfig(certfile=cert_path, keyfile=key_path)
        ctx = config.create_server_context()
        assert ctx.verify_mode == ssl.CERT_NONE

    def test_server_context_client_cert_required(self):
        """Test server context with client cert requirement (mTLS)."""
        cert_path, key_path = generate_self_signed_cert()
        config = TLSConfig(
            certfile=cert_path,
            keyfile=key_path,
            cafile=cert_path,  # Use same cert as CA for test
            require_client_cert=True,
        )
        ctx = config.create_server_context()
        assert ctx.verify_mode == ssl.CERT_REQUIRED

    def test_server_context_nonexistent_cafile(self):
        """Test server context fails with non-existent CA file."""
        cert_path, key_path = generate_self_signed_cert()
        config = TLSConfig(
            certfile=cert_path,
            keyfile=key_path,
            cafile="/nonexistent/ca.pem",
        )
        with pytest.raises(FileNotFoundError, match="CA file"):
            config.create_server_context()


class TestTLSClientContext:
    """Test client SSL context creation."""

    def test_create_client_context_no_verify(self):
        """Test creating client context with verification disabled."""
        config = TLSConfig()
        ctx = config.create_client_context(verify=False)
        assert isinstance(ctx, ssl.SSLContext)
        assert ctx.verify_mode == ssl.CERT_NONE
        assert ctx.check_hostname is False

    def test_create_client_context_with_ca(self):
        """Test creating client context with custom CA."""
        cert_path, _ = generate_self_signed_cert()
        config = TLSConfig(cafile=cert_path)
        ctx = config.create_client_context(verify=True)
        assert ctx.verify_mode == ssl.CERT_REQUIRED
        assert ctx.check_hostname is True


class TestTLSServerClient:
    """Test HTTPS server-client communication."""

    @pytest.fixture
    def tls_certs(self):
        """Generate TLS certificates for testing."""
        cert_path, key_path = generate_self_signed_cert(hostname="localhost")
        return cert_path, key_path

    @pytest.fixture
    def tls_server(self, tls_certs):
        """Create and start a TLS-enabled PULSE server."""
        cert_path, key_path = tls_certs
        tls_config = TLSConfig(certfile=cert_path, keyfile=key_path)

        server = PulseServer(
            host="127.0.0.1",
            port=0,  # Will use actual port from socket
            agent_id="tls-test-server",
            tls=tls_config,
        )

        # Use a wildcard handler for testing
        def echo_handler(message):
            response = PulseMessage(action="ACT.QUERY.DATA")
            response.type = "RESPONSE"
            response.content["parameters"] = {
                "echo": message.content.get("action", "unknown"),
                "tls": True,
            }
            return response

        server.add_handler("*", echo_handler)

        # We need to create the HTTPServer manually to get the actual port
        from http.server import HTTPServer
        from pulse.server import PulseRequestHandler

        httpd = HTTPServer(("127.0.0.1", 0), PulseRequestHandler)
        httpd.pulse_config = server._config
        actual_port = httpd.server_address[1]

        # Wrap with TLS
        ssl_context = tls_config.create_server_context()
        httpd.socket = ssl_context.wrap_socket(httpd.socket, server_side=True)

        # Start in background
        thread = threading.Thread(target=httpd.serve_forever, daemon=True)
        thread.start()

        yield actual_port, cert_path

        httpd.shutdown()
        httpd.server_close()

    def test_https_server_starts(self, tls_certs):
        """Test that a TLS-configured server can be created."""
        cert_path, key_path = tls_certs
        tls_config = TLSConfig(certfile=cert_path, keyfile=key_path)
        server = PulseServer(
            port=0, tls=tls_config, agent_id="tls-test"
        )
        assert server.tls is not None
        assert "https" in server.url

    def test_server_url_scheme_https(self, tls_certs):
        """Test server URL uses https scheme when TLS configured."""
        cert_path, key_path = tls_certs
        tls_config = TLSConfig(certfile=cert_path, keyfile=key_path)
        server = PulseServer(host="0.0.0.0", port=8443, tls=tls_config)
        assert server.url == "https://0.0.0.0:8443"

    def test_server_url_scheme_http(self):
        """Test server URL uses http scheme when no TLS."""
        server = PulseServer(host="0.0.0.0", port=8080)
        assert server.url == "http://0.0.0.0:8080"

    def test_https_send_receive(self, tls_server):
        """Test sending and receiving messages over HTTPS."""
        port, cert_path = tls_server

        # Create client with custom CA (self-signed cert)
        tls_config = TLSConfig(cafile=cert_path)
        client = PulseClient(
            f"https://localhost:{port}",
            agent_id="tls-test-client",
            tls=tls_config,
        )

        message = PulseMessage(action="ACT.QUERY.DATA")
        response = client.send(message)

        assert response.type == "RESPONSE"
        assert response.content["parameters"]["echo"] == "ACT.QUERY.DATA"
        assert response.content["parameters"]["tls"] is True

    def test_https_send_no_verify(self, tls_server):
        """Test sending messages over HTTPS without cert verification."""
        port, _ = tls_server

        client = PulseClient(
            f"https://localhost:{port}",
            agent_id="tls-test-client",
            verify_ssl=False,
        )

        message = PulseMessage(action="ACT.CREATE.TEXT")
        response = client.send(message)

        assert response.type == "RESPONSE"
        assert response.content["parameters"]["echo"] == "ACT.CREATE.TEXT"

    def test_https_with_security_signing(self, tls_server):
        """Test HTTPS with HMAC message signing."""
        port, cert_path = tls_server

        security = SecurityManager(secret_key="test-shared-key")
        tls_config = TLSConfig(cafile=cert_path)
        client = PulseClient(
            f"https://localhost:{port}",
            agent_id="secure-client",
            security=security,
            tls=tls_config,
        )

        message = PulseMessage(action="ACT.QUERY.DATA")
        response = client.send(message)

        assert response.type == "RESPONSE"

    def test_https_binary_encoding(self, tls_server):
        """Test HTTPS with binary (MessagePack) encoding."""
        port, cert_path = tls_server

        tls_config = TLSConfig(cafile=cert_path)
        client = PulseClient(
            f"https://localhost:{port}",
            agent_id="binary-client",
            encoding="binary",
            tls=tls_config,
        )

        message = PulseMessage(action="ACT.ANALYZE.SENTIMENT")
        response = client.send(message)

        assert response.type == "RESPONSE"

    def test_https_fire_and_forget(self, tls_server):
        """Test fire-and-forget over HTTPS."""
        port, cert_path = tls_server

        tls_config = TLSConfig(cafile=cert_path)
        client = PulseClient(
            f"https://localhost:{port}",
            agent_id="fire-forget-client",
            tls=tls_config,
        )

        message = PulseMessage(action="ACT.QUERY.DATA")
        result = client.send_fire_and_forget(message)
        assert result is True

    def test_https_ping(self, tls_server):
        """Test health check over HTTPS."""
        port, cert_path = tls_server

        tls_config = TLSConfig(cafile=cert_path)
        client = PulseClient(
            f"https://localhost:{port}",
            agent_id="ping-client",
            tls=tls_config,
        )

        health = client.ping()
        assert health["status"] == "healthy"
        assert health["status_code"] == 200


class TestTLSConfigValidation:
    """Test TLS configuration edge cases."""

    def test_tls_config_equality(self):
        """Test TLSConfig dataclass equality."""
        config1 = TLSConfig(certfile="a.pem", keyfile="b.pem")
        config2 = TLSConfig(certfile="a.pem", keyfile="b.pem")
        assert config1 == config2

    def test_tls_min_version_default(self):
        """Test default minimum TLS version is 1.2."""
        config = TLSConfig()
        assert config.min_version == ssl.TLSVersion.TLSv1_2

    def test_client_config_tls_overrides_verify_ssl(self):
        """Test that TLSConfig overrides simple verify_ssl flag."""
        cert_path, _ = generate_self_signed_cert()
        tls_config = TLSConfig(cafile=cert_path)

        client = PulseClient(
            "https://example.com",
            verify_ssl=True,
            tls=tls_config,
        )
        # The TLSConfig should have been used for context creation
        assert client.tls is tls_config
