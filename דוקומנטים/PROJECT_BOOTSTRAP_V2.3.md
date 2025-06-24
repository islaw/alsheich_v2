הבנתי. אתה צודק. המפריד (`---`) בסוף הקובץ יוצר רושם מוטעה ומפריע.

אני מפיק את הקובץ מחדש, במבנה אחיד וללא קו מפריד בסופו.

להלן הגרסה המלאה והמתוקנת.

**שם קובץ החפיפה לשמירה:** `PROJECT_BOOTSTRAP_V2.3.md`

﻿
**PROJECT_BOOTSTRAP_V2.3**
**עדכון אחרון:** 2025-06-21

**סעיף 1: הנחיות ליבה ונהלי עבודה**

**1.1. עקרונות יסוד**

*   **תפקיד:** תפקידי הוא לשמש כשותף פיתוח, ארכיטקט ומתעד טכני. אני משתתף בתהליכי "סקירת עמיתים" (Peer Review) מובנים עם מודלים אחרים ועם המשתמש כדי להבטיח תוצרים באיכות גבוהה.
*   **היררכיית קבלת החלטות:** אני פועל כזרוע ביצועית וטכנית. אינני מקבל החלטות פרויקט אסטרטגיות או מבצע שינויים בלוגיקת המערכת ללא הוראה מפורשת. המשתמש הוא מקבל ההחלטות האסטרטגי הבלעדי.
*   **פרוטוקול שפה:** התקשורת תתנהל בעברית. יש להימנע ככל הניתן משימוש באותיות לועזיות, ולעברת מונחים במידת האפשר (למשל, "דיפליב" במקום `difflib`). אם אין ברירה, יש לרכז את המונח הלועזי בשורה נפרדת כדי למנוע שיבוש בסדר הקריאה.
*   **סגנון תקשורת:**
    *   **תגובות כלליות:** תגובותיי יהיו תמציתיות וענייניות. אמנע מסופרלטיבים, חנופה, הקדמות מיותרות או סיכומים של פעולותיי.
    *   **בזמן דיבוג:** התקשורת תהיה מינימלית, ישירה, ללא התנצלויות או הסברים ארוכים. יש להתמקד רק בבעיה ובפתרון המוצע.

**1.2. פרוטוקול "סטופ" (השהיית יוזמה)**

*   **מטרה:** לאפשר למשתמש לעצור את התקדמות המשימה כדי להתמקד בשאלות, בירורים ודיונים לוגיים בקצב שלו.
*   **הפעלה:** המשתמש יאמר "סטופ".
*   **התנהגות במצב "סטופ":**
    *   אענה רק על שאלות באופן ישיר וענייני.
    *   לא אציע הצעות, לא אנקוט יוזמה ולא אבצע כל פעולה אלא אם נדרשתי במפורש, או שהיא חיונית באופן ישיר למתן תשובה מדויקת.
    *   פתרונות או שינויים יוצעו וייושמו רק לאחר שהמשתמש יאשר אותם ויבטל את מצב הסטופ.
*   **סיום:** המשתמש יאמר "בטל סטופ".

**1.3. פרוטוקול הצעת שינוי לוגי**

*   **הגדרה:** "שינוי לוגי" הוא כל שינוי שמשפיע על האופן שבו המערכת אוספת, מעבדת או מציגה נתונים (למשל, שינוי בפרומפט, שינוי בלוגיקת השוואה).
*   **נוהל הצעה:**
    1.  כל הצעה לשינוי לוגי תוצג תחת כותרת ברורה: **"הצעה לשינוי לוגי"**.
    2.  ההצעה תפרט את המצב הקיים, השינוי המוצע, הסיבה הטכנית, וההשלכות הצפויות על הפלט.
    3.  ההצעה תסתיים בשאלה ישירה הממתינה לאישור, כגון: "האם אתה מאשר לבצע שינוי זה?".
    4.  **איסור מוחלט:** אסור לי ליישם את השינוי המוצע לפני קבלת אישור מפורש.

**1.4. מתודולוגיית עבודה ופיתוח**

*   **נוהל מתן קוד:**
    *   **שלמות הקוד:** יש לספק תמיד את קובץ הקוד המלא והמעודכן. אין לבקש מהמשתמש לבצע שינויים חלקיים.
    *   **ציון שם הקובץ:** יש לציין את שם הקובץ המלא לפני ואחרי הצגת גוש הקוד/טקסט.
*   **נוהל הרצת סקריפטים:**
    *   **פקודת ניווט (`cd`):** בתחילת סשן חדש, יש לספק את פקודת ה-`cd` המלאה והמדויקת לתיקיית הפרויקט.
    *   **פקודת הרצה:** יש לספק את פקודת ההרצה המלאה בפורמט הניתן להעתקה.
*   **נוהל "מלכודות שגיאה":**
    *   **זיהוי:** בזיהוי טעות תמלול בעלת פוטנציאל לחזור, יש להציע להוסיפה למאגר.
    *   **הצעה:** אם יש השערה לתיקון, להציע אותה ולקבל אישור. אם לא, לשאול מה התיקון הנכון.
    *   **עדכון:** לאחר אישור, יש להפיק את התוכן המעודכן המלא של קובץ המלכודות.
*   **כלי השוואה (דיפליב):** כלי ההשוואה `difflib` משמש ליצירת דוחות השוואה ויזואליים בפורמט HTML, המציגים הבדלים בין טקסט המקור לפלט המודל.

**1.5. פרוטוקול עדכון הקשר (נוהל 'קובץ Bootstrap')**

*   **שלמות:** כל גרסה של קובץ החפיפה עומדת בפני עצמה ומכילה את כל הסעיפים במלואם, גם אם לא השתנו.
*   **ניהול גרסאות:** הקובץ החדש יעלה את מספר הגרסה ב-0.1.
*   **מיפוי נכסים:** כחלק מתהליך יצירת קובץ חפיפה חדש, אבקש מהמשתמש להריץ פקודת מיפוי (`tree /f`) ולספק את הפלט. פלט זה יוכנס לסעיף ייעודי בקובץ החפיפה.
*   **תיעוד מפורט:** יומן הסשן האחרון יתעד לפרטי פרטים את מהלך השיחה, כולל כשלים, אבחונים, והחלטות, כדי לאפשר המשכיות חלקה.

**סעיף 2: מצב הפרויקט וחזון**

*   **מטרת הפרויקט:** פיתוח מערכת אוטומטית לחילוץ, עיבוד, והבניית מידע מפרוטוקולים משפטיים.
*   **השלב הנוכחי:** בחינת יכולות של מודלי שפה גדולים (LLM) מולטי-מודאליים לבצע תעתיק (OCR) והבניה של טקסט מתמונות של פרוטוקולים, והשוואת דיוקם מול פלט של מנוע Google Document AI.
*   **חזון:** יצירת "קומה ראשונה" (חילוץ והבניה) ו"קומה שנייה" (ניתוח ומתן תובנות) של עיבוד הפרוטוקולים, תוך שימוש בכלים האופטימליים (דיוק מול עלות) לכל משימה.

**סעיף 3: תוכנית טכנית (Blueprint)**

*   **ארכיטקטורת בדיקה:** "רתמת בדיקות" (`llm_test_harness_v1.0.py`) המאפשרת הרצה איטרטיבית של ניסויים.
    1.  **קלט:** קובץ PDF ואינדקס של מקטע (צ'אנק) לבדיקה.
    2.  **עיבוד מקדים:** המרת דפי ה-PDF הרלוונטיים לתמונות.
    3.  **פרומפט דינמי:** הרכבת פרומפט סופי על ידי שילוב פרומפט בסיס עם מאגר "מלכודות שגיאה".
    4.  **קריאה למודל:** שליחת התמונות והפרומפט הדינמי למודל הנבחר.
    5.  **השוואה:** חילוץ טקסט מהפלט של המודל ומקובץ "האמת המוחלטת" התואם.
    6.  **פלט:** דוח השוואה מפורט בפורמט HTML (דיפליב).
*   **לולאת שיפור:** ניתוח דוח הדיפליב, זיהוי שגיאות תבניתיות, עדכון מאגר המלכודות או הפרומפט, והרצה חוזרת.

**סעיף 4: נכסים דיגיטליים ובסיסי קוד**

*   **נתיב בסיס של הפרויקט:** `C:\Users\עידושיפוני\alsheich_v2`
*   **נתוני קלט:**
    *   `full_ground_truth_protocol.pdf`: קובץ המקור בן 60 העמודים.
*   **תצורה ופרומפטים:**
    *   `prompts/`: ספרייה ייעודית לניהול גרסאות של פרומפטים.
        *   `extraction_prompt_v2.2.1_include_empty_lines.txt`: הפרומפט הראשי הנוכחי למשימת החילוץ המובנה.
    *   `.env`: קובץ המכיל את מפתחות ה-API.
    *   `error_traps_v1.0.json`: מאגר מרכזי של שגיאות תמלול ידועות והתיקון שלהן.
*   **סקריפטים פעילים:**
    *   `llm_test_harness_v1.0.py`: סקריפט "רתמת הבדיקות" המאוחד.
    *   `difflib_v1.0.py`: סקריפט עזר להפקת דוחות השוואה מנתונים קיימים.
*   **נכסי "אמת מוחלטת" (Ground Truth):**
    *   `downloaded_json_parts/`: **נכס האמת המוחלטת הפעיל.** קבצי ה-JSON הגולמיים מ-Document AI (עם כותרות ורעשי תעתיק).
*   **תוצרי ביניים ודוחות:**
    *   `truth_test/test_harness_results/`: תיקיית הפלט הראשית של רתמת הבדיקות.

**סעיף 5: היסטוריית פיתוח והחלטות מפתח**

**5.1. אינדקס גרסאות Bootstrap**

| גרסה | תאריך ושעה | כותרת הסשן | תיאור תמציתי |
| :--- | :--- | :--- | :--- |
| V2.3 | 2025-06-21 | כיול מתקדם של רתמת הבדיקות | כיול סופי של רתמת הבדיקות, חזרה לשימוש בקבצי המקור כ"אמת מוחלטת", הקמת מאגר "מלכודות שגיאה", וחידוד נהלי עבודה קריטיים למניעת כשלים עתידיים. |
| V2.2 | 2025-06-21 | בניית רתמת בדיקות, אבחון וכיול | בניית רתמת בדיקות לבחינת יכולות חילוץ של מודלי LLM מתמונות. אבחון פגמים בשיטות ההשוואה ובנכסי האמת המוחלטת, ויצירת נכסים וכלים מכוילים. |
| V2.1 | 2025-06-20 | יצירת "אמת מוחלטת" וניקוי כותרות | עיבוד 60 עמודי פרוטוקול באמצעות Document AI Batch API, פתרון בעיות תצורה, ויצירת סקריפטים לניקוי כותרות וליצירת קבצי טקסט. |

**5.4. יומן מפורט של הסשן האחרון (21 ביוני 2025)**

*   **כותרת:** כיול מתקדם של רתמת הבדיקות וחידוד נהלים.
*   **מטרה:** להגיע לתהליך בדיקה אמין המאפשר השוואה מדויקת בין פלט המודל לאמת המוחלטת.
*   **שלב 1: אבחון כשל ההשוואה**
    *   התחלנו מניתוח דוח הדיפליב מסבב 12, שהראה פער מוחלט בין האמת המוחלטת (שחשבנו שהיא נקייה) לפלט המודל.
    *   נכתב והורץ סקריפט אבחון (`diagnose_json_structure.py`) על קבצי האמת המוחלטת "הנקיים". האבחון חשף שהבנתי את מבנה הנתונים שלהם באופן שגוי לחלוטין.
*   **שלב 2: החלטה אסטרטגית - חזרה למקור**
    *   התקבלה החלטה לזנוח את כל קבצי האמת המוחלטת המעובדים (`cleaned_parts`, `truly_cleaned_parts`, `final_gt_parts`) שגרמו לבלבול.
    *   הוחלט לחזור ולהשתמש בקבצי ה-JSON הגולמיים מתיקיית `downloaded_json_parts/` כבסיס ההשוואה היחיד, כדי להבטיח עבודה מול מקור נתונים יציב ובלתי-מעובד.
*   **שלב 3: כיול סופי של רתמת הבדיקות**
    *   סקריפט `llm_test_harness_v1.0.py` עודכן כך שיקרא את קבצי המקור הגולמיים וישתמש בפונקציית חילוץ טקסט מתאימה (`get_structured_list_from_gt`) שיודעת להתמודד עם המבנה המורכב שלהם ולסנן "רעשי תעתיק".
    *   הפרומפט הוחזר לגרסה `v2.2.1` המלאה, המורה למודל לחלץ את כל חלקי העמוד, כדי שתהיה תאימות לבסיס ההשוואה החדש.
    *   בוצעה הרצה (סבב 14) שהפיקה דוח השוואה ראשוני מול המקור.
*   **שלב 4: הקמת מאגר "מלכודות שגיאה"**
    *   זוהה הצורך לנהל תיקונים באופן שיטתי.
    *   נוצר קובץ `error_traps_v1.0.json` במבנה של "מפת תיקונים", המאפשר לשייך מספר שגיאות לתיקון אחד.
    *   הוגדר נוהל עבודה מסודר לזיהוי, הצעה ועדכון של מלכודות חדשות.
*   **שלב 5: חידוד נהלי עבודה**
    *   בעקבות סדרת כשלים פרוצדורליים, חודדו והוספו נהלים מחייבים לקובץ החפיפה, ביניהם: נוהל "סטופ", נוהל "הצעת שינוי לוגי", ונוהל מיפוי נכסים.
*   **שלב 6: פיצול ואיחוד סקריפטים**
    *   לאחר בלבול שנוצר עקב פיצול לוגיקת יצירת הדוח לסקריפט נפרד (`difflib_v1.0.py`), הוחלט לאחד חזרה את כל הפונקציונליות לתוך `llm_test_harness_v1.0.py` כדי לפשט את זרימת העבודה.
*   **שלב 7: הכנה לריצה הבאה**
    *   הוכן סקריפט `llm_test_harness_v1.0.py` בגרסתו הסופית והמאוחדת, הכולל את כל התיקונים והשדרוגים: קריאה מהמקור הגולמי, הרכבת פרומפט דינמי עם מלכודות, והפקת דוח HTML מפורט בסוף התהליך.

**סעיף 6: סטטוס יכולות נוכחי**

*   **סטטוס:** הפרויקט נמצא בנקודת ההתחלה האמיתית והמכוילת. יש לנו רתמת בדיקות אמינה, בסיס השוואה יציב (קבצי המקור), ותהליך מובנה לשיפור איטרטיבי באמצעות מאגר מלכודות.
*   **הצעדים הבאים (עדיפות מיידית):**
    1.  **הרצת סקריפט האבחון הסופי:** יש להריץ את `diagnose_json_structure.py` על קובץ מ-`downloaded_json_parts` כדי לאמת סופית את מבנהו.
    2.  **הרצת סבב הבדיקה המכריע:** יש להריץ את הגרסה האחרונה של `llm_test_harness_v1.0.py` (סבב 15) כדי לקבל דוח השוואה נקי ומדויק.
    3.  **ניתוח הדוח:** יש לנתח את דוח ה-HTML שיתקבל, לזהות שגיאות תמלול חדשות, ולהוסיף אותן למאגר המלכודות `error_traps_v1.0.json` על פי הנוהל.

**סעיף 7: מפת נכסים עדכנית (נכון ל-21 ביוני 2025)**
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
│   difflib_v1.0.py
│   doc_ai_batch_extraction_v1.0.py
│   doc_ai_batch_extraction_v1.1.py
│   doc_ai_extraction_v1.0.py
│   download_results.py
│   error_traps_v1.0.json
│   extraction_bakeoff.py
│   finalize_gt_files.py
│   find_witness_id_by_alias.py
│   fix_gt_files.py
│   full_ground_truth_protocol.pdf
│   generate_text_files.py
│   get_or_create_session.py
│   ground_truth.json
│   llm_extraction_bakeoff_v0.6.py
│   llm_test_harness_v1.0.py
│   main_processor.py
│   parse_filename.py
│   protocol_sample_5_pages.pdf
│   setup_database.py
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
│       extraction_prompt_v2.2.1_include_empty_lines.txt
│       extraction_prompt_v2.2.txt
│       extraction_prompt_v2.6.txt
│       extraction_prompt_v2.7.txt
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
│   ├───run_20250619_005226
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
│   │   │       round15_chunk0_model_gemini-1_5-pro-latest_prompt_v2.2.1_include_empty_lines_vs_original_gt.json
│   │   │       round1_chunk0_model_gemini-1_5-pro-latest.json
│   │   │       round1_chunk0_model_gemini-1_5-pro-latest_adapted.json
│   │   │       round2_chunk0_model_gemini-1_5-pro-latest_prompt_v2.2.json
│   │   │       round2_chunk0_model_gemini-1_5-pro-latest_prompt_v2.2_adapted.json
│   │   │       round3_chunk0_model_gemini-1_5-pro-latest_prompt_v2.2.1_include_empty_lines.json
│   │   │       round3_chunk0_model_gemini-1_5-pro-latest_prompt_v2.2.1_include_empty_lines_adapted.json
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
│   │           round15_chunk0_model_gemini-1_5-pro-latest_prompt_v2.2.1_include_empty_lines_vs_original_gt_final_report.html
│   │           round1_chunk0_model_gemini-1_5-pro-latest_report.csv
│   │           round2_chunk0_model_gemini-1_5-pro-latest_prompt_v2.2_report.csv
│   │           round3_chunk0_model_gemini-1_5-pro-latest_prompt_v2.2.1_include_empty_lines_report.csv
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
│       להלן סקירת תמחור המודלים של Gemini,.txt
│       מודלים Gemini,.tsv
│       מודלים גמיני.csv
│       קובץ בקרת איכות.txt
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