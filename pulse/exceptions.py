"""PULSE Protocol custom exceptions."""


class PulseException(Exception):
    """Base exception for all PULSE Protocol errors."""

    pass


class ValidationError(PulseException):
    """Message validation failed."""

    pass


class EncodingError(PulseException):
    """Encoding/decoding operation failed."""

    pass


class DecodingError(PulseException):
    """Decoding operation failed."""

    pass


class SecurityError(PulseException):
    """Security validation failed."""

    pass


class NetworkError(PulseException):
    """Network communication failed."""

    pass


class TimeoutError(PulseException):
    """Operation timed out."""

    pass


class VocabularyError(PulseException):
    """Vocabulary-related error."""

    pass
