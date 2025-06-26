## 🧭 תוכנית עבודה מלאה: הפקת קובצי אמת מוחלטת (GT) חדשים ובניית לולאת בדיקה סטטיסטית

**טווח:** עמודים 1–20 של הפרוטוקול
**מודל ראשון:** Gemini 2.5 Pro
**יחידת עבודה:** מקטעים של 5 עמודים (Chunk)
**שיטת אגירה:** SQLite DB מובנה (meta.db)

---

### 🟦 שלב 1: הכנה כללית

1. ודא שקובץ `PROJECT_BOOTSTRAP_V2.7.md` טעון ופעיל.
2. ודא שהריפו הראשי נמצא בתיקייה:

   ```
   C:\Users\עידושיפוני\alsheich_v2
   ```
3. הפק קובץ tree חדש:

   ```bash
   tree /F /A > day1_execution/structure_day1.txt
   ```
4. אמת שכל הקבצים הקריטיים נמצאים:

   * `protocol_images/page_1.jpg` עד `page_20.jpg`
   * `llm_test_harness_v3.3.py`
   * `main_extraction_prompt_v4.2.txt`
   * `error_traps_v1.0.json`

---

### 🔵 שלב 2: הרצת Chunk 0 (עמודים 1–5)

#### 🎯 מטרה: הפקת קובץ GT ראשון, ידני, מושלם

1. הפעל את `llm_test_harness_v3.3.py` עם Gemini 2.5 Pro:

   ```bash
   python llm_test_harness_v3.3.py --chunk 0 --pages 1-5 --model gemini-2.5-pro --prompt prompts/main_extraction_prompt_v4.2.txt
   ```
2. שמור את הפלט תחת:

   * `truth_test/test_harness_results/json_outputs/round55_chunk0_model_gemini-2.5-pro_prompt_v4.2.json`
   * `truth_test/fixed_outputs/round55_chunk0_model_gemini-2.5-pro_raw.json` (לעריכה)
3. העבר את הקובץ לעריכת המשתמש.
4. לאחר העלאה חוזרת של הקובץ המתוקן:

   * שמור כ־`truth_test/final_gt_parts/FINAL_full_ground_truth_protocol-0.json`
   * הרץ השוואת פלט גולמי מול GT (השוואה **לפני תיקון**)
   * הפק דוח השוואה ודוח סטטיסטי → שמור תחת `reports/`
   * הוסף שגיאות לקובץ `error_traps_v1.1.json`
   * הכנס מטאדאטה למסד הנתונים `meta_db/meta.db`

---

### 🟢 שלב 3: ריצות המשך על Chunk 0 (מודלים נוספים)

1. כל מודל נוסף ירוץ על הקטע הזה בטור:

   * שמירת פלט → השוואה מול GT
   * הפקת דוח HTML ודוח שגיאות
   * עדכון `error_traps` **רק לאחר ההשוואה**
   * הרצת תיקון אוטומטי (אם רלוונטי)
   * השוואה שנייה (אחרי תיקון)
   * שמירת הדוחות והתוצרים
   * עדכון `meta.db` עם כל נתוני הריצה

---

### 🟣 שלב 4: הפקת GT עבור Chunk 1 (עמודים 6–10)

1. ריצה של Gemini 2.5 Pro → הפקת פלט
2. עריכה ידנית על ידי המשתמש
3. שמירת הקובץ כ־`FINAL_full_ground_truth_protocol-1.json`
4. חזרה על שלבי ההשוואה + הפקת שגיאות
5. הפעלת מודלים נוספים בטור מלא (בדיקה → תיקון → בדיקה חוזרת)
6. תיעוד נתונים למסד `meta.db`

---

### 🟠 שלב 5: חזרה על התהליך ל־Chunks 2–3 (עמודים 11–20)

1. לכל קטע:

   * הרצה במודל ראשון
   * תיקון ידני
   * השוואה כפולה
   * הזנת שגיאות
   * ריצת מודלים נוספים
   * תיעוד מטא + חישובי עלות במסד הנתונים

---

### 📊 תיעוד סטטיסטי ולוגי

לכל ריצה יש לשמור במסד הנתונים:

* input\_tokens
* output\_tokens
* reasoning\_tokens (אם קיימים)
* model name + version
* prompt version
* GT version
* trap file version used
* cost estimate
* זמן ריצה
* מזהה סשן
* נתיב פלט

---

### 📂 מבנה תיקיות חובה

* `final_gt_parts/` — קבצי אמת מוחלטת סופיים (0–3)
* `json_outputs/` — פלטים גולמיים של כל מודל
* `fixed_outputs/` — פלט לאחר תיקון אוטומטי
* `reports/` — דוחות השוואה כפולים (לפני/אחרי תיקון)
* `error_logs/` — שגיאות מדויקות
* `meta_db/` — כולל מסד `meta.db` ומבנה סכימה

---

### ✅ נקודת סיום התוכנית:

* 4 קובצי GT חדשים (20 עמודים)
* תיעוד מלא לכל מודל שרץ
* קובץ error\_traps מעודכן ודינמי
* תשתית השוואה + תיקון כפול פועלת אוטומטית
* בסיס סטטיסטי להשוואת מודלים לאורך זמן במסד נתונים מרכזי
