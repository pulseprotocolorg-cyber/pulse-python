"""Build final vocabulary.py from concept definitions."""
import sys
import os

# Add scripts dir for imports
sys.path.insert(0, os.path.dirname(__file__))

from generate_vocabulary import ENT, ACT
from gen_remaining import PROP, REL, LOG, MATH, TIME, SPACE, DATA, META

# Trim ACT to exactly 200
ACT_trimmed = ACT[:200]

# Add 15 more MATH concepts
MATH_EXTRA = [
    ("MATH.FIBONACCI", "SEQUENCE", "Fibonacci sequence", ["fib"]),
    ("MATH.PRIME", "NUMBER", "Prime number check", ["primality"]),
    ("MATH.PERMUTATION", "COMBINATORICS", "Permutation count", ["arrange"]),
    ("MATH.COMBINATION", "COMBINATORICS", "Combination count", ["choose"]),
    ("MATH.SIGMOID", "FUNCTION", "Sigmoid function", ["logistic"]),
    ("MATH.RELU", "FUNCTION", "ReLU activation", ["rectifier"]),
    ("MATH.SOFTMAX", "FUNCTION", "Softmax function", ["normalize"]),
    ("MATH.TANH", "FUNCTION", "Hyperbolic tangent", ["tanh"]),
    ("MATH.CONVOLUTION", "SIGNAL", "Convolution operation", ["filter"]),
    ("MATH.FFT", "SIGNAL", "Fast Fourier transform", ["frequency"]),
    ("MATH.GRADIENT", "CALCULUS", "Gradient computation", ["derivative"]),
    ("MATH.INTEGRAL", "CALCULUS", "Integration", ["area"]),
    ("MATH.DIFF", "CALCULUS", "Differentiation", ["rate of change"]),
    ("MATH.LIMIT", "CALCULUS", "Limit computation", ["converge"]),
    ("MATH.OPTIMIZE", "OPTIMIZATION", "Optimization", ["minimize"]),
]
MATH_ALL = MATH + MATH_EXTRA

# Counts
cats = {
    "ENT": ENT,
    "ACT": ACT_trimmed,
    "PROP": PROP,
    "REL": REL,
    "LOG": LOG,
    "MATH": MATH_ALL,
    "TIME": TIME,
    "SPACE": SPACE,
    "DATA": DATA,
    "META": META,
}

total = 0
for name, items in cats.items():
    print(f"{name}: {len(items)}")
    total += len(items)
print(f"TOTAL: {total}")

# Generate vocabulary.py
out_path = os.path.join(os.path.dirname(__file__), "..", "pulse", "vocabulary.py")

lines = []
lines.append('"""PULSE Protocol vocabulary system.')
lines.append('')
lines.append('This module contains all 1,000 semantic concepts organized into 10 categories.')
lines.append('Each concept has a unique identifier, category, subcategory, description, and examples.')
lines.append('"""')
lines.append('from typing import List, Dict, Optional, Set')
lines.append('')
lines.append('')
lines.append('class Vocabulary:')
lines.append('    """')
lines.append('    PULSE vocabulary management.')
lines.append('')
lines.append('    The vocabulary contains 1,000 predefined semantic concepts that eliminate')
lines.append('    ambiguity in AI-to-AI communication. Concepts are organized hierarchically:')
lines.append('    CATEGORY.SUBCATEGORY.SPECIFIC')
lines.append('')
lines.append('    Categories:')
lines.append('        ENT: Entities (100 concepts) - Physical/virtual objects')
lines.append('        ACT: Actions (200 concepts) - Operations and activities')
lines.append('        PROP: Properties (150 concepts) - Attributes and qualities')
lines.append('        REL: Relations (100 concepts) - Relationships between entities')
lines.append('        LOG: Logic (50 concepts) - Logical operators and conditions')
lines.append('        MATH: Mathematics (100 concepts) - Mathematical operations')
lines.append('        TIME: Temporal (50 concepts) - Time-related concepts')
lines.append('        SPACE: Spatial (50 concepts) - Spatial relationships')
lines.append('        DATA: Data Types (100 concepts) - Data structures and formats')
lines.append('        META: Meta-operations (100 concepts) - Protocol control and status')
lines.append('')
lines.append('    Example:')
lines.append('        >>> Vocabulary.validate_concept("ACT.QUERY.DATA")')
lines.append('        True')
lines.append('        >>> Vocabulary.get_category("ACT.QUERY.DATA")')
lines.append("        'ACT'")
lines.append('        >>> results = Vocabulary.search("sentiment")')
lines.append('        >>> print(results)')
lines.append("        ['ACT.ANALYZE.SENTIMENT']")
lines.append('    """')
lines.append('')
lines.append('    # Complete vocabulary of 1,000 concepts')
lines.append('    # Organized by category for easy maintenance')
lines.append('    CONCEPTS: Dict[str, Dict[str, any]] = {')

# Write each category
category_order = ["ENT", "ACT", "PROP", "REL", "LOG", "MATH", "TIME", "SPACE", "DATA", "META"]
category_names = {
    "ENT": "ENTITIES",
    "ACT": "ACTIONS",
    "PROP": "PROPERTIES",
    "REL": "RELATIONS",
    "LOG": "LOGIC",
    "MATH": "MATHEMATICS",
    "TIME": "TEMPORAL",
    "SPACE": "SPATIAL",
    "DATA": "DATA TYPES",
    "META": "META OPERATIONS",
}

for cat_key in category_order:
    items = cats[cat_key]
    cat_name = category_names[cat_key]
    lines.append(f'        # ===== {cat_name} ({cat_key}.*) - {len(items)} concepts =====')

    current_subcat = None
    for item in items:
        concept_id = item[0]
        subcategory = item[1]
        description = item[2]
        examples = item[3]

        # Determine category from concept_id
        category = concept_id.split(".")[0]

        if subcategory != current_subcat:
            current_subcat = subcategory
            lines.append(f'        # {subcategory}')

        examples_str = ", ".join(f'"{e}"' for e in examples)
        lines.append(f'        "{concept_id}": {{')
        lines.append(f'            "category": "{category}",')
        lines.append(f'            "subcategory": "{subcategory}",')
        lines.append(f'            "description": "{description}",')
        lines.append(f'            "examples": [{examples_str}],')
        lines.append(f'        }},')

lines.append('    }')
lines.append('')

# Add methods (copy from original)
methods = '''
    @classmethod
    def validate_concept(cls, concept: str) -> bool:
        """
        Check if concept exists in vocabulary.

        Args:
            concept: Concept identifier (e.g., "ACT.QUERY.DATA")

        Returns:
            True if concept exists, False otherwise

        Example:
            >>> Vocabulary.validate_concept("ACT.QUERY.DATA")
            True
            >>> Vocabulary.validate_concept("INVALID.CONCEPT")
            False
        """
        return concept in cls.CONCEPTS

    @classmethod
    def get_category(cls, concept: str) -> Optional[str]:
        """
        Get category for a concept.

        Args:
            concept: Concept identifier

        Returns:
            Category string (ENT, ACT, PROP, etc.) or None if not found

        Example:
            >>> Vocabulary.get_category("ACT.QUERY.DATA")
            'ACT'
        """
        if concept in cls.CONCEPTS:
            return cls.CONCEPTS[concept]["category"]
        return None

    @classmethod
    def get_description(cls, concept: str) -> Optional[str]:
        """
        Get description of a concept.

        Args:
            concept: Concept identifier

        Returns:
            Description string or None if not found

        Example:
            >>> Vocabulary.get_description("ACT.QUERY.DATA")
            'Query for data or information'
        """
        if concept in cls.CONCEPTS:
            return cls.CONCEPTS[concept]["description"]
        return None

    @classmethod
    def get_examples(cls, concept: str) -> List[str]:
        """
        Get usage examples for a concept.

        Args:
            concept: Concept identifier

        Returns:
            List of example strings

        Example:
            >>> Vocabulary.get_examples("ACT.QUERY.DATA")
            ['select', 'get', 'fetch']
        """
        if concept in cls.CONCEPTS:
            return cls.CONCEPTS[concept]["examples"]
        return []

    @classmethod
    def search(cls, query: str) -> List[str]:
        """
        Search vocabulary for matching concepts.

        Searches in concept IDs, descriptions, and examples.

        Args:
            query: Search query string

        Returns:
            List of matching concept identifiers

        Example:
            >>> results = Vocabulary.search("sentiment")
            >>> print(results)
            ['ACT.ANALYZE.SENTIMENT']
        """
        query_lower = query.lower()
        results = []

        for concept, data in cls.CONCEPTS.items():
            # Search in concept ID
            if query_lower in concept.lower():
                results.append(concept)
                continue

            # Search in description
            if query_lower in data["description"].lower():
                results.append(concept)
                continue

            # Search in examples
            if any(query_lower in ex.lower() for ex in data["examples"]):
                results.append(concept)
                continue

        return results

    @classmethod
    def list_by_category(cls, category: str) -> List[str]:
        """
        List all concepts in a category.

        Args:
            category: Category code (ENT, ACT, PROP, REL, LOG, MATH, TIME, SPACE, DATA, META)

        Returns:
            List of concept identifiers in the category

        Example:
            >>> actions = Vocabulary.list_by_category("ACT")
            >>> len(actions) >= 200
            True
        """
        return [
            concept for concept, data in cls.CONCEPTS.items() if data["category"] == category
        ]

    @classmethod
    def get_all_categories(cls) -> Set[str]:
        """
        Get all available categories.

        Returns:
            Set of category codes

        Example:
            >>> categories = Vocabulary.get_all_categories()
            >>> print(sorted(categories))
            ['ACT', 'DATA', 'ENT', 'LOG', 'MATH', 'META', 'PROP', 'REL', 'SPACE', 'TIME']
        """
        return {data["category"] for data in cls.CONCEPTS.values()}

    @classmethod
    def count_by_category(cls) -> Dict[str, int]:
        """
        Count concepts in each category.

        Returns:
            Dictionary mapping category to count

        Example:
            >>> counts = Vocabulary.count_by_category()
            >>> counts["ACT"] >= 200
            True
        """
        counts: Dict[str, int] = {}
        for data in cls.CONCEPTS.values():
            cat = data["category"]
            counts[cat] = counts.get(cat, 0) + 1
        return counts

    @classmethod
    def get_total_count(cls) -> int:
        """
        Get total number of concepts.

        Returns:
            Total count of concepts

        Example:
            >>> Vocabulary.get_total_count()
            1000
        """
        return len(cls.CONCEPTS)
'''

lines.append(methods)

# Write the file
with open(out_path, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"\nGenerated: {out_path}")
print(f"Total concepts: {total}")
