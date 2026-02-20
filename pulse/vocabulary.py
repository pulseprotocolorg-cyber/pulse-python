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
        # DATA
        "ENT.DATA.TEXT": {
            "category": "ENT",
            "subcategory": "DATA",
            "description": "Text data or document",
            "examples": ["string", "document", "article"],
        },
        "ENT.DATA.IMAGE": {
            "category": "ENT",
            "subcategory": "DATA",
            "description": "Image data",
            "examples": ["picture", "photo", "graphic"],
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
            "examples": ["sound", "music", "speech"],
        },
        "ENT.DATA.NUMBER": {
            "category": "ENT",
            "subcategory": "DATA",
            "description": "Numeric data",
            "examples": ["integer", "float", "decimal"],
        },
        "ENT.DATA.BOOLEAN": {
            "category": "ENT",
            "subcategory": "DATA",
            "description": "Boolean value",
            "examples": ["true", "false", "flag"],
        },
        "ENT.DATA.JSON": {
            "category": "ENT",
            "subcategory": "DATA",
            "description": "JSON formatted data",
            "examples": ["object", "structure"],
        },
        "ENT.DATA.XML": {
            "category": "ENT",
            "subcategory": "DATA",
            "description": "XML formatted data",
            "examples": ["markup", "structure"],
        },
        "ENT.DATA.CSV": {
            "category": "ENT",
            "subcategory": "DATA",
            "description": "CSV formatted data",
            "examples": ["spreadsheet", "table"],
        },
        "ENT.DATA.BINARY": {
            "category": "ENT",
            "subcategory": "DATA",
            "description": "Binary data",
            "examples": ["bytes", "blob", "raw"],
        },
        "ENT.DATA.HTML": {
            "category": "ENT",
            "subcategory": "DATA",
            "description": "HTML content",
            "examples": ["webpage", "markup"],
        },
        "ENT.DATA.MARKDOWN": {
            "category": "ENT",
            "subcategory": "DATA",
            "description": "Markdown text",
            "examples": ["formatted", "rich text"],
        },
        "ENT.DATA.YAML": {
            "category": "ENT",
            "subcategory": "DATA",
            "description": "YAML configuration",
            "examples": ["config", "settings"],
        },
        "ENT.DATA.PROTOBUF": {
            "category": "ENT",
            "subcategory": "DATA",
            "description": "Protocol buffer data",
            "examples": ["proto", "serialized"],
        },
        "ENT.DATA.GRAPH": {
            "category": "ENT",
            "subcategory": "DATA",
            "description": "Graph or network data",
            "examples": ["nodes", "edges"],
        },
        "ENT.DATA.TABLE": {
            "category": "ENT",
            "subcategory": "DATA",
            "description": "Tabular data",
            "examples": ["rows", "columns", "grid"],
        },
        "ENT.DATA.VECTOR": {
            "category": "ENT",
            "subcategory": "DATA",
            "description": "Vector embedding data",
            "examples": ["embedding", "feature"],
        },
        "ENT.DATA.MATRIX": {
            "category": "ENT",
            "subcategory": "DATA",
            "description": "Matrix data",
            "examples": ["2d array", "grid"],
        },
        "ENT.DATA.TENSOR": {
            "category": "ENT",
            "subcategory": "DATA",
            "description": "Tensor data",
            "examples": ["multidimensional", "nd-array"],
        },
        "ENT.DATA.LOG": {
            "category": "ENT",
            "subcategory": "DATA",
            "description": "Log data",
            "examples": ["entries", "records", "trace"],
        },
        # AGENT
        "ENT.AGENT.AI": {
            "category": "ENT",
            "subcategory": "AGENT",
            "description": "Artificial intelligence agent",
            "examples": ["bot", "assistant", "model"],
        },
        "ENT.AGENT.HUMAN": {
            "category": "ENT",
            "subcategory": "AGENT",
            "description": "Human user or operator",
            "examples": ["user", "person", "operator"],
        },
        "ENT.AGENT.SERVICE": {
            "category": "ENT",
            "subcategory": "AGENT",
            "description": "Service or microservice",
            "examples": ["api", "endpoint"],
        },
        "ENT.AGENT.SYSTEM": {
            "category": "ENT",
            "subcategory": "AGENT",
            "description": "System or platform",
            "examples": ["platform", "infrastructure"],
        },
        "ENT.AGENT.BOT": {
            "category": "ENT",
            "subcategory": "AGENT",
            "description": "Automated bot agent",
            "examples": ["robot", "crawler", "scraper"],
        },
        "ENT.AGENT.ORCHESTRATOR": {
            "category": "ENT",
            "subcategory": "AGENT",
            "description": "Orchestration agent",
            "examples": ["coordinator", "conductor"],
        },
        "ENT.AGENT.MONITOR": {
            "category": "ENT",
            "subcategory": "AGENT",
            "description": "Monitoring agent",
            "examples": ["watcher", "observer"],
        },
        "ENT.AGENT.PROXY": {
            "category": "ENT",
            "subcategory": "AGENT",
            "description": "Proxy or intermediary",
            "examples": ["middleware", "relay"],
        },
        "ENT.AGENT.GATEWAY": {
            "category": "ENT",
            "subcategory": "AGENT",
            "description": "Gateway or entry point",
            "examples": ["ingress", "entry"],
        },
        "ENT.AGENT.SCHEDULER": {
            "category": "ENT",
            "subcategory": "AGENT",
            "description": "Scheduling agent",
            "examples": ["cron", "timer"],
        },
        "ENT.AGENT.WORKER": {
            "category": "ENT",
            "subcategory": "AGENT",
            "description": "Worker process agent",
            "examples": ["executor", "runner"],
        },
        "ENT.AGENT.PIPELINE": {
            "category": "ENT",
            "subcategory": "AGENT",
            "description": "Pipeline processor",
            "examples": ["chain", "workflow"],
        },
        "ENT.AGENT.ROUTER": {
            "category": "ENT",
            "subcategory": "AGENT",
            "description": "Message router",
            "examples": ["dispatcher", "switch"],
        },
        "ENT.AGENT.VALIDATOR": {
            "category": "ENT",
            "subcategory": "AGENT",
            "description": "Validation agent",
            "examples": ["checker", "verifier"],
        },
        "ENT.AGENT.TRANSFORMER": {
            "category": "ENT",
            "subcategory": "AGENT",
            "description": "Data transformation agent",
            "examples": ["converter", "mapper"],
        },
        # RESOURCE
        "ENT.RESOURCE.DATABASE": {
            "category": "ENT",
            "subcategory": "RESOURCE",
            "description": "Database system",
            "examples": ["db", "storage"],
        },
        "ENT.RESOURCE.FILE": {
            "category": "ENT",
            "subcategory": "RESOURCE",
            "description": "File system resource",
            "examples": ["document", "file"],
        },
        "ENT.RESOURCE.API": {
            "category": "ENT",
            "subcategory": "RESOURCE",
            "description": "API endpoint",
            "examples": ["endpoint", "interface"],
        },
        "ENT.RESOURCE.NETWORK": {
            "category": "ENT",
            "subcategory": "RESOURCE",
            "description": "Network resource",
            "examples": ["connection", "socket"],
        },
        "ENT.RESOURCE.MEMORY": {
            "category": "ENT",
            "subcategory": "RESOURCE",
            "description": "Memory or cache",
            "examples": ["ram", "cache", "buffer"],
        },
        "ENT.RESOURCE.QUEUE": {
            "category": "ENT",
            "subcategory": "RESOURCE",
            "description": "Message queue",
            "examples": ["queue", "buffer"],
        },
        "ENT.RESOURCE.STORAGE": {
            "category": "ENT",
            "subcategory": "RESOURCE",
            "description": "Storage system",
            "examples": ["disk", "volume"],
        },
        "ENT.RESOURCE.COMPUTE": {
            "category": "ENT",
            "subcategory": "RESOURCE",
            "description": "Compute resource",
            "examples": ["cpu", "processing"],
        },
        "ENT.RESOURCE.GPU": {
            "category": "ENT",
            "subcategory": "RESOURCE",
            "description": "GPU resource",
            "examples": ["graphics", "cuda"],
        },
        "ENT.RESOURCE.CONTAINER": {
            "category": "ENT",
            "subcategory": "RESOURCE",
            "description": "Container or sandbox",
            "examples": ["docker", "pod"],
        },
        "ENT.RESOURCE.CLUSTER": {
            "category": "ENT",
            "subcategory": "RESOURCE",
            "description": "Compute cluster",
            "examples": ["swarm", "fleet"],
        },
        "ENT.RESOURCE.REGISTRY": {
            "category": "ENT",
            "subcategory": "RESOURCE",
            "description": "Service registry",
            "examples": ["catalog", "directory"],
        },
        "ENT.RESOURCE.BROKER": {
            "category": "ENT",
            "subcategory": "RESOURCE",
            "description": "Message broker",
            "examples": ["kafka", "rabbitmq"],
        },
        "ENT.RESOURCE.CACHE": {
            "category": "ENT",
            "subcategory": "RESOURCE",
            "description": "Cache system",
            "examples": ["redis", "memcached"],
        },
        "ENT.RESOURCE.CDN": {
            "category": "ENT",
            "subcategory": "RESOURCE",
            "description": "Content delivery network",
            "examples": ["edge", "distribution"],
        },
        "ENT.RESOURCE.DNS": {
            "category": "ENT",
            "subcategory": "RESOURCE",
            "description": "Domain name service",
            "examples": ["resolver", "nameserver"],
        },
        "ENT.RESOURCE.LOADBALANCER": {
            "category": "ENT",
            "subcategory": "RESOURCE",
            "description": "Load balancer",
            "examples": ["lb", "distributor"],
        },
        "ENT.RESOURCE.FIREWALL": {
            "category": "ENT",
            "subcategory": "RESOURCE",
            "description": "Firewall or WAF",
            "examples": ["filter", "shield"],
        },
        "ENT.RESOURCE.VAULT": {
            "category": "ENT",
            "subcategory": "RESOURCE",
            "description": "Secret vault",
            "examples": ["secrets", "keystore"],
        },
        "ENT.RESOURCE.LOGGER": {
            "category": "ENT",
            "subcategory": "RESOURCE",
            "description": "Logging service",
            "examples": ["log collector", "sink"],
        },
        # OBJECT
        "ENT.OBJECT.MODEL": {
            "category": "ENT",
            "subcategory": "OBJECT",
            "description": "ML model or data model",
            "examples": ["neural net", "schema"],
        },
        "ENT.OBJECT.SCHEMA": {
            "category": "ENT",
            "subcategory": "OBJECT",
            "description": "Data schema definition",
            "examples": ["structure", "blueprint"],
        },
        "ENT.OBJECT.CONFIG": {
            "category": "ENT",
            "subcategory": "OBJECT",
            "description": "Configuration object",
            "examples": ["settings", "preferences"],
        },
        "ENT.OBJECT.TOKEN": {
            "category": "ENT",
            "subcategory": "OBJECT",
            "description": "Authentication token",
            "examples": ["jwt", "session token"],
        },
        "ENT.OBJECT.SESSION": {
            "category": "ENT",
            "subcategory": "OBJECT",
            "description": "User or agent session",
            "examples": ["context", "connection"],
        },
        "ENT.OBJECT.CREDENTIAL": {
            "category": "ENT",
            "subcategory": "OBJECT",
            "description": "Authentication credential",
            "examples": ["login", "password"],
        },
        "ENT.OBJECT.CERTIFICATE": {
            "category": "ENT",
            "subcategory": "OBJECT",
            "description": "Security certificate",
            "examples": ["ssl", "x509"],
        },
        "ENT.OBJECT.KEY": {
            "category": "ENT",
            "subcategory": "OBJECT",
            "description": "Cryptographic key",
            "examples": ["secret", "public key"],
        },
        "ENT.OBJECT.EVENT": {
            "category": "ENT",
            "subcategory": "OBJECT",
            "description": "System event",
            "examples": ["notification", "signal"],
        },
        "ENT.OBJECT.TASK": {
            "category": "ENT",
            "subcategory": "OBJECT",
            "description": "Task or work item",
            "examples": ["job", "unit of work"],
        },
        "ENT.OBJECT.WORKFLOW": {
            "category": "ENT",
            "subcategory": "OBJECT",
            "description": "Workflow definition",
            "examples": ["process", "pipeline"],
        },
        "ENT.OBJECT.RULE": {
            "category": "ENT",
            "subcategory": "OBJECT",
            "description": "Business rule",
            "examples": ["policy", "constraint"],
        },
        "ENT.OBJECT.POLICY": {
            "category": "ENT",
            "subcategory": "OBJECT",
            "description": "Security or access policy",
            "examples": ["acl", "permission"],
        },
        "ENT.OBJECT.TEMPLATE": {
            "category": "ENT",
            "subcategory": "OBJECT",
            "description": "Template or pattern",
            "examples": ["blueprint", "boilerplate"],
        },
        "ENT.OBJECT.METRIC": {
            "category": "ENT",
            "subcategory": "OBJECT",
            "description": "Performance metric",
            "examples": ["measurement", "kpi"],
        },
        "ENT.OBJECT.ALERT": {
            "category": "ENT",
            "subcategory": "OBJECT",
            "description": "Alert or alarm",
            "examples": ["warning", "notification"],
        },
        "ENT.OBJECT.REPORT": {
            "category": "ENT",
            "subcategory": "OBJECT",
            "description": "Report or summary",
            "examples": ["analysis", "document"],
        },
        "ENT.OBJECT.MESSAGE": {
            "category": "ENT",
            "subcategory": "OBJECT",
            "description": "Message or communication",
            "examples": ["packet", "payload"],
        },
        "ENT.OBJECT.TRANSACTION": {
            "category": "ENT",
            "subcategory": "OBJECT",
            "description": "Transaction unit",
            "examples": ["operation", "atomic"],
        },
        "ENT.OBJECT.SNAPSHOT": {
            "category": "ENT",
            "subcategory": "OBJECT",
            "description": "State snapshot",
            "examples": ["checkpoint", "backup"],
        },
        # DOMAIN
        "ENT.DOMAIN.WEB": {
            "category": "ENT",
            "subcategory": "DOMAIN",
            "description": "Web domain",
            "examples": ["http", "website"],
        },
        "ENT.DOMAIN.MOBILE": {
            "category": "ENT",
            "subcategory": "DOMAIN",
            "description": "Mobile platform",
            "examples": ["ios", "android"],
        },
        "ENT.DOMAIN.CLOUD": {
            "category": "ENT",
            "subcategory": "DOMAIN",
            "description": "Cloud platform",
            "examples": ["aws", "azure", "gcp"],
        },
        "ENT.DOMAIN.IOT": {
            "category": "ENT",
            "subcategory": "DOMAIN",
            "description": "Internet of Things",
            "examples": ["sensor", "device"],
        },
        "ENT.DOMAIN.EDGE": {
            "category": "ENT",
            "subcategory": "DOMAIN",
            "description": "Edge computing",
            "examples": ["local", "proximity"],
        },
        "ENT.DOMAIN.BLOCKCHAIN": {
            "category": "ENT",
            "subcategory": "DOMAIN",
            "description": "Blockchain network",
            "examples": ["distributed ledger"],
        },
        "ENT.DOMAIN.ML": {
            "category": "ENT",
            "subcategory": "DOMAIN",
            "description": "Machine learning",
            "examples": ["ai", "deep learning"],
        },
        "ENT.DOMAIN.NLP": {
            "category": "ENT",
            "subcategory": "DOMAIN",
            "description": "Natural language processing",
            "examples": ["text analysis"],
        },
        "ENT.DOMAIN.CV": {
            "category": "ENT",
            "subcategory": "DOMAIN",
            "description": "Computer vision",
            "examples": ["image recognition"],
        },
        "ENT.DOMAIN.SECURITY": {
            "category": "ENT",
            "subcategory": "DOMAIN",
            "description": "Security domain",
            "examples": ["cybersecurity"],
        },
        "ENT.DOMAIN.DEVOPS": {
            "category": "ENT",
            "subcategory": "DOMAIN",
            "description": "DevOps domain",
            "examples": ["cicd", "deployment"],
        },
        "ENT.DOMAIN.DATABASE": {
            "category": "ENT",
            "subcategory": "DOMAIN",
            "description": "Database domain",
            "examples": ["sql", "nosql"],
        },
        "ENT.DOMAIN.MESSAGING": {
            "category": "ENT",
            "subcategory": "DOMAIN",
            "description": "Messaging domain",
            "examples": ["chat", "email"],
        },
        "ENT.DOMAIN.ANALYTICS": {
            "category": "ENT",
            "subcategory": "DOMAIN",
            "description": "Analytics domain",
            "examples": ["bi", "reporting"],
        },
        "ENT.DOMAIN.AUTOMATION": {
            "category": "ENT",
            "subcategory": "DOMAIN",
            "description": "Automation domain",
            "examples": ["rpa", "scripting"],
        },
        # COMPONENT
        "ENT.COMPONENT.MODULE": {
            "category": "ENT",
            "subcategory": "COMPONENT",
            "description": "Software module",
            "examples": ["package", "library"],
        },
        "ENT.COMPONENT.PLUGIN": {
            "category": "ENT",
            "subcategory": "COMPONENT",
            "description": "Plugin or extension",
            "examples": ["addon", "widget"],
        },
        "ENT.COMPONENT.SDK": {
            "category": "ENT",
            "subcategory": "COMPONENT",
            "description": "Software development kit",
            "examples": ["toolkit", "library"],
        },
        "ENT.COMPONENT.CLI": {
            "category": "ENT",
            "subcategory": "COMPONENT",
            "description": "Command line interface",
            "examples": ["terminal", "console"],
        },
        "ENT.COMPONENT.GUI": {
            "category": "ENT",
            "subcategory": "COMPONENT",
            "description": "Graphical interface",
            "examples": ["ui", "frontend"],
        },
        "ENT.COMPONENT.DRIVER": {
            "category": "ENT",
            "subcategory": "COMPONENT",
            "description": "Hardware or software driver",
            "examples": ["adapter"],
        },
        "ENT.COMPONENT.MIDDLEWARE": {
            "category": "ENT",
            "subcategory": "COMPONENT",
            "description": "Middleware layer",
            "examples": ["interceptor"],
        },
        "ENT.COMPONENT.RUNTIME": {
            "category": "ENT",
            "subcategory": "COMPONENT",
            "description": "Runtime environment",
            "examples": ["vm", "interpreter"],
        },
        "ENT.COMPONENT.COMPILER": {
            "category": "ENT",
            "subcategory": "COMPONENT",
            "description": "Compiler or transpiler",
            "examples": ["builder"],
        },
        "ENT.COMPONENT.DEBUGGER": {
            "category": "ENT",
            "subcategory": "COMPONENT",
            "description": "Debugging tool",
            "examples": ["inspector", "profiler"],
        },
        # ===== ACTIONS (ACT.*) - 200 concepts =====
        # QUERY
        "ACT.QUERY.DATA": {
            "category": "ACT",
            "subcategory": "QUERY",
            "description": "Query for data or information",
            "examples": ["select", "get", "fetch"],
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
            "examples": ["describe", "schema"],
        },
        "ACT.QUERY.COUNT": {
            "category": "ACT",
            "subcategory": "QUERY",
            "description": "Query count or quantity",
            "examples": ["count", "tally"],
        },
        "ACT.QUERY.EXISTS": {
            "category": "ACT",
            "subcategory": "QUERY",
            "description": "Check if resource exists",
            "examples": ["exists", "has"],
        },
        "ACT.QUERY.LIST": {
            "category": "ACT",
            "subcategory": "QUERY",
            "description": "List available items",
            "examples": ["enumerate", "browse"],
        },
        "ACT.QUERY.SEARCH": {
            "category": "ACT",
            "subcategory": "QUERY",
            "description": "Search for matching items",
            "examples": ["find", "lookup"],
        },
        "ACT.QUERY.FILTER": {
            "category": "ACT",
            "subcategory": "QUERY",
            "description": "Query with filters",
            "examples": ["where", "criteria"],
        },
        "ACT.QUERY.METADATA": {
            "category": "ACT",
            "subcategory": "QUERY",
            "description": "Query metadata",
            "examples": ["info", "properties"],
        },
        "ACT.QUERY.HISTORY": {
            "category": "ACT",
            "subcategory": "QUERY",
            "description": "Query historical data",
            "examples": ["log", "audit trail"],
        },
        "ACT.QUERY.CAPABILITY": {
            "category": "ACT",
            "subcategory": "QUERY",
            "description": "Query agent capabilities",
            "examples": ["features", "support"],
        },
        "ACT.QUERY.PERMISSION": {
            "category": "ACT",
            "subcategory": "QUERY",
            "description": "Query access permissions",
            "examples": ["rights", "roles"],
        },
        "ACT.QUERY.VERSION": {
            "category": "ACT",
            "subcategory": "QUERY",
            "description": "Query version info",
            "examples": ["release", "build"],
        },
        "ACT.QUERY.CONFIG": {
            "category": "ACT",
            "subcategory": "QUERY",
            "description": "Query configuration",
            "examples": ["settings", "preferences"],
        },
        "ACT.QUERY.HEALTH": {
            "category": "ACT",
            "subcategory": "QUERY",
            "description": "Health check query",
            "examples": ["heartbeat", "alive"],
        },
        "ACT.QUERY.STATS": {
            "category": "ACT",
            "subcategory": "QUERY",
            "description": "Query statistics",
            "examples": ["metrics", "counters"],
        },
        "ACT.QUERY.DEPENDENCIES": {
            "category": "ACT",
            "subcategory": "QUERY",
            "description": "Query dependencies",
            "examples": ["requires", "needs"],
        },
        "ACT.QUERY.RELATED": {
            "category": "ACT",
            "subcategory": "QUERY",
            "description": "Query related items",
            "examples": ["linked", "associated"],
        },
        "ACT.QUERY.DIFF": {
            "category": "ACT",
            "subcategory": "QUERY",
            "description": "Query differences",
            "examples": ["compare", "delta"],
        },
        "ACT.QUERY.PREVIEW": {
            "category": "ACT",
            "subcategory": "QUERY",
            "description": "Preview or dry-run query",
            "examples": ["simulate", "test"],
        },
        # ANALYZE
        "ACT.ANALYZE.SENTIMENT": {
            "category": "ACT",
            "subcategory": "ANALYZE",
            "description": "Analyze sentiment",
            "examples": ["emotion", "mood"],
        },
        "ACT.ANALYZE.PATTERN": {
            "category": "ACT",
            "subcategory": "ANALYZE",
            "description": "Analyze patterns",
            "examples": ["trend", "correlation"],
        },
        "ACT.ANALYZE.STATISTICS": {
            "category": "ACT",
            "subcategory": "ANALYZE",
            "description": "Statistical analysis",
            "examples": ["stats", "metrics"],
        },
        "ACT.ANALYZE.CLASSIFY": {
            "category": "ACT",
            "subcategory": "ANALYZE",
            "description": "Classify or categorize",
            "examples": ["categorize", "label"],
        },
        "ACT.ANALYZE.EXTRACT": {
            "category": "ACT",
            "subcategory": "ANALYZE",
            "description": "Extract information",
            "examples": ["parse", "mine"],
        },
        "ACT.ANALYZE.CLUSTER": {
            "category": "ACT",
            "subcategory": "ANALYZE",
            "description": "Cluster data points",
            "examples": ["group", "segment"],
        },
        "ACT.ANALYZE.PREDICT": {
            "category": "ACT",
            "subcategory": "ANALYZE",
            "description": "Predict outcomes",
            "examples": ["forecast", "project"],
        },
        "ACT.ANALYZE.DETECT": {
            "category": "ACT",
            "subcategory": "ANALYZE",
            "description": "Detect anomalies",
            "examples": ["identify", "spot"],
        },
        "ACT.ANALYZE.COMPARE": {
            "category": "ACT",
            "subcategory": "ANALYZE",
            "description": "Compare items",
            "examples": ["diff", "contrast"],
        },
        "ACT.ANALYZE.RANK": {
            "category": "ACT",
            "subcategory": "ANALYZE",
            "description": "Rank or score items",
            "examples": ["rate", "prioritize"],
        },
        "ACT.ANALYZE.PROFILE": {
            "category": "ACT",
            "subcategory": "ANALYZE",
            "description": "Profile performance",
            "examples": ["benchmark", "measure"],
        },
        "ACT.ANALYZE.AUDIT": {
            "category": "ACT",
            "subcategory": "ANALYZE",
            "description": "Audit for compliance",
            "examples": ["review", "inspect"],
        },
        "ACT.ANALYZE.DIAGNOSE": {
            "category": "ACT",
            "subcategory": "ANALYZE",
            "description": "Diagnose issues",
            "examples": ["troubleshoot", "debug"],
        },
        "ACT.ANALYZE.EVALUATE": {
            "category": "ACT",
            "subcategory": "ANALYZE",
            "description": "Evaluate quality",
            "examples": ["assess", "grade"],
        },
        "ACT.ANALYZE.CORRELATE": {
            "category": "ACT",
            "subcategory": "ANALYZE",
            "description": "Find correlations",
            "examples": ["relate", "link"],
        },
        "ACT.ANALYZE.TOKENIZE": {
            "category": "ACT",
            "subcategory": "ANALYZE",
            "description": "Tokenize text",
            "examples": ["split", "segment"],
        },
        "ACT.ANALYZE.EMBED": {
            "category": "ACT",
            "subcategory": "ANALYZE",
            "description": "Create embeddings",
            "examples": ["vectorize", "encode"],
        },
        "ACT.ANALYZE.PARSE": {
            "category": "ACT",
            "subcategory": "ANALYZE",
            "description": "Parse structured data",
            "examples": ["interpret", "read"],
        },
        "ACT.ANALYZE.VALIDATE": {
            "category": "ACT",
            "subcategory": "ANALYZE",
            "description": "Validate data quality",
            "examples": ["verify", "check"],
        },
        "ACT.ANALYZE.SUMMARIZE": {
            "category": "ACT",
            "subcategory": "ANALYZE",
            "description": "Summarize analysis results",
            "examples": ["digest", "recap"],
        },
        # CREATE
        "ACT.CREATE.TEXT": {
            "category": "ACT",
            "subcategory": "CREATE",
            "description": "Generate text",
            "examples": ["write", "compose"],
        },
        "ACT.CREATE.IMAGE": {
            "category": "ACT",
            "subcategory": "CREATE",
            "description": "Generate image",
            "examples": ["draw", "render"],
        },
        "ACT.CREATE.RECORD": {
            "category": "ACT",
            "subcategory": "CREATE",
            "description": "Create database record",
            "examples": ["insert", "add"],
        },
        "ACT.CREATE.FILE": {
            "category": "ACT",
            "subcategory": "CREATE",
            "description": "Create file",
            "examples": ["make", "generate"],
        },
        "ACT.CREATE.SESSION": {
            "category": "ACT",
            "subcategory": "CREATE",
            "description": "Create session",
            "examples": ["open", "establish"],
        },
        "ACT.CREATE.TOKEN": {
            "category": "ACT",
            "subcategory": "CREATE",
            "description": "Create auth token",
            "examples": ["issue", "generate"],
        },
        "ACT.CREATE.USER": {
            "category": "ACT",
            "subcategory": "CREATE",
            "description": "Create user account",
            "examples": ["register", "signup"],
        },
        "ACT.CREATE.CHANNEL": {
            "category": "ACT",
            "subcategory": "CREATE",
            "description": "Create comm channel",
            "examples": ["open", "establish"],
        },
        "ACT.CREATE.TASK": {
            "category": "ACT",
            "subcategory": "CREATE",
            "description": "Create task or job",
            "examples": ["schedule", "queue"],
        },
        "ACT.CREATE.EVENT": {
            "category": "ACT",
            "subcategory": "CREATE",
            "description": "Create event",
            "examples": ["emit", "trigger"],
        },
        "ACT.CREATE.SNAPSHOT": {
            "category": "ACT",
            "subcategory": "CREATE",
            "description": "Create snapshot",
            "examples": ["checkpoint", "backup"],
        },
        "ACT.CREATE.INDEX": {
            "category": "ACT",
            "subcategory": "CREATE",
            "description": "Create search index",
            "examples": ["build", "catalog"],
        },
        "ACT.CREATE.REPORT": {
            "category": "ACT",
            "subcategory": "CREATE",
            "description": "Generate report",
            "examples": ["compile", "produce"],
        },
        "ACT.CREATE.WORKFLOW": {
            "category": "ACT",
            "subcategory": "CREATE",
            "description": "Create workflow",
            "examples": ["define", "design"],
        },
        "ACT.CREATE.RULE": {
            "category": "ACT",
            "subcategory": "CREATE",
            "description": "Create rule or policy",
            "examples": ["define", "set"],
        },
        "ACT.CREATE.ALERT": {
            "category": "ACT",
            "subcategory": "CREATE",
            "description": "Create alert",
            "examples": ["set", "configure"],
        },
        "ACT.CREATE.TEMPLATE": {
            "category": "ACT",
            "subcategory": "CREATE",
            "description": "Create template",
            "examples": ["design", "define"],
        },
        "ACT.CREATE.COPY": {
            "category": "ACT",
            "subcategory": "CREATE",
            "description": "Create copy or clone",
            "examples": ["duplicate", "replicate"],
        },
        "ACT.CREATE.LINK": {
            "category": "ACT",
            "subcategory": "CREATE",
            "description": "Create link or reference",
            "examples": ["connect", "associate"],
        },
        "ACT.CREATE.BATCH": {
            "category": "ACT",
            "subcategory": "CREATE",
            "description": "Create batch of items",
            "examples": ["bulk create", "mass insert"],
        },
        # TRANSFORM
        "ACT.TRANSFORM.TRANSLATE": {
            "category": "ACT",
            "subcategory": "TRANSFORM",
            "description": "Translate languages",
            "examples": ["localize", "i18n"],
        },
        "ACT.TRANSFORM.CONVERT": {
            "category": "ACT",
            "subcategory": "TRANSFORM",
            "description": "Convert format",
            "examples": ["change", "reformat"],
        },
        "ACT.TRANSFORM.ENCODE": {
            "category": "ACT",
            "subcategory": "TRANSFORM",
            "description": "Encode data",
            "examples": ["serialize", "pack"],
        },
        "ACT.TRANSFORM.DECODE": {
            "category": "ACT",
            "subcategory": "TRANSFORM",
            "description": "Decode data",
            "examples": ["deserialize", "unpack"],
        },
        "ACT.TRANSFORM.SUMMARIZE": {
            "category": "ACT",
            "subcategory": "TRANSFORM",
            "description": "Summarize content",
            "examples": ["condense", "abstract"],
        },
        "ACT.TRANSFORM.COMPRESS": {
            "category": "ACT",
            "subcategory": "TRANSFORM",
            "description": "Compress data",
            "examples": ["zip", "deflate"],
        },
        "ACT.TRANSFORM.DECOMPRESS": {
            "category": "ACT",
            "subcategory": "TRANSFORM",
            "description": "Decompress data",
            "examples": ["unzip", "inflate"],
        },
        "ACT.TRANSFORM.ENCRYPT": {
            "category": "ACT",
            "subcategory": "TRANSFORM",
            "description": "Encrypt data",
            "examples": ["cipher", "protect"],
        },
        "ACT.TRANSFORM.DECRYPT": {
            "category": "ACT",
            "subcategory": "TRANSFORM",
            "description": "Decrypt data",
            "examples": ["decipher", "unlock"],
        },
        "ACT.TRANSFORM.HASH": {
            "category": "ACT",
            "subcategory": "TRANSFORM",
            "description": "Hash data",
            "examples": ["digest", "checksum"],
        },
        "ACT.TRANSFORM.NORMALIZE": {
            "category": "ACT",
            "subcategory": "TRANSFORM",
            "description": "Normalize data",
            "examples": ["standardize", "clean"],
        },
        "ACT.TRANSFORM.DENORMALIZE": {
            "category": "ACT",
            "subcategory": "TRANSFORM",
            "description": "Denormalize data",
            "examples": ["flatten", "expand"],
        },
        "ACT.TRANSFORM.MAP": {
            "category": "ACT",
            "subcategory": "TRANSFORM",
            "description": "Map data fields",
            "examples": ["project", "reshape"],
        },
        "ACT.TRANSFORM.REDUCE": {
            "category": "ACT",
            "subcategory": "TRANSFORM",
            "description": "Reduce data set",
            "examples": ["aggregate", "fold"],
        },
        "ACT.TRANSFORM.MERGE": {
            "category": "ACT",
            "subcategory": "TRANSFORM",
            "description": "Merge data sources",
            "examples": ["combine", "join"],
        },
        "ACT.TRANSFORM.SPLIT": {
            "category": "ACT",
            "subcategory": "TRANSFORM",
            "description": "Split data",
            "examples": ["partition", "chunk"],
        },
        "ACT.TRANSFORM.RESIZE": {
            "category": "ACT",
            "subcategory": "TRANSFORM",
            "description": "Resize content",
            "examples": ["scale", "crop"],
        },
        "ACT.TRANSFORM.FORMAT": {
            "category": "ACT",
            "subcategory": "TRANSFORM",
            "description": "Format output",
            "examples": ["prettify", "render"],
        },
        "ACT.TRANSFORM.ENRICH": {
            "category": "ACT",
            "subcategory": "TRANSFORM",
            "description": "Enrich with metadata",
            "examples": ["augment", "annotate"],
        },
        "ACT.TRANSFORM.REDACT": {
            "category": "ACT",
            "subcategory": "TRANSFORM",
            "description": "Redact sensitive data",
            "examples": ["mask", "anonymize"],
        },
        # UPDATE
        "ACT.UPDATE.DATA": {
            "category": "ACT",
            "subcategory": "UPDATE",
            "description": "Update existing data",
            "examples": ["modify", "change"],
        },
        "ACT.UPDATE.STATUS": {
            "category": "ACT",
            "subcategory": "UPDATE",
            "description": "Update status",
            "examples": ["set", "change"],
        },
        "ACT.UPDATE.CONFIG": {
            "category": "ACT",
            "subcategory": "UPDATE",
            "description": "Update configuration",
            "examples": ["configure", "adjust"],
        },
        "ACT.UPDATE.SCHEMA": {
            "category": "ACT",
            "subcategory": "UPDATE",
            "description": "Update schema",
            "examples": ["migrate", "alter"],
        },
        "ACT.UPDATE.PERMISSION": {
            "category": "ACT",
            "subcategory": "UPDATE",
            "description": "Update permissions",
            "examples": ["grant", "revoke"],
        },
        "ACT.UPDATE.METADATA": {
            "category": "ACT",
            "subcategory": "UPDATE",
            "description": "Update metadata",
            "examples": ["tag", "annotate"],
        },
        "ACT.UPDATE.PRIORITY": {
            "category": "ACT",
            "subcategory": "UPDATE",
            "description": "Update priority",
            "examples": ["reprioritize", "escalate"],
        },
        "ACT.UPDATE.STATE": {
            "category": "ACT",
            "subcategory": "UPDATE",
            "description": "Update state machine",
            "examples": ["transition", "advance"],
        },
        "ACT.UPDATE.VERSION": {
            "category": "ACT",
            "subcategory": "UPDATE",
            "description": "Update version",
            "examples": ["upgrade", "bump"],
        },
        "ACT.UPDATE.REPLACE": {
            "category": "ACT",
            "subcategory": "UPDATE",
            "description": "Replace entirely",
            "examples": ["swap", "substitute"],
        },
        "ACT.UPDATE.PATCH": {
            "category": "ACT",
            "subcategory": "UPDATE",
            "description": "Partial update",
            "examples": ["patch", "amend"],
        },
        "ACT.UPDATE.RENAME": {
            "category": "ACT",
            "subcategory": "UPDATE",
            "description": "Rename resource",
            "examples": ["alias", "relabel"],
        },
        "ACT.UPDATE.MOVE": {
            "category": "ACT",
            "subcategory": "UPDATE",
            "description": "Move resource",
            "examples": ["relocate", "transfer"],
        },
        "ACT.UPDATE.REORDER": {
            "category": "ACT",
            "subcategory": "UPDATE",
            "description": "Reorder items",
            "examples": ["rearrange", "sort"],
        },
        "ACT.UPDATE.REFRESH": {
            "category": "ACT",
            "subcategory": "UPDATE",
            "description": "Refresh or reload",
            "examples": ["reload", "sync"],
        },
        # DELETE
        "ACT.DELETE.DATA": {
            "category": "ACT",
            "subcategory": "DELETE",
            "description": "Delete data or records",
            "examples": ["remove", "erase"],
        },
        "ACT.DELETE.FILE": {
            "category": "ACT",
            "subcategory": "DELETE",
            "description": "Delete file",
            "examples": ["unlink", "destroy"],
        },
        "ACT.DELETE.SESSION": {
            "category": "ACT",
            "subcategory": "DELETE",
            "description": "End session",
            "examples": ["close", "terminate"],
        },
        "ACT.DELETE.TOKEN": {
            "category": "ACT",
            "subcategory": "DELETE",
            "description": "Revoke token",
            "examples": ["invalidate", "expire"],
        },
        "ACT.DELETE.USER": {
            "category": "ACT",
            "subcategory": "DELETE",
            "description": "Delete user account",
            "examples": ["deactivate", "purge"],
        },
        "ACT.DELETE.CACHE": {
            "category": "ACT",
            "subcategory": "DELETE",
            "description": "Clear cache",
            "examples": ["flush", "invalidate"],
        },
        "ACT.DELETE.INDEX": {
            "category": "ACT",
            "subcategory": "DELETE",
            "description": "Drop index",
            "examples": ["remove", "destroy"],
        },
        "ACT.DELETE.RULE": {
            "category": "ACT",
            "subcategory": "DELETE",
            "description": "Delete rule",
            "examples": ["remove", "disable"],
        },
        "ACT.DELETE.LINK": {
            "category": "ACT",
            "subcategory": "DELETE",
            "description": "Remove link",
            "examples": ["unlink", "detach"],
        },
        "ACT.DELETE.BATCH": {
            "category": "ACT",
            "subcategory": "DELETE",
            "description": "Batch delete",
            "examples": ["bulk remove", "purge"],
        },
        # PROCESS
        "ACT.PROCESS.BATCH": {
            "category": "ACT",
            "subcategory": "PROCESS",
            "description": "Process batch",
            "examples": ["bulk", "mass"],
        },
        "ACT.PROCESS.STREAM": {
            "category": "ACT",
            "subcategory": "PROCESS",
            "description": "Process stream",
            "examples": ["flow", "pipe"],
        },
        "ACT.PROCESS.VALIDATE": {
            "category": "ACT",
            "subcategory": "PROCESS",
            "description": "Validate data",
            "examples": ["verify", "check"],
        },
        "ACT.PROCESS.FILTER": {
            "category": "ACT",
            "subcategory": "PROCESS",
            "description": "Filter data",
            "examples": ["select", "screen"],
        },
        "ACT.PROCESS.SORT": {
            "category": "ACT",
            "subcategory": "PROCESS",
            "description": "Sort data",
            "examples": ["order", "arrange"],
        },
        "ACT.PROCESS.AGGREGATE": {
            "category": "ACT",
            "subcategory": "PROCESS",
            "description": "Aggregate data",
            "examples": ["combine", "merge"],
        },
        "ACT.PROCESS.DEDUPLICATE": {
            "category": "ACT",
            "subcategory": "PROCESS",
            "description": "Remove duplicates",
            "examples": ["distinct", "unique"],
        },
        "ACT.PROCESS.ENQUEUE": {
            "category": "ACT",
            "subcategory": "PROCESS",
            "description": "Add to queue",
            "examples": ["push", "submit"],
        },
        "ACT.PROCESS.DEQUEUE": {
            "category": "ACT",
            "subcategory": "PROCESS",
            "description": "Remove from queue",
            "examples": ["pop", "consume"],
        },
        "ACT.PROCESS.PIPELINE": {
            "category": "ACT",
            "subcategory": "PROCESS",
            "description": "Execute pipeline",
            "examples": ["chain", "sequence"],
        },
        "ACT.PROCESS.SCHEDULE": {
            "category": "ACT",
            "subcategory": "PROCESS",
            "description": "Schedule for later",
            "examples": ["defer", "delay"],
        },
        "ACT.PROCESS.RETRY": {
            "category": "ACT",
            "subcategory": "PROCESS",
            "description": "Retry operation",
            "examples": ["reattempt", "repeat"],
        },
        "ACT.PROCESS.ROLLBACK": {
            "category": "ACT",
            "subcategory": "PROCESS",
            "description": "Rollback operation",
            "examples": ["undo", "revert"],
        },
        "ACT.PROCESS.COMMIT": {
            "category": "ACT",
            "subcategory": "PROCESS",
            "description": "Commit transaction",
            "examples": ["finalize", "confirm"],
        },
        "ACT.PROCESS.CHECKPOINT": {
            "category": "ACT",
            "subcategory": "PROCESS",
            "description": "Save checkpoint",
            "examples": ["snapshot", "mark"],
        },
        "ACT.PROCESS.RESUME": {
            "category": "ACT",
            "subcategory": "PROCESS",
            "description": "Resume processing",
            "examples": ["continue", "restart"],
        },
        "ACT.PROCESS.PAUSE": {
            "category": "ACT",
            "subcategory": "PROCESS",
            "description": "Pause processing",
            "examples": ["suspend", "hold"],
        },
        "ACT.PROCESS.CANCEL": {
            "category": "ACT",
            "subcategory": "PROCESS",
            "description": "Cancel operation",
            "examples": ["abort", "stop"],
        },
        "ACT.PROCESS.EXECUTE": {
            "category": "ACT",
            "subcategory": "PROCESS",
            "description": "Execute command",
            "examples": ["run", "invoke"],
        },
        "ACT.PROCESS.DISPATCH": {
            "category": "ACT",
            "subcategory": "PROCESS",
            "description": "Dispatch to handler",
            "examples": ["route", "forward"],
        },
        # COMMUNICATE
        "ACT.COMMUNICATE.SEND": {
            "category": "ACT",
            "subcategory": "COMMUNICATE",
            "description": "Send message",
            "examples": ["transmit", "deliver"],
        },
        "ACT.COMMUNICATE.RECEIVE": {
            "category": "ACT",
            "subcategory": "COMMUNICATE",
            "description": "Receive message",
            "examples": ["accept", "get"],
        },
        "ACT.COMMUNICATE.BROADCAST": {
            "category": "ACT",
            "subcategory": "COMMUNICATE",
            "description": "Broadcast to all",
            "examples": ["multicast", "publish"],
        },
        "ACT.COMMUNICATE.SUBSCRIBE": {
            "category": "ACT",
            "subcategory": "COMMUNICATE",
            "description": "Subscribe to topic",
            "examples": ["listen", "follow"],
        },
        "ACT.COMMUNICATE.UNSUBSCRIBE": {
            "category": "ACT",
            "subcategory": "COMMUNICATE",
            "description": "Unsubscribe from topic",
            "examples": ["unlisten", "unfollow"],
        },
        "ACT.COMMUNICATE.PUBLISH": {
            "category": "ACT",
            "subcategory": "COMMUNICATE",
            "description": "Publish message",
            "examples": ["emit", "announce"],
        },
        "ACT.COMMUNICATE.REQUEST": {
            "category": "ACT",
            "subcategory": "COMMUNICATE",
            "description": "Send request",
            "examples": ["ask", "invoke"],
        },
        "ACT.COMMUNICATE.RESPOND": {
            "category": "ACT",
            "subcategory": "COMMUNICATE",
            "description": "Send response",
            "examples": ["reply", "answer"],
        },
        "ACT.COMMUNICATE.ACKNOWLEDGE": {
            "category": "ACT",
            "subcategory": "COMMUNICATE",
            "description": "Acknowledge receipt",
            "examples": ["ack", "confirm"],
        },
        "ACT.COMMUNICATE.NOTIFY": {
            "category": "ACT",
            "subcategory": "COMMUNICATE",
            "description": "Send notification",
            "examples": ["alert", "inform"],
        },
        "ACT.COMMUNICATE.PING": {
            "category": "ACT",
            "subcategory": "COMMUNICATE",
            "description": "Ping for liveness",
            "examples": ["heartbeat", "check"],
        },
        "ACT.COMMUNICATE.PONG": {
            "category": "ACT",
            "subcategory": "COMMUNICATE",
            "description": "Respond to ping",
            "examples": ["alive", "ok"],
        },
        "ACT.COMMUNICATE.HANDSHAKE": {
            "category": "ACT",
            "subcategory": "COMMUNICATE",
            "description": "Protocol handshake",
            "examples": ["negotiate", "init"],
        },
        "ACT.COMMUNICATE.SYNC": {
            "category": "ACT",
            "subcategory": "COMMUNICATE",
            "description": "Synchronize state",
            "examples": ["reconcile", "align"],
        },
        "ACT.COMMUNICATE.STREAM": {
            "category": "ACT",
            "subcategory": "COMMUNICATE",
            "description": "Stream data",
            "examples": ["flow", "push"],
        },
        "ACT.COMMUNICATE.NEGOTIATE": {
            "category": "ACT",
            "subcategory": "COMMUNICATE",
            "description": "Negotiate terms",
            "examples": ["agree", "settle"],
        },
        "ACT.COMMUNICATE.REGISTER": {
            "category": "ACT",
            "subcategory": "COMMUNICATE",
            "description": "Register with service",
            "examples": ["enroll", "join"],
        },
        "ACT.COMMUNICATE.DEREGISTER": {
            "category": "ACT",
            "subcategory": "COMMUNICATE",
            "description": "Deregister from service",
            "examples": ["leave", "quit"],
        },
        "ACT.COMMUNICATE.FORWARD": {
            "category": "ACT",
            "subcategory": "COMMUNICATE",
            "description": "Forward message",
            "examples": ["relay", "proxy"],
        },
        "ACT.COMMUNICATE.CALLBACK": {
            "category": "ACT",
            "subcategory": "COMMUNICATE",
            "description": "Callback notification",
            "examples": ["webhook", "hook"],
        },
        # CONTROL
        "ACT.CONTROL.START": {
            "category": "ACT",
            "subcategory": "CONTROL",
            "description": "Start process",
            "examples": ["begin", "launch"],
        },
        "ACT.CONTROL.STOP": {
            "category": "ACT",
            "subcategory": "CONTROL",
            "description": "Stop process",
            "examples": ["halt", "terminate"],
        },
        "ACT.CONTROL.RESTART": {
            "category": "ACT",
            "subcategory": "CONTROL",
            "description": "Restart process",
            "examples": ["reboot", "cycle"],
        },
        "ACT.CONTROL.ENABLE": {
            "category": "ACT",
            "subcategory": "CONTROL",
            "description": "Enable feature",
            "examples": ["activate", "turn on"],
        },
        "ACT.CONTROL.DISABLE": {
            "category": "ACT",
            "subcategory": "CONTROL",
            "description": "Disable feature",
            "examples": ["deactivate", "turn off"],
        },
        "ACT.CONTROL.SCALE": {
            "category": "ACT",
            "subcategory": "CONTROL",
            "description": "Scale resources",
            "examples": ["resize", "adjust"],
        },
        "ACT.CONTROL.DEPLOY": {
            "category": "ACT",
            "subcategory": "CONTROL",
            "description": "Deploy application",
            "examples": ["release", "ship"],
        },
        "ACT.CONTROL.UNDEPLOY": {
            "category": "ACT",
            "subcategory": "CONTROL",
            "description": "Undeploy application",
            "examples": ["remove", "teardown"],
        },
        "ACT.CONTROL.CONFIGURE": {
            "category": "ACT",
            "subcategory": "CONTROL",
            "description": "Configure system",
            "examples": ["setup", "tune"],
        },
        "ACT.CONTROL.LOCK": {
            "category": "ACT",
            "subcategory": "CONTROL",
            "description": "Lock resource",
            "examples": ["acquire", "hold"],
        },
        "ACT.CONTROL.UNLOCK": {
            "category": "ACT",
            "subcategory": "CONTROL",
            "description": "Unlock resource",
            "examples": ["release", "free"],
        },
        "ACT.CONTROL.THROTTLE": {
            "category": "ACT",
            "subcategory": "CONTROL",
            "description": "Throttle rate",
            "examples": ["limit", "slow"],
        },
        "ACT.CONTROL.MIGRATE": {
            "category": "ACT",
            "subcategory": "CONTROL",
            "description": "Migrate system",
            "examples": ["move", "transfer"],
        },
        "ACT.CONTROL.BACKUP": {
            "category": "ACT",
            "subcategory": "CONTROL",
            "description": "Backup data",
            "examples": ["archive", "save"],
        },
        "ACT.CONTROL.RESTORE": {
            "category": "ACT",
            "subcategory": "CONTROL",
            "description": "Restore from backup",
            "examples": ["recover", "unarchive"],
        },
        "ACT.CONTROL.FAILOVER": {
            "category": "ACT",
            "subcategory": "CONTROL",
            "description": "Trigger failover",
            "examples": ["switchover", "fallback"],
        },
        "ACT.CONTROL.PROMOTE": {
            "category": "ACT",
            "subcategory": "CONTROL",
            "description": "Promote replica",
            "examples": ["elevate", "upgrade"],
        },
        "ACT.CONTROL.DEMOTE": {
            "category": "ACT",
            "subcategory": "CONTROL",
            "description": "Demote replica",
            "examples": ["downgrade", "relegate"],
        },
        "ACT.CONTROL.DRAIN": {
            "category": "ACT",
            "subcategory": "CONTROL",
            "description": "Drain connections",
            "examples": ["evacuate", "empty"],
        },
        "ACT.CONTROL.INITIALIZE": {
            "category": "ACT",
            "subcategory": "CONTROL",
            "description": "Initialize system",
            "examples": ["bootstrap", "setup"],
        },
        # SECURITY
        "ACT.SECURITY.AUTHENTICATE": {
            "category": "ACT",
            "subcategory": "SECURITY",
            "description": "Authenticate identity",
            "examples": ["login", "verify"],
        },
        "ACT.SECURITY.AUTHORIZE": {
            "category": "ACT",
            "subcategory": "SECURITY",
            "description": "Authorize access",
            "examples": ["permit", "allow"],
        },
        "ACT.SECURITY.SIGN": {
            "category": "ACT",
            "subcategory": "SECURITY",
            "description": "Sign data",
            "examples": ["seal", "stamp"],
        },
        "ACT.SECURITY.VERIFY": {
            "category": "ACT",
            "subcategory": "SECURITY",
            "description": "Verify signature",
            "examples": ["validate", "check"],
        },
        "ACT.SECURITY.ENCRYPT": {
            "category": "ACT",
            "subcategory": "SECURITY",
            "description": "Encrypt payload",
            "examples": ["protect", "cipher"],
        },
        "ACT.SECURITY.DECRYPT": {
            "category": "ACT",
            "subcategory": "SECURITY",
            "description": "Decrypt payload",
            "examples": ["unlock", "decipher"],
        },
        "ACT.SECURITY.REVOKE": {
            "category": "ACT",
            "subcategory": "SECURITY",
            "description": "Revoke access",
            "examples": ["deny", "block"],
        },
        "ACT.SECURITY.ROTATE": {
            "category": "ACT",
            "subcategory": "SECURITY",
            "description": "Rotate credentials",
            "examples": ["renew", "refresh"],
        },
        "ACT.SECURITY.AUDIT": {
            "category": "ACT",
            "subcategory": "SECURITY",
            "description": "Security audit",
            "examples": ["review", "inspect"],
        },
        "ACT.SECURITY.SCAN": {
            "category": "ACT",
            "subcategory": "SECURITY",
            "description": "Security scan",
            "examples": ["check", "probe"],
        },
        "ACT.SECURITY.BLOCK": {
            "category": "ACT",
            "subcategory": "SECURITY",
            "description": "Block access",
            "examples": ["deny", "reject"],
        },
        "ACT.SECURITY.ALLOW": {
            "category": "ACT",
            "subcategory": "SECURITY",
            "description": "Allow access",
            "examples": ["permit", "whitelist"],
        },
        "ACT.SECURITY.QUARANTINE": {
            "category": "ACT",
            "subcategory": "SECURITY",
            "description": "Quarantine threat",
            "examples": ["isolate", "sandbox"],
        },
        "ACT.SECURITY.ESCALATE": {
            "category": "ACT",
            "subcategory": "SECURITY",
            "description": "Escalate privilege",
            "examples": ["elevate", "promote"],
        },
        "ACT.SECURITY.DEESCALATE": {
            "category": "ACT",
            "subcategory": "SECURITY",
            "description": "Reduce privilege",
            "examples": ["demote", "restrict"],
        },
        "ACT.SECURITY.LOG": {
            "category": "ACT",
            "subcategory": "SECURITY",
            "description": "Log security event",
            "examples": ["record", "trace"],
        },
        "ACT.SECURITY.CHALLENGE": {
            "category": "ACT",
            "subcategory": "SECURITY",
            "description": "Issue challenge",
            "examples": ["test", "probe"],
        },
        "ACT.SECURITY.TOKEN.REFRESH": {
            "category": "ACT",
            "subcategory": "SECURITY",
            "description": "Refresh auth token",
            "examples": ["renew", "extend"],
        },
        "ACT.SECURITY.MFA": {
            "category": "ACT",
            "subcategory": "SECURITY",
            "description": "Multi-factor auth",
            "examples": ["2fa", "otp"],
        },
        "ACT.SECURITY.LOGOUT": {
            "category": "ACT",
            "subcategory": "SECURITY",
            "description": "Terminate session",
            "examples": ["signout", "disconnect"],
        },
        # MANAGE
        "ACT.MANAGE.ASSIGN": {
            "category": "ACT",
            "subcategory": "MANAGE",
            "description": "Assign resource",
            "examples": ["allocate", "delegate"],
        },
        "ACT.MANAGE.RELEASE": {
            "category": "ACT",
            "subcategory": "MANAGE",
            "description": "Release resource",
            "examples": ["free", "deallocate"],
        },
        "ACT.MANAGE.MONITOR": {
            "category": "ACT",
            "subcategory": "MANAGE",
            "description": "Monitor resource",
            "examples": ["watch", "observe"],
        },
        "ACT.MANAGE.ALERT": {
            "category": "ACT",
            "subcategory": "MANAGE",
            "description": "Raise alert",
            "examples": ["warn", "notify"],
        },
        "ACT.MANAGE.HEAL": {
            "category": "ACT",
            "subcategory": "MANAGE",
            "description": "Self-heal system",
            "examples": ["repair", "fix"],
        },
        "ACT.MANAGE.BALANCE": {
            "category": "ACT",
            "subcategory": "MANAGE",
            "description": "Balance load",
            "examples": ["distribute", "spread"],
        },
        "ACT.MANAGE.OPTIMIZE": {
            "category": "ACT",
            "subcategory": "MANAGE",
            "description": "Optimize performance",
            "examples": ["tune", "improve"],
        },
        "ACT.MANAGE.PROVISION": {
            "category": "ACT",
            "subcategory": "MANAGE",
            "description": "Provision resource",
            "examples": ["create", "setup"],
        },
        "ACT.MANAGE.DEPROVISION": {
            "category": "ACT",
            "subcategory": "MANAGE",
            "description": "Remove resource",
            "examples": ["teardown", "destroy"],
        },
        "ACT.MANAGE.REGISTER": {
            "category": "ACT",
            "subcategory": "MANAGE",
            "description": "Register service",
            "examples": ["enroll", "catalog"],
        },
        "ACT.MANAGE.DISCOVER": {
            "category": "ACT",
            "subcategory": "MANAGE",
            "description": "Discover services",
            "examples": ["find", "locate"],
        },
        "ACT.MANAGE.ORCHESTRATE": {
            "category": "ACT",
            "subcategory": "MANAGE",
            "description": "Orchestrate workflow",
            "examples": ["coordinate", "conduct"],
        },
        "ACT.MANAGE.SCHEDULE": {
            "category": "ACT",
            "subcategory": "MANAGE",
            "description": "Schedule operation",
            "examples": ["plan", "queue"],
        },
        "ACT.MANAGE.INVENTORY": {
            "category": "ACT",
            "subcategory": "MANAGE",
            "description": "Inventory resources",
            "examples": ["catalog", "list"],
        },
        "ACT.MANAGE.REPORT": {
            "category": "ACT",
            "subcategory": "MANAGE",
            "description": "Generate mgmt report",
            "examples": ["summarize", "review"],
        },
        # ===== PROPERTIES (PROP.*) - 150 concepts =====
        # STATE
        "PROP.STATE.ACTIVE": {
            "category": "PROP",
            "subcategory": "STATE",
            "description": "Active or enabled",
            "examples": ["active", "enabled", "on"],
        },
        "PROP.STATE.INACTIVE": {
            "category": "PROP",
            "subcategory": "STATE",
            "description": "Inactive or disabled",
            "examples": ["inactive", "disabled", "off"],
        },
        "PROP.STATE.PENDING": {
            "category": "PROP",
            "subcategory": "STATE",
            "description": "Pending or waiting",
            "examples": ["pending", "waiting", "queued"],
        },
        "PROP.STATE.COMPLETE": {
            "category": "PROP",
            "subcategory": "STATE",
            "description": "Completed",
            "examples": ["complete", "done", "finished"],
        },
        "PROP.STATE.ERROR": {
            "category": "PROP",
            "subcategory": "STATE",
            "description": "Error state",
            "examples": ["error", "failed", "broken"],
        },
        "PROP.STATE.RUNNING": {
            "category": "PROP",
            "subcategory": "STATE",
            "description": "Currently running",
            "examples": ["executing", "processing"],
        },
        "PROP.STATE.STOPPED": {
            "category": "PROP",
            "subcategory": "STATE",
            "description": "Stopped",
            "examples": ["halted", "terminated"],
        },
        "PROP.STATE.PAUSED": {
            "category": "PROP",
            "subcategory": "STATE",
            "description": "Paused",
            "examples": ["suspended", "frozen"],
        },
        "PROP.STATE.STARTING": {
            "category": "PROP",
            "subcategory": "STATE",
            "description": "Starting up",
            "examples": ["initializing", "booting"],
        },
        "PROP.STATE.STOPPING": {
            "category": "PROP",
            "subcategory": "STATE",
            "description": "Shutting down",
            "examples": ["terminating", "closing"],
        },
        "PROP.STATE.DEGRADED": {
            "category": "PROP",
            "subcategory": "STATE",
            "description": "Degraded performance",
            "examples": ["impaired", "limited"],
        },
        "PROP.STATE.HEALTHY": {
            "category": "PROP",
            "subcategory": "STATE",
            "description": "Healthy state",
            "examples": ["ok", "normal"],
        },
        "PROP.STATE.UNHEALTHY": {
            "category": "PROP",
            "subcategory": "STATE",
            "description": "Unhealthy state",
            "examples": ["sick", "failing"],
        },
        "PROP.STATE.READY": {
            "category": "PROP",
            "subcategory": "STATE",
            "description": "Ready for use",
            "examples": ["available", "prepared"],
        },
        "PROP.STATE.BUSY": {
            "category": "PROP",
            "subcategory": "STATE",
            "description": "Busy or occupied",
            "examples": ["occupied", "working"],
        },
        "PROP.STATE.IDLE": {
            "category": "PROP",
            "subcategory": "STATE",
            "description": "Idle or free",
            "examples": ["free", "unused"],
        },
        "PROP.STATE.LOCKED": {
            "category": "PROP",
            "subcategory": "STATE",
            "description": "Locked state",
            "examples": ["held", "acquired"],
        },
        "PROP.STATE.UNLOCKED": {
            "category": "PROP",
            "subcategory": "STATE",
            "description": "Unlocked state",
            "examples": ["free", "released"],
        },
        "PROP.STATE.CONNECTED": {
            "category": "PROP",
            "subcategory": "STATE",
            "description": "Connected",
            "examples": ["online", "linked"],
        },
        "PROP.STATE.DISCONNECTED": {
            "category": "PROP",
            "subcategory": "STATE",
            "description": "Disconnected",
            "examples": ["offline", "unlinked"],
        },
        # QUALITY
        "PROP.QUALITY.HIGH": {
            "category": "PROP",
            "subcategory": "QUALITY",
            "description": "High quality",
            "examples": ["excellent", "premium"],
        },
        "PROP.QUALITY.MEDIUM": {
            "category": "PROP",
            "subcategory": "QUALITY",
            "description": "Medium quality",
            "examples": ["average", "standard"],
        },
        "PROP.QUALITY.LOW": {
            "category": "PROP",
            "subcategory": "QUALITY",
            "description": "Low quality",
            "examples": ["poor", "inferior"],
        },
        "PROP.QUALITY.VERIFIED": {
            "category": "PROP",
            "subcategory": "QUALITY",
            "description": "Verified quality",
            "examples": ["certified", "checked"],
        },
        "PROP.QUALITY.UNVERIFIED": {
            "category": "PROP",
            "subcategory": "QUALITY",
            "description": "Unverified quality",
            "examples": ["unchecked", "unknown"],
        },
        "PROP.QUALITY.TRUSTED": {
            "category": "PROP",
            "subcategory": "QUALITY",
            "description": "Trusted source",
            "examples": ["reliable", "proven"],
        },
        "PROP.QUALITY.UNTRUSTED": {
            "category": "PROP",
            "subcategory": "QUALITY",
            "description": "Untrusted source",
            "examples": ["suspicious", "unknown"],
        },
        "PROP.QUALITY.ACCURATE": {
            "category": "PROP",
            "subcategory": "QUALITY",
            "description": "Accurate result",
            "examples": ["precise", "exact"],
        },
        "PROP.QUALITY.APPROXIMATE": {
            "category": "PROP",
            "subcategory": "QUALITY",
            "description": "Approximate result",
            "examples": ["rough", "estimated"],
        },
        "PROP.QUALITY.COMPLETE": {
            "category": "PROP",
            "subcategory": "QUALITY",
            "description": "Complete data",
            "examples": ["full", "whole"],
        },
        "PROP.QUALITY.PARTIAL": {
            "category": "PROP",
            "subcategory": "QUALITY",
            "description": "Partial data",
            "examples": ["incomplete", "fragment"],
        },
        "PROP.QUALITY.FRESH": {
            "category": "PROP",
            "subcategory": "QUALITY",
            "description": "Fresh or recent",
            "examples": ["current", "new"],
        },
        "PROP.QUALITY.STALE": {
            "category": "PROP",
            "subcategory": "QUALITY",
            "description": "Stale or outdated",
            "examples": ["old", "expired"],
        },
        "PROP.QUALITY.STABLE": {
            "category": "PROP",
            "subcategory": "QUALITY",
            "description": "Stable version",
            "examples": ["production", "release"],
        },
        "PROP.QUALITY.EXPERIMENTAL": {
            "category": "PROP",
            "subcategory": "QUALITY",
            "description": "Experimental version",
            "examples": ["beta", "preview"],
        },
        # SIZE
        "PROP.SIZE.LARGE": {
            "category": "PROP",
            "subcategory": "SIZE",
            "description": "Large size",
            "examples": ["big", "huge", "massive"],
        },
        "PROP.SIZE.MEDIUM": {
            "category": "PROP",
            "subcategory": "SIZE",
            "description": "Medium size",
            "examples": ["average", "standard"],
        },
        "PROP.SIZE.SMALL": {
            "category": "PROP",
            "subcategory": "SIZE",
            "description": "Small size",
            "examples": ["tiny", "little", "mini"],
        },
        "PROP.SIZE.EMPTY": {
            "category": "PROP",
            "subcategory": "SIZE",
            "description": "Empty or zero size",
            "examples": ["none", "null"],
        },
        "PROP.SIZE.UNLIMITED": {
            "category": "PROP",
            "subcategory": "SIZE",
            "description": "Unlimited size",
            "examples": ["infinite", "unbounded"],
        },
        "PROP.SIZE.FIXED": {
            "category": "PROP",
            "subcategory": "SIZE",
            "description": "Fixed size",
            "examples": ["constant", "static"],
        },
        "PROP.SIZE.VARIABLE": {
            "category": "PROP",
            "subcategory": "SIZE",
            "description": "Variable size",
            "examples": ["dynamic", "flexible"],
        },
        "PROP.SIZE.GROWING": {
            "category": "PROP",
            "subcategory": "SIZE",
            "description": "Growing size",
            "examples": ["expanding", "increasing"],
        },
        "PROP.SIZE.SHRINKING": {
            "category": "PROP",
            "subcategory": "SIZE",
            "description": "Shrinking size",
            "examples": ["decreasing", "reducing"],
        },
        "PROP.SIZE.BYTES": {
            "category": "PROP",
            "subcategory": "SIZE",
            "description": "Size in bytes",
            "examples": ["b", "octets"],
        },
        "PROP.SIZE.KILOBYTES": {
            "category": "PROP",
            "subcategory": "SIZE",
            "description": "Size in kilobytes",
            "examples": ["kb", "kibibytes"],
        },
        "PROP.SIZE.MEGABYTES": {
            "category": "PROP",
            "subcategory": "SIZE",
            "description": "Size in megabytes",
            "examples": ["mb", "mibibytes"],
        },
        "PROP.SIZE.GIGABYTES": {
            "category": "PROP",
            "subcategory": "SIZE",
            "description": "Size in gigabytes",
            "examples": ["gb", "gibibytes"],
        },
        "PROP.SIZE.TERABYTES": {
            "category": "PROP",
            "subcategory": "SIZE",
            "description": "Size in terabytes",
            "examples": ["tb", "tebibytes"],
        },
        "PROP.SIZE.COUNT": {
            "category": "PROP",
            "subcategory": "SIZE",
            "description": "Count or quantity",
            "examples": ["number", "total"],
        },
        # PRIORITY
        "PROP.PRIORITY.CRITICAL": {
            "category": "PROP",
            "subcategory": "PRIORITY",
            "description": "Critical priority",
            "examples": ["p0", "emergency"],
        },
        "PROP.PRIORITY.HIGH": {
            "category": "PROP",
            "subcategory": "PRIORITY",
            "description": "High priority",
            "examples": ["urgent", "important"],
        },
        "PROP.PRIORITY.MEDIUM": {
            "category": "PROP",
            "subcategory": "PRIORITY",
            "description": "Medium priority",
            "examples": ["normal", "standard"],
        },
        "PROP.PRIORITY.LOW": {
            "category": "PROP",
            "subcategory": "PRIORITY",
            "description": "Low priority",
            "examples": ["minor", "trivial"],
        },
        "PROP.PRIORITY.BACKGROUND": {
            "category": "PROP",
            "subcategory": "PRIORITY",
            "description": "Background priority",
            "examples": ["deferred", "lazy"],
        },
        "PROP.PRIORITY.REALTIME": {
            "category": "PROP",
            "subcategory": "PRIORITY",
            "description": "Real-time priority",
            "examples": ["immediate", "instant"],
        },
        "PROP.PRIORITY.BATCH": {
            "category": "PROP",
            "subcategory": "PRIORITY",
            "description": "Batch priority",
            "examples": ["bulk", "queued"],
        },
        "PROP.PRIORITY.SCHEDULED": {
            "category": "PROP",
            "subcategory": "PRIORITY",
            "description": "Scheduled priority",
            "examples": ["planned", "timed"],
        },
        "PROP.PRIORITY.INTERACTIVE": {
            "category": "PROP",
            "subcategory": "PRIORITY",
            "description": "Interactive priority",
            "examples": ["user-facing"],
        },
        "PROP.PRIORITY.SYSTEM": {
            "category": "PROP",
            "subcategory": "PRIORITY",
            "description": "System priority",
            "examples": ["infrastructure"],
        },
        # DETAIL
        "PROP.DETAIL.HIGH": {
            "category": "PROP",
            "subcategory": "DETAIL",
            "description": "High detail",
            "examples": ["verbose", "comprehensive"],
        },
        "PROP.DETAIL.MEDIUM": {
            "category": "PROP",
            "subcategory": "DETAIL",
            "description": "Medium detail",
            "examples": ["standard", "normal"],
        },
        "PROP.DETAIL.LOW": {
            "category": "PROP",
            "subcategory": "DETAIL",
            "description": "Low detail",
            "examples": ["brief", "summary"],
        },
        "PROP.DETAIL.MINIMAL": {
            "category": "PROP",
            "subcategory": "DETAIL",
            "description": "Minimal detail",
            "examples": ["bare", "essential"],
        },
        "PROP.DETAIL.FULL": {
            "category": "PROP",
            "subcategory": "DETAIL",
            "description": "Full detail",
            "examples": ["complete", "exhaustive"],
        },
        "PROP.DETAIL.DEBUG": {
            "category": "PROP",
            "subcategory": "DETAIL",
            "description": "Debug level detail",
            "examples": ["trace", "diagnostic"],
        },
        "PROP.DETAIL.METADATA": {
            "category": "PROP",
            "subcategory": "DETAIL",
            "description": "Metadata only",
            "examples": ["headers", "info"],
        },
        "PROP.DETAIL.PREVIEW": {
            "category": "PROP",
            "subcategory": "DETAIL",
            "description": "Preview level",
            "examples": ["thumbnail", "snippet"],
        },
        "PROP.DETAIL.RAW": {
            "category": "PROP",
            "subcategory": "DETAIL",
            "description": "Raw unprocessed",
            "examples": ["original", "source"],
        },
        "PROP.DETAIL.FORMATTED": {
            "category": "PROP",
            "subcategory": "DETAIL",
            "description": "Formatted output",
            "examples": ["rendered", "styled"],
        },
        # TYPE
        "PROP.TYPE.SYNC": {
            "category": "PROP",
            "subcategory": "TYPE",
            "description": "Synchronous",
            "examples": ["blocking", "immediate"],
        },
        "PROP.TYPE.ASYNC": {
            "category": "PROP",
            "subcategory": "TYPE",
            "description": "Asynchronous",
            "examples": ["nonblocking", "deferred"],
        },
        "PROP.TYPE.STREAMING": {
            "category": "PROP",
            "subcategory": "TYPE",
            "description": "Streaming mode",
            "examples": ["continuous", "realtime"],
        },
        "PROP.TYPE.BATCH": {
            "category": "PROP",
            "subcategory": "TYPE",
            "description": "Batch mode",
            "examples": ["bulk", "grouped"],
        },
        "PROP.TYPE.ONESHOT": {
            "category": "PROP",
            "subcategory": "TYPE",
            "description": "One-shot operation",
            "examples": ["single", "once"],
        },
        "PROP.TYPE.RECURRING": {
            "category": "PROP",
            "subcategory": "TYPE",
            "description": "Recurring operation",
            "examples": ["periodic", "repeated"],
        },
        "PROP.TYPE.TRANSIENT": {
            "category": "PROP",
            "subcategory": "TYPE",
            "description": "Transient data",
            "examples": ["temporary", "ephemeral"],
        },
        "PROP.TYPE.PERSISTENT": {
            "category": "PROP",
            "subcategory": "TYPE",
            "description": "Persistent data",
            "examples": ["durable", "permanent"],
        },
        "PROP.TYPE.CACHED": {
            "category": "PROP",
            "subcategory": "TYPE",
            "description": "Cached data",
            "examples": ["buffered", "stored"],
        },
        "PROP.TYPE.COMPUTED": {
            "category": "PROP",
            "subcategory": "TYPE",
            "description": "Computed value",
            "examples": ["calculated", "derived"],
        },
        "PROP.TYPE.MUTABLE": {
            "category": "PROP",
            "subcategory": "TYPE",
            "description": "Mutable data",
            "examples": ["changeable", "writable"],
        },
        "PROP.TYPE.IMMUTABLE": {
            "category": "PROP",
            "subcategory": "TYPE",
            "description": "Immutable data",
            "examples": ["readonly", "frozen"],
        },
        "PROP.TYPE.PUBLIC": {
            "category": "PROP",
            "subcategory": "TYPE",
            "description": "Public access",
            "examples": ["open", "shared"],
        },
        "PROP.TYPE.PRIVATE": {
            "category": "PROP",
            "subcategory": "TYPE",
            "description": "Private access",
            "examples": ["restricted", "internal"],
        },
        "PROP.TYPE.PROTECTED": {
            "category": "PROP",
            "subcategory": "TYPE",
            "description": "Protected access",
            "examples": ["guarded", "limited"],
        },
        # PERFORMANCE
        "PROP.PERF.FAST": {
            "category": "PROP",
            "subcategory": "PERFORMANCE",
            "description": "Fast performance",
            "examples": ["quick", "rapid"],
        },
        "PROP.PERF.SLOW": {
            "category": "PROP",
            "subcategory": "PERFORMANCE",
            "description": "Slow performance",
            "examples": ["sluggish", "delayed"],
        },
        "PROP.PERF.OPTIMAL": {
            "category": "PROP",
            "subcategory": "PERFORMANCE",
            "description": "Optimal performance",
            "examples": ["best", "peak"],
        },
        "PROP.PERF.DEGRADED": {
            "category": "PROP",
            "subcategory": "PERFORMANCE",
            "description": "Degraded performance",
            "examples": ["reduced", "impaired"],
        },
        "PROP.PERF.LATENCY.LOW": {
            "category": "PROP",
            "subcategory": "PERFORMANCE",
            "description": "Low latency",
            "examples": ["quick response"],
        },
        "PROP.PERF.LATENCY.HIGH": {
            "category": "PROP",
            "subcategory": "PERFORMANCE",
            "description": "High latency",
            "examples": ["slow response"],
        },
        "PROP.PERF.THROUGHPUT.HIGH": {
            "category": "PROP",
            "subcategory": "PERFORMANCE",
            "description": "High throughput",
            "examples": ["fast", "efficient"],
        },
        "PROP.PERF.THROUGHPUT.LOW": {
            "category": "PROP",
            "subcategory": "PERFORMANCE",
            "description": "Low throughput",
            "examples": ["bottleneck"],
        },
        "PROP.PERF.CPU.HIGH": {
            "category": "PROP",
            "subcategory": "PERFORMANCE",
            "description": "High CPU usage",
            "examples": ["intensive", "heavy"],
        },
        "PROP.PERF.CPU.LOW": {
            "category": "PROP",
            "subcategory": "PERFORMANCE",
            "description": "Low CPU usage",
            "examples": ["lightweight", "efficient"],
        },
        "PROP.PERF.MEMORY.HIGH": {
            "category": "PROP",
            "subcategory": "PERFORMANCE",
            "description": "High memory usage",
            "examples": ["intensive"],
        },
        "PROP.PERF.MEMORY.LOW": {
            "category": "PROP",
            "subcategory": "PERFORMANCE",
            "description": "Low memory usage",
            "examples": ["efficient"],
        },
        "PROP.PERF.IO.HIGH": {
            "category": "PROP",
            "subcategory": "PERFORMANCE",
            "description": "High I/O usage",
            "examples": ["disk-heavy"],
        },
        "PROP.PERF.IO.LOW": {
            "category": "PROP",
            "subcategory": "PERFORMANCE",
            "description": "Low I/O usage",
            "examples": ["lightweight"],
        },
        "PROP.PERF.NETWORK.HIGH": {
            "category": "PROP",
            "subcategory": "PERFORMANCE",
            "description": "High network usage",
            "examples": ["bandwidth-heavy"],
        },
        # CONFIDENCE
        "PROP.CONFIDENCE.CERTAIN": {
            "category": "PROP",
            "subcategory": "CONFIDENCE",
            "description": "Certain result",
            "examples": ["definite", "100%"],
        },
        "PROP.CONFIDENCE.HIGH": {
            "category": "PROP",
            "subcategory": "CONFIDENCE",
            "description": "High confidence",
            "examples": ["likely", "probable"],
        },
        "PROP.CONFIDENCE.MEDIUM": {
            "category": "PROP",
            "subcategory": "CONFIDENCE",
            "description": "Medium confidence",
            "examples": ["possible", "maybe"],
        },
        "PROP.CONFIDENCE.LOW": {
            "category": "PROP",
            "subcategory": "CONFIDENCE",
            "description": "Low confidence",
            "examples": ["unlikely", "uncertain"],
        },
        "PROP.CONFIDENCE.UNKNOWN": {
            "category": "PROP",
            "subcategory": "CONFIDENCE",
            "description": "Unknown confidence",
            "examples": ["undetermined"],
        },
        "PROP.CONFIDENCE.SCORE": {
            "category": "PROP",
            "subcategory": "CONFIDENCE",
            "description": "Numeric score",
            "examples": ["probability", "weight"],
        },
        "PROP.CONFIDENCE.THRESHOLD": {
            "category": "PROP",
            "subcategory": "CONFIDENCE",
            "description": "Confidence threshold",
            "examples": ["cutoff", "limit"],
        },
        "PROP.CONFIDENCE.CALIBRATED": {
            "category": "PROP",
            "subcategory": "CONFIDENCE",
            "description": "Calibrated estimate",
            "examples": ["adjusted"],
        },
        "PROP.CONFIDENCE.PREDICTED": {
            "category": "PROP",
            "subcategory": "CONFIDENCE",
            "description": "Predicted value",
            "examples": ["estimated"],
        },
        "PROP.CONFIDENCE.OBSERVED": {
            "category": "PROP",
            "subcategory": "CONFIDENCE",
            "description": "Observed value",
            "examples": ["measured", "actual"],
        },
        # FORMAT
        "PROP.FORMAT.TEXT": {
            "category": "PROP",
            "subcategory": "FORMAT",
            "description": "Plain text format",
            "examples": ["txt", "ascii"],
        },
        "PROP.FORMAT.JSON": {
            "category": "PROP",
            "subcategory": "FORMAT",
            "description": "JSON format",
            "examples": ["application/json"],
        },
        "PROP.FORMAT.BINARY": {
            "category": "PROP",
            "subcategory": "FORMAT",
            "description": "Binary format",
            "examples": ["raw", "bytes"],
        },
        "PROP.FORMAT.XML": {
            "category": "PROP",
            "subcategory": "FORMAT",
            "description": "XML format",
            "examples": ["application/xml"],
        },
        "PROP.FORMAT.CSV": {
            "category": "PROP",
            "subcategory": "FORMAT",
            "description": "CSV format",
            "examples": ["text/csv"],
        },
        "PROP.FORMAT.HTML": {
            "category": "PROP",
            "subcategory": "FORMAT",
            "description": "HTML format",
            "examples": ["text/html"],
        },
        "PROP.FORMAT.PROTOBUF": {
            "category": "PROP",
            "subcategory": "FORMAT",
            "description": "Protobuf format",
            "examples": ["proto"],
        },
        "PROP.FORMAT.MSGPACK": {
            "category": "PROP",
            "subcategory": "FORMAT",
            "description": "MessagePack format",
            "examples": ["binary json"],
        },
        "PROP.FORMAT.AVRO": {
            "category": "PROP",
            "subcategory": "FORMAT",
            "description": "Avro format",
            "examples": ["schema-based"],
        },
        "PROP.FORMAT.PARQUET": {
            "category": "PROP",
            "subcategory": "FORMAT",
            "description": "Parquet format",
            "examples": ["columnar"],
        },
        # SCOPE
        "PROP.SCOPE.LOCAL": {
            "category": "PROP",
            "subcategory": "SCOPE",
            "description": "Local scope",
            "examples": ["instance", "node"],
        },
        "PROP.SCOPE.GLOBAL": {
            "category": "PROP",
            "subcategory": "SCOPE",
            "description": "Global scope",
            "examples": ["cluster", "world"],
        },
        "PROP.SCOPE.REGIONAL": {
            "category": "PROP",
            "subcategory": "SCOPE",
            "description": "Regional scope",
            "examples": ["zone", "region"],
        },
        "PROP.SCOPE.NAMESPACE": {
            "category": "PROP",
            "subcategory": "SCOPE",
            "description": "Namespace scope",
            "examples": ["tenant", "project"],
        },
        "PROP.SCOPE.SESSION": {
            "category": "PROP",
            "subcategory": "SCOPE",
            "description": "Session scope",
            "examples": ["connection", "user"],
        },
        "PROP.SCOPE.REQUEST": {
            "category": "PROP",
            "subcategory": "SCOPE",
            "description": "Request scope",
            "examples": ["call", "invocation"],
        },
        "PROP.SCOPE.TRANSACTION": {
            "category": "PROP",
            "subcategory": "SCOPE",
            "description": "Transaction scope",
            "examples": ["atomic", "unit"],
        },
        "PROP.SCOPE.THREAD": {
            "category": "PROP",
            "subcategory": "SCOPE",
            "description": "Thread scope",
            "examples": ["worker", "coroutine"],
        },
        "PROP.SCOPE.PROCESS": {
            "category": "PROP",
            "subcategory": "SCOPE",
            "description": "Process scope",
            "examples": ["pid", "container"],
        },
        "PROP.SCOPE.CLUSTER": {
            "category": "PROP",
            "subcategory": "SCOPE",
            "description": "Cluster scope",
            "examples": ["fleet", "swarm"],
        },
        # ENCODING
        "PROP.ENCODING.UTF8": {
            "category": "PROP",
            "subcategory": "ENCODING",
            "description": "UTF-8 encoding",
            "examples": ["unicode", "utf8"],
        },
        "PROP.ENCODING.ASCII": {
            "category": "PROP",
            "subcategory": "ENCODING",
            "description": "ASCII encoding",
            "examples": ["7bit", "basic"],
        },
        "PROP.ENCODING.BASE64": {
            "category": "PROP",
            "subcategory": "ENCODING",
            "description": "Base64 encoding",
            "examples": ["b64", "encoded"],
        },
        "PROP.ENCODING.HEX": {
            "category": "PROP",
            "subcategory": "ENCODING",
            "description": "Hexadecimal encoding",
            "examples": ["hex", "base16"],
        },
        "PROP.ENCODING.URL": {
            "category": "PROP",
            "subcategory": "ENCODING",
            "description": "URL encoding",
            "examples": ["percent", "urlencode"],
        },
        "PROP.ENCODING.GZIP": {
            "category": "PROP",
            "subcategory": "ENCODING",
            "description": "Gzip compression",
            "examples": ["gz", "deflate"],
        },
        "PROP.ENCODING.ZSTD": {
            "category": "PROP",
            "subcategory": "ENCODING",
            "description": "Zstandard compression",
            "examples": ["zstd"],
        },
        "PROP.ENCODING.LZ4": {
            "category": "PROP",
            "subcategory": "ENCODING",
            "description": "LZ4 compression",
            "examples": ["fast compress"],
        },
        "PROP.ENCODING.SNAPPY": {
            "category": "PROP",
            "subcategory": "ENCODING",
            "description": "Snappy compression",
            "examples": ["fast compress"],
        },
        "PROP.ENCODING.BROTLI": {
            "category": "PROP",
            "subcategory": "ENCODING",
            "description": "Brotli compression",
            "examples": ["br"],
        },
        # SECURITY
        "PROP.SECURITY.ENCRYPTED": {
            "category": "PROP",
            "subcategory": "SECURITY",
            "description": "Encrypted data",
            "examples": ["protected", "secured"],
        },
        "PROP.SECURITY.PLAINTEXT": {
            "category": "PROP",
            "subcategory": "SECURITY",
            "description": "Plaintext data",
            "examples": ["unencrypted", "clear"],
        },
        "PROP.SECURITY.SIGNED": {
            "category": "PROP",
            "subcategory": "SECURITY",
            "description": "Digitally signed",
            "examples": ["authenticated"],
        },
        "PROP.SECURITY.UNSIGNED": {
            "category": "PROP",
            "subcategory": "SECURITY",
            "description": "Not signed",
            "examples": ["unauthenticated"],
        },
        "PROP.SECURITY.CLASSIFIED": {
            "category": "PROP",
            "subcategory": "SECURITY",
            "description": "Classified data",
            "examples": ["secret", "sensitive"],
        },
        "PROP.SECURITY.PUBLIC": {
            "category": "PROP",
            "subcategory": "SECURITY",
            "description": "Public data",
            "examples": ["open", "unrestricted"],
        },
        "PROP.SECURITY.INTERNAL": {
            "category": "PROP",
            "subcategory": "SECURITY",
            "description": "Internal only",
            "examples": ["private", "restricted"],
        },
        "PROP.SECURITY.CONFIDENTIAL": {
            "category": "PROP",
            "subcategory": "SECURITY",
            "description": "Confidential data",
            "examples": ["private", "secret"],
        },
        "PROP.SECURITY.COMPLIANT": {
            "category": "PROP",
            "subcategory": "SECURITY",
            "description": "Compliance verified",
            "examples": ["approved"],
        },
        "PROP.SECURITY.NONCOMPLIANT": {
            "category": "PROP",
            "subcategory": "SECURITY",
            "description": "Not compliant",
            "examples": ["violation"],
        },
        # ===== RELATIONS (REL.*) - 100 concepts =====
        # STRUCTURAL
        "REL.CONTAINS": {
            "category": "REL",
            "subcategory": "STRUCTURAL",
            "description": "Contains relationship",
            "examples": ["includes", "has"],
        },
        "REL.PART.OF": {
            "category": "REL",
            "subcategory": "STRUCTURAL",
            "description": "Part of relationship",
            "examples": ["component", "member"],
        },
        "REL.PARENT.OF": {
            "category": "REL",
            "subcategory": "STRUCTURAL",
            "description": "Parent relationship",
            "examples": ["owner", "container"],
        },
        "REL.CHILD.OF": {
            "category": "REL",
            "subcategory": "STRUCTURAL",
            "description": "Child relationship",
            "examples": ["nested", "sub"],
        },
        "REL.SIBLING.OF": {
            "category": "REL",
            "subcategory": "STRUCTURAL",
            "description": "Sibling relationship",
            "examples": ["peer", "adjacent"],
        },
        "REL.ROOT.OF": {
            "category": "REL",
            "subcategory": "STRUCTURAL",
            "description": "Root element",
            "examples": ["top", "origin"],
        },
        "REL.LEAF.OF": {
            "category": "REL",
            "subcategory": "STRUCTURAL",
            "description": "Leaf element",
            "examples": ["terminal", "end"],
        },
        "REL.ANCESTOR.OF": {
            "category": "REL",
            "subcategory": "STRUCTURAL",
            "description": "Ancestor in hierarchy",
            "examples": ["grandparent"],
        },
        "REL.DESCENDANT.OF": {
            "category": "REL",
            "subcategory": "STRUCTURAL",
            "description": "Descendant in hierarchy",
            "examples": ["grandchild"],
        },
        "REL.MEMBER.OF": {
            "category": "REL",
            "subcategory": "STRUCTURAL",
            "description": "Member of group",
            "examples": ["belongs", "in"],
        },
        "REL.GROUP.OF": {
            "category": "REL",
            "subcategory": "STRUCTURAL",
            "description": "Group of items",
            "examples": ["collection", "set"],
        },
        "REL.INSTANCE.OF": {
            "category": "REL",
            "subcategory": "STRUCTURAL",
            "description": "Instance of type",
            "examples": ["example", "object"],
        },
        "REL.TYPE.OF": {
            "category": "REL",
            "subcategory": "STRUCTURAL",
            "description": "Type classification",
            "examples": ["class", "kind"],
        },
        "REL.SUBTYPE.OF": {
            "category": "REL",
            "subcategory": "STRUCTURAL",
            "description": "Subtype relationship",
            "examples": ["specialization"],
        },
        "REL.SUPERTYPE.OF": {
            "category": "REL",
            "subcategory": "STRUCTURAL",
            "description": "Supertype relationship",
            "examples": ["generalization"],
        },
        "REL.IMPLEMENTS": {
            "category": "REL",
            "subcategory": "STRUCTURAL",
            "description": "Implements interface",
            "examples": ["realizes"],
        },
        "REL.EXTENDS": {
            "category": "REL",
            "subcategory": "STRUCTURAL",
            "description": "Extends base",
            "examples": ["inherits", "derives"],
        },
        "REL.COMPOSED.OF": {
            "category": "REL",
            "subcategory": "STRUCTURAL",
            "description": "Composed of parts",
            "examples": ["built from"],
        },
        "REL.WRAPS": {
            "category": "REL",
            "subcategory": "STRUCTURAL",
            "description": "Wraps or decorates",
            "examples": ["decorates", "adapts"],
        },
        "REL.PROXIES": {
            "category": "REL",
            "subcategory": "STRUCTURAL",
            "description": "Proxies for",
            "examples": ["delegates", "represents"],
        },
        # ASSOCIATIVE
        "REL.RELATED.TO": {
            "category": "REL",
            "subcategory": "ASSOCIATIVE",
            "description": "Related to",
            "examples": ["associated", "linked"],
        },
        "REL.SIMILAR.TO": {
            "category": "REL",
            "subcategory": "ASSOCIATIVE",
            "description": "Similar to",
            "examples": ["like", "resembles"],
        },
        "REL.DIFFERENT.FROM": {
            "category": "REL",
            "subcategory": "ASSOCIATIVE",
            "description": "Different from",
            "examples": ["unlike", "distinct"],
        },
        "REL.EQUIVALENT.TO": {
            "category": "REL",
            "subcategory": "ASSOCIATIVE",
            "description": "Equivalent to",
            "examples": ["equal", "same as"],
        },
        "REL.OPPOSITE.OF": {
            "category": "REL",
            "subcategory": "ASSOCIATIVE",
            "description": "Opposite of",
            "examples": ["inverse", "contrary"],
        },
        "REL.ALIAS.OF": {
            "category": "REL",
            "subcategory": "ASSOCIATIVE",
            "description": "Alias for",
            "examples": ["synonym", "alternate"],
        },
        "REL.REFERENCE.TO": {
            "category": "REL",
            "subcategory": "ASSOCIATIVE",
            "description": "Reference to",
            "examples": ["pointer", "link"],
        },
        "REL.COPY.OF": {
            "category": "REL",
            "subcategory": "ASSOCIATIVE",
            "description": "Copy of original",
            "examples": ["clone", "duplicate"],
        },
        "REL.VERSION.OF": {
            "category": "REL",
            "subcategory": "ASSOCIATIVE",
            "description": "Version of",
            "examples": ["revision", "iteration"],
        },
        "REL.VARIANT.OF": {
            "category": "REL",
            "subcategory": "ASSOCIATIVE",
            "description": "Variant of",
            "examples": ["alternative", "option"],
        },
        "REL.COMPLEMENT.OF": {
            "category": "REL",
            "subcategory": "ASSOCIATIVE",
            "description": "Complement of",
            "examples": ["supplement"],
        },
        "REL.SUBSTITUTE.FOR": {
            "category": "REL",
            "subcategory": "ASSOCIATIVE",
            "description": "Substitute for",
            "examples": ["replacement"],
        },
        "REL.COMPATIBLE.WITH": {
            "category": "REL",
            "subcategory": "ASSOCIATIVE",
            "description": "Compatible with",
            "examples": ["works with"],
        },
        "REL.INCOMPATIBLE.WITH": {
            "category": "REL",
            "subcategory": "ASSOCIATIVE",
            "description": "Incompatible with",
            "examples": ["conflicts"],
        },
        "REL.MAPS.TO": {
            "category": "REL",
            "subcategory": "ASSOCIATIVE",
            "description": "Maps to target",
            "examples": ["corresponds", "translates"],
        },
        # DEPENDENCY
        "REL.DEPENDS.ON": {
            "category": "REL",
            "subcategory": "DEPENDENCY",
            "description": "Depends on",
            "examples": ["requires", "needs"],
        },
        "REL.REQUIRED.BY": {
            "category": "REL",
            "subcategory": "DEPENDENCY",
            "description": "Required by",
            "examples": ["needed by"],
        },
        "REL.OPTIONAL.FOR": {
            "category": "REL",
            "subcategory": "DEPENDENCY",
            "description": "Optional for",
            "examples": ["nice to have"],
        },
        "REL.BLOCKS": {
            "category": "REL",
            "subcategory": "DEPENDENCY",
            "description": "Blocks progress",
            "examples": ["prevents"],
        },
        "REL.BLOCKED.BY": {
            "category": "REL",
            "subcategory": "DEPENDENCY",
            "description": "Blocked by",
            "examples": ["waiting for"],
        },
        "REL.ENABLES": {
            "category": "REL",
            "subcategory": "DEPENDENCY",
            "description": "Enables capability",
            "examples": ["unlocks"],
        },
        "REL.ENABLED.BY": {
            "category": "REL",
            "subcategory": "DEPENDENCY",
            "description": "Enabled by",
            "examples": ["provided by"],
        },
        "REL.IMPORTS": {
            "category": "REL",
            "subcategory": "DEPENDENCY",
            "description": "Imports from",
            "examples": ["uses", "includes"],
        },
        "REL.EXPORTS": {
            "category": "REL",
            "subcategory": "DEPENDENCY",
            "description": "Exports to",
            "examples": ["provides", "shares"],
        },
        "REL.CONSUMES": {
            "category": "REL",
            "subcategory": "DEPENDENCY",
            "description": "Consumes resource",
            "examples": ["uses", "reads"],
        },
        "REL.PRODUCES": {
            "category": "REL",
            "subcategory": "DEPENDENCY",
            "description": "Produces output",
            "examples": ["creates", "writes"],
        },
        "REL.PROVIDES": {
            "category": "REL",
            "subcategory": "DEPENDENCY",
            "description": "Provides service",
            "examples": ["offers", "supplies"],
        },
        "REL.USES": {
            "category": "REL",
            "subcategory": "DEPENDENCY",
            "description": "Uses resource",
            "examples": ["utilizes"],
        },
        "REL.USED.BY": {
            "category": "REL",
            "subcategory": "DEPENDENCY",
            "description": "Used by consumer",
            "examples": ["consumed by"],
        },
        "REL.UPGRADES": {
            "category": "REL",
            "subcategory": "DEPENDENCY",
            "description": "Upgrades from",
            "examples": ["succeeds"],
        },
        # CAUSAL
        "REL.CAUSES": {
            "category": "REL",
            "subcategory": "CAUSAL",
            "description": "Causes effect",
            "examples": ["triggers", "produces"],
        },
        "REL.CAUSED.BY": {
            "category": "REL",
            "subcategory": "CAUSAL",
            "description": "Caused by source",
            "examples": ["due to"],
        },
        "REL.TRIGGERS": {
            "category": "REL",
            "subcategory": "CAUSAL",
            "description": "Triggers event",
            "examples": ["initiates"],
        },
        "REL.TRIGGERED.BY": {
            "category": "REL",
            "subcategory": "CAUSAL",
            "description": "Triggered by event",
            "examples": ["initiated by"],
        },
        "REL.PREVENTS": {
            "category": "REL",
            "subcategory": "CAUSAL",
            "description": "Prevents outcome",
            "examples": ["avoids", "blocks"],
        },
        "REL.MITIGATES": {
            "category": "REL",
            "subcategory": "CAUSAL",
            "description": "Mitigates risk",
            "examples": ["reduces"],
        },
        "REL.AMPLIFIES": {
            "category": "REL",
            "subcategory": "CAUSAL",
            "description": "Amplifies effect",
            "examples": ["increases"],
        },
        "REL.CORRELATES.WITH": {
            "category": "REL",
            "subcategory": "CAUSAL",
            "description": "Correlates with",
            "examples": ["associated"],
        },
        "REL.PRECEDES": {
            "category": "REL",
            "subcategory": "CAUSAL",
            "description": "Precedes in sequence",
            "examples": ["comes before"],
        },
        "REL.FOLLOWS": {
            "category": "REL",
            "subcategory": "CAUSAL",
            "description": "Follows in sequence",
            "examples": ["comes after"],
        },
        "REL.LEADS.TO": {
            "category": "REL",
            "subcategory": "CAUSAL",
            "description": "Leads to outcome",
            "examples": ["results in"],
        },
        "REL.RESULTS.FROM": {
            "category": "REL",
            "subcategory": "CAUSAL",
            "description": "Results from cause",
            "examples": ["comes from"],
        },
        "REL.INFLUENCES": {
            "category": "REL",
            "subcategory": "CAUSAL",
            "description": "Influences behavior",
            "examples": ["affects"],
        },
        "REL.INFLUENCED.BY": {
            "category": "REL",
            "subcategory": "CAUSAL",
            "description": "Influenced by",
            "examples": ["affected by"],
        },
        "REL.DETERMINES": {
            "category": "REL",
            "subcategory": "CAUSAL",
            "description": "Determines outcome",
            "examples": ["decides"],
        },
        # TEMPORAL
        "REL.BEFORE": {
            "category": "REL",
            "subcategory": "TEMPORAL",
            "description": "Before in time",
            "examples": ["prior", "earlier"],
        },
        "REL.AFTER": {
            "category": "REL",
            "subcategory": "TEMPORAL",
            "description": "After in time",
            "examples": ["later", "subsequent"],
        },
        "REL.CONCURRENT.WITH": {
            "category": "REL",
            "subcategory": "TEMPORAL",
            "description": "Concurrent with",
            "examples": ["simultaneous"],
        },
        "REL.STARTS.WITH": {
            "category": "REL",
            "subcategory": "TEMPORAL",
            "description": "Starts with event",
            "examples": ["begins at"],
        },
        "REL.ENDS.WITH": {
            "category": "REL",
            "subcategory": "TEMPORAL",
            "description": "Ends with event",
            "examples": ["finishes at"],
        },
        "REL.OVERLAPS.WITH": {
            "category": "REL",
            "subcategory": "TEMPORAL",
            "description": "Overlaps in time",
            "examples": ["intersects"],
        },
        "REL.DURING": {
            "category": "REL",
            "subcategory": "TEMPORAL",
            "description": "During period",
            "examples": ["within"],
        },
        "REL.REPLACES": {
            "category": "REL",
            "subcategory": "TEMPORAL",
            "description": "Replaces previous",
            "examples": ["supersedes"],
        },
        "REL.REPLACED.BY": {
            "category": "REL",
            "subcategory": "TEMPORAL",
            "description": "Replaced by newer",
            "examples": ["superseded"],
        },
        "REL.EXPIRES.AT": {
            "category": "REL",
            "subcategory": "TEMPORAL",
            "description": "Expires at time",
            "examples": ["until", "valid until"],
        },
        # OWNERSHIP
        "REL.OWNS": {
            "category": "REL",
            "subcategory": "OWNERSHIP",
            "description": "Owns resource",
            "examples": ["possesses"],
        },
        "REL.OWNED.BY": {
            "category": "REL",
            "subcategory": "OWNERSHIP",
            "description": "Owned by entity",
            "examples": ["belongs to"],
        },
        "REL.CREATED.BY": {
            "category": "REL",
            "subcategory": "OWNERSHIP",
            "description": "Created by agent",
            "examples": ["authored by"],
        },
        "REL.MANAGED.BY": {
            "category": "REL",
            "subcategory": "OWNERSHIP",
            "description": "Managed by agent",
            "examples": ["administered by"],
        },
        "REL.ASSIGNED.TO": {
            "category": "REL",
            "subcategory": "OWNERSHIP",
            "description": "Assigned to agent",
            "examples": ["delegated to"],
        },
        "REL.SHARED.WITH": {
            "category": "REL",
            "subcategory": "OWNERSHIP",
            "description": "Shared with agent",
            "examples": ["accessible by"],
        },
        "REL.RESTRICTED.TO": {
            "category": "REL",
            "subcategory": "OWNERSHIP",
            "description": "Restricted to agent",
            "examples": ["limited to"],
        },
        "REL.GRANTED.TO": {
            "category": "REL",
            "subcategory": "OWNERSHIP",
            "description": "Granted to agent",
            "examples": ["permitted"],
        },
        "REL.REVOKED.FROM": {
            "category": "REL",
            "subcategory": "OWNERSHIP",
            "description": "Revoked from agent",
            "examples": ["removed"],
        },
        "REL.DELEGATED.TO": {
            "category": "REL",
            "subcategory": "OWNERSHIP",
            "description": "Delegated to agent",
            "examples": ["forwarded"],
        },
        # SPATIAL
        "REL.LOCATED.AT": {
            "category": "REL",
            "subcategory": "SPATIAL",
            "description": "Located at place",
            "examples": ["positioned"],
        },
        "REL.ADJACENT.TO": {
            "category": "REL",
            "subcategory": "SPATIAL",
            "description": "Adjacent to",
            "examples": ["next to", "beside"],
        },
        "REL.CONNECTED.TO": {
            "category": "REL",
            "subcategory": "SPATIAL",
            "description": "Connected to",
            "examples": ["linked"],
        },
        "REL.DISCONNECTED.FROM": {
            "category": "REL",
            "subcategory": "SPATIAL",
            "description": "Disconnected from",
            "examples": ["separated"],
        },
        "REL.UPSTREAM.OF": {
            "category": "REL",
            "subcategory": "SPATIAL",
            "description": "Upstream in flow",
            "examples": ["before"],
        },
        "REL.DOWNSTREAM.OF": {
            "category": "REL",
            "subcategory": "SPATIAL",
            "description": "Downstream in flow",
            "examples": ["after"],
        },
        "REL.INPUT.TO": {
            "category": "REL",
            "subcategory": "SPATIAL",
            "description": "Input to process",
            "examples": ["feeds"],
        },
        "REL.OUTPUT.OF": {
            "category": "REL",
            "subcategory": "SPATIAL",
            "description": "Output of process",
            "examples": ["produces"],
        },
        "REL.SOURCE.OF": {
            "category": "REL",
            "subcategory": "SPATIAL",
            "description": "Source of data",
            "examples": ["origin"],
        },
        "REL.TARGET.OF": {
            "category": "REL",
            "subcategory": "SPATIAL",
            "description": "Target of action",
            "examples": ["destination"],
        },
        "REL.ENDPOINT.OF": {
            "category": "REL",
            "subcategory": "SPATIAL",
            "description": "Endpoint of",
            "examples": ["terminus"],
        },
        "REL.GATEWAY.TO": {
            "category": "REL",
            "subcategory": "SPATIAL",
            "description": "Gateway to resource",
            "examples": ["entry point"],
        },
        "REL.BRIDGE.BETWEEN": {
            "category": "REL",
            "subcategory": "SPATIAL",
            "description": "Bridge between",
            "examples": ["connector"],
        },
        "REL.LAYER.OF": {
            "category": "REL",
            "subcategory": "SPATIAL",
            "description": "Layer in stack",
            "examples": ["level", "tier"],
        },
        "REL.CHANNEL.TO": {
            "category": "REL",
            "subcategory": "SPATIAL",
            "description": "Communication channel",
            "examples": ["pipe", "conduit"],
        },
        # ===== LOGIC (LOG.*) - 50 concepts =====
        # OPERATOR
        "LOG.AND": {
            "category": "LOG",
            "subcategory": "OPERATOR",
            "description": "Logical AND",
            "examples": ["all", "both"],
        },
        "LOG.OR": {
            "category": "LOG",
            "subcategory": "OPERATOR",
            "description": "Logical OR",
            "examples": ["any", "either"],
        },
        "LOG.NOT": {
            "category": "LOG",
            "subcategory": "OPERATOR",
            "description": "Logical NOT",
            "examples": ["negate", "inverse"],
        },
        "LOG.XOR": {
            "category": "LOG",
            "subcategory": "OPERATOR",
            "description": "Exclusive OR",
            "examples": ["one of"],
        },
        "LOG.NAND": {
            "category": "LOG",
            "subcategory": "OPERATOR",
            "description": "NOT AND",
            "examples": ["not all"],
        },
        "LOG.NOR": {
            "category": "LOG",
            "subcategory": "OPERATOR",
            "description": "NOT OR",
            "examples": ["none"],
        },
        "LOG.IMPLIES": {
            "category": "LOG",
            "subcategory": "OPERATOR",
            "description": "Logical implication",
            "examples": ["therefore"],
        },
        "LOG.IFF": {
            "category": "LOG",
            "subcategory": "OPERATOR",
            "description": "If and only if",
            "examples": ["equivalent"],
        },
        "LOG.EXISTS": {
            "category": "LOG",
            "subcategory": "OPERATOR",
            "description": "Existential quantifier",
            "examples": ["some", "there exists"],
        },
        "LOG.FORALL": {
            "category": "LOG",
            "subcategory": "OPERATOR",
            "description": "Universal quantifier",
            "examples": ["all", "every"],
        },
        "LOG.TRUE": {
            "category": "LOG",
            "subcategory": "OPERATOR",
            "description": "Boolean true",
            "examples": ["yes", "1"],
        },
        "LOG.FALSE": {
            "category": "LOG",
            "subcategory": "OPERATOR",
            "description": "Boolean false",
            "examples": ["no", "0"],
        },
        "LOG.NULL": {
            "category": "LOG",
            "subcategory": "OPERATOR",
            "description": "Null or undefined",
            "examples": ["none", "nil"],
        },
        "LOG.EMPTY": {
            "category": "LOG",
            "subcategory": "OPERATOR",
            "description": "Empty value",
            "examples": ["blank", "void"],
        },
        "LOG.UNKNOWN": {
            "category": "LOG",
            "subcategory": "OPERATOR",
            "description": "Unknown value",
            "examples": ["undefined", "indeterminate"],
        },
        # CONDITIONAL
        "LOG.IF": {
            "category": "LOG",
            "subcategory": "CONDITIONAL",
            "description": "If condition",
            "examples": ["when", "provided"],
        },
        "LOG.THEN": {
            "category": "LOG",
            "subcategory": "CONDITIONAL",
            "description": "Then clause",
            "examples": ["result", "consequence"],
        },
        "LOG.ELSE": {
            "category": "LOG",
            "subcategory": "CONDITIONAL",
            "description": "Else clause",
            "examples": ["otherwise", "alternative"],
        },
        "LOG.SWITCH": {
            "category": "LOG",
            "subcategory": "CONDITIONAL",
            "description": "Switch statement",
            "examples": ["case", "match"],
        },
        "LOG.CASE": {
            "category": "LOG",
            "subcategory": "CONDITIONAL",
            "description": "Case branch",
            "examples": ["option", "variant"],
        },
        "LOG.DEFAULT": {
            "category": "LOG",
            "subcategory": "CONDITIONAL",
            "description": "Default case",
            "examples": ["fallback", "otherwise"],
        },
        "LOG.WHILE": {
            "category": "LOG",
            "subcategory": "CONDITIONAL",
            "description": "While condition",
            "examples": ["loop", "repeat"],
        },
        "LOG.UNTIL": {
            "category": "LOG",
            "subcategory": "CONDITIONAL",
            "description": "Until condition",
            "examples": ["stop when"],
        },
        "LOG.WHEN": {
            "category": "LOG",
            "subcategory": "CONDITIONAL",
            "description": "When triggered",
            "examples": ["on event"],
        },
        "LOG.UNLESS": {
            "category": "LOG",
            "subcategory": "CONDITIONAL",
            "description": "Unless condition",
            "examples": ["except when"],
        },
        # COMPARISON
        "LOG.EQUAL": {
            "category": "LOG",
            "subcategory": "COMPARISON",
            "description": "Equal to",
            "examples": ["eq", "same"],
        },
        "LOG.NOT.EQUAL": {
            "category": "LOG",
            "subcategory": "COMPARISON",
            "description": "Not equal to",
            "examples": ["neq", "different"],
        },
        "LOG.GREATER": {
            "category": "LOG",
            "subcategory": "COMPARISON",
            "description": "Greater than",
            "examples": ["gt", "more"],
        },
        "LOG.LESS": {
            "category": "LOG",
            "subcategory": "COMPARISON",
            "description": "Less than",
            "examples": ["lt", "fewer"],
        },
        "LOG.GREATER.EQUAL": {
            "category": "LOG",
            "subcategory": "COMPARISON",
            "description": "Greater or equal",
            "examples": ["gte", "at least"],
        },
        "LOG.LESS.EQUAL": {
            "category": "LOG",
            "subcategory": "COMPARISON",
            "description": "Less or equal",
            "examples": ["lte", "at most"],
        },
        "LOG.BETWEEN": {
            "category": "LOG",
            "subcategory": "COMPARISON",
            "description": "Between values",
            "examples": ["range", "within"],
        },
        "LOG.IN": {
            "category": "LOG",
            "subcategory": "COMPARISON",
            "description": "Value in set",
            "examples": ["member of"],
        },
        "LOG.NOT.IN": {
            "category": "LOG",
            "subcategory": "COMPARISON",
            "description": "Value not in set",
            "examples": ["not member"],
        },
        "LOG.LIKE": {
            "category": "LOG",
            "subcategory": "COMPARISON",
            "description": "Pattern match",
            "examples": ["matches", "regex"],
        },
        "LOG.NOT.LIKE": {
            "category": "LOG",
            "subcategory": "COMPARISON",
            "description": "No pattern match",
            "examples": ["not matches"],
        },
        "LOG.CONTAINS": {
            "category": "LOG",
            "subcategory": "COMPARISON",
            "description": "Contains value",
            "examples": ["includes", "has"],
        },
        "LOG.STARTS.WITH": {
            "category": "LOG",
            "subcategory": "COMPARISON",
            "description": "Starts with prefix",
            "examples": ["begins"],
        },
        "LOG.ENDS.WITH": {
            "category": "LOG",
            "subcategory": "COMPARISON",
            "description": "Ends with suffix",
            "examples": ["terminates"],
        },
        "LOG.IS.NULL": {
            "category": "LOG",
            "subcategory": "COMPARISON",
            "description": "Is null check",
            "examples": ["is none"],
        },
        # SET
        "LOG.UNION": {
            "category": "LOG",
            "subcategory": "SET",
            "description": "Set union",
            "examples": ["combine", "merge"],
        },
        "LOG.INTERSECT": {
            "category": "LOG",
            "subcategory": "SET",
            "description": "Set intersection",
            "examples": ["common", "overlap"],
        },
        "LOG.DIFFERENCE": {
            "category": "LOG",
            "subcategory": "SET",
            "description": "Set difference",
            "examples": ["except", "minus"],
        },
        "LOG.SUBSET": {
            "category": "LOG",
            "subcategory": "SET",
            "description": "Is subset",
            "examples": ["contained in"],
        },
        "LOG.SUPERSET": {
            "category": "LOG",
            "subcategory": "SET",
            "description": "Is superset",
            "examples": ["contains all"],
        },
        "LOG.DISJOINT": {
            "category": "LOG",
            "subcategory": "SET",
            "description": "Sets are disjoint",
            "examples": ["no overlap"],
        },
        "LOG.COMPLEMENT": {
            "category": "LOG",
            "subcategory": "SET",
            "description": "Set complement",
            "examples": ["inverse"],
        },
        "LOG.CARTESIAN": {
            "category": "LOG",
            "subcategory": "SET",
            "description": "Cartesian product",
            "examples": ["cross join"],
        },
        "LOG.POWER.SET": {
            "category": "LOG",
            "subcategory": "SET",
            "description": "Power set",
            "examples": ["all subsets"],
        },
        "LOG.PARTITION": {
            "category": "LOG",
            "subcategory": "SET",
            "description": "Partition set",
            "examples": ["divide", "group"],
        },
        # ===== MATHEMATICS (MATH.*) - 100 concepts =====
        # ARITHMETIC
        "MATH.ADD": {
            "category": "MATH",
            "subcategory": "ARITHMETIC",
            "description": "Addition",
            "examples": ["plus", "sum"],
        },
        "MATH.SUBTRACT": {
            "category": "MATH",
            "subcategory": "ARITHMETIC",
            "description": "Subtraction",
            "examples": ["minus", "difference"],
        },
        "MATH.MULTIPLY": {
            "category": "MATH",
            "subcategory": "ARITHMETIC",
            "description": "Multiplication",
            "examples": ["times", "product"],
        },
        "MATH.DIVIDE": {
            "category": "MATH",
            "subcategory": "ARITHMETIC",
            "description": "Division",
            "examples": ["quotient", "ratio"],
        },
        "MATH.MODULO": {
            "category": "MATH",
            "subcategory": "ARITHMETIC",
            "description": "Modulo operation",
            "examples": ["remainder", "mod"],
        },
        "MATH.POWER": {
            "category": "MATH",
            "subcategory": "ARITHMETIC",
            "description": "Exponentiation",
            "examples": ["exponent", "raise"],
        },
        "MATH.SQRT": {
            "category": "MATH",
            "subcategory": "ARITHMETIC",
            "description": "Square root",
            "examples": ["root"],
        },
        "MATH.ABS": {
            "category": "MATH",
            "subcategory": "ARITHMETIC",
            "description": "Absolute value",
            "examples": ["magnitude"],
        },
        "MATH.NEGATE": {
            "category": "MATH",
            "subcategory": "ARITHMETIC",
            "description": "Negation",
            "examples": ["opposite", "invert"],
        },
        "MATH.INCREMENT": {
            "category": "MATH",
            "subcategory": "ARITHMETIC",
            "description": "Increment by one",
            "examples": ["add 1", "next"],
        },
        "MATH.DECREMENT": {
            "category": "MATH",
            "subcategory": "ARITHMETIC",
            "description": "Decrement by one",
            "examples": ["subtract 1", "prev"],
        },
        "MATH.FLOOR": {
            "category": "MATH",
            "subcategory": "ARITHMETIC",
            "description": "Floor function",
            "examples": ["round down"],
        },
        "MATH.CEIL": {
            "category": "MATH",
            "subcategory": "ARITHMETIC",
            "description": "Ceiling function",
            "examples": ["round up"],
        },
        "MATH.ROUND": {
            "category": "MATH",
            "subcategory": "ARITHMETIC",
            "description": "Round to nearest",
            "examples": ["approximate"],
        },
        "MATH.TRUNCATE": {
            "category": "MATH",
            "subcategory": "ARITHMETIC",
            "description": "Truncate decimal",
            "examples": ["cut", "trim"],
        },
        # AGGREGATE
        "MATH.SUM": {
            "category": "MATH",
            "subcategory": "AGGREGATE",
            "description": "Sum total",
            "examples": ["total", "aggregate"],
        },
        "MATH.AVERAGE": {
            "category": "MATH",
            "subcategory": "AGGREGATE",
            "description": "Average or mean",
            "examples": ["mean", "avg"],
        },
        "MATH.MIN": {
            "category": "MATH",
            "subcategory": "AGGREGATE",
            "description": "Minimum value",
            "examples": ["lowest", "smallest"],
        },
        "MATH.MAX": {
            "category": "MATH",
            "subcategory": "AGGREGATE",
            "description": "Maximum value",
            "examples": ["highest", "largest"],
        },
        "MATH.COUNT": {
            "category": "MATH",
            "subcategory": "AGGREGATE",
            "description": "Count items",
            "examples": ["tally", "number"],
        },
        "MATH.MEDIAN": {
            "category": "MATH",
            "subcategory": "AGGREGATE",
            "description": "Median value",
            "examples": ["middle", "50th"],
        },
        "MATH.MODE": {
            "category": "MATH",
            "subcategory": "AGGREGATE",
            "description": "Mode value",
            "examples": ["most frequent"],
        },
        "MATH.RANGE": {
            "category": "MATH",
            "subcategory": "AGGREGATE",
            "description": "Range of values",
            "examples": ["spread"],
        },
        "MATH.VARIANCE": {
            "category": "MATH",
            "subcategory": "AGGREGATE",
            "description": "Variance",
            "examples": ["var", "spread"],
        },
        "MATH.STDDEV": {
            "category": "MATH",
            "subcategory": "AGGREGATE",
            "description": "Standard deviation",
            "examples": ["sigma", "std"],
        },
        "MATH.PERCENTILE": {
            "category": "MATH",
            "subcategory": "AGGREGATE",
            "description": "Percentile rank",
            "examples": ["quantile"],
        },
        "MATH.HISTOGRAM": {
            "category": "MATH",
            "subcategory": "AGGREGATE",
            "description": "Histogram distribution",
            "examples": ["bins"],
        },
        "MATH.CUMSUM": {
            "category": "MATH",
            "subcategory": "AGGREGATE",
            "description": "Cumulative sum",
            "examples": ["running total"],
        },
        "MATH.MOVING.AVG": {
            "category": "MATH",
            "subcategory": "AGGREGATE",
            "description": "Moving average",
            "examples": ["rolling avg"],
        },
        "MATH.WEIGHTED.AVG": {
            "category": "MATH",
            "subcategory": "AGGREGATE",
            "description": "Weighted average",
            "examples": ["weighted mean"],
        },
        # LINALG
        "MATH.MATRIX.MULTIPLY": {
            "category": "MATH",
            "subcategory": "LINALG",
            "description": "Matrix multiplication",
            "examples": ["matmul"],
        },
        "MATH.MATRIX.TRANSPOSE": {
            "category": "MATH",
            "subcategory": "LINALG",
            "description": "Matrix transpose",
            "examples": ["swap axes"],
        },
        "MATH.MATRIX.INVERSE": {
            "category": "MATH",
            "subcategory": "LINALG",
            "description": "Matrix inverse",
            "examples": ["invert"],
        },
        "MATH.MATRIX.DETERMINANT": {
            "category": "MATH",
            "subcategory": "LINALG",
            "description": "Matrix determinant",
            "examples": ["det"],
        },
        "MATH.DOT.PRODUCT": {
            "category": "MATH",
            "subcategory": "LINALG",
            "description": "Dot product",
            "examples": ["inner product"],
        },
        "MATH.CROSS.PRODUCT": {
            "category": "MATH",
            "subcategory": "LINALG",
            "description": "Cross product",
            "examples": ["outer"],
        },
        "MATH.NORM": {
            "category": "MATH",
            "subcategory": "LINALG",
            "description": "Vector norm",
            "examples": ["magnitude", "length"],
        },
        "MATH.NORMALIZE": {
            "category": "MATH",
            "subcategory": "LINALG",
            "description": "Normalize vector",
            "examples": ["unit vector"],
        },
        "MATH.EIGENVALUE": {
            "category": "MATH",
            "subcategory": "LINALG",
            "description": "Eigenvalue",
            "examples": ["lambda"],
        },
        "MATH.SVD": {
            "category": "MATH",
            "subcategory": "LINALG",
            "description": "Singular value decomp",
            "examples": ["svd"],
        },
        "MATH.PCA": {
            "category": "MATH",
            "subcategory": "LINALG",
            "description": "Principal components",
            "examples": ["pca"],
        },
        "MATH.COSINE.SIMILARITY": {
            "category": "MATH",
            "subcategory": "LINALG",
            "description": "Cosine similarity",
            "examples": ["cos sim"],
        },
        "MATH.EUCLIDEAN.DISTANCE": {
            "category": "MATH",
            "subcategory": "LINALG",
            "description": "Euclidean distance",
            "examples": ["l2"],
        },
        "MATH.MANHATTAN.DISTANCE": {
            "category": "MATH",
            "subcategory": "LINALG",
            "description": "Manhattan distance",
            "examples": ["l1"],
        },
        "MATH.HAMMING.DISTANCE": {
            "category": "MATH",
            "subcategory": "LINALG",
            "description": "Hamming distance",
            "examples": ["bitwise"],
        },
        # STATISTICS
        "MATH.STAT.MEAN": {
            "category": "MATH",
            "subcategory": "STATISTICS",
            "description": "Statistical mean",
            "examples": ["average"],
        },
        "MATH.STAT.STDEV": {
            "category": "MATH",
            "subcategory": "STATISTICS",
            "description": "Std deviation",
            "examples": ["sigma"],
        },
        "MATH.STAT.CORRELATION": {
            "category": "MATH",
            "subcategory": "STATISTICS",
            "description": "Correlation coeff",
            "examples": ["r value"],
        },
        "MATH.STAT.REGRESSION": {
            "category": "MATH",
            "subcategory": "STATISTICS",
            "description": "Regression analysis",
            "examples": ["fit line"],
        },
        "MATH.STAT.TTEST": {
            "category": "MATH",
            "subcategory": "STATISTICS",
            "description": "T-test",
            "examples": ["significance"],
        },
        "MATH.STAT.ANOVA": {
            "category": "MATH",
            "subcategory": "STATISTICS",
            "description": "Analysis of variance",
            "examples": ["anova"],
        },
        "MATH.STAT.CHI.SQUARE": {
            "category": "MATH",
            "subcategory": "STATISTICS",
            "description": "Chi-squared test",
            "examples": ["chi2"],
        },
        "MATH.STAT.PVALUE": {
            "category": "MATH",
            "subcategory": "STATISTICS",
            "description": "P-value",
            "examples": ["significance"],
        },
        "MATH.STAT.CONFIDENCE": {
            "category": "MATH",
            "subcategory": "STATISTICS",
            "description": "Confidence interval",
            "examples": ["ci"],
        },
        "MATH.STAT.SAMPLE": {
            "category": "MATH",
            "subcategory": "STATISTICS",
            "description": "Random sample",
            "examples": ["subset"],
        },
        "MATH.STAT.DISTRIBUTION": {
            "category": "MATH",
            "subcategory": "STATISTICS",
            "description": "Distribution type",
            "examples": ["pdf"],
        },
        "MATH.STAT.NORMAL": {
            "category": "MATH",
            "subcategory": "STATISTICS",
            "description": "Normal distribution",
            "examples": ["gaussian"],
        },
        "MATH.STAT.UNIFORM": {
            "category": "MATH",
            "subcategory": "STATISTICS",
            "description": "Uniform distribution",
            "examples": ["flat"],
        },
        "MATH.STAT.POISSON": {
            "category": "MATH",
            "subcategory": "STATISTICS",
            "description": "Poisson distribution",
            "examples": ["events"],
        },
        "MATH.STAT.BAYES": {
            "category": "MATH",
            "subcategory": "STATISTICS",
            "description": "Bayesian inference",
            "examples": ["posterior"],
        },
        # TRIGONOMETRY
        "MATH.SIN": {
            "category": "MATH",
            "subcategory": "TRIGONOMETRY",
            "description": "Sine function",
            "examples": ["sin"],
        },
        "MATH.COS": {
            "category": "MATH",
            "subcategory": "TRIGONOMETRY",
            "description": "Cosine function",
            "examples": ["cos"],
        },
        "MATH.TAN": {
            "category": "MATH",
            "subcategory": "TRIGONOMETRY",
            "description": "Tangent function",
            "examples": ["tan"],
        },
        "MATH.ASIN": {
            "category": "MATH",
            "subcategory": "TRIGONOMETRY",
            "description": "Arc sine",
            "examples": ["inverse sin"],
        },
        "MATH.ACOS": {
            "category": "MATH",
            "subcategory": "TRIGONOMETRY",
            "description": "Arc cosine",
            "examples": ["inverse cos"],
        },
        "MATH.ATAN": {
            "category": "MATH",
            "subcategory": "TRIGONOMETRY",
            "description": "Arc tangent",
            "examples": ["inverse tan"],
        },
        "MATH.ATAN2": {
            "category": "MATH",
            "subcategory": "TRIGONOMETRY",
            "description": "Two-argument atan",
            "examples": ["angle"],
        },
        "MATH.DEGREES": {
            "category": "MATH",
            "subcategory": "TRIGONOMETRY",
            "description": "Convert to degrees",
            "examples": ["deg"],
        },
        "MATH.RADIANS": {
            "category": "MATH",
            "subcategory": "TRIGONOMETRY",
            "description": "Convert to radians",
            "examples": ["rad"],
        },
        "MATH.HYPOT": {
            "category": "MATH",
            "subcategory": "TRIGONOMETRY",
            "description": "Hypotenuse",
            "examples": ["distance"],
        },
        # FUNCTION
        "MATH.LOG": {
            "category": "MATH",
            "subcategory": "FUNCTION",
            "description": "Logarithm",
            "examples": ["ln", "log"],
        },
        "MATH.LOG10": {
            "category": "MATH",
            "subcategory": "FUNCTION",
            "description": "Base-10 logarithm",
            "examples": ["common log"],
        },
        "MATH.LOG2": {
            "category": "MATH",
            "subcategory": "FUNCTION",
            "description": "Base-2 logarithm",
            "examples": ["binary log"],
        },
        "MATH.EXP": {
            "category": "MATH",
            "subcategory": "FUNCTION",
            "description": "Exponential function",
            "examples": ["e^x"],
        },
        "MATH.FACTORIAL": {
            "category": "MATH",
            "subcategory": "FUNCTION",
            "description": "Factorial",
            "examples": ["n!"],
        },
        "MATH.GCD": {
            "category": "MATH",
            "subcategory": "FUNCTION",
            "description": "Greatest common divisor",
            "examples": ["hcf"],
        },
        "MATH.LCM": {
            "category": "MATH",
            "subcategory": "FUNCTION",
            "description": "Least common multiple",
            "examples": ["lcm"],
        },
        "MATH.RANDOM": {
            "category": "MATH",
            "subcategory": "FUNCTION",
            "description": "Random number",
            "examples": ["rand"],
        },
        "MATH.CLAMP": {
            "category": "MATH",
            "subcategory": "FUNCTION",
            "description": "Clamp to range",
            "examples": ["limit"],
        },
        "MATH.INTERPOLATE": {
            "category": "MATH",
            "subcategory": "FUNCTION",
            "description": "Interpolation",
            "examples": ["lerp"],
        },
        # CONSTANT
        "MATH.PI": {
            "category": "MATH",
            "subcategory": "CONSTANT",
            "description": "Pi constant",
            "examples": ["3.14159"],
        },
        "MATH.E": {
            "category": "MATH",
            "subcategory": "CONSTANT",
            "description": "Euler's number",
            "examples": ["2.71828"],
        },
        "MATH.INF": {
            "category": "MATH",
            "subcategory": "CONSTANT",
            "description": "Infinity",
            "examples": ["unlimited"],
        },
        "MATH.NEG.INF": {
            "category": "MATH",
            "subcategory": "CONSTANT",
            "description": "Negative infinity",
            "examples": ["-inf"],
        },
        "MATH.NAN": {
            "category": "MATH",
            "subcategory": "CONSTANT",
            "description": "Not a number",
            "examples": ["undefined"],
        },
        # SEQUENCE
        "MATH.FIBONACCI": {
            "category": "MATH",
            "subcategory": "SEQUENCE",
            "description": "Fibonacci sequence",
            "examples": ["fib"],
        },
        # NUMBER
        "MATH.PRIME": {
            "category": "MATH",
            "subcategory": "NUMBER",
            "description": "Prime number check",
            "examples": ["primality"],
        },
        # COMBINATORICS
        "MATH.PERMUTATION": {
            "category": "MATH",
            "subcategory": "COMBINATORICS",
            "description": "Permutation count",
            "examples": ["arrange"],
        },
        "MATH.COMBINATION": {
            "category": "MATH",
            "subcategory": "COMBINATORICS",
            "description": "Combination count",
            "examples": ["choose"],
        },
        # FUNCTION
        "MATH.SIGMOID": {
            "category": "MATH",
            "subcategory": "FUNCTION",
            "description": "Sigmoid function",
            "examples": ["logistic"],
        },
        "MATH.RELU": {
            "category": "MATH",
            "subcategory": "FUNCTION",
            "description": "ReLU activation",
            "examples": ["rectifier"],
        },
        "MATH.SOFTMAX": {
            "category": "MATH",
            "subcategory": "FUNCTION",
            "description": "Softmax function",
            "examples": ["normalize"],
        },
        "MATH.TANH": {
            "category": "MATH",
            "subcategory": "FUNCTION",
            "description": "Hyperbolic tangent",
            "examples": ["tanh"],
        },
        # SIGNAL
        "MATH.CONVOLUTION": {
            "category": "MATH",
            "subcategory": "SIGNAL",
            "description": "Convolution operation",
            "examples": ["filter"],
        },
        "MATH.FFT": {
            "category": "MATH",
            "subcategory": "SIGNAL",
            "description": "Fast Fourier transform",
            "examples": ["frequency"],
        },
        # CALCULUS
        "MATH.GRADIENT": {
            "category": "MATH",
            "subcategory": "CALCULUS",
            "description": "Gradient computation",
            "examples": ["derivative"],
        },
        "MATH.INTEGRAL": {
            "category": "MATH",
            "subcategory": "CALCULUS",
            "description": "Integration",
            "examples": ["area"],
        },
        "MATH.DIFF": {
            "category": "MATH",
            "subcategory": "CALCULUS",
            "description": "Differentiation",
            "examples": ["rate of change"],
        },
        "MATH.LIMIT": {
            "category": "MATH",
            "subcategory": "CALCULUS",
            "description": "Limit computation",
            "examples": ["converge"],
        },
        # OPTIMIZATION
        "MATH.OPTIMIZE": {
            "category": "MATH",
            "subcategory": "OPTIMIZATION",
            "description": "Optimization",
            "examples": ["minimize"],
        },
        # ===== TEMPORAL (TIME.*) - 50 concepts =====
        # RELATIVE
        "TIME.BEFORE": {
            "category": "TIME",
            "subcategory": "RELATIVE",
            "description": "Before in time",
            "examples": ["prior", "earlier"],
        },
        "TIME.AFTER": {
            "category": "TIME",
            "subcategory": "RELATIVE",
            "description": "After in time",
            "examples": ["later", "subsequent"],
        },
        "TIME.DURING": {
            "category": "TIME",
            "subcategory": "RELATIVE",
            "description": "During period",
            "examples": ["while", "throughout"],
        },
        "TIME.PAST": {
            "category": "TIME",
            "subcategory": "RELATIVE",
            "description": "Past time",
            "examples": ["previous", "historical"],
        },
        "TIME.FUTURE": {
            "category": "TIME",
            "subcategory": "RELATIVE",
            "description": "Future time",
            "examples": ["upcoming", "next"],
        },
        "TIME.SINCE": {
            "category": "TIME",
            "subcategory": "RELATIVE",
            "description": "Since time point",
            "examples": ["from", "starting"],
        },
        "TIME.UNTIL": {
            "category": "TIME",
            "subcategory": "RELATIVE",
            "description": "Until time point",
            "examples": ["to", "ending"],
        },
        "TIME.AGO": {
            "category": "TIME",
            "subcategory": "RELATIVE",
            "description": "Time ago",
            "examples": ["back", "prior"],
        },
        "TIME.FROM.NOW": {
            "category": "TIME",
            "subcategory": "RELATIVE",
            "description": "Time from now",
            "examples": ["ahead"],
        },
        "TIME.RECENTLY": {
            "category": "TIME",
            "subcategory": "RELATIVE",
            "description": "Recently occurred",
            "examples": ["just", "lately"],
        },
        "TIME.SOON": {
            "category": "TIME",
            "subcategory": "RELATIVE",
            "description": "Coming soon",
            "examples": ["shortly", "imminent"],
        },
        "TIME.EARLIEST": {
            "category": "TIME",
            "subcategory": "RELATIVE",
            "description": "Earliest possible",
            "examples": ["first", "minimum"],
        },
        "TIME.LATEST": {
            "category": "TIME",
            "subcategory": "RELATIVE",
            "description": "Latest possible",
            "examples": ["last", "deadline"],
        },
        "TIME.NEXT": {
            "category": "TIME",
            "subcategory": "RELATIVE",
            "description": "Next occurrence",
            "examples": ["following"],
        },
        "TIME.PREVIOUS": {
            "category": "TIME",
            "subcategory": "RELATIVE",
            "description": "Previous occurrence",
            "examples": ["preceding"],
        },
        # ABSOLUTE
        "TIME.NOW": {
            "category": "TIME",
            "subcategory": "ABSOLUTE",
            "description": "Current time",
            "examples": ["current", "present"],
        },
        "TIME.TODAY": {
            "category": "TIME",
            "subcategory": "ABSOLUTE",
            "description": "Today's date",
            "examples": ["current day"],
        },
        "TIME.YESTERDAY": {
            "category": "TIME",
            "subcategory": "ABSOLUTE",
            "description": "Yesterday",
            "examples": ["previous day"],
        },
        "TIME.TOMORROW": {
            "category": "TIME",
            "subcategory": "ABSOLUTE",
            "description": "Tomorrow",
            "examples": ["next day"],
        },
        "TIME.EPOCH": {
            "category": "TIME",
            "subcategory": "ABSOLUTE",
            "description": "Unix epoch",
            "examples": ["1970-01-01"],
        },
        "TIME.START": {
            "category": "TIME",
            "subcategory": "ABSOLUTE",
            "description": "Start time",
            "examples": ["begin", "onset"],
        },
        "TIME.END": {
            "category": "TIME",
            "subcategory": "ABSOLUTE",
            "description": "End time",
            "examples": ["finish", "conclusion"],
        },
        "TIME.CREATED": {
            "category": "TIME",
            "subcategory": "ABSOLUTE",
            "description": "Creation time",
            "examples": ["born", "made"],
        },
        "TIME.MODIFIED": {
            "category": "TIME",
            "subcategory": "ABSOLUTE",
            "description": "Modification time",
            "examples": ["updated", "changed"],
        },
        "TIME.EXPIRED": {
            "category": "TIME",
            "subcategory": "ABSOLUTE",
            "description": "Expiration time",
            "examples": ["invalid after"],
        },
        # DURATION
        "TIME.DURATION": {
            "category": "TIME",
            "subcategory": "DURATION",
            "description": "Time duration",
            "examples": ["span", "length"],
        },
        "TIME.MILLISECOND": {
            "category": "TIME",
            "subcategory": "DURATION",
            "description": "Milliseconds",
            "examples": ["ms"],
        },
        "TIME.SECOND": {
            "category": "TIME",
            "subcategory": "DURATION",
            "description": "Seconds",
            "examples": ["sec", "s"],
        },
        "TIME.MINUTE": {
            "category": "TIME",
            "subcategory": "DURATION",
            "description": "Minutes",
            "examples": ["min", "m"],
        },
        "TIME.HOUR": {
            "category": "TIME",
            "subcategory": "DURATION",
            "description": "Hours",
            "examples": ["hr", "h"],
        },
        "TIME.DAY": {
            "category": "TIME",
            "subcategory": "DURATION",
            "description": "Days",
            "examples": ["d"],
        },
        "TIME.WEEK": {
            "category": "TIME",
            "subcategory": "DURATION",
            "description": "Weeks",
            "examples": ["wk"],
        },
        "TIME.MONTH": {
            "category": "TIME",
            "subcategory": "DURATION",
            "description": "Months",
            "examples": ["mo"],
        },
        "TIME.YEAR": {
            "category": "TIME",
            "subcategory": "DURATION",
            "description": "Years",
            "examples": ["yr"],
        },
        "TIME.INSTANT": {
            "category": "TIME",
            "subcategory": "DURATION",
            "description": "Instantaneous",
            "examples": ["immediate"],
        },
        "TIME.SHORT": {
            "category": "TIME",
            "subcategory": "DURATION",
            "description": "Short duration",
            "examples": ["brief"],
        },
        "TIME.LONG": {
            "category": "TIME",
            "subcategory": "DURATION",
            "description": "Long duration",
            "examples": ["extended"],
        },
        "TIME.INFINITE": {
            "category": "TIME",
            "subcategory": "DURATION",
            "description": "Infinite duration",
            "examples": ["forever"],
        },
        "TIME.TTL": {
            "category": "TIME",
            "subcategory": "DURATION",
            "description": "Time to live",
            "examples": ["expiry", "lifetime"],
        },
        "TIME.TIMEOUT": {
            "category": "TIME",
            "subcategory": "DURATION",
            "description": "Timeout period",
            "examples": ["deadline"],
        },
        # SCHEDULING
        "TIME.SCHEDULE.ONCE": {
            "category": "TIME",
            "subcategory": "SCHEDULING",
            "description": "Run once",
            "examples": ["one-time"],
        },
        "TIME.SCHEDULE.RECURRING": {
            "category": "TIME",
            "subcategory": "SCHEDULING",
            "description": "Recurring schedule",
            "examples": ["repeated"],
        },
        "TIME.SCHEDULE.CRON": {
            "category": "TIME",
            "subcategory": "SCHEDULING",
            "description": "Cron expression",
            "examples": ["periodic"],
        },
        "TIME.SCHEDULE.INTERVAL": {
            "category": "TIME",
            "subcategory": "SCHEDULING",
            "description": "Fixed interval",
            "examples": ["every N"],
        },
        "TIME.SCHEDULE.DELAY": {
            "category": "TIME",
            "subcategory": "SCHEDULING",
            "description": "Delayed execution",
            "examples": ["deferred"],
        },
        "TIME.SCHEDULE.IMMEDIATE": {
            "category": "TIME",
            "subcategory": "SCHEDULING",
            "description": "Immediate execution",
            "examples": ["now"],
        },
        "TIME.SCHEDULE.PEAK": {
            "category": "TIME",
            "subcategory": "SCHEDULING",
            "description": "Peak hours",
            "examples": ["busy time"],
        },
        "TIME.SCHEDULE.OFFPEAK": {
            "category": "TIME",
            "subcategory": "SCHEDULING",
            "description": "Off-peak hours",
            "examples": ["quiet time"],
        },
        "TIME.SCHEDULE.WINDOW": {
            "category": "TIME",
            "subcategory": "SCHEDULING",
            "description": "Time window",
            "examples": ["slot", "period"],
        },
        "TIME.SCHEDULE.DEADLINE": {
            "category": "TIME",
            "subcategory": "SCHEDULING",
            "description": "Deadline time",
            "examples": ["due by"],
        },
        # ===== SPATIAL (SPACE.*) - 50 concepts =====
        # CONTAINMENT
        "SPACE.INSIDE": {
            "category": "SPACE",
            "subcategory": "CONTAINMENT",
            "description": "Inside or within",
            "examples": ["internal"],
        },
        "SPACE.OUTSIDE": {
            "category": "SPACE",
            "subcategory": "CONTAINMENT",
            "description": "Outside or external",
            "examples": ["external"],
        },
        "SPACE.BOUNDARY": {
            "category": "SPACE",
            "subcategory": "CONTAINMENT",
            "description": "At boundary",
            "examples": ["edge", "border"],
        },
        "SPACE.CENTER": {
            "category": "SPACE",
            "subcategory": "CONTAINMENT",
            "description": "At center",
            "examples": ["middle", "core"],
        },
        "SPACE.SURFACE": {
            "category": "SPACE",
            "subcategory": "CONTAINMENT",
            "description": "On surface",
            "examples": ["outer", "face"],
        },
        "SPACE.INTERIOR": {
            "category": "SPACE",
            "subcategory": "CONTAINMENT",
            "description": "In interior",
            "examples": ["inner", "deep"],
        },
        "SPACE.ENCLOSED": {
            "category": "SPACE",
            "subcategory": "CONTAINMENT",
            "description": "Enclosed space",
            "examples": ["contained"],
        },
        "SPACE.OPEN": {
            "category": "SPACE",
            "subcategory": "CONTAINMENT",
            "description": "Open space",
            "examples": ["exposed"],
        },
        "SPACE.NESTED": {
            "category": "SPACE",
            "subcategory": "CONTAINMENT",
            "description": "Nested level",
            "examples": ["inner", "recursive"],
        },
        "SPACE.FLAT": {
            "category": "SPACE",
            "subcategory": "CONTAINMENT",
            "description": "Flat structure",
            "examples": ["single level"],
        },
        # PROXIMITY
        "SPACE.NEAR": {
            "category": "SPACE",
            "subcategory": "PROXIMITY",
            "description": "Near or close",
            "examples": ["adjacent"],
        },
        "SPACE.FAR": {
            "category": "SPACE",
            "subcategory": "PROXIMITY",
            "description": "Far or distant",
            "examples": ["remote"],
        },
        "SPACE.LOCAL": {
            "category": "SPACE",
            "subcategory": "PROXIMITY",
            "description": "Local scope",
            "examples": ["same node"],
        },
        "SPACE.REMOTE": {
            "category": "SPACE",
            "subcategory": "PROXIMITY",
            "description": "Remote location",
            "examples": ["different node"],
        },
        "SPACE.ADJACENT": {
            "category": "SPACE",
            "subcategory": "PROXIMITY",
            "description": "Directly adjacent",
            "examples": ["next to"],
        },
        "SPACE.DISTRIBUTED": {
            "category": "SPACE",
            "subcategory": "PROXIMITY",
            "description": "Distributed across",
            "examples": ["spread"],
        },
        "SPACE.CENTRALIZED": {
            "category": "SPACE",
            "subcategory": "PROXIMITY",
            "description": "Centralized in one",
            "examples": ["single point"],
        },
        "SPACE.CLUSTERED": {
            "category": "SPACE",
            "subcategory": "PROXIMITY",
            "description": "Clustered together",
            "examples": ["grouped"],
        },
        "SPACE.SCATTERED": {
            "category": "SPACE",
            "subcategory": "PROXIMITY",
            "description": "Scattered widely",
            "examples": ["dispersed"],
        },
        "SPACE.COLOCATED": {
            "category": "SPACE",
            "subcategory": "PROXIMITY",
            "description": "Co-located",
            "examples": ["same place"],
        },
        # DIRECTION
        "SPACE.ABOVE": {
            "category": "SPACE",
            "subcategory": "DIRECTION",
            "description": "Above or over",
            "examples": ["top"],
        },
        "SPACE.BELOW": {
            "category": "SPACE",
            "subcategory": "DIRECTION",
            "description": "Below or under",
            "examples": ["bottom"],
        },
        "SPACE.LEFT": {
            "category": "SPACE",
            "subcategory": "DIRECTION",
            "description": "To the left",
            "examples": ["port"],
        },
        "SPACE.RIGHT": {
            "category": "SPACE",
            "subcategory": "DIRECTION",
            "description": "To the right",
            "examples": ["starboard"],
        },
        "SPACE.FORWARD": {
            "category": "SPACE",
            "subcategory": "DIRECTION",
            "description": "Forward direction",
            "examples": ["ahead"],
        },
        "SPACE.BACKWARD": {
            "category": "SPACE",
            "subcategory": "DIRECTION",
            "description": "Backward direction",
            "examples": ["behind"],
        },
        "SPACE.INBOUND": {
            "category": "SPACE",
            "subcategory": "DIRECTION",
            "description": "Inbound traffic",
            "examples": ["incoming"],
        },
        "SPACE.OUTBOUND": {
            "category": "SPACE",
            "subcategory": "DIRECTION",
            "description": "Outbound traffic",
            "examples": ["outgoing"],
        },
        "SPACE.UPSTREAM": {
            "category": "SPACE",
            "subcategory": "DIRECTION",
            "description": "Upstream in flow",
            "examples": ["source-ward"],
        },
        "SPACE.DOWNSTREAM": {
            "category": "SPACE",
            "subcategory": "DIRECTION",
            "description": "Downstream in flow",
            "examples": ["sink-ward"],
        },
        # TOPOLOGY
        "SPACE.TOPO.POINT": {
            "category": "SPACE",
            "subcategory": "TOPOLOGY",
            "description": "Single point",
            "examples": ["node", "vertex"],
        },
        "SPACE.TOPO.EDGE": {
            "category": "SPACE",
            "subcategory": "TOPOLOGY",
            "description": "Edge or link",
            "examples": ["connection"],
        },
        "SPACE.TOPO.PATH": {
            "category": "SPACE",
            "subcategory": "TOPOLOGY",
            "description": "Path through graph",
            "examples": ["route"],
        },
        "SPACE.TOPO.CYCLE": {
            "category": "SPACE",
            "subcategory": "TOPOLOGY",
            "description": "Cycle in graph",
            "examples": ["loop"],
        },
        "SPACE.TOPO.TREE": {
            "category": "SPACE",
            "subcategory": "TOPOLOGY",
            "description": "Tree structure",
            "examples": ["hierarchy"],
        },
        "SPACE.TOPO.MESH": {
            "category": "SPACE",
            "subcategory": "TOPOLOGY",
            "description": "Mesh topology",
            "examples": ["fully connected"],
        },
        "SPACE.TOPO.STAR": {
            "category": "SPACE",
            "subcategory": "TOPOLOGY",
            "description": "Star topology",
            "examples": ["hub and spoke"],
        },
        "SPACE.TOPO.RING": {
            "category": "SPACE",
            "subcategory": "TOPOLOGY",
            "description": "Ring topology",
            "examples": ["circular"],
        },
        "SPACE.TOPO.BUS": {
            "category": "SPACE",
            "subcategory": "TOPOLOGY",
            "description": "Bus topology",
            "examples": ["linear"],
        },
        "SPACE.TOPO.GRAPH": {
            "category": "SPACE",
            "subcategory": "TOPOLOGY",
            "description": "Graph structure",
            "examples": ["network"],
        },
        # REGION
        "SPACE.REGION.ZONE": {
            "category": "SPACE",
            "subcategory": "REGION",
            "description": "Availability zone",
            "examples": ["az"],
        },
        "SPACE.REGION.DATACENTER": {
            "category": "SPACE",
            "subcategory": "REGION",
            "description": "Data center",
            "examples": ["dc", "colo"],
        },
        "SPACE.REGION.RACK": {
            "category": "SPACE",
            "subcategory": "REGION",
            "description": "Server rack",
            "examples": ["cabinet"],
        },
        "SPACE.REGION.NODE": {
            "category": "SPACE",
            "subcategory": "REGION",
            "description": "Single node",
            "examples": ["host", "server"],
        },
        "SPACE.REGION.POD": {
            "category": "SPACE",
            "subcategory": "REGION",
            "description": "Pod or group",
            "examples": ["cell"],
        },
        "SPACE.REGION.PARTITION": {
            "category": "SPACE",
            "subcategory": "REGION",
            "description": "Partition or shard",
            "examples": ["segment"],
        },
        "SPACE.REGION.REPLICA": {
            "category": "SPACE",
            "subcategory": "REGION",
            "description": "Replica location",
            "examples": ["copy"],
        },
        "SPACE.REGION.PRIMARY": {
            "category": "SPACE",
            "subcategory": "REGION",
            "description": "Primary location",
            "examples": ["master"],
        },
        "SPACE.REGION.SECONDARY": {
            "category": "SPACE",
            "subcategory": "REGION",
            "description": "Secondary location",
            "examples": ["slave"],
        },
        "SPACE.REGION.EDGE": {
            "category": "SPACE",
            "subcategory": "REGION",
            "description": "Edge location",
            "examples": ["cdn", "pop"],
        },
        # ===== DATA TYPES (DATA.*) - 100 concepts =====
        # STRUCTURE
        "DATA.LIST": {
            "category": "DATA",
            "subcategory": "STRUCTURE",
            "description": "List or array",
            "examples": ["array", "sequence"],
        },
        "DATA.DICT": {
            "category": "DATA",
            "subcategory": "STRUCTURE",
            "description": "Dictionary or map",
            "examples": ["map", "object"],
        },
        "DATA.SET": {
            "category": "DATA",
            "subcategory": "STRUCTURE",
            "description": "Set collection",
            "examples": ["unique"],
        },
        "DATA.TUPLE": {
            "category": "DATA",
            "subcategory": "STRUCTURE",
            "description": "Tuple or pair",
            "examples": ["fixed sequence"],
        },
        "DATA.STRING": {
            "category": "DATA",
            "subcategory": "STRUCTURE",
            "description": "String type",
            "examples": ["text", "char"],
        },
        "DATA.INTEGER": {
            "category": "DATA",
            "subcategory": "STRUCTURE",
            "description": "Integer type",
            "examples": ["int", "whole"],
        },
        "DATA.FLOAT": {
            "category": "DATA",
            "subcategory": "STRUCTURE",
            "description": "Float type",
            "examples": ["decimal", "real"],
        },
        "DATA.QUEUE": {
            "category": "DATA",
            "subcategory": "STRUCTURE",
            "description": "FIFO queue",
            "examples": ["fifo"],
        },
        "DATA.STACK": {
            "category": "DATA",
            "subcategory": "STRUCTURE",
            "description": "LIFO stack",
            "examples": ["lifo"],
        },
        "DATA.DEQUE": {
            "category": "DATA",
            "subcategory": "STRUCTURE",
            "description": "Double-ended queue",
            "examples": ["deque"],
        },
        "DATA.HEAP": {
            "category": "DATA",
            "subcategory": "STRUCTURE",
            "description": "Heap or priority queue",
            "examples": ["priority queue"],
        },
        "DATA.TREE": {
            "category": "DATA",
            "subcategory": "STRUCTURE",
            "description": "Tree structure",
            "examples": ["hierarchical"],
        },
        "DATA.GRAPH": {
            "category": "DATA",
            "subcategory": "STRUCTURE",
            "description": "Graph structure",
            "examples": ["network"],
        },
        "DATA.LINKED.LIST": {
            "category": "DATA",
            "subcategory": "STRUCTURE",
            "description": "Linked list",
            "examples": ["chain"],
        },
        "DATA.HASH.TABLE": {
            "category": "DATA",
            "subcategory": "STRUCTURE",
            "description": "Hash table",
            "examples": ["hashtable", "map"],
        },
        "DATA.BTREE": {
            "category": "DATA",
            "subcategory": "STRUCTURE",
            "description": "B-tree index",
            "examples": ["balanced tree"],
        },
        "DATA.TRIE": {
            "category": "DATA",
            "subcategory": "STRUCTURE",
            "description": "Trie or prefix tree",
            "examples": ["autocomplete"],
        },
        "DATA.BLOOM.FILTER": {
            "category": "DATA",
            "subcategory": "STRUCTURE",
            "description": "Bloom filter",
            "examples": ["probabilistic set"],
        },
        "DATA.RING.BUFFER": {
            "category": "DATA",
            "subcategory": "STRUCTURE",
            "description": "Ring buffer",
            "examples": ["circular buffer"],
        },
        "DATA.SPARSE.ARRAY": {
            "category": "DATA",
            "subcategory": "STRUCTURE",
            "description": "Sparse array",
            "examples": ["compressed"],
        },
        # PRIMITIVE
        "DATA.BOOLEAN": {
            "category": "DATA",
            "subcategory": "PRIMITIVE",
            "description": "Boolean type",
            "examples": ["bool", "flag"],
        },
        "DATA.BYTE": {
            "category": "DATA",
            "subcategory": "PRIMITIVE",
            "description": "Byte value",
            "examples": ["uint8", "octet"],
        },
        "DATA.INT8": {
            "category": "DATA",
            "subcategory": "PRIMITIVE",
            "description": "8-bit integer",
            "examples": ["sbyte"],
        },
        "DATA.INT16": {
            "category": "DATA",
            "subcategory": "PRIMITIVE",
            "description": "16-bit integer",
            "examples": ["short"],
        },
        "DATA.INT32": {
            "category": "DATA",
            "subcategory": "PRIMITIVE",
            "description": "32-bit integer",
            "examples": ["int"],
        },
        "DATA.INT64": {
            "category": "DATA",
            "subcategory": "PRIMITIVE",
            "description": "64-bit integer",
            "examples": ["long"],
        },
        "DATA.UINT32": {
            "category": "DATA",
            "subcategory": "PRIMITIVE",
            "description": "Unsigned 32-bit",
            "examples": ["uint"],
        },
        "DATA.UINT64": {
            "category": "DATA",
            "subcategory": "PRIMITIVE",
            "description": "Unsigned 64-bit",
            "examples": ["ulong"],
        },
        "DATA.FLOAT32": {
            "category": "DATA",
            "subcategory": "PRIMITIVE",
            "description": "32-bit float",
            "examples": ["single"],
        },
        "DATA.FLOAT64": {
            "category": "DATA",
            "subcategory": "PRIMITIVE",
            "description": "64-bit float",
            "examples": ["double"],
        },
        "DATA.DECIMAL": {
            "category": "DATA",
            "subcategory": "PRIMITIVE",
            "description": "Decimal precision",
            "examples": ["exact"],
        },
        "DATA.CHAR": {
            "category": "DATA",
            "subcategory": "PRIMITIVE",
            "description": "Single character",
            "examples": ["rune"],
        },
        "DATA.NULL": {
            "category": "DATA",
            "subcategory": "PRIMITIVE",
            "description": "Null value",
            "examples": ["none", "nil"],
        },
        "DATA.VOID": {
            "category": "DATA",
            "subcategory": "PRIMITIVE",
            "description": "Void type",
            "examples": ["nothing"],
        },
        "DATA.ENUM": {
            "category": "DATA",
            "subcategory": "PRIMITIVE",
            "description": "Enumeration type",
            "examples": ["choices"],
        },
        # COMPLEX
        "DATA.TIMESTAMP": {
            "category": "DATA",
            "subcategory": "COMPLEX",
            "description": "Timestamp value",
            "examples": ["datetime"],
        },
        "DATA.DATE": {
            "category": "DATA",
            "subcategory": "COMPLEX",
            "description": "Date value",
            "examples": ["calendar date"],
        },
        "DATA.TIME": {
            "category": "DATA",
            "subcategory": "COMPLEX",
            "description": "Time value",
            "examples": ["clock time"],
        },
        "DATA.DURATION": {
            "category": "DATA",
            "subcategory": "COMPLEX",
            "description": "Duration value",
            "examples": ["interval"],
        },
        "DATA.UUID": {
            "category": "DATA",
            "subcategory": "COMPLEX",
            "description": "UUID identifier",
            "examples": ["guid", "unique id"],
        },
        "DATA.URI": {
            "category": "DATA",
            "subcategory": "COMPLEX",
            "description": "URI or URL",
            "examples": ["link", "address"],
        },
        "DATA.EMAIL": {
            "category": "DATA",
            "subcategory": "COMPLEX",
            "description": "Email address",
            "examples": ["mail"],
        },
        "DATA.IP.ADDRESS": {
            "category": "DATA",
            "subcategory": "COMPLEX",
            "description": "IP address",
            "examples": ["ipv4", "ipv6"],
        },
        "DATA.MAC.ADDRESS": {
            "category": "DATA",
            "subcategory": "COMPLEX",
            "description": "MAC address",
            "examples": ["hardware addr"],
        },
        "DATA.REGEX": {
            "category": "DATA",
            "subcategory": "COMPLEX",
            "description": "Regular expression",
            "examples": ["pattern"],
        },
        "DATA.SEMVER": {
            "category": "DATA",
            "subcategory": "COMPLEX",
            "description": "Semantic version",
            "examples": ["version"],
        },
        "DATA.CURRENCY": {
            "category": "DATA",
            "subcategory": "COMPLEX",
            "description": "Currency value",
            "examples": ["money"],
        },
        "DATA.GEO.POINT": {
            "category": "DATA",
            "subcategory": "COMPLEX",
            "description": "Geographic point",
            "examples": ["lat/long"],
        },
        "DATA.RANGE": {
            "category": "DATA",
            "subcategory": "COMPLEX",
            "description": "Range of values",
            "examples": ["interval"],
        },
        "DATA.OPTIONAL": {
            "category": "DATA",
            "subcategory": "COMPLEX",
            "description": "Optional value",
            "examples": ["maybe", "nullable"],
        },
        # SERIALIZATION
        "DATA.JSON.OBJECT": {
            "category": "DATA",
            "subcategory": "SERIALIZATION",
            "description": "JSON object",
            "examples": ["dict"],
        },
        "DATA.JSON.ARRAY": {
            "category": "DATA",
            "subcategory": "SERIALIZATION",
            "description": "JSON array",
            "examples": ["list"],
        },
        "DATA.JSON.PATCH": {
            "category": "DATA",
            "subcategory": "SERIALIZATION",
            "description": "JSON Patch",
            "examples": ["rfc6902"],
        },
        "DATA.JSON.POINTER": {
            "category": "DATA",
            "subcategory": "SERIALIZATION",
            "description": "JSON Pointer",
            "examples": ["path"],
        },
        "DATA.JSON.SCHEMA": {
            "category": "DATA",
            "subcategory": "SERIALIZATION",
            "description": "JSON Schema",
            "examples": ["validation"],
        },
        "DATA.PROTOBUF.MSG": {
            "category": "DATA",
            "subcategory": "SERIALIZATION",
            "description": "Protobuf message",
            "examples": ["proto"],
        },
        "DATA.AVRO.RECORD": {
            "category": "DATA",
            "subcategory": "SERIALIZATION",
            "description": "Avro record",
            "examples": ["schema"],
        },
        "DATA.MSGPACK.OBJ": {
            "category": "DATA",
            "subcategory": "SERIALIZATION",
            "description": "MessagePack object",
            "examples": ["binary"],
        },
        "DATA.CBOR.OBJ": {
            "category": "DATA",
            "subcategory": "SERIALIZATION",
            "description": "CBOR object",
            "examples": ["binary"],
        },
        "DATA.XML.ELEMENT": {
            "category": "DATA",
            "subcategory": "SERIALIZATION",
            "description": "XML element",
            "examples": ["node"],
        },
        # COLLECTION
        "DATA.BATCH": {
            "category": "DATA",
            "subcategory": "COLLECTION",
            "description": "Batch of items",
            "examples": ["group"],
        },
        "DATA.PAGE": {
            "category": "DATA",
            "subcategory": "COLLECTION",
            "description": "Page of results",
            "examples": ["slice"],
        },
        "DATA.CHUNK": {
            "category": "DATA",
            "subcategory": "COLLECTION",
            "description": "Data chunk",
            "examples": ["segment"],
        },
        "DATA.PARTITION": {
            "category": "DATA",
            "subcategory": "COLLECTION",
            "description": "Data partition",
            "examples": ["shard"],
        },
        "DATA.WINDOW": {
            "category": "DATA",
            "subcategory": "COLLECTION",
            "description": "Sliding window",
            "examples": ["frame"],
        },
        "DATA.STREAM": {
            "category": "DATA",
            "subcategory": "COLLECTION",
            "description": "Data stream",
            "examples": ["flow"],
        },
        "DATA.CURSOR": {
            "category": "DATA",
            "subcategory": "COLLECTION",
            "description": "Database cursor",
            "examples": ["iterator"],
        },
        "DATA.ITERATOR": {
            "category": "DATA",
            "subcategory": "COLLECTION",
            "description": "Iterator object",
            "examples": ["generator"],
        },
        "DATA.BUFFER": {
            "category": "DATA",
            "subcategory": "COLLECTION",
            "description": "Data buffer",
            "examples": ["pool"],
        },
        "DATA.PIPELINE": {
            "category": "DATA",
            "subcategory": "COLLECTION",
            "description": "Data pipeline",
            "examples": ["chain"],
        },
        # SCHEMA
        "DATA.SCHEMA.TABLE": {
            "category": "DATA",
            "subcategory": "SCHEMA",
            "description": "Table schema",
            "examples": ["relation"],
        },
        "DATA.SCHEMA.COLUMN": {
            "category": "DATA",
            "subcategory": "SCHEMA",
            "description": "Column definition",
            "examples": ["field"],
        },
        "DATA.SCHEMA.INDEX": {
            "category": "DATA",
            "subcategory": "SCHEMA",
            "description": "Index definition",
            "examples": ["key"],
        },
        "DATA.SCHEMA.CONSTRAINT": {
            "category": "DATA",
            "subcategory": "SCHEMA",
            "description": "Constraint rule",
            "examples": ["check"],
        },
        "DATA.SCHEMA.FOREIGN.KEY": {
            "category": "DATA",
            "subcategory": "SCHEMA",
            "description": "Foreign key",
            "examples": ["reference"],
        },
        "DATA.SCHEMA.PRIMARY.KEY": {
            "category": "DATA",
            "subcategory": "SCHEMA",
            "description": "Primary key",
            "examples": ["id"],
        },
        "DATA.SCHEMA.VIEW": {
            "category": "DATA",
            "subcategory": "SCHEMA",
            "description": "View definition",
            "examples": ["projection"],
        },
        "DATA.SCHEMA.MIGRATION": {
            "category": "DATA",
            "subcategory": "SCHEMA",
            "description": "Schema migration",
            "examples": ["evolution"],
        },
        "DATA.SCHEMA.TRIGGER": {
            "category": "DATA",
            "subcategory": "SCHEMA",
            "description": "Database trigger",
            "examples": ["hook"],
        },
        "DATA.SCHEMA.PROCEDURE": {
            "category": "DATA",
            "subcategory": "SCHEMA",
            "description": "Stored procedure",
            "examples": ["function"],
        },
        # ENCODING
        "DATA.ENCODING.UTF8": {
            "category": "DATA",
            "subcategory": "ENCODING",
            "description": "UTF-8 encoded",
            "examples": ["unicode"],
        },
        "DATA.ENCODING.ASCII": {
            "category": "DATA",
            "subcategory": "ENCODING",
            "description": "ASCII encoded",
            "examples": ["7-bit"],
        },
        "DATA.ENCODING.BASE64": {
            "category": "DATA",
            "subcategory": "ENCODING",
            "description": "Base64 encoded",
            "examples": ["b64"],
        },
        "DATA.ENCODING.HEX": {
            "category": "DATA",
            "subcategory": "ENCODING",
            "description": "Hex encoded",
            "examples": ["base16"],
        },
        "DATA.ENCODING.URL": {
            "category": "DATA",
            "subcategory": "ENCODING",
            "description": "URL encoded",
            "examples": ["percent"],
        },
        "DATA.ENCODING.HTML": {
            "category": "DATA",
            "subcategory": "ENCODING",
            "description": "HTML entities",
            "examples": ["escaped"],
        },
        "DATA.ENCODING.BINARY": {
            "category": "DATA",
            "subcategory": "ENCODING",
            "description": "Raw binary",
            "examples": ["bytes"],
        },
        "DATA.ENCODING.COMPRESSED": {
            "category": "DATA",
            "subcategory": "ENCODING",
            "description": "Compressed data",
            "examples": ["zipped"],
        },
        "DATA.ENCODING.ENCRYPTED": {
            "category": "DATA",
            "subcategory": "ENCODING",
            "description": "Encrypted data",
            "examples": ["ciphered"],
        },
        "DATA.ENCODING.SIGNED": {
            "category": "DATA",
            "subcategory": "ENCODING",
            "description": "Signed data",
            "examples": ["verified"],
        },
        # ACCESS
        "DATA.ACCESS.READ": {
            "category": "DATA",
            "subcategory": "ACCESS",
            "description": "Read access",
            "examples": ["get", "fetch"],
        },
        "DATA.ACCESS.WRITE": {
            "category": "DATA",
            "subcategory": "ACCESS",
            "description": "Write access",
            "examples": ["put", "set"],
        },
        "DATA.ACCESS.APPEND": {
            "category": "DATA",
            "subcategory": "ACCESS",
            "description": "Append access",
            "examples": ["add", "push"],
        },
        "DATA.ACCESS.DELETE": {
            "category": "DATA",
            "subcategory": "ACCESS",
            "description": "Delete access",
            "examples": ["remove"],
        },
        "DATA.ACCESS.EXECUTE": {
            "category": "DATA",
            "subcategory": "ACCESS",
            "description": "Execute access",
            "examples": ["run"],
        },
        "DATA.ACCESS.ADMIN": {
            "category": "DATA",
            "subcategory": "ACCESS",
            "description": "Admin access",
            "examples": ["full"],
        },
        "DATA.ACCESS.OWNER": {
            "category": "DATA",
            "subcategory": "ACCESS",
            "description": "Owner access",
            "examples": ["creator"],
        },
        "DATA.ACCESS.SHARED": {
            "category": "DATA",
            "subcategory": "ACCESS",
            "description": "Shared access",
            "examples": ["collaborative"],
        },
        "DATA.ACCESS.READONLY": {
            "category": "DATA",
            "subcategory": "ACCESS",
            "description": "Read-only access",
            "examples": ["immutable"],
        },
        "DATA.ACCESS.WRITEONLY": {
            "category": "DATA",
            "subcategory": "ACCESS",
            "description": "Write-only access",
            "examples": ["sink"],
        },
        # ===== META OPERATIONS (META.*) - 100 concepts =====
        # STATUS
        "META.STATUS.SUCCESS": {
            "category": "META",
            "subcategory": "STATUS",
            "description": "Operation successful",
            "examples": ["ok", "done"],
        },
        "META.STATUS.FAILURE": {
            "category": "META",
            "subcategory": "STATUS",
            "description": "Operation failed",
            "examples": ["error", "failed"],
        },
        "META.STATUS.PENDING": {
            "category": "META",
            "subcategory": "STATUS",
            "description": "Operation pending",
            "examples": ["waiting"],
        },
        "META.STATUS.RUNNING": {
            "category": "META",
            "subcategory": "STATUS",
            "description": "Operation running",
            "examples": ["in progress"],
        },
        "META.STATUS.CANCELLED": {
            "category": "META",
            "subcategory": "STATUS",
            "description": "Operation cancelled",
            "examples": ["aborted"],
        },
        "META.STATUS.TIMEOUT": {
            "category": "META",
            "subcategory": "STATUS",
            "description": "Operation timed out",
            "examples": ["expired"],
        },
        "META.STATUS.PARTIAL": {
            "category": "META",
            "subcategory": "STATUS",
            "description": "Partial completion",
            "examples": ["incomplete"],
        },
        "META.STATUS.SKIPPED": {
            "category": "META",
            "subcategory": "STATUS",
            "description": "Operation skipped",
            "examples": ["bypassed"],
        },
        "META.STATUS.QUEUED": {
            "category": "META",
            "subcategory": "STATUS",
            "description": "Queued for execution",
            "examples": ["scheduled"],
        },
        "META.STATUS.RETRY": {
            "category": "META",
            "subcategory": "STATUS",
            "description": "Retrying operation",
            "examples": ["reattempting"],
        },
        "META.STATUS.BLOCKED": {
            "category": "META",
            "subcategory": "STATUS",
            "description": "Operation blocked",
            "examples": ["stuck"],
        },
        "META.STATUS.DEGRADED": {
            "category": "META",
            "subcategory": "STATUS",
            "description": "Degraded operation",
            "examples": ["impaired"],
        },
        "META.STATUS.UNKNOWN": {
            "category": "META",
            "subcategory": "STATUS",
            "description": "Unknown status",
            "examples": ["indeterminate"],
        },
        "META.STATUS.CREATED": {
            "category": "META",
            "subcategory": "STATUS",
            "description": "Resource created",
            "examples": ["new"],
        },
        "META.STATUS.DELETED": {
            "category": "META",
            "subcategory": "STATUS",
            "description": "Resource deleted",
            "examples": ["removed"],
        },
        # ERROR
        "META.ERROR.VALIDATION": {
            "category": "META",
            "subcategory": "ERROR",
            "description": "Validation error",
            "examples": ["invalid"],
        },
        "META.ERROR.TIMEOUT": {
            "category": "META",
            "subcategory": "ERROR",
            "description": "Timeout error",
            "examples": ["expired"],
        },
        "META.ERROR.NOT_FOUND": {
            "category": "META",
            "subcategory": "ERROR",
            "description": "Resource not found",
            "examples": ["missing"],
        },
        "META.ERROR.PERMISSION": {
            "category": "META",
            "subcategory": "ERROR",
            "description": "Permission denied",
            "examples": ["forbidden"],
        },
        "META.ERROR.NETWORK": {
            "category": "META",
            "subcategory": "ERROR",
            "description": "Network error",
            "examples": ["connection"],
        },
        "META.ERROR.GENERAL": {
            "category": "META",
            "subcategory": "ERROR",
            "description": "General error",
            "examples": ["unknown"],
        },
        "META.ERROR.INTERNAL": {
            "category": "META",
            "subcategory": "ERROR",
            "description": "Internal server error",
            "examples": ["bug"],
        },
        "META.ERROR.CONFLICT": {
            "category": "META",
            "subcategory": "ERROR",
            "description": "Resource conflict",
            "examples": ["duplicate"],
        },
        "META.ERROR.RATE_LIMIT": {
            "category": "META",
            "subcategory": "ERROR",
            "description": "Rate limit exceeded",
            "examples": ["throttled"],
        },
        "META.ERROR.QUOTA": {
            "category": "META",
            "subcategory": "ERROR",
            "description": "Quota exceeded",
            "examples": ["limit"],
        },
        "META.ERROR.UNAVAILABLE": {
            "category": "META",
            "subcategory": "ERROR",
            "description": "Service unavailable",
            "examples": ["down"],
        },
        "META.ERROR.DEPRECATED": {
            "category": "META",
            "subcategory": "ERROR",
            "description": "Deprecated feature",
            "examples": ["obsolete"],
        },
        "META.ERROR.UNSUPPORTED": {
            "category": "META",
            "subcategory": "ERROR",
            "description": "Unsupported operation",
            "examples": ["not implemented"],
        },
        "META.ERROR.OVERFLOW": {
            "category": "META",
            "subcategory": "ERROR",
            "description": "Overflow error",
            "examples": ["too large"],
        },
        "META.ERROR.UNDERFLOW": {
            "category": "META",
            "subcategory": "ERROR",
            "description": "Underflow error",
            "examples": ["too small"],
        },
        "META.ERROR.ENCODING": {
            "category": "META",
            "subcategory": "ERROR",
            "description": "Encoding error",
            "examples": ["codec"],
        },
        "META.ERROR.DECODING": {
            "category": "META",
            "subcategory": "ERROR",
            "description": "Decoding error",
            "examples": ["parse"],
        },
        "META.ERROR.SIGNATURE": {
            "category": "META",
            "subcategory": "ERROR",
            "description": "Signature error",
            "examples": ["tampered"],
        },
        "META.ERROR.REPLAY": {
            "category": "META",
            "subcategory": "ERROR",
            "description": "Replay attack detected",
            "examples": ["duplicate"],
        },
        "META.ERROR.SCHEMA": {
            "category": "META",
            "subcategory": "ERROR",
            "description": "Schema mismatch",
            "examples": ["incompatible"],
        },
        # CONTROL
        "META.RESPONSE": {
            "category": "META",
            "subcategory": "CONTROL",
            "description": "Response to request",
            "examples": ["reply"],
        },
        "META.REQUEST": {
            "category": "META",
            "subcategory": "CONTROL",
            "description": "Request for action",
            "examples": ["ask"],
        },
        "META.ACK": {
            "category": "META",
            "subcategory": "CONTROL",
            "description": "Acknowledgement",
            "examples": ["received"],
        },
        "META.NACK": {
            "category": "META",
            "subcategory": "CONTROL",
            "description": "Negative ack",
            "examples": ["rejected"],
        },
        "META.HEARTBEAT": {
            "category": "META",
            "subcategory": "CONTROL",
            "description": "Heartbeat signal",
            "examples": ["alive"],
        },
        "META.HANDSHAKE": {
            "category": "META",
            "subcategory": "CONTROL",
            "description": "Protocol handshake",
            "examples": ["init"],
        },
        "META.GOODBYE": {
            "category": "META",
            "subcategory": "CONTROL",
            "description": "Disconnect signal",
            "examples": ["bye"],
        },
        "META.RESET": {
            "category": "META",
            "subcategory": "CONTROL",
            "description": "Reset connection",
            "examples": ["clear"],
        },
        "META.REDIRECT": {
            "category": "META",
            "subcategory": "CONTROL",
            "description": "Redirect to other",
            "examples": ["forward"],
        },
        "META.RETRY": {
            "category": "META",
            "subcategory": "CONTROL",
            "description": "Retry request",
            "examples": ["again"],
        },
        "META.CANCEL": {
            "category": "META",
            "subcategory": "CONTROL",
            "description": "Cancel operation",
            "examples": ["abort"],
        },
        "META.KEEPALIVE": {
            "category": "META",
            "subcategory": "CONTROL",
            "description": "Keep alive signal",
            "examples": ["ping"],
        },
        "META.FLOW.CONTROL": {
            "category": "META",
            "subcategory": "CONTROL",
            "description": "Flow control",
            "examples": ["backpressure"],
        },
        "META.RATE.LIMIT": {
            "category": "META",
            "subcategory": "CONTROL",
            "description": "Rate limiting",
            "examples": ["throttle"],
        },
        "META.CIRCUIT.BREAK": {
            "category": "META",
            "subcategory": "CONTROL",
            "description": "Circuit breaker",
            "examples": ["protection"],
        },
        # PROTOCOL
        "META.PROTOCOL.VERSION": {
            "category": "META",
            "subcategory": "PROTOCOL",
            "description": "Protocol version",
            "examples": ["ver"],
        },
        "META.PROTOCOL.PULSE": {
            "category": "META",
            "subcategory": "PROTOCOL",
            "description": "PULSE protocol",
            "examples": ["pulse"],
        },
        "META.PROTOCOL.HTTP": {
            "category": "META",
            "subcategory": "PROTOCOL",
            "description": "HTTP protocol",
            "examples": ["web"],
        },
        "META.PROTOCOL.HTTPS": {
            "category": "META",
            "subcategory": "PROTOCOL",
            "description": "HTTPS protocol",
            "examples": ["secure web"],
        },
        "META.PROTOCOL.WS": {
            "category": "META",
            "subcategory": "PROTOCOL",
            "description": "WebSocket",
            "examples": ["ws"],
        },
        "META.PROTOCOL.WSS": {
            "category": "META",
            "subcategory": "PROTOCOL",
            "description": "Secure WebSocket",
            "examples": ["wss"],
        },
        "META.PROTOCOL.GRPC": {
            "category": "META",
            "subcategory": "PROTOCOL",
            "description": "gRPC protocol",
            "examples": ["rpc"],
        },
        "META.PROTOCOL.MQTT": {
            "category": "META",
            "subcategory": "PROTOCOL",
            "description": "MQTT protocol",
            "examples": ["iot"],
        },
        "META.PROTOCOL.AMQP": {
            "category": "META",
            "subcategory": "PROTOCOL",
            "description": "AMQP protocol",
            "examples": ["messaging"],
        },
        "META.PROTOCOL.TCP": {
            "category": "META",
            "subcategory": "PROTOCOL",
            "description": "TCP protocol",
            "examples": ["stream"],
        },
        "META.PROTOCOL.UDP": {
            "category": "META",
            "subcategory": "PROTOCOL",
            "description": "UDP protocol",
            "examples": ["datagram"],
        },
        "META.PROTOCOL.TLS": {
            "category": "META",
            "subcategory": "PROTOCOL",
            "description": "TLS protocol",
            "examples": ["ssl"],
        },
        "META.PROTOCOL.QUIC": {
            "category": "META",
            "subcategory": "PROTOCOL",
            "description": "QUIC protocol",
            "examples": ["http3"],
        },
        "META.PROTOCOL.DNS": {
            "category": "META",
            "subcategory": "PROTOCOL",
            "description": "DNS protocol",
            "examples": ["resolution"],
        },
        "META.PROTOCOL.SSH": {
            "category": "META",
            "subcategory": "PROTOCOL",
            "description": "SSH protocol",
            "examples": ["secure shell"],
        },
        # CAPABILITY
        "META.CAP.ENCODE.JSON": {
            "category": "META",
            "subcategory": "CAPABILITY",
            "description": "JSON encoding",
            "examples": ["json"],
        },
        "META.CAP.ENCODE.BINARY": {
            "category": "META",
            "subcategory": "CAPABILITY",
            "description": "Binary encoding",
            "examples": ["msgpack"],
        },
        "META.CAP.ENCODE.COMPACT": {
            "category": "META",
            "subcategory": "CAPABILITY",
            "description": "Compact encoding",
            "examples": ["pulse compact"],
        },
        "META.CAP.SECURITY.SIGN": {
            "category": "META",
            "subcategory": "CAPABILITY",
            "description": "Message signing",
            "examples": ["hmac"],
        },
        "META.CAP.SECURITY.ENCRYPT": {
            "category": "META",
            "subcategory": "CAPABILITY",
            "description": "Encryption support",
            "examples": ["tls"],
        },
        "META.CAP.STREAM": {
            "category": "META",
            "subcategory": "CAPABILITY",
            "description": "Streaming support",
            "examples": ["chunked"],
        },
        "META.CAP.BATCH": {
            "category": "META",
            "subcategory": "CAPABILITY",
            "description": "Batch operations",
            "examples": ["bulk"],
        },
        "META.CAP.SUBSCRIBE": {
            "category": "META",
            "subcategory": "CAPABILITY",
            "description": "Pub/sub support",
            "examples": ["events"],
        },
        "META.CAP.COMPRESS": {
            "category": "META",
            "subcategory": "CAPABILITY",
            "description": "Compression support",
            "examples": ["gzip"],
        },
        "META.CAP.CACHE": {
            "category": "META",
            "subcategory": "CAPABILITY",
            "description": "Caching support",
            "examples": ["etag"],
        },
        # AUDIT
        "META.AUDIT.CREATE": {
            "category": "META",
            "subcategory": "AUDIT",
            "description": "Resource created",
            "examples": ["born"],
        },
        "META.AUDIT.READ": {
            "category": "META",
            "subcategory": "AUDIT",
            "description": "Resource read",
            "examples": ["accessed"],
        },
        "META.AUDIT.UPDATE": {
            "category": "META",
            "subcategory": "AUDIT",
            "description": "Resource updated",
            "examples": ["modified"],
        },
        "META.AUDIT.DELETE": {
            "category": "META",
            "subcategory": "AUDIT",
            "description": "Resource deleted",
            "examples": ["removed"],
        },
        "META.AUDIT.LOGIN": {
            "category": "META",
            "subcategory": "AUDIT",
            "description": "Login event",
            "examples": ["authenticated"],
        },
        "META.AUDIT.LOGOUT": {
            "category": "META",
            "subcategory": "AUDIT",
            "description": "Logout event",
            "examples": ["disconnected"],
        },
        "META.AUDIT.PERMISSION.CHANGE": {
            "category": "META",
            "subcategory": "AUDIT",
            "description": "Permission changed",
            "examples": ["acl"],
        },
        "META.AUDIT.CONFIG.CHANGE": {
            "category": "META",
            "subcategory": "AUDIT",
            "description": "Config changed",
            "examples": ["settings"],
        },
        "META.AUDIT.SECURITY.EVENT": {
            "category": "META",
            "subcategory": "AUDIT",
            "description": "Security event",
            "examples": ["incident"],
        },
        "META.AUDIT.COMPLIANCE": {
            "category": "META",
            "subcategory": "AUDIT",
            "description": "Compliance event",
            "examples": ["regulation"],
        },
        # INFO
        "META.INFO.AGENT": {
            "category": "META",
            "subcategory": "INFO",
            "description": "Agent information",
            "examples": ["about"],
        },
        "META.INFO.PROTOCOL": {
            "category": "META",
            "subcategory": "INFO",
            "description": "Protocol information",
            "examples": ["spec"],
        },
        "META.INFO.CAPABILITY": {
            "category": "META",
            "subcategory": "INFO",
            "description": "Capability listing",
            "examples": ["features"],
        },
        "META.INFO.VOCABULARY": {
            "category": "META",
            "subcategory": "INFO",
            "description": "Vocabulary info",
            "examples": ["concepts"],
        },
        "META.INFO.SCHEMA": {
            "category": "META",
            "subcategory": "INFO",
            "description": "Schema information",
            "examples": ["structure"],
        },
        "META.INFO.HEALTH": {
            "category": "META",
            "subcategory": "INFO",
            "description": "Health information",
            "examples": ["status"],
        },
        "META.INFO.METRICS": {
            "category": "META",
            "subcategory": "INFO",
            "description": "Metrics information",
            "examples": ["stats"],
        },
        "META.INFO.VERSION": {
            "category": "META",
            "subcategory": "INFO",
            "description": "Version information",
            "examples": ["build"],
        },
        "META.INFO.UPTIME": {
            "category": "META",
            "subcategory": "INFO",
            "description": "Uptime information",
            "examples": ["duration"],
        },
        "META.INFO.LOAD": {
            "category": "META",
            "subcategory": "INFO",
            "description": "Load information",
            "examples": ["utilization"],
        },
        "META.INFO.CONNECTIONS": {
            "category": "META",
            "subcategory": "INFO",
            "description": "Connection info",
            "examples": ["peers"],
        },
        "META.INFO.ROUTES": {
            "category": "META",
            "subcategory": "INFO",
            "description": "Routing information",
            "examples": ["endpoints"],
        },
        "META.INFO.CONFIG": {
            "category": "META",
            "subcategory": "INFO",
            "description": "Configuration info",
            "examples": ["settings"],
        },
        "META.INFO.LIMITS": {
            "category": "META",
            "subcategory": "INFO",
            "description": "Rate/size limits",
            "examples": ["quotas"],
        },
        "META.INFO.DOCUMENTATION": {
            "category": "META",
            "subcategory": "INFO",
            "description": "Documentation link",
            "examples": ["docs"],
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
