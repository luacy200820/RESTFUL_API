import pymysql
from app import app
from config import mysql
from flask import jsonify
from flask import flask,request
import urllib.parse

@app.route("/")
def create_tabel():
    conn=mysql.connect()
    cursor = conn.cursor()
    sql = '''CREATE TABLE lab(`key` VARCHAR(255), `value` VARCHAR(255), PRIMARY KEY (`key`))'''
    cursor.execute(sql)
    conn.close()
    return "create new table!"

@app.route('/key',methods=['POST','GET'])
def key():
    if request.method == 'POST':
        result = request.get_json()
        key_ = urllib.parse.quote(result['key'],safe='"')
        value_ = urllib.parse.quote(result['value'],safe='"')

        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM lab WHERE `key`=%s",key_)
        rows = cursor.fetchall()
        if rows:
            res = jsonify('existed')
            res.status = 400
            return res

        else:
            sql = "INSERT INTO lab(`key`,`value`) VALUES(%s,%s)"
            data = (key_,value_)
            cursor.execute(sql,data)
            conn.commit()
            res = jsonify('insert successfully')
            res.status_code= 201
            return res
    
    else:
        ans = []
        sql = "SELECT `key` FROM lab"
        conn= mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            ans.append(urllib.parse.unquote(row['key']))

        res = jsonify(ans)
        res.status_code = 200
        return res

@app.route('/key/<path:msg>',methods=['PUT','GET','DELETE'])
def key_fetch(msg):
    if request.method == 'GET':
        msg = urllib.parse.quote(msg,safe='"')
        conn=mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM lab WHERE `key`=%s",msg)
        row = cursor.fetchall()
        if row:
            ans = {}
            for i in row:
                ans[urllib.parse.unquote(i['key'])] = urllib.parse.unquote(i['value'])
            res = jsonify(ans)
            res.status_code = 200
            return res
        else:
            res=jsonify("not found")
            res.status_code=404
            return res
    elif request.method =='PUT':
        
        result = request.get_json()
        msg = urllib.parse.quote(msg,safe='"')
        result = urllib.parse.quote(result['value'],safe='"')
        conn=mysql.connect()
        cursor= conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT `key` FROM lab WHERE `key`=%s",msg)
        row = cursor.fetchall()
        if row:
            cursor.execute("UPDATE lab set `value`=%s WHERE `key`=%s",(result,msg))
            conn.commit()
            res=jsonify("update successfully")
            res.status_code=200
            return res
        else:
            sql = "INSERT INTO lab(`key`,`value`) VALUES(%s,%s)"
            data = (msg,result)
            cursor.execute(sql,data)
            conn.commit()
            res=jsonify("insert successfully")
            res.status_code=201
            return res

    elif request.method == 'DELETE':
        msg = urllib.parse.quote(msg,safe='/')
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE from lab where `key`=%s",msg)
        conn.commit()
        res=jsonify("insert successfully")
        res.status_code=200

        return res


if __name__ == "__main__":
    app.run(host = "0.0.0.0",debug=True)

