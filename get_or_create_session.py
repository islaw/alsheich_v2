# get_or_create_session.py

import sqlite3
from datetime import datetime
from allocate_global_id_range import allocate_global_id_range

def get_or_create_session(cursor: sqlite3.Cursor, witness_id: int, testimony_date: str) -> (str, bool):
    """Gets an existing session or creates a new one, allocating ID if new."""
    now_iso = datetime.utcnow().isoformat()
    
    cursor.execute("SELECT session_id FROM testimony_sessions WHERE witness_id = ? AND testimony_date = ?", (witness_id, testimony_date))
    result = cursor.fetchone()
    if result:
        return result[0], False

    new_id = f"ALS-{(allocate_global_id_range(cursor, 1)):07d}"
    cursor.execute("""
        INSERT INTO testimony_sessions (session_id, witness_id, testimony_date, last_updated, status)
        VALUES (?, ?, ?, ?, 'pending')
    """, (new_id, witness_id, testimony_date, now_iso))
    return new_id, True

def update_session_status(cursor: sqlite3.Cursor, session_id: str, status: str, cost: float, chunks: int, input_tokens: int, output_tokens: int):
    """Updates the final status of a session, including aggregated metadata."""
    now_iso = datetime.utcnow().isoformat()
    cursor.execute("""
        UPDATE testimony_sessions
        SET status = ?, total_cost = ?, total_chunks = ?, total_input_tokens = ?, total_output_tokens = ?, last_updated = ?
        WHERE session_id = ?
    """, (status, cost, chunks, input_tokens, output_tokens, now_iso, session_id))