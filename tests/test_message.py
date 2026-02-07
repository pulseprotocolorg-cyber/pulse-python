"""Tests for PULSE message core functionality."""
import pytest
import json
from datetime import datetime


class TestMessageCreation:
    """Test basic message creation functionality."""

    def test_create_simple_message(self, sample_action):
        """Test creating a simple message with just an action."""
        from pulse.message import PulseMessage

        message = PulseMessage(action=sample_action)

        assert message.content["action"] == sample_action
        assert message.type == "REQUEST"
        assert "envelope" in dir(message)

    def test_create_message_with_target(self, sample_action, sample_target):
        """Test creating a message with action and target."""
        from pulse.message import PulseMessage

        message = PulseMessage(action=sample_action, target=sample_target)

        assert message.content["action"] == sample_action
        assert message.content["object"] == sample_target

    def test_create_message_with_parameters(self, sample_action, sample_parameters):
        """Test creating a message with parameters."""
        from pulse.message import PulseMessage

        message = PulseMessage(action=sample_action, parameters=sample_parameters)

        assert message.content["parameters"] == sample_parameters

    def test_create_message_with_custom_sender(self, sample_action):
        """Test creating a message with custom sender."""
        from pulse.message import PulseMessage

        sender_id = "test-agent-001"
        message = PulseMessage(action=sample_action, sender=sender_id)

        assert message.envelope["sender"] == sender_id

    def test_envelope_has_required_fields(self, sample_action):
        """Test that envelope contains all required fields."""
        from pulse.message import PulseMessage

        message = PulseMessage(action=sample_action)

        required_fields = ["version", "timestamp", "sender", "receiver", "message_id", "nonce"]
        for field in required_fields:
            assert field in message.envelope, f"Missing required field: {field}"

    def test_envelope_version_is_correct(self, sample_action):
        """Test that envelope version is 1.0."""
        from pulse.message import PulseMessage

        message = PulseMessage(action=sample_action)

        assert message.envelope["version"] == "1.0"

    def test_message_id_is_unique(self, sample_action):
        """Test that each message gets a unique message_id."""
        from pulse.message import PulseMessage

        message1 = PulseMessage(action=sample_action)
        message2 = PulseMessage(action=sample_action)

        assert message1.envelope["message_id"] != message2.envelope["message_id"]

    def test_timestamp_is_iso_format(self, sample_action):
        """Test that timestamp is in ISO format."""
        from pulse.message import PulseMessage

        message = PulseMessage(action=sample_action)
        timestamp = message.envelope["timestamp"]

        # Should end with Z (UTC timezone indicator)
        assert timestamp.endswith("Z")

        # Should be parseable as ISO format
        timestamp_clean = timestamp.rstrip("Z")
        parsed_time = datetime.fromisoformat(timestamp_clean)
        assert isinstance(parsed_time, datetime)


class TestJSONSerialization:
    """Test JSON encoding and decoding."""

    def test_to_json_returns_string(self, sample_action):
        """Test that to_json() returns a string."""
        from pulse.message import PulseMessage

        message = PulseMessage(action=sample_action)
        json_str = message.to_json()

        assert isinstance(json_str, str)

    def test_to_json_is_valid_json(self, sample_action):
        """Test that to_json() produces valid JSON."""
        from pulse.message import PulseMessage

        message = PulseMessage(action=sample_action)
        json_str = message.to_json()

        # Should not raise exception
        parsed = json.loads(json_str)
        assert isinstance(parsed, dict)

    def test_json_contains_envelope(self, sample_action):
        """Test that JSON output contains envelope."""
        from pulse.message import PulseMessage

        message = PulseMessage(action=sample_action)
        json_str = message.to_json()

        assert "envelope" in json_str
        parsed = json.loads(json_str)
        assert "envelope" in parsed

    def test_json_contains_type(self, sample_action):
        """Test that JSON output contains type."""
        from pulse.message import PulseMessage

        message = PulseMessage(action=sample_action)
        json_str = message.to_json()

        assert "type" in json_str
        parsed = json.loads(json_str)
        assert "type" in parsed

    def test_json_contains_content(self, sample_action):
        """Test that JSON output contains content."""
        from pulse.message import PulseMessage

        message = PulseMessage(action=sample_action)
        json_str = message.to_json()

        assert "content" in json_str
        parsed = json.loads(json_str)
        assert "content" in parsed

    def test_from_json_recreates_message(self, sample_action, sample_target):
        """Test that from_json() can recreate a message."""
        from pulse.message import PulseMessage

        original = PulseMessage(action=sample_action, target=sample_target)
        json_str = original.to_json()

        recreated = PulseMessage.from_json(json_str)

        assert recreated.content["action"] == original.content["action"]
        assert recreated.content["object"] == original.content["object"]

    def test_json_roundtrip_preserves_data(self, sample_action, sample_target, sample_parameters):
        """Test that JSON roundtrip preserves all data."""
        from pulse.message import PulseMessage

        original = PulseMessage(
            action=sample_action, target=sample_target, parameters=sample_parameters
        )
        json_str = original.to_json()
        recreated = PulseMessage.from_json(json_str)

        # Check content
        assert recreated.content["action"] == original.content["action"]
        assert recreated.content["object"] == original.content["object"]
        assert recreated.content["parameters"] == original.content["parameters"]

        # Check envelope
        assert recreated.envelope["message_id"] == original.envelope["message_id"]
        assert recreated.envelope["sender"] == original.envelope["sender"]

        # Check type
        assert recreated.type == original.type

    def test_to_dict_returns_dict(self, sample_action):
        """Test that to_dict() returns a dictionary."""
        from pulse.message import PulseMessage

        message = PulseMessage(action=sample_action)
        data = message.to_dict()

        assert isinstance(data, dict)
        assert "envelope" in data
        assert "type" in data
        assert "content" in data
