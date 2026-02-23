"""PULSE Protocol adapter base class.

Adapters bridge PULSE messages to external APIs. Your bot speaks PULSE,
the adapter translates to the target service's native format.

Example:
    >>> from pulse.adapter import PulseAdapter
    >>> class MyAdapter(PulseAdapter):
    ...     def to_native(self, message):
    ...         return {"query": message.content["parameters"]["text"]}
    ...     def call_api(self, native_request):
    ...         return requests.post(self.base_url, json=native_request).json()
    ...     def from_native(self, native_response):
    ...         return PulseMessage(
    ...             action="ACT.RESPOND",
    ...             parameters={"result": native_response}
    ...         )
    >>> adapter = MyAdapter(name="my-service", base_url="https://api.example.com")
    >>> response = adapter.send(request_message)
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone

from pulse.message import PulseMessage
from pulse.exceptions import NetworkError, PulseException


class AdapterError(PulseException):
    """Adapter operation failed."""

    pass


class AdapterConnectionError(AdapterError):
    """Adapter could not connect to the target service."""

    pass


# Standard mapping of common HTTP/API errors to PULSE error codes
ERROR_MAP = {
    400: "META.ERROR.VALIDATION",
    401: "META.ERROR.AUTH",
    403: "META.ERROR.AUTH",
    404: "META.ERROR.NOT_FOUND",
    408: "META.ERROR.TIMEOUT",
    429: "META.ERROR.RATE_LIMIT",
    500: "META.ERROR.INTERNAL",
    502: "META.ERROR.INTERNAL",
    503: "META.ERROR.UNAVAILABLE",
    504: "META.ERROR.TIMEOUT",
}


class PulseAdapter(ABC):
    """Base class for all PULSE adapters.

    An adapter translates PULSE messages to a target service's native API
    and converts responses back to PULSE messages. This enables any bot
    to work with any service through a single interface.

    The adapter lifecycle:
        1. Create adapter with configuration
        2. Optionally call connect() for persistent connections
        3. Call send() with PULSE messages
        4. Optionally call disconnect() to clean up

    Subclasses must implement:
        - to_native(): Convert PULSE message → native API format
        - call_api(): Execute the native API call
        - from_native(): Convert native response → PULSE message

    Attributes:
        name: Human-readable adapter name (e.g., "openai", "binance")
        base_url: Target service base URL
        connected: Whether the adapter has an active connection

    Example:
        >>> adapter = BinanceAdapter(api_key="...", api_secret="...")
        >>> order = PulseMessage(
        ...     action="ACT.TRANSACT.REQUEST",
        ...     parameters={"asset": "BTC/USDT", "side": "BUY", "quantity": 0.1}
        ... )
        >>> result = adapter.send(order)
        >>> print(result.content["parameters"]["status"])
    """

    def __init__(
        self,
        name: str,
        base_url: Optional[str] = None,
        config: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Initialize the adapter.

        Args:
            name: Adapter identifier (e.g., "openai", "binance", "kraken")
            base_url: Target service base URL
            config: Additional configuration (API keys, timeouts, etc.)

        Example:
            >>> adapter = MyAdapter(
            ...     name="binance",
            ...     base_url="https://api.binance.com",
            ...     config={"api_key": "...", "timeout": 30}
            ... )
        """
        self.name = name
        self.base_url = base_url
        self.config = config or {}
        self.connected = False
        self._request_count = 0
        self._error_count = 0
        self._last_request_time: Optional[str] = None

    @abstractmethod
    def to_native(self, message: PulseMessage) -> Any:
        """Convert a PULSE message to the target service's native format.

        This method handles the translation from PULSE semantic concepts
        to the specific API format expected by the target service.

        Args:
            message: PULSE message to convert

        Returns:
            Native request object (dict, string, bytes, etc.)

        Raises:
            AdapterError: If the message cannot be converted

        Example:
            >>> # For a Binance adapter:
            >>> native = adapter.to_native(pulse_message)
            >>> # Returns: {"symbol": "BTCUSDT", "side": "BUY", ...}
        """

    @abstractmethod
    def call_api(self, native_request: Any) -> Any:
        """Execute the native API call to the target service.

        This method sends the translated request to the target service
        and returns the raw response.

        Args:
            native_request: The native request from to_native()

        Returns:
            Native response from the target service

        Raises:
            AdapterConnectionError: If the service is unreachable
            AdapterError: If the API call fails

        Example:
            >>> response = adapter.call_api(native_request)
            >>> # Returns: {"orderId": "12345", "status": "FILLED", ...}
        """

    @abstractmethod
    def from_native(self, native_response: Any) -> PulseMessage:
        """Convert a native API response to a PULSE message.

        This method translates the target service's response format
        back into a standard PULSE message.

        Args:
            native_response: Raw response from call_api()

        Returns:
            PULSE message with the response data

        Raises:
            AdapterError: If the response cannot be converted

        Example:
            >>> pulse_response = adapter.from_native(native_response)
            >>> print(pulse_response.content["parameters"]["result"])
        """

    def send(self, message: PulseMessage) -> PulseMessage:
        """Send a PULSE message through the adapter.

        This is the main method users call. It orchestrates the full
        translation pipeline: PULSE → native → API call → native → PULSE.

        Args:
            message: PULSE message to send

        Returns:
            PULSE response message

        Raises:
            AdapterError: If any step in the pipeline fails
            AdapterConnectionError: If the target service is unreachable

        Example:
            >>> request = PulseMessage(
            ...     action="ACT.QUERY.DATA",
            ...     parameters={"query": "BTC price"}
            ... )
            >>> response = adapter.send(request)
        """
        self._request_count += 1
        self._last_request_time = (
            datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        )

        try:
            native_request = self.to_native(message)
            native_response = self.call_api(native_request)
            response = self.from_native(native_response)

            # Set response envelope fields
            response.type = "RESPONSE"
            response.envelope["receiver"] = message.envelope["sender"]
            response.envelope["sender"] = f"adapter:{self.name}"

            return response

        except (AdapterError, AdapterConnectionError):
            self._error_count += 1
            raise
        except Exception as e:
            self._error_count += 1
            raise AdapterError(
                f"Adapter '{self.name}' failed: {e}"
            ) from e

    def connect(self) -> None:
        """Establish a persistent connection to the target service.

        Override this method if your adapter needs persistent connections
        (WebSockets, connection pools, etc.).

        Raises:
            AdapterConnectionError: If connection fails

        Example:
            >>> adapter.connect()
            >>> # ... send multiple messages ...
            >>> adapter.disconnect()
        """
        self.connected = True

    def disconnect(self) -> None:
        """Close the connection to the target service.

        Override this method to clean up resources.

        Example:
            >>> adapter.disconnect()
        """
        self.connected = False

    def health_check(self) -> Dict[str, Any]:
        """Check adapter health and return status information.

        Returns:
            Dictionary with health status information

        Example:
            >>> status = adapter.health_check()
            >>> print(status["connected"])  # True/False
        """
        return {
            "adapter": self.name,
            "connected": self.connected,
            "base_url": self.base_url,
            "requests": self._request_count,
            "errors": self._error_count,
            "last_request": self._last_request_time,
            "error_rate": (
                self._error_count / self._request_count
                if self._request_count > 0
                else 0.0
            ),
        }

    @staticmethod
    def map_error_code(status_code: int) -> str:
        """Map an HTTP status code to a PULSE error concept.

        Args:
            status_code: HTTP status code (e.g., 400, 401, 500)

        Returns:
            PULSE error concept string

        Example:
            >>> PulseAdapter.map_error_code(429)
            'META.ERROR.RATE_LIMIT'
            >>> PulseAdapter.map_error_code(500)
            'META.ERROR.INTERNAL'
        """
        return ERROR_MAP.get(status_code, "META.ERROR.UNKNOWN")

    def create_error_response(
        self, error_code: str, error_message: str, original: Optional[PulseMessage] = None
    ) -> PulseMessage:
        """Create a standardized PULSE error response.

        Args:
            error_code: PULSE error concept (e.g., "META.ERROR.VALIDATION")
            error_message: Human-readable error description
            original: Original message that caused the error (optional)

        Returns:
            PULSE error message

        Example:
            >>> error = adapter.create_error_response(
            ...     "META.ERROR.RATE_LIMIT",
            ...     "Too many requests, retry after 60 seconds"
            ... )
        """
        error_msg = PulseMessage(
            action=error_code,
            parameters={
                "error": error_message,
                "adapter": self.name,
            },
            sender=f"adapter:{self.name}",
            validate=False,
        )
        error_msg.type = "ERROR"

        if original:
            error_msg.envelope["receiver"] = original.envelope["sender"]
            error_msg.content["parameters"]["in_reply_to"] = original.envelope["message_id"]

        return error_msg

    @property
    def supported_actions(self) -> List[str]:
        """Return list of PULSE actions this adapter supports.

        Override this property to declare which actions your adapter handles.

        Returns:
            List of supported PULSE action concepts

        Example:
            >>> adapter.supported_actions
            ['ACT.QUERY.DATA', 'ACT.ANALYZE.SENTIMENT', 'ACT.CREATE.TEXT']
        """
        return []

    def supports(self, action: str) -> bool:
        """Check if this adapter supports a given PULSE action.

        Args:
            action: PULSE action concept to check

        Returns:
            True if the action is supported

        Example:
            >>> adapter.supports("ACT.QUERY.DATA")
            True
        """
        actions = self.supported_actions
        if not actions:
            return True  # Empty list means all actions accepted
        return action in actions

    def __repr__(self) -> str:
        """Return string representation."""
        return (
            f"PulseAdapter(name='{self.name}', "
            f"url='{self.base_url}', "
            f"connected={self.connected})"
        )
