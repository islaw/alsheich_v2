# setup_database.py (v25.1 - DB Fix)

import sqlite3
import logging
import os

DB_PATH = 'data/alsheich_project.db'
LOG_FILE = 'logs/setup_database.log'

def setup_logging():
    os.makedirs('logs', exist_ok=True)
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        handlers=[logging.FileHandler(LOG_FILE, 'w', 'utf-8'), logging.StreamHandler()])

def setup_database():
    os.makedirs('data', exist_ok=True)
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        logging.info(f"Database connection established at {DB_PATH}")

        # --- Robust Global ID Counter Table ---
        cursor.execute('''CREATE TABLE IF NOT EXISTS global_id_counter (
                            singleton INTEGER PRIMARY KEY DEFAULT 1,
                            counter INTEGER NOT NULL
                         );''')
        cursor.execute("INSERT OR IGNORE INTO global_id_counter (singleton, counter) VALUES (1, 1000);")
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS witnesses (witness_id INTEGER PRIMARY KEY, full_name TEXT NOT NULL UNIQUE);''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS witness_aliases (alias_id INTEGER PRIMARY KEY, witness_id INTEGER NOT NULL, alias_name TEXT NOT NULL UNIQUE, FOREIGN KEY (witness_id) REFERENCES witnesses (witness_id));''')
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS testimony_sessions (
                            session_id TEXT PRIMARY KEY, 
                            witness_id INTEGER NOT NULL, 
                            testimony_date TEXT NOT NULL, 
                            status TEXT,
                            total_cost REAL DEFAULT 0,
                            total_chunks INTEGER DEFAULT 0,
                            total_input_tokens INTEGER DEFAULT 0,
                            total_output_tokens INTEGER DEFAULT 0,
                            last_updated TEXT,
                            FOREIGN KEY (witness_id) REFERENCES witnesses (witness_id));''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS processed_documents (
                            document_id TEXT PRIMARY KEY,
                            session_id TEXT NOT NULL,
                            document_type TEXT NOT NULL,
                            file_path TEXT,
                            parent_document_id TEXT,
                            created_at TEXT,
                            FOREIGN KEY (session_id) REFERENCES testimony_sessions(session_id));''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS llm_api_log (
                            log_id INTEGER PRIMARY KEY,
                            timestamp TEXT NOT NULL,
                            session_id TEXT NOT NULL,
                            page_number_processed INTEGER,
                            prompt_token_count INTEGER,
                            candidates_token_count INTEGER,
                            total_token_count INTEGER,
                            finish_reason TEXT,
                            calculated_cost REAL,
                            FOREIGN KEY (session_id) REFERENCES testimony_sessions(session_id));''')
        
        witnesses_data = {
            "ניר חפץ": ["ניר חפץ", "נירחפץ", "חפץ", "ניר"],
            "עמיקם שורר": ["עמיקם שורר", "עמיקםשורר", "שורר", "עמיקם"],
            "פרגו ברנע": ["פרגו ברנע", "פרגוברנע", "ברנע", "פרגו"],
            "ההגנה": ["ההגנה"]
        }
        
        logging.info("Populating database with comprehensive witness and alias list...")
        for name, aliases in witnesses_data.items():
            cursor.execute("INSERT OR IGNORE INTO witnesses (full_name) VALUES (?)", (name,))
            conn.commit()
            cursor.execute("SELECT witness_id FROM witnesses WHERE full_name = ?", (name,))
            witness_id_result = cursor.fetchone()
            if witness_id_result:
                witness_id = witness_id_result[0]
                for alias in aliases:
                    cursor.execute("INSERT OR IGNORE INTO witness_aliases (witness_id, alias_name) VALUES (?, ?)", (witness_id, alias))
        logging.info("Initial witnesses and aliases populated or verified.")

        conn.commit()
        logging.info("Database setup complete.")

    except sqlite3.Error as e:
        logging.critical(f"A database error occurred: {e}", exc_info=True)
    finally:
        if conn:
            conn.close()
            logging.info("Database connection closed.")


if __name__ == '__main__':
    setup_logging()
    if os.path.exists(DB_PATH):
        try:
            os.remove(DB_PATH)
            logging.info(f"Removed old database file at {DB_PATH} for a clean setup.")
        except OSError as e:
            logging.critical(f"Could not remove existing database file: {e}")
    setup_database()