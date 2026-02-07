"""
PULSE Protocol - Practical Use Cases.

This example demonstrates real-world use cases for PULSE Protocol:
1. Sentiment Analysis Pipeline
2. Database Query System
3. Text Generation Service
4. Multi-Agent Communication
5. Error Handling and Responses
"""

from pulse import PulseMessage, Vocabulary, ValidationError
import json


def print_header(title):
    """Print a section header."""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70 + "\n")


def use_case_1_sentiment_analysis():
    """Use Case 1: Sentiment Analysis Pipeline."""
    print_header("USE CASE 1: Sentiment Analysis Pipeline")

    # Customer feedback texts
    feedbacks = [
        "I absolutely love this product! Best purchase ever!",
        "Terrible experience. Very disappointed with the service.",
        "It's okay, nothing special but works as expected.",
    ]

    print("Analyzing customer feedback with PULSE...\n")

    for i, feedback in enumerate(feedbacks, 1):
        # Create sentiment analysis request
        request = PulseMessage(
            action="ACT.ANALYZE.SENTIMENT",
            target="ENT.DATA.TEXT",
            parameters={
                "text": feedback,
                "detail_level": "PROP.DETAIL.HIGH",
                "include_confidence": True,
            },
            sender="feedback-analyzer",
        )

        print(f"Feedback {i}: \"{feedback[:50]}...\"")
        print(f"  Request ID: {request.envelope['message_id']}")
        print(f"  Action: {request.content['action']}")
        print(f"  Target: {request.content['object']}")
        print()

    print("✓ All feedback requests created successfully")


def use_case_2_database_query():
    """Use Case 2: Database Query System."""
    print_header("USE CASE 2: Database Query System")

    # Different types of database queries
    queries = [
        {
            "name": "Get Active Users",
            "table": "users",
            "filters": {"status": "active"},
            "limit": 100,
        },
        {
            "name": "Recent Orders",
            "table": "orders",
            "filters": {"created_date": "PROP.TIME.RECENT"},
            "sort": {"field": "created_date", "order": "DESC"},
            "limit": 50,
        },
        {
            "name": "High Priority Tasks",
            "table": "tasks",
            "filters": {"priority": "PROP.PRIORITY.HIGH", "status": "PROP.STATE.PENDING"},
        },
    ]

    print("Creating database query requests...\n")

    for query_spec in queries:
        request = PulseMessage(
            action="ACT.QUERY.DATA",
            target="ENT.RESOURCE.DATABASE",
            parameters=query_spec,
            sender="query-service",
        )

        print(f"Query: {query_spec['name']}")
        print(f"  Message ID: {request.envelope['message_id']}")
        print(f"  Table: {query_spec['table']}")
        print(f"  Filters: {query_spec.get('filters', {})}")
        print()

    print("✓ All database queries created successfully")


def use_case_3_text_generation():
    """Use Case 3: Text Generation Service."""
    print_header("USE CASE 3: Text Generation Service")

    # Different text generation tasks
    tasks = [
        {
            "type": "Product Description",
            "prompt": "Write a compelling product description for a smart watch",
            "max_length": 200,
            "tone": "professional",
        },
        {
            "type": "Email Response",
            "prompt": "Draft a friendly response to a customer inquiry",
            "max_length": 150,
            "tone": "friendly",
        },
        {
            "type": "Social Media Post",
            "prompt": "Create an engaging tweet about AI technology",
            "max_length": 280,
            "tone": "casual",
        },
    ]

    print("Generating text with AI agents...\n")

    for task in tasks:
        request = PulseMessage(
            action="ACT.CREATE.TEXT",
            target="ENT.DATA.TEXT",
            parameters={
                "prompt": task["prompt"],
                "max_length": task["max_length"],
                "style": task["tone"],
                "quality": "PROP.QUALITY.HIGH",
            },
            sender="content-generator",
        )

        print(f"Task: {task['type']}")
        print(f"  Prompt: {task['prompt']}")
        print(f"  Max Length: {task['max_length']} chars")
        print(f"  Tone: {task['tone']}")
        print(f"  Message ID: {request.envelope['message_id'][:8]}...")
        print()

    print("✓ All text generation requests created")


def use_case_4_multi_agent_communication():
    """Use Case 4: Multi-Agent Communication."""
    print_header("USE CASE 4: Multi-Agent Communication")

    print("Simulating multi-agent workflow...\n")

    # Agent 1: Data Collector sends query to Data Service
    step1 = PulseMessage(
        action="ACT.QUERY.DATA",
        target="ENT.RESOURCE.DATABASE",
        parameters={"table": "sales_data", "period": "last_month"},
        sender="data-collector",
    )
    step1.envelope["receiver"] = "data-service"

    print("Step 1: Data Collector → Data Service")
    print(f"  Action: {step1.content['action']}")
    print(f"  Sender: {step1.envelope['sender']}")
    print(f"  Receiver: {step1.envelope['receiver']}")
    print()

    # Agent 2: Data Service sends data to Analysis Service
    step2 = PulseMessage(
        action="ACT.TRANSFORM.CONVERT",
        target="ENT.DATA.JSON",
        parameters={"format": "normalized", "include_metadata": True},
        sender="data-service",
    )
    step2.envelope["receiver"] = "analysis-service"
    step2.type = "RESPONSE"

    print("Step 2: Data Service → Analysis Service")
    print(f"  Action: {step2.content['action']}")
    print(f"  Type: {step2.type}")
    print(f"  Sender: {step2.envelope['sender']}")
    print(f"  Receiver: {step2.envelope['receiver']}")
    print()

    # Agent 3: Analysis Service requests processing
    step3 = PulseMessage(
        action="ACT.ANALYZE.STATISTICS",
        target="ENT.DATA.NUMBER",
        parameters={"metrics": ["average", "trend", "forecast"], "detail": "PROP.DETAIL.HIGH"},
        sender="analysis-service",
    )
    step3.envelope["receiver"] = "stats-processor"

    print("Step 3: Analysis Service → Stats Processor")
    print(f"  Action: {step3.content['action']}")
    print(f"  Sender: {step3.envelope['sender']}")
    print(f"  Receiver: {step3.envelope['receiver']}")
    print(f"  Metrics: {step3.content['parameters']['metrics']}")
    print()

    print("✓ Multi-agent workflow created successfully")


def use_case_5_error_handling():
    """Use Case 5: Error Handling and Responses."""
    print_header("USE CASE 5: Error Handling and Responses")

    print("Demonstrating error handling...\n")

    # Success Response
    print("1. Success Response:")
    success = PulseMessage(action="META.RESPONSE", validate=False)
    success.type = "RESPONSE"
    success.content = {
        "status": "META.STATUS.SUCCESS",
        "result": {"records": 150, "processing_time": "0.23s"},
        "message": "Query completed successfully",
    }
    print(f"  Status: {success.content['status']}")
    print(f"  Result: {success.content['result']}")
    print()

    # Validation Error
    print("2. Validation Error (caught automatically):")
    try:
        invalid = PulseMessage(action="INVALID.CONCEPT")
    except ValidationError as e:
        print(f"  ✗ Caught: {str(e)[:80]}...")
    print()

    # Error Response Message
    print("3. Error Response Message:")
    error = PulseMessage(action="META.ERROR.VALIDATION", validate=False)
    error.type = "ERROR"
    error.content = {
        "error_code": "META.ERROR.VALIDATION",
        "message": "Invalid parameter 'limit': must be positive integer",
        "details": {"field": "limit", "provided": -1, "expected": "> 0"},
        "suggestion": "Please provide a positive integer for limit parameter",
    }
    print(f"  Error Code: {error.content['error_code']}")
    print(f"  Message: {error.content['message']}")
    print(f"  Details: {error.content['details']}")
    print()

    # Network Error
    print("4. Network Error Response:")
    network_error = PulseMessage(action="META.ERROR.NETWORK", validate=False)
    network_error.type = "ERROR"
    network_error.content = {
        "error_code": "META.ERROR.NETWORK",
        "message": "Connection timeout to agent-service",
        "details": {"agent": "data-processor", "timeout": "30s"},
        "retry_after": 60,
    }
    print(f"  Error Code: {network_error.content['error_code']}")
    print(f"  Message: {network_error.content['message']}")
    print(f"  Retry After: {network_error.content['retry_after']}s")
    print()

    print("✓ Error handling examples complete")


def use_case_6_vocabulary_exploration():
    """Use Case 6: Exploring Available Capabilities."""
    print_header("USE CASE 6: Exploring Available Capabilities")

    print("Discovering what actions are available...\n")

    # Show available action categories
    actions = Vocabulary.list_by_category("ACT")
    analyze_actions = [a for a in actions if "ANALYZE" in a]

    print(f"Analysis Actions ({len(analyze_actions)} available):")
    for action in sorted(analyze_actions):
        desc = Vocabulary.get_description(action)
        print(f"  • {action}")
        print(f"    {desc}")
    print()

    # Show data types
    print("Supported Data Types:")
    data_types = Vocabulary.list_by_category("ENT")
    data_entities = [d for d in data_types if d.startswith("ENT.DATA")]
    for dtype in sorted(data_entities)[:8]:
        desc = Vocabulary.get_description(dtype)
        print(f"  • {dtype}: {desc}")
    print()

    # Show meta operations
    print("Protocol Status Codes:")
    meta_statuses = [m for m in Vocabulary.list_by_category("META") if "STATUS" in m]
    for status in sorted(meta_statuses):
        desc = Vocabulary.get_description(status)
        print(f"  • {status}: {desc}")
    print()

    print("✓ Vocabulary exploration complete")


def main():
    """Run all use case examples."""
    print("\n" + "="*70)
    print("  PULSE Protocol - Practical Use Cases Demo")
    print("  Demonstrating Real-World AI-to-AI Communication")
    print("="*70)

    use_case_1_sentiment_analysis()
    use_case_2_database_query()
    use_case_3_text_generation()
    use_case_4_multi_agent_communication()
    use_case_5_error_handling()
    use_case_6_vocabulary_exploration()

    print_header("Summary")
    print("This demo showed:")
    print("  ✓ Sentiment analysis pipeline")
    print("  ✓ Database query system")
    print("  ✓ Text generation service")
    print("  ✓ Multi-agent communication workflow")
    print("  ✓ Error handling patterns")
    print("  ✓ Vocabulary exploration")
    print()
    print("Key Benefits:")
    print("  • Unambiguous communication between AI systems")
    print("  • Type-safe message structure")
    print("  • Automatic validation")
    print("  • Discoverable capabilities via vocabulary")
    print("  • Standardized error handling")
    print()
    print("="*70)
    print()


if __name__ == "__main__":
    main()
