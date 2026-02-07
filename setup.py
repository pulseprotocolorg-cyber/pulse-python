"""PULSE Protocol - Setup configuration."""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pulse-protocol",
    version="0.1.0",
    author="Sergey Klein",
    author_email="",
    description="Protocol for Universal Language-based System Exchange - Universal semantic protocol for AI-to-AI communication",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pulse-protocol/pulse-python",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pydantic>=2.0",
        "cryptography>=41.0",
        "msgpack>=1.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
            "black>=23.0",
            "pylint>=2.0",
            "mypy>=1.0",
        ],
    },
)
