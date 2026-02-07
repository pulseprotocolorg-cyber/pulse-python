# Contributing to PULSE Protocol

Thank you for your interest in contributing to PULSE Protocol!

## Development Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/pulse-protocol/pulse-python.git
   cd pulse-python
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   pip install -e .
   ```

## Development Workflow

1. **Create a branch** for your feature or bugfix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Write tests first** (TDD approach):
   - Add tests in `tests/`
   - Run tests: `pytest`

3. **Implement your changes**:
   - Follow PEP 8 style guide
   - Use type hints
   - Add docstrings (Google style)

4. **Run quality checks**:
   ```bash
   # Format code
   black pulse/ tests/

   # Lint
   pylint pulse/

   # Type check
   mypy pulse/

   # Run tests with coverage
   pytest --cov=pulse --cov-report=html
   ```

5. **Commit your changes**:
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

   Use conventional commits:
   - `feat:` - New feature
   - `fix:` - Bug fix
   - `docs:` - Documentation
   - `test:` - Tests
   - `refactor:` - Code refactoring

6. **Push and create Pull Request**:
   ```bash
   git push origin feature/your-feature-name
   ```

## Code Style

- **PEP 8** compliance
- **Line length**: 100 characters
- **Type hints**: Required for all functions
- **Docstrings**: Required for all public APIs (Google style)
- **Black** for formatting
- **Pylint** for linting

## Testing

- **Coverage**: Minimum 90% overall, 95% for core modules
- **Test types**: Unit, integration, performance, security
- All tests must pass before PR merge

## Questions?

- Open an issue on GitHub
- Join our Discord community
- Email: dev@pulse-protocol.org

Thank you for contributing! 🚀
