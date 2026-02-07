"""Tests for PULSE message security features."""
import pytest
import time
from datetime import datetime, timezone, timedelta
from pulse import PulseMessage, SecurityManager, KeyManager, SecurityError


class TestSecurityManager:
    """Test SecurityManager functionality."""

    def test_init_with_key(self):
        """Test SecurityManager initialization with provided key."""
        security = SecurityManager(secret_key="test-key-12345")
        assert security.secret_key == "test-key-12345"

    def test_init_without_key_generates_random(self):
        """Test that SecurityManager generates random key if none provided."""
        security1 = SecurityManager()
        security2 = SecurityManager()

        assert security1.secret_key is not None
        assert security2.secret_key is not None
        assert security1.secret_key != security2.secret_key
        assert len(security1.secret_key) > 20  # URL-safe base64 of 32 bytes

    def test_generate_key(self):
        """Test key generation."""
        key1 = SecurityManager.generate_key()
        key2 = SecurityManager.generate_key()

        assert key1 is not None
        assert key2 is not None
        assert key1 != key2
        assert len(key1) > 40  # URL-safe base64 encoding of 32 bytes

    def test_sign_message(self):
        """Test message signing."""
        security = SecurityManager(secret_key="test-key")
        message = PulseMessage(action="ACT.QUERY.DATA", validate=False)

        signature = security.sign_message(message)

        assert signature is not None
        assert isinstance(signature, str)
        assert len(signature) == 64  # HMAC-SHA256 hex is 64 characters
        assert message.envelope['signature'] == signature

    def test_sign_message_deterministic(self):
        """Test that signing is deterministic."""
        security = SecurityManager(secret_key="test-key")

        message1 = PulseMessage(action="ACT.QUERY.DATA", validate=False)
        message1.envelope['message_id'] = "fixed-id"
        message1.envelope['timestamp'] = "2025-02-05T12:00:00Z"
        message1.envelope['nonce'] = "fixed-nonce"

        message2 = PulseMessage(action="ACT.QUERY.DATA", validate=False)
        message2.envelope['message_id'] = "fixed-id"
        message2.envelope['timestamp'] = "2025-02-05T12:00:00Z"
        message2.envelope['nonce'] = "fixed-nonce"

        sig1 = security.sign_message(message1)
        sig2 = security.sign_message(message2)

        assert sig1 == sig2  # Same message and key produce same signature

    def test_sign_different_messages_different_signatures(self):
        """Test that different messages produce different signatures."""
        security = SecurityManager(secret_key="test-key")

        message1 = PulseMessage(action="ACT.QUERY.DATA", validate=False)
        message2 = PulseMessage(action="ACT.CREATE.TEXT", validate=False)

        sig1 = security.sign_message(message1)
        sig2 = security.sign_message(message2)

        assert sig1 != sig2

    def test_verify_signature_valid(self):
        """Test signature verification with valid signature."""
        security = SecurityManager(secret_key="test-key")
        message = PulseMessage(action="ACT.QUERY.DATA", validate=False)

        security.sign_message(message)
        assert security.verify_signature(message)

    def test_verify_signature_invalid(self):
        """Test signature verification with invalid signature."""
        security = SecurityManager(secret_key="test-key")
        message = PulseMessage(action="ACT.QUERY.DATA", validate=False)

        security.sign_message(message)

        # Tamper with message
        message.content['action'] = "ACT.MODIFY.DATA"

        assert not security.verify_signature(message)

    def test_verify_signature_missing(self):
        """Test signature verification when signature is missing."""
        security = SecurityManager(secret_key="test-key")
        message = PulseMessage(action="ACT.QUERY.DATA", validate=False)

        # No signature
        assert not security.verify_signature(message)

    def test_verify_signature_wrong_key(self):
        """Test signature verification with wrong key."""
        security1 = SecurityManager(secret_key="key1")
        security2 = SecurityManager(secret_key="key2")

        message = PulseMessage(action="ACT.QUERY.DATA", validate=False)
        security1.sign_message(message)

        # Different key
        assert not security2.verify_signature(message)

    def test_verify_signature_with_explicit_signature(self):
        """Test signature verification with explicitly provided signature."""
        security = SecurityManager(secret_key="test-key")
        message = PulseMessage(action="ACT.QUERY.DATA", validate=False)

        signature = security.sign_message(message)

        # Verify with explicit signature
        assert security.verify_signature(message, expected_signature=signature)

        # Wrong explicit signature
        assert not security.verify_signature(message, expected_signature="wrong")

    def test_sign_and_verify_roundtrip(self):
        """Test complete sign and verify roundtrip."""
        security = SecurityManager(secret_key="test-key")
        message = PulseMessage(
            action="ACT.ANALYZE.SENTIMENT",
            target="ENT.DATA.TEXT",
            parameters={"text": "Hello world", "detail": "high"},
            validate=False
        )

        # Sign
        security.sign_message(message)
        assert message.envelope['signature'] is not None

        # Verify
        assert security.verify_signature(message)

        # Serialize and deserialize
        json_str = message.to_json()
        decoded = PulseMessage.from_json(json_str)

        # Verify after deserialization
        assert security.verify_signature(decoded)

    def test_tamper_detection(self):
        """Test that tampering is detected."""
        security = SecurityManager(secret_key="test-key")
        message = PulseMessage(action="ACT.QUERY.DATA", validate=False)

        security.sign_message(message)
        assert security.verify_signature(message)

        # Tamper with different parts
        test_cases = [
            ("content action", lambda m: m.content.update({'action': 'TAMPERED'})),
            ("parameters", lambda m: m.content.update({'parameters': {'tampered': True}})),
            ("type", lambda m: setattr(m, 'type', 'TAMPERED')),
            ("sender", lambda m: m.envelope.update({'sender': 'tampered-agent'})),
        ]

        for test_name, tamper_fn in test_cases:
            message = PulseMessage(action="ACT.QUERY.DATA", validate=False)
            security.sign_message(message)

            tamper_fn(message)
            assert not security.verify_signature(message), f"Tampering {test_name} not detected"


class TestReplayProtection:
    """Test replay protection functionality."""

    def test_check_replay_protection_valid_message(self):
        """Test replay protection with valid recent message."""
        security = SecurityManager()
        message = PulseMessage(action="ACT.QUERY.DATA", validate=False)

        result = security.check_replay_protection(message)

        assert result['is_valid']
        assert result['timestamp_valid']
        assert result['age_seconds'] < 5  # Just created
        assert result['reason'] is None

    def test_check_replay_protection_old_message(self):
        """Test replay protection with old message."""
        security = SecurityManager()
        message = PulseMessage(action="ACT.QUERY.DATA", validate=False)

        # Set old timestamp
        old_time = datetime.now(timezone.utc) - timedelta(seconds=400)
        message.envelope['timestamp'] = old_time.isoformat().replace('+00:00', 'Z')

        result = security.check_replay_protection(message, max_age_seconds=300)

        assert not result['is_valid']
        assert not result['timestamp_valid']
        assert result['age_seconds'] > 300
        assert "too old" in result['reason'].lower()

    def test_check_replay_protection_future_message(self):
        """Test replay protection with message from future."""
        security = SecurityManager()
        message = PulseMessage(action="ACT.QUERY.DATA", validate=False)

        # Set future timestamp
        future_time = datetime.now(timezone.utc) + timedelta(seconds=120)
        message.envelope['timestamp'] = future_time.isoformat().replace('+00:00', 'Z')

        result = security.check_replay_protection(message)

        assert not result['is_valid']
        assert not result['timestamp_valid']
        assert "future" in result['reason'].lower()

    def test_check_replay_protection_missing_timestamp(self):
        """Test replay protection with missing timestamp."""
        security = SecurityManager()
        message = PulseMessage(action="ACT.QUERY.DATA", validate=False)
        message.envelope['timestamp'] = None

        result = security.check_replay_protection(message)

        assert not result['is_valid']
        assert not result['timestamp_valid']
        assert "missing timestamp" in result['reason'].lower()

    def test_check_replay_protection_nonce_deduplication(self):
        """Test replay protection with nonce store."""
        security = SecurityManager()
        nonce_store = set()

        message1 = PulseMessage(action="ACT.QUERY.DATA", validate=False)
        result1 = security.check_replay_protection(message1, nonce_store=nonce_store)

        assert result1['is_valid']
        assert result1['nonce_unique']
        assert message1.envelope['nonce'] in nonce_store

        # Same message again (replay attack)
        result2 = security.check_replay_protection(message1, nonce_store=nonce_store)

        assert not result2['is_valid']
        assert not result2['nonce_unique']
        assert "duplicate nonce" in result2['reason'].lower()

    def test_check_replay_protection_missing_nonce(self):
        """Test replay protection with missing nonce."""
        security = SecurityManager()
        nonce_store = set()

        message = PulseMessage(action="ACT.QUERY.DATA", validate=False)
        message.envelope['nonce'] = None

        result = security.check_replay_protection(message, nonce_store=nonce_store)

        assert not result['is_valid']
        assert not result['nonce_unique']
        assert "missing nonce" in result['reason'].lower()

    def test_check_replay_protection_custom_max_age(self):
        """Test replay protection with custom max age."""
        security = SecurityManager()
        message = PulseMessage(action="ACT.QUERY.DATA", validate=False)

        # Set timestamp 90 seconds ago
        old_time = datetime.now(timezone.utc) - timedelta(seconds=90)
        message.envelope['timestamp'] = old_time.isoformat().replace('+00:00', 'Z')

        # Should be invalid with 60s max age
        result = security.check_replay_protection(message, max_age_seconds=60)
        assert not result['is_valid']

        # Should be valid with 120s max age
        result = security.check_replay_protection(message, max_age_seconds=120)
        assert result['is_valid']


class TestKeyManager:
    """Test KeyManager functionality."""

    def test_init(self):
        """Test KeyManager initialization."""
        km = KeyManager()
        assert km is not None
        assert len(km.list_agents()) == 0

    def test_generate_and_store(self):
        """Test key generation and storage."""
        km = KeyManager()
        key = km.generate_and_store("agent-1")

        assert key is not None
        assert len(key) > 40
        assert km.get_key("agent-1") == key

    def test_store_key(self):
        """Test storing existing key."""
        km = KeyManager()
        km.store_key("agent-1", "my-secret-key")

        assert km.get_key("agent-1") == "my-secret-key"

    def test_get_key_not_found(self):
        """Test getting non-existent key."""
        km = KeyManager()
        assert km.get_key("non-existent") is None

    def test_remove_key(self):
        """Test key removal."""
        km = KeyManager()
        km.store_key("agent-1", "key-1")

        assert km.remove_key("agent-1")
        assert km.get_key("agent-1") is None

    def test_remove_key_not_found(self):
        """Test removing non-existent key."""
        km = KeyManager()
        assert not km.remove_key("non-existent")

    def test_list_agents(self):
        """Test listing agents."""
        km = KeyManager()
        km.store_key("agent-1", "key-1")
        km.store_key("agent-2", "key-2")
        km.store_key("agent-3", "key-3")

        agents = km.list_agents()
        assert len(agents) == 3
        assert "agent-1" in agents
        assert "agent-2" in agents
        assert "agent-3" in agents

    def test_key_isolation(self):
        """Test that keys are isolated per agent."""
        km = KeyManager()
        km.store_key("agent-1", "key-1")
        km.store_key("agent-2", "key-2")

        assert km.get_key("agent-1") == "key-1"
        assert km.get_key("agent-2") == "key-2"
        assert km.get_key("agent-1") != km.get_key("agent-2")


class TestSecurityIntegration:
    """Test integration of security features."""

    def test_full_secure_message_flow(self):
        """Test complete secure message flow."""
        # Setup
        km = KeyManager()
        key = km.generate_and_store("sender-agent")
        security = SecurityManager(secret_key=key)
        nonce_store = set()

        # Create and sign message
        message = PulseMessage(
            action="ACT.QUERY.DATA",
            target="ENT.DATA.TEXT",
            parameters={"query": "test"},
            sender="sender-agent",
            validate=False
        )
        security.sign_message(message)

        # Verify signature
        assert security.verify_signature(message)

        # Check replay protection
        result = security.check_replay_protection(message, nonce_store=nonce_store)
        assert result['is_valid']

        # Simulate transmission (JSON)
        json_data = message.to_json()
        received = PulseMessage.from_json(json_data)

        # Receiver verifies
        receiver_security = SecurityManager(secret_key=km.get_key("sender-agent"))
        assert receiver_security.verify_signature(received)

    def test_binary_encoding_with_signature(self):
        """Test that signature survives binary encoding."""
        security = SecurityManager(secret_key="test-key")
        message = PulseMessage(action="ACT.QUERY.DATA", validate=False)

        # Sign
        security.sign_message(message)
        original_sig = message.envelope['signature']

        # Binary roundtrip
        binary = message.to_binary()
        decoded = PulseMessage.from_binary(binary)

        # Signature preserved
        assert decoded.envelope['signature'] == original_sig
        assert security.verify_signature(decoded)

    def test_multiple_agents_different_keys(self):
        """Test multiple agents with different keys."""
        km = KeyManager()
        key1 = km.generate_and_store("agent-1")
        key2 = km.generate_and_store("agent-2")

        security1 = SecurityManager(secret_key=key1)
        security2 = SecurityManager(secret_key=key2)

        message1 = PulseMessage(action="ACT.QUERY.DATA", sender="agent-1", validate=False)
        message2 = PulseMessage(action="ACT.QUERY.DATA", sender="agent-2", validate=False)

        security1.sign_message(message1)
        security2.sign_message(message2)

        # Each agent can verify their own messages
        assert security1.verify_signature(message1)
        assert security2.verify_signature(message2)

        # But not each other's
        assert not security1.verify_signature(message2)
        assert not security2.verify_signature(message1)
