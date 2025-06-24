import os
import json
import difflib

# --- הגדרות ---
TEST_ROUND = 8 # שימוש בנתונים מריצה 8
CHUNK_INDEX = 0
MODEL_NAME = "gemini-2.5-pro"
PROMPT_VERSION_IN_FILENAME = "v2.2.1_include_empty_lines"

# נתיבים
GROUND_TRUTH_DIR = "truth_test/truly_cleaned_parts/" 
OUTPUT_DIR_BASE = "truth_test/test_harness_results/"
# -------------------

def load_json_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"CRITICAL ERROR: File not found at '{path}'")
        return None
    except json.JSONDecodeError:
        print(f"CRITICAL ERROR: Failed to parse JSON file at '{path}'")
        return None

def get_structured_list_from_model(data):
    structured_list = []
    if not data or "pages" not in data:
        return []
    for page_data in data.get("pages", []):
        page_num = page_data.get("page_metadata", {}).get("visual_page_number", "N/A")
        if "error" in page_data:
            structured_list.append({"page": page_num, "line_num": "N/A", "text": f"MODEL_ERROR: {page_data['error']}"})
            continue
        for item in page_data.get("protocol_body", []):
            line_num = item.get("line_number", "N/A")
            text = item.get("text", "")
            speaker = item.get("speaker")
            if speaker:
                text = f"{speaker}: {text}"
            for i, sub_line in enumerate(text.splitlines()):
                current_line_num = line_num if i == 0 else "..."
                structured_list.append({"page": page_num, "line_num": current_line_num, "text": sub_line})
    return structured_list

def get_structured_list_from_gt(data):
    structured_list = []
    full_text = data.get('text', '')
    if not full_text: return []
    
    for page in data.get("pages", []):
        page_num = page.get("pageNumber")
        
        page_text_content = ""
        if 'layout' in page and 'textAnchor' in page['layout'] and 'textSegments' in page['layout']['textAnchor']:
             for segment in page['layout']['textAnchor']['textSegments']:
                start_index = int(segment.get('startIndex', 0))
                end_index = int(segment.get('endIndex', 0))
                page_text_content += full_text[start_index:end_index]

        page_text_lines = page_text_content.strip().split('\n')
        
        for line_content in page_text_lines:
            line_content = line_content.strip()
            if not line_content: continue
            
            line_num_str = "N/A"
            parts = line_content.split(maxsplit=1)
            if len(parts) > 1 and parts[0].isdigit() and len(parts[0]) <= 2:
                 line_num_str = parts[0]

            structured_list.append({"page": page_num, "line_num": line_num_str, "text": line_content})
            
    return structured_list

def generate_detailed_html_report(gt_list, model_list, report_path):
    html = """
    <html><head><style>
        body { font-family: Arial, sans-serif; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; vertical-align: top; font-family: 'Courier New', monospace; white-space: pre-wrap; }
        th { background-color: #f2f2f2; }
        .diff_add { background-color: #e6ffed; }
        .diff_sub { background-color: #ffebe9; }
        .context { color: #888; }
        .tag { font-weight: bold; }
    </style></head><body>
        <h2>Detailed Comparison Report</h2>
        <table>
            <tr><th>Tag</th><th>Page (GT)</th><th>Line (GT)</th><th>Expected (Ground Truth)</th>
                <th>Page (Model)</th><th>Line (Model)</th><th>Actual (Model Output)</th></tr>
    """
    
    matcher = difflib.SequenceMatcher(None, [d['text'] for d in gt_list], [d['text'] for d in model_list])

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'equal':
            for i in range(i1, i2):
                 html += f'<tr class="context"><td>{tag}</td><td>{gt_list[i]["page"]}</td><td>{gt_list[i]["line_num"]}</td><td>{gt_list[i]["text"]}</td><td>{model_list[i]["page"]}</td><td>{model_list[i]["line_num"]}</td><td>{model_list[i]["text"]}</td></tr>'
        else:
            if tag == 'replace' or tag == 'delete':
                for i in range(i1, i2):
                    html += f'<tr class="diff_sub"><td>{tag}</td><td>{gt_list[i]["page"]}</td><td>{gt_list[i]["line_num"]}</td><td>{gt_list[i]["text"]}</td><td></td><td></td><td></td></tr>'
            if tag == 'replace' or tag == 'insert':
                for j in range(j1, j2):
                     html += f'<tr class="diff_add"><td>{tag}</td><td></td><td></td><td></td><td>{model_list[j]["page"]}</td><td>{model_list[j]["line_num"]}</td><td>{model_list[j]["text"]}</td></tr>'

    html += "</table></body></html>"
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(html)

def main():
    print("--- Generating Detailed Report from Existing Data (difflib_v1.0) ---")

    base_filename = f"round{TEST_ROUND}_chunk{CHUNK_INDEX}_model_{MODEL_NAME.replace('.', '_')}_prompt_{PROMPT_VERSION_IN_FILENAME}"
    json_outputs_dir = os.path.join(OUTPUT_DIR_BASE, "json_outputs")
    
    model_output_path = os.path.join(json_outputs_dir, f"{base_filename}.json")
    
    gt_path = os.path.join(GROUND_TRUTH_DIR, f"TRULY_CLEANED_full_ground_truth_protocol-{CHUNK_INDEX}.json")
    report_path = os.path.join(OUTPUT_DIR_BASE, "reports", f"{base_filename}_difflib_v1.0_report.html")

    print(f"Loading model output from: {model_output_path}")
    model_output_raw = load_json_file(model_output_path)
    print(f"Loading ground truth from: {gt_path}")
    ground_truth_json = load_json_file(gt_path)

    if not model_output_raw or not ground_truth_json:
        print("Could not load necessary files. Aborting.")
        return

    print("Structuring data for detailed comparison...")
    gt_structured = get_structured_list_from_gt(ground_truth_json)
    model_structured = get_structured_list_from_model(model_output_raw)

    print("Generating detailed HTML report...")
    generate_detailed_html_report(gt_structured, model_structured, report_path)
    print(f"\nSUCCESS: Detailed report saved to:")
    print(report_path)

if __name__ == "__main__":
    main()