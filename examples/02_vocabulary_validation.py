"""
PULSE Protocol - Vocabulary and Validation Example.

This example demonstrates:
1. Using different vocabulary concepts
2. Message validation
3. Handling validation errors
4. Vocabulary search functionality
"""

from pulse import PulseMessage, Vocabulary, MessageValidator, ValidationError


def print_section(title):
    """Print a section header."""
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def example_vocabulary_categories():
    """Demonstrate vocabulary categories."""
    print_section("1. Vocabulary Categories")

    categories = Vocabulary.get_all_categories()
    print(f"Available categories: {sorted(categories)}")
    print()

    counts = Vocabulary.count_by_category()
    print("Concepts per category:")
    for cat in sorted(counts.keys()):
        count = counts[cat]
        print(f"  {cat}: {count} concepts")

    print(f"\nTotal concepts: {Vocabulary.get_total_count()}")


def example_vocabulary_search():
    """Demonstrate vocabulary search."""
    print_section("2. Vocabulary Search")

    # Search for sentiment-related concepts
    print("Searching for 'sentiment':")
    results = Vocabulary.search("sentiment")
    for concept in results:
        desc = Vocabulary.get_description(concept)
        print(f"  {concept}: {desc}")

    print("\nSearching for 'query':")
    results = Vocabulary.search("query")
    for concept in results[:5]:  # Show first 5
        desc = Vocabulary.get_description(concept)
        print(f"  {concept}: {desc}")

    print("\nSearching for 'data':")
    results = Vocabulary.search("data")
    print(f"  Found {len(results)} concepts containing 'data'")


def example_valid_messages():
    """Create valid messages with different concepts."""
    print_section("3. Creating Valid Messages")

    examples = [
        {
            "name": "Sentiment Analysis",
            "action": "ACT.ANALYZE.SENTIMENT",
            "target": "ENT.DATA.TEXT",
            "params": {"text": "I love PULSE Protocol!"},
        },
        {
            "name": "Data Query",
            "action": "ACT.QUERY.DATA",
            "target": "ENT.RESOURCE.DATABASE",
            "params": {"table": "users", "limit": 10},
        },
        {
            "name": "Text Generation",
            "action": "ACT.CREATE.TEXT",
            "target": "ENT.DATA.TEXT",
            "params": {"prompt": "Write a poem", "max_length": 100},
        },
        {
            "name": "Image Classification",
            "action": "ACT.ANALYZE.CLASSIFY",
            "target": "ENT.DATA.IMAGE",
            "params": {"model": "resnet50"},
        },
    ]

    for ex in examples:
        message = PulseMessage(
            action=ex["action"], target=ex["target"], parameters=ex["params"]
        )
        print(f"\n✓ {ex['name']}:")
        print(f"  Action: {ex['action']}")
        print(f"  Target: {ex['target']}")
        print(f"  Valid: {MessageValidator.validate_message(message, check_freshness=False)}")


def example_invalid_messages():
    """Demonstrate validation errors."""
    print_section("4. Validation Errors")

    print("\nTrying to create message with invalid action:")
    try:
        message = PulseMessage(action="INVALID.ACTION")
    except ValidationError as e:
        print(f"✗ ValidationError: {e}")

    print("\nTrying to create message with invalid target:")
    try:
        message = PulseMessage(action="ACT.QUERY.DATA", target="INVALID.TARGET")
    except ValidationError as e:
        print(f"✗ ValidationError: {e}")

    print("\nSkipping validation on creation, then validating manually:")
    message = PulseMessage(action="ACT.QUERY.DATA", target="INVALID.TARGET", validate=False)
    print("✓ Message created (validation skipped)")

    try:
        message.validate()
    except ValidationError as e:
        print(f"✗ Manual validation failed: {e}")


def example_concept_details():
    """Show detailed concept information."""
    print_section("5. Concept Details")

    concept = "ACT.ANALYZE.SENTIMENT"
    print(f"Concept: {concept}")
    print(f"  Category: {Vocabulary.get_category(concept)}")
    print(f"  Description: {Vocabulary.get_description(concept)}")
    print(f"  Examples: {', '.join(Vocabulary.get_examples(concept))}")

    print(f"\nConcept: ENT.DATA.TEXT")
    print(f"  Category: {Vocabulary.get_category('ENT.DATA.TEXT')}")
    print(f"  Description: {Vocabulary.get_description('ENT.DATA.TEXT')}")
    print(f"  Examples: {', '.join(Vocabulary.get_examples('ENT.DATA.TEXT'))}")


def example_list_by_category():
    """List concepts by category."""
    print_section("6. List Concepts by Category")

    # List action concepts
    actions = Vocabulary.list_by_category("ACT")
    print(f"ACT (Actions) - {len(actions)} concepts:")
    for concept in sorted(actions)[:10]:  # Show first 10
        print(f"  {concept}")
    if len(actions) > 10:
        print(f"  ... and {len(actions) - 10} more")

    # List entity concepts
    print(f"\nENT (Entities) - {len(Vocabulary.list_by_category('ENT'))} concepts:")
    entities = Vocabulary.list_by_category("ENT")
    for concept in sorted(entities)[:10]:  # Show first 10
        print(f"  {concept}")
    if len(entities) > 10:
        print(f"  ... and {len(entities) - 10} more")


def main():
    """Run all examples."""
    print("=" * 60)
    print("PULSE Protocol - Vocabulary & Validation Demo")
    print("=" * 60)

    example_vocabulary_categories()
    example_vocabulary_search()
    example_valid_messages()
    example_invalid_messages()
    example_concept_details()
    example_list_by_category()

    print("\n" + "=" * 60)
    print("✓ Demo completed successfully!")
    print("=" * 60)
    print("\nKey Takeaways:")
    print("  • PULSE has 120+ semantic concepts across 10 categories")
    print("  • All concepts are validated automatically")
    print("  • Invalid concepts provide helpful suggestions")
    print("  • You can search vocabulary by keyword")
    print("  • Validation can be skipped if needed")
    print()


if __name__ == "__main__":
    main()
