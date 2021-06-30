import sqlite3

def connect(dbname):
    conn=sqlite3.connect(dbname)
    conn.execute("CREATE TABLE IF NOT EXISTS OYO_HOTELS(NAME TEXT,ADDRESS TEXT, PRICE INT, RATING TEXT,AMENITIES TEXT)")
    print("Table created successfully!")
    conn.close()


def insert_values(dbname,values):
    conn=sqlite3.connect(dbname)
    conn.execute("INSERT INTO OYO_HOTELS(NAME, ADDRESS, PRICE, RATING, AMENITIES) VALUES(?, ?, ?, ?, ?)",values)
    conn.commit()
    conn.close()


def get_info(dbname):
    conn=sqlite3.connect(dbname)
    cur=conn.cursor()
    cur.execute("SELECT * FROM OYO_HOTELS")
    data=cur.fetchall()

    for record in data:
        print(record)

    conn.close()
