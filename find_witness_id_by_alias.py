# find_witness_id_by_alias.py

import sqlite3
import re

class WitnessNotFoundError(Exception): pass
class MultipleWitnessesFoundError(Exception): pass

def _normalize_name_for_db(name: str) -> str:
    return re.sub(r'[\s_-]+', '', name).lower()

def find_witness_id_by_alias(conn: sqlite3.Connection, alias_name: str) -> int:
    normalized_input = _normalize_name_for_db(alias_name)
    conn.create_function("NORMALIZE", 1, _normalize_name_for_db)
    cursor = conn.cursor()
    cursor.execute("SELECT witness_id FROM witness_aliases WHERE NORMALIZE(alias_name) = ?", (normalized_input,))
    results = cursor.fetchall()
    
    if not results:
        raise WitnessNotFoundError(f"No witness found for alias '{alias_name}'")
    
    unique_ids = {row[0] for row in results}
    if len(unique_ids) > 1:
        raise MultipleWitnessesFoundError(f"Alias '{alias_name}' matches multiple witnesses: {unique_ids}")
        
    return results[0][0]