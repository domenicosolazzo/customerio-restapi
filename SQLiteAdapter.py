# SQLite3 adapter
import sqlite3 as lite
class SQLiteAdapter(object):
    """
    SQLite3 adapter for the CustomerIo database
    """
    def __init__(self, dbName):
        self.dbName = dbName


    def saveEmail(self, email):
        conn = lite.connect(self.dbName)
        cursor = conn.cursor()
        result = cursor.execute("INSERT INTO Emails VALUES(NULL,?)", (email,))
        conn.commit()
        conn.close()
        return result

    def retrieveEmail(self, email):
        conn = lite.connect(self.dbName)
        cursor = conn.cursor()
        resultSet = cursor.execute("SELECT * FROM Emails WHERE Email LIKE ?", (email,))
        result = resultSet.fetchall()
        conn.close()
        return result

if __name__ == "__main__":
    email = raw_input('Which email do you want to add? ')
    db = SQLiteAdapter('test.db')
    print db.saveEmail(email)
    print db.retrieveEmail(email)