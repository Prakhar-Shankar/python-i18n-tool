#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Command-line interface for i18n-checker.

This module provides the entry point for the i18n-checker tool when called from the command line.
"""

import argparse
import sys
from i18n_checker.checker import run_checker

def main():
    """
    Main entry point for the i18n-checker command-line tool.
    
    Parses command-line arguments and runs the checker.
    """
    parser = argparse.ArgumentParser(
        description="i18n Key Management Tool - Detects missing and unused localization keys"
    )
    parser.add_argument(
        "--scan", 
        help="Path to the codebase to scan", 
        required=True
    )
    parser.add_argument(
        "--fix", 
        help="Generate suggestions to fix missing keys", 
        action="store_true"
    )
    parser.add_argument(
        "--output", 
        help="Output file for detailed report (default: i18n_report.txt)"
    )
    parser.add_argument(
        "--format", 
        help="Output format: txt or html (default: txt)", 
        choices=["txt", "html"], 
        default="txt"
    )
    
    args = parser.parse_args()
    
    # Run the checker with the provided arguments
    result = run_checker(args)
    
    # Return success if result is not None
    return 0 if result is not None else 1

if __name__ == "__main__":
    sys.exit(main()) 