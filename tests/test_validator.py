"""Tests for PULSE message validation."""
import pytest
from datetime import datetime, timezone, timedelta
from pulse.message import PulseMessage
from pulse.validator import MessageValidator
from pulse.exceptions import ValidationError


class TestEnvelopeValidation:
    """Test envelope validation."""

    def test_valid_envelope_passes(self):
        """Test valid envelope passes validation."""
        message = PulseMessage(action="ACT.QUERY.DATA")
        assert MessageValidator.validate_envelope(message.envelope) is True

    def test_missing_version_fails(self):
        """Test missing version field fails."""
        envelope = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "sender": "test",
            "receiver": None,
            "message_id": "123",
            "nonce": "456",
        }
        with pytest.raises(ValidationError, match="Missing required envelope field: version"):
            MessageValidator.validate_envelope(envelope)

    def test_missing_timestamp_fails(self):
        """Test missing timestamp fails."""
        envelope = {
            "version": "1.0",
            "sender": "test",
            "receiver": None,
            "message_id": "123",
            "nonce": "456",
        }
        with pytest.raises(ValidationError, match="Missing required envelope field: timestamp"):
            MessageValidator.validate_envelope(envelope)

    def test_invalid_version_fails(self):
        """Test invalid version number fails."""
        message = PulseMessage(action="ACT.QUERY.DATA", validate=False)
        message.envelope["version"] = "2.0"
        with pytest.raises(ValidationError, match="Unsupported protocol version"):
            MessageValidator.validate_envelope(message.envelope)

    def test_invalid_timestamp_format_fails(self):
        """Test invalid timestamp format fails."""
        message = PulseMessage(action="ACT.QUERY.DATA", validate=False)
        message.envelope["timestamp"] = "not-a-timestamp"
        with pytest.raises(ValidationError, match="Invalid timestamp format"):
            MessageValidator.validate_envelope(message.envelope)

    def test_empty_message_id_fails(self):
        """Test empty message ID fails."""
        message = PulseMessage(action="ACT.QUERY.DATA", validate=False)
        message.envelope["message_id"] = ""
        with pytest.raises(ValidationError, match="Message ID cannot be empty"):
            MessageValidator.validate_envelope(message.envelope)

    def test_empty_sender_fails(self):
        """Test empty sender fails."""
        message = PulseMessage(action="ACT.QUERY.DATA", validate=False)
        message.envelope["sender"] = ""
        with pytest.raises(ValidationError, match="Sender ID cannot be empty"):
            MessageValidator.validate_envelope(message.envelope)


class TestContentValidation:
    """Test content validation."""

    def test_valid_content_passes(self):
        """Test valid content passes validation."""
        message = PulseMessage(action="ACT.QUERY.DATA")
        assert MessageValidator.validate_content(message.content) is True

    def test_missing_action_fails(self):
        """Test missing action fails."""
        content = {"parameters": {}}
        with pytest.raises(ValidationError, match="Missing required field 'action'"):
            MessageValidator.validate_content(content)

    def test_empty_action_fails(self):
        """Test empty action fails."""
        content = {"action": ""}
        with pytest.raises(ValidationError, match="Action cannot be empty"):
            MessageValidator.validate_content(content)

    def test_invalid_action_concept_fails(self):
        """Test invalid action concept fails."""
        content = {"action": "INVALID.CONCEPT"}
        with pytest.raises(ValidationError, match="Invalid action concept"):
            MessageValidator.validate_content(content)

    def test_invalid_action_with_suggestions(self):
        """Test invalid action provides suggestions."""
        content = {"action": "ACT.QUERY.INVALID"}
        with pytest.raises(ValidationError, match="Did you mean"):
            MessageValidator.validate_content(content)

    def test_invalid_object_concept_fails(self):
        """Test invalid object concept fails."""
        content = {"action": "ACT.QUERY.DATA", "object": "INVALID.OBJECT"}
        with pytest.raises(ValidationError, match="Invalid object concept"):
            MessageValidator.validate_content(content)

    def test_empty_object_string_fails(self):
        """Test empty object string fails."""
        content = {"action": "ACT.QUERY.DATA", "object": "   "}
        with pytest.raises(ValidationError, match="Object cannot be empty"):
            MessageValidator.validate_content(content)

    def test_parameters_not_dict_fails(self):
        """Test non-dict parameters fails."""
        content = {"action": "ACT.QUERY.DATA", "parameters": "not a dict"}
        with pytest.raises(ValidationError, match="Parameters must be a dictionary"):
            MessageValidator.validate_content(content)

    def test_valid_object_none_passes(self):
        """Test None object is valid."""
        content = {"action": "ACT.QUERY.DATA", "object": None}
        assert MessageValidator.validate_content(content) is True


class TestTimestampValidation:
    """Test timestamp freshness validation."""

    def test_current_timestamp_passes(self):
        """Test current timestamp passes validation."""
        timestamp = datetime.now(timezone.utc).isoformat() + "Z"
        assert MessageValidator.validate_timestamp_freshness(timestamp) is True

    def test_old_timestamp_fails(self):
        """Test old timestamp fails validation."""
        old_time = datetime.now(timezone.utc) - timedelta(minutes=10)
        timestamp = old_time.isoformat() + "Z"
        with pytest.raises(ValidationError, match="Message too old"):
            MessageValidator.validate_timestamp_freshness(timestamp, max_age_seconds=300)

    def test_future_timestamp_fails(self):
        """Test future timestamp fails validation."""
        future_time = datetime.now(timezone.utc) + timedelta(minutes=5)
        timestamp = future_time.isoformat() + "Z"
        with pytest.raises(ValidationError, match="timestamp in future"):
            MessageValidator.validate_timestamp_freshness(timestamp)

    def test_minor_clock_skew_allowed(self):
        """Test minor clock skew is allowed."""
        # 30 seconds in future should be OK (within 60 second tolerance)
        future_time = datetime.now(timezone.utc) + timedelta(seconds=30)
        timestamp = future_time.isoformat() + "Z"
        assert MessageValidator.validate_timestamp_freshness(timestamp) is True

    def test_custom_max_age(self):
        """Test custom max age parameter."""
        old_time = datetime.now(timezone.utc) - timedelta(seconds=90)
        timestamp = old_time.isoformat() + "Z"

        # Should fail with default 300 second max
        with pytest.raises(ValidationError):
            MessageValidator.validate_timestamp_freshness(timestamp, max_age_seconds=60)

        # Should pass with 120 second max
        assert MessageValidator.validate_timestamp_freshness(timestamp, max_age_seconds=120) is True


class TestFullMessageValidation:
    """Test complete message validation."""

    def test_valid_message_passes(self):
        """Test valid message passes all validation."""
        message = PulseMessage(action="ACT.QUERY.DATA", target="ENT.DATA.TEXT")
        assert MessageValidator.validate_message(message, check_freshness=False) is True

    def test_validation_on_creation(self):
        """Test validation runs on message creation by default."""
        # Should not raise
        message = PulseMessage(action="ACT.QUERY.DATA")
        assert message is not None

    def test_invalid_action_on_creation_fails(self):
        """Test invalid action on creation fails."""
        with pytest.raises(ValidationError):
            PulseMessage(action="INVALID.ACTION")

    def test_can_skip_validation_on_creation(self):
        """Test can skip validation on creation."""
        # Should not raise even with invalid action
        message = PulseMessage(action="INVALID.ACTION", validate=False)
        assert message is not None

    def test_manual_validation_catches_errors(self):
        """Test manual validation catches errors."""
        message = PulseMessage(action="ACT.QUERY.DATA", validate=False)
        message.content["action"] = "INVALID.ACTION"

        with pytest.raises(ValidationError):
            message.validate()

    def test_freshness_check_optional(self):
        """Test freshness check can be disabled."""
        message = PulseMessage(action="ACT.QUERY.DATA")
        # Mess up the timestamp
        old_time = datetime.now(timezone.utc) - timedelta(hours=1)
        message.envelope["timestamp"] = old_time.isoformat() + "Z"

        # Should pass without freshness check
        assert MessageValidator.validate_message(message, check_freshness=False) is True

        # Should fail with freshness check
        with pytest.raises(ValidationError):
            MessageValidator.validate_message(message, check_freshness=True)


class TestMessageTypeValidation:
    """Test message type validation."""

    def test_valid_request_type(self):
        """Test REQUEST type is valid."""
        assert MessageValidator.validate_message_type("REQUEST") is True

    def test_valid_response_type(self):
        """Test RESPONSE type is valid."""
        assert MessageValidator.validate_message_type("RESPONSE") is True

    def test_valid_error_type(self):
        """Test ERROR type is valid."""
        assert MessageValidator.validate_message_type("ERROR") is True

    def test_valid_status_type(self):
        """Test STATUS type is valid."""
        assert MessageValidator.validate_message_type("STATUS") is True

    def test_invalid_type_fails(self):
        """Test invalid message type fails."""
        with pytest.raises(ValidationError, match="Invalid message type"):
            MessageValidator.validate_message_type("INVALID")

    def test_lowercase_type_fails(self):
        """Test lowercase type fails."""
        with pytest.raises(ValidationError):
            MessageValidator.validate_message_type("request")
