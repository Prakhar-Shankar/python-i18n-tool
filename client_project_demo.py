#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Client Project CI/CD Demo Script
--------------------------------

This script demonstrates how another project would use i18n-checker
in their CI/CD pipeline.

Usage:
    python client_project_demo.py
"""

import os
import sys
import time
import shutil
from datetime import datetime

# Colors for terminal output
colors = {
    'red': '\033[91m',
    'green': '\033[92m',
    'yellow': '\033[93m',
    'blue': '\033[94m',
    'purple': '\033[95m',
    'cyan': '\033[96m',
    'bold': '\033[1m',
    'end': '\033[0m'
}

def print_with_color(message, color):
    """Print message with color."""
    print(f"{colors.get(color, '')}{message}{colors['end']}")

def print_step(step, message):
    """Print a step header."""
    print_with_color(f"\n[STEP {step}] {message}", "cyan")
    time.sleep(0.5)

def simulate_client_cicd():
    """Simulate how a client project would use i18n-checker in CI/CD."""
    print_with_color("\n===== CLIENT PROJECT CI/CD DEMONSTRATION =====", "blue")
    print_with_color("This shows how another project would integrate i18n-checker into their workflow", "yellow")
    
    # Step 1: Project Setup
    print_step("1/5", "Setting up client project")
    print("→ Project structure:")
    print("  demo-client-project/")
    print("  ├── src/")
    print("  │   └── app.js         (JavaScript application with i18n keys)")
    print("  ├── locales/")
    print("  │   └── en.json        (English translations)")
    print("  ├── package.json       (Node.js project configuration)")
    print("  └── .github/workflows/")
    print("      └── i18n-validation.yml  (GitHub Actions workflow)")
    
    # Step 2: Examining the code
    print_step("2/5", "Examining project code")
    print("→ app.js contains several i18n keys:")
    
    keys = ["welcome.title", "welcome.message", "user.name", "user.email", "errors.unexpected"]
    for key in keys:
        print(f"  - {key}")
    
    print("\n→ Translation file (en.json) contains:")
    included_keys = ["welcome.title", "welcome.message", "user.name", "user.email", "buttons.save"]
    for key in included_keys:
        if key in keys:
            print_with_color(f"  ✓ {key}", "green")
        else:
            print(f"  - {key}")
    
    # Step 3: CI/CD Integration
    print_step("3/5", "CI/CD Integration")
    print("→ GitHub Actions workflow:")
    
    workflow_steps = [
        "1. Check out code repository",
        "2. Set up Python environment",
        "3. Install i18n-checker from PyPI",
        "4. Run i18n validation",
        "5. Check for critical issues",
        "6. Upload report as build artifact"
    ]
    
    for step in workflow_steps:
        print(f"  - {step}")
    
    # Step 4: Running i18n validation
    print_step("4/5", "Running i18n validation")
    print("→ Executing validation command:")
    print_with_color("  $ i18n-checker --scan . --format html --output client_i18n_report.html", "yellow")
    time.sleep(1)
    
    # Simulate results
    missing_key = "errors.unexpected"
    unused_key = "buttons.save"
    
    print("\n→ Validation results:")
    print_with_color(f"  ❌ Missing key: {missing_key}", "red")
    print(f"    Found in: src/app.js:21")
    print_with_color(f"  ⚠️ Unused key: {unused_key}", "yellow")
    
    # Step 5: CI/CD actions
    print_step("5/5", "CI/CD pipeline actions")
    
    # Determine if build should pass or fail based on thresholds
    threshold = 5
    missing_count = 1
    
    if missing_count > threshold:
        print_with_color(f"  ❌ Build failed: {missing_count} missing keys exceeds threshold of {threshold}", "red")
        status = "failed"
    else:
        print_with_color(f"  ✅ Build passed: {missing_count} missing keys is below threshold of {threshold}", "green")
        status = "passed"
    
    # Artifact creation
    print("\n→ Generated artifacts:")
    print_with_color(f"  📄 i18n validation report: client_i18n_report.html", "purple")
    
    # Create a simple HTML file for demo purposes
    with open("client_i18n_report.html", "w") as f:
        f.write("<html><body><h1>i18n Validation Report</h1>")
        f.write("<h2>Missing Keys (1)</h2><ul>")
        f.write(f'<li style="color:red">{missing_key} - src/app.js:21</li>')
        f.write("</ul><h2>Unused Keys (1)</h2><ul>")
        f.write(f'<li style="color:orange">{unused_key}</li>')
        f.write("</ul></body></html>")
    
    # Final status
    print_with_color("\n===== CI/CD PIPELINE RESULT =====", "blue")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if status == "passed":
        print_with_color(f"✅ BUILD PASSED | {timestamp}", "green")
        print_with_color("i18n validation successful. Minor issues found.", "green")
    else:
        print_with_color(f"❌ BUILD FAILED | {timestamp}", "red")
        print_with_color("i18n validation failed. Please fix missing keys.", "red")
    
    print("\n→ Next steps for the development team:")
    print("  1. Review the i18n report")
    print("  2. Add missing translations")
    print("  3. Remove unused keys if they're no longer needed")
    print("  4. Run validation again before merging")
    
    print_with_color("\nThis demonstrates how i18n-checker integrates into any project's CI/CD workflow", "yellow")
    
if __name__ == "__main__":
    simulate_client_cicd() 