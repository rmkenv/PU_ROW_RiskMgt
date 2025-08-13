# Contributing to Power Utility ROW Risk Management System

Thank you for considering contributing to the Power Utility ROW Risk Management System! This document provides guidelines and information for contributors.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Documentation](#documentation)
- [Submitting Changes](#submitting-changes)
- [Issue Guidelines](#issue-guidelines)
- [Recognition](#recognition)

## Code of Conduct

This project adheres to a code of conduct to ensure a welcoming environment for all contributors. Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md).

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- GDAL/OGR libraries installed on your system
- Basic familiarity with geospatial data processing

### Development Setup

1. **Fork and Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/power-utility-row-risk-management.git
   cd power-utility-row-risk-management
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Development Dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -e .[dev]
   ```

4. **Install Pre-commit Hooks**
   ```bash
   pre-commit install
   ```

5. **Verify Installation**
   ```bash
   pytest tests/
   ```

## Development Workflow

### Branching Strategy

We use a feature branch workflow:

1. **Create a Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Your Changes**
   - Write code
   - Add tests
   - Update documentation

3. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "Add feature: your descriptive commit message"
   ```

4. **Push and Create Pull Request**
   ```bash
   git push origin feature/your-feature-name
   ```

### Branch Naming Conventions

- `feature/description` - New features
- `bugfix/description` - Bug fixes
- `docs/description` - Documentation improvements
- `refactor/description` - Code refactoring
- `test/description` - Test improvements

## Coding Standards

### Python Style Guide

We follow PEP 8 with some modifications:

- **Line Length**: 88 characters (Black default)
- **Import Organization**: Use `isort` for consistent imports
- **Type Hints**: Required for all public functions
- **Docstrings**: Google-style docstrings for all modules, classes, and functions

### Code Formatting

We use automated tools to maintain code quality:

```bash
# Format code
black row_risk_manager/
isort row_risk_manager/

# Lint code
flake8 row_risk_manager/
pylint row_risk_manager/

# Type checking
mypy row_risk_manager/
```

### Example Code Structure

```python
"""Module docstring describing purpose."""

from typing import Optional, List, Dict, Any
import logging

import geopandas as gpd
import numpy as np
from loguru import logger


class ExampleClass:
    """Class docstring describing purpose and usage.
    
    Args:
        param1: Description of parameter 1.
        param2: Description of parameter 2.
        
    Attributes:
        attribute1: Description of attribute 1.
    """
    
    def __init__(self, param1: str, param2: Optional[int] = None) -> None:
        """Initialize the class."""
        self.attribute1 = param1
        self._private_attr = param2
        
    def public_method(self, data: gpd.GeoDataFrame) -> Dict[str, Any]:
        """Public method docstring.
        
        Args:
            data: Input geospatial dataframe.
            
        Returns:
            Dictionary containing processed results.
            
        Raises:
            ValueError: If data is invalid.
        """
        if data.empty:
            raise ValueError("Input data cannot be empty")
            
        return {"processed": True, "count": len(data)}
```

## Testing

### Test Organization

Tests are organized in the `tests/` directory mirroring the source structure:

```
tests/
├── __init__.py
├── conftest.py                    # Pytest configuration and fixtures
├── test_core.py                   # Core functionality tests
├── test_data_acquisition.py       # Data acquisition tests
├── test_vegetation_analysis.py    # Vegetation analysis tests
└── test_risk_assessment.py       # Risk assessment tests
```

### Writing Tests

- Use `pytest` for all tests
- Aim for >85% code coverage
- Write both unit and integration tests
- Use fixtures for common test data

```python
import pytest
import geopandas as gpd
from shapely.geometry import Point

from row_risk_manager.core import ROWRiskAssessment


class TestROWRiskAssessment:
    """Test suite for ROWRiskAssessment class."""
    
    @pytest.fixture
    def sample_corridor(self):
        """Create sample corridor data for testing."""
        return gpd.GeoDataFrame({
            'geometry': [Point(0, 0).buffer(100)],
            'line_name': ['Test Line'],
            'voltage': [500]
        }, crs='EPSG:4326')
    
    def test_initialization(self, sample_corridor, tmp_path):
        """Test ROWRiskAssessment initialization."""
        corridor_path = tmp_path / "test_corridor.shp"
        sample_corridor.to_file(corridor_path)
        
        assessment = ROWRiskAssessment(str(corridor_path))
        
        assert len(assessment.row_corridor) == 1
        assert assessment.config is not None
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=row_risk_manager

# Run specific test file
pytest tests/test_vegetation_analysis.py

# Run tests with specific markers
pytest -m "not slow"
```

## Documentation

### Docstring Style

Use Google-style docstrings:

```python
def calculate_ndvi(red_band: np.ndarray, nir_band: np.ndarray) -> np.ndarray:
    """Calculate NDVI from red and near-infrared bands.
    
    The Normalized Difference Vegetation Index (NDVI) is calculated as:
    NDVI = (NIR - Red) / (NIR + Red)
    
    Args:
        red_band: Red band reflectance values (0-1).
        nir_band: Near-infrared band reflectance values (0-1).
        
    Returns:
        NDVI values ranging from -1 to 1.
        
    Raises:
        ValueError: If band dimensions don't match.
        
    Example:
        >>> red = np.array([[0.1, 0.2], [0.3, 0.4]])
        >>> nir = np.array([[0.8, 0.7], [0.6, 0.5]])
        >>> ndvi = calculate_ndvi(red, nir)
        >>> ndvi.shape
        (2, 2)
    """
```

### Building Documentation

```bash
# Install documentation dependencies
pip install -e .[docs]

# Build documentation
cd docs
make html

# View documentation
open _build/html/index.html
```

## Submitting Changes

### Pull Request Process

1. **Ensure Your Fork is Up to Date**
   ```bash
   git remote add upstream https://github.com/original/power-utility-row-risk-management.git
   git fetch upstream
   git rebase upstream/main
   ```

2. **Create Quality Pull Request**
   - Clear, descriptive title
   - Detailed description of changes
   - Reference relevant issues
   - Include screenshots for UI changes

3. **Pull Request Checklist**
   - [ ] Tests pass locally
   - [ ] Code follows style guidelines
   - [ ] Documentation updated
   - [ ] CHANGELOG.md updated (if applicable)
   - [ ] No merge conflicts

### Pull Request Template

```markdown
## Description
Brief description of changes and motivation.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
Describe the tests you ran and how to reproduce them.

## Screenshots (if applicable)
Add screenshots for visual changes.

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Tests added/updated
- [ ] Documentation updated
```

## Issue Guidelines

### Bug Reports

Use the bug report template and include:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- System information (OS, Python version, etc.)
- Error messages or logs

### Feature Requests

Use the feature request template and include:
- Clear description of the feature
- Use case and motivation
- Proposed implementation (optional)
- Alternative solutions considered

### Issue Labels

- `bug`: Something isn't working
- `enhancement`: New feature or request
- `documentation`: Improvements to documentation
- `good first issue`: Good for newcomers
- `help wanted`: Extra attention needed
- `priority: high/medium/low`: Priority level

## Development Best Practices

### Geospatial Data Handling

- Always specify coordinate reference systems (CRS)
- Use appropriate data types (Float32 vs Float64)
- Handle missing data appropriately
- Validate geospatial inputs

```python
def process_corridor(corridor_gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """Process ROW corridor data."""
    # Always check CRS
    if corridor_gdf.crs is None:
        logger.warning("No CRS specified, assuming EPSG:4326")
        corridor_gdf.crs = "EPSG:4326"
    
    # Validate geometry
    if not corridor_gdf.geometry.is_valid.all():
        corridor_gdf.geometry = corridor_gdf.geometry.buffer(0)
    
    return corridor_gdf
```

### Error Handling

- Use specific exception types
- Provide helpful error messages
- Log errors appropriately

```python
from row_risk_manager.exceptions import DataValidationError

def validate_satellite_data(data: np.ndarray) -> None:
    """Validate satellite data array."""
    if data.size == 0:
        raise DataValidationError("Satellite data array is empty")
    
    if not np.isfinite(data).all():
        raise DataValidationError("Satellite data contains invalid values")
```

### Performance Considerations

- Use vectorized operations with NumPy/Pandas
- Consider memory usage for large datasets
- Profile code for bottlenecks
- Use appropriate data structures

## Recognition

Contributors will be recognized in:
- CONTRIBUTORS.md file
- Release notes for significant contributions
- Annual contributor acknowledgments

### Types of Contributions

We value all types of contributions:
- Code improvements
- Bug reports and fixes
- Documentation improvements
- Test improvements
- Performance optimizations
- User experience enhancements
- Community support

## Questions?

If you have questions about contributing, please:
- Check existing documentation
- Search closed issues
- Create a new discussion
- Contact maintainers

Thank you for contributing to the Power Utility ROW Risk Management System!