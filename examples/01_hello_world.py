"""
PULSE Protocol - Hello World Example.

This is the simplest possible PULSE message example.
Demonstrates creating a message and serializing it to JSON.
"""

from pulse import PulseMessage


def main():
    """Run Hello World example."""
    print("=" * 60)
    print("PULSE Protocol - Hello World Example")
    print("=" * 60)
    print()

    # Create a simple PULSE message
    message = PulseMessage(
        action="ACT.QUERY.DATA",
        target="ENT.DATA.TEXT",
        parameters={"query": "hello world"},
        sender="hello-world-agent",
    )

    print("Created PULSE Message:")
    print("-" * 60)
    print(message.to_json())
    print("-" * 60)
    print()

    # Show message details
    print("Message Details:")
    print(f"  Action: {message.content['action']}")
    print(f"  Target: {message.content['object']}")
    print(f"  Sender: {message.envelope['sender']}")
    print(f"  Message ID: {message.envelope['message_id']}")
    print(f"  Timestamp: {message.envelope['timestamp']}")
    print(f"  Type: {message.type}")
    print()

    # Test JSON roundtrip
    print("Testing JSON Roundtrip:")
    print("-" * 60)
    json_str = message.to_json()
    recreated = PulseMessage.from_json(json_str)

    print(f"Original action:   {message.content['action']}")
    print(f"Recreated action:  {recreated.content['action']}")
    print(f"Match: {message.content['action'] == recreated.content['action']}")
    print()

    print("=" * 60)
    print("✓ Hello World example completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
