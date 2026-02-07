"""Tests for PULSE message encoding/decoding."""
import pytest
from pulse import PulseMessage, Encoder, JSONEncoder, BinaryEncoder
from pulse.exceptions import EncodingError, DecodingError


class TestJSONEncoding:
    """Test JSON encoding functionality."""

    def test_json_encode_basic_message(self):
        """Test JSON encoding of basic message."""
        message = PulseMessage(action="ACT.QUERY.DATA")
        encoder = JSONEncoder()

        json_bytes = encoder.encode(message)

        assert isinstance(json_bytes, bytes)
        assert b'"action"' in json_bytes
        assert b'"ACT.QUERY.DATA"' in json_bytes

    def test_json_decode_basic_message(self):
        """Test JSON decoding of basic message."""
        message = PulseMessage(action="ACT.QUERY.DATA")
        encoder = JSONEncoder()

        json_bytes = encoder.encode(message)
        decoded = encoder.decode(json_bytes)

        assert decoded.content["action"] == message.content["action"]

    def test_json_roundtrip(self):
        """Test JSON encoding and decoding roundtrip."""
        message = PulseMessage(
            action="ACT.ANALYZE.SENTIMENT",
            target="ENT.DATA.TEXT",
            parameters={"text": "Hello world", "detail": "high"},
        )
        encoder = JSONEncoder()

        json_bytes = encoder.encode(message)
        decoded = encoder.decode(json_bytes)

        assert decoded.content["action"] == message.content["action"]
        assert decoded.content["object"] == message.content["object"]
        assert decoded.content["parameters"] == message.content["parameters"]
        assert decoded.envelope["sender"] == message.envelope["sender"]


class TestBinaryEncoding:
    """Test binary (MessagePack) encoding functionality."""

    def test_binary_encode_basic_message(self):
        """Test binary encoding of basic message."""
        message = PulseMessage(action="ACT.QUERY.DATA")
        encoder = BinaryEncoder()

        binary = encoder.encode(message)

        assert isinstance(binary, bytes)
        assert len(binary) > 0

    def test_binary_decode_basic_message(self):
        """Test binary decoding of basic message."""
        message = PulseMessage(action="ACT.QUERY.DATA")
        encoder = BinaryEncoder()

        binary = encoder.encode(message)
        decoded = encoder.decode(binary)

        assert decoded.content["action"] == message.content["action"]

    def test_binary_roundtrip(self):
        """Test binary encoding and decoding roundtrip."""
        message = PulseMessage(
            action="ACT.ANALYZE.SENTIMENT",
            target="ENT.DATA.TEXT",
            parameters={"text": "Hello world", "score": 0.95, "confidence": "high"},
        )
        encoder = BinaryEncoder()

        binary = encoder.encode(message)
        decoded = encoder.decode(binary)

        assert decoded.content["action"] == message.content["action"]
        assert decoded.content["object"] == message.content["object"]
        assert decoded.content["parameters"] == message.content["parameters"]

    def test_binary_smaller_than_json(self):
        """Test that binary encoding is smaller than JSON."""
        message = PulseMessage(
            action="ACT.QUERY.DATA",
            target="ENT.RESOURCE.DATABASE",
            parameters={"table": "users", "filters": {"status": "active"}, "limit": 100},
        )

        json_encoder = JSONEncoder()
        binary_encoder = BinaryEncoder()

        json_size = len(json_encoder.encode(message, indent=None))
        binary_size = len(binary_encoder.encode(message))

        assert binary_size < json_size
        reduction = json_size / binary_size
        assert reduction > 1.5  # At least 1.5× reduction

    def test_binary_preserves_types(self):
        """Test that binary encoding preserves data types."""
        message = PulseMessage(
            action="ACT.QUERY.DATA",
            parameters={
                "string": "text",
                "number": 42,
                "float": 3.14,
                "boolean": True,
                "null": None,
                "list": [1, 2, 3],
                "dict": {"key": "value"},
            },
            validate=False,
        )

        encoder = BinaryEncoder()
        binary = encoder.encode(message)
        decoded = encoder.decode(binary)

        params = decoded.content["parameters"]
        assert params["string"] == "text"
        assert params["number"] == 42
        assert params["float"] == 3.14
        assert params["boolean"] is True
        assert params["null"] is None
        assert params["list"] == [1, 2, 3]
        assert params["dict"] == {"key": "value"}


class TestPulseMessageMethods:
    """Test binary encoding methods on PulseMessage class."""

    def test_to_binary_method(self):
        """Test to_binary() method."""
        message = PulseMessage(action="ACT.QUERY.DATA")
        binary = message.to_binary()

        assert isinstance(binary, bytes)
        assert len(binary) > 0

    def test_from_binary_method(self):
        """Test from_binary() class method."""
        message = PulseMessage(action="ACT.QUERY.DATA", target="ENT.DATA.TEXT")
        binary = message.to_binary()

        decoded = PulseMessage.from_binary(binary)

        assert decoded.content["action"] == message.content["action"]
        assert decoded.content["object"] == message.content["object"]

    def test_binary_roundtrip_via_methods(self):
        """Test complete binary roundtrip using message methods."""
        original = PulseMessage(
            action="ACT.CREATE.TEXT",
            target="ENT.DATA.TEXT",
            parameters={"prompt": "Write a story", "max_length": 1000},
        )

        binary = original.to_binary()
        decoded = PulseMessage.from_binary(binary)

        assert decoded.content["action"] == original.content["action"]
        assert decoded.content["object"] == original.content["object"]
        assert decoded.content["parameters"] == original.content["parameters"]
        assert decoded.envelope["message_id"] == original.envelope["message_id"]


class TestUnifiedEncoder:
    """Test unified Encoder class."""

    def test_encode_json_format(self):
        """Test encoding with JSON format."""
        message = PulseMessage(action="ACT.QUERY.DATA")
        encoder = Encoder()

        data = encoder.encode(message, format="json")
        assert isinstance(data, bytes)
        assert b'"action"' in data

    def test_encode_binary_format(self):
        """Test encoding with binary format."""
        message = PulseMessage(action="ACT.QUERY.DATA")
        encoder = Encoder()

        data = encoder.encode(message, format="binary")
        assert isinstance(data, bytes)

    def test_decode_json_auto_detect(self):
        """Test decoding JSON with auto-detection."""
        message = PulseMessage(action="ACT.QUERY.DATA")
        encoder = Encoder()

        json_data = encoder.encode(message, format="json")
        decoded = encoder.decode(json_data)

        assert decoded.content["action"] == message.content["action"]

    def test_decode_binary_auto_detect(self):
        """Test decoding binary with auto-detection."""
        message = PulseMessage(action="ACT.QUERY.DATA")
        encoder = Encoder()

        binary_data = encoder.encode(message, format="binary")
        decoded = encoder.decode(binary_data)

        assert decoded.content["action"] == message.content["action"]

    def test_decode_with_explicit_format(self):
        """Test decoding with explicitly specified format."""
        message = PulseMessage(action="ACT.QUERY.DATA")
        encoder = Encoder()

        binary_data = encoder.encode(message, format="binary")
        decoded = encoder.decode(binary_data, format="binary")

        assert decoded.content["action"] == message.content["action"]

    def test_invalid_format_raises_error(self):
        """Test that invalid format raises error."""
        message = PulseMessage(action="ACT.QUERY.DATA")
        encoder = Encoder()

        with pytest.raises(EncodingError, match="Unknown format"):
            encoder.encode(message, format="invalid")

    def test_get_size_comparison(self):
        """Test size comparison functionality."""
        message = PulseMessage(
            action="ACT.QUERY.DATA",
            target="ENT.RESOURCE.DATABASE",
            parameters={"table": "users", "limit": 100},
        )
        encoder = Encoder()

        comparison = encoder.get_size_comparison(message)

        assert "json" in comparison
        assert "binary" in comparison
        assert "binary_reduction" in comparison
        assert "savings_percent" in comparison

        assert comparison["json"] > comparison["binary"]
        assert comparison["binary_reduction"] > 1.0
        assert 0 < comparison["savings_percent"] < 100


class TestErrorHandling:
    """Test error handling in encoding/decoding."""

    def test_decode_invalid_json(self):
        """Test decoding invalid JSON raises error."""
        encoder = JSONEncoder()
        invalid_json = b"{'invalid': json}"

        with pytest.raises(DecodingError):
            encoder.decode(invalid_json)

    def test_decode_invalid_binary(self):
        """Test decoding invalid binary raises error."""
        encoder = BinaryEncoder()
        invalid_binary = b"\x00\x01\x02\x03"

        with pytest.raises(DecodingError):
            encoder.decode(invalid_binary)

    def test_compact_encoder_not_implemented(self):
        """Test that compact encoder raises not implemented error."""
        from pulse import CompactEncoder

        message = PulseMessage(action="ACT.QUERY.DATA", validate=False)

        with pytest.raises(EncodingError, match="not yet implemented"):
            CompactEncoder.encode(message)

        with pytest.raises(DecodingError, match="not yet implemented"):
            CompactEncoder.decode(b"\x00")


class TestPerformance:
    """Test encoding performance characteristics."""

    def test_binary_encoding_performance(self):
        """Test binary encoding is reasonably fast."""
        import time

        message = PulseMessage(action="ACT.QUERY.DATA", target="ENT.DATA.TEXT")
        encoder = BinaryEncoder()

        start = time.time()
        for _ in range(1000):
            encoder.encode(message)
        duration = time.time() - start

        # Should encode 1000 messages in well under 1 second
        assert duration < 1.0

    def test_binary_decoding_performance(self):
        """Test binary decoding is reasonably fast."""
        import time

        message = PulseMessage(action="ACT.QUERY.DATA", target="ENT.DATA.TEXT")
        encoder = BinaryEncoder()
        binary = encoder.encode(message)

        start = time.time()
        for _ in range(1000):
            encoder.decode(binary)
        duration = time.time() - start

        # Should decode 1000 messages in well under 1 second
        assert duration < 1.0
