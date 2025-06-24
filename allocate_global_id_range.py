# allocate_global_id_range.py (v25.1 - DB Fix)

import sqlite3

class GlobalIDError(Exception): pass

def allocate_global_id_range(cursor: sqlite3.Cursor, count: int) -> int:
    try:
        # Select the single row where our counter lives
        cursor.execute("SELECT counter FROM global_id_counter WHERE singleton = 1")
        current_val_tuple = cursor.fetchone()
        if not current_val_tuple:
            raise GlobalIDError("Global ID counter is not initialized correctly.")

        current_val = current_val_tuple[0]
        new_val = current_val + count

        # Update the single row
        cursor.execute("UPDATE global_id_counter SET counter = ? WHERE singleton = 1", (new_val,))
        return current_val

    except sqlite3.Error as e:
        raise GlobalIDError(f"Database error during ID allocation: {e}") from e