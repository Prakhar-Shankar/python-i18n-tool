## i18n Checker

#### A powerful tool for detecting unused and missing localization keys across multiple languages and frameworks

## Project Overview

Localization is a critical aspect of modern software development, ensuring that applications support multiple languages. However, managing internationalization (i18n) keys can become complex as projects grow. Unused keys in translation files bloat the project, while missing keys can lead to broken or untranslated UI elements.

This project develops a tool that efficiently detects: 

  `Unused Keys`: Keys present in the i18n JSON/YAML/PO files but not used in the codebase.
    
  `Missing Keys`: Keys referenced in the code but absent in the translation files.

Originally designed for Python projects, this tool supports multiple programming languages and frameworks, making it highly versatile. It features a CLI tool for developers and can be integrated into CI/CD pipelines to automate i18n validation in real-time during development workflows.

## Installation

You can install the i18n-checker tool using pip:

```bash
# Install from PyPI (once published)
pip install i18n-checker

# Install from the source code directory
git clone https://github.com/Prakhar-Shankar/python-i18n-tool.git
cd i18n-checker
pip install -e .
```

After installation, the `i18n-checker` command will be available in your terminal.

## Usage

The tool is designed to be easy to use with a simple command-line interface:

```bash
# Basic usage - scan a directory
i18n-checker --scan ./your_project_directory

# Generate a detailed report file
i18n-checker --scan ./your_project_directory --output report.txt

# Generate suggestions to fix missing keys
i18n-checker --scan ./your_project_directory --fix

# Generate an HTML report with tabular format
i18n-checker --scan ./your_project_directory --format html

# Generate HTML report with suggestions
i18n-checker --scan ./your_project_directory --format html --fix --output i18n_report.html
```

## Features

1. **Comprehensive Scanning**: Scans Python, JavaScript, TypeScript, and Vue files for i18n key usage.

2. **Detailed Reporting**: Provides information about:
   - Missing i18n keys (used in code but not in translation files)
   - Unused i18n keys (in translation files but not used in code)
   - Line numbers and file paths where keys are used
   - Which translation files contain which keys
   - Language detection for better organization

3. **Fix Suggestions**: With the `--fix` flag, the tool generates suggestions for adding missing keys to the appropriate translation files.

4. **Multiple Report Formats**:
   - Text reports (default): Comprehensive textual information
   - HTML reports: Beautiful tabular format with color coding and visual organization

## Example Output

### Text Format
The tool provides:
- Console output with summary information
- Detailed report file with comprehensive findings
- Specific file locations for each missing or unused key
- JSON snippets for suggested fixes

### HTML Format
The HTML report includes:
- Tabular format for both missing and unused keys
- Color-coded entries for better readability
- Index counting for easy reference
- Language detection and display
- File paths and line numbers where keys are used
- Suggestions formatted in code blocks for easy copying

## CI/CD Integration

The i18n-checker includes built-in support for CI/CD pipelines, making it easy to automate internationalization validation as part of your development workflow:

### GitHub Actions Integration

A GitHub Actions workflow is provided in the `.github/workflows/ci_cd.yml` file, which:

1. Runs automated tests on multiple Python versions (3.8, 3.9, 3.10)
2. Performs code quality checks with flake8
3. Builds and validates the package
4. Can be configured to automatically publish releases to PyPI

### Using in Your CI/CD Pipeline

Add i18n validation to your existing CI/CD pipeline:

```yaml
# Example step for GitLab CI
i18n-validation:
  stage: test
  script:
    - pip install i18n-checker
    - i18n-checker --scan ./src --format html --output i18n_report.html
  artifacts:
    paths:
      - i18n_report.html
```

### Benefits of CI/CD Integration

- **Catch i18n issues early**: Identify missing and unused keys before they reach production
- **Automated Reports**: Generate reports automatically on each commit or pull request
- **Quality Assurance**: Maintain high-quality translations across your application
- **Workflow Integration**: Seamlessly fits into existing development workflows

## Supported File Types

- **Code Files**: Python (.py), JavaScript (.js), TypeScript (.ts), Vue (.vue)
- **Translation Files**: JSON (.json)

Future versions will add support for more file formats.

## Programmatic Usage

You can also use the tool programmatically in your Python code:

```python
from i18n_checker.checker import run_checker

# Create args similar to command-line args
class Args:
    def __init__(self):
        self.scan = './your_project'
        self.fix = True
        self.output = 'report.html'
        self.format = 'html'

# Run the checker
result = run_checker(Args())

# Process the results
if result:
    missing_keys = result['missing_keys']
    unused_keys = result['unused_keys']
    # Do something with the results
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
