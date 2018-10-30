import sqlite3 as sql
from flask import session
from passlib.hash import sha256_crypt

def insertUser(request):
    con = sql.connect("user.db")
   
    sqlQuery = "select username from user_info where (username ='" + request.form['username'] + "')"
    cur = con.cursor()
    cur.execute(sqlQuery)
    row = cur.fetchone()
    
    if not row:
        cur.execute("INSERT INTO user_info (username,password,name,default_breakfast,default_lunch,default_snacks,default_dinner,mess_reg) VALUES (?,?,?,?,?,?,?,?)", (request.form['username'], 
                   sha256_crypt.encrypt(request.form['password']),request.form['name'],request.form['defaultb'],request.form['defaultl'],request.form['defaults'],request.form['defaultd'],request.form['defaultd']))
        con.commit()
        print "added user successfully"
       
    con.close()
    return not row


def authenticate(request):
    con = sql.connect("user.db")
    sqlQuery = "select password from user_info where username = '%s'"%request.form['username']  
    cursor = con.cursor()
    cursor.execute(sqlQuery)
    row = cursor.fetchone()
    con.close()
    if row:
       return sha256_crypt.verify(request.form['password'], row[0])
    else:
       return False


def retrieveUsers(): 
	con = sql.connect("user.db")
        # Uncomment line below if you want output in dictionary format
	#con.row_factory = sql.Row
	cur = con.cursor()
	cur.execute("SELECT * FROM user_info;")
	rows = cur.fetchall()
	con.close()
	return rows
def retrievePerson(username):
    con = sql.connect("user.db")
    sqlQuery = "select * from user_info where username = '%s'"%username
    cursor = con.cursor()
    cursor.execute(sqlQuery)
    row = cursor.fetchone()
    con.close()
    return row

  
