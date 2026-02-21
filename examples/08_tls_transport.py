#!/usr/bin/env python3
"""
PULSE Protocol - TLS Transport Example

Demonstrates:
1. Generating self-signed certificates for development
2. Creating a TLS-enabled (HTTPS) PULSE server
3. Connecting a client over HTTPS
4. Combining TLS with HMAC message signing (defense in depth)
5. Health checks over HTTPS

This implements Security Layer 1 (Transport) of the
PULSE 7-layer security model.
"""
import time
import threading
from pulse import (
    PulseMessage,
    PulseClient,
    PulseServer,
    SecurityManager,
    TLSConfig,
    generate_self_signed_cert,
)


def main():
    print("=" * 60)
    print("PULSE Protocol - TLS Transport Example")
    print("=" * 60)

    # ----------------------------------------------------------------
    # Step 1: Generate self-signed certificates
    # ----------------------------------------------------------------
    print("\n[1] Generating self-signed TLS certificates...")
    cert_path, key_path = generate_self_signed_cert(
        hostname="localhost",
        org_name="PULSE Protocol Example",
        days_valid=30,
    )
    print(f"    Certificate: {cert_path}")
    print(f"    Private key: {key_path}")
    print("    (In production, use certificates from a trusted CA)")

    # ----------------------------------------------------------------
    # Step 2: Create TLS-enabled server
    # ----------------------------------------------------------------
    print("\n[2] Starting HTTPS server...")
    tls_config = TLSConfig(certfile=cert_path, keyfile=key_path)

    # Also add HMAC signing for defense in depth
    shared_key = SecurityManager.generate_key()
    server_security = SecurityManager(secret_key=shared_key)

    server = PulseServer(
        host="127.0.0.1",
        port=8443,
        agent_id="secure-server",
        tls=tls_config,
        security=server_security,
    )

    # Register a handler
    def handle_query(message):
        """Handle incoming queries with a response."""
        action = message.content.get("action", "unknown")
        sender = message.envelope.get("sender", "unknown")
        print(f"    Server received: {action} from {sender}")

        response = PulseMessage(action="ACT.QUERY.DATA")
        response.type = "RESPONSE"
        response.content["parameters"] = {
            "status": "processed",
            "original_action": action,
            "transport": "TLS 1.2+",
            "signing": "HMAC-SHA256",
        }
        return response

    server.add_handler("*", handle_query)

    # Start server in background
    server.start(blocking=False)
    print(f"    Server running at {server.url}")
    print(f"    TLS enabled: {server.tls is not None}")

    # Give server time to start
    time.sleep(0.5)

    # ----------------------------------------------------------------
    # Step 3: Create HTTPS client
    # ----------------------------------------------------------------
    print("\n[3] Creating HTTPS client...")

    # For self-signed certs, we trust our own CA
    client_tls = TLSConfig(cafile=cert_path)
    client_security = SecurityManager(secret_key=shared_key)

    client = PulseClient(
        f"https://127.0.0.1:8443",
        agent_id="secure-client",
        security=client_security,
        tls=client_tls,
    )
    print(f"    Client: {client}")

    # ----------------------------------------------------------------
    # Step 4: Health check over HTTPS
    # ----------------------------------------------------------------
    print("\n[4] Health check over HTTPS...")
    health = client.ping()
    print(f"    Status: {health['status']}")
    print(f"    Latency: {health['latency_ms']}ms")

    # ----------------------------------------------------------------
    # Step 5: Send messages over HTTPS
    # ----------------------------------------------------------------
    print("\n[5] Sending messages over HTTPS with HMAC signing...")

    # Query message
    msg1 = PulseMessage(
        action="ACT.QUERY.DATA",
        target="ENT.DATA.TEXT",
        parameters={"query": "What is PULSE Protocol?"},
    )
    response1 = client.send(msg1)
    print(f"    Response: {response1.content['parameters']}")

    # Analysis message
    msg2 = PulseMessage(
        action="ACT.ANALYZE.SENTIMENT",
        target="ENT.DATA.TEXT",
        parameters={"text": "TLS transport is working!"},
    )
    response2 = client.send(msg2)
    print(f"    Response: {response2.content['parameters']}")

    # ----------------------------------------------------------------
    # Step 6: Client stats
    # ----------------------------------------------------------------
    print("\n[6] Client statistics:")
    stats = client.stats
    print(f"    Messages sent: {stats['messages_sent']}")
    print(f"    Bytes sent: {stats['bytes_sent']}")
    print(f"    Bytes received: {stats['bytes_received']}")

    # ----------------------------------------------------------------
    # Step 7: Server stats
    # ----------------------------------------------------------------
    print("\n[7] Server statistics:")
    server_stats = server.stats
    print(f"    Messages received: {server_stats['messages_received']}")

    # ----------------------------------------------------------------
    # Cleanup
    # ----------------------------------------------------------------
    print("\n[8] Shutting down server...")
    server.stop()
    print("    Server stopped.")

    # ----------------------------------------------------------------
    # Summary
    # ----------------------------------------------------------------
    print("\n" + "=" * 60)
    print("Security layers demonstrated:")
    print("  Layer 1: TLS 1.2+ transport encryption")
    print("  Layer 2: HMAC-SHA256 message signing")
    print("  Layer 5: Replay protection (nonce + timestamp)")
    print("  Layer 6: Audit trail (server logging)")
    print("")
    print("In production:")
    print("  - Use certificates from a trusted CA (Let's Encrypt, etc.)")
    print("  - Enable mutual TLS (mTLS) for agent authentication")
    print("  - Use TLS 1.3 for best security")
    print("  - Store keys in a secrets manager (Vault, AWS SM, etc.)")
    print("=" * 60)


if __name__ == "__main__":
    main()
