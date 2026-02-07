"""PULSE Protocol Performance Benchmarks.

Comprehensive performance testing suite for:
- Message creation
- JSON encoding/decoding
- Binary encoding/decoding
- Signing and verification
- Validation
- Vocabulary operations
"""
import time
from typing import Dict, Any, Callable
import statistics

from pulse import (
    PulseMessage,
    Encoder,
    SecurityManager,
    Vocabulary,
    ValidationError,
)


class BenchmarkResult:
    """Container for benchmark results."""

    def __init__(self, name: str):
        """Initialize benchmark result.

        Args:
            name: Benchmark name
        """
        self.name = name
        self.times = []
        self.iterations = 0

    def add_time(self, duration: float):
        """Add a timing measurement.

        Args:
            duration: Duration in seconds
        """
        self.times.append(duration)
        self.iterations += 1

    def get_stats(self) -> Dict[str, Any]:
        """Get statistical summary.

        Returns:
            Dictionary with mean, median, min, max, std
        """
        if not self.times:
            return {}

        return {
            'name': self.name,
            'iterations': self.iterations,
            'total_time': sum(self.times),
            'mean': statistics.mean(self.times),
            'median': statistics.median(self.times),
            'min': min(self.times),
            'max': max(self.times),
            'stdev': statistics.stdev(self.times) if len(self.times) > 1 else 0,
            'ops_per_sec': self.iterations / sum(self.times) if sum(self.times) > 0 else 0,
        }

    def __str__(self) -> str:
        """Format results as string."""
        stats = self.get_stats()
        if not stats:
            return f"{self.name}: No data"

        return (
            f"{self.name}:\n"
            f"  Iterations: {stats['iterations']}\n"
            f"  Total time: {stats['total_time']:.3f}s\n"
            f"  Mean: {stats['mean']*1000:.3f}ms\n"
            f"  Median: {stats['median']*1000:.3f}ms\n"
            f"  Min: {stats['min']*1000:.3f}ms\n"
            f"  Max: {stats['max']*1000:.3f}ms\n"
            f"  Stdev: {stats['stdev']*1000:.3f}ms\n"
            f"  Ops/sec: {stats['ops_per_sec']:.0f}"
        )


class PerformanceBenchmarks:
    """Performance benchmarks for PULSE Protocol."""

    def __init__(self, iterations: int = 1000):
        """Initialize benchmarks.

        Args:
            iterations: Number of iterations per benchmark
        """
        self.iterations = iterations
        self.results = {}

    def benchmark(self, name: str, func: Callable, *args, **kwargs) -> BenchmarkResult:
        """Run a benchmark.

        Args:
            name: Benchmark name
            func: Function to benchmark
            *args: Function arguments
            **kwargs: Function keyword arguments

        Returns:
            BenchmarkResult with timing data
        """
        result = BenchmarkResult(name)

        # Warmup
        for _ in range(min(10, self.iterations // 10)):
            func(*args, **kwargs)

        # Actual benchmark
        for _ in range(self.iterations):
            start = time.perf_counter()
            func(*args, **kwargs)
            duration = time.perf_counter() - start
            result.add_time(duration)

        self.results[name] = result
        return result

    def benchmark_message_creation(self):
        """Benchmark message creation."""
        print("\n=== Message Creation ===")

        # Simple message
        result = self.benchmark(
            "Create simple message",
            lambda: PulseMessage(action="ACT.QUERY.DATA", validate=False)
        )
        print(result)

        # Complex message
        result = self.benchmark(
            "Create complex message",
            lambda: PulseMessage(
                action="ACT.ANALYZE.SENTIMENT",
                target="ENT.DATA.TEXT",
                parameters={
                    "text": "Hello world",
                    "detail": "high",
                    "options": {"language": "en", "format": "json"}
                },
                validate=False
            )
        )
        print(result)

        # With validation
        result = self.benchmark(
            "Create with validation",
            lambda: PulseMessage(action="ACT.QUERY.DATA", validate=True)
        )
        print(result)

    def benchmark_json_encoding(self):
        """Benchmark JSON encoding/decoding."""
        print("\n=== JSON Encoding/Decoding ===")

        message = PulseMessage(
            action="ACT.QUERY.DATA",
            target="ENT.DATA.TEXT",
            parameters={"query": "test", "limit": 10},
            validate=False
        )

        # JSON encoding
        result = self.benchmark(
            "JSON encode",
            lambda: message.to_json(indent=None)
        )
        print(result)

        # JSON decoding
        json_str = message.to_json(indent=None)
        result = self.benchmark(
            "JSON decode",
            lambda: PulseMessage.from_json(json_str)
        )
        print(result)

        # JSON roundtrip
        def json_roundtrip():
            msg = PulseMessage(action="ACT.QUERY.DATA", validate=False)
            json_str = msg.to_json(indent=None)
            return PulseMessage.from_json(json_str)

        result = self.benchmark("JSON roundtrip", json_roundtrip)
        print(result)

    def benchmark_binary_encoding(self):
        """Benchmark binary encoding/decoding."""
        print("\n=== Binary Encoding/Decoding ===")

        message = PulseMessage(
            action="ACT.QUERY.DATA",
            target="ENT.DATA.TEXT",
            parameters={"query": "test", "limit": 10},
            validate=False
        )

        # Binary encoding
        result = self.benchmark(
            "Binary encode",
            lambda: message.to_binary()
        )
        print(result)

        # Binary decoding
        binary_data = message.to_binary()
        result = self.benchmark(
            "Binary decode",
            lambda: PulseMessage.from_binary(binary_data)
        )
        print(result)

        # Binary roundtrip
        def binary_roundtrip():
            msg = PulseMessage(action="ACT.QUERY.DATA", validate=False)
            binary = msg.to_binary()
            return PulseMessage.from_binary(binary)

        result = self.benchmark("Binary roundtrip", binary_roundtrip)
        print(result)

    def benchmark_security(self):
        """Benchmark security operations."""
        print("\n=== Security Operations ===")

        security = SecurityManager(secret_key="benchmark-key")
        message = PulseMessage(action="ACT.QUERY.DATA", validate=False)

        # Signing
        result = self.benchmark(
            "Sign message",
            lambda: security.sign_message(message)
        )
        print(result)

        # Verification (valid)
        security.sign_message(message)
        result = self.benchmark(
            "Verify signature (valid)",
            lambda: security.verify_signature(message)
        )
        print(result)

        # Replay protection check
        result = self.benchmark(
            "Replay protection check",
            lambda: security.check_replay_protection(message)
        )
        print(result)

    def benchmark_validation(self):
        """Benchmark validation operations."""
        print("\n=== Validation Operations ===")

        # Valid message validation
        message = PulseMessage(action="ACT.QUERY.DATA", validate=False)
        result = self.benchmark(
            "Validate valid message",
            lambda: message.validate(check_freshness=False)
        )
        print(result)

        # Envelope validation
        from pulse.validator import MessageValidator
        result = self.benchmark(
            "Validate envelope",
            lambda: MessageValidator.validate_envelope(message.envelope)
        )
        print(result)

        # Content validation
        result = self.benchmark(
            "Validate content",
            lambda: MessageValidator.validate_content(message.content)
        )
        print(result)

    def benchmark_vocabulary(self):
        """Benchmark vocabulary operations."""
        print("\n=== Vocabulary Operations ===")

        # Validate concept
        result = self.benchmark(
            "Validate concept",
            lambda: Vocabulary.validate_concept("ACT.QUERY.DATA")
        )
        print(result)

        # Search
        result = self.benchmark(
            "Search vocabulary",
            lambda: Vocabulary.search("query")
        )
        print(result)

        # Get category
        result = self.benchmark(
            "Get category",
            lambda: Vocabulary.get_category("ACT.QUERY.DATA")
        )
        print(result)

    def benchmark_encoder_comparison(self):
        """Benchmark encoder size comparison."""
        print("\n=== Encoder Size Comparison ===")

        encoder = Encoder()
        message = PulseMessage(
            action="ACT.QUERY.DATA",
            target="ENT.DATA.TEXT",
            parameters={"query": "test", "limit": 10},
            validate=False
        )

        result = self.benchmark(
            "Get size comparison",
            lambda: encoder.get_size_comparison(message)
        )
        print(result)

        # Show actual sizes
        sizes = encoder.get_size_comparison(message)
        print(f"\n  Actual sizes:")
        print(f"    JSON:   {sizes['json']} bytes")
        print(f"    Binary: {sizes['binary']} bytes")
        print(f"    Reduction: {sizes['binary_reduction']}×")
        print(f"    Savings: {sizes['savings_percent']}%")

    def run_all(self):
        """Run all benchmarks."""
        print("=" * 70)
        print("  PULSE Protocol Performance Benchmarks")
        print(f"  Iterations per test: {self.iterations}")
        print("=" * 70)

        start_time = time.time()

        self.benchmark_message_creation()
        self.benchmark_json_encoding()
        self.benchmark_binary_encoding()
        self.benchmark_security()
        self.benchmark_validation()
        self.benchmark_vocabulary()
        self.benchmark_encoder_comparison()

        total_time = time.time() - start_time

        print("\n" + "=" * 70)
        print(f"  Total benchmark time: {total_time:.2f}s")
        print("=" * 70)

    def get_summary(self) -> Dict[str, Any]:
        """Get summary of all benchmarks.

        Returns:
            Dictionary with all benchmark statistics
        """
        return {
            name: result.get_stats()
            for name, result in self.results.items()
        }


def run_benchmarks(iterations: int = 1000):
    """Run performance benchmarks.

    Args:
        iterations: Number of iterations per benchmark

    Returns:
        PerformanceBenchmarks instance with results
    """
    benchmarks = PerformanceBenchmarks(iterations=iterations)
    benchmarks.run_all()
    return benchmarks


if __name__ == '__main__':
    import sys

    # Get iterations from command line
    iterations = 1000
    if len(sys.argv) > 1:
        try:
            iterations = int(sys.argv[1])
        except ValueError:
            print(f"Invalid iterations: {sys.argv[1]}, using default: 1000")

    run_benchmarks(iterations=iterations)
