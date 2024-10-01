from fastapi import FastAPI
import pymysql

app = FastAPI()

def connect():
    conn = pymysql.connect(
        host ='127.0.0.1',
        user ='root',
        password='qwer1234',
        db='todolist',
        charset='utf8'
    )
    return conn

@app.get("/select")
async def select():
    conn = connect()
    curs = conn.cursor()

    sql = "select scode, sicon, smemo, sdate"
    curs.execute(sql)
    rows= curs.fetchall()
    conn.close()
    print(rows)


@app.get("/insert")
async def insert(code: str=None, icon: str = None, memo: str = None, date:str = None):
    conn = connect()
    curs = conn.cursor()

    try:
        sql = "insert into todolist(scode, sicon, smemo, sdate) values(%s,%s,%s,%s)"
        curs.execute()
        return {'results' : 'Ok'}
     
    except Exception as e:
        conn.close()
        print("Error:", e)
        return {'results':'Error'}
