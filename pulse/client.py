"""PULSE Protocol HTTP client for network communication.

This module provides:
- PulseClient for sending PULSE messages over HTTP/HTTPS
- Automatic retry with exponential backoff
- Message signing and verification
- Support for JSON and Binary encoding formats
- Connection pooling and timeout management

Example:
    >>> client = PulseClient(base_url="https://agent-002.example.com")
    >>> message = PulseMessage(action="ACT.QUERY.DATA", target="ENT.DATA.TEXT")
    >>> response = client.send(message)
    >>> print(response.content)
"""
import json
import ssl
import time
import urllib.request
import urllib.error
from typing import Optional, Dict, Any, List
from datetime import datetime, timezone

from pulse.message import PulseMessage
from pulse.security import SecurityManager
from pulse.encoder import JSONEncoder, BinaryEncoder
from pulse.exceptions import NetworkError, SecurityError, TimeoutError


class PulseClient:
    """
    HTTP client for sending and receiving PULSE messages.

    Supports both JSON and Binary (MessagePack) encoding formats,
    automatic message signing, retry logic with exponential backoff,
    and TLS verification.

    Attributes:
        base_url: Target server URL
        encoding: Message encoding format ("json" or "binary")
        security: SecurityManager for message signing (optional)
        timeout: Request timeout in seconds

    Example:
        >>> # Basic usage
        >>> client = PulseClient("https://agent-002.example.com")
        >>> message = PulseMessage(action="ACT.QUERY.DATA")
        >>> response = client.send(message)

        >>> # With security
        >>> security = SecurityManager(secret_key="shared-secret")
        >>> client = PulseClient(
        ...     "https://agent-002.example.com",
        ...     security=security,
        ...     encoding="binary"
        ... )
        >>> response = client.send(message)
    """

    def __init__(
        self,
        base_url: str,
        agent_id: str = "default-agent",
        encoding: str = "json",
        security: Optional[SecurityManager] = None,
        timeout: int = 30,
        max_retries: int = 3,
        retry_base_delay: float = 1.0,
        verify_ssl: bool = True,
        tls: Optional["TLSConfig"] = None,
        client_certfile: Optional[str] = None,
        client_keyfile: Optional[str] = None,
    ) -> None:
        """
        Initialize PULSE client.

        Args:
            base_url: Target server base URL (e.g., "https://agent.example.com")
            agent_id: This agent's identifier for message sender field
            encoding: Message encoding format ("json" or "binary")
            security: SecurityManager for signing messages (None = no signing)
            timeout: Request timeout in seconds (default 30)
            max_retries: Maximum retry attempts for transient failures (default 3)
            retry_base_delay: Base delay in seconds for exponential backoff (default 1.0)
            verify_ssl: Whether to verify SSL certificates (default True)
            tls: TLSConfig for advanced TLS settings (overrides verify_ssl)
            client_certfile: Path to client certificate for mTLS
            client_keyfile: Path to client private key for mTLS

        Raises:
            ValueError: If encoding format is not supported

        Example:
            >>> client = PulseClient("https://agent-002.example.com")
            >>> client = PulseClient(
            ...     "https://agent-002.example.com",
            ...     encoding="binary",
            ...     timeout=10
            ... )

            >>> # With TLS config and custom CA
            >>> from pulse.tls import TLSConfig
            >>> tls = TLSConfig(cafile="/path/to/ca.pem")
            >>> client = PulseClient("https://agent.example.com", tls=tls)
        """
        if encoding not in ("json", "binary"):
            raise ValueError(
                f"Unsupported encoding: '{encoding}'. Use 'json' or 'binary'."
            )

        self.base_url = base_url.rstrip("/")
        self.agent_id = agent_id
        self.encoding = encoding
        self.security = security
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_base_delay = retry_base_delay
        self.verify_ssl = verify_ssl
        self.tls = tls

        # SSL context - use TLSConfig if provided, otherwise basic
        if tls is not None:
            self._ssl_context = tls.create_client_context(
                verify=verify_ssl,
                client_certfile=client_certfile,
                client_keyfile=client_keyfile,
            )
        else:
            self._ssl_context = self._create_ssl_context()

        # Stats tracking
        self._stats = {
            "messages_sent": 0,
            "messages_failed": 0,
            "retries_total": 0,
            "bytes_sent": 0,
            "bytes_received": 0,
        }

    def _create_ssl_context(self) -> ssl.SSLContext:
        """
        Create SSL context for HTTPS connections.

        Returns:
            Configured SSL context
        """
        context = ssl.create_default_context()
        if not self.verify_ssl:
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
        return context

    def send(
        self,
        message: PulseMessage,
        path: str = "/pulse/v1/messages",
        receiver: Optional[str] = None,
    ) -> PulseMessage:
        """
        Send a PULSE message and receive a response.

        Signs the message (if security configured), encodes it,
        sends via HTTP POST, and decodes the response.

        Args:
            message: PulseMessage to send
            path: API endpoint path (default "/pulse/v1/messages")
            receiver: Optional receiver agent ID to set in envelope

        Returns:
            PulseMessage response from the server

        Raises:
            NetworkError: If request fails after all retries
            SecurityError: If response signature verification fails
            TimeoutError: If request times out

        Example:
            >>> client = PulseClient("https://agent-002.example.com")
            >>> message = PulseMessage(action="ACT.QUERY.DATA")
            >>> response = client.send(message)
            >>> print(response.type)  # "RESPONSE"
        """
        # Set receiver if specified
        if receiver:
            message.envelope["receiver"] = receiver

        # Set sender
        message.envelope["sender"] = self.agent_id

        # Sign message if security is configured
        if self.security:
            self.security.sign_message(message)

        # Encode message
        encoded_data, content_type = self._encode_message(message)

        # Build request
        url = f"{self.base_url}{path}"
        headers = {
            "Content-Type": content_type,
            "Accept": content_type,
            "X-PULSE-Version": "1.0",
            "X-PULSE-Sender": self.agent_id,
            "X-PULSE-Encoding": self.encoding,
        }

        # Send with retry
        response_data = self._send_with_retry(url, encoded_data, headers)

        # Decode response
        response_message = self._decode_response(response_data)

        # Verify response signature if security configured
        if self.security and response_message.envelope.get("signature"):
            if not self.security.verify_signature(response_message):
                raise SecurityError("Response signature verification failed")

        self._stats["messages_sent"] += 1
        self._stats["bytes_sent"] += len(encoded_data)
        self._stats["bytes_received"] += len(response_data)

        return response_message

    def send_fire_and_forget(
        self,
        message: PulseMessage,
        path: str = "/pulse/v1/messages",
        receiver: Optional[str] = None,
    ) -> bool:
        """
        Send a PULSE message without waiting for a structured response.

        Useful for STATUS messages, notifications, and events where
        a response is not expected.

        Args:
            message: PulseMessage to send
            path: API endpoint path
            receiver: Optional receiver agent ID

        Returns:
            True if message was accepted (2xx status), False otherwise

        Example:
            >>> status = PulseMessage(action="ACT.NOTIFY")
            >>> status.type = "STATUS"
            >>> success = client.send_fire_and_forget(status)
        """
        if receiver:
            message.envelope["receiver"] = receiver

        message.envelope["sender"] = self.agent_id

        if self.security:
            self.security.sign_message(message)

        encoded_data, content_type = self._encode_message(message)

        url = f"{self.base_url}{path}"
        headers = {
            "Content-Type": content_type,
            "X-PULSE-Version": "1.0",
            "X-PULSE-Sender": self.agent_id,
            "X-PULSE-Encoding": self.encoding,
        }

        try:
            request = urllib.request.Request(
                url, data=encoded_data, headers=headers, method="POST"
            )
            with urllib.request.urlopen(
                request, timeout=self.timeout, context=self._ssl_context
            ) as response:
                self._stats["messages_sent"] += 1
                self._stats["bytes_sent"] += len(encoded_data)
                return 200 <= response.status < 300
        except Exception:
            self._stats["messages_failed"] += 1
            return False

    def ping(self, path: str = "/pulse/v1/health") -> Dict[str, Any]:
        """
        Check if the target server is reachable and healthy.

        Args:
            path: Health check endpoint path

        Returns:
            Dictionary with health status and latency

        Example:
            >>> health = client.ping()
            >>> print(f"Status: {health['status']}, Latency: {health['latency_ms']}ms")
        """
        url = f"{self.base_url}{path}"
        start_time = time.monotonic()

        try:
            request = urllib.request.Request(url, method="GET")
            request.add_header("X-PULSE-Version", "1.0")

            with urllib.request.urlopen(
                request, timeout=self.timeout, context=self._ssl_context
            ) as response:
                latency = (time.monotonic() - start_time) * 1000
                body = response.read().decode("utf-8")

                return {
                    "status": "healthy",
                    "status_code": response.status,
                    "latency_ms": round(latency, 2),
                    "body": body,
                }
        except urllib.error.URLError as e:
            latency = (time.monotonic() - start_time) * 1000
            return {
                "status": "unreachable",
                "error": str(e.reason),
                "latency_ms": round(latency, 2),
            }
        except Exception as e:
            latency = (time.monotonic() - start_time) * 1000
            return {
                "status": "error",
                "error": str(e),
                "latency_ms": round(latency, 2),
            }

    def _encode_message(self, message: PulseMessage) -> tuple:
        """
        Encode message based on configured format.

        Args:
            message: PulseMessage to encode

        Returns:
            Tuple of (encoded_bytes, content_type_string)
        """
        if self.encoding == "binary":
            data = BinaryEncoder.encode(message)
            content_type = "application/x-pulse-binary"
        else:
            data = JSONEncoder.encode(message, indent=None)
            content_type = "application/json"

        return data, content_type

    def _decode_response(self, data: bytes) -> PulseMessage:
        """
        Decode response based on configured format.

        Args:
            data: Response bytes

        Returns:
            PulseMessage instance
        """
        if self.encoding == "binary":
            # Try binary first, fall back to JSON
            try:
                return BinaryEncoder.decode(data)
            except Exception:
                pass

        # Try JSON
        try:
            return JSONEncoder.decode(data)
        except Exception:
            pass

        # Try binary as last resort
        try:
            return BinaryEncoder.decode(data)
        except Exception as e:
            raise NetworkError(f"Failed to decode response: {e}") from e

    def _send_with_retry(
        self, url: str, data: bytes, headers: Dict[str, str]
    ) -> bytes:
        """
        Send HTTP request with exponential backoff retry.

        Args:
            url: Request URL
            data: Request body bytes
            headers: HTTP headers

        Returns:
            Response body bytes

        Raises:
            NetworkError: If all retries fail
            TimeoutError: If request times out
        """
        last_error = None

        for attempt in range(1, self.max_retries + 1):
            try:
                request = urllib.request.Request(
                    url, data=data, headers=headers, method="POST"
                )

                with urllib.request.urlopen(
                    request, timeout=self.timeout, context=self._ssl_context
                ) as response:
                    return response.read()

            except urllib.error.HTTPError as e:
                last_error = e
                status = e.code

                # Don't retry client errors (4xx) except 429 (rate limit)
                if 400 <= status < 500 and status != 429:
                    error_body = ""
                    try:
                        error_body = e.read().decode("utf-8")
                    except Exception:
                        pass
                    raise NetworkError(
                        f"Server returned {status}: {error_body}"
                    ) from e

                # Retry on 5xx and 429
                self._stats["retries_total"] += 1
                if attempt < self.max_retries:
                    delay = self.retry_base_delay * (2 ** (attempt - 1))
                    time.sleep(delay)

            except urllib.error.URLError as e:
                last_error = e
                self._stats["retries_total"] += 1

                if attempt < self.max_retries:
                    delay = self.retry_base_delay * (2 ** (attempt - 1))
                    time.sleep(delay)

            except TimeoutError:
                raise

            except Exception as e:
                last_error = e
                self._stats["retries_total"] += 1

                if attempt < self.max_retries:
                    delay = self.retry_base_delay * (2 ** (attempt - 1))
                    time.sleep(delay)

        self._stats["messages_failed"] += 1
        raise NetworkError(
            f"Failed after {self.max_retries} attempts: {last_error}"
        ) from last_error

    @property
    def stats(self) -> Dict[str, Any]:
        """
        Get client statistics.

        Returns:
            Dictionary with message counts, bytes transferred, retry info

        Example:
            >>> print(client.stats)
            {'messages_sent': 5, 'messages_failed': 0, ...}
        """
        return dict(self._stats)

    def reset_stats(self) -> None:
        """Reset all statistics to zero."""
        for key in self._stats:
            self._stats[key] = 0

    def __repr__(self) -> str:
        """Return string representation of client."""
        return (
            f"PulseClient(base_url='{self.base_url}', "
            f"encoding='{self.encoding}', "
            f"secure={'yes' if self.security else 'no'})"
        )
