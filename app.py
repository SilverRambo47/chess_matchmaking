import sqlite3

# Function to get database connection
def get_db_connection():
    conn = sqlite3.connect('chess.db')
    conn.row_factory = sqlite3.Row
    return conn

def add_to_queue(ip, port, pseudo):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Queue (ip, port, pseudo, entry_date)
        VALUES (?, ?, ?, datetime('now'))
    ''', (ip, port, pseudo))
    conn.commit()
    conn.close()

def get_queue():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Queue ORDER BY entry_date')
    queue = cursor.fetchall()
    conn.close()
    return queue

def create_match(player1_ip, player1_port, player2_ip, player2_port, board):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Matches (player1_ip, player1_port, player2_ip, player2_port, board, is_finished, result)
        VALUES (?, ?, ?, ?, ?, 0, '')
    ''', (player1_ip, player1_port, player2_ip, player2_port, board))
    match_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return match_id

def update_match_result(match_id, is_finished, result):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE Matches
        SET is_finished = ?, result = ?
        WHERE id = ?
    ''', (is_finished, result, match_id))
    conn.commit()
    conn.close()

def add_turn(match_id, player, move):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Turns (match_id, player, move)
        VALUES (?, ?, ?)
    ''', (match_id, player, move))
    conn.commit()
    conn.close()
