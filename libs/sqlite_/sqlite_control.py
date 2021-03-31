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
        # connect SQLite
        self.__conn = sqlite3.connect(db_name, detect_types=sqlite3.PARSE_DECLTYPES)
        
        # Converts np.array to TEXT when inserting
        sqlite3.register_adapter(np.ndarray, self.__adapt_array)
        # Converts TEXT to np.array when selecting
        sqlite3.register_converter("array", self.__convert_array)
        
    def insertData(self, session, image, canvas):
        """
        * Insert DB Data
        
        Parameters
            session <String> : Session ID
            image <nd.array> : Original Image Array
            canvas <nd.array> : Canvas Image
        returns
            None
        """
        c = self.__conn.cursor()
        
        sql =   """
                INSERT INTO IMAGE (session, image, canvas)
                VALUES (?, ?, ?) ;
                """
        
        try:
            c.execute(sql, ( session, image,  canvas ))
            self.__conn.commit()
        except:
            print("Insert Database ERROR !!")
            print("Error Location: ./libs/sqlite_control/insertData()")
        finally: c.close()
        
        return 

    def updateCanvas(self, session, canvas):
        """
        * Update DB Data
        
        Parameters
            session <String> : Session ID
            canvas <nd.array> : Canvas Image
        returns
            None
        """
        c = self.__conn.cursor()
        
        sql =   """
                UPDATE IMAGE SET canvas = ? WHERE session = ? ;
                """
        
        try:
            c.execute(sql, (canvas, session))
            self.__conn.commit()
        except:
            print("Update Canvas ERROR !!")
            print("Error Location: ./libs/sqlite_control/updateCanvas()")
        finally: c.close()
        
        return 

    def getCanvas(self, session, index = -1):
        """
        * Select DB Data
        
        Parameters
            session <String> : Session ID
            index <int> : Data Index
        returns
            data <nd.array> : Image Array
        """
        c = self.__conn.cursor()
        
        sql =   """
                SELECT canvas FROM IMAGE
                WHERE session = ? ;
                """
        try:
            data = c.execute(sql, (session, )).fetchall()
        except:
            print("Select DB Error !!")
            print("Error Location: ./libs/sqlite_control/getCanvas()")
        
        return data[index][0]
    
    def checkJobID(self, session):
        """
        * Check Job ID in DB
        
        Parameters
            session <String> : Session ID
        returns
            boolean : Job ID in DB or not
        """
        c = self.__conn.cursor()
        sql = "SELECT count(*) FROM IMAGE WHERE session = ? ;"
        try:
            data = c.execute(sql, (session, )).fetchone()[0]
            print("session in db count:", data)
            if data >0 :
                return True
            else:
                return False
        except:
            print("Select DB Error !!")
            print("Error Location: ./libs/sqlite_control/getCanvas()")
        
        return False
    
    def undoCanvas(self, session):
        """
        * Undo
        
        Parameters
            session <String> : Session ID
        returns
             <nd.array> : Image Array
        """
        self.__deleteCanvas(session)
        
        return self.getCanvas(session)
    
    def __deleteCanvas(self, session):
        """
        * Delete DB Last Data
        
        Parameters
            session <String> : Session ID
        returns
            None
        """
        c = self.__conn.cursor()
        
        try:
            sql =   """
                    SELECT id FROM IMAGE WHERE session = ? ;
                    """
            
            id = c.execute(sql, (session, )).fetchall()[-1][0]
            
            sql =   """
                    DELETE FROM IMAGE
                    WHERE session = ? AND id = ?;
                    """
        
            c.execute(sql, (session, id, ))
        except:
            print("Delete DB Error !!")
            print("Error Location: ./libs/sqlite_control/deleteCanvas()")
            
        return
    
    def createTable(self):
        """
        * Create Database Table
        * If table exists -> do not create
        
        returns
            Boolean <boolean> : Create Success
        """
        if self.__checkTable(): return False 
        
        c = self.__conn.cursor()
        sql =   """
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
        """
        * Close Database Connection
        """
        self.__conn.close()
        return 
    
    def __checkTable(self):
        """
        * table exists in table or not ? 
        
        returns
            Boolean <boolean> : Table Exists in DB
        """
        c = self.__conn.cursor()
        
        sql =   """
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

    # nd.array to text  when Insert DB
    def __adapt_array(self, arr):
        """
        http://stackoverflow.com/a/31312102/190597 (SoulNibbler)
        """
        out = io.BytesIO()
        np.save(out, arr)
        out.seek(0)
        return sqlite3.Binary(out.read())
    
    # text to nd.array when Select DB
    def __convert_array(self, text):
        out = io.BytesIO(text)
        out.seek(0)
        return np.load(out)
        
        
