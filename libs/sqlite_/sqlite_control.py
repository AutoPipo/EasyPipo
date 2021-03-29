'''
21.03.29
sqlite control
'''

import sqlite3 as sqlite
import numpy as np
import json
import base64
from io import BytesIO
import array

#   클래스로 만들어버리기

def get_db_query(dbname):
    return sqlite.connect(dbname)
    
def insertData(conn, session, image, canvas):
    c = conn.cursor()
    buffer = BytesIO()
    # b_image = base64.b64encode(image)
    # b_canvas = base64.b64encode(canvas)
    image = sqlite.register_adapter(np.array, blob)    
    canvas = sqlite.register_adapter(np.array, blob)    
    #sqlite3.register_converter("array", convert_array)
    
    sql = """
    INSERT INTO IMAGE (session, image, canvas)
    VALUES (?, ?, ?);
    """
    #c.execute(sql)
    c.execute(sql, ( session, image,  canvas ))
    try:
        c.execute(sql, ( session, image,  canvas ))
        conn.commit()
    except:
        print("Insert Database ERROR !!")
        print("Error Location: ./libs./sqlite_control/insertData()")
    finally: c.close()
    return True

def updateCanvas(conn, session, canvas):
    c = conn.cursor()
    sql = """
    UPDATE IMAGE SET canvas = {}
    WHERE session = {};
    """.format(canvas, session)
    
    try:
        c.execute(sql)
        conn.commit()
    except:
        print("Update Canvas ERROR !!")
        print("Error Location: ./libs./sqlite_control/updateCanvas()")
    finally: c.close()
    return True

def getCanvas(conn, session, index = -1):
    c = conn.cursor()
    sql = """
    SELECT canvas FROM IMAGE
    WHERE session = {}
    """.format(session)
    
    data = c.execute(sql).fetchall()[index]
    return data

def createTable(conn):
    if checkTable(conn): return True 
    
    c = conn.cursor()
    sql = """
    CREATE TABLE IMAGE(
        id integer PRIMARY KEY AUTOINCREMENT,
        session varchar(30) NOT NULL,
        image MEDIUMBLOB,
        canvas MEDIUMBLOB
    );
    """
    c.execute(sql)
    conn.commit()
    c.close()
    return False

def checkTable(conn):
    c = conn.cursor()
    # information_schema.tables
    sql = """
    SELECT COUNT(*)
    FROM  sqlite_master
    WHERE type='table'
    AND name = 'IMAGE' ;
    """
    
    if c.execute(sql).fetchone()[0] == 1:
        c.close()
        return True
    
    c.close()
    return False


