# File: db_setup.py

import sqlite3

def create_tables():
    conn = sqlite3.connect('chess.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Queue (
        id INTEGER PRIMARY KEY,
        ip TEXT NOT NULL,
        port INTEGER NOT NULL,
        pseudo TEXT NOT NULL,
        entry_date TEXT NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Matches (
        id INTEGER PRIMARY KEY,
        player1_ip TEXT NOT NULL,
        player1_port INTEGER NOT NULL,
        player2_ip TEXT NOT NULL,
        player2_port INTEGER NOT NULL,
        board TEXT NOT NULL,
        is_finished BOOLEAN NOT NULL CHECK (is_finished IN (0, 1)),
        result TEXT NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Turns (
        id INTEGER PRIMARY KEY,
        match_id INTEGER NOT NULL,
        player TEXT NOT NULL,
        move TEXT NOT NULL,
        FOREIGN KEY (match_id) REFERENCES Matches (id)
    )
    ''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
