"""PULSE Protocol security features.

This module provides:
- HMAC-SHA256 message signing for integrity verification
- Signature verification
- Key management utilities
- Replay protection (timestamp-based)

Security Features:
- HMAC-SHA256 for message authentication
- Deterministic signing (same message + key = same signature)
- No encryption (protocol is not end-to-end encrypted by default)
- Compatible with TLS for transport security
"""
from typing import Optional, Dict, Any
import hmac
import hashlib
import secrets
from datetime import datetime, timezone


class SecurityManager:
    """
    Manages PULSE message security operations.

    Provides HMAC-SHA256 signing and verification for message integrity.
    Does not provide encryption - use TLS for transport security.

    Example:
        >>> security = SecurityManager(secret_key="my-secret-key")
        >>> message = PulseMessage(action="ACT.QUERY.DATA")
        >>> security.sign_message(message)
        >>> assert security.verify_signature(message)
    """

    def __init__(self, secret_key: Optional[str] = None):
        """
        Initialize SecurityManager with a secret key.

        Args:
            secret_key: Secret key for HMAC signing (generates if None)
                       Should be kept secure and shared between parties

        Example:
            >>> # Generate random key
            >>> security = SecurityManager()

            >>> # Use specific key
            >>> security = SecurityManager(secret_key="my-secret-key")
        """
        if secret_key is None:
            # Generate a secure random key
            self.secret_key = secrets.token_urlsafe(32)
        else:
            self.secret_key = secret_key

    @staticmethod
    def generate_key() -> str:
        """
        Generate a secure random key for HMAC signing.

        Returns:
            URL-safe base64-encoded random key (32 bytes)

        Example:
            >>> key = SecurityManager.generate_key()
            >>> print(f"Key length: {len(key)}")  # ~43 characters
        """
        return secrets.token_urlsafe(32)

    def sign_message(self, message) -> str:
        """
        Sign a PULSE message with HMAC-SHA256.

        Creates a signature from the message envelope and content.
        The signature is deterministic - same message and key produce
        same signature, enabling verification.

        Args:
            message: PulseMessage instance to sign

        Returns:
            Hex-encoded HMAC-SHA256 signature

        Raises:
            ValueError: If message is invalid

        Example:
            >>> security = SecurityManager(secret_key="test-key")
            >>> message = PulseMessage(action="ACT.QUERY.DATA")
            >>> signature = security.sign_message(message)
            >>> print(f"Signature: {signature[:16]}...")  # First 16 chars
        """
        # Create canonical string from message
        canonical = self._create_canonical_string(message)

        # Sign with HMAC-SHA256
        signature = hmac.new(
            self.secret_key.encode('utf-8'),
            canonical.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

        # Store signature in envelope
        message.envelope['signature'] = signature

        return signature

    def verify_signature(self, message, expected_signature: Optional[str] = None) -> bool:
        """
        Verify PULSE message signature.

        Recomputes the signature and compares with the stored or provided
        signature using constant-time comparison to prevent timing attacks.

        Args:
            message: PulseMessage instance to verify
            expected_signature: Expected signature (uses message.envelope['signature'] if None)

        Returns:
            True if signature is valid, False otherwise

        Example:
            >>> security = SecurityManager(secret_key="test-key")
            >>> message = PulseMessage(action="ACT.QUERY.DATA")
            >>> security.sign_message(message)
            >>> assert security.verify_signature(message)  # Valid

            >>> # Tamper with message
            >>> message.content['action'] = "ACT.MODIFY.DATA"
            >>> assert not security.verify_signature(message)  # Invalid
        """
        if expected_signature is None:
            expected_signature = message.envelope.get('signature')

        if not expected_signature:
            return False

        # Temporarily remove signature to compute canonical string
        stored_signature = message.envelope.get('signature')
        message.envelope['signature'] = None

        try:
            # Recompute signature
            canonical = self._create_canonical_string(message)
            computed_signature = hmac.new(
                self.secret_key.encode('utf-8'),
                canonical.encode('utf-8'),
                hashlib.sha256
            ).hexdigest()

            # Constant-time comparison to prevent timing attacks
            return hmac.compare_digest(computed_signature, expected_signature)
        finally:
            # Restore original signature
            message.envelope['signature'] = stored_signature

    def _create_canonical_string(self, message) -> str:
        """
        Create canonical string representation for signing.

        Uses deterministic field ordering to ensure consistent signatures.
        Includes envelope (except signature) and content.

        Args:
            message: PulseMessage instance

        Returns:
            Canonical string representation
        """
        import json

        # Create deterministic dict with sorted keys
        canonical_data = {
            'envelope': {
                'version': message.envelope.get('version'),
                'timestamp': message.envelope.get('timestamp'),
                'sender': message.envelope.get('sender'),
                'receiver': message.envelope.get('receiver'),
                'message_id': message.envelope.get('message_id'),
                'nonce': message.envelope.get('nonce'),
                # Note: signature is excluded from canonical string
            },
            'type': message.type,
            'content': message.content
        }

        # Use compact JSON with sorted keys for deterministic output
        return json.dumps(canonical_data, sort_keys=True, separators=(',', ':'))

    @staticmethod
    def check_replay_protection(
        message,
        max_age_seconds: int = 300,
        nonce_store: Optional[set] = None
    ) -> Dict[str, Any]:
        """
        Check message for replay attack indicators.

        Validates:
        1. Timestamp freshness (within max_age_seconds)
        2. Nonce uniqueness (if nonce_store provided)

        Args:
            message: PulseMessage to check
            max_age_seconds: Maximum message age in seconds (default 5 minutes)
            nonce_store: Optional set of seen nonces for deduplication

        Returns:
            Dictionary with check results:
                - 'is_valid': bool - Overall validity
                - 'timestamp_valid': bool - Timestamp check
                - 'nonce_unique': bool - Nonce check (or None if not checked)
                - 'age_seconds': float - Message age
                - 'reason': str - Reason if invalid

        Example:
            >>> security = SecurityManager()
            >>> message = PulseMessage(action="ACT.QUERY.DATA")
            >>> result = security.check_replay_protection(message)
            >>> assert result['is_valid']
            >>> print(f"Message age: {result['age_seconds']:.2f}s")
        """
        from pulse.validator import MessageValidator

        result = {
            'is_valid': True,
            'timestamp_valid': True,
            'nonce_unique': None,
            'age_seconds': 0.0,
            'reason': None
        }

        # Check timestamp freshness
        timestamp_str = message.envelope.get('timestamp')
        if not timestamp_str:
            result['is_valid'] = False
            result['timestamp_valid'] = False
            result['reason'] = "Missing timestamp"
            return result

        try:
            # Parse timestamp
            if timestamp_str.endswith('Z'):
                timestamp_str = timestamp_str[:-1] + '+00:00'
            message_time = datetime.fromisoformat(timestamp_str)
            current_time = datetime.now(timezone.utc)

            # Calculate age
            age = (current_time - message_time).total_seconds()
            result['age_seconds'] = age

            # Check if too old or from future
            if age > max_age_seconds:
                result['is_valid'] = False
                result['timestamp_valid'] = False
                result['reason'] = f"Message too old ({age:.1f}s > {max_age_seconds}s)"
                return result

            if age < -60:  # Allow 60 seconds clock skew
                result['is_valid'] = False
                result['timestamp_valid'] = False
                result['reason'] = f"Message from future ({age:.1f}s)"
                return result

        except Exception as e:
            result['is_valid'] = False
            result['timestamp_valid'] = False
            result['reason'] = f"Invalid timestamp format: {str(e)}"
            return result

        # Check nonce uniqueness if store provided
        if nonce_store is not None:
            nonce = message.envelope.get('nonce')
            if not nonce:
                result['is_valid'] = False
                result['nonce_unique'] = False
                result['reason'] = "Missing nonce"
                return result

            if nonce in nonce_store:
                result['is_valid'] = False
                result['nonce_unique'] = False
                result['reason'] = f"Duplicate nonce detected (replay attack?)"
                return result

            # Mark nonce as seen
            nonce_store.add(nonce)
            result['nonce_unique'] = True

        return result


class KeyManager:
    """
    Manages security keys for PULSE Protocol.

    Simple key storage and retrieval. In production, use a proper
    secrets management system (HashiCorp Vault, AWS Secrets Manager, etc.).

    Example:
        >>> km = KeyManager()
        >>> key = km.generate_and_store("agent-1")
        >>> retrieved = km.get_key("agent-1")
        >>> assert key == retrieved
    """

    def __init__(self):
        """Initialize key manager with empty key store."""
        self._keys: Dict[str, str] = {}

    def generate_and_store(self, agent_id: str) -> str:
        """
        Generate and store a new key for an agent.

        Args:
            agent_id: Unique agent identifier

        Returns:
            Generated secret key

        Example:
            >>> km = KeyManager()
            >>> key = km.generate_and_store("agent-1")
            >>> print(f"Generated key: {key[:16]}...")
        """
        key = SecurityManager.generate_key()
        self._keys[agent_id] = key
        return key

    def store_key(self, agent_id: str, key: str) -> None:
        """
        Store an existing key for an agent.

        Args:
            agent_id: Unique agent identifier
            key: Secret key to store

        Example:
            >>> km = KeyManager()
            >>> km.store_key("agent-1", "my-secret-key")
        """
        self._keys[agent_id] = key

    def get_key(self, agent_id: str) -> Optional[str]:
        """
        Retrieve stored key for an agent.

        Args:
            agent_id: Unique agent identifier

        Returns:
            Secret key if found, None otherwise

        Example:
            >>> km = KeyManager()
            >>> km.store_key("agent-1", "my-secret-key")
            >>> key = km.get_key("agent-1")
            >>> assert key == "my-secret-key"
        """
        return self._keys.get(agent_id)

    def remove_key(self, agent_id: str) -> bool:
        """
        Remove stored key for an agent.

        Args:
            agent_id: Unique agent identifier

        Returns:
            True if key was removed, False if not found

        Example:
            >>> km = KeyManager()
            >>> km.store_key("agent-1", "my-secret-key")
            >>> assert km.remove_key("agent-1")
            >>> assert km.get_key("agent-1") is None
        """
        if agent_id in self._keys:
            del self._keys[agent_id]
            return True
        return False

    def list_agents(self) -> list:
        """
        List all agents with stored keys.

        Returns:
            List of agent IDs

        Example:
            >>> km = KeyManager()
            >>> km.store_key("agent-1", "key1")
            >>> km.store_key("agent-2", "key2")
            >>> agents = km.list_agents()
            >>> assert len(agents) == 2
        """
        return list(self._keys.keys())
