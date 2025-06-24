import os
import difflib

# --- הגדרות ---
# הנתיבים לקבצים שנוצרו בריצה האחרונה (סבב 7)
REPORTS_DIR = "truth_test/test_harness_results/reports/"
BASE_FILENAME = "round7_chunk0_model_gemini-2_5-pro_prompt_v2.2.1_include_empty_lines"

EXPECTED_FILE = os.path.join(REPORTS_DIR, f"{BASE_FILENAME}_expected_content.txt")
ACTUAL_FILE = os.path.join(REPORTS_DIR, f"{BASE_FILENAME}_actual_content.txt")
DIFF_REPORT_FILE = os.path.join(REPORTS_DIR, f"{BASE_FILENAME}_diff_report.html")
# ----------------

def main():
    print("--- Starting Detailed Text Comparison ---")

    try:
        with open(EXPECTED_FILE, 'r', encoding='utf-8') as f:
            expected_text = f.read()
        with open(ACTUAL_FILE, 'r', encoding='utf-8') as f:
            actual_text = f.read()
    except FileNotFoundError as e:
        print(f"CRITICAL ERROR: Could not find input text file. {e}")
        return

    # פיצול הטקסט לשורות לצורך ההשוואה
    expected_lines = expected_text.splitlines()
    actual_lines = actual_text.splitlines()

    # יצירת דוח ההבדלים בפורמט HTML
    html_diff = difflib.HtmlDiff(wrapcolumn=80).make_file(
        expected_lines,
        actual_lines,
        fromdesc='Expected (Ground Truth)',
        todesc='Actual (Model Output)'
    )

    try:
        with open(DIFF_REPORT_FILE, 'w', encoding='utf-8') as f:
            f.write(html_diff)
        print(f"\nSUCCESS: Detailed comparison report saved to:")
        print(DIFF_REPORT_FILE)
        print("\nPlease open this HTML file in a web browser to see the differences.")
    except IOError as e:
        print(f"CRITICAL ERROR: Could not write HTML report file. {e}")

    print("\n--- Comparison Finished ---")


if __name__ == "__main__":
    main()