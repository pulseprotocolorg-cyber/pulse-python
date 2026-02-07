"""
PULSE Protocol - Security Features.

This example demonstrates:
1. HMAC-SHA256 message signing
2. Signature verification
3. Replay protection (timestamp and nonce)
4. Key management
5. Secure message flow between agents
6. Tamper detection
"""

from pulse import PulseMessage, SecurityManager, KeyManager
from datetime import datetime, timezone, timedelta
import time


def print_header(title):
    """Print section header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")


def demo_message_signing():
    """Demonstrate message signing with HMAC-SHA256."""
    print_header("1. Message Signing with HMAC-SHA256")

    print("Creating security manager with secret key...\n")

    # Initialize SecurityManager with a secret key
    security = SecurityManager(secret_key="my-secret-key-12345")

    # Create a message
    message = PulseMessage(
        action="ACT.QUERY.DATA",
        target="ENT.DATA.TEXT",
        parameters={"query": "hello world"},
        validate=False
    )

    print(f"Original message:")
    print(f"  Action: {message.content['action']}")
    print(f"  Signature: {message.envelope.get('signature')}")
    print()

    # Sign the message
    signature = security.sign_message(message)

    print(f"Message signed!")
    print(f"  Signature: {signature[:32]}...")
    print(f"  Length: {len(signature)} characters (HMAC-SHA256)")
    print(f"  Stored in envelope: {message.envelope['signature'][:32]}...")
    print()


def demo_signature_verification():
    """Demonstrate signature verification."""
    print_header("2. Signature Verification")

    security = SecurityManager(secret_key="my-secret-key")

    print("Test 1: Verify valid signature\n")

    message = PulseMessage(action="ACT.QUERY.DATA", validate=False)
    security.sign_message(message)

    is_valid = security.verify_signature(message)
    print(f"  ✓ Signature valid: {is_valid}")
    print()

    print("Test 2: Detect tampering\n")

    # Tamper with the message
    original_action = message.content['action']
    message.content['action'] = "ACT.MODIFY.DATA"

    is_valid = security.verify_signature(message)
    print(f"  Original action: {original_action}")
    print(f"  Tampered action: {message.content['action']}")
    print(f"  ✗ Signature valid: {is_valid}")
    print(f"  → Tampering detected successfully!")
    print()

    print("Test 3: Wrong key detection\n")

    message = PulseMessage(action="ACT.QUERY.DATA", validate=False)
    security1 = SecurityManager(secret_key="key1")
    security2 = SecurityManager(secret_key="key2")

    security1.sign_message(message)
    is_valid = security2.verify_signature(message)

    print(f"  Signed with: key1")
    print(f"  Verified with: key2")
    print(f"  ✗ Signature valid: {is_valid}")
    print(f"  → Wrong key detected successfully!")
    print()


def demo_replay_protection():
    """Demonstrate replay attack protection."""
    print_header("3. Replay Attack Protection")

    security = SecurityManager()
    nonce_store = set()

    print("Test 1: Valid recent message\n")

    message = PulseMessage(action="ACT.QUERY.DATA", validate=False)
    result = security.check_replay_protection(message, nonce_store=nonce_store)

    print(f"  Message age: {result['age_seconds']:.2f} seconds")
    print(f"  Timestamp valid: {result['timestamp_valid']}")
    print(f"  Nonce unique: {result['nonce_unique']}")
    print(f"  ✓ Overall valid: {result['is_valid']}")
    print()

    print("Test 2: Replay attack detection\n")

    # Try to send same message again (replay attack)
    result = security.check_replay_protection(message, nonce_store=nonce_store)

    print(f"  Nonce unique: {result['nonce_unique']}")
    print(f"  ✗ Overall valid: {result['is_valid']}")
    print(f"  Reason: {result['reason']}")
    print(f"  → Replay attack detected successfully!")
    print()

    print("Test 3: Old message detection\n")

    # Create message with old timestamp
    old_message = PulseMessage(action="ACT.QUERY.DATA", validate=False)
    old_time = datetime.now(timezone.utc) - timedelta(seconds=400)
    old_message.envelope['timestamp'] = old_time.isoformat().replace('+00:00', 'Z')

    result = security.check_replay_protection(old_message, max_age_seconds=300)

    print(f"  Message age: {result['age_seconds']:.1f} seconds")
    print(f"  Max allowed age: 300 seconds")
    print(f"  ✗ Overall valid: {result['is_valid']}")
    print(f"  Reason: {result['reason']}")
    print(f"  → Old message rejected successfully!")
    print()


def demo_key_management():
    """Demonstrate key management."""
    print_header("4. Key Management")

    km = KeyManager()

    print("Generating keys for multiple agents...\n")

    # Generate keys for multiple agents
    agents = ["agent-1", "agent-2", "agent-3"]
    for agent_id in agents:
        key = km.generate_and_store(agent_id)
        print(f"  {agent_id}: {key[:24]}...")

    print()

    print("Listing all agents with keys...\n")
    all_agents = km.list_agents()
    print(f"  Total agents: {len(all_agents)}")
    print(f"  Agents: {', '.join(all_agents)}")
    print()

    print("Retrieving specific key...\n")
    key = km.get_key("agent-1")
    print(f"  agent-1 key: {key[:24]}...")
    print()

    print("Removing agent key...\n")
    removed = km.remove_key("agent-2")
    print(f"  Removed agent-2: {removed}")
    print(f"  Remaining agents: {', '.join(km.list_agents())}")
    print()


def demo_secure_message_flow():
    """Demonstrate complete secure message flow."""
    print_header("5. Secure Message Flow (Sender → Receiver)")

    # Setup
    km = KeyManager()
    sender_key = km.generate_and_store("sender-agent")
    nonce_store = set()

    print("Step 1: Sender creates and signs message\n")

    sender_security = SecurityManager(secret_key=sender_key)
    message = PulseMessage(
        action="ACT.ANALYZE.SENTIMENT",
        target="ENT.DATA.TEXT",
        parameters={"text": "PULSE Protocol is secure!", "detail": "high"},
        sender="sender-agent",
        validate=False
    )

    sender_security.sign_message(message)
    print(f"  ✓ Message created")
    print(f"  ✓ Message signed")
    print(f"  Signature: {message.envelope['signature'][:32]}...")
    print()

    print("Step 2: Message transmitted (JSON encoding)\n")

    json_data = message.to_json(indent=None)
    print(f"  ✓ Serialized to JSON")
    print(f"  Size: {len(json_data)} bytes")
    print()

    print("Step 3: Receiver verifies message\n")

    # Receiver gets message
    received = PulseMessage.from_json(json_data)

    # Receiver gets sender's public key (in real system, from key store)
    receiver_security = SecurityManager(secret_key=km.get_key("sender-agent"))

    # Verify signature
    is_valid_sig = receiver_security.verify_signature(received)
    print(f"  ✓ Signature verified: {is_valid_sig}")

    # Check replay protection
    replay_result = receiver_security.check_replay_protection(
        received,
        nonce_store=nonce_store
    )
    print(f"  ✓ Replay protection checked: {replay_result['is_valid']}")
    print(f"  Message age: {replay_result['age_seconds']:.2f}s")
    print()

    if is_valid_sig and replay_result['is_valid']:
        print("  ✓✓ Message authenticated and accepted!")
        print(f"  Action: {received.content['action']}")
        print(f"  Text: {received.content['parameters']['text']}")
    print()


def demo_tamper_detection():
    """Demonstrate tamper detection."""
    print_header("6. Tamper Detection")

    security = SecurityManager(secret_key="test-key")

    print("Creating and signing original message...\n")

    message = PulseMessage(
        action="ACT.TRANSFER.MONEY",
        target="ENT.RESOURCE.DATABASE",
        parameters={"amount": 100, "to": "account-123"},
        validate=False
    )

    security.sign_message(message)
    print(f"  Original amount: ${message.content['parameters']['amount']}")
    print(f"  Original account: {message.content['parameters']['to']}")
    print(f"  ✓ Signature: {message.envelope['signature'][:32]}...")
    print()

    print("Verifying original message...\n")
    is_valid = security.verify_signature(message)
    print(f"  ✓ Valid: {is_valid}")
    print()

    print("Attempting to tamper with amount (100 → 1000000)...\n")

    # Attacker tries to modify amount
    message.content['parameters']['amount'] = 1000000

    print(f"  Tampered amount: ${message.content['parameters']['amount']}")
    print(f"  Signature unchanged: {message.envelope['signature'][:32]}...")
    print()

    print("Verifying tampered message...\n")
    is_valid = security.verify_signature(message)
    print(f"  ✗ Valid: {is_valid}")
    print(f"  → Tampering detected! Transaction rejected.")
    print()

    print("  💡 Key Insight:")
    print("     Any modification to the message content invalidates the signature.")
    print("     This ensures message integrity and prevents tampering.")
    print()


def demo_performance():
    """Demonstrate security performance."""
    print_header("7. Performance Characteristics")

    security = SecurityManager(secret_key="test-key")

    print("Signing performance...\n")

    # Test signing
    message = PulseMessage(action="ACT.QUERY.DATA", validate=False)
    start = time.time()
    for _ in range(1000):
        security.sign_message(message)
    duration = time.time() - start

    print(f"  1,000 signatures: {duration:.3f}s")
    print(f"  Average: {duration/1000*1000:.3f}ms per signature")
    print()

    print("Verification performance...\n")

    # Test verification
    security.sign_message(message)
    start = time.time()
    for _ in range(1000):
        security.verify_signature(message)
    duration = time.time() - start

    print(f"  1,000 verifications: {duration:.3f}s")
    print(f"  Average: {duration/1000*1000:.3f}ms per verification")
    print()

    print("  💡 Performance:")
    print("     HMAC-SHA256 is fast enough for real-time applications.")
    print("     Minimal overhead (~1-2ms) for message security.")
    print()


def demo_best_practices():
    """Show security best practices."""
    print_header("8. Security Best Practices")

    print("✓ Best Practices:\n")

    print("1. Key Management")
    print("   • Generate strong random keys (32+ bytes)")
    print("   • Store keys securely (env vars, secrets manager)")
    print("   • Rotate keys periodically")
    print("   • Use different keys for different purposes")
    print()

    print("2. Message Signing")
    print("   • Sign ALL messages in production")
    print("   • Verify signatures before processing")
    print("   • Use HMAC-SHA256 or stronger")
    print()

    print("3. Replay Protection")
    print("   • Always check timestamp freshness")
    print("   • Maintain nonce deduplication store")
    print("   • Use short validity windows (5 minutes)")
    print("   • Clear old nonces periodically")
    print()

    print("4. Transport Security")
    print("   • Use TLS for network transmission")
    print("   • PULSE signatures provide integrity, not confidentiality")
    print("   • TLS + signatures = defense in depth")
    print()

    print("5. Error Handling")
    print("   • Reject invalid signatures immediately")
    print("   • Log security violations")
    print("   • Don't leak information in error messages")
    print("   • Use constant-time comparisons")
    print()

    print("6. Production Checklist")
    print("   ☐ All messages signed")
    print("   ☐ All signatures verified")
    print("   ☐ Replay protection enabled")
    print("   ☐ TLS configured")
    print("   ☐ Keys stored securely")
    print("   ☐ Security monitoring enabled")
    print()


def main():
    """Run all security demonstrations."""
    print("\n" + "=" * 70)
    print("  PULSE Protocol - Security Features")
    print("=" * 70)

    demo_message_signing()
    demo_signature_verification()
    demo_replay_protection()
    demo_key_management()
    demo_secure_message_flow()
    demo_tamper_detection()
    demo_performance()
    demo_best_practices()

    print_header("Summary")
    print("Key Takeaways:")
    print("  • HMAC-SHA256 provides message integrity")
    print("  • Signatures detect any tampering")
    print("  • Replay protection prevents duplicate messages")
    print("  • Key management is critical for security")
    print("  • Fast performance (~1-2ms overhead)")
    print("  • Use TLS for transport security")
    print("  • Defense in depth: signatures + TLS + validation")
    print()
    print("=" * 70)
    print()


if __name__ == "__main__":
    main()
