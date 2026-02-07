"""
PULSE Protocol - CLI Usage Examples.

This example demonstrates:
1. Using the PULSE CLI tool
2. Creating messages from command line
3. Validating, signing, and encoding messages
4. CLI workflow integration
5. Programmatic CLI usage
"""
import subprocess
import tempfile
import os
from pathlib import Path

# Note: These examples show CLI commands. To run them, you need to:
# 1. Install the package: pip install -e .
# 2. Run commands from terminal


def print_header(title):
    """Print section header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")


def demo_cli_help():
    """Show CLI help."""
    print_header("1. CLI Help")

    print("To see all available commands:\n")
    print("  $ pulse --help\n")

    print("To see help for a specific command:\n")
    print("  $ pulse create --help")
    print("  $ pulse sign --help")
    print("  $ pulse verify --help")
    print()


def demo_create_message():
    """Demonstrate creating messages with CLI."""
    print_header("2. Creating Messages")

    print("Create a simple message:\n")
    print("  $ pulse create --action ACT.QUERY.DATA -o message.json\n")

    print("Create a message with parameters:\n")
    print('  $ pulse create --action ACT.QUERY.DATA \\')
    print('      --target ENT.DATA.TEXT \\')
    print('      --parameters \'{"query": "test", "limit": 10}\' \\')
    print('      -o message.json\n')

    print("Create without validation (for custom actions):\n")
    print("  $ pulse create --action CUSTOM.ACTION --no-validate -o message.json\n")


def demo_validate_message():
    """Demonstrate validating messages."""
    print_header("3. Validating Messages")

    print("Validate a message file:\n")
    print("  $ pulse validate message.json\n")

    print("Validate with freshness check:\n")
    print("  $ pulse validate message.json --check-freshness\n")

    print("Example output:")
    print("  ✓ Message is valid")
    print("    Action: ACT.QUERY.DATA")
    print("    Type: REQUEST")
    print("    Sender: default-agent")
    print()


def demo_sign_verify():
    """Demonstrate signing and verifying messages."""
    print_header("4. Signing and Verifying")

    print("Sign a message:\n")
    print("  $ pulse sign message.json --key my-secret-key -o signed.json\n")

    print("Verify signature:\n")
    print("  $ pulse verify signed.json --key my-secret-key\n")

    print("Example output:")
    print("  ✓ Signature is valid")
    print("    Action: ACT.QUERY.DATA")
    print("    Sender: default-agent")
    print()

    print("If signature is invalid:")
    print("  ✗ Signature is invalid (message may be tampered)")
    print()


def demo_encode_decode():
    """Demonstrate encoding and decoding."""
    print_header("5. Encoding and Decoding")

    print("Encode to binary:\n")
    print("  $ pulse encode message.json --format binary -o message.bin\n")

    print("Encode with size comparison:\n")
    print("  $ pulse encode message.json --format binary --compare\n")

    print("Example output:")
    print("  ✓ Encoded to binary: message.bin")
    print("    Size: 89 bytes\n")
    print("  Size comparison:")
    print("    JSON:   856 bytes")
    print("    Binary: 89 bytes (9.6× smaller)")
    print("    Savings: 89.6%\n")

    print("Decode from binary:\n")
    print("  $ pulse decode message.bin --format binary -o decoded.json\n")

    print("Auto-detect format:\n")
    print("  $ pulse decode message.bin -o decoded.json\n")


def demo_complete_workflow():
    """Demonstrate complete CLI workflow."""
    print_header("6. Complete Workflow")

    print("Step 1: Create a message\n")
    print('$ pulse create --action ACT.TRANSFER.MONEY \\')
    print('    --target ENT.RESOURCE.DATABASE \\')
    print('    --parameters \'{"amount": 1000, "to": "account-123"}\' \\')
    print('    -o transfer.json\n')

    print("Step 2: Validate the message\n")
    print("$ pulse validate transfer.json\n")
    print("  ✓ Message is valid\n")

    print("Step 3: Sign the message\n")
    print("$ pulse sign transfer.json --key bank-secret-key -o transfer-signed.json\n")
    print("  ✓ Message signed: transfer-signed.json\n")

    print("Step 4: Verify signature\n")
    print("$ pulse verify transfer-signed.json --key bank-secret-key\n")
    print("  ✓ Signature is valid\n")

    print("Step 5: Encode for transmission\n")
    print("$ pulse encode transfer-signed.json --format binary -o transfer.bin --compare\n")
    print("  ✓ Encoded to binary: transfer.bin")
    print("    Size: 94 bytes\n")
    print("  Size comparison:")
    print("    JSON:   912 bytes")
    print("    Binary: 94 bytes (9.7× smaller)")
    print("    Savings: 89.7%\n")

    print("Step 6: Decode on receiver side\n")
    print("$ pulse decode transfer.bin -o received.json\n")
    print("  ✓ Decoded to: received.json\n")

    print("Step 7: Verify received message\n")
    print("$ pulse verify received.json --key bank-secret-key\n")
    print("  ✓ Signature is valid\n")


def demo_programmatic_usage():
    """Demonstrate programmatic CLI usage from Python."""
    print_header("7. Programmatic Usage from Python")

    print("You can also use the CLI programmatically:\n")

    print("```python")
    print("import subprocess")
    print("import json")
    print()
    print("# Create message via CLI")
    print("result = subprocess.run([")
    print("    'pulse', 'create',")
    print("    '--action', 'ACT.QUERY.DATA',")
    print("    '--target', 'ENT.DATA.TEXT',")
    print("    '-o', 'message.json'")
    print("], capture_output=True, text=True)")
    print()
    print("if result.returncode == 0:")
    print("    print('Message created successfully')")
    print()
    print("# Sign message")
    print("subprocess.run([")
    print("    'pulse', 'sign',")
    print("    'message.json',")
    print("    '--key', 'my-key',")
    print("    '-o', 'signed.json'")
    print("])")
    print("```\n")


def demo_use_cases():
    """Show real-world use cases."""
    print_header("8. Real-World Use Cases")

    print("Use Case 1: Automated Message Generation\n")
    print("Generate signed messages in batch:")
    print("```bash")
    print("for i in {1..100}; do")
    print('  pulse create --action ACT.QUERY.DATA \\')
    print('    --parameters "{\\\"id\\\": $i}" \\')
    print('    -o "message_$i.json"')
    print()
    print('  pulse sign "message_$i.json" \\')
    print('    --key "batch-key" \\')
    print('    -o "signed_$i.json"')
    print("done")
    print("```\n")

    print("Use Case 2: Message Validation Pipeline\n")
    print("Validate and process incoming messages:")
    print("```bash")
    print("#!/bin/bash")
    print("for file in incoming/*.json; do")
    print("  if pulse validate \"$file\" --check-freshness; then")
    print("    if pulse verify \"$file\" --key \"$SECRET_KEY\"; then")
    print('      echo "✓ Processing $file"')
    print('      process_message "$file"')
    print("    else")
    print('      echo "✗ Invalid signature: $file"')
    print("    fi")
    print("  else")
    print('    echo "✗ Invalid message: $file"')
    print("  fi")
    print("done")
    print("```\n")

    print("Use Case 3: Binary Encoding for Storage\n")
    print("Convert JSON messages to binary for efficient storage:")
    print("```bash")
    print("for file in messages/*.json; do")
    print('  pulse encode "$file" --format binary -o "archive/${file%.json}.bin"')
    print("done")
    print("```\n")


def demo_best_practices():
    """Show CLI best practices."""
    print_header("9. CLI Best Practices")

    print("✓ Best Practices:\n")

    print("1. Always validate before processing")
    print("   $ pulse validate message.json && process_message message.json\n")

    print("2. Use environment variables for keys")
    print("   $ pulse sign message.json --key \"$SECRET_KEY\" -o signed.json\n")

    print("3. Enable freshness check for security-critical operations")
    print("   $ pulse validate message.json --check-freshness\n")

    print("4. Use binary encoding for network transmission")
    print("   $ pulse encode message.json --format binary\n")

    print("5. Verify signatures before processing")
    print("   $ pulse verify message.json --key \"$KEY\" && process\n")

    print("6. Keep secret keys secure")
    print("   - Never hardcode keys in scripts")
    print("   - Use environment variables or key management systems")
    print("   - Rotate keys regularly\n")

    print("7. Use --compare to understand encoding efficiency")
    print("   $ pulse encode message.json --compare\n")


def main():
    """Run all CLI usage demonstrations."""
    print("\n" + "=" * 70)
    print("  PULSE Protocol - CLI Usage Examples")
    print("=" * 70)

    demo_cli_help()
    demo_create_message()
    demo_validate_message()
    demo_sign_verify()
    demo_encode_decode()
    demo_complete_workflow()
    demo_programmatic_usage()
    demo_use_cases()
    demo_best_practices()

    print_header("Summary")
    print("Key Takeaways:")
    print("  • CLI provides simple interface for all PULSE operations")
    print("  • Create, validate, sign, verify, encode, decode messages")
    print("  • Suitable for automation and scripting")
    print("  • Can be used programmatically from Python")
    print("  • Binary encoding provides 10× size reduction")
    print("  • Always validate and verify signatures in production")
    print()
    print("For more information:")
    print("  $ pulse --help")
    print("  $ pulse <command> --help")
    print()
    print("=" * 70)
    print()


if __name__ == "__main__":
    main()
