# תוכנית ביצוע מפורטה - יום 1: מיגור הרעש ויצירת סט אמת
## מטרה: מ-50+ התרעות ל-<10 התרעות אמיתיות לכל עמוד
### 🔄 עודכנה לפי ביקורת מודלים 1 ו-3 - מאושרת לביצוע מיידי

---

## ✅ סטטוס אישור המודלים

**מודל 1**: ✅ מאושר - "ניתן לצאת לביצוע מיידי"  
**מודל 3**: ✅ מאושר - "אני מאשר את התוכנית וממליץ לצאת לביצוע מיידי"

**תיקונים שיושמו:**
- 🔧 הוסרה שגיאת "מוזס ← מילצ'ן" (טופלה ברמת הפרומפט)
- 🔧 עודכנה דוגמת הבדיקה לשגיאות אמיתיות ועדכניות
- 🔧 חוזק התיעוד הכמותי לבחירת שיטת חילוץ
- 🔧 נוסף ארגון קבצים ופקודות הרצה מרוכזות

---

## שלב 1.1: ניסוי PDF vs OCR (1 שעה)
**מטרה**: החלטה אמפירית על שיטת החילוץ האופטימלית

### 📋 חומרי גלם נדרשים:
- `full_ground_truth_protocol.pdf` (מקור)
- `protocol_images/page_1.jpg` (תמונה של עמוד 1)
- `downloaded_json_parts/full_ground_truth_protocol-0.json` (אמת מוחלטת לעמוד 1)

### 🔧 פעולות מדויקות:

#### 1.1.1 הכנת סקריפט בדיקה (15 דקות)
```bash
cd C:\Users\עידושיפוני\alsheich_v2
```

**📁 צור תיקיית עבודה:**
```bash
mkdir day1_execution
cd day1_execution
```

**צור קובץ: `pdf_vs_ocr_test.py`**
```python
import fitz  # PyMuPDF
import json
import os
from datetime import datetime

def extract_from_pdf(pdf_path, page_num=0):
    """חילוץ טקסט מעמוד PDF"""
    doc = fitz.open(pdf_path)
    page = doc[page_num]
    text = page.get_text()
    doc.close()
    return text

def load_ground_truth(gt_path):
    """טעינת אמת מוחלטת"""
    with open(gt_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def quick_comparison_metrics(text1, text2):
    """מדדי השוואה בסיסיים"""
    # ניקוי בסיסי לשם השוואה
    clean1 = ''.join(text1.split())
    clean2 = ''.join(text2.split())
    
    # חישוב דמיון בסיסי
    if len(clean2) == 0:
        return 0.0
    
    matching_chars = sum(1 for i, char in enumerate(clean1) 
                        if i < len(clean2) and char == clean2[i])
    
    similarity = matching_chars / max(len(clean1), len(clean2))
    
    return {
        'similarity_score': similarity,
        'pdf_length': len(text1),
        'gt_length': len(text2),
        'char_difference': abs(len(text1) - len(text2))
    }

def main():
    # קבצים לבדיקה
    pdf_path = "full_ground_truth_protocol.pdf"
    gt_path = "downloaded_json_parts/full_ground_truth_protocol-0.json"
    ocr_image_path = "protocol_images/page_1.jpg"  # לרפרנס
    
    # חילוץ מPDF
    pdf_text = extract_from_pdf(pdf_path, page_num=0)
    
    # טעינת אמת מוחלטת
    gt_data = load_ground_truth(gt_path)
    gt_text = gt_data.get('extracted_text', '')
    
    # השוואה
    comparison = quick_comparison_metrics(pdf_text, gt_text)
    
    # דוח
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report = {
        'timestamp': timestamp,
        'pdf_extraction': {
            'method': 'PyMuPDF direct',
            'text_sample': pdf_text[:200] + "...",
            'full_length': len(pdf_text)
        },
        'ground_truth': {
            'source': gt_path,
            'text_sample': gt_text[:200] + "...",
            'full_length': len(gt_text)
        },
        'comparison_metrics': comparison,
        'recommendation': 'PDF' if comparison['similarity_score'] > 0.8 else 'OCR'
    }
    
    # שמירת דוח
    with open(f'pdf_vs_ocr_test_report_{timestamp}.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"דוח נשמר: pdf_vs_ocr_test_report_{timestamp}.json")
    print(f"ציון דמיון: {comparison['similarity_score']:.2%}")
    print(f"המלצה: {report['recommendation']}")
    
    return report

if __name__ == "__main__":
    main()
```

#### 1.1.2 הרצת הבדיקה (5 דקות)
```bash
python pdf_vs_ocr_test.py
```

#### 1.1.3 ניתוח תוצאות והחלטה (10 דקות)
- **אם ציון דמיון > 80%**: המשך עם PDF
- **אם ציון דמיון < 80%**: המשך עם OCR התמונות הקיימות

**צור תיעוד מפורט: `extraction_method_decision.txt`**
```
=== החלטה על שיטת חילוץ ===
תאריך: 2025-06-24
שיטה נבחרת: [PDF/OCR]

נימוק כמותי:
• ציון דמיון מול GT: [X.X]%
• אורך טקסט PDF: [XXXX] תווים
• אורך GT: [XXXX] תווים
• הבדל באורך: [X.X]%

החלטה: נבחרה שיטת [PDF/OCR] בהתבסס על ציון הדמיון הגבוה.
```

---

## שלב 1.2: פיתוח noise_and_error_lexicon.py (2 שעות)
**מטרה**: לקסיקון מדויק עם דוגמאות אמיתיות מהדוח הקיים

### 📋 חומרי גלם נדרשים:
- דוח HTML: `truth_test/test_harness_results/reports/round49_chunk0_model_gemini-2.5-pro_prompt_main_extraction_prompt_v4.2_text_diff_report.html`
- קובץ השוואה קיים (לניתוח התבניות)

### 🔧 פעולות מדויקות:

#### 1.2.1 ניתוח הדוח הקיים (30 דקות)
**פתח את הדוח HTML ותעד באופן ידני:**

**רעש מזוהה (דוגמאות מהדוח האמיתי):**
- `עוייד` ← `עו"ד` 
- `אבייד` ← `אב"ד`
- `<<1>>`, `<<4>>`, `<ASA>`, `%2` (סמנים מערכתיים)
- רווחים מיותרים לפני/אחרי סימני פיסוק

**שגיאות קריטיות מזוהות:**
- `מוזס` ← `מילצ'ן` (שגיאת שם!)
- `פירר` ← `פויר` (שגיאת שם)
- `הגזמתי` ← `הזמנתי` (שגיאת הקשר)

#### 1.2.2 יצירת הלקסיקון (60 דקות)
**צור קובץ: `noise_and_error_lexicon.py`**
```python
"""
לקסיקון רעש ושגיאות למערכת השוואה אינטליגנטית
מבוסס על ניתוח אמפירי של דוחות השוואה קיימים
"""

import re
from typing import Dict, List, Tuple, Union
from dataclasses import dataclass

@dataclass
class ErrorPattern:
    pattern: Union[str, re.Pattern]
    category: str
    severity: str  # 'noise', 'minor', 'critical'
    description: str
    examples: List[Tuple[str, str]] = None

class NoiseAndErrorLexicon:
    def __init__(self):
        self.patterns = self._initialize_patterns()
    
    def _initialize_patterns(self) -> Dict[str, List[ErrorPattern]]:
        """אתחול מאגר התבניות על בסיס ניתוח דוחות אמיתיים"""
        
        return {
            # ========== רעש מותר - להתעלם ==========
            'allowed_noise': [
                ErrorPattern(
                    pattern=[("עוייד", "עו\"ד"), ("אבייד", "אב\"ד")],
                    category='quotes_normalization',
                    severity='noise',
                    description='החלפת ייי במירכאות',
                    examples=[("השופט עוייד", "השופט עו\"ד")]
                ),
                ErrorPattern(
                    pattern=re.compile(r'<<\d+>>'),
                    category='system_markers',
                    severity='noise',
                    description='מרקרים מספריים',
                    examples=[("טקסט<<1>>", "טקסט")]
                ),
                ErrorPattern(
                    pattern=re.compile(r'<[A-Z]+>'),
                    category='system_markers',
                    severity='noise',
                    description='תגיות מערכת באותיות גדולות',
                    examples=[("טקסט<ASA>", "טקסט")]
                ),
                ErrorPattern(
                    pattern=re.compile(r'%\d+'),
                    category='system_markers',
                    severity='noise',
                    description='מספורי אחוז',
                    examples=[("טקסט%2", "טקסט")]
                ),
                ErrorPattern(
                    pattern=re.compile(r'\s+'),
                    category='spacing_formatting',
                    severity='noise',
                    description='רווחים מרובים',
                    examples=[("מילה   מילה", "מילה מילה")]
                ),
                ErrorPattern(
                    pattern=re.compile(r'^\s+|\s+$'),
                    category='spacing_formatting',
                    severity='noise',
                    description='רווחים בקצוות השורה',
                    examples=[("  טקסט  ", "טקסט")]
                ),
                ErrorPattern(
                    pattern=re.compile(r'\n\s*\n'),
                    category='spacing_formatting',
                    severity='noise',
                    description='ירידות שורה ריקות',
                    examples=[("שורה1\n\nשורה2", "שורה1\nשורה2")]
                ),
                ErrorPattern(
                    pattern=re.compile(r':\s*'),
                    category='punctuation_spacing',
                    severity='noise',
                    description='רווח אחרי נקודתיים',
                    examples=[("שאלה :", "שאלה:")]
                )
            ],
            
            # ========== שגיאות קלות - לדיווח אבל לא חסימה ==========
            'minor_errors': [
                ErrorPattern(
                    pattern=re.compile(r'\d{2} :\d{2}'),
                    category='time_format',
                    severity='minor',
                    description='פורמט שעה שגוי',
                    examples=[("22 :30", "22:30")]
                ),
                ErrorPattern(
                    pattern=re.compile(r'[א-ת]+ [א-ת]+(?=\s*:)'),
                    category='speaker_formatting',
                    severity='minor',
                    description='פורמט דובר',
                    examples=[("השופט ברעם :", "השופט ברעם:")]
                )
            ],
            
            # ========== שגיאות קריטיות - חסימה מיידית ==========
            'critical_errors': [
                # הערה: שגיאת "מוזס ← מילצ'ן" הוסרה - טופלה ברמת הפרומפט (שגיאת פרשנות)
                ErrorPattern(
                    pattern=[
                        ("פירר", "פויר"),
                        ("נוית", "לילת"),
                        ("כרמל", "אליס")
                    ],
                    category='name_errors',
                    severity='critical',
                    description='שגיאות בשמות אנשים',
                    examples=[("מר פירר אמר", "מר פויר אמר")]
                ),
                ErrorPattern(
                    pattern=re.compile(r'\d{1,2}\.\d{1,2}\.\d{4}'),
                    category='date_errors',
                    severity='critical',
                    description='שגיאות בתאריכים',
                    examples=[("ביום 15.06.2024", "ביום 15.06.2025")]
                ),
                ErrorPattern(
                    pattern=re.compile(r'ת/\d+'),
                    category='case_number_errors',
                    severity='critical',
                    description='שגיאות במספרי תיק',
                    examples=[("תיק ת/1000", "תיק ת/2000")]
                ),
                ErrorPattern(
                    pattern=re.compile(r'\d{9}'),
                    category='id_number_errors',
                    severity='critical',
                    description='שגיאות במספרי תעודת זהות',
                    examples=[("ת.ז. 123456789", "ת.ז. 987654321")]
                ),
                ErrorPattern(
                    pattern=[
                        ("הגזמתי", "הזמנתי"),
                        ("מכירות", "מכירוח"),
                        ("ביטוח", "ביטות")
                    ],
                    category='context_errors',
                    severity='critical',
                    description='שגיאות הקשר משמעותיות',
                    examples=[("הגזמתי בדברים", "הזמנתי בדברים")]
                )
            ]
        }
    
    def get_pattern_by_category(self, category: str) -> List[ErrorPattern]:
        """החזרת תבניות לפי קטגוריה"""
        all_patterns = []
        for pattern_group in self.patterns.values():
            all_patterns.extend([p for p in pattern_group if p.category == category])
        return all_patterns
    
    def get_patterns_by_severity(self, severity: str) -> List[ErrorPattern]:
        """החזרת תבניות לפי רמת חומרה"""
        all_patterns = []
        for pattern_group in self.patterns.values():
            all_patterns.extend([p for p in pattern_group if p.severity == severity])
        return all_patterns
    
    def export_to_json(self, filename: str = None):
        """יצוא הלקסיקון לקובץ JSON"""
        import json
        from datetime import datetime
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"lexicon_export_{timestamp}.json"
        
        export_data = {}
        for group_name, patterns in self.patterns.items():
            export_data[group_name] = []
            for pattern in patterns:
                pattern_dict = {
                    'category': pattern.category,
                    'severity': pattern.severity,
                    'description': pattern.description,
                    'examples': pattern.examples or []
                }
                
                # טיפול בביטויים רגולריים
                if isinstance(pattern.pattern, re.Pattern):
                    pattern_dict['pattern'] = pattern.pattern.pattern
                    pattern_dict['pattern_type'] = 'regex'
                else:
                    pattern_dict['pattern'] = pattern.pattern
                    pattern_dict['pattern_type'] = 'literal'
                
                export_data[group_name].append(pattern_dict)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)
        
        print(f"לקסיקון יוצא לקובץ: {filename}")
        return filename

# יצירת מופע גלובלי
LEXICON = NoiseAndErrorLexicon()

if __name__ == "__main__":
    # בדיקה עצמית
    print("=== בדיקת לקסיקון רעש ושגיאות ===")
    
    # סטטיסטיקות
    noise_patterns = LEXICON.get_patterns_by_severity('noise')
    minor_patterns = LEXICON.get_patterns_by_severity('minor')
    critical_patterns = LEXICON.get_patterns_by_severity('critical')
    
    print(f"תבניות רעש: {len(noise_patterns)}")
    print(f"שגיאות קלות: {len(minor_patterns)}")
    print(f"שגיאות קריטיות: {len(critical_patterns)}")
    
    # יצוא לקובץ
    export_file = LEXICON.export_to_json()
    print(f"לקסיקון נשמר בקובץ: {export_file}")
```

#### 1.2.3 בדיקת הלקסיקון (30 דקות)
```bash
python noise_and_error_lexicon.py
```

**ודא שהפלט כולל:**
- מספר תבניות רעש: ~8
- מספר שגיאות קלות: ~2  
- מספר שגיאות קריטיות: ~6
- קובץ JSON מיוצא עם כל התבניות

---

## שלב 1.3: פיתוח intelligent_comparator.py (2 שעות)
**מטרה**: מנוע השוואה חכם שמחזיר JSON מפורט עם סיווג

### 🔧 פעולות מדויקות:

#### 1.3.1 יצירת המנוע הבסיסי (90 דקות)
**צור קובץ: `intelligent_comparator.py`**
```python
"""
מנוע השוואה אינטליגנטי לטקסטים משפטיים
מסווג הבדלים לרעש, שגיאות קלות ושגיאות קריטיות
"""

import re
import json
import difflib
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass, asdict
from datetime import datetime
from noise_and_error_lexicon import LEXICON

@dataclass
class DifferenceAnalysis:
    """ניתוח הבדל יחיד"""
    line_number: int
    ground_truth_text: str
    model_output_text: str
    difference_type: str  # 'noise', 'minor', 'critical', 'unknown'
    category: str
    severity_score: float  # 0.0 (רעש) עד 1.0 (קריטי)
    description: str
    confidence: float  # רמת ביטחון בסיווג
    requires_human_review: bool

@dataclass
class ComparisonResult:
    """תוצאת השוואה מלאה"""
    timestamp: str
    ground_truth_length: int
    model_output_length: int
    total_differences: int
    noise_filtered: List[DifferenceAnalysis]
    minor_issues: List[DifferenceAnalysis]
    critical_errors: List[DifferenceAnalysis]
    unknown_differences: List[DifferenceAnalysis]
    statistics: Dict[str, Any]
    auto_approvable: bool
    requires_manual_review: bool
    overall_confidence: float

class IntelligentTextComparator:
    def __init__(self, lexicon=None):
        self.lexicon = lexicon or LEXICON
        self.confidence_threshold = 0.8  # סף ביטחון לאישור אוטומטי
    
    def normalize_text_for_comparison(self, text: str) -> str:
        """נרמול טקסט לצורך השוואה בסיסית"""
        # הסרת רווחים מיותרים
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        # נרמול מירכאות
        text = text.replace('עוייד', 'עו"ד')
        text = text.replace('אבייד', 'אב"ד')
        
        # הסרת סמנים מערכתיים
        text = re.sub(r'<<\d+>>', '', text)
        text = re.sub(r'<[A-Z]+>', '', text)
        text = re.sub(r'%\d+', '', text)
        
        return text
    
    def classify_difference(self, gt_text: str, output_text: str, line_num: int) -> DifferenceAnalysis:
        """סיווג הבדל יחיד"""
        
        # בדיקה מול תבניות רעש
        for pattern in self.lexicon.get_patterns_by_severity('noise'):
            if self._matches_pattern(gt_text, output_text, pattern):
                return DifferenceAnalysis(
                    line_number=line_num,
                    ground_truth_text=gt_text,
                    model_output_text=output_text,
                    difference_type='noise',
                    category=pattern.category,
                    severity_score=0.1,
                    description=pattern.description,
                    confidence=0.9,
                    requires_human_review=False
                )
        
        # בדיקה מול שגיאות קריטיות
        for pattern in self.lexicon.get_patterns_by_severity('critical'):
            if self._matches_pattern(gt_text, output_text, pattern):
                return DifferenceAnalysis(
                    line_number=line_num,
                    ground_truth_text=gt_text,
                    model_output_text=output_text,
                    difference_type='critical',
                    category=pattern.category,
                    severity_score=1.0,
                    description=pattern.description,
                    confidence=0.95,
                    requires_human_review=True
                )
        
        # בדיקה מול שגיאות קלות
        for pattern in self.lexicon.get_patterns_by_severity('minor'):
            if self._matches_pattern(gt_text, output_text, pattern):
                return DifferenceAnalysis(
                    line_number=line_num,
                    ground_truth_text=gt_text,
                    model_output_text=output_text,
                    difference_type='minor',
                    category=pattern.category,
                    severity_score=0.5,
                    description=pattern.description,
                    confidence=0.8,
                    requires_human_review=False
                )
        
        # הבדל לא מזוהה - דורש בדיקה
        return DifferenceAnalysis(
            line_number=line_num,
            ground_truth_text=gt_text,
            model_output_text=output_text,
            difference_type='unknown',
            category='unclassified',
            severity_score=0.7,  # ערך ברירת מחדל בינוני
            description='הבדל לא מזוהה - דורש בדיקה ידנית',
            confidence=0.3,
            requires_human_review=True
        )
    
    def _matches_pattern(self, gt_text: str, output_text: str, pattern) -> bool:
        """בדיקה האם הבדל תואם לתבנית"""
        
        if isinstance(pattern.pattern, list):
            # רשימת החלפות ליטרליות
            for wrong, correct in pattern.pattern:
                if wrong in output_text and correct in gt_text:
                    return True
                if wrong in gt_text and correct in output_text:
                    return True
        
        elif isinstance(pattern.pattern, re.Pattern):
            # ביטוי רגולרי
            if pattern.pattern.search(gt_text) or pattern.pattern.search(output_text):
                return True
        
        return False
    
    def analyze_differences(self, ground_truth: str, model_output: str) -> ComparisonResult:
        """ניתוח מלא של הבדלים בין אמת מוחלטת לפלט מודל"""
        
        timestamp = datetime.now().isoformat()
        
        # פיצול לשורות
        gt_lines = ground_truth.strip().split('\n')
        output_lines = model_output.strip().split('\n')
        
        # יצירת ההבדלים הבסיסיים
        differ = difflib.unified_diff(gt_lines, output_lines, lineterm='')
        diff_lines = list(differ)
        
        # סיווג כל הבדל
        noise_filtered = []
        minor_issues = []
        critical_errors = []
        unknown_differences = []
        
        line_num = 0
        for line in diff_lines:
            if line.startswith('@@'):
                continue
            
            if line.startswith('-'):
                gt_text = line[1:].strip()
                output_text = ""
            elif line.startswith('+'):
                output_text = line[1:].strip()
                gt_text = ""
            else:
                continue
            
            line_num += 1
            analysis = self.classify_difference(gt_text, output_text, line_num)
            
            if analysis.difference_type == 'noise':
                noise_filtered.append(analysis)
            elif analysis.difference_type == 'minor':
                minor_issues.append(analysis)
            elif analysis.difference_type == 'critical':
                critical_errors.append(analysis)
            else:
                unknown_differences.append(analysis)
        
        # חישוב סטטיסטיקות
        total_differences = len(noise_filtered) + len(minor_issues) + len(critical_errors) + len(unknown_differences)
        
        if total_differences > 0:
            noise_reduction_percent = len(noise_filtered) / total_differences * 100
        else:
            noise_reduction_percent = 0
        
        significant_issues = len(critical_errors) + len(unknown_differences)
        auto_approvable = significant_issues == 0 and len(minor_issues) <= 2
        requires_manual_review = significant_issues > 0 or len(minor_issues) > 5
        
        # ציון ביטחון כללי
        if critical_errors:
            overall_confidence = 0.2
        elif unknown_differences:
            overall_confidence = 0.5
        elif minor_issues:
            overall_confidence = 0.8
        else:
            overall_confidence = 0.95
        
        statistics = {
            'noise_reduction_percent': noise_reduction_percent,
            'significant_issues_count': significant_issues,
            'accuracy_score': 1.0 - (significant_issues / max(total_differences, 1)),
            'processing_efficiency': len(noise_filtered) / max(total_differences, 1)
        }
        
        return ComparisonResult(
            timestamp=timestamp,
            ground_truth_length=len(ground_truth),
            model_output_length=len(model_output),
            total_differences=total_differences,
            noise_filtered=noise_filtered,
            minor_issues=minor_issues,
            critical_errors=critical_errors,
            unknown_differences=unknown_differences,
            statistics=statistics,
            auto_approvable=auto_approvable,
            requires_manual_review=requires_manual_review,
            overall_confidence=overall_confidence
        )
    
    def generate_report_json(self, comparison_result: ComparisonResult, output_file: str = None) -> str:
        """יצירת דוח JSON מפורט"""
        
        if not output_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"intelligent_comparison_report_{timestamp}.json"
        
        # המרה לדיקטיונרי
        report_data = asdict(comparison_result)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2)
        
        return output_file
    
    def generate_summary_report(self, comparison_result: ComparisonResult) -> str:
        """יצירת דוח סיכום קצר"""
        
        summary = f"""
=== דוח השוואה אינטליגנטית ===
זמן: {comparison_result.timestamp}

📊 סטטיסטיקות כלליות:
• סה"כ הבדלים זוהו: {comparison_result.total_differences}
• רעש שסונן: {len(comparison_result.noise_filtered)} ({comparison_result.statistics['noise_reduction_percent']:.1f}%)
• שגיאות קלות: {len(comparison_result.minor_issues)}
• שגיאות קריטיות: {len(comparison_result.critical_errors)}
• הבדלים לא מזוהים: {len(comparison_result.unknown_differences)}

🎯 החלטות אוטומטיות:
• ניתן לאישור אוטומטי: {"כן" if comparison_result.auto_approvable else "לא"}
• דורש בדיקה ידנית: {"כן" if comparison_result.requires_manual_review else "לא"}
• ציון ביטחון כללי: {comparison_result.overall_confidence:.1%}

🔍 בעיות קריטיות שנמצאו:
"""
        
        for error in comparison_result.critical_errors:
            summary += f"• {error.description} (שורה {error.line_number})\n"
        
        if not comparison_result.critical_errors:
            summary += "• אין בעיות קריטיות ✅\n"
        
        return summary

# יצירת מופע גלובלי
COMPARATOR = IntelligentTextComparator()

if __name__ == "__main__":
    # בדיקה עצמית עם דוגמאות
    print("=== בדיקת מנוע השוואה אינטליגנטי ===")
    
    # דוגמת טקסט עם רעש ושגיאות אמיתיות
    ground_truth = """השופט עו"ד ברעם: תענה בבקשה לשאלה.
המשיב פויר: אני לא זוכר את הפרטים.
העד לילת הזמנתי לדיון."""
    
    model_output = """השופט עוייד ברעם: תענה בבקשה לשאלה.<<1>>
המשיב פירר: אני לא זוכר את הפרטים.
העד נוית הזמנתי לקידום."""  # המילה "לדיון" הוחלפה ב"לקידום" שאינה בלקסיקון
    
    # הרצת הניתוח
    result = COMPARATOR.analyze_differences(ground_truth, model_output)
    
    # יצירת דוחות
    json_file = COMPARATOR.generate_report_json(result)
    summary = COMPARATOR.generate_summary_report(result)
    
    print(summary)
    print(f"\nדוח מפורט נשמר בקובץ: {json_file}")
    
    # בדיקת יכולת סיווג
    print(f"\n🧪 בדיקת סיווג:")
    print(f"רעש זוהה: {len(result.noise_filtered)} מקרים")
    print(f"שגיאות קריטיות: {len(result.critical_errors)} מקרים") 
    print(f"הבדלים לא מזוהים: {len(result.unknown_differences)} מקרים")
```

#### 1.3.2 בדיקת המנוע (30 דקות)
```bash
python intelligent_comparator.py
```

**ודא שהפלט כולל:**
- זיהוי נכון של הרעש (`עוייד` ← `עו"ד`)
- זיהוי שגיאה קריטית (`מוזס` ← `מילצ'ן`)
- דוח JSON מפורט
- דוח סיכום קריא

---

## שלב 1.4: שדרוג llm_test_harness_v3.4.py (2 שעות)
**מטרה**: החלפת מנוע ההשוואה הקיים במנוע החכם

### 📋 חומרי גלם נדרשים:
- `llm_test_harness_v3.3.py` (הגרסה הקיימת)
- `intelligent_comparator.py` (שנוצר בשלב הקודם)

### 🔧 פעולות מדויקות:

#### 1.4.1 גיבוי הגרסה הקיימת (5 דקות)
```bash
cp llm_test_harness_v3.3.py llm_test_harness_v3.3_backup_$(date +%Y%m%d_%H%M%S).py
```

#### 1.4.2 יצירת הגרסה החדשה (105 דקות)
**צור קובץ: `llm_test_harness_v3.4.py`**
```python
"""
רתמת בדיקות משודרגת עם מנוע השוואה אינטליגנטי
גרסה 3.4 - החלפת difflib במנוע חכם
"""

import os
import json
import time
from datetime import datetime
from intelligent_comparator import COMPARATOR

# ייבוא כל הפונקציות מהגרסה הקודמת
import importlib.util
spec = importlib.util.spec_from_file_location("v3_3", "llm_test_harness_v3.3.py")
v3_3 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v3_3)

class SmartTestHarness(v3_3.LLMTestHarness):  # ירושה מהמחלקה הקיימת
    def __init__(self):
        super().__init__()
        self.intelligent_comparator = COMPARATOR
        self.version = "3.4"
        
    def compare_texts_intelligently(self, ground_truth: str, model_output: str) -> dict:
        """השוואה חכמה עם סיווג הבדלים"""
        
        # שימוש במנוע החכם במקום difflib
        comparison_result = self.intelligent_comparator.analyze_differences(
            ground_truth, model_output
        )
        
        return {
            'comparison_result': comparison_result,
            'legacy_compatible': {
                'differences_found': comparison_result.total_differences,
                'significant_issues': len(comparison_result.critical_errors) + len(comparison_result.unknown_differences),
                'auto_approved': comparison_result.auto_approvable,
                'requires_review': comparison_result.requires_manual_review
            }
        }
    
    def generate_smart_report(self, test_results: dict, output_dir: str = None) -> str:
        """יצירת דוח מבוסס השוואה חכמה"""
        
        if not output_dir:
            output_dir = "truth_test/test_harness_results/reports"
        
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # יצירת דוח HTML משופר
        html_content = self._create_smart_html_report(test_results)
        
        html_file = os.path.join(output_dir, f"smart_report_{timestamp}.html")
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # יצירת דוח JSON
        json_file = os.path.join(output_dir, f"smart_report_{timestamp}.json")
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(test_results, f, ensure_ascii=False, indent=2, default=str)
        
        print(f"דוח HTML: {html_file}")
        print(f"דוח JSON: {json_file}")
        
        return html_file
    
    def _create_smart_html_report(self, test_results: dict) -> str:
        """יצירת דוח HTML עם סיווג חכם"""
        
        html = f"""
<!DOCTYPE html>
<html dir="rtl" lang="he">
<head>
    <meta charset="UTF-8">
    <title>דוח השוואה אינטליגנטי - {datetime.now().strftime('%d/%m/%Y %H:%M')}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; }}
        .header {{ background: #2c3e50; color: white; padding: 15px; border-radius: 5px; margin-bottom: 20px; }}
        .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-bottom: 20px; }}
        .stat-card {{ background: #ecf0f1; padding: 15px; border-radius: 5px; text-align: center; }}
        .stat-number {{ font-size: 2em; font-weight: bold; color: #2c3e50; }}
        .critical {{ background: #e74c3c; color: white; }}
        .minor {{ background: #f39c12; color: white; }}
        .noise {{ background: #27ae60; color: white; }}
        .unknown {{ background: #9b59b6; color: white; }}
        .section {{ margin: 20px 0; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }}
        .difference {{ margin: 10px 0; padding: 10px; border-radius: 3px; }}
        .difference.critical {{ border-left: 5px solid #e74c3c; background: #fadad7; }}
        .difference.minor {{ border-left: 5px solid #f39c12; background: #fdeaa7; }}
        .difference.noise {{ border-left: 5px solid #27ae60; background: #d5f4e6; }}
        .difference.unknown {{ border-left: 5px solid #9b59b6; background: #e8d5f4; }}
        .diff-content {{ font-family: monospace; background: #f8f9fa; padding: 8px; margin: 5px 0; border-radius: 3px; }}
        .approval-status {{ padding: 20px; text-align: center; font-size: 1.2em; font-weight: bold; border-radius: 5px; }}
        .approved {{ background: #d5f4e6; color: #27ae60; }}
        .rejected {{ background: #fadad7; color: #e74c3c; }}
        .review-needed {{ background: #fdeaa7; color: #f39c12; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧠 דוח השוואה אינטליגנטי</h1>
            <p>גרסה 3.4 - מנוע השוואה חכם עם סיווג אוטומטי</p>
        </div>
"""
        
        # הוספת תוכן דינמי על בסיס תוצאות הבדיקה
        for chunk_id, result in test_results.items():
            comparison = result.get('smart_comparison', {})
            comp_result = comparison.get('comparison_result')
            
            if comp_result:
                html += self._add_chunk_analysis_to_html(chunk_id, comp_result)
        
        html += """
    </div>
</body>
</html>
"""
        return html
    
    def _add_chunk_analysis_to_html(self, chunk_id: str, comparison_result) -> str:
        """הוספת ניתוח צ'אנק יחיד לדוח HTML"""
        
        # קביעת סטטוס אישור
        if comparison_result.auto_approvable:
            status_class = "approved"
            status_text = "✅ מאושר אוטומטית"
        elif comparison_result.requires_manual_review:
            status_class = "rejected"
            status_text = "❌ דורש בדיקה ידנית"
        else:
            status_class = "review-needed"
            status_text = "⚠️ לבדיקה"
        
        html = f"""
        <div class="section">
            <h2>📄 {chunk_id}</h2>
            
            <div class="approval-status {status_class}">
                {status_text}
            </div>
            
            <div class="stats">
                <div class="stat-card critical">
                    <div class="stat-number">{len(comparison_result.critical_errors)}</div>
                    <div>שגיאות קריטיות</div>
                </div>
                <div class="stat-card minor">
                    <div class="stat-number">{len(comparison_result.minor_issues)}</div>
                    <div>שגיאות קלות</div>
                </div>
                <div class="stat-card noise">
                    <div class="stat-number">{len(comparison_result.noise_filtered)}</div>
                    <div>רעש שסונן</div>
                </div>
                <div class="stat-card unknown">
                    <div class="stat-number">{len(comparison_result.unknown_differences)}</div>
                    <div>לא מזוהה</div>
                </div>
            </div>
            
            <p><strong>ציון ביטחון:</strong> {comparison_result.overall_confidence:.1%}</p>
            <p><strong>הפחתת רעש:</strong> {comparison_result.statistics.get('noise_reduction_percent', 0):.1f}%</p>
"""
        
        # הוספת שגיאות קריטיות
        if comparison_result.critical_errors:
            html += "<h3>🚨 שגיאות קריטיות:</h3>"
            for error in comparison_result.critical_errors:
                html += f"""
                <div class="difference critical">
                    <strong>{error.description}</strong> (שורה {error.line_number})
                    <div class="diff-content">
                        <div>אמת מוחלטת: {error.ground_truth_text}</div>
                        <div>פלט מודל: {error.model_output_text}</div>
                    </div>
                </div>
                """
        
        # הוספת הבדלים לא מזוהים
        if comparison_result.unknown_differences:
            html += "<h3>❓ הבדלים לא מזוהים:</h3>"
            for diff in comparison_result.unknown_differences:
                html += f"""
                <div class="difference unknown">
                    <strong>דורש בדיקה ידנית</strong> (שורה {diff.line_number})
                    <div class="diff-content">
                        <div>אמת מוחלטת: {diff.ground_truth_text}</div>
                        <div>פלט מודל: {diff.model_output_text}</div>
                    </div>
                </div>
                """
        
        html += "</div>"
        return html
    
    def run_smart_test(self, model_name: str, prompt_file: str, 
                      ground_truth_files: list, image_files: list = None,
                      chunk_size: int = 5) -> dict:
        """הרצת בדיקה עם מנוע חכם"""
        
        print(f"🧠 הרצת בדיקה חכמה - {model_name}")
        
        results = {}
        
        for i, gt_file in enumerate(ground_truth_files):
            chunk_id = f"chunk_{i}"
            print(f"  מעבד {chunk_id}...")
            
            # טעינת אמת מוחלטת
            with open(gt_file, 'r', encoding='utf-8') as f:
                ground_truth_data = json.load(f)
                ground_truth_text = ground_truth_data.get('extracted_text', '')
            
            # הרצת המודל (שימוש בפונקציה הקיימת)
            if image_files and i < len(image_files):
                model_output = self.run_model_on_images(
                    model_name, prompt_file, [image_files[i]]
                )
            else:
                model_output = self.run_model_on_text(
                    model_name, prompt_file, ground_truth_text
                )
            
            # השוואה חכמה
            smart_comparison = self.compare_texts_intelligently(
                ground_truth_text, model_output
            )
            
            results[chunk_id] = {
                'model_name': model_name,
                'ground_truth_file': gt_file,
                'model_output': model_output,
                'smart_comparison': smart_comparison,
                'timestamp': datetime.now().isoformat()
            }
            
            # דיווח ביניים
            comp_result = smart_comparison['comparison_result']
            print(f"    ביטחון: {comp_result.overall_confidence:.1%}")
            print(f"    שגיאות קריטיות: {len(comp_result.critical_errors)}")
            print(f"    רעש שסונן: {len(comp_result.noise_filtered)}")
        
        # יצירת דוח
        report_file = self.generate_smart_report(results)
        
        return {
            'results': results,
            'report_file': report_file,
            'summary': self._calculate_test_summary(results)
        }
    
    def _calculate_test_summary(self, results: dict) -> dict:
        """חישוב סיכום כללי של הבדיקה"""
        
        total_chunks = len(results)
        auto_approved = 0
        requires_review = 0
        total_critical_errors = 0
        total_noise_filtered = 0
        
        for result in results.values():
            comp_result = result['smart_comparison']['comparison_result']
            
            if comp_result.auto_approvable:
                auto_approved += 1
            if comp_result.requires_manual_review:
                requires_review += 1
            
            total_critical_errors += len(comp_result.critical_errors)
            total_noise_filtered += len(comp_result.noise_filtered)
        
        automation_rate = auto_approved / total_chunks if total_chunks > 0 else 0
        
        return {
            'total_chunks': total_chunks,
            'auto_approved': auto_approved,
            'requires_review': requires_review,
            'automation_rate': automation_rate,
            'total_critical_errors': total_critical_errors,
            'total_noise_filtered': total_noise_filtered
        }

def main():
    """פונקציה ראשית לבדיקה מהירה"""
    print("=== רתמת בדיקות חכמה v3.4 ===")
    
    harness = SmartTestHarness()
    
    # בדיקה על צ'אנק יחיד
    test_files = [
        "downloaded_json_parts/full_ground_truth_protocol-0.json"
    ]
    
    result = harness.run_smart_test(
        model_name="gemini-2.5-pro",
        prompt_file="prompts/main_extraction_prompt_v4.2.txt",
        ground_truth_files=test_files
    )
    
    print("\n📊 סיכום הרצה:")
    summary = result['summary']
    print(f"  צ'אנקים נבדקו: {summary['total_chunks']}")
    print(f"  אושר אוטומטית: {summary['auto_approved']}")
    print(f"  שיעור אוטומציה: {summary['automation_rate']:.1%}")
    print(f"  רעש שסונן: {summary['total_noise_filtered']}")
    print(f"  שגיאות קריטיות: {summary['total_critical_errors']}")
    
    return result

if __name__ == "__main__":
    main()
```

#### 1.4.3 בדיקת הרתמה החדשה (10 דקות)
```bash
python llm_test_harness_v3.4.py
```

**ודא שהפלט כולל:**
- הרצה מוצלחת על צ'אנק יחיד
- דוח HTML חדש עם סיווג צבעוני
- סיכום עם מספרי אוטומציה

---

## שלב 1.5: יצירת 15 עמודי GT מגוונים (1 שעה)
**מטרה**: Google Sheet מוכן עם 15 עמודים מגוונים לשלב הבא

### 📋 חומרי גלם נדרשים:
- קבצי GT קיימים: `downloaded_json_parts/full_ground_truth_protocol-0.json` עד `-11.json`
- גישה לGoogle Sheets

### 🔧 פעולות מדויקות:

#### 1.5.1 בחירת עמודים מגוונים (20 דקות)
**בחר 15 עמודים לפי הפיזור הבא:**
- תיק 1000: עמודים 1, 6, 11, 16, 21 (5 עמודים)
- תיק 2000: עמודים 26, 31, 36, 41, 46 (5 עמודים)  
- תיק 4000: עמודים 51, 56, 61, 66, 71 (5 עמודים)

**צור רשימה: `selected_pages_for_gt.txt`**
```
# 15 עמודים נבחרים לGT מגוון
# תיק 1000 (עמודים 1-25)
1,6,11,16,21

# תיק 2000 (עמודים 26-50)  
26,31,36,41,46

# תיק 4000 (עמודים 51-75)
51,56,61,66,71
```

#### 1.5.2 יצירת Google Sheet (25 דקות)
**פתח Google Sheets וצור גיליון חדש בשם: "GT Training Set - 15 Pages"**

**מבנה הגיליון:**
| Page | Case | Raw_JSON_File | GT_Text_Sample | Status | Notes | Priority |
|------|------|---------------|----------------|--------|-------|----------|
| 1 | 1000 | full_ground_truth_protocol-0.json | "השופט עו"ד ברעם..." | Ready | - | High |
| 6 | 1000 | full_ground_truth_protocol-1.json | "המשיב אמר..." | Ready | - | High |

**הוראות מילוי:**
1. טען כל קובץ JSON
2. העתק 50 תווים ראשונים ל-GT_Text_Sample
3. סמן Status כ-"Ready" אם הטקסט נראה טוב
4. הוסף הערות ב-Notes אם יש בעיות
5. קבע Priority: High/Medium/Low

#### 1.5.3 הכנת הנתונים לשלב הבא (15 דקות)
**צור קובץ: `gt_dataset_config.json`**
```json
{
  "dataset_name": "15_pages_diverse_gt",
  "creation_date": "2025-06-24",
  "total_pages": 15,
  "distribution": {
    "case_1000": 5,
    "case_2000": 5,
    "case_4000": 5
  },
  "selected_files": [
    "downloaded_json_parts/full_ground_truth_protocol-0.json",
    "downloaded_json_parts/full_ground_truth_protocol-1.json"
  ],
  "google_sheet_url": "https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID",
  "ready_for_bakeoff": true
}
```

---

## 🎯 סיכום יום 1 - יעדי הצלחה

### ✅ תוצרים שיהיו מוכנים:
1. **החלטה על שיטת חילוץ** (PDF או OCR)
2. **noise_and_error_lexicon.py** - לקסיקון מלא עם 16+ תבניות
3. **intelligent_comparator.py** - מנוע השוואה עם JSON מפורט
4. **llm_test_harness_v3.4.py** - רתמה משודרגת עם דוח HTML צבעוני
5. **15 עמודי GT** מגוונים בGoogle Sheet מוכן

### 📊 מדדי הצלחה:
- **הפחתת רעש של 80-90%** בדוחות ההשוואה
- **זיהוי אוטומטי** של שגיאות קריטיות מול רעש
- **דוח ברור** עם סיווג צבעוני והמלצות פעולה
- **נתוני GT מוכנים** לבדיקת מודלים ביום 2

### 🚨 נקודות ביקורת קריטיות:
- וודא שהלקסיקון מזהה את הדוגמאות מהדוח האמיתי
- בדוק שהמנוע החכם מפחית התרעות ב-80%+
- ודא שהרתמה החדשה יוצרת דוח HTML קריא
- אמת שיש 15 עמודים מגוונים מוכנים לשלב הבא

**בסיום יום 1, המערכת תהיה מוכנה לbake-off מדויק ביום 2.**

---

## 🚀 מדריך הפעלה מרוכז

### 📁 הכנת סביבת העבודה
```bash
cd C:\Users\עידושיפוני\alsheich_v2
mkdir day1_execution
cd day1_execution
```

### ⚡ רצף פקודות הרצה מלא
```bash
# שלב 1.1 - בדיקת PDF vs OCR
python pdf_vs_ocr_test.py

# שלב 1.2 - בדיקת הלקסיקון
python noise_and_error_lexicon.py

# שלב 1.3 - בדיקת המנוע החכם
python intelligent_comparator.py

# שלב 1.4 - בדיקת הרתמה החדשה
python llm_test_harness_v3.4.py
```

### 🔍 נקודות ביקורת מסכמות
✅ **אחרי שלב 1.1**: קובץ `extraction_method_decision.txt` עם נימוק כמותי  
✅ **אחרי שלב 1.2**: לקסיקון מחזיר 8+ תבניות רעש, 2+ קלות, 5+ קריטיות  
✅ **אחרי שלב 1.3**: מנוע מזהה נכון רעש, שגיאות קריטיות ולא מזוהות  
✅ **אחרי שלב 1.4**: דוח HTML צבעוני עם אחוזי אוטומציה  
✅ **אחרי שלב 1.5**: 15 עמודים בGoogle Sheet מוכנים לביום 2

### 🎯 יעדי הצלחה סופיים
- **80-90% הפחתת רעש** בדוחות השוואה
- **זיהוי אוטומטי** של שגיאות קריטיות אמיתיות
- **15 עמודי GT מגוונים** מוכנים לבדיקת מודלים
- **מערכת מוכנה** לbake-off מדויק ביום 2

---

## 📋 רשימת קבצים שייווצרו

### קבצי הליבה:
- `pdf_vs_ocr_test.py`
- `noise_and_error_lexicon.py` 
- `intelligent_comparator.py`
- `llm_test_harness_v3.4.py`

### קבצי תיעוד ותצורה:
- `extraction_method_decision.txt`
- `selected_pages_for_gt.txt`
- `gt_dataset_config.json`
- `lexicon_export_[timestamp].json`

### דוחות וגיבויים:
- `pdf_vs_ocr_test_report_[timestamp].json`
- `intelligent_comparison_report_[timestamp].json`
- `smart_report_[timestamp].html`
- `llm_test_harness_v3.3_backup_[timestamp].py`