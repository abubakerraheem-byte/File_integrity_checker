# ==========================================================
# HashGuard Pro Database
# ==========================================================

import sqlite3


def create_database():

    conn = sqlite3.connect("hashguard.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS history(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT,
        hash_value TEXT,
        status TEXT
    )
    """)

    conn.commit()
    conn.close()



def save_record(filename, hash_value, status):

    conn = sqlite3.connect("hashguard.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO history(filename, hash_value, status)
    VALUES(?,?,?)
    """,
    (filename, hash_value, status))

    conn.commit()
    conn.close()



def get_history():

    conn = sqlite3.connect("hashguard.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM history"
    )

    data = cursor.fetchall()

    conn.close()

    return data

# ==========================================================
# Integrity Monitoring Table
# ==========================================================

def create_integrity_table():

    conn = sqlite3.connect("hashguard.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS integrity(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT,
        filepath TEXT,
        hash_value TEXT
    )
    """)

    conn.commit()
    conn.close()



def save_integrity(filename, filepath, hash_value):

    conn = sqlite3.connect("hashguard.db")

    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO integrity(
        filename,
        filepath,
        hash_value
    )
    VALUES(?,?,?)
    """,
    (
        filename,
        filepath,
        hash_value
    ))

    conn.commit()
    conn.close()



def get_integrity():

    conn = sqlite3.connect("hashguard.db")

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM integrity"
    )

    data = cursor.fetchall()

    conn.close()

    return data

