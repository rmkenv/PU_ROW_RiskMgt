# Create the complete GitHub repository structure for the ROW Risk Management system

import os
from pathlib import Path

# Create the repository structure
repo_structure = {
    'root_files': [
        'README.md',
        'LICENSE',
        'requirements.txt',
        'setup.py',
        'pyproject.toml',
        '.gitignore',
        'CONTRIBUTING.md',
        'CHANGELOG.md'
    ],
    'directories': {
        'row_risk_manager': [
            '__init__.py',
            'core.py',
            'data_acquisition.py',
            'vegetation_analysis.py',
            'risk_assessment.py',
            'prioritization.py',
            'reporting.py',
            'utils.py',
            'config.py'
        ],
        'tests': [
            '__init__.py',
            'test_core.py',
            'test_data_acquisition.py',
            'test_vegetation_analysis.py',
            'test_risk_assessment.py',
            'conftest.py'
        ],
        'docs': [
            'index.rst',
            'installation.rst',
            'quickstart.rst',
            'api_reference.rst',
            'examples.rst',
            'conf.py'
        ],
        'examples': [
            'basic_workflow.py',
            'advanced_analysis.py',
            'custom_risk_models.py',
            'README.md'
        ],
        'data': [
            'sample_row_corridor.geojson',
            'README.md',
            '.gitkeep'
        ],
        'configs': [
            'default_config.json',
            'development_config.json',
            'production_config.json'
        ],
        'scripts': [
            'download_sample_data.py',
            'setup_environment.py',
            'run_tests.py'
        ],
        '.github': {
            'workflows': [
                'ci.yml',
                'docs.yml'
            ],
            'ISSUE_TEMPLATE': [
                'bug_report.md',
                'feature_request.md'
            ]
        }
    }
}

print("Repository Structure:")
print("====================")

# Print the structure
for category, items in repo_structure.items():
    if category == 'root_files':
        print("\nRoot Files:")
        for file in items:
            print(f"  {file}")
    elif category == 'directories':
        print("\nDirectories:")
        for dir_name, files in items.items():
            if isinstance(files, dict):
                print(f"  {dir_name}/")
                for subdir, subfiles in files.items():
                    print(f"    {subdir}/")
                    for subfile in subfiles:
                        print(f"      {subfile}")
            else:
                print(f"  {dir_name}/")
                for file in files:
                    print(f"    {file}")

print(f"\nTotal files to create: {sum(len(files) if isinstance(files, list) else sum(len(subfiles) for subfiles in files.values()) for files in repo_structure['directories'].values()) + len(repo_structure['root_files'])}")