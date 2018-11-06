import sqlite3 as sql
from flask import session
from passlib.hash import sha256_crypt
#import datetime
from datetime import datetime
from datetime import date
from datetime import timedelta
import ast
import calendar
def datelist():
    ls=[]
    #date = datetime.now().date()
    date = datetime(2018,8,1,12,4,5)
    dstr = date.strftime("%d-%m-%Y")
    year = dstr.split('-')[2]
    year = int(year)
    if (year)%400==0 or (year+1)%400==0:
        loop=366
    elif (year)%100==0 or (year+1)%100==0:
        loop=365
    elif (year)%4==0 or (year+1)%4==0:
        loop=366
    else:
        loop=365
    for i in range(loop):
        ls.append(date.strftime("%d-%m-%Y"))
        date += timedelta(days=1)
    return ls
def datewise(request):
    print()
    #get the dates for which mess is needed to change. do almost as same as daywise
def daywise(request):
    print()
    #make database connection and take the mess_reg field and convert the string to dictionary.
    
    #dictionary = ast.literal_eval({insert the mess_reg string field})
    #for key, value in dictionary.items():
    #    dat = datetime.strptime(key, "%d-%m-%Y")
    #    day = calendar.day_name[dat.weekday()]
        # if(day==request['day']):
        #     if(request['breakfast']==True):
        #         value[0]=request['mess']
        #     if(request['lunch']==True):
        #         value[1]=request['mess']
        #     if(request['snacks']==True):
        #         value[2]=request['mess']
        #     if(request['dinner']==True):
        #         value[3]=request['mess']
    #send to database for the given request username
def insertUser(request):
    con = sql.connect("user.db")
    
    sqlQuery = "select username from user_info where (username ='" + request.form['username'] + "')"
    cur = con.cursor()
    cur.execute(sqlQuery)
    row = cur.fetchone()
    
    if not row:
        ls = datelist()
        breakfast = request.form['defaultb']
        lunch = request.form['defaultl']
        snack = request.form['defaults']
        dinner = request.form['defaultd']
        datedict = dict()
        meal=[breakfast,lunch,snack,dinner]
        for a in ls:
            datedict[a]=meal
        datestr= str(datedict)
        cur.execute("INSERT INTO user_info (username,password,name,default_breakfast,default_lunch,default_snacks,default_dinner,mess_reg) VALUES (?,?,?,?,?,?,?,?)", (request.form['username'], 
                   sha256_crypt.encrypt(request.form['password']),request.form['name'],request.form['defaultb'],request.form['defaultl'],request.form['defaults'],request.form['defaultd'],datestr))
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

  
