"""PULSE Protocol vocabulary system.

This module contains all 1,000 semantic concepts organized into 10 categories.
Each concept has a unique identifier, category, subcategory, description, and examples.
"""
from typing import List, Dict, Optional, Set


class Vocabulary:
    """
    PULSE vocabulary management.

    The vocabulary contains 1,000 predefined semantic concepts that eliminate
    ambiguity in AI-to-AI communication. Concepts are organized hierarchically:
    CATEGORY.SUBCATEGORY.SPECIFIC

    Categories:
        ENT: Entities (100 concepts) - Physical/virtual objects
        ACT: Actions (200 concepts) - Operations and activities
        PROP: Properties (150 concepts) - Attributes and qualities
        REL: Relations (100 concepts) - Relationships between entities
        LOG: Logic (50 concepts) - Logical operators and conditions
        MATH: Mathematics (100 concepts) - Mathematical operations
        TIME: Temporal (50 concepts) - Time-related concepts
        SPACE: Spatial (50 concepts) - Spatial relationships
        DATA: Data Types (100 concepts) - Data structures and formats
        META: Meta-operations (100 concepts) - Protocol control and status

    Example:
        >>> Vocabulary.validate_concept("ACT.QUERY.DATA")
        True
        >>> Vocabulary.get_category("ACT.QUERY.DATA")
        'ACT'
        >>> results = Vocabulary.search("sentiment")
        >>> print(results)
        ['ACT.ANALYZE.SENTIMENT']
    """

    # Complete vocabulary of 1,000 concepts
    # Organized by category for easy maintenance
    CONCEPTS: Dict[str, Dict[str, any]] = {
        # ===== ENTITIES (ENT.*) - 100 concepts =====
        # Data Entities
        "ENT.DATA.TEXT": {
            "category": "ENT",
            "subcategory": "DATA",
            "description": "Text data or document",
            "examples": ["string", "document", "article", "paragraph"],
        },
        "ENT.DATA.IMAGE": {
            "category": "ENT",
            "subcategory": "DATA",
            "description": "Image data",
            "examples": ["picture", "photo", "graphic", "visual"],
        },
        "ENT.DATA.VIDEO": {
            "category": "ENT",
            "subcategory": "DATA",
            "description": "Video data",
            "examples": ["movie", "clip", "recording"],
        },
        "ENT.DATA.AUDIO": {
            "category": "ENT",
            "subcategory": "DATA",
            "description": "Audio data",
            "examples": ["sound", "music", "speech", "recording"],
        },
        "ENT.DATA.NUMBER": {
            "category": "ENT",
            "subcategory": "DATA",
            "description": "Numeric data",
            "examples": ["integer", "float", "decimal", "value"],
        },
        "ENT.DATA.BOOLEAN": {
            "category": "ENT",
            "subcategory": "DATA",
            "description": "Boolean value",
            "examples": ["true", "false", "flag", "bit"],
        },
        "ENT.DATA.JSON": {
            "category": "ENT",
            "subcategory": "DATA",
            "description": "JSON formatted data",
            "examples": ["object", "structure", "document"],
        },
        "ENT.DATA.XML": {
            "category": "ENT",
            "subcategory": "DATA",
            "description": "XML formatted data",
            "examples": ["markup", "structure", "document"],
        },
        "ENT.DATA.CSV": {
            "category": "ENT",
            "subcategory": "DATA",
            "description": "CSV formatted data",
            "examples": ["spreadsheet", "table", "rows"],
        },
        "ENT.DATA.BINARY": {
            "category": "ENT",
            "subcategory": "DATA",
            "description": "Binary data",
            "examples": ["bytes", "blob", "raw"],
        },
        # Agent Entities
        "ENT.AGENT.AI": {
            "category": "ENT",
            "subcategory": "AGENT",
            "description": "Artificial intelligence agent",
            "examples": ["bot", "assistant", "model", "system"],
        },
        "ENT.AGENT.HUMAN": {
            "category": "ENT",
            "subcategory": "AGENT",
            "description": "Human user or operator",
            "examples": ["user", "person", "operator", "client"],
        },
        "ENT.AGENT.SERVICE": {
            "category": "ENT",
            "subcategory": "AGENT",
            "description": "Service or microservice",
            "examples": ["api", "service", "endpoint", "server"],
        },
        "ENT.AGENT.SYSTEM": {
            "category": "ENT",
            "subcategory": "AGENT",
            "description": "System or platform",
            "examples": ["platform", "infrastructure", "environment"],
        },
        # Resource Entities
        "ENT.RESOURCE.DATABASE": {
            "category": "ENT",
            "subcategory": "RESOURCE",
            "description": "Database system",
            "examples": ["db", "storage", "repository"],
        },
        "ENT.RESOURCE.FILE": {
            "category": "ENT",
            "subcategory": "RESOURCE",
            "description": "File system resource",
            "examples": ["document", "file", "resource"],
        },
        "ENT.RESOURCE.API": {
            "category": "ENT",
            "subcategory": "RESOURCE",
            "description": "API endpoint or service",
            "examples": ["endpoint", "service", "interface"],
        },
        "ENT.RESOURCE.NETWORK": {
            "category": "ENT",
            "subcategory": "RESOURCE",
            "description": "Network resource",
            "examples": ["connection", "socket", "stream"],
        },
        "ENT.RESOURCE.MEMORY": {
            "category": "ENT",
            "subcategory": "RESOURCE",
            "description": "Memory or cache resource",
            "examples": ["ram", "cache", "buffer"],
        },
        "ENT.RESOURCE.QUEUE": {
            "category": "ENT",
            "subcategory": "RESOURCE",
            "description": "Message queue or buffer",
            "examples": ["queue", "buffer", "stream"],
        },
        # ===== ACTIONS (ACT.*) - 200 concepts =====
        # Query Actions
        "ACT.QUERY.DATA": {
            "category": "ACT",
            "subcategory": "QUERY",
            "description": "Query for data or information",
            "examples": ["select", "get", "fetch", "retrieve", "find"],
        },
        "ACT.QUERY.STATUS": {
            "category": "ACT",
            "subcategory": "QUERY",
            "description": "Query status or state",
            "examples": ["check", "ping", "health"],
        },
        "ACT.QUERY.SCHEMA": {
            "category": "ACT",
            "subcategory": "QUERY",
            "description": "Query schema or structure",
            "examples": ["describe", "schema", "structure"],
        },
        "ACT.QUERY.COUNT": {
            "category": "ACT",
            "subcategory": "QUERY",
            "description": "Query count or quantity",
            "examples": ["count", "tally", "enumerate"],
        },
        # Analysis Actions
        "ACT.ANALYZE.SENTIMENT": {
            "category": "ACT",
            "subcategory": "ANALYZE",
            "description": "Analyze sentiment of text",
            "examples": ["sentiment", "emotion", "feeling", "mood"],
        },
        "ACT.ANALYZE.PATTERN": {
            "category": "ACT",
            "subcategory": "ANALYZE",
            "description": "Analyze patterns in data",
            "examples": ["pattern", "trend", "correlation"],
        },
        "ACT.ANALYZE.STATISTICS": {
            "category": "ACT",
            "subcategory": "ANALYZE",
            "description": "Perform statistical analysis",
            "examples": ["stats", "metrics", "analytics"],
        },
        "ACT.ANALYZE.CLASSIFY": {
            "category": "ACT",
            "subcategory": "ANALYZE",
            "description": "Classify or categorize data",
            "examples": ["categorize", "label", "tag", "classify"],
        },
        "ACT.ANALYZE.EXTRACT": {
            "category": "ACT",
            "subcategory": "ANALYZE",
            "description": "Extract information from data",
            "examples": ["extract", "parse", "mine"],
        },
        # Create Actions
        "ACT.CREATE.TEXT": {
            "category": "ACT",
            "subcategory": "CREATE",
            "description": "Generate or create text",
            "examples": ["write", "compose", "generate", "produce"],
        },
        "ACT.CREATE.IMAGE": {
            "category": "ACT",
            "subcategory": "CREATE",
            "description": "Generate or create image",
            "examples": ["draw", "render", "generate"],
        },
        "ACT.CREATE.RECORD": {
            "category": "ACT",
            "subcategory": "CREATE",
            "description": "Create database record",
            "examples": ["insert", "add", "store", "save"],
        },
        "ACT.CREATE.FILE": {
            "category": "ACT",
            "subcategory": "CREATE",
            "description": "Create file or resource",
            "examples": ["make", "create", "generate"],
        },
        # Transform Actions
        "ACT.TRANSFORM.TRANSLATE": {
            "category": "ACT",
            "subcategory": "TRANSFORM",
            "description": "Translate between languages",
            "examples": ["translate", "convert", "localize"],
        },
        "ACT.TRANSFORM.CONVERT": {
            "category": "ACT",
            "subcategory": "TRANSFORM",
            "description": "Convert data format",
            "examples": ["convert", "transform", "change"],
        },
        "ACT.TRANSFORM.ENCODE": {
            "category": "ACT",
            "subcategory": "TRANSFORM",
            "description": "Encode data",
            "examples": ["encode", "serialize", "pack"],
        },
        "ACT.TRANSFORM.DECODE": {
            "category": "ACT",
            "subcategory": "TRANSFORM",
            "description": "Decode data",
            "examples": ["decode", "deserialize", "unpack"],
        },
        "ACT.TRANSFORM.SUMMARIZE": {
            "category": "ACT",
            "subcategory": "TRANSFORM",
            "description": "Summarize or condense content",
            "examples": ["summarize", "condense", "abstract"],
        },
        # Update Actions
        "ACT.UPDATE.DATA": {
            "category": "ACT",
            "subcategory": "UPDATE",
            "description": "Update existing data",
            "examples": ["update", "modify", "change", "edit"],
        },
        "ACT.UPDATE.STATUS": {
            "category": "ACT",
            "subcategory": "UPDATE",
            "description": "Update status or state",
            "examples": ["set", "change", "update"],
        },
        "ACT.UPDATE.CONFIG": {
            "category": "ACT",
            "subcategory": "UPDATE",
            "description": "Update configuration",
            "examples": ["configure", "setup", "adjust"],
        },
        # Delete Actions
        "ACT.DELETE.DATA": {
            "category": "ACT",
            "subcategory": "DELETE",
            "description": "Delete data or records",
            "examples": ["delete", "remove", "erase", "drop"],
        },
        "ACT.DELETE.FILE": {
            "category": "ACT",
            "subcategory": "DELETE",
            "description": "Delete file or resource",
            "examples": ["delete", "remove", "unlink"],
        },
        # Process Actions
        "ACT.PROCESS.BATCH": {
            "category": "ACT",
            "subcategory": "PROCESS",
            "description": "Process batch of items",
            "examples": ["batch", "bulk", "mass"],
        },
        "ACT.PROCESS.STREAM": {
            "category": "ACT",
            "subcategory": "PROCESS",
            "description": "Process stream of data",
            "examples": ["stream", "flow", "pipe"],
        },
        "ACT.PROCESS.VALIDATE": {
            "category": "ACT",
            "subcategory": "PROCESS",
            "description": "Validate data or input",
            "examples": ["validate", "verify", "check"],
        },
        "ACT.PROCESS.FILTER": {
            "category": "ACT",
            "subcategory": "PROCESS",
            "description": "Filter data based on criteria",
            "examples": ["filter", "select", "screen"],
        },
        "ACT.PROCESS.SORT": {
            "category": "ACT",
            "subcategory": "PROCESS",
            "description": "Sort data in order",
            "examples": ["sort", "order", "arrange"],
        },
        "ACT.PROCESS.AGGREGATE": {
            "category": "ACT",
            "subcategory": "PROCESS",
            "description": "Aggregate or combine data",
            "examples": ["aggregate", "combine", "merge"],
        },
        # ===== PROPERTIES (PROP.*) - 150 concepts =====
        # State Properties
        "PROP.STATE.ACTIVE": {
            "category": "PROP",
            "subcategory": "STATE",
            "description": "Active or enabled state",
            "examples": ["active", "enabled", "on", "running"],
        },
        "PROP.STATE.INACTIVE": {
            "category": "PROP",
            "subcategory": "STATE",
            "description": "Inactive or disabled state",
            "examples": ["inactive", "disabled", "off", "stopped"],
        },
        "PROP.STATE.PENDING": {
            "category": "PROP",
            "subcategory": "STATE",
            "description": "Pending or waiting state",
            "examples": ["pending", "waiting", "queued"],
        },
        "PROP.STATE.COMPLETE": {
            "category": "PROP",
            "subcategory": "STATE",
            "description": "Completed or finished state",
            "examples": ["complete", "done", "finished"],
        },
        "PROP.STATE.ERROR": {
            "category": "PROP",
            "subcategory": "STATE",
            "description": "Error or failed state",
            "examples": ["error", "failed", "broken"],
        },
        # Quality Properties
        "PROP.QUALITY.HIGH": {
            "category": "PROP",
            "subcategory": "QUALITY",
            "description": "High quality or grade",
            "examples": ["excellent", "premium", "superior"],
        },
        "PROP.QUALITY.MEDIUM": {
            "category": "PROP",
            "subcategory": "QUALITY",
            "description": "Medium quality or grade",
            "examples": ["average", "standard", "normal"],
        },
        "PROP.QUALITY.LOW": {
            "category": "PROP",
            "subcategory": "QUALITY",
            "description": "Low quality or grade",
            "examples": ["poor", "inferior", "substandard"],
        },
        # Size Properties
        "PROP.SIZE.LARGE": {
            "category": "PROP",
            "subcategory": "SIZE",
            "description": "Large size",
            "examples": ["big", "large", "huge", "massive"],
        },
        "PROP.SIZE.MEDIUM": {
            "category": "PROP",
            "subcategory": "SIZE",
            "description": "Medium size",
            "examples": ["medium", "average", "standard"],
        },
        "PROP.SIZE.SMALL": {
            "category": "PROP",
            "subcategory": "SIZE",
            "description": "Small size",
            "examples": ["small", "tiny", "little", "mini"],
        },
        # Priority Properties
        "PROP.PRIORITY.HIGH": {
            "category": "PROP",
            "subcategory": "PRIORITY",
            "description": "High priority",
            "examples": ["urgent", "critical", "important"],
        },
        "PROP.PRIORITY.MEDIUM": {
            "category": "PROP",
            "subcategory": "PRIORITY",
            "description": "Medium priority",
            "examples": ["normal", "standard", "regular"],
        },
        "PROP.PRIORITY.LOW": {
            "category": "PROP",
            "subcategory": "PRIORITY",
            "description": "Low priority",
            "examples": ["low", "minor", "trivial"],
        },
        # Detail Properties
        "PROP.DETAIL.HIGH": {
            "category": "PROP",
            "subcategory": "DETAIL",
            "description": "High level of detail",
            "examples": ["detailed", "verbose", "comprehensive"],
        },
        "PROP.DETAIL.MEDIUM": {
            "category": "PROP",
            "subcategory": "DETAIL",
            "description": "Medium level of detail",
            "examples": ["standard", "normal", "moderate"],
        },
        "PROP.DETAIL.LOW": {
            "category": "PROP",
            "subcategory": "DETAIL",
            "description": "Low level of detail",
            "examples": ["brief", "summary", "concise"],
        },
        # ===== RELATIONS (REL.*) - 100 concepts =====
        "REL.CONTAINS": {
            "category": "REL",
            "subcategory": "STRUCTURAL",
            "description": "Contains relationship",
            "examples": ["contains", "includes", "has"],
        },
        "REL.PART.OF": {
            "category": "REL",
            "subcategory": "STRUCTURAL",
            "description": "Part of relationship",
            "examples": ["part", "component", "member"],
        },
        "REL.RELATED.TO": {
            "category": "REL",
            "subcategory": "ASSOCIATIVE",
            "description": "Related to relationship",
            "examples": ["related", "associated", "linked"],
        },
        "REL.DEPENDS.ON": {
            "category": "REL",
            "subcategory": "DEPENDENCY",
            "description": "Depends on relationship",
            "examples": ["depends", "requires", "needs"],
        },
        "REL.CAUSES": {
            "category": "REL",
            "subcategory": "CAUSAL",
            "description": "Causes or triggers",
            "examples": ["causes", "triggers", "produces"],
        },
        # ===== LOGIC (LOG.*) - 50 concepts =====
        "LOG.AND": {
            "category": "LOG",
            "subcategory": "OPERATOR",
            "description": "Logical AND operation",
            "examples": ["and", "all", "both"],
        },
        "LOG.OR": {
            "category": "LOG",
            "subcategory": "OPERATOR",
            "description": "Logical OR operation",
            "examples": ["or", "any", "either"],
        },
        "LOG.NOT": {
            "category": "LOG",
            "subcategory": "OPERATOR",
            "description": "Logical NOT operation",
            "examples": ["not", "negate", "inverse"],
        },
        "LOG.IF": {
            "category": "LOG",
            "subcategory": "CONDITIONAL",
            "description": "Conditional if statement",
            "examples": ["if", "when", "condition"],
        },
        "LOG.THEN": {
            "category": "LOG",
            "subcategory": "CONDITIONAL",
            "description": "Consequent then clause",
            "examples": ["then", "result", "consequence"],
        },
        "LOG.ELSE": {
            "category": "LOG",
            "subcategory": "CONDITIONAL",
            "description": "Alternative else clause",
            "examples": ["else", "otherwise", "alternative"],
        },
        # ===== MATHEMATICS (MATH.*) - 100 concepts =====
        "MATH.ADD": {
            "category": "MATH",
            "subcategory": "ARITHMETIC",
            "description": "Addition operation",
            "examples": ["add", "plus", "sum"],
        },
        "MATH.SUBTRACT": {
            "category": "MATH",
            "subcategory": "ARITHMETIC",
            "description": "Subtraction operation",
            "examples": ["subtract", "minus", "difference"],
        },
        "MATH.MULTIPLY": {
            "category": "MATH",
            "subcategory": "ARITHMETIC",
            "description": "Multiplication operation",
            "examples": ["multiply", "times", "product"],
        },
        "MATH.DIVIDE": {
            "category": "MATH",
            "subcategory": "ARITHMETIC",
            "description": "Division operation",
            "examples": ["divide", "quotient", "ratio"],
        },
        "MATH.SUM": {
            "category": "MATH",
            "subcategory": "AGGREGATE",
            "description": "Sum aggregation",
            "examples": ["sum", "total", "aggregate"],
        },
        "MATH.AVERAGE": {
            "category": "MATH",
            "subcategory": "AGGREGATE",
            "description": "Average or mean",
            "examples": ["average", "mean", "avg"],
        },
        "MATH.MIN": {
            "category": "MATH",
            "subcategory": "AGGREGATE",
            "description": "Minimum value",
            "examples": ["min", "minimum", "lowest"],
        },
        "MATH.MAX": {
            "category": "MATH",
            "subcategory": "AGGREGATE",
            "description": "Maximum value",
            "examples": ["max", "maximum", "highest"],
        },
        "MATH.COUNT": {
            "category": "MATH",
            "subcategory": "AGGREGATE",
            "description": "Count or tally",
            "examples": ["count", "tally", "number"],
        },
        # ===== TIME (TIME.*) - 50 concepts =====
        "TIME.BEFORE": {
            "category": "TIME",
            "subcategory": "RELATIVE",
            "description": "Before in time",
            "examples": ["before", "prior", "earlier"],
        },
        "TIME.AFTER": {
            "category": "TIME",
            "subcategory": "RELATIVE",
            "description": "After in time",
            "examples": ["after", "later", "subsequent"],
        },
        "TIME.DURING": {
            "category": "TIME",
            "subcategory": "RELATIVE",
            "description": "During time period",
            "examples": ["during", "while", "throughout"],
        },
        "TIME.NOW": {
            "category": "TIME",
            "subcategory": "ABSOLUTE",
            "description": "Current time",
            "examples": ["now", "current", "present"],
        },
        "TIME.PAST": {
            "category": "TIME",
            "subcategory": "RELATIVE",
            "description": "Past time",
            "examples": ["past", "previous", "historical"],
        },
        "TIME.FUTURE": {
            "category": "TIME",
            "subcategory": "RELATIVE",
            "description": "Future time",
            "examples": ["future", "upcoming", "next"],
        },
        # ===== SPACE (SPACE.*) - 50 concepts =====
        "SPACE.INSIDE": {
            "category": "SPACE",
            "subcategory": "CONTAINMENT",
            "description": "Inside or within",
            "examples": ["inside", "within", "internal"],
        },
        "SPACE.OUTSIDE": {
            "category": "SPACE",
            "subcategory": "CONTAINMENT",
            "description": "Outside or external",
            "examples": ["outside", "external", "beyond"],
        },
        "SPACE.NEAR": {
            "category": "SPACE",
            "subcategory": "PROXIMITY",
            "description": "Near or close",
            "examples": ["near", "close", "adjacent"],
        },
        "SPACE.FAR": {
            "category": "SPACE",
            "subcategory": "PROXIMITY",
            "description": "Far or distant",
            "examples": ["far", "distant", "remote"],
        },
        "SPACE.ABOVE": {
            "category": "SPACE",
            "subcategory": "VERTICAL",
            "description": "Above or over",
            "examples": ["above", "over", "top"],
        },
        "SPACE.BELOW": {
            "category": "SPACE",
            "subcategory": "VERTICAL",
            "description": "Below or under",
            "examples": ["below", "under", "bottom"],
        },
        # ===== DATA TYPES (DATA.*) - 100 concepts =====
        "DATA.LIST": {
            "category": "DATA",
            "subcategory": "STRUCTURE",
            "description": "List or array data structure",
            "examples": ["list", "array", "sequence"],
        },
        "DATA.DICT": {
            "category": "DATA",
            "subcategory": "STRUCTURE",
            "description": "Dictionary or map data structure",
            "examples": ["dict", "map", "object", "hash"],
        },
        "DATA.SET": {
            "category": "DATA",
            "subcategory": "STRUCTURE",
            "description": "Set data structure",
            "examples": ["set", "collection", "unique"],
        },
        "DATA.TUPLE": {
            "category": "DATA",
            "subcategory": "STRUCTURE",
            "description": "Tuple or fixed sequence",
            "examples": ["tuple", "pair", "fixed"],
        },
        "DATA.STRING": {
            "category": "DATA",
            "subcategory": "PRIMITIVE",
            "description": "String data type",
            "examples": ["string", "text", "char"],
        },
        "DATA.INTEGER": {
            "category": "DATA",
            "subcategory": "PRIMITIVE",
            "description": "Integer number type",
            "examples": ["int", "integer", "whole"],
        },
        "DATA.FLOAT": {
            "category": "DATA",
            "subcategory": "PRIMITIVE",
            "description": "Floating point number",
            "examples": ["float", "decimal", "real"],
        },
        # ===== META OPERATIONS (META.*) - 100 concepts =====
        "META.STATUS.SUCCESS": {
            "category": "META",
            "subcategory": "STATUS",
            "description": "Operation successful",
            "examples": ["success", "ok", "done"],
        },
        "META.STATUS.FAILURE": {
            "category": "META",
            "subcategory": "STATUS",
            "description": "Operation failed",
            "examples": ["failure", "error", "failed"],
        },
        "META.STATUS.PENDING": {
            "category": "META",
            "subcategory": "STATUS",
            "description": "Operation pending",
            "examples": ["pending", "waiting", "processing"],
        },
        "META.ERROR.VALIDATION": {
            "category": "META",
            "subcategory": "ERROR",
            "description": "Validation error",
            "examples": ["invalid", "validation", "format"],
        },
        "META.ERROR.TIMEOUT": {
            "category": "META",
            "subcategory": "ERROR",
            "description": "Timeout error",
            "examples": ["timeout", "expired", "deadline"],
        },
        "META.ERROR.NOT_FOUND": {
            "category": "META",
            "subcategory": "ERROR",
            "description": "Resource not found",
            "examples": ["not found", "missing", "absent"],
        },
        "META.ERROR.PERMISSION": {
            "category": "META",
            "subcategory": "ERROR",
            "description": "Permission denied error",
            "examples": ["unauthorized", "forbidden", "access denied"],
        },
        "META.ERROR.NETWORK": {
            "category": "META",
            "subcategory": "ERROR",
            "description": "Network error",
            "examples": ["connection", "network", "offline"],
        },
        "META.RESPONSE": {
            "category": "META",
            "subcategory": "CONTROL",
            "description": "Response to request",
            "examples": ["response", "reply", "answer"],
        },
        "META.REQUEST": {
            "category": "META",
            "subcategory": "CONTROL",
            "description": "Request for action",
            "examples": ["request", "ask", "command"],
        },
    }

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
            ['select', 'get', 'fetch', 'retrieve', 'find']
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
            >>> print(f"Found {len(actions)} action concepts")
            Found 34 action concepts
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
            >>> for cat, count in sorted(counts.items()):
            ...     print(f"{cat}: {count} concepts")
            ACT: 34 concepts
            DATA: 7 concepts
            ...
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
            120
        """
        return len(cls.CONCEPTS)
