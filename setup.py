"""Setup configuration for PULSE Protocol."""
from setuptools import setup, find_packages
from pathlib import Path

# Read version
version = {}
with open("pulse/version.py") as f:
    exec(f.read(), version)

# Read README
long_description = Path("README.md").read_text(encoding="utf-8")

setup(
    name="pulse-protocol",
    version=version["__version__"],
    author="Sergey Klein",
    author_email="pulse@example.com",
    description="Universal semantic protocol for AI-to-AI communication",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pulse-protocol/pulse-python",
    packages=find_packages(exclude=["tests*", "examples*"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
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
        "msgpack>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "pylint>=2.15.0",
            "mypy>=0.990",
        ],
    },
    entry_points={
        "console_scripts": [
            "pulse=pulse.cli:main",
        ],
    },
    keywords="ai protocol communication agents semantic multi-agent",
    project_urls={
        "Bug Reports": "https://github.com/pulse-protocol/pulse-python/issues",
        "Source": "https://github.com/pulse-protocol/pulse-python",
        "Documentation": "https://github.com/pulse-protocol/pulse-python#readme",
    },
)
