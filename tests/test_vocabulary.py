"""Tests for PULSE vocabulary system.

Tests cover:
- Concept validation (existing, non-existent, all categories)
- Category operations (get, list, count)
- Descriptions and examples
- Search functionality
- Exact counts for all 10 categories (1000 total)
- Data integrity across all concepts
- New concepts from vocabulary expansion
"""
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
        """Test concepts from all 10 categories validate correctly."""
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
            assert Vocabulary.validate_concept(concept) is True, f"{concept} should be valid"

    def test_validate_new_ent_concepts(self):
        """Test new ENT concepts from expansion."""
        new_concepts = [
            "ENT.DATA.VECTOR",
            "ENT.AGENT.ORCHESTRATOR",
            "ENT.RESOURCE.GPU",
            "ENT.OBJECT.TOKEN",
            "ENT.DOMAIN.ML",
            "ENT.COMPONENT.SDK",
        ]
        for concept in new_concepts:
            assert Vocabulary.validate_concept(concept) is True, f"{concept} should be valid"

    def test_validate_new_act_concepts(self):
        """Test new ACT concepts from expansion."""
        new_concepts = [
            "ACT.SECURITY.AUTHENTICATE",
            "ACT.COMMUNICATE.SEND",
            "ACT.CONTROL.START",
            "ACT.MANAGE.MONITOR",
            "ACT.PROCESS.BATCH",
        ]
        for concept in new_concepts:
            assert Vocabulary.validate_concept(concept) is True, f"{concept} should be valid"

    def test_validate_new_prop_concepts(self):
        """Test new PROP concepts from expansion."""
        new_concepts = [
            "PROP.STATE.RUNNING",
            "PROP.QUALITY.TRUSTED",
            "PROP.PERF.FAST",
            "PROP.CONFIDENCE.HIGH",
            "PROP.TYPE.ASYNC",
            "PROP.SCOPE.LOCAL",
        ]
        for concept in new_concepts:
            assert Vocabulary.validate_concept(concept) is True, f"{concept} should be valid"

    def test_validate_new_rel_concepts(self):
        """Test new REL concepts from expansion."""
        new_concepts = [
            "REL.PARENT.OF",
            "REL.DEPENDS.ON",
            "REL.TRIGGERS",
            "REL.OWNS",
            "REL.UPSTREAM.OF",
        ]
        for concept in new_concepts:
            assert Vocabulary.validate_concept(concept) is True, f"{concept} should be valid"

    def test_validate_new_data_concepts(self):
        """Test new DATA concepts from expansion."""
        new_concepts = [
            "DATA.QUEUE",
            "DATA.HEAP",
            "DATA.UUID",
            "DATA.TIMESTAMP",
            "DATA.BLOOM.FILTER",
        ]
        for concept in new_concepts:
            assert Vocabulary.validate_concept(concept) is True, f"{concept} should be valid"

    def test_validate_new_math_concepts(self):
        """Test new MATH concepts from expansion."""
        new_concepts = [
            "MATH.COSINE.SIMILARITY",
            "MATH.STDDEV",
            "MATH.SIGMOID",
            "MATH.FFT",
            "MATH.GRADIENT",
        ]
        for concept in new_concepts:
            assert Vocabulary.validate_concept(concept) is True, f"{concept} should be valid"

    def test_validate_new_meta_concepts(self):
        """Test new META concepts from expansion."""
        new_concepts = [
            "META.HEARTBEAT",
            "META.PROTOCOL.HTTP",
            "META.AUDIT.LOGIN",
            "META.CAP.ENCODE.JSON",
            "META.INFO.HEALTH",
        ]
        for concept in new_concepts:
            assert Vocabulary.validate_concept(concept) is True, f"{concept} should be valid"


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
        """Test getting all 10 categories."""
        categories = Vocabulary.get_all_categories()
        expected = {"ENT", "ACT", "PROP", "REL", "LOG", "MATH", "TIME", "SPACE", "DATA", "META"}
        assert categories == expected
        assert len(categories) == 10

    def test_list_by_category_act(self):
        """Test listing ACT concepts returns exactly 200."""
        actions = Vocabulary.list_by_category("ACT")
        assert len(actions) == 200
        assert all(concept.startswith("ACT.") for concept in actions)

    def test_list_by_category_ent(self):
        """Test listing ENT concepts returns exactly 100."""
        entities = Vocabulary.list_by_category("ENT")
        assert len(entities) == 100
        assert all(concept.startswith("ENT.") for concept in entities)

    def test_list_by_category_prop(self):
        """Test listing PROP concepts returns exactly 150."""
        props = Vocabulary.list_by_category("PROP")
        assert len(props) == 150
        assert all(concept.startswith("PROP.") for concept in props)

    def test_list_by_category_rel(self):
        """Test listing REL concepts returns exactly 100."""
        rels = Vocabulary.list_by_category("REL")
        assert len(rels) == 100
        assert all(concept.startswith("REL.") for concept in rels)

    def test_list_by_category_log(self):
        """Test listing LOG concepts returns exactly 50."""
        logs = Vocabulary.list_by_category("LOG")
        assert len(logs) == 50
        assert all(concept.startswith("LOG.") for concept in logs)

    def test_list_by_category_math(self):
        """Test listing MATH concepts returns exactly 100."""
        maths = Vocabulary.list_by_category("MATH")
        assert len(maths) == 100
        assert all(concept.startswith("MATH.") for concept in maths)

    def test_list_by_category_time(self):
        """Test listing TIME concepts returns exactly 50."""
        times = Vocabulary.list_by_category("TIME")
        assert len(times) == 50
        assert all(concept.startswith("TIME.") for concept in times)

    def test_list_by_category_space(self):
        """Test listing SPACE concepts returns exactly 50."""
        spaces = Vocabulary.list_by_category("SPACE")
        assert len(spaces) == 50
        assert all(concept.startswith("SPACE.") for concept in spaces)

    def test_list_by_category_data(self):
        """Test listing DATA concepts returns exactly 100."""
        data = Vocabulary.list_by_category("DATA")
        assert len(data) == 100
        assert all(concept.startswith("DATA.") for concept in data)

    def test_list_by_category_meta(self):
        """Test listing META concepts returns exactly 100."""
        meta = Vocabulary.list_by_category("META")
        assert len(meta) == 100
        assert all(concept.startswith("META.") for concept in meta)

    def test_count_by_category(self):
        """Test counting concepts by category matches expected."""
        counts = Vocabulary.count_by_category()
        expected = {
            "ENT": 100,
            "ACT": 200,
            "PROP": 150,
            "REL": 100,
            "LOG": 50,
            "MATH": 100,
            "TIME": 50,
            "SPACE": 50,
            "DATA": 100,
            "META": 100,
        }
        for cat, expected_count in expected.items():
            assert counts[cat] == expected_count, (
                f"{cat}: expected {expected_count}, got {counts[cat]}"
            )

    def test_list_by_nonexistent_category(self):
        """Test listing concepts for non-existent category returns empty."""
        result = Vocabulary.list_by_category("NONEXISTENT")
        assert result == []


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

    def test_new_concept_has_description(self):
        """Test new concepts have proper descriptions."""
        desc = Vocabulary.get_description("ACT.SECURITY.AUTHENTICATE")
        assert desc is not None
        assert "authenticat" in desc.lower() or "identity" in desc.lower()

    def test_new_concept_has_examples(self):
        """Test new concepts have examples."""
        examples = Vocabulary.get_examples("MATH.COSINE.SIMILARITY")
        assert isinstance(examples, list)
        assert len(examples) > 0


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

    def test_search_finds_new_concepts(self):
        """Test search finds concepts from vocabulary expansion."""
        results = Vocabulary.search("authenticate")
        assert any("SECURITY" in r for r in results)

    def test_search_security_concepts(self):
        """Test searching for security-related concepts."""
        results = Vocabulary.search("encrypt")
        assert len(results) > 0

    def test_search_topology_concepts(self):
        """Test searching for topology concepts."""
        results = Vocabulary.search("mesh")
        assert any("TOPO" in r for r in results)


class TestVocabularyCounts:
    """Test vocabulary counting functions."""

    def test_get_total_count_exactly_1000(self):
        """Test total concept count is exactly 1000."""
        assert Vocabulary.get_total_count() == 1000

    def test_total_matches_sum_of_categories(self):
        """Test total count matches sum of all categories."""
        total = Vocabulary.get_total_count()
        counts = Vocabulary.count_by_category()
        sum_of_categories = sum(counts.values())
        assert total == sum_of_categories

    def test_exactly_10_categories(self):
        """Test there are exactly 10 categories."""
        categories = Vocabulary.get_all_categories()
        assert len(categories) == 10


class TestVocabularyIntegrity:
    """Test vocabulary data integrity."""

    def test_all_concepts_have_category(self):
        """Test all 1000 concepts have a category field."""
        for concept, data in Vocabulary.CONCEPTS.items():
            assert "category" in data, f"{concept} missing category"
            assert isinstance(data["category"], str)
            assert len(data["category"]) > 0

    def test_all_concepts_have_subcategory(self):
        """Test all 1000 concepts have a subcategory field."""
        for concept, data in Vocabulary.CONCEPTS.items():
            assert "subcategory" in data, f"{concept} missing subcategory"
            assert isinstance(data["subcategory"], str)
            assert len(data["subcategory"]) > 0

    def test_all_concepts_have_description(self):
        """Test all 1000 concepts have a description."""
        for concept, data in Vocabulary.CONCEPTS.items():
            assert "description" in data, f"{concept} missing description"
            assert isinstance(data["description"], str)
            assert len(data["description"]) > 0

    def test_all_concepts_have_examples(self):
        """Test all 1000 concepts have examples."""
        for concept, data in Vocabulary.CONCEPTS.items():
            assert "examples" in data, f"{concept} missing examples"
            assert isinstance(data["examples"], list)
            assert len(data["examples"]) > 0, f"{concept} has empty examples"

    def test_concept_ids_match_category(self):
        """Test concept IDs start with their category."""
        for concept, data in Vocabulary.CONCEPTS.items():
            category = data["category"]
            assert concept.startswith(f"{category}."), (
                f"{concept} should start with {category}."
            )

    def test_no_duplicate_concepts(self):
        """Test no duplicate concept IDs exist."""
        concepts = list(Vocabulary.CONCEPTS.keys())
        assert len(concepts) == len(set(concepts)), "Duplicate concepts found"

    def test_all_categories_represented(self):
        """Test all 10 expected categories are present."""
        expected = {"ENT", "ACT", "PROP", "REL", "LOG", "MATH", "TIME", "SPACE", "DATA", "META"}
        found = {data["category"] for data in Vocabulary.CONCEPTS.values()}
        assert found == expected


class TestVocabularySubcategories:
    """Test subcategory organization."""

    def test_ent_has_subcategories(self):
        """Test ENT has multiple subcategories."""
        subcats = {
            data["subcategory"]
            for concept, data in Vocabulary.CONCEPTS.items()
            if data["category"] == "ENT"
        }
        assert "DATA" in subcats
        assert "AGENT" in subcats
        assert "RESOURCE" in subcats
        assert "OBJECT" in subcats
        assert len(subcats) >= 5

    def test_act_has_subcategories(self):
        """Test ACT has multiple subcategories."""
        subcats = {
            data["subcategory"]
            for concept, data in Vocabulary.CONCEPTS.items()
            if data["category"] == "ACT"
        }
        assert "QUERY" in subcats
        assert "CREATE" in subcats
        assert "TRANSFORM" in subcats
        assert "SECURITY" in subcats
        assert "COMMUNICATE" in subcats
        assert "CONTROL" in subcats
        assert len(subcats) >= 8

    def test_prop_has_subcategories(self):
        """Test PROP has multiple subcategories."""
        subcats = {
            data["subcategory"]
            for concept, data in Vocabulary.CONCEPTS.items()
            if data["category"] == "PROP"
        }
        assert "STATE" in subcats
        assert "QUALITY" in subcats
        assert "PRIORITY" in subcats
        assert "PERFORMANCE" in subcats
        assert len(subcats) >= 8

    def test_math_has_subcategories(self):
        """Test MATH has multiple subcategories."""
        subcats = {
            data["subcategory"]
            for concept, data in Vocabulary.CONCEPTS.items()
            if data["category"] == "MATH"
        }
        assert "ARITHMETIC" in subcats
        assert "AGGREGATE" in subcats
        assert "LINALG" in subcats
        assert "STATISTICS" in subcats
        assert len(subcats) >= 5
