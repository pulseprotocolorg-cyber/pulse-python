"""
PULSE Protocol - Error Handling Patterns.

This example demonstrates:
1. Handling validation errors
2. Encoding/decoding errors
3. Creating error response messages
4. Retry strategies
5. Error recovery patterns
"""

from pulse import PulseMessage, Vocabulary, ValidationError, EncodingError, DecodingError
import time


def print_header(title):
    """Print section header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")


def demo_validation_errors():
    """Demonstrate handling validation errors."""
    print_header("1. Validation Error Handling")

    print("Attempting to create messages with validation errors...\n")

    # Invalid action concept
    print("Test 1: Invalid action concept")
    try:
        message = PulseMessage(action="INVALID.ACTION")
    except ValidationError as e:
        print(f"✓ Caught ValidationError: {str(e)[:80]}...")
        print("  → Suggestion: Check vocabulary for valid concepts")
    print()

    # Invalid target concept
    print("Test 2: Invalid target concept")
    try:
        message = PulseMessage(action="ACT.QUERY.DATA", target="INVALID.TARGET")
    except ValidationError as e:
        print(f"✓ Caught ValidationError: {str(e)[:80]}...")
        print("  → Using vocabulary search to find alternatives")
        results = Vocabulary.search("DATA")
        print(f"  → Found alternatives: {results[:3]}")
    print()

    # Skip validation for custom concepts
    print("Test 3: Skip validation for custom workflow")
    try:
        message = PulseMessage(action="CUSTOM.ACTION", validate=False)
        print("✓ Message created (validation skipped)")
        print(f"  Action: {message.content['action']}")
        print("  → Use validate=False for custom extensions")
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
    print()


def demo_encoding_errors():
    """Demonstrate handling encoding/decoding errors."""
    print_header("2. Encoding/Decoding Error Handling")

    print("Testing encoding error scenarios...\n")

    # Invalid JSON decoding
    print("Test 1: Decode invalid JSON")
    try:
        invalid_json = b"{'not': 'valid json'}"
        message = PulseMessage.from_json(invalid_json.decode())
    except Exception as e:
        print(f"✓ Caught error: {type(e).__name__}")
        print(f"  Message: {str(e)[:60]}...")
        print("  → Validate JSON format before decoding")
    print()

    # Invalid binary decoding
    print("Test 2: Decode invalid binary data")
    try:
        invalid_binary = b"\x00\x01\x02\x03\x04"
        message = PulseMessage.from_binary(invalid_binary)
    except DecodingError as e:
        print(f"✓ Caught DecodingError: {str(e)[:60]}...")
        print("  → Verify data format matches decoder")
    print()

    # Safe decoding pattern
    print("Test 3: Safe decoding with try/except")
    data = b'{"envelope": {}, "type": "REQUEST", "content": {"action": "ACT.QUERY.DATA"}}'

    try:
        message = PulseMessage.from_json(data.decode())
        print("✓ Successfully decoded message")
        print(f"  Action: {message.content['action']}")
    except (DecodingError, ValidationError) as e:
        print(f"✗ Decoding failed: {e}")
        # Fallback strategy
        print("  → Applying fallback strategy...")
    print()


def demo_error_response_messages():
    """Create proper error response messages."""
    print_header("3. Creating Error Response Messages")

    print("Creating different types of error responses...\n")

    # Validation error response
    print("Error Type 1: Validation Error")
    validation_error = PulseMessage(action="META.ERROR.VALIDATION", validate=False)
    validation_error.type = "ERROR"
    validation_error.content = {
        "error_code": "META.ERROR.VALIDATION",
        "message": "Invalid parameter 'limit': must be positive integer",
        "details": {"field": "limit", "provided": "-10", "expected": "integer > 0"},
        "suggestion": "Provide a positive integer for the limit parameter",
    }
    print(f"  Code: {validation_error.content['error_code']}")
    print(f"  Message: {validation_error.content['message']}")
    print(f"  Suggestion: {validation_error.content['suggestion']}")
    print()

    # Not found error response
    print("Error Type 2: Not Found Error")
    not_found_error = PulseMessage(action="META.ERROR.NOT_FOUND", validate=False)
    not_found_error.type = "ERROR"
    not_found_error.content = {
        "error_code": "META.ERROR.NOT_FOUND",
        "message": "Resource not found: user with ID 'user-12345'",
        "details": {"resource_type": "user", "resource_id": "user-12345"},
        "suggestion": "Verify the resource ID exists in the system",
    }
    print(f"  Code: {not_found_error.content['error_code']}")
    print(f"  Message: {not_found_error.content['message']}")
    print()

    # Timeout error response
    print("Error Type 3: Timeout Error")
    timeout_error = PulseMessage(action="META.ERROR.TIMEOUT", validate=False)
    timeout_error.type = "ERROR"
    timeout_error.content = {
        "error_code": "META.ERROR.TIMEOUT",
        "message": "Operation timed out after 30 seconds",
        "details": {"timeout_seconds": 30, "operation": "database_query"},
        "retry_after": 60,
        "suggestion": "Consider increasing timeout or optimizing query",
    }
    print(f"  Code: {timeout_error.content['error_code']}")
    print(f"  Message: {timeout_error.content['message']}")
    print(f"  Retry after: {timeout_error.content['retry_after']}s")
    print()


def demo_retry_strategy():
    """Demonstrate retry strategies for failed operations."""
    print_header("4. Retry Strategies")

    print("Implementing exponential backoff retry...\n")

    def simulate_flaky_operation(attempt):
        """Simulate operation that fails sometimes."""
        if attempt < 3:
            raise ConnectionError(f"Network error on attempt {attempt}")
        return "Success!"

    max_retries = 5
    base_delay = 0.1  # 100ms

    print("Attempting operation with exponential backoff:")
    for attempt in range(1, max_retries + 1):
        try:
            print(f"  Attempt {attempt}...", end=" ")
            result = simulate_flaky_operation(attempt)
            print(f"✓ {result}")
            break
        except ConnectionError as e:
            print(f"✗ Failed: {e}")

            if attempt < max_retries:
                delay = base_delay * (2 ** (attempt - 1))
                print(f"    → Retrying in {delay:.1f}s")
                time.sleep(delay)
            else:
                print(f"    → Max retries reached, giving up")
    print()


def demo_error_recovery():
    """Demonstrate error recovery patterns."""
    print_header("5. Error Recovery Patterns")

    print("Pattern 1: Graceful Degradation\n")

    def process_with_fallback(data):
        """Process data with fallback to simpler method."""
        try:
            # Try primary method (binary encoding)
            message = PulseMessage(
                action="ACT.PROCESS.BATCH", parameters=data, validate=False
            )
            result = message.to_binary()
            print("  ✓ Primary method (binary): Success")
            return result
        except Exception as e:
            print(f"  ✗ Primary method failed: {type(e).__name__}")

            try:
                # Fallback to JSON
                message = PulseMessage(
                    action="ACT.PROCESS.BATCH", parameters={"simple": True}, validate=False
                )
                result = message.to_json()
                print("  ✓ Fallback method (JSON): Success")
                return result
            except Exception as e2:
                print(f"  ✗ Fallback also failed: {type(e2).__name__}")
                return None

    # Test with complex data
    complex_data = {"items": list(range(1000)), "nested": {"deep": {"data": "value"}}}
    result = process_with_fallback(complex_data)
    print(f"  Result: {type(result).__name__} ({len(result) if result else 0} bytes)")
    print()

    print("Pattern 2: Circuit Breaker\n")

    class CircuitBreaker:
        """Simple circuit breaker implementation."""

        def __init__(self, failure_threshold=3, timeout=10):
            self.failure_count = 0
            self.failure_threshold = failure_threshold
            self.timeout = timeout
            self.last_failure_time = None
            self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN

        def call(self, func):
            """Execute function with circuit breaker protection."""
            if self.state == "OPEN":
                if time.time() - self.last_failure_time > self.timeout:
                    self.state = "HALF_OPEN"
                    print(f"    Circuit: HALF_OPEN (testing)")
                else:
                    print(f"    Circuit: OPEN (blocking call)")
                    raise Exception("Circuit breaker is OPEN")

            try:
                result = func()
                if self.state == "HALF_OPEN":
                    self.state = "CLOSED"
                    self.failure_count = 0
                    print(f"    Circuit: CLOSED (recovered)")
                return result
            except Exception as e:
                self.failure_count += 1
                self.last_failure_time = time.time()

                if self.failure_count >= self.failure_threshold:
                    self.state = "OPEN"
                    print(f"    Circuit: OPEN (too many failures)")

                raise e

    breaker = CircuitBreaker(failure_threshold=2, timeout=1)

    def flaky_service():
        """Simulate flaky service."""
        import random

        if random.random() < 0.7:
            raise ConnectionError("Service unavailable")
        return "Success"

    print("  Testing circuit breaker:")
    for i in range(5):
        try:
            result = breaker.call(flaky_service)
            print(f"  Attempt {i+1}: ✓ {result}")
        except Exception as e:
            print(f"  Attempt {i+1}: ✗ {type(e).__name__}")

        time.sleep(0.2)
    print()


def demo_best_practices():
    """Show error handling best practices."""
    print_header("6. Error Handling Best Practices")

    print("✓ Best Practices:\n")

    print("1. Always validate input early")
    print("   try:")
    print("       message = PulseMessage(action=user_input)")
    print("   except ValidationError as e:")
    print("       return error_response(e)")
    print()

    print("2. Use specific exception types")
    print("   except ValidationError: # Handle validation issues")
    print("   except EncodingError:   # Handle encoding failures")
    print("   except DecodingError:   # Handle decoding failures")
    print()

    print("3. Provide helpful error messages")
    print("   error_msg = f'Invalid action: {action}. Did you mean: {suggestions}?'")
    print()

    print("4. Implement retry with backoff")
    print("   for attempt in range(max_retries):")
    print("       try: return operation()")
    print("       except TransientError: time.sleep(2 ** attempt)")
    print()

    print("5. Use circuit breakers for external services")
    print("   if circuit_breaker.is_open():")
    print("       return cached_response()")
    print()

    print("6. Log errors with context")
    print("   logger.error(f'Operation failed', extra={")
    print("       'message_id': msg.envelope['message_id'],")
    print("       'action': msg.content['action'],")
    print("       'error': str(e)")
    print("   })")
    print()


def main():
    """Run all error handling demonstrations."""
    print("\n" + "=" * 70)
    print("  PULSE Protocol - Error Handling Patterns")
    print("=" * 70)

    demo_validation_errors()
    demo_encoding_errors()
    demo_error_response_messages()
    demo_retry_strategy()
    demo_error_recovery()
    demo_best_practices()

    print_header("Summary")
    print("Key Takeaways:")
    print("  • Validate early, fail fast")
    print("  • Use specific exception types")
    print("  • Provide helpful error messages with suggestions")
    print("  • Implement retry strategies for transient failures")
    print("  • Use circuit breakers for external services")
    print("  • Create proper error response messages")
    print("  • Always log errors with sufficient context")
    print()
    print("=" * 70)
    print()


if __name__ == "__main__":
    main()
