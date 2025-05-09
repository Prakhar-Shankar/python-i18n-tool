#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CI/CD Demo Script for i18n-checker
----------------------------------

This script demonstrates how the i18n-checker can be integrated into a CI/CD pipeline
for automated internationalization validation.

Usage:
    python demo_cicd.py

This will:
1. Scan a sample codebase for i18n issues
2. Generate an HTML report
3. Simulate a CI/CD pipeline validation step
"""

import os
import sys
import time
import argparse
from datetime import datetime
from i18n_checker.checker import run_checker

def print_with_color(message, color):
    """Print message with color."""
    colors = {
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'purple': '\033[95m',
        'cyan': '\033[96m',
        'end': '\033[0m'
    }
    print(f"{colors.get(color, '')}{message}{colors['end']}")

def simulate_cicd_pipeline():
    """Simulate a CI/CD pipeline for demonstration purposes."""
    print_with_color("\n===== CI/CD PIPELINE DEMONSTRATION =====", "blue")
    print_with_color("Starting i18n validation in CI/CD pipeline...", "blue")
    
    # Step 1: Prepare environment
    print_with_color("\n[STEP 1/5] Preparing environment...", "cyan")
    time.sleep(1)
    print("→ Checking for test code directory...")
    if not os.path.exists("test_code"):
        print_with_color("  ✗ Test code directory not found!", "red")
        return False
    print_with_color("  ✓ Test code directory found", "green")
    
    # Step 2: Set up args for the i18n checker
    print_with_color("\n[STEP 2/5] Setting up i18n checker...", "cyan")
    time.sleep(1)
    
    class Args:
        def __init__(self):
            self.scan = './test_code'
            self.fix = True
            self.output = 'ci_cd_report.html'
            self.format = 'html'
    
    args = Args()
    print_with_color("  ✓ i18n checker configured", "green")
    
    # Step 3: Run the checker
    print_with_color("\n[STEP 3/5] Running i18n validation...", "cyan")
    time.sleep(1)
    print("→ Scanning for i18n issues...")
    
    start_time = time.time()
    try:
        result = run_checker(args)
        duration = time.time() - start_time
        if result:
            print_with_color(f"  ✓ Scan completed in {duration:.2f} seconds", "green")
        else:
            print_with_color("  ✗ Scan failed!", "red")
            return False
    except Exception as e:
        print_with_color(f"  ✗ Error during scan: {str(e)}", "red")
        return False
    
    # Step 4: Analyze results
    print_with_color("\n[STEP 4/5] Analyzing results...", "cyan")
    time.sleep(1)
    
    # Handle missing_keys which could be a dict or a set
    missing_keys = result.get('missing_keys', {})
    unused_keys = result.get('unused_keys', set())
    
    # Calculate total missing keys based on the data structure
    if isinstance(missing_keys, dict):
        total_missing = sum(len(keys) for keys in missing_keys.values())
    elif isinstance(missing_keys, set):
        total_missing = len(missing_keys)
    else:
        # Fallback for any other type
        total_missing = len(list(missing_keys)) if hasattr(missing_keys, '__len__') else 0
    
    # For unused keys (also handle both possible data structures)
    if isinstance(unused_keys, dict):
        total_unused = sum(len(keys) for keys in unused_keys.values())
    else:
        total_unused = len(unused_keys)
    
    print(f"→ Found {total_missing} missing keys and {total_unused} unused keys")
    
    # Determine if this would pass or fail in a real CI pipeline
    threshold = 5  # Increased threshold for demonstration purposes
    if total_missing > threshold:
        print_with_color(f"  ✗ Too many missing keys (threshold: {threshold})", "red")
        status = "failed"
    else:
        print_with_color(f"  ✓ Missing keys within acceptable threshold", "green")
        status = "passed"
    
    # Step 5: Generate report artifact
    print_with_color("\n[STEP 5/5] Generating artifacts...", "cyan")
    time.sleep(1)
    
    if os.path.exists(args.output):
        print_with_color(f"  ✓ Report generated at: {args.output}", "green")
        report_size = os.path.getsize(args.output) / 1024  # KB
        print(f"    Report size: {report_size:.2f} KB")
    else:
        print_with_color(f"  ✗ Failed to generate report at: {args.output}", "red")
    
    # Final CI/CD status
    print_with_color("\n===== CI/CD PIPELINE RESULT =====", "blue")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if status == "passed":
        print_with_color(f"✅ BUILD PASSED | {timestamp}", "green")
        print_with_color("i18n validation successful. Report artifact generated.", "green")
    else:
        print_with_color(f"❌ BUILD FAILED | {timestamp}", "red")
        print_with_color("i18n validation failed. Too many i18n issues found.", "red")
        print_with_color("Please fix the issues and try again.", "red")
    
    return status == "passed"

if __name__ == "__main__":
    success = simulate_cicd_pipeline()
    sys.exit(0 if success else 1) 