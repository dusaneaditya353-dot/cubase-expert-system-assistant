# Contributing to Cubase Expert System Assistant

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/cubase-expert-system-assistant.git`
3. Create a branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test your changes
6. Commit: `git commit -m "feat: add new feature"`
7. Push: `git push origin feature/your-feature-name`
8. Open a Pull Request

## Development Setup

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Frontend
```bash
cd frontend
npm install
```

## Code Style

### Python
- Follow PEP 8
- Use type hints
- Write docstrings for functions and classes
- Maximum line length: 100 characters

### TypeScript/React
- Use TypeScript strict mode
- Follow React best practices
- Use functional components with hooks
- Use meaningful variable names

## Testing

### Backend Tests
```bash
cd backend
pytest tests/ -v
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Commit Messages

Follow conventional commits:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes
- `refactor:` Code refactoring
- `test:` Test additions/changes
- `chore:` Build/tooling changes

## Pull Request Process

1. Update documentation if needed
2. Add tests for new features
3. Ensure all tests pass
4. Update CHANGELOG.md
5. Request review from maintainers

## Adding Knowledge Base Entries

To add new Cubase knowledge:

1. Edit `backend/knowledge_loader.py`
2. Add entry to the `entries` list:
```python
{
    "id": "kb_unique_id",
    "title": "Entry Title",
    "category": "category_name",
    "content": "Detailed content...",
    "tags": ["tag1", "tag2"],
    "last_updated": "2025-12-12"
}
```
3. Add corresponding tests

## Code Review

All submissions require review. We use GitHub pull requests for this purpose.

## Questions?

Open an issue or reach out to the maintainers.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
