"""PULSE Protocol CLI tool.

Command-line interface for creating, validating, signing, and encoding PULSE messages.

Usage:
    pulse create --action ACT.QUERY.DATA --target ENT.DATA.TEXT
    pulse validate message.json
    pulse sign message.json --key my-secret-key
    pulse verify message.json --key my-secret-key
    pulse encode message.json --format binary
    pulse decode message.bin --format binary
"""
import argparse
import sys
import json
from typing import Optional
from pathlib import Path

from pulse import (
    PulseMessage,
    SecurityManager,
    Encoder,
    ValidationError,
    EncodingError,
    DecodingError,
    SecurityError,
)


def create_message_command(args) -> int:
    """Create a new PULSE message.

    Args:
        args: Command arguments

    Returns:
        Exit code (0 for success)
    """
    try:
        # Parse parameters if provided
        parameters = {}
        if args.parameters:
            try:
                parameters = json.loads(args.parameters)
            except json.JSONDecodeError as e:
                print(f"Error: Invalid JSON in parameters: {e}", file=sys.stderr)
                return 1

        # Create message
        message = PulseMessage(
            action=args.action,
            target=args.target,
            parameters=parameters,
            sender=args.sender or "cli-agent",
            validate=not args.no_validate
        )

        # Output
        output = message.to_json(indent=args.indent)

        if args.output:
            Path(args.output).write_text(output, encoding='utf-8')
            print(f"Message created: {args.output}")
        else:
            print(output)

        return 0

    except ValidationError as e:
        print(f"Validation error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def validate_message_command(args) -> int:
    """Validate a PULSE message.

    Args:
        args: Command arguments

    Returns:
        Exit code (0 for success)
    """
    try:
        # Read message
        content = Path(args.file).read_text(encoding='utf-8')
        message = PulseMessage.from_json(content)

        # Validate
        message.validate(check_freshness=args.check_freshness)

        print("✓ Message is valid")
        print(f"  Action: {message.content['action']}")
        print(f"  Type: {message.type}")
        print(f"  Sender: {message.envelope['sender']}")

        return 0

    except ValidationError as e:
        print(f"✗ Validation error: {e}", file=sys.stderr)
        return 1
    except FileNotFoundError:
        print(f"Error: File not found: {args.file}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def sign_message_command(args) -> int:
    """Sign a PULSE message with HMAC-SHA256.

    Args:
        args: Command arguments

    Returns:
        Exit code (0 for success)
    """
    try:
        # Read message
        content = Path(args.file).read_text(encoding='utf-8')
        message = PulseMessage.from_json(content)

        # Sign
        security = SecurityManager(secret_key=args.key)
        signature = security.sign_message(message)

        # Output
        output = message.to_json(indent=args.indent)

        if args.output:
            Path(args.output).write_text(output, encoding='utf-8')
            print(f"✓ Message signed: {args.output}")
        else:
            print(output)

        print(f"  Signature: {signature[:32]}...", file=sys.stderr)

        return 0

    except FileNotFoundError:
        print(f"Error: File not found: {args.file}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def verify_signature_command(args) -> int:
    """Verify PULSE message signature.

    Args:
        args: Command arguments

    Returns:
        Exit code (0 for success, 1 for invalid signature)
    """
    try:
        # Read message
        content = Path(args.file).read_text(encoding='utf-8')
        message = PulseMessage.from_json(content)

        # Verify
        security = SecurityManager(secret_key=args.key)
        is_valid = security.verify_signature(message)

        if is_valid:
            print("✓ Signature is valid")
            print(f"  Action: {message.content['action']}")
            print(f"  Sender: {message.envelope['sender']}")
            return 0
        else:
            print("✗ Signature is invalid (message may be tampered)", file=sys.stderr)
            return 1

    except FileNotFoundError:
        print(f"Error: File not found: {args.file}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def encode_message_command(args) -> int:
    """Encode PULSE message to binary format.

    Args:
        args: Command arguments

    Returns:
        Exit code (0 for success)
    """
    try:
        # Read message
        content = Path(args.file).read_text(encoding='utf-8')
        message = PulseMessage.from_json(content)

        # Encode
        encoder = Encoder()

        if args.format == 'binary':
            encoded = encoder.encode(message, format='binary')
            output_file = args.output or (args.file.rsplit('.', 1)[0] + '.bin')
            Path(output_file).write_bytes(encoded)

            print(f"✓ Encoded to binary: {output_file}")
            print(f"  Size: {len(encoded)} bytes")

        elif args.format == 'json':
            encoded = encoder.encode(message, format='json')
            output_file = args.output or (args.file.rsplit('.', 1)[0] + '.out.json')
            Path(output_file).write_bytes(encoded)

            print(f"✓ Encoded to JSON: {output_file}")
            print(f"  Size: {len(encoded)} bytes")

        # Show size comparison
        if args.compare:
            sizes = encoder.get_size_comparison(message)
            print("\nSize comparison:")
            print(f"  JSON:   {sizes['json']} bytes")
            print(f"  Binary: {sizes['binary']} bytes ({sizes['binary_reduction']}× smaller)")
            print(f"  Savings: {sizes['savings_percent']}%")

        return 0

    except FileNotFoundError:
        print(f"Error: File not found: {args.file}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def decode_message_command(args) -> int:
    """Decode PULSE message from binary format.

    Args:
        args: Command arguments

    Returns:
        Exit code (0 for success)
    """
    try:
        # Read encoded data
        data = Path(args.file).read_bytes()

        # Decode
        encoder = Encoder()

        if args.format:
            message = encoder.decode(data, format=args.format)
        else:
            # Auto-detect
            message = encoder.decode(data)

        # Output
        output = message.to_json(indent=args.indent)

        if args.output:
            Path(args.output).write_text(output, encoding='utf-8')
            print(f"✓ Decoded to: {args.output}")
        else:
            print(output)

        return 0

    except FileNotFoundError:
        print(f"Error: File not found: {args.file}", file=sys.stderr)
        return 1
    except DecodingError as e:
        print(f"Decoding error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog='pulse',
        description='PULSE Protocol CLI - Create, validate, sign, and encode messages',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create a message
  pulse create --action ACT.QUERY.DATA --target ENT.DATA.TEXT -o message.json

  # Validate a message
  pulse validate message.json

  # Sign a message
  pulse sign message.json --key my-secret-key -o signed.json

  # Verify signature
  pulse verify signed.json --key my-secret-key

  # Encode to binary
  pulse encode message.json --format binary -o message.bin

  # Decode from binary
  pulse decode message.bin --format binary -o decoded.json

For more information, visit: https://github.com/pulse-protocol/pulse-python
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Command to execute')

    # Create command
    create_parser = subparsers.add_parser('create', help='Create a new PULSE message')
    create_parser.add_argument('--action', required=True, help='PULSE action concept (e.g., ACT.QUERY.DATA)')
    create_parser.add_argument('--target', help='Target object concept (e.g., ENT.DATA.TEXT)')
    create_parser.add_argument('--parameters', help='JSON string of parameters')
    create_parser.add_argument('--sender', help='Sender agent ID (default: cli-agent)')
    create_parser.add_argument('--no-validate', action='store_true', help='Skip validation')
    create_parser.add_argument('-o', '--output', help='Output file (default: stdout)')
    create_parser.add_argument('--indent', type=int, default=2, help='JSON indentation (default: 2)')

    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Validate a PULSE message')
    validate_parser.add_argument('file', help='Message file to validate')
    validate_parser.add_argument('--check-freshness', action='store_true', help='Check timestamp freshness')

    # Sign command
    sign_parser = subparsers.add_parser('sign', help='Sign a message with HMAC-SHA256')
    sign_parser.add_argument('file', help='Message file to sign')
    sign_parser.add_argument('--key', required=True, help='Secret key for signing')
    sign_parser.add_argument('-o', '--output', help='Output file (default: overwrite input)')
    sign_parser.add_argument('--indent', type=int, default=2, help='JSON indentation (default: 2)')

    # Verify command
    verify_parser = subparsers.add_parser('verify', help='Verify message signature')
    verify_parser.add_argument('file', help='Signed message file')
    verify_parser.add_argument('--key', required=True, help='Secret key for verification')

    # Encode command
    encode_parser = subparsers.add_parser('encode', help='Encode message to binary format')
    encode_parser.add_argument('file', help='Message file to encode')
    encode_parser.add_argument('--format', choices=['binary', 'json'], default='binary', help='Output format')
    encode_parser.add_argument('-o', '--output', help='Output file (default: auto)')
    encode_parser.add_argument('--compare', action='store_true', help='Show size comparison')

    # Decode command
    decode_parser = subparsers.add_parser('decode', help='Decode message from binary')
    decode_parser.add_argument('file', help='Encoded file to decode')
    decode_parser.add_argument('--format', choices=['binary', 'json'], help='Input format (default: auto-detect)')
    decode_parser.add_argument('-o', '--output', help='Output file (default: stdout)')
    decode_parser.add_argument('--indent', type=int, default=2, help='JSON indentation (default: 2)')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    # Route to command handlers
    commands = {
        'create': create_message_command,
        'validate': validate_message_command,
        'sign': sign_message_command,
        'verify': verify_signature_command,
        'encode': encode_message_command,
        'decode': decode_message_command,
    }

    handler = commands.get(args.command)
    if handler:
        return handler(args)
    else:
        print(f"Error: Unknown command: {args.command}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
