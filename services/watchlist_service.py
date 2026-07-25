import sqlite3

# Creates SQLite database and watchlist table
# Used to store user watchlist stocks permanently

def init_db():
    conn = sqlite3.connect("watchlist.db")

    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS Watchlist(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT UNIQUE
            )
    """)

    conn.commit()
    conn.close()



def add_stock(symbol):

    conn = sqlite3.connect("watchlist.db")

    cursor = conn.cursor()

    cursor.execute(
        "INSERT OR IGNORE INTO watchlist(symbol) VALUES (?)",
        (symbol,)
    )

    conn.commit()
    conn.close()



def get_watchlist():

    conn = sqlite3.connect("watchlist.db")

    cursor = conn.cursor()

    cursor.execute(
        "SELECT symbol FROM watchlist"
    )

    data = cursor.fetchall()

    conn.close()

    return data