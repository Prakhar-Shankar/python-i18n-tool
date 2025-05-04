# i18n-checker: Comprehensive Documentation

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Key Components](#2-key-components)
3. [Core Functionality](#3-core-functionality)
4. [CI/CD Integration](#4-cicd-integration)
5. [Testing Structure](#5-testing-structure)
6. [Demo Components](#6-demo-components)
7. [Installation & Usage](#7-installation--usage)
8. [Code Explanations](#8-code-explanations)
9. [File Reference](#9-file-reference)
10. [Converting This Document to PDF](#10-converting-this-document-to-pdf)

## 1. Project Overview

The i18n-checker is a powerful tool designed for detecting unused and missing localization keys across multiple languages and frameworks. It helps developers maintain clean and complete internationalization (i18n) implementations by:

- Finding **unused keys** that exist in translation files but aren't referenced in code
- Identifying **missing keys** that are used in code but not defined in translation files
- Generating detailed reports in various formats (text, HTML)
- Suggesting fixes for missing translations
- Integrating with CI/CD pipelines to automate i18n validation

Originally designed for Python projects, the tool has been expanded to support multiple programming languages including JavaScript, TypeScript, and Vue.js, making it versatile for a wide range of development environments.

## 2. Key Components

The i18n-checker consists of several key components:

### 2.1 Core Engine

**Location:** `i18n_checker/checker.py`  
The core functionality responsible for scanning files, extracting keys, and analyzing usage patterns.

### 2.2 Command-Line Interface

**Location:** `i18n_checker/cli.py`  
Provides a user-friendly interface for running the tool from the command line.

### 2.3 Package Setup

**Files:** `setup.py`, `pyproject.toml`, `MANIFEST.in`, `requirements.txt`  
These files configure the Python package, making it installable via pip.

### 2.4 CI/CD Integration

**Location:** `.github/workflows/ci_cd.yml`  
GitHub Actions workflow that automates testing and validation of the i18n-checker tool itself.

### 2.5 Testing Framework

**Location:** `tests/` directory  
Contains unit and integration tests that verify the tool's functionality.

### 2.6 Documentation

**Files:** `README.md`, `testing_plan.md`  
Detailed information about the tool, its features, and testing approach.

## 3. Core Functionality

### 3.1 File Scanning

The tool scans a project directory to identify:
- Code files (Python, JavaScript, TypeScript, Vue.js)
- Translation files (JSON)

```python
def find_files(directory, extensions):
    """Find all files with given extensions in the directory."""
    found_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(extensions):
                found_files.append(os.path.join(root, file))
    return found_files
```

### 3.2 Key Extraction

For translation files:
- Parses JSON files to extract all keys
- Handles nested keys with dot notation
- Identifies the language based on file path or name

```python
def extract_keys_from_json(file_path, parent_key=""):
    """Extract all keys from a JSON file, including nested keys."""
    keys = set()
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            keys = extract_nested_keys(data, parent_key)
    except json.JSONDecodeError:
        print(f"⚠️ Error: Could not parse {file_path}. Skipping...")
    return keys
```

For code files:
- Uses regex patterns to find i18n key usage
- Supports various i18n implementation patterns
- Records file and line number for each key usage

```python
def extract_used_keys_from_python(file_path):
    """Extract i18n keys used in Python files."""
    key_pattern = re.compile(r'_\(["\']([^"\']+)["\']\)|gettext\(["\']([^"\']+)["\']\)')
    used_keys = {}

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, 1):
                matches = key_pattern.findall(line)
                for match in matches:
                    key = match[0] if match[0] else match[1]
                    if key not in used_keys:
                        used_keys[key] = []
                    used_keys[key].append((file_path, line_num, line.strip()))
    except Exception as e:
        print(f"⚠️ Error reading {file_path}: {e}")
    
    return used_keys
```

### 3.3 Analysis and Reporting

- Compares keys in translation files with keys used in code
- Identifies missing and unused keys
- Generates detailed reports in text or HTML format
- Creates fix suggestions for missing keys

```python
def generate_html_report(missing_keys, unused_keys, used_keys, json_key_locations, missing_key_suggestions, fix_missing):
    """Generate an HTML report with missing and unused keys."""
    # Implementation details...
```

## 4. CI/CD Integration

### 4.1 GitHub Actions Workflow

The i18n-checker includes a GitHub Actions workflow that:
- Runs tests on multiple Python versions (3.8, 3.9, 3.10)
- Checks code quality with flake8
- Builds and validates the package
- Can be configured to publish to PyPI automatically

```yaml
name: i18n-checker CI/CD Pipeline

on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]
  workflow_dispatch:  # Allow manual triggers

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, '3.10']

    steps:
    - uses: actions/checkout@v3
    # Additional steps for testing, linting, etc.
```

### 4.2 Client Project Integration

Projects using i18n-checker can integrate it into their CI/CD pipeline:

```yaml
# Example GitHub Actions workflow for client projects
name: i18n Validation

on:
  push:
    branches: [ main, master ]

jobs:
  i18n-check:
    runs-on: ubuntu-latest
    name: Check for i18n issues
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
        
    - name: Install i18n-checker
      run: |
        python -m pip install --upgrade pip
        pip install i18n-checker
        
    - name: Run i18n validation
      run: |
        i18n-checker --scan . --format html --output i18n_report.html
```

## 5. Testing Structure

### 5.1 Testing Plan

The testing plan includes comprehensive testing across multiple dimensions:

| Testing Type | Purpose | Examples |
|-------------|---------|----------|
| Unit | Test individual functions | Key extraction, pattern matching |
| Integration | Test module interactions | CLI ↔ Checker Engine |
| Performance | Test efficiency | Large directory scanning |
| Stress | Test resource handling | Memory usage with large files |
| Compliance | Test framework compatibility | Various i18n patterns |
| Load | Test under high load | CI/CD pipeline integration |
| Security | Test code safety | File access, input validation |
| Volume | Test with high volumes | Enterprise-level applications |

### 5.2 Unit Tests

The `tests/` directory contains unit tests for core functionality:

```python
def test_extract_keys_from_json(self):
    """Test extracting keys from a JSON file."""
    keys = extract_keys_from_json(self.json_path)
    expected_keys = {"greeting", "user", "user.name", "user.email", "messages"}
    self.assertEqual(keys, expected_keys)
```

## 6. Demo Components

The project includes several demonstration components:

### 6.1 Internal CI/CD Demo

The `demo_cicd.py` script simulates the CI/CD pipeline for the i18n-checker tool itself:

```python
def simulate_cicd_pipeline():
    """Simulate a CI/CD pipeline for demonstration purposes."""
    # Steps:
    # 1. Prepare environment
    # 2. Configure i18n checker
    # 3. Run validation
    # 4. Analyze results
    # 5. Generate reports
```

### 6.2 Client Project Demo

The `client_project_demo.py` script demonstrates how a client project would integrate i18n-checker:

```python
def simulate_client_cicd():
    """Simulate how a client project would use i18n-checker in CI/CD."""
    # Steps:
    # 1. Project setup
    # 2. Examine code for i18n keys
    # 3. CI/CD integration
    # 4. Run validation
    # 5. Process results
```

### 6.3 Demo Client Project

The `demo-client-project/` directory contains a sample JavaScript application that uses i18n:
- Source code with i18n key usage
- Translation files in JSON format
- GitHub Actions workflow for i18n validation
- Package configuration with scripts for i18n checking

## 7. Installation & Usage

### 7.1 Installation

```bash
# Install from PyPI (once published)
pip install i18n-checker

# Install from source
git clone https://github.com/Prakhar-Shankar/python-i18n-tool.git
cd i18n-checker
pip install -e .
```

### 7.2 Basic Usage

```bash
# Basic usage - scan a directory
i18n-checker --scan ./your_project_directory

# Generate a detailed report file
i18n-checker --scan ./your_project_directory --output report.txt

# Generate suggestions to fix missing keys
i18n-checker --scan ./your_project_directory --fix

# Generate an HTML report with tabular format
i18n-checker --scan ./your_project_directory --format html
```

### 7.3 Programmatic Usage

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

## 8. Code Explanations

### 8.1 checker.py

The main engine of the i18n-checker tool performs these key operations:

1. **File Discovery**:
   - Scans directories for code and translation files
   - Filters by file extensions

2. **Key Extraction**:
   - From JSON files: Parses and extracts all keys, including nested ones
   - From code files: Uses regex patterns to find i18n key usage

3. **Analysis**:
   - Compares translation keys with keys used in code
   - Identifies missing and unused keys

4. **Reporting**:
   - Generates text or HTML reports
   - Creates fix suggestions for missing keys

Key functions:
- `find_files()`: Find files with specific extensions
- `extract_keys_from_json()`: Extract keys from JSON translation files
- `extract_used_keys_from_python()`: Extract i18n keys from Python files
- `extract_used_keys_from_js_ts()`: Extract i18n keys from JavaScript/TypeScript
- `extract_used_keys_from_vue()`: Extract i18n keys from Vue.js files
- `run_checker()`: Main function that orchestrates the entire process

### 8.2 cli.py

The command-line interface provides a user-friendly way to run the tool:

1. **Argument Parsing**:
   - Defines command-line arguments (scan directory, output file, etc.)
   - Validates user input

2. **Execution**:
   - Calls the checker engine with the specified arguments
   - Returns appropriate exit codes

Key functions:
- `main()`: Entry point for the command-line tool
- `parse_args()`: Parse command-line arguments

## 9. File Reference

### 9.1 Core Project Files

| File/Directory | Purpose |
|----------------|---------|
| `i18n_checker/` | Core code directory |
| `i18n_checker/checker.py` | Main engine for i18n checking |
| `i18n_checker/cli.py` | Command-line interface |
| `setup.py` | Package setup for pip installation |
| `pyproject.toml` | Python project configuration |
| `requirements.txt` | Package dependencies |
| `MANIFEST.in` | Files to include in the package |
| `LICENSE` | MIT license file |
| `README.md` | Project documentation |

### 9.2 Testing Files

| File/Directory | Purpose |
|----------------|---------|
| `tests/` | Test directory |
| `tests/test_basic.py` | Basic unit tests |
| `test_code/` | Sample code for testing |
| `testing_plan.md` | Testing strategy documentation |

### 9.3 CI/CD Files

| File/Directory | Purpose |
|----------------|---------|
| `.github/workflows/ci_cd.yml` | GitHub Actions workflow |

### 9.4 Demo and Presentation Files

| File/Directory | Purpose |
|----------------|---------|
| `demo_cicd.py` | Demonstrates i18n-checker's own CI/CD |
| `client_project_demo.py` | Shows how clients would use i18n-checker |
| `demo-client-project/` | Sample client project directory |
| `presentation_script.md` | Script for project presentation |

## 10. Converting This Document to PDF

To convert this Markdown document to PDF, you can use one of the following methods:

### Method 1: Using Pandoc

```bash
# Install Pandoc and a PDF engine
sudo apt-get install pandoc texlive-xetex

# Convert to PDF
pandoc i18n-checker-documentation.md -o i18n-checker-documentation.pdf --pdf-engine=xelatex
```

### Method 2: Using a Web Browser

1. Open the Markdown file in a web browser (you may need to use a Markdown viewer extension)
2. Use the browser's print functionality (Ctrl+P or Cmd+P)
3. Select "Save as PDF" as the destination
4. Click "Save" or "Print"

### Method 3: Using Online Tools

Several online tools can convert Markdown to PDF:
- [MarkdownToPDF.com](https://www.markdowntopdf.com/)
- [CloudConvert](https://cloudconvert.com/md-to-pdf)
- [Dillinger.io](https://dillinger.io/) (Export to PDF) 