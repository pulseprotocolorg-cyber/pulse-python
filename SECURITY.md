# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.4.x   | :white_check_mark: |
| < 0.4   | :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability, please email:

**security@pulse-protocol.org** (placeholder - update before publishing)

We will respond within 48 hours.

Please do NOT open public issues for security vulnerabilities.

## Security Features

- HMAC-SHA256 message signing
- Replay protection (timestamp + nonce)
- Tamper detection
- Constant-time signature comparison

## Best Practices

1. Always verify signatures in production
2. Use TLS for network transmission
3. Rotate keys regularly
4. Store keys securely (not in code)
