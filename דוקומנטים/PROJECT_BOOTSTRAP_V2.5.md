הבנתי. אני מפיק כעת את קובץ החפיפה המלא והמעודכן, `PROJECT_BOOTSTRAP_V2.5.md`, עם דגש מיוחד על תיעוד מפורט של הדיון האסטרטגי ותוכניות הפעולה שהגדרת.

הקובץ כולל את כל הנהלים החדשים, יומן מפורט של הסשן, ואת מפת הנכסים המעודכנת. הוא מתוכנן להעביר את מלוא ההקשר והמחשבה האסטרטגית לשיחה הבאה.

-----

**שם קובץ החפיפה לשמירה:**

```
PROJECT_BOOTSTRAP_V2.5.md
```

\--- התחלה של קובץ `PROJECT_BOOTSTRAP_V2.5.md` ---
﻿
**PROJECT\_BOOTSTRAP\_V2.5**
**עדכון אחרון:** 2025-06-22

**סעיף 1: הנחיות ליבה ונהלי עבודה**

**1.1. עקרונות יסוד**

  * **תפקיד:** תפקידי הוא לשמש כשותף פיתוח, ארכיטקט ומתעד טכני.
  * **היררכיית קבלת החלטות:** המשתמש הוא מקבל ההחלטות האסטרטגי הבלעדי.
  * **פרוטוקול שפה:** התקשורת תתנהל בעברית.

**1.2. פרוטוקול "סטופ" (השהיית יוזמה)**

  * **מטרה:** לאפשר למשתמש לעצור את התקדמות המשימה כדי להתמקד בשאלות ודיונים לוגיים.

**1.3. פרוטוקול הצעת שינוי לוגי**

  * **הגדרה:** "שינוי לוגי" הוא כל שינוי שמשפיע על האופן שבו המערכת פועלת.
  * **נוהל הצעה:** כל הצעה תפרט את המצב הקיים, השינוי המוצע, הסיבה וההשלכות, ותמתין לאישור מפורש לפני יישום.

**1.4. מתודולוגיית עבודה ופיתוח**

  * **נוהל מתן קוד:**
      * **שלמות הקוד:** יש לספק תמיד את קובץ הקוד המלא והמעודכן.
      * **מבנה הצגת קובץ:** שם הקובץ יוצג בתיבת קוד, ולאחר מכן התוכן המלא יופיע בין סמני פתיחה וסגירה ברורים.
      * **ניהול גרסאות סקריפטים:** כל שינוי לוגי בסקריפט יחייב שמירה כקובץ חדש עם מספר גרסה מוגדל. חל איסור מוחלט לערוך או לדרוס גרסה קיימת. *נימוק:* מניעת דריסה של גרסאות מתפקדות ושמירה על היסטוריה הניתנת לשחזור.
  * **נוהל הרצת סקריפטים:**
      * **פקודת הרצה:** יש לספק את פקודת ההרצה המלאה והמדויקת בתיבת קוד.
      * **טיפול בפלט ארוך:** כאשר צפוי פלט ארוך (כמו הרצת אבחון), הסקריפט יתכנת כך שישמור את הפלט לקובץ בתיקייה ייעודית (כגון `diagnostics/`) במקום להדפיסו למסך.
  * **נוהל "מלכודות שגיאה" (`error_traps.json`):**
      * **עקרון שימוש:** ישמש כ"מוצא אחרון" ורק למקרים מובהקים וחד-משמעיים. אין להשתמש בו למקרים גבוליים או מילים שעלולות להיות נכונות בהקשר אחר.
      * **לולאת עדכון:** זיהוי שגיאה בדוח -\> הצעה לעדכון המאגר -\> אישור משתמש -\> הפקת קובץ `json` מעודכן -\> הרצה חוזרת.

**1.5. פרוטוקול עדכון הקשר (נוהל 'קובץ Bootstrap')**

  * **שלמות וניהול גרסאות:** כל גרסה עומדת בפני עצמה ומספרה עולה ב-0.1.
  * **תזמון עדכון:** קובץ חפיפה חדש יופק **רק בסיום סשן עבודה**, ולא במהלכו.
  * **מיפוי נכסים:** לפני יצירת קובץ חפיפה חדש, תתבצע בקשה להרצת `tree /f`.

**סעיף 2: מצב הפרויקט וחזון**

  * **מטרת הפרויקט:** פיתוח מערכת אוטומטית לחילוץ, עיבוד, והבניית מידע מפרוטוקולים משפטיים.
  * **השלב הנוכחי:** **כיול מוצלח של תהליך הבדיקה.** הגענו למצב יציב שבו רתמת הבדיקות (`llm_test_harness_v3.2`) והפרומפט (`main_extraction_prompt_v4.2`) מפיקים דוח השוואה מהימן. אנו מוכנים להתחיל בלולאת השיפור ובבחינת אסטרטגיות מתקדמות.
  * **חזון אסטרטגי (בהתאם לדיון האחרון):**
    1.  **שיפור דיוק בסיסי:** שימוש בלולאת "מלכודות שגיאה" והנדסת פרומפטים.
    2.  **הטמעת בקרת איכות אוטומטית (Automated QA Layer):** פיתוח "שכבת בדיקה שנייה" המשתמשת במודל שפה נוסף כדי לסמן שגיאות חשודות באופן אוטומטי.
    3.  **ביצוע "Bake-off" בין מודלים:** בניית יכולת להרצה השוואתית של מספר מודלים (ממתחרים שונים) ובחינת השונות הסטטיסטית בביצועיהם.
    4.  **מערכת ייצור עם הצלבה:** בחינת ארכיטקטורה עתידית שבה שני מודלים רצים במקביל, ואי-הסכמה ביניהם מפעילה התרעה.

**סעיף 3: תוכנית טכנית (Blueprint)**

  * **ארכיטקטורת בדיקה נוכחית:** `llm_test_harness_v3.2.py`.
      * **מודל:** `gemini-2.5-pro`.
      * **פרומפט:** `prompts/main_extraction_prompt_v4.2.txt`.
      * **אמת מוחלטת:** `downloaded_json_parts/`, ניקוי באמצעות סף גיאומטרי של `480px`.

**סעיף 4: נכסים דיגיטליים ובסיסי קוד**

  * **נתיב בסיס:** `C:\Users\עידושיפוני\alsheich_v2`
  * **סקריפטים פעילים ועדכניים:**
      * **`llm_test_harness_v3.2.py`**: רתמת הבדיקות האחרונה שהופקה.
      * **`diagnose_paragraph_geometry.py`**: סקריפט אבחון גיאומטרי.
      * **`llm_test_harness_v3.0.py`**: גרסת רתמת הבדיקות עם מצב אבחון `--debug-geometry`.
  * **נכסי "אמת מוחלטת":** `downloaded_json_parts/`.
  * **תצורה ופרומפטים:**
      * `prompts/main_extraction_prompt_v4.2.txt`: הפרומפט הפעיל.
      * `error_traps_v1.0.json`: מאגר מלכודות השגיאה.

**סעיף 5: היסטוריית פיתוח והחלטות מפתח**

**5.1. אינדקס גרסאות Bootstrap**

| גרסה | תאריך | כותרת הסשן | תיאור תמציתי |
| :--- | :--- | :--- | :--- |
| V2.5 | 2025-06-22 | אבחון מתקדם, כיול סופי וגיבוש אסטרטגיה | סנכרון מלא, סדרת אבחונים וכיולים של הסינון הגיאומטרי, הגעה להרצה מוצלחת, ודיון אסטרטגי מקיף על עתיד הפרויקט. |

**5.4. יומן מפורט של הסשן האחרון (22 ביוני 2025)**

  * **כותרת:** סנכרון, אבחון מתקדם, כיול סופי וגיבוש אסטרטגיה ארוכת טווח.
  * **מטרה:** להגיע להרצה מוצלחת ויציבה של רתמת הבדיקות, ולתכנן את השלבים הבאים.
  * **שלב 1: סנכרון וחידוד נהלים.** הסשן החל בהעברת מידע על הפרויקט וסנכרון מלא. במהלכו, גובשו ואומצו הנהלים הבאים:
    1.  כל שינוי לוגי בסקריפט מחייב יצירת קובץ בגרסה חדשה.
    2.  קובץ חפיפה יופק רק בסוף סשן עבודה.
    3.  סקריפטים יתוכנתו לשמור פלט ארוך לקובץ ייעודי.
  * **שלב 2: פריצת דרך באבחון הבעיה הגיאומטרית.** לאחר סדרת כישלונות בניקוי קובץ האמת המוחלטת, נוצרה רתמת בדיקות (`v3.0`) עם מצב אבחון (`--debug-geometry`). הרצתה חשפה את הבעיה האמיתית: גובה העמוד בקובץ ה-JSON היה `2378px` ולא `1122px` כפי שהונח, מה שהפך את סף הסינון ללא רלוונטי.
  * **שלב 3: כיול סופי והצלחה.** נקבע ערך סף חדש ומדויק (`480px`). הופקה גרסה `v3.1` והרצתה הצליחה. לאחר מכן, הופקה גרסה `v3.2` שכללה שיפורים במבנה הפלט, והרצתה (`סבב 49`) הצליחה גם היא, והוכיחה שהחידוד בפרומפט (`v4.2`) מנע מהמודל "לפרש" שמות (`מוזס`/`מילצ'ן`).
  * **שלב 4: דיון אסטרטגי מעמיק ואישור תוכניות:**
      * **תוכניות לביצוע מיידי (שאושרו):**
        1.  **עדכון קובץ `error_traps.json`:** הפקת קובץ עם שגיאות התמלול המובהקות שזוהו בדוח האחרון.
        2.  **שיפור לוגיקת ההשוואה:** שדרוג רתמת הבדיקות כך שתתעלם מהבדלי מיקום של "כותרות קטנות" (כמו `נוכחים:`), כדי שהן לא יסומנו כשגיאה.
      * **תוכניות עקרוניות להמשך (שאושרו):**
        1.  **בדיקת שונות סטטיסטית:** בניית יכולת להרצות זהות של אותו מודל כדי למדוד את עקביותו.
        2.  **השוואה בין מודלים (Bake-off):** בניית יכולת להריץ מספר מודלים במקביל על אותם נתונים.
        3.  **הקמת מאגר נתונים השוואתי:** איסוף כל התוצאות למאגר שיאפשר ניתוח והצלבת נתונים.
        4.  **שכבת QA אוטומטית:** בחינת הרעיון של שימוש במודל שני לבקרת איכות אוטומטית.

**סעיף 6: סטטוס יכולות נוכחי וצעדים הבאים**

  * **סטטוס:** תהליך הכיול הבסיסי הושלם. המערכת יציבה ומוכנה לשלב הבא.
  * **הצעדים הבאים (עדיפות מיידית בתחילת הסשן הבא):**
    1.  הפקת קובץ `error_traps.json` מעודכן.
    2.  הפקת `llm_test_harness_v3.3.py` שתכלול את לוגיקת ההשוואה המשופרת (התעלמות מהבדלי מיקום של כותרות קטנות).
    3.  הרצת סבב בדיקה עם שני השיפורים הללו.

**סעיף 7: מפת נכסים עדכנית (נכון ל-22 ביוני 2025)**

```
C:.
│   .env
│   24 עמודים ניר חפץ 30-11-21.pdf
│   24 עמודים פרגו ברנע 8-05-24.pdf
│   advanced_extractor.py
│   allocate_global_id_range.py
│   analyze_bakeoff_results.py
│   Bakeoff_Results_Prompt-v2.0_Gemini-Family_Real-Run-01.csv
│   clean_json_headers_v1.1.py
│   clean_json_headers_v1.2.py
│   compare_text_content.py
│   create_truly_clean_gt.py
│   db_operations.py
│   diagnose_cleaning_effect.py
│   diagnose_json_structure.py
│   diagnose_json_structure_v2.py
│   diagnose_paragraph_geometry.py
│   difflib_v1.0.py
│   doc_ai_batch_extraction_v1.0.py
│   doc_ai_batch_extraction_v1.1.py
│   doc_ai_extraction_v1.0.py
│   download_results.py
│   error_traps_v1.0.json
│   extraction_bakeoff.py
│   finalize_gt_files.py
│   final_test_harness.py
│   find_witness_id_by_alias.py
│   fix_gt_files.py
│   full_ground_truth_protocol.pdf
│   generate_text_files.py
│   get_or_create_session.py
│   ground_truth.json
│   llm_extraction_bakeoff_v0.6.py
│   llm_test_harness_v1.0.py
│   llm_test_harness_v1.1.py
│   llm_test_harness_v1.3.py
│   llm_test_harness_v2.0.py
│   llm_test_harness_v2.1.py
│   llm_test_harness_v2.2.py
│   llm_test_harness_v2.3.py
│   llm_test_harness_v2.4.py
│   llm_test_harness_v2.5.py
│   llm_test_harness_v2.6.py
│   llm_test_harness_v2.7.py
│   llm_test_harness_v2.8.py
│   llm_test_harness_v2.9.py
│   llm_test_harness_v3.0.py
│   llm_test_harness_v3.1.py
│   main_processor.py
│   parse_filename.py
│   prepare_images.py
│   protocol_sample_5_pages.pdf
│   setup_database.py
│   simple_text_prompt.txt
│   עמוד ראשון פרגו ברנע 8-05-24.docx
│   פרגו ברנע 8-05-24.pdf
│   שם הקובץ הוא diagnose_json_structure.py
│
├───0_DATA
│   ├───input_files
│   │       24 עמודים פרגו ברנע 8-05-24.pdf
│   │
│   └───output_files
│       ├───24_עמודים_פרגו_ברנע
│       │   └───2024-05-08
│       │           raw_extraction_24 עמודים פרגו ברנע 8-05-24.txt
│       │
│       ├───bake-off_output
│       │       final_output.docx
│       │       final_output.xlsx
│       │       script_output.docx
│       │       script_output.xlsx
│       │
│       ├───bale-off_output
│       │       output_result.docx
│       │       output_result.xlsx
│       │
│       ├───ניר_חפץ
│       │   └───2021-11-30
│       │           chunk_ALS-0001007.txt
│       │           chunk_ALS-0001008.txt
│       │           chunk_ALS-0001009.txt
│       │
│       └───פרגו_ברנע
│           └───2024-05-08
│                   chunk_001.txt
│                   chunk_002.txt
│                   chunk_003.txt
│                   chunk_004.txt
│                   chunk_005.txt
│                   chunk_006.txt
│                   chunk_007.txt
│                   chunk_008.txt
│                   chunk_009.txt
│                   chunk_ALS-0001002.txt
│                   chunk_ALS-0001003.txt
│                   chunk_ALS-0001004.txt
│                   chunk_ALS-0001006.txt
│                   chunk_ALS-0001007.txt
│                   chunk_ALS-0001008.txt
│                   chunk_ALS-0001010.txt
│                   chunk_ALS-0001011.txt
│                   chunk_ALS-0001012.txt
│                   chunk_ALS-0001014.txt
│                   chunk_ALS-0001015.txt
│                   chunk_ALS-0001016.txt
│                   chunk_ALS-0001018.txt
│                   chunk_ALS-0001019.txt
│                   chunk_ALS-0001020.txt
│                   chunk_ALS-0001022.txt
│                   chunk_ALS-0001023.txt
│                   chunk_ALS-0001024.txt
│                   chunk_ALS-0001026.txt
│                   chunk_ALS-0001027.txt
│                   chunk_ALS-0001028.txt
│                   chunk_ALS-0001030.txt
│                   chunk_ALS-0001031.txt
│                   chunk_ALS-0001032.txt
│                   chunk_ALS-0001034.txt
│                   chunk_ALS-0001035.txt
│                   chunk_ALS-0001036.txt
│                   chunk_ALS-0001038.txt
│                   chunk_ALS-0001039.txt
│                   chunk_ALS-0001040.txt
│                   chunk_ALS-0001042.txt
│                   chunk_ALS-0001043.txt
│                   chunk_ALS-0001044.txt
│                   cleaned_protocol.txt
│
├───1_BAKEOFF_RESULTS
│   └───protocol_sample
│           protocol_sample_output.docx
│           protocol_sample_output.xlsx
│
├───data
│       alsheich_project.db
│
├───dirty_text_files
│       DIRTY_full_stitched_text.txt
│       full_ground_truth_protocol-0.txt
│       full_ground_truth_protocol-1.txt
│       full_ground_truth_protocol-10.txt
│       full_ground_truth_protocol-11.txt
│       full_ground_truth_protocol-2.txt
│       full_ground_truth_protocol-3.txt
│       full_ground_truth_protocol-4.txt
│       full_ground_truth_protocol-5.txt
│       full_ground_truth_protocol-6.txt
│       full_ground_truth_protocol-7.txt
│       full_ground_truth_protocol-8.txt
│       full_ground_truth_protocol-9.txt
│
├───downloaded_json_parts
│       full_ground_truth_protocol-0.json
│       full_ground_truth_protocol-1.json
│       full_ground_truth_protocol-10.json
│       full_ground_truth_protocol-11.json
│       full_ground_truth_protocol-2.json
│       full_ground_truth_protocol-3.json
│       full_ground_truth_protocol-4.json
│       full_ground_truth_protocol-5.json
│       full_ground_truth_protocol-6.json
│       full_ground_truth_protocol-7.json
│       full_ground_truth_protocol-8.json
│       full_ground_truth_protocol-9.json
│
├───logs
│       main_processor.log
│       protocol_cleaner.log
│       setup_database.log
│
├───prompts
│       extraction_prompt_v1.0.txt
│       extraction_prompt_v2.2.1_continuous.txt
│       extraction_prompt_v2.2.1_include_empty_lines.txt
│       extraction_prompt_v2.2.txt
│       extraction_prompt_v2.6.txt
│       extraction_prompt_v2.7.txt
│       extraction_prompt_v2.8_continuous_with_markers.txt
│       final_text_prompt.txt
│       main_extraction_prompt_v3.0.txt
│       main_extraction_prompt_v4.0.txt
│       main_extraction_prompt_v4.1.txt
│       simple_text_prompt.txt
│
├───protocol_images
│       page_1.jpg
│       page_10.jpg
│       page_11.jpg
│       page_12.jpg
│       page_13.jpg
│       page_14.jpg
│       page_15.jpg
│       page_16.jpg
│       page_17.jpg
│       page_18.jpg
│       page_19.jpg
│       page_2.jpg
│       page_20.jpg
│       page_21.jpg
│       page_22.jpg
│       page_23.jpg
│       page_24.jpg
│       page_25.jpg
│       page_26.jpg
│       page_27.jpg
│       page_28.jpg
│       page_29.jpg
│       page_3.jpg
│       page_30.jpg
│       page_31.jpg
│       page_32.jpg
│       page_33.jpg
│       page_34.jpg
│       page_35.jpg
│       page_36.jpg
│       page_37.jpg
│       page_38.jpg
│       page_39.jpg
│       page_4.jpg
│       page_40.jpg
│       page_41.jpg
│       page_42.jpg
│       page_43.jpg
│       page_44.jpg
│       page_45.jpg
│       page_46.jpg
│       page_47.jpg
│       page_48.jpg
│       page_49.jpg
│       page_5.jpg
│       page_50.jpg
│       page_51.jpg
│       page_52.jpg
│       page_53.jpg
│       page_54.jpg
│       page_55.jpg
│       page_56.jpg
│       page_57.jpg
│       page_58.jpg
│       page_59.jpg
│       page_6.jpg
│       page_60.jpg
│       page_7.jpg
│       page_8.jpg
│       page_9.jpg
│
├───test_results
│   ├───20250618_134712
│   │   └───gemini-1.5-pro
│   ├───run_20250618_131153
│   ├───run_20250618_133924
│   ├───run_20250618_140758
│   │   │   summary_results.csv
│   │   │
│   │   ├───gemini-1.0-pro-vision-latest
│   │   ├───gemini-1.5-flash-latest
│   │   │       page_1_output.json
│   │   │       page_2_output.json
│   │   │       page_3_output.json
│   │   │       page_4_output.json
│   │   │       page_5_output.json
│   │   │
│   │   ├───gemini-1.5-pro-latest
│   │   │       page_1_output.json
│   │   │       page_2_output.json
│   │   │       page_3_output.json
│   │   │       page_4_output.json
│   │   │       page_5_output.json
│   │   │
│   │   └───gemini-pro-vision
│   ├───run_20250618_195519
│   │   │   summary_results.csv
│   │   │
│   │   ├───gemini-1.5-flash-latest
│   │   │       פלאש1.5page_1_output.json
│   │   │       פלאש1.5page_2_output.json
│   │   │       פלאש1.5page_3_output.json
│   │   │       פלאש1.5page_4_output.json
│   │   │       פלאש1.5page_5_output.json
│   │   │
│   │   ├───gemini-1.5-pro-latest
│   │   │       פרו1.5page_1_output.json
│   │   │       פרו1.5page_2_output.json
│   │   │       פרו1.5page_3_output.json
│   │   │       פרו1.5page_4_output.json
│   │   │       פרו1.5page_5_output.json
│   │   │
│   │   ├───gemini-2.0-flash
│   │   │       page_1_output.json
│   │   │       page_2_output.json
│   │   │       page_3_output.json
│   │   │       page_4_output.json
│   │   │       page_5_output.json
│   │   │
│   │   ├───gemini-2.5-flash
│   │   │       page_1_output.json
│   │   │       page_2_output.json
│   │   │       page_3_output.json
│   │   │       page_4_output.json
│   │   │       page_5_output.json
│   │   │
│   │   ├───gemini-2.5-flash-lite-preview-06-17
│   │   │       page_1_output.json
│   │   │       page_2_output.json
│   │   │       page_3_output.json
│   │   │       page_4_output.json
│   │   │       page_5_output.json
│   │   │
│   │   └───gemini-2.5-pro
│   │           page_1_output.json
│   │           page_2_output.json
│   │           page_3_output.json
│   │           page_4_output.json
│   │           page_5_output.json
│   │
│   ├───run_20250619_005226
│   │   │   summary_results.csv
│   │   │
│   │   ├───gemini-1.5-flash-latest
│   │   │       gemini-1.5-flash-latest_page_1_output.json
│   │   │       gemini-1.5-flash-latest_page_2_output.json
│   │   │       gemini-1.5-flash-latest_page_3_output.json
│   │   │       gemini-1.5-flash-latest_page_4_output.json
│   │   │       gemini-1.5-flash-latest_page_5_output.json
│   │   │
│   │   ├───gemini-1.5-pro-latest
│   │   │       gemini-1.5-pro-latest_page_1_output.json
│   │   │       gemini-1.5-pro-latest_page_2_output.json
│   │   │       gemini-1.5-pro-latest_page_3_output.json
│   │   │       gemini-1.5-pro-latest_page_4_output.json
│   │   │       gemini-1.5-pro-latest_page_5_output.json
│   │   │
│   │   ├───gemini-2.0-flash
│   │   │       gemini-2.0-flash_page_1_output.json
│   │   │       gemini-2.0-flash_page_2_output.json
│   │   │       gemini-2.0-flash_page_3_output.json
│   │   │       gemini-2.0-flash_page_4_output.json
│   │   │       gemini-2.0-flash_page_5_output.json
│   │   │
│   │   ├───gemini-2.5-flash
│   │   │       gemini-2.5-flash_page_1_output.json
│   │   │       gemini-2.5-flash_page_2_output.json
│   │   │       gemini-2.5-flash_page_3_output.json
│   │   │       gemini-2.5-flash_page_4_output.json
│   │   │       gemini-2.5-flash_page_5_output.json
│   │   │
│   │   ├───gemini-2.5-flash-lite-preview-06-17
│   │   │       gemini-2.5-flash-lite-preview-06-17_page_1_output.json
│   │   │       gemini-2.5-flash-lite-preview-06-17_page_2_output.json
│   │   │       gemini-2.5-flash-lite-preview-06-17_page_3_output.json
│   │   │       gemini-2.5-flash-lite-preview-06-17_page_4_output_error.txt
│   │   │       gemini-2.5-flash-lite-preview-06-17_page_5_output.json
│   │   │
│   │   └───gemini-2.5-pro
│   │           gemini-2.5-pro_page_1_output.json
│   │           gemini-2.5-pro_page_2_output.json
│   │           gemini-2.5-pro_page_3_output.json
│   │           gemini-2.5-pro_page_4_output.json
│   │           gemini-2.5-pro_page_5_output.json
│   │
│   ├───run_20250619_012103
│   │   └───gemini-1.5-flash-latest
│   └───run_20250620_201415
│       └───gemini-1.5-flash-latest
├───test_results_doc_ai
│   ├───run_20250619_172210_doc_ai
│   │       summary_results.csv
│   │
│   ├───run_20250619_172711_doc_ai
│   │       summary_results.csv
│   │
│   ├───run_20250619_174424_doc_ai
│   │       protocol_sample_5_pages.pdf_extracted_text.txt
│   │       protocol_sample_5_pages.pdf_full_output.json
│   │       summary_results.csv
│   │
│   ├───run_20250619_195630_doc_ai
│   └───run_20250619_195822_doc_ai
│           summary_results.csv
│
├───test_results_doc_ai_batch
│   ├───run_20250619_201536
│   │       summary_results.csv
│   │
│   ├───run_20250619_203127
│   │       summary_results.csv
│   │
│   ├───run_20250619_203911
│   │       summary_results.csv
│   │
│   ├───run_20250619_204733
│   │       summary_results.csv
│   │
│   ├───run_20250619_205052
│   │       summary_results.csv
│   │
│   ├───run_20250619_211636
│   │       summary_results.csv
│   │
│   ├───run_20250619_212333
│   │       summary_results.csv
│   │
│   ├───run_20250619_213231
│   │       extracted_text.txt
│   │       full_output.json
│   │       summary_results.csv
│   │
│   └───run_20250620_111716_stitched
│           full_stitched_output.json
│           full_stitched_text.txt
│           summary_results.csv
│
├───truth_test
│   │   CLEANED_full_stitched_output.json
│   │
│   ├───cleaned_parts
│   │       CLEANED_full_ground_truth_protocol-0.json
│   │       CLEANED_full_ground_truth_protocol-1.json
│   │       CLEANED_full_ground_truth_protocol-10.json
│   │       CLEANED_full_ground_truth_protocol-11.json
│   │       CLEANED_full_ground_truth_protocol-2.json
│   │       CLEANED_full_ground_truth_protocol-3.json
│   │       CLEANED_full_ground_truth_protocol-4.json
│   │       CLEANED_full_ground_truth_protocol-5.json
│   │       CLEANED_full_ground_truth_protocol-6.json
│   │       CLEANED_full_ground_truth_protocol-7.json
│   │       CLEANED_full_ground_truth_protocol-8.json
│   │       CLEANED_full_ground_truth_protocol-9.json
│   │
│   ├───cleaned_text_files
│   │       CLEANED_full_ground_truth_protocol-0.txt
│   │       CLEANED_full_ground_truth_protocol-1.txt
│   │       CLEANED_full_ground_truth_protocol-10.txt
│   │       CLEANED_full_ground_truth_protocol-11.txt
│   │       CLEANED_full_ground_truth_protocol-2.txt
│   │       CLEANED_full_ground_truth_protocol-3.txt
│   │       CLEANED_full_ground_truth_protocol-4.txt
│   │       CLEANED_full_ground_truth_protocol-5.txt
│   │       CLEANED_full_ground_truth_protocol-6.txt
│   │       CLEANED_full_ground_truth_protocol-7.txt
│   │       CLEANED_full_ground_truth_protocol-8.txt
│   │       CLEANED_full_ground_truth_protocol-9.txt
│   │       CLEANED_full_stitched_text.txt
│   │
│   ├───final_gt_parts
│   │       FINAL_full_ground_truth_protocol-0.json
│   │       FINAL_full_ground_truth_protocol-1.json
│   │       FINAL_full_ground_truth_protocol-10.json
│   │       FINAL_full_ground_truth_protocol-11.json
│   │       FINAL_full_ground_truth_protocol-2.json
│   │       FINAL_full_ground_truth_protocol-3.json
│   │       FINAL_full_ground_truth_protocol-4.json
│   │       FINAL_full_ground_truth_protocol-5.json
│   │       FINAL_full_ground_truth_protocol-6.json
│   │       FINAL_full_ground_truth_protocol-7.json
│   │       FINAL_full_ground_truth_protocol-8.json
│   │       FINAL_full_ground_truth_protocol-9.json
│   │
│   ├───test_harness_results
│   │   ├───json_outputs
│   │   │       round10_chunk0_model_gemini-1_5-pro-latest_prompt_v2.2.1_include_empty_lines.json
│   │   │       round11_chunk0_model_gemini-1_5-pro-latest_prompt_v2.2.1_include_empty_lines_traps_v1.1.json
│   │   │       round12_chunk0_model_gemini-1_5-pro-latest_prompt_v2.6_traps_v1.1.json
│   │   │       round13_chunk0_model_gemini-1_5-pro-latest_prompt_v2.7_traps_v1.1.json
│   │   │       round14_chunk0_model_gemini-1_5-pro-latest_prompt_v2.2.1_include_empty_lines_vs_original_gt.json
│   │   │       round15_chunk0_model_gemini-1_5-pro-latest_prompt_extraction_prompt_v2.2.1_include_empty_lines.json
│   │   │       round15_chunk0_model_gemini-1_5-pro-latest_prompt_v2.2.1_include_empty_lines_vs_original_gt.json
│   │   │       round17_chunk0_model_gemini-1_5-pro-latest_prompt_extraction_prompt_v2.8_continuous_with_markers.txt
│   │   │       round19_chunk0_model_gemini-1_5-flash-latest_prompt_extraction_prompt_v2.8_continuous_with_markers.txt
│   │   │       round1_chunk0_model_gemini-1_5-pro-latest.json
│   │   │       round1_chunk0_model_gemini-1_5-pro-latest_adapted.json
│   │   │       round20_chunk0_model_gemini-2_0-flash_prompt_extraction_prompt_v2.8_continuous_with_markers.txt
│   │   │       round25_chunk0_model_gemini-2_0-flash_prompt_extraction_prompt_v2.2.1_include_empty_lines.json
│   │   │       round27_chunk0_model_gemini-1_5-pro-latest_prompt_extraction_prompt_v2.2.1_include_empty_lines.json
│   │   │       round28_chunk0_model_gpt-4o_prompt_extraction_prompt_v2.2.1_include_empty_lines.json
│   │   │       round2_chunk0_model_gemini-1_5-pro-latest_prompt_v2.2.json
│   │   │       round2_chunk0_model_gemini-1_5-pro-latest_prompt_v2.2_adapted.json
│   │   │       round36_chunk0_model_gemini-1.5-pro-latest_prompt_main_extraction_prompt_v3.0.json
│   │   │       round37_chunk0_model_gemini-2.5-pro_prompt_main_extraction_prompt_v3.0.json
│   │   │       round38_chunk0_model_gemini-2.5-pro_prompt_main_extraction_prompt_v4.0.json
│   │   │       round39_chunk0_model_gemini-2.5-pro_prompt_main_extraction_prompt_v4.1.json
│   │   │       round3_chunk0_model_gemini-1_5-pro-latest_prompt_v2.2.1_include_empty_lines.json
│   │   │       round3_chunk0_model_gemini-1_5-pro-latest_prompt_v2.2.1_include_empty_lines_adapted.json
│   │   │       round40_chunk0_model_gemini-2.5-pro_prompt_main_extraction_prompt_v4.1.json
│   │   │       round45_chunk0_model_gemini-2.5-pro_prompt_main_extraction_prompt_v4.1.json
│   │   │       round47_chunk0_model_gemini-2.5-pro_prompt_main_extraction_prompt_v4.1.json
│   │   │       round49_chunk0_model_gemini-2.5-pro_prompt_main_extraction_prompt_v4.2.json
│   │   │       round5_chunk0_model_gemini-1_5-pro-latest_prompt_v2.2.1_include_empty_lines.json
│   │   │       round5_chunk0_model_gemini-1_5-pro-latest_prompt_v2.2.1_include_empty_lines_adapted.json
│   │   │       round6_chunk0_model_gemini-2_5-pro_prompt_v2.2.1_include_empty_lines.json
│   │   │       round6_chunk0_model_gemini-2_5-pro_prompt_v2.2.1_include_empty_lines_adapted.json
│   │   │       round8_chunk0_model_gemini-2_5-pro_prompt_v2.2.1_include_empty_lines.json
│   │   │       round9_chunk0_model_gemini-1_5-pro-latest_prompt_v2.2.1_include_empty_lines.json
│   │   │
│   │   └───reports
│   │           round10_chunk0_model_gemini-1_5-pro-latest_prompt_v2.2.1_include_empty_lines_content_only_report.html
│   │           round11_chunk0_model_gemini-1_5-pro-latest_prompt_v2.2.1_include_empty_lines_traps_v1.1_difflib_report.html
│   │           round12_chunk0_model_gemini-1_5-pro-latest_prompt_v2.6_traps_v1.1_final_report.html
│   │           round13_chunk0_model_gemini-1_5-pro-latest_prompt_v2.7_traps_v1.1_final_report.html
│   │           round14_chunk0_model_gemini-1_5-pro-latest_prompt_v2.2.1_include_empty_lines_vs_original_gt_final_report.html
│   │           round15_chunk0_model_gemini-1_5-pro-latest_prompt_extraction_prompt_v2.2.1_include_empty_lines_final_report.html
│   │           round15_chunk0_model_gemini-1_5-pro-latest_prompt_v2.2.1_include_empty_lines_vs_original_gt_final_report.html
│   │           round17_chunk0_model_gemini-1_5-pro-latest_prompt_extraction_prompt_v2.8_continuous_with_markers_final_report.html
│   │           round19_chunk0_model_gemini-1_5-flash-latest_prompt_extraction_prompt_v2.8_continuous_with_markers_final_report.html
│   │           round1_chunk0_model_gemini-1_5-pro-latest_report.csv
│   │           round20_chunk0_model_gemini-2_0-flash_prompt_extraction_prompt_v2.8_continuous_with_markers_final_report.html
│   │           round25_chunk0_model_gemini-2_0-flash_prompt_extraction_prompt_v2.2.1_include_empty_lines_final_report.html
│   │           round27_chunk0_model_gemini-1_5-pro-latest_prompt_extraction_prompt_v2.2.1_include_empty_lines_final_report.html
│   │           round28_chunk0_model_gpt-4o_prompt_extraction_prompt_v2.2.1_include_empty_lines_final_report.html
│   │           round2_chunk0_model_gemini-1_5-pro-latest_prompt_v2.2_report.csv
│   │           round30_model_gemini-1.5-pro-latest_report.html
│   │           round31_model_gemini-2.5-pro_report.html
│   │           round32_model_gemini-2.5-pro_report.html
│   │           round34_model_gemini-1.5-pro-latest_report.html
│   │           round34_model_gemini-2.5-pro_report.html
│   │           round35_model_gemini-1.5-pro-latest_FINAL_report.html
│   │           round35_model_gemini-2.5-pro_FINAL_report.html
│   │           round36_chunk0_model_gemini-1.5-pro-latest_prompt_main_extraction_prompt_v3.0_final_report.html
│   │           round37_chunk0_model_gemini-2.5-pro_prompt_main_extraction_prompt_v3.0_final_report.html
│   │           round38_chunk0_model_gemini-2.5-pro_prompt_main_extraction_prompt_v4.0_text_diff_report.html
│   │           round39_chunk0_model_gemini-2.5-pro_prompt_main_extraction_prompt_v4.1_text_diff_report.html
│   │           round3_chunk0_model_gemini-1_5-pro-latest_prompt_v2.2.1_include_empty_lines_report.csv
│   │           round40_chunk0_model_gemini-2.5-pro_prompt_main_extraction_prompt_v4.1_text_diff_report.html
│   │           round45_chunk0_model_gemini-2.5-pro_prompt_main_extraction_prompt_v4.1_text_diff_report.html
│   │           round47_chunk0_model_gemini-2.5-pro_prompt_main_extraction_prompt_v4.1_text_diff_report.html
│   │           round49_chunk0_model_gemini-2.5-pro_prompt_main_extraction_prompt_v4.2_text_diff_report.html
│   │           round5_chunk0_model_gemini-1_5-pro-latest_prompt_v2.2.1_include_empty_lines_report.csv
│   │           round6_chunk0_model_gemini-2_5-pro_prompt_v2.2.1_include_empty_lines_report.csv
│   │           round7_chunk0_model_gemini-2_5-pro_prompt_v2.2.1_include_empty_lines_actual_content.txt
│   │           round7_chunk0_model_gemini-2_5-pro_prompt_v2.2.1_include_empty_lines_diff_report.html
│   │           round7_chunk0_model_gemini-2_5-pro_prompt_v2.2.1_include_empty_lines_expected_content.txt
│   │           round9_chunk0_model_gemini-1_5-pro-latest_prompt_v2.2.1_include_empty_lines_difflib_v1.0_report.html
│   │
│   └───truly_cleaned_parts
│           TRULY_CLEANED_full_ground_truth_protocol-0.json
│           TRULY_CLEANED_full_ground_truth_protocol-1.json
│           TRULY_CLEANED_full_ground_truth_protocol-10.json
│           TRULY_CLEANED_full_ground_truth_protocol-11.json
│           TRULY_CLEANED_full_ground_truth_protocol-2.json
│           TRULY_CLEANED_full_ground_truth_protocol-3.json
│           TRULY_CLEANED_full_ground_truth_protocol-4.json
│           TRULY_CLEANED_full_ground_truth_protocol-5.json
│           TRULY_CLEANED_full_ground_truth_protocol-6.json
│           TRULY_CLEANED_full_ground_truth_protocol-7.json
│           TRULY_CLEANED_full_ground_truth_protocol-8.json
│           TRULY_CLEANED_full_ground_truth_protocol-9.json
│
├───__pycache__
│       allocate_global_id_range.cpython-313.pyc
│       db_operations.cpython-313.pyc
│       find_witness_id_by_alias.cpython-313.pyc
│       get_or_create_session.cpython-313.pyc
│       parse_filename.cpython-313.pyc
│
├───דוקומנטים
│       ### מסמך רשמי קובץ חפיפה מאוחד v81.txt
│       61.txt
│       77.txt
│       80.txt
│       83 מסמך רשמי קובץ חפיפה מלא ומשולב.txt
│       llm_extraction_bakeoff_v0.6.py
│       PROJECT_BOOTSTRAP_V1.7.md
│       PROJECT_BOOTSTRAP_V1.7_HE.md
│       PROJECT_BOOTSTRAP_V2.0.txt
│       PROJECT_BOOTSTRAP_V2.1.md
│       PROJECT_BOOTSTRAP_V2.2.md
│       PROJECT_BOOTSTRAP_V2.3.md
│
└───מחסן
    │   llm_extraction_bakeoff_v0.4.py
    │   PROJECT_BOOTSTRAP_GENERATION_PROMPT_V2.md
    │   protocol_sample.pdf
    │   test_internal_parser.py
    │   test_word_extraction.py
    │   verify_word_integrity.py
    │   ניר חפץ 30-11-21.pdf
    │   עמוד ראשון פרגו ברנע 8-05-24.pdf
    │
    └───test_results
        └───run_20250620_195936
```