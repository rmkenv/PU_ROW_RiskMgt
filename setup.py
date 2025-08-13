#!/usr/bin/env python3
"""
Setup script for Power Utility ROW Risk Management System
"""

from setuptools import setup, find_packages
import os
from pathlib import Path

# Read the README file for long description
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

# Read requirements from requirements.txt
def parse_requirements(filename):
    """Load requirements from a pip requirements file."""
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]

# Get version
def get_version():
    """Get version from __init__.py"""
    version_file = this_directory / "row_risk_manager" / "__init__.py"
    if version_file.exists():
        with open(version_file) as f:
            for line in f:
                if line.startswith('__version__'):
                    return line.split('=')[1].strip().strip('"').strip("'")
    return "1.0.0"

# Core dependencies (production only)
install_requires = [
    "geopandas>=0.13.0",
    "rasterio>=1.3.6",
    "shapely>=2.0.0",
    "fiona>=1.9.0",
    "pyproj>=3.5.0",
    "earthpy>=0.9.4",
    "rasterstats>=0.19.0",
    "scikit-learn>=1.2.0",
    "xgboost>=1.7.0",
    "pandas>=1.5.0",
    "numpy>=1.24.0",
    "folium>=0.14.0",
    "plotly>=5.13.0",
    "requests>=2.28.0",
    "click>=8.1.0",
    "pyyaml>=6.0",
    "tqdm>=4.64.0",
    "loguru>=0.6.0"
]

# Development dependencies
extras_require = {
    'dev': [
        "pytest>=7.2.0",
        "pytest-cov>=4.0.0",
        "black>=23.1.0",
        "isort>=5.12.0",
        "flake8>=6.0.0",
        "pylint>=2.16.0",
        "mypy>=1.0.0",
        "pre-commit>=3.0.0"
    ],
    'docs': [
        "sphinx>=6.1.0",
        "sphinx-rtd-theme>=1.2.0",
        "nbsphinx>=0.8.12",
        "sphinx-autodoc-typehints>=1.22.0"
    ],
    'notebook': [
        "jupyter>=1.0.0",
        "jupyterlab>=3.6.0",
        "ipykernel>=6.21.0",
        "ipywidgets>=8.0.0"
    ],
    'lidar': [
        "laspy>=2.4.0",
        "pdal>=3.2.0",
        "whitebox>=2.3.0",
        "pyntcloud>=0.3.1"
    ],
    'satellite': [
        "sentinel-sat>=1.1.1",
        "landsat-util>=0.12.0",
        "rioxarray>=0.15.0",
        "xarray>=2023.1.0"
    ],
    'visualization': [
        "streamlit>=1.20.0",
        "dash>=2.8.0",
        "bokeh>=3.0.0",
        "contextily>=1.3.0",
        "holoviews>=1.16.0"
    ],
    'ml': [
        "lightgbm>=3.3.5",
        "statsmodels>=0.13.5",
        "cvxpy>=1.3.0"
    ],
    'cloud': [
        "boto3>=1.26.0",
        "azure-storage-blob>=12.14.0",
        "google-cloud-core>=2.3.0"
    ]
}

# All extras combined
extras_require['all'] = list(set(
    dep for deps in extras_require.values() for dep in deps
))

setup(
    name="row-risk-manager",
    version=get_version(),
    author="ROW Risk Management Team",
    author_email="support@row-risk-manager.org",
    description="Comprehensive Python workflow for power utility ROW risk management",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/power-utility-row-risk-management",
    project_urls={
        "Bug Tracker": "https://github.com/yourusername/power-utility-row-risk-management/issues",
        "Documentation": "https://row-risk-manager.readthedocs.io",
        "Source": "https://github.com/yourusername/power-utility-row-risk-management",
    },
    packages=find_packages(exclude=["tests", "tests.*", "docs", "examples"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Other Audience",
        "Topic :: Scientific/Engineering :: GIS",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Environment :: Web Environment",
    ],
    python_requires=">=3.8",
    install_requires=install_requires,
    extras_require=extras_require,
    include_package_data=True,
    package_data={
        "row_risk_manager": [
            "data/*.json",
            "configs/*.json",
            "templates/*.html",
            "static/css/*.css",
            "static/js/*.js"
        ],
    },
    entry_points={
        "console_scripts": [
            "row-risk-assess=row_risk_manager.cli:main",
            "row-download-data=row_risk_manager.data_acquisition:download_cli",
            "row-analyze-vegetation=row_risk_manager.vegetation_analysis:analyze_cli",
            "row-assess-risk=row_risk_manager.risk_assessment:assess_cli",
            "row-generate-report=row_risk_manager.reporting:report_cli",
        ],
    },
    keywords=[
        "utility", "power", "transmission", "right-of-way", "ROW",
        "vegetation", "risk", "assessment", "satellite", "lidar",
        "GIS", "remote-sensing", "NDVI", "canopy-height",
        "wildfire", "flood", "landslide", "NERC", "FAC-003"
    ],
    zip_safe=False,
    test_suite="tests",
    tests_require=extras_require['dev'],
)