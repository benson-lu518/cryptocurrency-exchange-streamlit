import sqlite3 
conn = sqlite3.connect('data.db',check_same_thread=False)
# conn.row_factory = lambda cursor, row: row[0] #return list
c = conn.cursor()
class UserDao:
    def getAllUsernames():
        #retrun list first row
        conn.row_factory = lambda cursor, row: row[0] #expected only one row 
        c = conn.cursor()
        c.execute('SELECT username FROM userstable order by username')
        useraccounts=c.fetchall()
        c.row_factory = None
        return useraccounts
    
    def getAllPasswords():
        #retrun list first row 
        conn.row_factory = lambda cursor, row: row[0] #expected only one row 
        c = conn.cursor()
        c.execute('SELECT password FROM userstable order by username')
        passwords=c.fetchall()
        c.row_factory = None
        return passwords

    def getUserByUsername(username):
        #default return list[tuple(,)]
        c.execute('SELECT * FROM userstable WHERE username =?',(username,))
        userInfo=c.fetchall()
        return userInfo
    
    def getUserByPassword(password):
        #default return list[tuple(,)]
         c.execute('SELECT * FROM userstable WHERE password =?',(password,))
         userInfo=c.fetchall()
         return userInfo
    
    def getCashByUsername(username):
        #return float 
        c.execute('SELECT cash FROM userstable WHERE username=?',(username,))
        cashList=c.fetchall()
        return cashList[0][0] #list[tuple(cash,)]

    def updateCashByUsername(username,remainCash):
        c.execute('UPDATE userstable SET cash=? WHERE username=?',(remainCash,username))
        conn.commit()

    def insertUser(username,name,email,password,cash):
        c.execute('INSERT INTO userstable(username,name,email,password,cash) VALUES (?,?,?,?,?)',(username,name,email,password,cash))
        conn.commit()

    