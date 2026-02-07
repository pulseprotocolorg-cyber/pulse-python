# PULSE Protocol - Python Implementation

**Protocol for Universal Language-based System Exchange**

Universal semantic protocol for AI-to-AI communication. Think "TCP/IP for Artificial Intelligence."

## 🚀 Quick Start

```bash
# Install
pip install pulse-protocol

# Create a message
from pulse import PulseMessage

message = PulseMessage(
    action="ACT.QUERY.DATA",
    target="ENT.DATA.TEXT",
    parameters={"query": "hello world"}
)

# Serialize to JSON
json_output = message.to_json()
print(json_output)
```

## 📦 Installation

```bash
pip install pulse-protocol
```

For development:

```bash
git clone https://github.com/pulse-protocol/pulse-python.git
cd pulse-python
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
pip install -e .
```

## 🧪 Running Tests

```bash
# Run all tests
pytest

# With coverage
pytest --cov=pulse --cov-report=html

# Specific test
pytest tests/test_message.py
```

## 📖 Documentation

- [Full Documentation](https://pulse-protocol.org/docs)
- [API Reference](https://pulse-protocol.org/api)
- [Examples](./examples/)

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.

## 📄 License

Apache License 2.0 - See [LICENSE](LICENSE) for details.

## 🌟 Features

- ✅ Universal semantic vocabulary (1,000 concepts)
- ✅ Three encoding formats (JSON, Binary, Compact)
- ✅ Enterprise-grade security (HMAC-SHA256, TLS 1.3)
- ✅ Replay attack protection
- ✅ 90%+ test coverage
- ✅ Type hints and full documentation

## 📊 Status

**Version:** 0.1.0 (Alpha)
**Python:** 3.8+
**License:** Apache 2.0

---

Built with ❤️ by the PULSE Protocol team
