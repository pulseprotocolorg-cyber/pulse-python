"""PULSE Protocol HTTP/HTTPS server for receiving messages.

This module provides:
- PulseServer for receiving PULSE messages over HTTP/HTTPS
- TLS support (HTTPS) with TLSConfig integration
- Request handler with automatic message decoding
- Message signature verification
- Replay attack protection
- Pluggable message handler callbacks

Example:
    >>> def handle_message(message):
    ...     print(f"Received: {message.content['action']}")
    ...     return PulseMessage(action="ACT.RESPOND")
    ...
    >>> server = PulseServer(host="0.0.0.0", port=8080)
    >>> server.add_handler("ACT.QUERY.DATA", handle_message)
    >>> server.start()  # Blocks until stopped

    >>> # With TLS
    >>> from pulse.tls import TLSConfig
    >>> tls = TLSConfig(certfile="cert.pem", keyfile="key.pem")
    >>> server = PulseServer(port=8443, tls=tls)
    >>> server.start()
"""
import json
import ssl
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Optional, Dict, Any, Callable, List
from datetime import datetime, timezone

from pulse.message import PulseMessage
from pulse.security import SecurityManager
from pulse.encoder import JSONEncoder, BinaryEncoder
from pulse.validator import MessageValidator
from pulse.exceptions import (
    NetworkError,
    SecurityError,
    ValidationError,
)


class PulseRequestHandler(BaseHTTPRequestHandler):
    """
    HTTP request handler for PULSE Protocol messages.

    Handles incoming POST requests containing PULSE messages,
    validates them, and dispatches to registered handlers.
    """

    def do_POST(self) -> None:
        """Handle incoming POST request with PULSE message."""
        try:
            # Read request body
            content_length = int(self.headers.get("Content-Length", 0))
            if content_length == 0:
                self._send_error(400, "Empty request body")
                return

            body = self.rfile.read(content_length)
            content_type = self.headers.get("Content-Type", "application/json")

            # Decode message
            message = self._decode_message(body, content_type)
            if message is None:
                return  # Error already sent

            # Validate message
            try:
                message.validate(check_freshness=False)
            except ValidationError as e:
                self._send_error(400, f"Validation failed: {e}")
                return

            # Check security if configured
            server_config = self.server.pulse_config
            if server_config.get("security"):
                security = server_config["security"]

                # Verify signature
                if message.envelope.get("signature"):
                    if not security.verify_signature(message):
                        self._send_error(403, "Signature verification failed")
                        return
                elif server_config.get("require_signatures", False):
                    self._send_error(403, "Message signature required")
                    return

                # Check replay protection
                nonce_store = server_config.get("nonce_store")
                if nonce_store is not None:
                    result = SecurityManager.check_replay_protection(
                        message, nonce_store=nonce_store
                    )
                    if not result["is_valid"]:
                        self._send_error(
                            403, f"Replay protection: {result['reason']}"
                        )
                        return

            # Dispatch to handler
            action = message.content.get("action", "")
            handlers = server_config.get("handlers", {})

            handler = handlers.get(action) or handlers.get("*")

            if handler is None:
                self._send_error(
                    404, f"No handler registered for action: {action}"
                )
                return

            # Call handler
            response_message = handler(message)

            if response_message is None:
                # Handler returned nothing — send 204 No Content
                self.send_response(204)
                self.end_headers()
                server_config["stats"]["messages_received"] += 1
                return

            # Encode and send response
            if not isinstance(response_message, PulseMessage):
                self._send_error(500, "Handler must return PulseMessage or None")
                return

            # Sign response if security configured
            if server_config.get("security"):
                server_config["security"].sign_message(response_message)

            # Encode response
            encoding = self.headers.get("X-PULSE-Encoding", "json")
            response_data, response_content_type = self._encode_response(
                response_message, encoding
            )

            # Send response
            self.send_response(200)
            self.send_header("Content-Type", response_content_type)
            self.send_header("Content-Length", str(len(response_data)))
            self.send_header("X-PULSE-Version", "1.0")
            self.end_headers()
            self.wfile.write(response_data)

            server_config["stats"]["messages_received"] += 1

        except Exception as e:
            self._send_error(500, f"Internal error: {e}")
            server_config = getattr(self.server, "pulse_config", {})
            stats = server_config.get("stats", {})
            if "errors" in stats:
                stats["errors"] += 1

    def do_GET(self) -> None:
        """Handle health check and info requests."""
        if self.path in ("/pulse/v1/health", "/health"):
            server_config = self.server.pulse_config
            health = {
                "status": "healthy",
                "version": "1.0",
                "agent_id": server_config.get("agent_id", "unknown"),
                "encoding": server_config.get("encoding", "json"),
                "security": server_config.get("security") is not None,
                "handlers": list(server_config.get("handlers", {}).keys()),
                "stats": server_config.get("stats", {}),
                "timestamp": datetime.now(timezone.utc)
                .isoformat()
                .replace("+00:00", "Z"),
            }
            body = json.dumps(health, indent=2).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            self._send_error(404, "Not found. Use POST /pulse/v1/messages")

    def _decode_message(
        self, data: bytes, content_type: str
    ) -> Optional[PulseMessage]:
        """
        Decode incoming message based on Content-Type.

        Args:
            data: Request body bytes
            content_type: Content-Type header value

        Returns:
            PulseMessage or None if decoding failed
        """
        try:
            if "x-pulse-binary" in content_type or "msgpack" in content_type:
                return BinaryEncoder.decode(data)
            else:
                return JSONEncoder.decode(data)
        except Exception as e:
            self._send_error(400, f"Failed to decode message: {e}")
            return None

    def _encode_response(
        self, message: PulseMessage, encoding: str
    ) -> tuple:
        """
        Encode response message.

        Args:
            message: PulseMessage to encode
            encoding: Encoding format

        Returns:
            Tuple of (encoded_bytes, content_type)
        """
        if encoding == "binary":
            return BinaryEncoder.encode(message), "application/x-pulse-binary"
        else:
            return JSONEncoder.encode(message, indent=None), "application/json"

    def _send_error(self, status: int, message: str) -> None:
        """Send error response."""
        error = PulseMessage.__new__(PulseMessage)
        error.envelope = {
            "version": "1.0",
            "timestamp": datetime.now(timezone.utc)
            .isoformat()
            .replace("+00:00", "Z"),
            "sender": getattr(self.server, "pulse_config", {}).get(
                "agent_id", "server"
            ),
            "receiver": None,
            "message_id": None,
            "nonce": None,
            "signature": None,
        }
        error.type = "ERROR"
        error.content = {
            "action": "META.ERROR.GENERAL",
            "object": None,
            "parameters": {"error": message, "status_code": status},
        }

        body = json.dumps(error.to_dict()).encode("utf-8")

        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args) -> None:
        """Suppress default HTTP server logging."""
        server_config = getattr(self.server, "pulse_config", {})
        if server_config.get("verbose", False):
            super().log_message(format, *args)


class PulseServer:
    """
    HTTP server for receiving PULSE Protocol messages.

    Provides a simple HTTP server that receives, validates, and dispatches
    PULSE messages to registered handler functions.

    Attributes:
        host: Server bind address
        port: Server listen port
        agent_id: This server's agent identifier

    Example:
        >>> def echo_handler(message):
        ...     response = PulseMessage(action="ACT.RESPOND")
        ...     response.type = "RESPONSE"
        ...     response.content["parameters"] = {
        ...         "echo": message.content["parameters"]
        ...     }
        ...     return response
        ...
        >>> server = PulseServer(port=8080)
        >>> server.add_handler("ACT.QUERY.DATA", echo_handler)
        >>> server.start()  # Blocks until Ctrl+C
    """

    def __init__(
        self,
        host: str = "127.0.0.1",
        port: int = 8080,
        agent_id: str = "server-agent",
        security: Optional[SecurityManager] = None,
        require_signatures: bool = False,
        enable_replay_protection: bool = True,
        verbose: bool = False,
        tls: Optional["TLSConfig"] = None,
    ) -> None:
        """
        Initialize PULSE server.

        Args:
            host: Bind address (default "127.0.0.1" for local only)
            port: Listen port (default 8080)
            agent_id: Server's agent identifier
            security: SecurityManager for signature verification
            require_signatures: Reject unsigned messages (default False)
            enable_replay_protection: Enable nonce tracking (default True)
            verbose: Enable HTTP request logging (default False)
            tls: TLSConfig for HTTPS support (None = plain HTTP)

        Example:
            >>> server = PulseServer(port=9090, agent_id="my-server")
            >>> server = PulseServer(
            ...     security=SecurityManager(secret_key="shared-key"),
            ...     require_signatures=True
            ... )

            >>> # With TLS
            >>> from pulse.tls import TLSConfig
            >>> tls = TLSConfig(certfile="cert.pem", keyfile="key.pem")
            >>> server = PulseServer(port=8443, tls=tls)
        """
        self.host = host
        self.port = port
        self.agent_id = agent_id
        self.tls = tls

        self._handlers: Dict[str, Callable] = {}
        self._httpd: Optional[HTTPServer] = None
        self._thread: Optional[threading.Thread] = None

        # Server config passed to request handler
        self._config = {
            "agent_id": agent_id,
            "security": security,
            "require_signatures": require_signatures,
            "handlers": self._handlers,
            "nonce_store": set() if enable_replay_protection else None,
            "encoding": "json",
            "verbose": verbose,
            "tls_enabled": tls is not None,
            "stats": {
                "messages_received": 0,
                "errors": 0,
                "started_at": None,
            },
        }

    def add_handler(
        self, action: str, handler: Callable[[PulseMessage], Optional[PulseMessage]]
    ) -> None:
        """
        Register a message handler for a specific action.

        The handler receives a PulseMessage and should return a PulseMessage
        response (or None for fire-and-forget messages).

        Use "*" as action to create a catch-all handler.

        Args:
            action: PULSE action concept (e.g., "ACT.QUERY.DATA") or "*"
            handler: Callable that takes PulseMessage and returns PulseMessage or None

        Example:
            >>> def handle_query(msg):
            ...     return PulseMessage(action="ACT.RESPOND")
            ...
            >>> server.add_handler("ACT.QUERY.DATA", handle_query)
            >>> server.add_handler("*", default_handler)  # Catch-all
        """
        self._handlers[action] = handler

    def remove_handler(self, action: str) -> bool:
        """
        Remove a registered handler.

        Args:
            action: Action to remove handler for

        Returns:
            True if handler was removed, False if not found
        """
        if action in self._handlers:
            del self._handlers[action]
            return True
        return False

    def start(self, blocking: bool = True) -> None:
        """
        Start the PULSE server.

        If TLS is configured, the server will use HTTPS. Otherwise plain HTTP.

        Args:
            blocking: If True, blocks until server is stopped (default True).
                     If False, starts in background thread.

        Raises:
            FileNotFoundError: If TLS cert/key files don't exist
            ssl.SSLError: If TLS configuration is invalid

        Example:
            >>> server.start()  # Blocks
            >>> server.start(blocking=False)  # Background
            >>> # ... do other work ...
            >>> server.stop()
        """
        self._httpd = HTTPServer((self.host, self.port), PulseRequestHandler)
        self._httpd.pulse_config = self._config

        # Wrap socket with TLS if configured
        if self.tls is not None:
            ssl_context = self.tls.create_server_context()
            self._httpd.socket = ssl_context.wrap_socket(
                self._httpd.socket, server_side=True
            )

        self._config["stats"]["started_at"] = (
            datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        )

        if blocking:
            try:
                self._httpd.serve_forever()
            except KeyboardInterrupt:
                self.stop()
        else:
            self._thread = threading.Thread(
                target=self._httpd.serve_forever, daemon=True
            )
            self._thread.start()

    def stop(self) -> None:
        """
        Stop the PULSE server.

        Example:
            >>> server.start(blocking=False)
            >>> # ... later ...
            >>> server.stop()
        """
        if self._httpd:
            self._httpd.shutdown()
            self._httpd.server_close()
            self._httpd = None
            self._thread = None

    @property
    def is_running(self) -> bool:
        """Check if server is running."""
        return self._httpd is not None

    @property
    def stats(self) -> Dict[str, Any]:
        """
        Get server statistics.

        Returns:
            Dictionary with message counts and timing info
        """
        return dict(self._config["stats"])

    @property
    def url(self) -> str:
        """Get the server's base URL."""
        scheme = "https" if self.tls else "http"
        return f"{scheme}://{self.host}:{self.port}"

    def __repr__(self) -> str:
        """Return string representation."""
        status = "running" if self.is_running else "stopped"
        return (
            f"PulseServer(host='{self.host}', port={self.port}, "
            f"agent_id='{self.agent_id}', status='{status}')"
        )
