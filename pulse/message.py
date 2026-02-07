"""PULSE Protocol core message implementation."""
from datetime import datetime, timezone
from typing import Optional, Dict, Any
import uuid
import json
from pulse.validator import MessageValidator
from pulse.exceptions import ValidationError


class PulseMessage:
    """
    Core PULSE Protocol message.

    A PulseMessage encapsulates all information needed for AI-to-AI
    communication, including envelope metadata, message type, and content.

    Attributes:
        envelope: Message metadata (sender, receiver, timestamp, etc.)
        type: Message type (REQUEST, RESPONSE, ERROR, STATUS)
        content: Message payload with action and parameters

    Example:
        >>> message = PulseMessage(
        ...     action="ACT.QUERY.DATA",
        ...     target="ENT.DATA.TEXT"
        ... )
        >>> json_str = message.to_json()
    """

    def __init__(
        self,
        action: str,
        target: Optional[str] = None,
        parameters: Optional[Dict[str, Any]] = None,
        sender: str = "default-agent",
        validate: bool = True,
    ) -> None:
        """
        Initialize a PULSE message.

        Args:
            action: PULSE action concept (e.g., "ACT.QUERY.DATA")
            target: Target object concept (e.g., "ENT.DATA.TEXT")
            parameters: Additional parameters for the action
            sender: Agent ID of the sender
            validate: Whether to validate the message (default True)

        Raises:
            ValidationError: If validation is enabled and message is invalid

        Example:
            >>> message = PulseMessage(
            ...     action="ACT.QUERY.DATA",
            ...     target="ENT.DATA.TEXT",
            ...     parameters={"query": "test"}
            ... )
        """
        self.envelope = self._create_envelope(sender)
        self.type = "REQUEST"
        self.content = {
            "action": action,
            "object": target,
            "parameters": parameters or {},
        }

        # Validate message if requested
        if validate:
            self.validate()

    def _create_envelope(self, sender: str) -> Dict[str, Any]:
        """
        Create message envelope with metadata.

        Args:
            sender: Agent ID of the sender

        Returns:
            Dictionary containing envelope fields
        """
        return {
            "version": "1.0",
            "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "sender": sender,
            "receiver": None,
            "message_id": str(uuid.uuid4()),
            "nonce": str(uuid.uuid4()),
            "signature": None,
        }

    def to_json(self, indent: Optional[int] = 2) -> str:
        """
        Serialize message to JSON string.

        Serializes the PULSE message to a JSON string format
        that can be transmitted over the network or saved to disk.

        Args:
            indent: Number of spaces for indentation (None for compact)

        Returns:
            JSON string representation of the message

        Example:
            >>> message = PulseMessage(action="ACT.QUERY.DATA")
            >>> json_str = message.to_json()
            >>> print(json_str)
            {
              "envelope": {...},
              "type": "REQUEST",
              "content": {...}
            }
        """
        return json.dumps(self.to_dict(), indent=indent)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert message to dictionary.

        Returns:
            Dictionary representation of the message
        """
        return {"envelope": self.envelope, "type": self.type, "content": self.content}

    @classmethod
    def from_json(cls, json_str: str) -> "PulseMessage":
        """
        Deserialize message from JSON string.

        Creates a PulseMessage instance from a JSON string.

        Args:
            json_str: JSON string representation of a message

        Returns:
            PulseMessage instance

        Raises:
            json.JSONDecodeError: If JSON is invalid

        Example:
            >>> json_str = '{"envelope": {...}, "type": "REQUEST", "content": {...}}'
            >>> message = PulseMessage.from_json(json_str)
        """
        data = json.loads(json_str)
        message = cls.__new__(cls)
        message.envelope = data["envelope"]
        message.type = data["type"]
        message.content = data["content"]
        return message

    def __repr__(self) -> str:
        """Return string representation of message."""
        return f"PulseMessage(action={self.content['action']}, type={self.type})"

    def __str__(self) -> str:
        """Return human-readable string representation."""
        return self.to_json()

    def validate(self, check_freshness: bool = False) -> bool:
        """
        Validate this message.

        Args:
            check_freshness: Whether to check timestamp freshness (default False)

        Returns:
            True if message is valid

        Raises:
            ValidationError: If message is invalid

        Example:
            >>> message = PulseMessage(action="ACT.QUERY.DATA", validate=False)
            >>> message.validate()
            True
        """
        return MessageValidator.validate_message(self, check_freshness=check_freshness)
