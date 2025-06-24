# db_operations.py

import sqlite3
from datetime import datetime

def add_document_record(cursor: sqlite3.Cursor, doc_id: str, session_id: str, doc_type: str, file_path: str, parent_id: str = None):
    now_iso = datetime.utcnow().isoformat()
    cursor.execute("""
        INSERT INTO processed_documents (document_id, session_id, document_type, file_path, parent_document_id, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (doc_id, session_id, doc_type, file_path, parent_id, now_iso))

def log_api_call(cursor: sqlite3.Cursor, session_id: str, page_num: int, metadata: dict):
    """Logs a single API call transaction to the llm_api_log table."""
    now_iso = datetime.utcnow().isoformat()
    cursor.execute("""
        INSERT INTO llm_api_log (timestamp, session_id, page_number_processed, prompt_token_count, 
                               candidates_token_count, total_token_count, finish_reason, calculated_cost)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        now_iso,
        session_id,
        page_num,
        metadata.get('prompt_token_count'),
        metadata.get('candidates_token_count'),
        metadata.get('total_token_count'),
        metadata.get('finish_reason'),
        metadata.get('cost', 0.0)
    ))