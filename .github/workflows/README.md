# GitHub Actions Workflows

This directory contains CI/CD workflows for the Analytics Tutorials project.

## Workflows

### CI Workflow (`ci.yml`)

Runs on every push and pull request to `main` and `develop` branches.

**Jobs:**

1. **lint-and-format**
   - Installs uv package manager via direct shell script
   - Runs Ruff linter to check code quality
   - Runs Ruff formatter to check code formatting
   - Runs Black to verify consistent formatting
   - Fails if any issues are found

2. **test**
   - Tests across multiple Python versions (3.8-3.12)
   - Tests on multiple OS platforms (Ubuntu, Windows, macOS)
   - Installs uv with platform-specific scripts (Unix/Windows)
   - Generates test data with `setup_database.py`
   - Runs pytest with coverage reporting
   - Uploads coverage to Codecov (for Ubuntu + Python 3.11)

3. **validate-tutorials**
   - Validates tutorial script syntax
   - Runs the getting started tutorial to ensure basic functionality
   - Ensures tutorials are executable

**Note:** The workflow uses direct uv installation scripts instead of the GitHub Action to ensure reliability across all platforms.

## Running CI Checks Locally

Before pushing, run these commands to catch issues early:

```bash
# Run all linting and formatting checks
ruff check .
ruff format --check .
black --check .

# Run tests
pytest

# Or use the Makefile
make ci
```

## Workflow Triggers

- **Push**: Runs on pushes to `main` and `develop` branches
- **Pull Request**: Runs on PRs targeting `main` and `develop` branches

## Required Status Checks

For pull requests to be merged, all CI jobs must pass:
- ✅ Linting (Ruff)
- ✅ Formatting (Black + Ruff)
- ✅ Tests on all supported Python versions and platforms
- ✅ Tutorial validation

## Badges

The CI status badge in README.md shows the current build status:

```markdown
[![CI](https://github.com/Wicks-Analytics/analytics_tutorials/actions/workflows/ci.yml/badge.svg)](https://github.com/Wicks-Analytics/analytics_tutorials/actions/workflows/ci.yml)
```

## Modifying Workflows

When modifying workflows:
1. Test changes in a feature branch
2. Ensure all jobs complete successfully
3. Update this README if adding new jobs or workflows

## Secrets and Environment Variables

Currently, no secrets are required for CI. If adding integrations that need secrets:
1. Add secrets in repository settings
2. Reference them in workflow with `${{ secrets.SECRET_NAME }}`
3. Document them in this README
