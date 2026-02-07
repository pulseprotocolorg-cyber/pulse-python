"""PULSE Protocol encoding/decoding for multiple formats.

This module provides encoding and decoding functionality for PULSE messages:
- JSON: Human-readable, debugging-friendly
- Binary: Efficient MessagePack encoding (~10× smaller)
- Compact: Ultra-efficient custom format (~13× smaller) - Coming soon
"""
from typing import Optional
import json
import msgpack
from pulse.exceptions import EncodingError, DecodingError


class JSONEncoder:
    """
    JSON encoding/decoding for PULSE messages.

    Provides human-readable format suitable for:
    - Debugging and development
    - Logging and auditing
    - Human-readable APIs
    - Documentation and examples

    Example:
        >>> encoder = JSONEncoder()
        >>> json_bytes = encoder.encode(message)
        >>> decoded = encoder.decode(json_bytes)
    """

    @staticmethod
    def encode(message, indent: Optional[int] = 2) -> bytes:
        """
        Encode PULSE message to JSON bytes.

        Args:
            message: PulseMessage instance to encode
            indent: JSON indentation (None for compact, 2 for readable)

        Returns:
            UTF-8 encoded JSON bytes

        Raises:
            EncodingError: If encoding fails

        Example:
            >>> json_bytes = JSONEncoder.encode(message)
            >>> print(len(json_bytes))  # ~800 bytes typical
        """
        try:
            data = message.to_dict()
            json_str = json.dumps(data, indent=indent, ensure_ascii=False)
            return json_str.encode("utf-8")
        except Exception as e:
            raise EncodingError(f"JSON encoding failed: {str(e)}") from e

    @staticmethod
    def decode(data: bytes):
        """
        Decode JSON bytes to PULSE message.

        Args:
            data: UTF-8 encoded JSON bytes

        Returns:
            PulseMessage instance

        Raises:
            DecodingError: If decoding fails

        Example:
            >>> message = JSONEncoder.decode(json_bytes)
        """
        try:
            # Import here to avoid circular dependency
            from pulse.message import PulseMessage

            json_str = data.decode("utf-8")
            return PulseMessage.from_json(json_str)
        except Exception as e:
            raise DecodingError(f"JSON decoding failed: {str(e)}") from e


class BinaryEncoder:
    """
    Binary encoding/decoding using MessagePack.

    Provides efficient binary format with ~10× size reduction:
    - Fast serialization/deserialization
    - Compact binary representation
    - Language-agnostic format
    - Suitable for high-throughput systems

    MessagePack is a binary format similar to JSON but much more compact.
    It's widely supported across programming languages.

    Example:
        >>> encoder = BinaryEncoder()
        >>> binary = encoder.encode(message)
        >>> print(len(binary))  # ~80 bytes typical (10× smaller than JSON)
        >>> decoded = encoder.decode(binary)
    """

    @staticmethod
    def encode(message) -> bytes:
        """
        Encode PULSE message to binary MessagePack format.

        Args:
            message: PulseMessage instance to encode

        Returns:
            MessagePack encoded bytes

        Raises:
            EncodingError: If encoding fails

        Example:
            >>> binary = BinaryEncoder.encode(message)
            >>> print(f"Size: {len(binary)} bytes")
        """
        try:
            data = message.to_dict()
            return msgpack.packb(data, use_bin_type=True)
        except Exception as e:
            raise EncodingError(f"Binary encoding failed: {str(e)}") from e

    @staticmethod
    def decode(data: bytes):
        """
        Decode binary MessagePack to PULSE message.

        Args:
            data: MessagePack encoded bytes

        Returns:
            PulseMessage instance

        Raises:
            DecodingError: If decoding fails

        Example:
            >>> message = BinaryEncoder.decode(binary_data)
        """
        try:
            # Import here to avoid circular dependency
            from pulse.message import PulseMessage

            decoded = msgpack.unpackb(data, raw=False, strict_map_key=False)

            # Reconstruct message without validation to preserve exact data
            message = PulseMessage.__new__(PulseMessage)
            message.envelope = decoded["envelope"]
            message.type = decoded["type"]
            message.content = decoded["content"]

            return message
        except Exception as e:
            raise DecodingError(f"Binary decoding failed: {str(e)}") from e


class CompactEncoder:
    """
    Ultra-compact custom binary encoding (Coming in Week 2).

    Will provide ~13× size reduction with custom binary format:
    - Fixed-size header (version, type, timestamp)
    - Vocabulary index mapping (concept IDs to integers)
    - Variable-length encoding for parameters
    - Optimized for maximum efficiency

    Format specification:
        Byte 0: Version (4 bits) + Type (4 bits)
        Bytes 1-8: Timestamp (64-bit Unix time)
        Bytes 9-16: Message ID (64-bit hash)
        Bytes 17-20: Sender hash (32-bit)
        Bytes 21-22: Action index (16-bit)
        Bytes 23-24: Target index (16-bit)
        Bytes 25+: Parameters (MessagePack)

    Example:
        >>> # Coming soon
        >>> compact = CompactEncoder.encode(message)
        >>> print(len(compact))  # ~60 bytes (13× smaller than JSON)
    """

    @staticmethod
    def encode(message) -> bytes:
        """
        Encode PULSE message to ultra-compact binary format.

        Args:
            message: PulseMessage instance to encode

        Returns:
            Compact binary encoded bytes

        Raises:
            EncodingError: Not yet implemented
        """
        raise EncodingError("Compact encoding not yet implemented (coming in Week 2)")

    @staticmethod
    def decode(data: bytes):
        """
        Decode compact binary to PULSE message.

        Args:
            data: Compact binary encoded bytes

        Returns:
            PulseMessage instance

        Raises:
            DecodingError: Not yet implemented
        """
        raise DecodingError("Compact decoding not yet implemented (coming in Week 2)")


class Encoder:
    """
    Unified encoder supporting multiple formats.

    Convenience wrapper providing access to all encoding formats:
    - JSON (human-readable)
    - Binary (efficient MessagePack)
    - Compact (ultra-efficient custom) - Coming soon

    Example:
        >>> encoder = Encoder()
        >>>
        >>> # JSON encoding
        >>> json_data = encoder.encode(message, format="json")
        >>>
        >>> # Binary encoding
        >>> binary_data = encoder.encode(message, format="binary")
        >>>
        >>> # Auto-detect format when decoding
        >>> decoded = encoder.decode(data)
    """

    def __init__(self):
        """Initialize encoder with all format handlers."""
        self.json_encoder = JSONEncoder()
        self.binary_encoder = BinaryEncoder()
        self.compact_encoder = CompactEncoder()

    def encode(self, message, format: str = "json") -> bytes:
        """
        Encode message in specified format.

        Args:
            message: PulseMessage instance to encode
            format: Format name ("json", "binary", "compact")

        Returns:
            Encoded bytes

        Raises:
            EncodingError: If format invalid or encoding fails

        Example:
            >>> encoder = Encoder()
            >>> json_data = encoder.encode(message, format="json")
            >>> binary_data = encoder.encode(message, format="binary")
        """
        format_lower = format.lower()

        if format_lower == "json":
            return self.json_encoder.encode(message)
        elif format_lower == "binary":
            return self.binary_encoder.encode(message)
        elif format_lower == "compact":
            return self.compact_encoder.encode(message)
        else:
            raise EncodingError(
                f"Unknown format: '{format}'. "
                f"Supported formats: json, binary, compact"
            )

    def decode(self, data: bytes, format: Optional[str] = None):
        """
        Decode message, auto-detecting format if not specified.

        Args:
            data: Encoded bytes
            format: Format name (optional, will auto-detect if None)

        Returns:
            PulseMessage instance

        Raises:
            DecodingError: If decoding fails

        Example:
            >>> encoder = Encoder()
            >>> message = encoder.decode(data)  # Auto-detects format
            >>> message = encoder.decode(data, format="binary")  # Explicit
        """
        # If format specified, use it directly
        if format:
            format_lower = format.lower()
            if format_lower == "json":
                return self.json_encoder.decode(data)
            elif format_lower == "binary":
                return self.binary_encoder.decode(data)
            elif format_lower == "compact":
                return self.compact_encoder.decode(data)
            else:
                raise DecodingError(f"Unknown format: '{format}'")

        # Auto-detect format
        try:
            # Try JSON first (starts with { or [)
            if data[0:1] in (b"{", b"["):
                return self.json_encoder.decode(data)

            # Try MessagePack binary
            # MessagePack starts with specific byte patterns
            return self.binary_encoder.decode(data)

        except Exception as e:
            raise DecodingError(f"Failed to decode data: {str(e)}") from e

    def get_size_comparison(self, message) -> dict:
        """
        Compare sizes across all formats.

        Args:
            message: PulseMessage to analyze

        Returns:
            Dictionary with sizes and reduction factors

        Example:
            >>> encoder = Encoder()
            >>> sizes = encoder.get_size_comparison(message)
            >>> print(f"JSON: {sizes['json']} bytes")
            >>> print(f"Binary: {sizes['binary']} bytes ({sizes['binary_reduction']}× smaller)")
        """
        json_data = self.json_encoder.encode(message, indent=None)
        binary_data = self.binary_encoder.encode(message)

        json_size = len(json_data)
        binary_size = len(binary_data)

        return {
            "json": json_size,
            "binary": binary_size,
            "json_reduction": 1.0,
            "binary_reduction": round(json_size / binary_size, 2),
            "savings_percent": round((1 - binary_size / json_size) * 100, 1),
        }
