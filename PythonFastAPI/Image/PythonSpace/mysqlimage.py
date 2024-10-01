"""
author:
Description:
Date:
Usage:
"""

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
import pymysql
import os
import shutil

app = FastAPI()

UPLOAD_FOLDER = 'uploads'  # uplads라는 폴더 만들기
if not os.path.exists(UPLOAD_FOLDER): #uploads 폴더 없으면
    os.makedirs(UPLOAD_FOLDER)        #uploads폴더 만들라

def connect():
    conn = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='qwer1234',
        db='phthon',
        charset='utf8'
    )
    return conn

@app.get("/insert")
async def insert(name: str=None, phone: str=None, address: str=None, relation: str=None, filename: str=None):
    conn = connect()
    curs = conn.cursor()

    try:
        sql = "insert into address(name, phone, address, relation, filename) values (%s,%s,%s,%s,%s)"
        curs.execute(sql,(name, phone, address, relation, filename)) # 순서는 위 순서
        conn.commit()
        conn.close()
        return {'result':'OK'}
    
    except Exception as e:
        conn.close()
        print("Error:", e)
        return {'result':'Error'}






@app.get("/update")
async def insert(seq : str = None, name : str = None, phone : str = None, address : str = None, relation : str = None):
    conn = connect()
    curs = conn.cursor()
    print("relation: ", relation)

    try:
        sql = "update address set name=%s, phone=%s, address=%s, relation=%s where seq=%s"
        curs.execute(sql, (name, phone, address, relation, seq))
        conn.commit()
        conn.close()

        return {"result" : "OK"}        
    except Exception as e:
        conn.close()
        print("Error :",e)
        return {"result" : "Error"}


@app.get("/updateAll")
async def insert(seq : str = None, name : str = None, phone : str = None, address : str = None, relation : str = None, filename : str = None):
    conn = connect()
    curs = conn.cursor()
    print("relation: ", relation)

    try:
        sql = "update address set name=%s, phone=%s, address=%s, relation=%s, filename=%s where seq=%s"
        curs.execute(sql, (name, phone, address, relation, filename, seq))
        conn.commit()
        conn.close()

        return {"result" : "OK"}        
    except Exception as e:
        conn.close()
        print("Error :",e)
        return {"result" : "Error"}











@app.post("/upload")
async def upload_file(file:UploadFile=File(...)):
    try:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename) # file
        with open(file_path, "wb") as buffer: #buffer라고 이름 지음 "wb" : write binarry
            shutil.copyfileobj(file.file, buffer) #buffer로 옮긴다
        return {'result': 'OK'}

    except Exception as e:
        print("Error", e)
        return({'result' : 'Error'})


@app.get("/select")
async def select():
    conn = connect()
    curs = conn.cursor()

    sql = 'select seq, name, phone, address, relation, filename from address order by name'
    curs.execute(sql)
    rows = curs.fetchall()
    conn.close()
    print(rows)
    return{'results' : rows}
    



@app.get("/view/{file_name}")
async def get_file(file_name: str):
    file_path = os.path.join(UPLOAD_FOLDER, file_name)
    if os.path.exists(file_path):
        return FileResponse(path=file_path, filename=file_name)
    return{'result' : 'Error'}



@app.delete("deleteFile/{file_name}")
async def delete_file(file_name:str):
    try: 
        file_path = os.path.join(UPLOAD_FOLDER, file_name)
        if os.path.exists(file_path):
            os.remove(file_path)
        return {'result':'OK'}
    except Exception as e:
        print ("Error:", e)
        return{'result': 'Error'}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000)  #파이썬 서버의 IP