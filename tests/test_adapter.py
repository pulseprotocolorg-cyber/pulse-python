"""Tests for PULSE adapter base class."""
import pytest

from pulse.message import PulseMessage
from pulse.exceptions import PulseException
from pulse.adapter import (
    PulseAdapter,
    AdapterError,
    AdapterConnectionError,
    ERROR_MAP,
)


# --- Test Adapter Implementations ---


class EchoAdapter(PulseAdapter):
    """Simple adapter that echoes messages back. For testing."""

    def to_native(self, message):
        return message.content["parameters"]

    def call_api(self, native_request):
        return {"echo": native_request, "status": "ok"}

    def from_native(self, native_response):
        return PulseMessage(
            action="ACT.RESPOND",
            parameters={"result": native_response},
            validate=False,
        )

    @property
    def supported_actions(self):
        return ["ACT.QUERY.DATA", "ACT.ANALYZE.SENTIMENT"]


class FailingAdapter(PulseAdapter):
    """Adapter that always fails. For testing error handling."""

    def to_native(self, message):
        return {}

    def call_api(self, native_request):
        raise ConnectionError("Service unavailable")

    def from_native(self, native_response):
        return PulseMessage(action="ACT.RESPOND", validate=False)


class ConversionFailAdapter(PulseAdapter):
    """Adapter that fails during to_native. For testing."""

    def to_native(self, message):
        raise AdapterError("Cannot convert this action")

    def call_api(self, native_request):
        return {}

    def from_native(self, native_response):
        return PulseMessage(action="ACT.RESPOND", validate=False)


class ResponseFailAdapter(PulseAdapter):
    """Adapter that fails during from_native. For testing."""

    def to_native(self, message):
        return {}

    def call_api(self, native_request):
        return {"bad": "data"}

    def from_native(self, native_response):
        raise AdapterError("Cannot parse response")


# --- Fixtures ---


@pytest.fixture
def echo_adapter():
    """Create an EchoAdapter for testing."""
    return EchoAdapter(
        name="echo",
        base_url="https://echo.example.com",
        config={"api_key": "test-key"},
    )


@pytest.fixture
def failing_adapter():
    """Create a FailingAdapter for testing."""
    return FailingAdapter(name="failing", base_url="https://fail.example.com")


@pytest.fixture
def sample_message():
    """Create a sample PULSE message."""
    return PulseMessage(
        action="ACT.QUERY.DATA",
        target="ENT.DATA.TEXT",
        parameters={"query": "test data", "limit": 10},
        sender="test-agent",
    )


# --- Test Initialization ---


class TestAdapterInit:
    """Test adapter initialization."""

    def test_basic_init(self, echo_adapter):
        """Test basic adapter creation."""
        assert echo_adapter.name == "echo"
        assert echo_adapter.base_url == "https://echo.example.com"
        assert echo_adapter.config == {"api_key": "test-key"}
        assert echo_adapter.connected is False

    def test_init_defaults(self):
        """Test default values."""
        adapter = EchoAdapter(name="minimal")
        assert adapter.base_url is None
        assert adapter.config == {}
        assert adapter.connected is False
        assert adapter._request_count == 0
        assert adapter._error_count == 0
        assert adapter._last_request_time is None

    def test_repr(self, echo_adapter):
        """Test string representation."""
        repr_str = repr(echo_adapter)
        assert "echo" in repr_str
        assert "echo.example.com" in repr_str
        assert "False" in repr_str  # connected=False


# --- Test Send Pipeline ---


class TestAdapterSend:
    """Test the send pipeline."""

    def test_send_success(self, echo_adapter, sample_message):
        """Test successful send returns PULSE response."""
        response = echo_adapter.send(sample_message)

        assert isinstance(response, PulseMessage)
        assert response.type == "RESPONSE"
        assert response.envelope["receiver"] == "test-agent"
        assert response.envelope["sender"] == "adapter:echo"

    def test_send_preserves_data(self, echo_adapter, sample_message):
        """Test that send preserves request data in response."""
        response = echo_adapter.send(sample_message)

        result = response.content["parameters"]["result"]
        assert result["status"] == "ok"
        assert result["echo"]["query"] == "test data"
        assert result["echo"]["limit"] == 10

    def test_send_increments_counter(self, echo_adapter, sample_message):
        """Test that request counter increments."""
        assert echo_adapter._request_count == 0

        echo_adapter.send(sample_message)
        assert echo_adapter._request_count == 1

        echo_adapter.send(sample_message)
        assert echo_adapter._request_count == 2

    def test_send_sets_last_request_time(self, echo_adapter, sample_message):
        """Test that last request time is set."""
        assert echo_adapter._last_request_time is None

        echo_adapter.send(sample_message)
        assert echo_adapter._last_request_time is not None
        assert echo_adapter._last_request_time.endswith("Z")

    def test_send_failure_increments_error_count(self, failing_adapter, sample_message):
        """Test that errors increment error counter."""
        assert failing_adapter._error_count == 0

        with pytest.raises(AdapterError):
            failing_adapter.send(sample_message)

        assert failing_adapter._error_count == 1
        assert failing_adapter._request_count == 1

    def test_send_wraps_unexpected_errors(self, failing_adapter, sample_message):
        """Test that unexpected errors are wrapped in AdapterError."""
        with pytest.raises(AdapterError, match="Adapter 'failing' failed"):
            failing_adapter.send(sample_message)

    def test_send_conversion_error(self, sample_message):
        """Test error during to_native phase."""
        adapter = ConversionFailAdapter(name="conv-fail")
        with pytest.raises(AdapterError, match="Cannot convert"):
            adapter.send(sample_message)

    def test_send_response_error(self, sample_message):
        """Test error during from_native phase."""
        adapter = ResponseFailAdapter(name="resp-fail")
        with pytest.raises(AdapterError, match="Cannot parse"):
            adapter.send(sample_message)


# --- Test Connection Management ---


class TestAdapterConnection:
    """Test connect/disconnect lifecycle."""

    def test_connect(self, echo_adapter):
        """Test connect sets connected flag."""
        assert echo_adapter.connected is False
        echo_adapter.connect()
        assert echo_adapter.connected is True

    def test_disconnect(self, echo_adapter):
        """Test disconnect clears connected flag."""
        echo_adapter.connect()
        echo_adapter.disconnect()
        assert echo_adapter.connected is False

    def test_context_style_usage(self, echo_adapter, sample_message):
        """Test connect/send/disconnect pattern."""
        echo_adapter.connect()
        response = echo_adapter.send(sample_message)
        echo_adapter.disconnect()

        assert isinstance(response, PulseMessage)
        assert echo_adapter.connected is False


# --- Test Health Check ---


class TestAdapterHealthCheck:
    """Test health check functionality."""

    def test_health_check_initial(self, echo_adapter):
        """Test health check with no requests."""
        status = echo_adapter.health_check()

        assert status["adapter"] == "echo"
        assert status["connected"] is False
        assert status["base_url"] == "https://echo.example.com"
        assert status["requests"] == 0
        assert status["errors"] == 0
        assert status["last_request"] is None
        assert status["error_rate"] == 0.0

    def test_health_check_after_requests(self, echo_adapter, sample_message):
        """Test health check after successful requests."""
        echo_adapter.send(sample_message)
        echo_adapter.send(sample_message)

        status = echo_adapter.health_check()
        assert status["requests"] == 2
        assert status["errors"] == 0
        assert status["error_rate"] == 0.0
        assert status["last_request"] is not None

    def test_health_check_with_errors(self, failing_adapter, sample_message):
        """Test health check after errors."""
        try:
            failing_adapter.send(sample_message)
        except AdapterError:
            pass
        try:
            failing_adapter.send(sample_message)
        except AdapterError:
            pass

        status = failing_adapter.health_check()
        assert status["requests"] == 2
        assert status["errors"] == 2
        assert status["error_rate"] == 1.0


# --- Test Error Mapping ---


class TestErrorMapping:
    """Test error code mapping."""

    def test_map_common_errors(self):
        """Test mapping of common HTTP errors to PULSE codes."""
        assert PulseAdapter.map_error_code(400) == "META.ERROR.VALIDATION"
        assert PulseAdapter.map_error_code(401) == "META.ERROR.AUTH"
        assert PulseAdapter.map_error_code(403) == "META.ERROR.AUTH"
        assert PulseAdapter.map_error_code(404) == "META.ERROR.NOT_FOUND"
        assert PulseAdapter.map_error_code(429) == "META.ERROR.RATE_LIMIT"
        assert PulseAdapter.map_error_code(500) == "META.ERROR.INTERNAL"
        assert PulseAdapter.map_error_code(503) == "META.ERROR.UNAVAILABLE"

    def test_map_unknown_error(self):
        """Test mapping of unknown status code."""
        assert PulseAdapter.map_error_code(418) == "META.ERROR.UNKNOWN"
        assert PulseAdapter.map_error_code(999) == "META.ERROR.UNKNOWN"

    def test_create_error_response(self, echo_adapter):
        """Test creating standardized error response."""
        error = echo_adapter.create_error_response(
            "META.ERROR.RATE_LIMIT",
            "Too many requests",
        )

        assert isinstance(error, PulseMessage)
        assert error.type == "ERROR"
        assert error.content["action"] == "META.ERROR.RATE_LIMIT"
        assert error.content["parameters"]["error"] == "Too many requests"
        assert error.content["parameters"]["adapter"] == "echo"

    def test_create_error_response_with_original(self, echo_adapter, sample_message):
        """Test error response linked to original message."""
        error = echo_adapter.create_error_response(
            "META.ERROR.VALIDATION",
            "Invalid parameters",
            original=sample_message,
        )

        assert error.envelope["receiver"] == "test-agent"
        assert error.content["parameters"]["in_reply_to"] == sample_message.envelope["message_id"]


# --- Test Supported Actions ---


class TestSupportedActions:
    """Test action support checking."""

    def test_supported_actions_list(self, echo_adapter):
        """Test getting supported actions."""
        actions = echo_adapter.supported_actions
        assert "ACT.QUERY.DATA" in actions
        assert "ACT.ANALYZE.SENTIMENT" in actions
        assert len(actions) == 2

    def test_supports_valid_action(self, echo_adapter):
        """Test checking a supported action."""
        assert echo_adapter.supports("ACT.QUERY.DATA") is True
        assert echo_adapter.supports("ACT.ANALYZE.SENTIMENT") is True

    def test_supports_invalid_action(self, echo_adapter):
        """Test checking an unsupported action."""
        assert echo_adapter.supports("ACT.CREATE.TEXT") is False
        assert echo_adapter.supports("INVALID") is False

    def test_supports_all_when_empty(self):
        """Test that empty supported_actions means all accepted."""
        adapter = FailingAdapter(name="all-actions")
        assert adapter.supports("ACT.QUERY.DATA") is True
        assert adapter.supports("ANYTHING") is True


# --- Test Exception Classes ---


class TestAdapterExceptions:
    """Test adapter exception hierarchy."""

    def test_adapter_error_is_pulse_exception(self):
        """Test AdapterError inherits from PulseException."""
        error = AdapterError("test")
        assert isinstance(error, PulseException)

    def test_connection_error_is_adapter_error(self):
        """Test AdapterConnectionError inherits from AdapterError."""
        error = AdapterConnectionError("cannot connect")
        assert isinstance(error, AdapterError)
        assert isinstance(error, PulseException)

    def test_error_message(self):
        """Test error messages are preserved."""
        error = AdapterError("something broke")
        assert str(error) == "something broke"
