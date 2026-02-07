"""PULSE Protocol message validation."""
from datetime import datetime, timezone, timedelta
from typing import Dict, Any
from pulse.vocabulary import Vocabulary
from pulse.exceptions import ValidationError


class MessageValidator:
    """
    Validate PULSE messages for correctness and security.

    Performs three-stage validation:
    1. Envelope validation - Check required fields and formats
    2. Content validation - Verify semantic concepts
    3. Timestamp validation - Ensure freshness and prevent replay

    Example:
        >>> from pulse import PulseMessage
        >>> from pulse.validator import MessageValidator
        >>> message = PulseMessage(action="ACT.QUERY.DATA")
        >>> MessageValidator.validate_message(message)
        True
    """

    @staticmethod
    def validate_envelope(envelope: Dict[str, Any]) -> bool:
        """
        Validate envelope structure and required fields.

        Args:
            envelope: Message envelope dictionary

        Returns:
            True if valid

        Raises:
            ValidationError: If envelope is invalid

        Example:
            >>> envelope = {"version": "1.0", "timestamp": "2025-01-01T00:00:00Z", ...}
            >>> MessageValidator.validate_envelope(envelope)
            True
        """
        required_fields = ["version", "timestamp", "sender", "receiver", "message_id", "nonce"]

        # Check all required fields exist
        for field in required_fields:
            if field not in envelope:
                raise ValidationError(f"Missing required envelope field: {field}")

        # Validate version
        if envelope["version"] != "1.0":
            raise ValidationError(
                f"Unsupported protocol version: {envelope['version']}. Only version 1.0 is supported."
            )

        # Validate timestamp format
        try:
            timestamp = envelope["timestamp"]
            # Remove 'Z' suffix if present and parse
            timestamp_clean = timestamp.rstrip("Z")
            datetime.fromisoformat(timestamp_clean)
        except (ValueError, AttributeError) as e:
            raise ValidationError(f"Invalid timestamp format: {envelope['timestamp']}. {str(e)}")

        # Validate message_id is not empty
        if not envelope["message_id"] or len(envelope["message_id"].strip()) == 0:
            raise ValidationError("Message ID cannot be empty")

        # Validate nonce is not empty
        if not envelope["nonce"] or len(envelope["nonce"].strip()) == 0:
            raise ValidationError("Nonce cannot be empty")

        # Validate sender is not empty
        if not envelope["sender"] or len(envelope["sender"].strip()) == 0:
            raise ValidationError("Sender ID cannot be empty")

        return True

    @staticmethod
    def validate_content(content: Dict[str, Any]) -> bool:
        """
        Validate content structure and semantic concepts.

        Args:
            content: Message content dictionary

        Returns:
            True if valid

        Raises:
            ValidationError: If content is invalid

        Example:
            >>> content = {"action": "ACT.QUERY.DATA", "object": "ENT.DATA.TEXT"}
            >>> MessageValidator.validate_content(content)
            True
        """
        # Action is required
        if "action" not in content:
            raise ValidationError("Missing required field 'action' in content")

        action = content["action"]

        # Validate action is not empty
        if not action or len(action.strip()) == 0:
            raise ValidationError("Action cannot be empty")

        # Validate action is a valid vocabulary concept
        if not Vocabulary.validate_concept(action):
            suggestions = Vocabulary.search(action.split(".")[-1] if "." in action else action)
            if suggestions:
                raise ValidationError(
                    f"Invalid action concept: '{action}'. Did you mean one of: {suggestions[:3]}?"
                )
            else:
                raise ValidationError(
                    f"Invalid action concept: '{action}'. Not found in PULSE vocabulary."
                )

        # Validate object/target if present
        if "object" in content and content["object"] is not None:
            obj = content["object"]
            if len(obj.strip()) == 0:
                raise ValidationError("Object cannot be empty string")

            if not Vocabulary.validate_concept(obj):
                suggestions = Vocabulary.search(obj.split(".")[-1] if "." in obj else obj)
                if suggestions:
                    raise ValidationError(
                        f"Invalid object concept: '{obj}'. Did you mean one of: {suggestions[:3]}?"
                    )
                else:
                    raise ValidationError(
                        f"Invalid object concept: '{obj}'. Not found in PULSE vocabulary."
                    )

        # Validate parameters is a dict if present
        if "parameters" in content:
            if not isinstance(content["parameters"], dict):
                raise ValidationError("Parameters must be a dictionary")

        return True

    @staticmethod
    def validate_timestamp_freshness(
        timestamp: str, max_age_seconds: int = 300, allow_future_seconds: int = 60
    ) -> bool:
        """
        Validate message timestamp is fresh (not too old or in future).

        Args:
            timestamp: ISO format timestamp string
            max_age_seconds: Maximum age in seconds (default 300 = 5 minutes)
            allow_future_seconds: Allow clock skew in seconds (default 60 = 1 minute)

        Returns:
            True if timestamp is fresh

        Raises:
            ValidationError: If timestamp is too old or too far in future

        Example:
            >>> MessageValidator.validate_timestamp_freshness("2025-01-01T00:00:00Z")
            # Raises ValidationError if message is > 5 minutes old
        """
        try:
            # Parse timestamp
            timestamp_clean = timestamp.rstrip("Z")
            msg_time = datetime.fromisoformat(timestamp_clean)

            # Make timezone-aware if not already
            if msg_time.tzinfo is None:
                msg_time = msg_time.replace(tzinfo=timezone.utc)

            # Get current time
            now = datetime.now(timezone.utc)

            # Calculate age
            age = (now - msg_time).total_seconds()

            # Check if too old
            if age > max_age_seconds:
                raise ValidationError(
                    f"Message too old: {age:.0f} seconds (max allowed: {max_age_seconds})"
                )

            # Check if too far in future (clock skew)
            if age < -allow_future_seconds:
                raise ValidationError(
                    f"Message timestamp in future: {-age:.0f} seconds ahead (max allowed: {allow_future_seconds})"
                )

            return True

        except ValueError as e:
            raise ValidationError(f"Invalid timestamp format: {timestamp}. {str(e)}")

    @classmethod
    def validate_message(
        cls, message, check_freshness: bool = True, max_age_seconds: int = 300
    ) -> bool:
        """
        Validate complete PULSE message.

        Performs all validation checks:
        1. Envelope structure and fields
        2. Content and vocabulary concepts
        3. Timestamp freshness (optional)

        Args:
            message: PulseMessage instance to validate
            check_freshness: Whether to check timestamp freshness (default True)
            max_age_seconds: Maximum message age if checking freshness (default 300)

        Returns:
            True if message is valid

        Raises:
            ValidationError: If any validation check fails

        Example:
            >>> from pulse import PulseMessage
            >>> message = PulseMessage(action="ACT.QUERY.DATA")
            >>> MessageValidator.validate_message(message)
            True
        """
        # Validate envelope
        cls.validate_envelope(message.envelope)

        # Validate content
        cls.validate_content(message.content)

        # Validate timestamp freshness if requested
        if check_freshness:
            cls.validate_timestamp_freshness(
                message.envelope["timestamp"], max_age_seconds=max_age_seconds
            )

        return True

    @staticmethod
    def validate_message_type(message_type: str) -> bool:
        """
        Validate message type is one of the allowed values.

        Args:
            message_type: Message type string

        Returns:
            True if valid

        Raises:
            ValidationError: If message type is invalid

        Example:
            >>> MessageValidator.validate_message_type("REQUEST")
            True
        """
        valid_types = ["REQUEST", "RESPONSE", "ERROR", "STATUS"]

        if message_type not in valid_types:
            raise ValidationError(
                f"Invalid message type: '{message_type}'. Must be one of: {valid_types}"
            )

        return True
