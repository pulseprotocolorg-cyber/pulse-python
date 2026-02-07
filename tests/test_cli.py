"""Tests for PULSE CLI tool."""
import pytest
import json
import tempfile
from pathlib import Path
from pulse.cli import (
    create_message_command,
    validate_message_command,
    sign_message_command,
    verify_signature_command,
    encode_message_command,
    decode_message_command,
)
from pulse import PulseMessage


class Args:
    """Mock args object for CLI commands."""
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class TestCreateCommand:
    """Test create command."""

    def test_create_simple_message(self, tmp_path):
        """Test creating a simple message."""
        output_file = tmp_path / "message.json"

        args = Args(
            action="ACT.QUERY.DATA",
            target=None,
            parameters=None,
            sender=None,
            no_validate=True,
            output=str(output_file),
            indent=2
        )

        result = create_message_command(args)

        assert result == 0
        assert output_file.exists()

        # Verify content
        message = PulseMessage.from_json(output_file.read_text())
        assert message.content['action'] == "ACT.QUERY.DATA"

    def test_create_with_parameters(self, tmp_path):
        """Test creating message with parameters."""
        output_file = tmp_path / "message.json"

        args = Args(
            action="ACT.QUERY.DATA",
            target="ENT.DATA.TEXT",
            parameters='{"query": "test", "limit": 10}',
            sender="test-agent",
            no_validate=True,
            output=str(output_file),
            indent=2
        )

        result = create_message_command(args)

        assert result == 0

        message = PulseMessage.from_json(output_file.read_text())
        assert message.content['parameters']['query'] == "test"
        assert message.content['parameters']['limit'] == 10
        assert message.envelope['sender'] == "test-agent"

    def test_create_with_validation(self, tmp_path):
        """Test creating message with validation."""
        output_file = tmp_path / "message.json"

        args = Args(
            action="ACT.QUERY.DATA",
            target="ENT.DATA.TEXT",
            parameters=None,
            sender=None,
            no_validate=False,  # Enable validation
            output=str(output_file),
            indent=2
        )

        result = create_message_command(args)
        assert result == 0

    def test_create_invalid_action(self, tmp_path):
        """Test creating message with invalid action."""
        output_file = tmp_path / "message.json"

        args = Args(
            action="INVALID.ACTION",
            target=None,
            parameters=None,
            sender=None,
            no_validate=False,  # Validation enabled
            output=str(output_file),
            indent=2
        )

        result = create_message_command(args)
        assert result == 1  # Should fail


class TestValidateCommand:
    """Test validate command."""

    def test_validate_valid_message(self, tmp_path):
        """Test validating a valid message."""
        # Create valid message file
        message = PulseMessage(action="ACT.QUERY.DATA", validate=False)
        message_file = tmp_path / "message.json"
        message_file.write_text(message.to_json())

        args = Args(
            file=str(message_file),
            check_freshness=False
        )

        result = validate_message_command(args)
        assert result == 0

    def test_validate_invalid_message(self, tmp_path):
        """Test validating an invalid message."""
        # Create invalid message file
        message = PulseMessage(action="INVALID.ACTION", validate=False)
        message_file = tmp_path / "message.json"
        message_file.write_text(message.to_json())

        args = Args(
            file=str(message_file),
            check_freshness=False
        )

        result = validate_message_command(args)
        assert result == 1  # Should fail

    def test_validate_nonexistent_file(self):
        """Test validating non-existent file."""
        args = Args(
            file="/nonexistent/file.json",
            check_freshness=False
        )

        result = validate_message_command(args)
        assert result == 1


class TestSignCommand:
    """Test sign command."""

    def test_sign_message(self, tmp_path):
        """Test signing a message."""
        # Create message file
        message = PulseMessage(action="ACT.QUERY.DATA", validate=False)
        input_file = tmp_path / "message.json"
        input_file.write_text(message.to_json())

        output_file = tmp_path / "signed.json"

        args = Args(
            file=str(input_file),
            key="test-secret-key",
            output=str(output_file),
            indent=2
        )

        result = sign_message_command(args)
        assert result == 0
        assert output_file.exists()

        # Verify signature exists
        signed_message = PulseMessage.from_json(output_file.read_text())
        assert signed_message.envelope['signature'] is not None

    def test_sign_nonexistent_file(self):
        """Test signing non-existent file."""
        args = Args(
            file="/nonexistent/file.json",
            key="test-key",
            output=None,
            indent=2
        )

        result = sign_message_command(args)
        assert result == 1


class TestVerifyCommand:
    """Test verify command."""

    def test_verify_valid_signature(self, tmp_path):
        """Test verifying valid signature."""
        from pulse import SecurityManager

        # Create and sign message
        message = PulseMessage(action="ACT.QUERY.DATA", validate=False)
        security = SecurityManager(secret_key="test-key")
        security.sign_message(message)

        message_file = tmp_path / "signed.json"
        message_file.write_text(message.to_json())

        args = Args(
            file=str(message_file),
            key="test-key"
        )

        result = verify_signature_command(args)
        assert result == 0  # Valid signature

    def test_verify_invalid_signature(self, tmp_path):
        """Test verifying invalid signature."""
        from pulse import SecurityManager

        # Create and sign with one key, verify with another
        message = PulseMessage(action="ACT.QUERY.DATA", validate=False)
        security1 = SecurityManager(secret_key="key1")
        security1.sign_message(message)

        message_file = tmp_path / "signed.json"
        message_file.write_text(message.to_json())

        args = Args(
            file=str(message_file),
            key="key2"  # Different key
        )

        result = verify_signature_command(args)
        assert result == 1  # Invalid signature


class TestEncodeCommand:
    """Test encode command."""

    def test_encode_to_binary(self, tmp_path):
        """Test encoding to binary."""
        # Create message file
        message = PulseMessage(action="ACT.QUERY.DATA", validate=False)
        input_file = tmp_path / "message.json"
        input_file.write_text(message.to_json())

        output_file = tmp_path / "message.bin"

        args = Args(
            file=str(input_file),
            format="binary",
            output=str(output_file),
            compare=False
        )

        result = encode_message_command(args)
        assert result == 0
        assert output_file.exists()

        # Verify it's binary
        binary_data = output_file.read_bytes()
        assert len(binary_data) > 0
        assert len(binary_data) < len(input_file.read_text())  # Smaller than JSON

    def test_encode_with_comparison(self, tmp_path):
        """Test encoding with size comparison."""
        message = PulseMessage(action="ACT.QUERY.DATA", validate=False)
        input_file = tmp_path / "message.json"
        input_file.write_text(message.to_json())

        args = Args(
            file=str(input_file),
            format="binary",
            output=None,
            compare=True
        )

        result = encode_message_command(args)
        assert result == 0


class TestDecodeCommand:
    """Test decode command."""

    def test_decode_from_binary(self, tmp_path):
        """Test decoding from binary."""
        # Create binary message file
        message = PulseMessage(action="ACT.QUERY.DATA", validate=False)
        binary_file = tmp_path / "message.bin"
        binary_file.write_bytes(message.to_binary())

        output_file = tmp_path / "decoded.json"

        args = Args(
            file=str(binary_file),
            format="binary",
            output=str(output_file),
            indent=2
        )

        result = decode_message_command(args)
        assert result == 0
        assert output_file.exists()

        # Verify decoded message
        decoded = PulseMessage.from_json(output_file.read_text())
        assert decoded.content['action'] == "ACT.QUERY.DATA"

    def test_decode_auto_detect(self, tmp_path):
        """Test decode with auto-detection."""
        message = PulseMessage(action="ACT.QUERY.DATA", validate=False)
        binary_file = tmp_path / "message.bin"
        binary_file.write_bytes(message.to_binary())

        output_file = tmp_path / "decoded.json"

        args = Args(
            file=str(binary_file),
            format=None,  # Auto-detect
            output=str(output_file),
            indent=2
        )

        result = decode_message_command(args)
        assert result == 0


class TestCLIIntegration:
    """Integration tests for CLI commands."""

    def test_full_workflow(self, tmp_path):
        """Test complete CLI workflow: create -> sign -> verify -> encode -> decode."""
        # 1. Create message
        message_file = tmp_path / "message.json"
        args = Args(
            action="ACT.QUERY.DATA",
            target="ENT.DATA.TEXT",
            parameters='{"query": "test"}',
            sender="cli-test",
            no_validate=False,
            output=str(message_file),
            indent=2
        )
        assert create_message_command(args) == 0

        # 2. Sign message
        signed_file = tmp_path / "signed.json"
        args = Args(
            file=str(message_file),
            key="test-key",
            output=str(signed_file),
            indent=2
        )
        assert sign_message_command(args) == 0

        # 3. Verify signature
        args = Args(
            file=str(signed_file),
            key="test-key"
        )
        assert verify_signature_command(args) == 0

        # 4. Encode to binary
        binary_file = tmp_path / "message.bin"
        args = Args(
            file=str(signed_file),
            format="binary",
            output=str(binary_file),
            compare=False
        )
        assert encode_message_command(args) == 0

        # 5. Decode from binary
        decoded_file = tmp_path / "decoded.json"
        args = Args(
            file=str(binary_file),
            format="binary",
            output=str(decoded_file),
            indent=2
        )
        assert decode_message_command(args) == 0

        # Verify final result
        decoded = PulseMessage.from_json(decoded_file.read_text())
        assert decoded.content['action'] == "ACT.QUERY.DATA"
        assert decoded.content['parameters']['query'] == "test"
        assert decoded.envelope['signature'] is not None
