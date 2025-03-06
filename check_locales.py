import argparse
import os
import json
import re

def find_files(directory, extensions):
    """Find all files with given extensions in the directory."""
    found_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(extensions):
                found_files.append(os.path.join(root, file))
    return found_files

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

def extract_nested_keys(data, parent_key=""):
    """Recursively extract nested keys from a dictionary."""
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

def extract_used_keys_from_python(file_path):
    """Extract i18n keys used in Python files (e.g., _('greeting'), gettext('user.name'))."""
    key_pattern = re.compile(r'_\(["\']([^"\']+)["\']\)|gettext\(["\']([^"\']+)["\']\)')
    used_keys = set()

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                matches = key_pattern.findall(line)
                for match in matches:
                    key = match[0] if match[0] else match[1]
                    used_keys.add(key)
    except Exception as e:
        print(f"⚠️ Error reading {file_path}: {e}")
    
    return used_keys

def main():
    parser = argparse.ArgumentParser(description="i18n Key Management Tool")
    parser.add_argument("--scan", help="Path to the codebase to scan", required=True)
    args = parser.parse_args()

    if not os.path.exists(args.scan):
        print(f"Error: Directory {args.scan} does not exist!")
        return

    print(f"📂 Scanning directory: {args.scan}")

    # Find all JSON files
    json_files = find_files(args.scan, ".json")
    all_json_keys = set()

    if json_files:
        print(f"✅ Found {len(json_files)} JSON file(s):")
        for file in json_files:
            print(f"🔍 Extracting keys from: {file}")
            keys = extract_keys_from_json(file)
            all_json_keys.update(keys)

    # Find all Python files
    python_files = find_files(args.scan, ".py")
    python_files = python_files = [file for file in python_files if os.path.basename(file) != "check_locales.py"]
    used_keys = set()

    if python_files:
        print(f"\n🐍 Scanning {len(python_files)} Python file(s) for used i18n keys:")
        for file in python_files:
            print(f"🔎 Checking: {file}")
            keys = extract_used_keys_from_python(file)
            used_keys.update(keys)

    # Compare JSON keys and used keys
    missing_keys = used_keys - all_json_keys
    unused_keys = all_json_keys - used_keys

    # Display results
    print("\n🚨 Missing Keys (Used in Code but Not in JSON):")
    if missing_keys:
        for key in sorted(missing_keys):
            print(f" ❌ {key}")
    else:
        print(" ✅ None!")

    print("\n🗑️ Unused Keys (Present in JSON but Not Used in Code):")
    if unused_keys:
        for key in sorted(unused_keys):
            print(f" ⚠️ {key}")
    else:
        print(" ✅ None!")

if __name__ == "__main__":
    main()
