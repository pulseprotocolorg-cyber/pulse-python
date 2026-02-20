"""Tests for PULSE Protocol Compact Encoder.

Tests cover:
- Encoding and decoding roundtrip
- Size comparison with JSON and Binary
- Edge cases: empty parameters, unknown concepts
- Format auto-detection
- Error handling
"""
import pytest

from pulse.message import PulseMessage
from pulse.encoder import CompactEncoder, Encoder
from pulse.exceptions import EncodingError, DecodingError


class TestCompactEncoderRoundtrip:
    """Test compact encoding/decoding roundtrip."""

    def test_basic_roundtrip(self):
        """Test basic encode/decode preserves action and type."""
        message = PulseMessage(
            action="ACT.QUERY.DATA",
            target="ENT.DATA.TEXT",
            parameters={"query": "hello"},
        )

        compact = CompactEncoder.encode(message)
        decoded = CompactEncoder.decode(compact)

        assert decoded.content["action"] == "ACT.QUERY.DATA"
        assert decoded.content["object"] == "ENT.DATA.TEXT"
        assert decoded.content["parameters"]["query"] == "hello"
        assert decoded.type == "REQUEST"

    def test_roundtrip_no_target(self):
        """Test roundtrip with no target object."""
        message = PulseMessage(action="ACT.QUERY.DATA")

        compact = CompactEncoder.encode(message)
        decoded = CompactEncoder.decode(compact)

        assert decoded.content["action"] == "ACT.QUERY.DATA"
        assert decoded.content["object"] is None

    def test_roundtrip_no_parameters(self):
        """Test roundtrip with empty parameters."""
        message = PulseMessage(action="ACT.QUERY.DATA")

        compact = CompactEncoder.encode(message)
        decoded = CompactEncoder.decode(compact)

        assert decoded.content["parameters"] == {}

    def test_roundtrip_complex_parameters(self):
        """Test roundtrip with complex nested parameters."""
        params = {
            "query": "test",
            "filters": {"min": 0, "max": 100},
            "tags": ["alpha", "beta"],
            "nested": {"deep": {"value": 42}},
        }
        message = PulseMessage(
            action="ACT.QUERY.DATA",
            parameters=params,
        )

        compact = CompactEncoder.encode(message)
        decoded = CompactEncoder.decode(compact)

        assert decoded.content["parameters"]["query"] == "test"
        assert decoded.content["parameters"]["filters"]["max"] == 100
        assert decoded.content["parameters"]["tags"] == ["alpha", "beta"]
        assert decoded.content["parameters"]["nested"]["deep"]["value"] == 42

    def test_roundtrip_response_type(self):
        """Test roundtrip preserves RESPONSE type."""
        message = PulseMessage(action="ACT.QUERY.DATA")
        message.type = "RESPONSE"

        compact = CompactEncoder.encode(message)
        decoded = CompactEncoder.decode(compact)

        assert decoded.type == "RESPONSE"

    def test_roundtrip_error_type(self):
        """Test roundtrip preserves ERROR type."""
        message = PulseMessage(action="META.ERROR.VALIDATION", validate=False)
        message.type = "ERROR"

        compact = CompactEncoder.encode(message)
        decoded = CompactEncoder.decode(compact)

        assert decoded.type == "ERROR"

    def test_roundtrip_status_type(self):
        """Test roundtrip preserves STATUS type."""
        message = PulseMessage(action="ACT.QUERY.DATA")
        message.type = "STATUS"

        compact = CompactEncoder.encode(message)
        decoded = CompactEncoder.decode(compact)

        assert decoded.type == "STATUS"

    def test_roundtrip_preserves_version(self):
        """Test roundtrip preserves version number."""
        message = PulseMessage(action="ACT.QUERY.DATA")

        compact = CompactEncoder.encode(message)
        decoded = CompactEncoder.decode(compact)

        assert decoded.envelope["version"] == "1.0"

    def test_roundtrip_various_actions(self):
        """Test roundtrip with different vocabulary concepts."""
        actions = [
            "ACT.QUERY.DATA",
            "ACT.ANALYZE.SENTIMENT",
            "ACT.CREATE.TEXT",
            "ACT.TRANSFORM.CONVERT",
        ]

        for action in actions:
            message = PulseMessage(action=action)
            compact = CompactEncoder.encode(message)
            decoded = CompactEncoder.decode(compact)
            assert decoded.content["action"] == action, f"Failed for {action}"


class TestCompactEncoderSize:
    """Test compact encoding size reduction."""

    def test_compact_smaller_than_json(self):
        """Test that compact is smaller than JSON."""
        message = PulseMessage(
            action="ACT.QUERY.DATA",
            target="ENT.DATA.TEXT",
            parameters={"query": "hello"},
        )

        from pulse.encoder import JSONEncoder

        json_data = JSONEncoder.encode(message, indent=None)
        compact_data = CompactEncoder.encode(message)

        assert len(compact_data) < len(json_data)

    def test_compact_smaller_than_binary(self):
        """Test that compact is smaller than binary (MessagePack)."""
        message = PulseMessage(
            action="ACT.QUERY.DATA",
            target="ENT.DATA.TEXT",
        )

        from pulse.encoder import BinaryEncoder

        binary_data = BinaryEncoder.encode(message)
        compact_data = CompactEncoder.encode(message)

        assert len(compact_data) < len(binary_data)

    def test_empty_params_is_30_bytes(self):
        """Test that message with empty params is exactly 30 bytes (header only)."""
        message = PulseMessage(action="ACT.QUERY.DATA")

        compact = CompactEncoder.encode(message)
        assert len(compact) == 30

    def test_size_comparison_via_encoder(self):
        """Test size comparison through unified Encoder."""
        message = PulseMessage(
            action="ACT.QUERY.DATA",
            target="ENT.DATA.TEXT",
            parameters={"query": "test"},
        )

        encoder = Encoder()
        sizes = encoder.get_size_comparison(message)

        assert "compact" in sizes
        assert "compact_reduction" in sizes
        assert sizes["compact"] < sizes["json"]
        assert sizes["compact"] < sizes["binary"]
        assert sizes["compact_reduction"] > sizes["binary_reduction"]


class TestCompactEncoderFormat:
    """Test compact encoder format details."""

    def test_magic_byte(self):
        """Test that compact data starts with magic byte."""
        message = PulseMessage(action="ACT.QUERY.DATA")
        compact = CompactEncoder.encode(message)

        assert compact[0] == 0xAE

    def test_auto_detect_compact(self):
        """Test that Encoder auto-detects compact format."""
        message = PulseMessage(action="ACT.QUERY.DATA")
        compact = CompactEncoder.encode(message)

        encoder = Encoder()
        decoded = encoder.decode(compact)

        assert decoded.content["action"] == "ACT.QUERY.DATA"

    def test_explicit_compact_decode(self):
        """Test explicit compact format decoding via Encoder."""
        message = PulseMessage(action="ACT.QUERY.DATA")
        compact = CompactEncoder.encode(message)

        encoder = Encoder()
        decoded = encoder.decode(compact, format="compact")

        assert decoded.content["action"] == "ACT.QUERY.DATA"

    def test_encode_via_unified_encoder(self):
        """Test encoding via unified Encoder with compact format."""
        message = PulseMessage(action="ACT.QUERY.DATA")

        encoder = Encoder()
        compact = encoder.encode(message, format="compact")

        assert compact[0] == 0xAE

        decoded = encoder.decode(compact)
        assert decoded.content["action"] == "ACT.QUERY.DATA"


class TestCompactEncoderErrors:
    """Test compact encoder error handling."""

    def test_decode_too_short(self):
        """Test decoding data that is too short."""
        with pytest.raises(DecodingError, match="too short"):
            CompactEncoder.decode(b"\xAE" * 10)

    def test_decode_wrong_magic(self):
        """Test decoding data with wrong magic byte."""
        with pytest.raises(DecodingError, match="Invalid magic byte"):
            CompactEncoder.decode(b"\xFF" * 30)

    def test_decode_empty(self):
        """Test decoding empty data."""
        with pytest.raises(DecodingError):
            CompactEncoder.decode(b"")


class TestCompactEncoderHelpers:
    """Test compact encoder helper methods."""

    def test_fnv1a_deterministic(self):
        """Test FNV-1a hash is deterministic."""
        h1 = CompactEncoder._fnv1a_32("test-agent")
        h2 = CompactEncoder._fnv1a_32("test-agent")
        assert h1 == h2

    def test_fnv1a_different_inputs(self):
        """Test FNV-1a produces different hashes for different inputs."""
        h1 = CompactEncoder._fnv1a_32("agent-001")
        h2 = CompactEncoder._fnv1a_32("agent-002")
        assert h1 != h2

    def test_timestamp_roundtrip(self):
        """Test timestamp conversion roundtrip."""
        original = "2026-02-20T12:00:00Z"
        micros = CompactEncoder._timestamp_to_micros(original)
        restored = CompactEncoder._micros_to_timestamp(micros)

        # Should match to the second (microsecond rounding may differ)
        assert restored.startswith("2026-02-20T12:00:00")
