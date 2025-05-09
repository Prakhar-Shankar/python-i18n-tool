#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
i18n Key Management Tool
------------------------

This script helps manage internationalization (i18n) keys by scanning a codebase to:
1. Identify keys used in code but missing in translation files
2. Identify keys in translation files that are not used in code
3. Provide suggestions to fix missing keys
4. Generate detailed reports about i18n key usage

Supported file types:
- Code: Python (.py), JavaScript (.js), TypeScript (.ts), Vue (.vue)
- Translations: JSON (.json)
"""

import argparse
import os
import json
import re
from collections import defaultdict
from typing import Dict, Set, List, Tuple


def find_files(directory, extensions):
    """
    Find all files with given extensions in the directory.
    
    Args:
        directory (str): Directory to scan
        extensions (str or tuple): File extensions to match
        
    Returns:
        list: List of file paths matching the extensions
    """
    found_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(extensions):
                found_files.append(os.path.join(root, file))
    return found_files

def extract_keys_from_json(file_path, parent_key=""):
    """
    Extract all keys from a JSON file, including nested keys.
    
    Args:
        file_path (str): Path to the JSON file
        parent_key (str): Parent key for nested objects
        
    Returns:
        set: Set of all keys in the JSON file
    """
    keys = set()
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            keys = extract_nested_keys(data, parent_key)
    except json.JSONDecodeError:
        print(f"⚠️ Error: Could not parse {file_path}. Skipping...")
    return keys

def extract_nested_keys(data, parent_key=""):
    """
    Recursively extract nested keys from a dictionary.
    
    Args:
        data: Dictionary, list or primitive to extract keys from
        parent_key (str): Parent key for nested objects
        
    Returns:
        set: Set of extracted keys
    """
    keys = set()
    if isinstance(data, dict):
        for key, value in data.items():
            full_key = f"{parent_key}.{key}" if parent_key else key
            keys.add(full_key)
            keys.update(extract_nested_keys(value, full_key))
    elif isinstance(data, list):
        for i, item in enumerate(data):
            keys.update(extract_nested_keys(item, f"{parent_key}[{i}]"))
    return keys

def determine_language_from_path(file_path):
    """
    Determine the language from the file path.
    
    Args:
        file_path (str): Path to the file
        
    Returns:
        str: Detected language code
    """
    # Try to find language code in the path
    file_base = os.path.basename(file_path)
    file_dir = os.path.dirname(file_path)
    
    # Check if the filename itself is a language code (e.g., en.json, fr.json)
    lang_match = re.match(r'([a-z]{2})(_[A-Z]{2})?\.', file_base)
    if lang_match:
        return lang_match.group(1)
    
    # Check if a parent directory is a language code
    path_parts = file_dir.split(os.path.sep)
    for part in reversed(path_parts):
        if re.match(r'^[a-z]{2}(_[A-Z]{2})?$', part):
            return part
    
    # Default to "unknown" if we can't determine
    return "unknown"

def extract_used_keys_from_python(file_path):
    """
    Extract i18n keys used in Python files (e.g., _('greeting'), gettext('user.name')).
    
    Args:
        file_path (str): Path to the Python file
        
    Returns:
        dict: Dictionary mapping keys to their locations in the file
    """
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

def extract_used_keys_from_js_ts(file_path):
    """
    Extract 
      keys used in JavaScript/TypeScript files.
    
    Patterns detected:
    - t("key") or t('key')
    - t.namespace("key")
    - t({ key: "value" })
    - this.$t("key") (Vue)
    
    Args:
        file_path (str): Path to the JS/TS file
        
    Returns:
        dict: Dictionary mapping keys to their locations in the file
    """
    key_patterns = [
        r't\(["\']([^"\']+)["\']\)',  # Matches t("key") or t('key')
        r't\.\w+\(["\']([^"\']+)["\']\)',  # Matches t.namespace("key")
        r't\(\{.*?["\']key["\']:\s*["\']([^"\']+)["\'].*?\}\)',  # Matches t({ key: "value" })
        r'this.\$t\(["\']([^"\']+)["\']\)',  # Matches Vue's this.$t("key")
    ]

    used_keys = {}
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, 1):
                for pattern in key_patterns:
                    matches = re.findall(pattern, line)
                    for key in matches:
                        if key not in used_keys:
                            used_keys[key] = []
                        used_keys[key].append((file_path, line_num, line.strip()))
    except Exception as e:
        print(f"⚠️ Error reading {file_path}: {e}")

    return used_keys

def extract_used_keys_from_vue(file_path):
    """
    Extract i18n keys used in Vue files.
    
    Patterns detected:
    - $t('key') or $t("key")
    - t('key') or t("key")
    - i18n.t('key')
    
    Args:
        file_path (str): Path to the Vue file
        
    Returns:
        dict: Dictionary mapping keys to their locations in the file
    """
    key_patterns = [
        r'\$t\(["\']([^"\']+)["\']\)',  # Matches $t("key") or $t('key')
        r't\(["\']([^"\']+)["\']\)',    # Matches t("key") or t('key')
        r'i18n\.t\(["\']([^"\']+)["\']\)',  # Matches i18n.t("key")
    ]
    
    used_keys = {}
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, 1):
                for pattern in key_patterns:
                    matches = re.findall(pattern, line)
                    for key in matches:
                        if key not in used_keys:
                            used_keys[key] = []
                        used_keys[key].append((file_path, line_num, line.strip()))
    except Exception as e:
        print(f"⚠️ Error reading {file_path}: {e}")
        
    return used_keys

def find_json_key_locations(json_files: List[str]) -> Dict[str, List[Tuple[str, str]]]:
    """
    Find which JSON files contain each key.
    
    Args:
        json_files (List[str]): List of JSON file paths
        
    Returns:
        Dict[str, List[Tuple[str, str]]]: Dictionary mapping keys to tuples of (file_path, language)
    """
    key_locations = defaultdict(list)
    
    for file_path in json_files:
        try:
            language = determine_language_from_path(file_path)
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                keys = extract_nested_keys(data)
                for key in keys:
                    key_locations[key].append((file_path, language))
        except json.JSONDecodeError:
            print(f"⚠️ Error: Could not parse {file_path}. Skipping...")
            
    return key_locations

def suggest_fix_for_missing_key(key: str, json_files: List[str]) -> Dict[str, str]:
    """
    Suggest a fix for missing keys by creating placeholder entries.
    
    Args:
        key (str): The missing key
        json_files (List[str]): List of JSON file paths
        
    Returns:
        Dict[str, str]: Dictionary mapping file paths to suggested JSON content
    """
    suggestions = {}
    
    # Find best JSON file to add the key to
    target_file = None
    for file in json_files:
        if file.endswith("en.json"):  # Prefer English as base language
            target_file = file
            break
    
    if not target_file and json_files:
        target_file = json_files[0]  # Use first available if no English
        
    if not target_file:
        return suggestions
        
    # Create a placeholder value
    if "." in key:
        parts = key.split(".")
        nested_obj = {}
        current = nested_obj
        
        for i, part in enumerate(parts):
            if i == len(parts) - 1:
                current[part] = f"MISSING: {key}"
            else:
                current[part] = {}
                current = current[part]
                
        suggestions[target_file] = json.dumps(nested_obj, indent=4)
    else:
        suggestions[target_file] = f'{{ "{key}": "MISSING: {key}" }}'
        
    return suggestions

def generate_html_report(missing_keys, unused_keys, used_keys, json_key_locations, missing_key_suggestions, fix_missing):
    """
    Generate an HTML report with tabular format.
    
    Args:
        missing_keys (Set[str]): Keys used in code but missing in translations
        unused_keys (Set[str]): Keys in translations but not used in code
        used_keys (Dict): Dictionary of used keys with their locations
        json_key_locations (Dict): Dictionary of JSON keys with their locations
        missing_key_suggestions (Dict): Dictionary of suggested fixes
        fix_missing (bool): Whether fix suggestions are enabled
        
    Returns:
        str: HTML content for the report
    """
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>i18n Internationalization Report</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        h1, h2 {
            color: #2c3e50;
        }
        .container {
            background-color: #fff;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
        }
        th, td {
            padding: 10px;
            text-align: left;
            border: 1px solid #ddd;
        }
        th {
            background-color: #0e293c;
            color: white;
        }
        tr:nth-child(even) {
            background-color: #f2f2f2;
        }
        .key-path {
            color: #2ecc71;
            font-family: monospace;
        }
        .file-path {
            color: #3498db;
            font-family: monospace;
        }
        .language-tag {
            display: inline-block;
            padding: 2px 6px;
            background-color: #e0f2f1;
            border-radius: 4px;
            font-size: 0.9em;
            color: #00897b;
        }
        .suggestion {
            background-color: #fff8e1;
            border-left: 4px solid #ffc107;
            padding: 10px;
            margin: 10px 0;
            font-family: monospace;
            white-space: pre;
            overflow-x: auto;
        }
        .none-found {
            color: green;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <h1>i18n Internationalization Report</h1>
    
    <div class="container">
        <h2>🚨 Missing Keys (Used in Code but Not in JSON)</h2>
"""
    
    # Missing keys table
    if missing_keys:
        html_content += """
        <table>
            <thead>
                <tr>
                    <th>(index)</th>
                    <th>path</th>
                    <th>line</th>
                    <th>file</th>
                    <th>language</th>
                </tr>
            </thead>
            <tbody>
"""
        
        for i, key in enumerate(sorted(missing_keys)):
            for j, (file_path, line_num, _) in enumerate(used_keys[key]):
                # For each occurrence determine language from file extension/path
                file_ext = os.path.splitext(file_path)[1]
                lang = ""
                if file_ext == ".py":
                    lang = "Python"
                elif file_ext == ".js":
                    lang = "JavaScript"
                elif file_ext == ".ts":
                    lang = "TypeScript"
                elif file_ext == ".vue":
                    lang = "Vue"
                
                html_content += f"""
                <tr>
                    <td>{i if j==0 else ''}</td>
                    <td class="key-path">'{key}'</td>
                    <td>{line_num}</td>
                    <td class="file-path">'{file_path}'</td>
                    <td><span class="language-tag">{lang}</span></td>
                </tr>"""
        
        html_content += """
            </tbody>
        </table>
"""

        # Add suggestions if enabled
        if fix_missing:
            html_content += "<h3>Suggestions to Fix Missing Keys</h3>"
            for key in sorted(missing_keys):
                if key in missing_key_suggestions:
                    for file_path, json_content in missing_key_suggestions[key].items():
                        html_content += f"""
        <div>
            <p>For key <code class="key-path">{key}</code>, add to <code class="file-path">{file_path}</code>:</p>
            <div class="suggestion">{json_content}</div>
        </div>"""
    else:
        html_content += '<p class="none-found">✅ No missing keys found!</p>'
    
    # Unused keys section
    html_content += """
    </div>
    
    <div class="container">
        <h2>🗑️ Unused Keys (Present in JSON but Not Used in Code)</h2>
"""
    
    if unused_keys:
        html_content += """
        <table>
            <thead>
                <tr>
                    <th>(index)</th>
                    <th>key</th>
                    <th>file</th>
                    <th>language</th>
                </tr>
            </thead>
            <tbody>
"""
        
        for i, key in enumerate(sorted(unused_keys)):
            for j, (file_path, language) in enumerate(json_key_locations.get(key, [("Unknown", "unknown")])):
                html_content += f"""
                <tr>
                    <td>{i if j==0 else ''}</td>
                    <td class="key-path">'{key}'</td>
                    <td class="file-path">'{file_path}'</td>
                    <td><span class="language-tag">{language}</span></td>
                </tr>"""
        
        html_content += """
            </tbody>
        </table>
"""
    else:
        html_content += '<p class="none-found">✅ No unused keys found!</p>'
    
    html_content += """
    </div>
</body>
</html>
"""
    
    return html_content

def run_checker(args=None):
    """
    Main function that coordinates the scanning and reporting process.
    
    Args:
        args: Command line arguments (optional, for programmatic use)
        
    Returns:
        dict: Results containing missing and unused keys
    """
    if args is None:
        parser = argparse.ArgumentParser(description="i18n Key Management Tool")
        parser.add_argument("--scan", help="Path to the codebase to scan", required=True)
        parser.add_argument("--fix", help="Generate suggestions to fix missing keys", action="store_true")
        parser.add_argument("--output", help="Output file for detailed report (default: i18n_report.txt)")
        parser.add_argument("--format", help="Output format: txt or html (default: txt)", choices=["txt", "html"], default="txt")
        args = parser.parse_args()

    scan_dir = args.scan
    output_file = args.output if args.output else f"i18n_report.{args.format}"
    fix_missing = args.fix
    output_format = args.format

    if not os.path.exists(scan_dir):
        print(f"Error: Directory {scan_dir} does not exist!")
        return None

    print(f"📂 Scanning directory: {scan_dir}")

    # Scan JSON files
    json_files = find_files(scan_dir, ".json")
    all_json_keys = set()
    
    if json_files:
        print(f"✅ Found {len(json_files)} JSON file(s):")
        for file in json_files:
            print(f"🔍 Extracting keys from: {file}")
            keys = extract_keys_from_json(file)
            all_json_keys.update(keys)
    
    # Find which JSON file contains each key
    json_key_locations = find_json_key_locations(json_files)

    # Scan Python files
    python_files = find_files(scan_dir, ".py")
    python_files = [file for file in python_files if os.path.basename(file) != "check_locales.py" and "i18n_checker" not in file]
    
    used_keys = {}  # Dictionary mapping keys to where they're used
    
    if python_files:
        print(f"\n🐍 Scanning {len(python_files)} Python file(s) for used i18n keys:")
        for file in python_files:
            print(f"🔎 Checking: {file}")
            keys = extract_used_keys_from_python(file)
            for key, locations in keys.items():
                if key not in used_keys:
                    used_keys[key] = []
                used_keys[key].extend(locations)

    # Scan JS/TS files
    js_ts_files = find_files(scan_dir, (".js", ".ts"))

    if js_ts_files:
        print(f"\n📜 Scanning {len(js_ts_files)} JavaScript/TypeScript file(s) for used i18n keys:")
        for file in js_ts_files:
            print(f"🔎 Checking: {file}")
            keys = extract_used_keys_from_js_ts(file)
            for key, locations in keys.items():
                if key not in used_keys:
                    used_keys[key] = []
                used_keys[key].extend(locations)
    
    # Scan Vue files
    vue_files = find_files(scan_dir, ".vue")
    
    if vue_files:
        print(f"\n🖼️ Scanning {len(vue_files)} Vue file(s) for used i18n keys:")
        for file in vue_files:
            print(f"🔎 Checking: {file}")
            keys = extract_used_keys_from_vue(file)
            for key, locations in keys.items():
                if key not in used_keys:
                    used_keys[key] = []
                used_keys[key].extend(locations)

    # Compare JSON keys and used keys
    used_key_set = set(used_keys.keys())
    missing_keys = used_key_set - all_json_keys
    unused_keys = all_json_keys - used_key_set

    # Generate missing key suggestions if requested
    missing_key_suggestions = {}
    if fix_missing and missing_keys:
        for key in missing_keys:
            missing_key_suggestions[key] = suggest_fix_for_missing_key(key, json_files)

    # Generate report based on format
    if output_format == "html":
        # Generate HTML report
        html_content = generate_html_report(
            missing_keys,
            unused_keys,
            used_keys,
            json_key_locations,
            missing_key_suggestions,
            fix_missing
        )
        
        with open(output_file, "w", encoding="utf-8") as report:
            report.write(html_content)
    else:
        # Generate text report (default)
        with open(output_file, "w", encoding="utf-8") as report:
            report.write("======================================================\n")
            report.write("          i18n INTERNATIONALIZATION REPORT            \n")
            report.write("======================================================\n\n")

            # Missing keys section
            report.write("🚨 MISSING KEYS (Used in Code but Not in JSON):\n")
            report.write("------------------------------------------------------\n")
            if missing_keys:
                for key in sorted(missing_keys):
                    report.write(f"❌ Missing Key: {key}\n")
                    report.write(f"   Used in:\n")
                    for file_path, line_num, line_content in used_keys[key]:
                        report.write(f"   - {file_path}:{line_num} -> {line_content}\n")
                    
                    if fix_missing and key in missing_key_suggestions:
                        report.write("\n   Suggestion to fix:\n")
                        for file_path, json_content in missing_key_suggestions[key].items():
                            report.write(f"   Add to {file_path}:\n{json_content}\n")
                    report.write("\n")
            else:
                report.write("✅ No missing keys found!\n\n")

            # Unused keys section
            report.write("🗑️ UNUSED KEYS (Present in JSON but Not Used in Code):\n")
            report.write("------------------------------------------------------\n")
            if unused_keys:
                for key in sorted(unused_keys):
                    report.write(f"⚠️ Unused Key: {key}\n")
                    report.write(f"   Defined in:\n")
                    for file_path, lang in json_key_locations.get(key, [("Unknown", "unknown")]):
                        report.write(f"   - {file_path} ({lang})\n")
                    report.write("\n")
            else:
                report.write("✅ No unused keys found!\n\n")

    # Display summary to console
    print("\n🚨 Missing Keys (Used in Code but Not in JSON):")
    if missing_keys:
        for key in sorted(missing_keys):
            print(f" ❌ {key}")
            # Print first occurrence
            if key in used_keys and used_keys[key]:
                file_path, line_num, _ = used_keys[key][0]
                print(f"    First seen in: {file_path}:{line_num}")
    else:
        print(" ✅ None!")

    print("\n🗑️ Unused Keys (Present in JSON but Not Used in Code):")
    if unused_keys:
        for key in sorted(unused_keys):
            print(f" ⚠️ {key}")
            # Print where it's defined
            if key in json_key_locations:
                for file_path, lang in json_key_locations[key][:1]:  # Just show first file
                    print(f"    Defined in: {file_path} ({lang})")
    else:
        print(" ✅ None!")
        
    print(f"\n📝 Detailed report written to: {output_file}")
    
    return {
        "missing_keys": missing_keys,
        "unused_keys": unused_keys,
        "used_keys": used_keys,
        "json_key_locations": json_key_locations
    }   