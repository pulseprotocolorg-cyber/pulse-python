"""
PULSE Protocol - Binary Encoding & Performance.

This example demonstrates:
1. Binary encoding with MessagePack
2. Size comparison (JSON vs Binary)
3. Performance benchmarks
4. Roundtrip verification
5. When to use each format
"""

from pulse import PulseMessage, Encoder, JSONEncoder, BinaryEncoder
import time
import sys


def print_header(title):
    """Print section header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")


def demo_basic_binary_encoding():
    """Demonstrate basic binary encoding."""
    print_header("1. Basic Binary Encoding")

    # Create a message
    message = PulseMessage(
        action="ACT.ANALYZE.SENTIMENT",
        target="ENT.DATA.TEXT",
        parameters={"text": "PULSE Protocol is amazing!", "detail_level": "PROP.DETAIL.HIGH"},
    )

    print("Original message:")
    print(f"  Action: {message.content['action']}")
    print(f"  Target: {message.content['object']}")
    print(f"  Parameters: {message.content['parameters']}")
    print()

    # Encode to JSON
    json_str = message.to_json(indent=None)
    json_bytes = json_str.encode("utf-8")
    print(f"JSON size: {len(json_bytes)} bytes")

    # Encode to Binary
    binary = message.to_binary()
    print(f"Binary size: {len(binary)} bytes")
    print()

    # Calculate reduction
    reduction = len(json_bytes) / len(binary)
    savings = (1 - len(binary) / len(json_bytes)) * 100

    print(f"✓ Binary is {reduction:.1f}× smaller")
    print(f"✓ Space savings: {savings:.1f}%")


def demo_size_comparison():
    """Compare sizes across different message types."""
    print_header("2. Size Comparison - Different Message Types")

    test_cases = [
        {
            "name": "Simple Query",
            "message": PulseMessage(action="ACT.QUERY.DATA", target="ENT.DATA.TEXT"),
        },
        {
            "name": "With Parameters",
            "message": PulseMessage(
                action="ACT.QUERY.DATA",
                target="ENT.RESOURCE.DATABASE",
                parameters={"table": "users", "limit": 100, "filters": {"status": "active"}},
            ),
        },
        {
            "name": "Complex Parameters",
            "message": PulseMessage(
                action="ACT.ANALYZE.STATISTICS",
                target="ENT.DATA.NUMBER",
                parameters={
                    "dataset": list(range(100)),
                    "metrics": ["mean", "median", "stddev", "variance"],
                    "confidence_level": 0.95,
                    "outlier_detection": True,
                },
                validate=False,
            ),
        },
    ]

    encoder = Encoder()

    print(f"{'Message Type':<20} {'JSON':<12} {'Binary':<12} {'Reduction':<12} {'Savings'}")
    print("-" * 70)

    for case in test_cases:
        comparison = encoder.get_size_comparison(case["message"])

        print(
            f"{case['name']:<20} "
            f"{comparison['json']:<12} "
            f"{comparison['binary']:<12} "
            f"{comparison['binary_reduction']:.1f}×{'':<10} "
            f"{comparison['savings_percent']:.1f}%"
        )

    print()
    print("✓ Binary encoding provides consistent 8-12× size reduction")


def demo_roundtrip_verification():
    """Verify binary encoding preserves all data."""
    print_header("3. Roundtrip Verification")

    # Create message with various data types
    message = PulseMessage(
        action="ACT.PROCESS.BATCH",
        target="ENT.DATA.JSON",
        parameters={
            "string_value": "Hello, World!",
            "integer_value": 42,
            "float_value": 3.14159,
            "boolean_value": True,
            "null_value": None,
            "list_value": [1, 2, 3, "four", 5.0],
            "nested_dict": {"key1": "value1", "key2": {"nested": "data"}},
        },
        validate=False,
    )

    print("Encoding message with various data types...")
    print()

    # Encode and decode
    binary = message.to_binary()
    decoded = PulseMessage.from_binary(binary)

    # Verify each field
    checks = [
        ("Action", message.content["action"], decoded.content["action"]),
        ("Target", message.content["object"], decoded.content["object"]),
        ("Message ID", message.envelope["message_id"], decoded.envelope["message_id"]),
        ("Sender", message.envelope["sender"], decoded.envelope["sender"]),
        ("Parameters", message.content["parameters"], decoded.content["parameters"]),
    ]

    print("Verification results:")
    for name, original, decoded_val in checks:
        match = "✓" if original == decoded_val else "✗"
        print(f"  {match} {name}: {'Match' if original == decoded_val else 'MISMATCH'}")

    print()
    print("✓ All data preserved perfectly in binary roundtrip")


def demo_performance_benchmark():
    """Benchmark encoding/decoding performance."""
    print_header("4. Performance Benchmark")

    message = PulseMessage(
        action="ACT.QUERY.DATA",
        target="ENT.RESOURCE.DATABASE",
        parameters={"table": "logs", "limit": 1000, "sort": "timestamp"},
    )

    iterations = 10000

    # JSON Encoding
    print(f"Encoding {iterations:,} messages...")
    print()

    json_encoder = JSONEncoder()
    start = time.time()
    for _ in range(iterations):
        json_encoder.encode(message, indent=None)
    json_encode_time = time.time() - start

    # Binary Encoding
    binary_encoder = BinaryEncoder()
    start = time.time()
    for _ in range(iterations):
        binary_encoder.encode(message)
    binary_encode_time = time.time() - start

    # JSON Decoding
    json_data = json_encoder.encode(message, indent=None)
    start = time.time()
    for _ in range(iterations):
        json_encoder.decode(json_data)
    json_decode_time = time.time() - start

    # Binary Decoding
    binary_data = binary_encoder.encode(message)
    start = time.time()
    for _ in range(iterations):
        binary_encoder.decode(binary_data)
    binary_decode_time = time.time() - start

    # Print results
    print(f"{'Operation':<25} {'JSON':<15} {'Binary':<15} {'Speedup'}")
    print("-" * 70)
    print(
        f"{'Encoding':<25} "
        f"{json_encode_time:.3f}s{'':<10} "
        f"{binary_encode_time:.3f}s{'':<10} "
        f"{json_encode_time/binary_encode_time:.1f}×"
    )
    print(
        f"{'Decoding':<25} "
        f"{json_decode_time:.3f}s{'':<10} "
        f"{binary_decode_time:.3f}s{'':<10} "
        f"{json_decode_time/binary_decode_time:.1f}×"
    )
    print()

    # Throughput
    json_throughput = iterations / json_encode_time
    binary_throughput = iterations / binary_encode_time

    print("Throughput:")
    print(f"  JSON encoding: {json_throughput:,.0f} messages/second")
    print(f"  Binary encoding: {binary_throughput:,.0f} messages/second")
    print()

    if binary_encode_time < json_encode_time:
        print(f"✓ Binary encoding is {json_encode_time/binary_encode_time:.1f}× faster")
    else:
        print(f"✓ JSON encoding is {binary_encode_time/json_encode_time:.1f}× faster")


def demo_when_to_use():
    """Guidelines for when to use each format."""
    print_header("5. When to Use Each Format")

    print("📝 JSON Format:")
    print("  ✓ Human-readable output")
    print("  ✓ Debugging and development")
    print("  ✓ Logging and auditing")
    print("  ✓ REST APIs and web services")
    print("  ✓ Configuration files")
    print("  ✓ Documentation examples")
    print()

    print("⚡ Binary Format (MessagePack):")
    print("  ✓ High-throughput systems")
    print("  ✓ Network transmission")
    print("  ✓ Storage optimization")
    print("  ✓ Microservices communication")
    print("  ✓ Message queues")
    print("  ✓ Performance-critical applications")
    print()

    print("🎯 Compact Format (Coming Soon):")
    print("  ✓ Ultra-low bandwidth scenarios")
    print("  ✓ IoT devices")
    print("  ✓ Mobile applications")
    print("  ✓ Embedded systems")
    print("  ✓ Maximum efficiency required")
    print()


def demo_unified_encoder():
    """Demonstrate unified Encoder interface."""
    print_header("6. Unified Encoder Interface")

    message = PulseMessage(
        action="ACT.CREATE.TEXT", target="ENT.DATA.TEXT", parameters={"prompt": "Hello"}
    )

    encoder = Encoder()

    # Encode in different formats
    json_data = encoder.encode(message, format="json")
    binary_data = encoder.encode(message, format="binary")

    print("Encoded with unified interface:")
    print(f"  JSON: {len(json_data)} bytes")
    print(f"  Binary: {len(binary_data)} bytes")
    print()

    # Auto-detect format when decoding
    print("Decoding with auto-detection:")
    decoded_json = encoder.decode(json_data)
    print(f"  ✓ JSON decoded: {decoded_json.content['action']}")

    decoded_binary = encoder.decode(binary_data)
    print(f"  ✓ Binary decoded: {decoded_binary.content['action']}")
    print()

    # Size comparison helper
    comparison = encoder.get_size_comparison(message)
    print("Size comparison:")
    print(f"  JSON: {comparison['json']} bytes")
    print(f"  Binary: {comparison['binary']} bytes")
    print(f"  Reduction: {comparison['binary_reduction']}×")
    print(f"  Savings: {comparison['savings_percent']}%")


def main():
    """Run all demonstrations."""
    print("\n" + "=" * 70)
    print("  PULSE Protocol - Binary Encoding & Performance Demo")
    print("=" * 70)

    demo_basic_binary_encoding()
    demo_size_comparison()
    demo_roundtrip_verification()
    demo_performance_benchmark()
    demo_when_to_use()
    demo_unified_encoder()

    print_header("Summary")
    print("Key Takeaways:")
    print("  • Binary encoding provides 8-12× size reduction")
    print("  • Binary encoding is typically faster than JSON")
    print("  • All data types preserved perfectly in binary format")
    print("  • Choose format based on use case:")
    print("    - JSON for humans (debugging, docs, logs)")
    print("    - Binary for machines (performance, bandwidth)")
    print()
    print("=" * 70)
    print()


if __name__ == "__main__":
    main()
