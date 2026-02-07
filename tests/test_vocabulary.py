"""Tests for PULSE vocabulary system."""
import pytest
from pulse.vocabulary import Vocabulary


class TestVocabularyValidation:
    """Test concept validation."""

    def test_validate_existing_concept(self):
        """Test validation of existing concept returns True."""
        assert Vocabulary.validate_concept("ACT.QUERY.DATA") is True

    def test_validate_nonexistent_concept(self):
        """Test validation of non-existent concept returns False."""
        assert Vocabulary.validate_concept("INVALID.CONCEPT") is False

    def test_validate_empty_string(self):
        """Test validation of empty string returns False."""
        assert Vocabulary.validate_concept("") is False

    def test_validate_all_categories(self):
        """Test concepts from all categories validate correctly."""
        test_concepts = [
            "ENT.DATA.TEXT",
            "ACT.QUERY.DATA",
            "PROP.STATE.ACTIVE",
            "REL.CONTAINS",
            "LOG.AND",
            "MATH.ADD",
            "TIME.NOW",
            "SPACE.INSIDE",
            "DATA.LIST",
            "META.STATUS.SUCCESS",
        ]
        for concept in test_concepts:
            assert Vocabulary.validate_concept(concept) is True


class TestVocabularyCategories:
    """Test category operations."""

    def test_get_category_of_action(self):
        """Test getting category of action concept."""
        assert Vocabulary.get_category("ACT.QUERY.DATA") == "ACT"

    def test_get_category_of_entity(self):
        """Test getting category of entity concept."""
        assert Vocabulary.get_category("ENT.DATA.TEXT") == "ENT"

    def test_get_category_nonexistent(self):
        """Test getting category of non-existent concept returns None."""
        assert Vocabulary.get_category("INVALID.CONCEPT") is None

    def test_get_all_categories(self):
        """Test getting all categories."""
        categories = Vocabulary.get_all_categories()
        expected = {"ENT", "ACT", "PROP", "REL", "LOG", "MATH", "TIME", "SPACE", "DATA", "META"}
        assert categories == expected

    def test_list_by_category_act(self):
        """Test listing concepts by ACT category."""
        actions = Vocabulary.list_by_category("ACT")
        assert len(actions) > 0
        assert all(concept.startswith("ACT.") for concept in actions)

    def test_list_by_category_ent(self):
        """Test listing concepts by ENT category."""
        entities = Vocabulary.list_by_category("ENT")
        assert len(entities) > 0
        assert all(concept.startswith("ENT.") for concept in entities)

    def test_count_by_category(self):
        """Test counting concepts by category."""
        counts = Vocabulary.count_by_category()
        assert isinstance(counts, dict)
        assert all(count > 0 for count in counts.values())
        assert "ACT" in counts
        assert "ENT" in counts


class TestVocabularyDescriptions:
    """Test description and documentation."""

    def test_get_description(self):
        """Test getting concept description."""
        desc = Vocabulary.get_description("ACT.QUERY.DATA")
        assert desc == "Query for data or information"

    def test_get_description_nonexistent(self):
        """Test getting description of non-existent concept."""
        assert Vocabulary.get_description("INVALID.CONCEPT") is None

    def test_get_examples(self):
        """Test getting concept examples."""
        examples = Vocabulary.get_examples("ACT.QUERY.DATA")
        assert isinstance(examples, list)
        assert len(examples) > 0
        assert "fetch" in examples or "get" in examples

    def test_get_examples_nonexistent(self):
        """Test getting examples of non-existent concept."""
        assert Vocabulary.get_examples("INVALID.CONCEPT") == []


class TestVocabularySearch:
    """Test vocabulary search functionality."""

    def test_search_by_concept_id(self):
        """Test searching by concept ID."""
        results = Vocabulary.search("QUERY")
        assert len(results) > 0
        assert "ACT.QUERY.DATA" in results

    def test_search_by_description(self):
        """Test searching by description."""
        results = Vocabulary.search("sentiment")
        assert len(results) > 0
        assert "ACT.ANALYZE.SENTIMENT" in results

    def test_search_by_example(self):
        """Test searching by example."""
        results = Vocabulary.search("fetch")
        assert len(results) > 0
        # Should find ACT.QUERY.DATA which has "fetch" in examples

    def test_search_case_insensitive(self):
        """Test search is case insensitive."""
        results_lower = Vocabulary.search("query")
        results_upper = Vocabulary.search("QUERY")
        results_mixed = Vocabulary.search("QuErY")
        assert results_lower == results_upper == results_mixed

    def test_search_no_results(self):
        """Test search with no matches returns empty list."""
        results = Vocabulary.search("xyz123nonexistent")
        assert results == []


class TestVocabularyCounts:
    """Test vocabulary counting functions."""

    def test_get_total_count(self):
        """Test getting total concept count."""
        count = Vocabulary.get_total_count()
        assert count > 100  # Should have 100+ concepts
        assert isinstance(count, int)

    def test_total_matches_sum_of_categories(self):
        """Test total count matches sum of all categories."""
        total = Vocabulary.get_total_count()
        counts = Vocabulary.count_by_category()
        sum_of_categories = sum(counts.values())
        assert total == sum_of_categories


class TestVocabularyIntegrity:
    """Test vocabulary data integrity."""

    def test_all_concepts_have_category(self):
        """Test all concepts have a category field."""
        for concept, data in Vocabulary.CONCEPTS.items():
            assert "category" in data
            assert isinstance(data["category"], str)
            assert len(data["category"]) > 0

    def test_all_concepts_have_description(self):
        """Test all concepts have a description."""
        for concept, data in Vocabulary.CONCEPTS.items():
            assert "description" in data
            assert isinstance(data["description"], str)
            assert len(data["description"]) > 0

    def test_all_concepts_have_examples(self):
        """Test all concepts have examples."""
        for concept, data in Vocabulary.CONCEPTS.items():
            assert "examples" in data
            assert isinstance(data["examples"], list)
            assert len(data["examples"]) > 0

    def test_concept_ids_match_category(self):
        """Test concept IDs start with their category."""
        for concept, data in Vocabulary.CONCEPTS.items():
            category = data["category"]
            assert concept.startswith(f"{category}."), f"{concept} should start with {category}."
