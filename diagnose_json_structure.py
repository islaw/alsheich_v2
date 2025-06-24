import json
import os

def inspect_json_structure(file_path):
    """
    Inspects and prints the structure of a JSON file, focusing on keys
    at different levels to understand its schema.
    """
    print(f"--- Inspecting JSON structure of: {file_path} ---")

    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from {file_path}: {e}")
            return

    # Inspect top-level keys
    if isinstance(data, dict):
        print("\nTop-level keys:")
        print(list(data.keys()))

        # Inspect keys of the first page object, if 'pages' exists and is a list
        if 'pages' in data and isinstance(data['pages'], list) and data['pages']:
            first_page = data['pages'][0]
            if isinstance(first_page, dict):
                print("\nKeys in the first page object:")
                print(list(first_page.keys()))

                # Inspect keys of the first line object in the first page
                if 'lines' in first_page and isinstance(first_page['lines'], list) and first_page['lines']:
                    first_line = first_page['lines'][0]
                    if isinstance(first_line, dict):
                        print("\nKeys in the first line object of the first page:")
                        print(list(first_line.keys()))

    elif isinstance(data, list) and data:
        print("\nJSON is a list. Keys of the first object in the list:")
        first_item = data[0]
        if isinstance(first_item, dict):
            print(list(first_item.keys()))
    else:
        print(f"\nJSON content is of type {type(data)} and could not be inspected for keys.")

    print("\n--- Inspection Finished ---")


if __name__ == "__main__":
    # Corrected file path to point to the raw ground truth from Document AI
    # This is the authoritative source for comparison.
    file_to_inspect = 'downloaded_json_parts/full_ground_truth_protocol-0.json'
    inspect_json_structure(file_to_inspect)