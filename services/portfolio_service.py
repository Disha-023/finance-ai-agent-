import sqlite3


def init_portfolio_db():

    conn = sqlite3.connect("portfolio.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS portfolio (
            symbol TEXT,
            quantity INTEGER,
            buy_price REAL
        )
    """)

    conn.commit()
    conn.close()


def add_to_portfolio(symbol, quantity, buy_price):

    conn = sqlite3.connect("portfolio.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO portfolio
        VALUES (?, ?, ?)
        """,
        (symbol, quantity, buy_price)
    )

    conn.commit()
    conn.close()


def get_portfolio():

    conn = sqlite3.connect("portfolio.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM portfolio")

    data = cursor.fetchall()

    conn.close()

    return data