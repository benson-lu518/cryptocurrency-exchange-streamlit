import sqlite3 
conn = sqlite3.connect('data.db')
conn.row_factory = lambda cursor, row: row[0]
c = conn.cursor()


def drop_table():
    c.execute('DROP TABLE IF EXISTS userstable')
    c.execute('DROP TABLE IF EXISTS tradingInfo')
    c.execute('DROP TABLE IF EXISTS holdinginfo')
    conn.commit()


def create_table():
    c.execute(
        '''
       CREATE TABLE IF NOT EXISTS userstable
       (
       username TEXT PRIMARY KEY,
       name TEXT,
       email TEXT,
       password TEXT,
       cash NUMERIC
       )
       ''')
    c.execute(
        '''
       CREATE TABLE IF NOT EXISTS tradinginfo
       (
       trade_id INTEGER PRIMARY KEY AUTOINCREMENT,
       username TEXT,
       currency TEXT,
       amount NUMERIC,
       quantity NUMERIC,
       price NUMERIC,
       createddate TIMESTAMP,
       FOREIGN KEY(username) REFERENCES userstable(username)
       )
       ''')
    c.execute(
        '''
        CREATE TABLE IF NOT EXISTS holdinginfo
        (
        holding_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT, 
        currency TEXT,
        amount NUMERIC,
        quantity NUMERIC,
        boughtprice NUMERIC,
        createddate TIMESTAMP,
        lastUpdateddate TIMESTAMP,
        FOREIGN KEY(username) REFERENCES userstable(username)
        ) 
        '''
    )
    conn.commit()

if __name__ == '__main__':
    drop_table()
    create_table()
