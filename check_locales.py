import argparse
import os
import json

def find_json_files(directory):
    """Recursively find all JSON files in the given directory."""
    json_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".json"):
                json_files.append(os.path.join(root, file))
    return json_files

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
            keys.update(extract_nested_keys(value, full_key))  # Recursion for nested objects
    elif isinstance(data, list):
        for i, item in enumerate(data):
            keys.update(extract_nested_keys(item, f"{parent_key}[{i}]"))
    return keys

def main():
    parser = argparse.ArgumentParser(description="i18n Key Management Tool")
    parser.add_argument("--scan", help="Path to the codebase to scan", required=True)
    args = parser.parse_args()

    if not os.path.exists(args.scan):
        print(f"Error: Directory {args.scan} does not exist!")
        return

    print(f"📂 Scanning directory: {args.scan}")

    # Find all JSON files
    json_files = find_json_files(args.scan)

    if json_files:
        print(f"✅ Found {len(json_files)} JSON file(s):")
        all_keys = set()
        for file in json_files:
            print(f"🔍 Extracting keys from: {file}")
            keys = extract_keys_from_json(file)
            all_keys.update(keys)

        print("\n📌 Extracted JSON keys:")
        for key in sorted(all_keys):
            print(f" - {key}")

    else:
        print("⚠️ No JSON files found.")

if __name__ == "__main__":
    main()
