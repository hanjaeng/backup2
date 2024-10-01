# -*- coding: utf-8 -*-
"""
author      : Kenny
Description : MYSQL의 Pytion Database와 CRUD on Web
Usage1      : http://127.0.0.1/select
Usage       : http://127.0.0.1/insert?code=a001
"""
# Usage       : http://127.0.0.1/insert?id=...
# Usage       : http://127.0.0.1/insert?code=a001
# Usage       : http://127.0.0.1:5000/insert?code=a001&name=james&dept=math&phone=001&address=seoul

from flask import Flask, jsonify, request
import pymysql
import json

app = Flask(__name__)
app.config['JSON_AS_ASCII']  = False # for utf8 (한글이 깨질수 있어서)

def connection():   #외부에서는 모름(내부에서만 씀)
    # MySQL Connection
    conn = pymysql.connect(
        host="127.0.0.1",   # 데이터베이스 ip
        user="root",
        password="qwer1234",
        db="education",
        charset="utf8"
    )
    return conn

@app.route("/select") # 위의  Usage1 : http://127.0.0.1/insert
def select():  #select의 함수가 실행됨
    conn = connection()
    curs = conn.cursor()

    #sql 문장
    sql = "select * from student"
    curs.execute(sql)
    row = curs.fetchall()
    conn.close()
    print(row)

    # JSON 만들기
    result = json.dumps(row, ensure_ascii=False).encode('utf8')
    # return result
    return result
    

@app.route("/insert")
def insert():
    code = request.args.get("code")
    name = request.args.get("name")
    dept = request.args.get("dept")
    phone = request.args.get("phone")
    address = request.args.get("address")

    conn = connection()
    curs = conn.cursor()

    sql = "insert into student(scode, sname, sdept, sphone, saddress) value(%s,%s,%s,%s,%s)"
    curs.execute(sql, (code, name,dept, phone, address))
    conn.commit()
    return jsonify([{'result' : 'OK'}])

 

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True) # 서버 ip