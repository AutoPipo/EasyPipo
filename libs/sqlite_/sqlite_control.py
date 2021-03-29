'''
# Start : 21.03.29
# Update : 21.03.30
# Author : Minku Koo
# SQLite Control Class
'''

import sqlite3, io, array
import numpy as np

class dbControl:
    def __init__(self, db_name):
        # self.db_name = db_name
        self.__conn = sqlite3.connect(db_name, detect_types=sqlite3.PARSE_DECLTYPES)
        # Converts np.array to TEXT when inserting
        sqlite3.register_adapter(np.ndarray, self.__adapt_array)

        # Converts TEXT to np.array when selecting
        sqlite3.register_converter("array", self.__convert_array)
        
    def insertData(self, session, image, canvas):
        c = self.__conn.cursor()
        
        sql = """
        INSERT INTO IMAGE (session, image, canvas)
        VALUES (?, ?, ?) ;
        """
        print("data insert")
        
        try:
            c.execute(sql, ( session, image,  canvas ))
            self.__conn.commit()
        except:
            print("Insert Database ERROR !!")
            print("Error Location: ./libs/sqlite_control/insertData()")
        finally: c.close()
        return 

    def updateCanvas(self, session, canvas):
        c = self.__conn.cursor()
        
        sql = """
        UPDATE IMAGE SET canvas = ? WHERE session = ? ;
        """
        print("data update")
        
        try:
            c.execute(sql, (canvas, session))
            self.__conn.commit()
        except:
            print("Update Canvas ERROR !!")
            print("Error Location: ./libs/sqlite_control/updateCanvas()")
        finally: c.close()
        return True

    def getCanvas(self, session, index = -1):
        c = self.__conn.cursor()
        sql = """
        SELECT canvas FROM IMAGE
        WHERE session = ? ;
        """
        
        data = c.execute(sql, (session, )).fetchone()[0]
        return data

    def createTable(self):
        if self.__checkTable(): 
            print("table exist!")
            return False 
        
        c = self.__conn.cursor()
        sql = """
        CREATE TABLE IMAGE(
            id integer PRIMARY KEY AUTOINCREMENT,
            session varchar(30) NOT NULL,
            image array,
            canvas array
        );
        """
        c.execute(sql)
        self.__conn.commit()
        c.close()
        return True
    
    def dbClose(self):
        self.__conn.close()
        return 
    
    def __checkTable(self):
        c = self.__conn.cursor()
        
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

    
    def __adapt_array(self, arr):
        """
        http://stackoverflow.com/a/31312102/190597 (SoulNibbler)
        """
        out = io.BytesIO()
        np.save(out, arr)
        out.seek(0)
        return sqlite3.Binary(out.read())

    def __convert_array(self, text):
        out = io.BytesIO(text)
        out.seek(0)
        return np.load(out)
