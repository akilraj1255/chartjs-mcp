# Contributing to Chart.js MCP Server

First off, thank you for considering contributing to the Chart.js MCP Server! It's people like you that make this tool better for everyone.

## How Can I Contribute?

### Reporting Bugs
* Check the existing issues to see if the bug has already been reported.
* If not, open a new issue. Include as much detail as possible: your environment, the steps to reproduce, and what you expected vs what actually happened.

### Suggesting Enhancements
* Open an issue with the "enhancement" label.
* Describe the feature you'd like to see and why it would be useful.

### Pull Requests
1. Fork the repo and create your branch from `master`.
2. If you've added code that should be tested, add tests.
3. If you've changed APIs, update the documentation.
4. Ensure the test suite passes (`uv run python test_comprehensive.py`).
5. Make sure your code follows the existing style.
6. Issue the pull request!

## Development Setup

1. Clone your fork.
2. Install dependencies using `uv`:
   ```bash
   uv sync
   ```
3. Run the server in development mode:
   ```bash
   uv run mcp dev server.py
   ```

## Code of Conduct

Please be respectful and professional in all interactions.

Together, we can make this the best data visualization tool for AI! 🚀
