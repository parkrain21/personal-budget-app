import json
import pandas as pd
import psycopg2 as pg
import datetime as dt

with open('dbkeys.json') as f:
    config = json.load(f)
    
conn = pg.connect(
    dbname = config['dbname'],
    user = config['user'],
    password = config['password'],
    host = config['host'],
    port = config['port'],
)

def create_journal(date, debit, credit, amount, desc, cust=None):
    cur = conn.cursor()
    # process data input from user to postgres db
    cur.execute("""INSERT INTO journal (date, debit, credit, amount, desc, cust)
                    VALUES (%s, %s, %s, %s, %s, %s)""",
                    (date, debit, credit, amount, desc, cust))

    close_conn(cur,conn)

def view_journal():
    cur = conn.cursor()

    close_conn(cur,conn)
# returns records based on parameter (date=returns all entries for that day, gj_no= returns one.)

def update_journal():
    cur = conn.cursor()

    close_conn(cur,conn)
# allows user to modify existing entries

def delete_journal():
    cur = conn.cursor()

    close_conn(cur,conn)
# removes a record from the Journal (void)

# --------------------
def create_account():
    cur = conn.cursor()
    
    close_conn(cur,conn)
# adds a new account to the chart of accounts/tb

def get_account():
    cur = conn.cursor()
    cur.execute(""" 
    SELECT coa.account_code, coa.account_name, SUM(bal) total_balance

    FROM (
        (SELECT account_code code, SUM(amount) bal FROM accounts coa

            LEFT JOIN test_gj gj on coa.account_code = gj.debit
            GROUP BY account_code
            ORDER BY account_code)
        UNION ALL
        (SELECT account_code code, SUM(amount) * -1 bal FROM accounts coa

            LEFT JOIN test_gj gj on coa.account_code = gj.credit
            GROUP BY account_code
            ORDER BY account_code)) x

    RIGHT JOIN accounts coa ON coa.account_code = x.code

    GROUP BY account_code, account_name
    ORDER BY account_code
    """)

    raw_output = cur.fetchall() 
    df = pd.DataFrame(raw_output, columns=['Code', 'Description', 'Amount'])
    df['Amount'] = df['Amount'].fillna(0)
    close_conn(cur,conn)

    return df
# return a list of tuples of (code, accname, category and amount)

def update_account():
    cur = conn.cursor()

    close_conn(cur,conn)


def delete_account():
    cur = conn.cursor()
    
    close_conn(cur,conn)


def close_conn(cursor, connection):
    cursor.close()
    connection.close()

# df = get_account()
# amount = int((df.iloc[0,-1]))
# new = format(amount, ',.2f')
# print(new)