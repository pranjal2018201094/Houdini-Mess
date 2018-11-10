import sqlite3 as sql
from flask import session
from passlib.hash import sha256_crypt
import datetime
import ast
import json
import re
def datelist():
    ls=[]
    #date = datetime.datetime.now().date()
    date = datetime.datetime(2018,8,1,12,4,5)
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
        date += datetime.timedelta(days=1)
    return ls
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
    # print(row)
    return row

def retrieveTodaysMess(username):
    con = sql.connect("user.db")
    sqlQuery = "select * from user_info where username = '%s'"%username
    cursor = con.cursor()
    cursor.execute(sqlQuery)
    row = cursor.fetchone()
    # string to Dictionary
    dictionary = ast.literal_eval(row[6])
    # retrieve todays meal
    y =datetime.datetime.today().strftime('%d-%m-%Y')
    # print y
    todays_mess = dictionary[y]
    con.close()
    return todays_mess

##todays menu 

def retrieveTodaysMenu(username):
    con = sql.connect("user.db")
    sqlQuery = "select * from user_info where username = '%s'"%username
    cursor = con.cursor()
    cursor.execute(sqlQuery)
    row = cursor.fetchone()
    # string to Dictionary
    dictionary = ast.literal_eval(row[6])
    # retrieve todays meal
    y =datetime.datetime.today().strftime('%d-%m-%Y')
    # print y
    todays_mess = dictionary[y]
    con.close()
    con = sql.connect("admin.db")



def calendarGenerate(username):
    con = sql.connect("user.db")
    sqlQuery = "select * from user_info where username = '%s'"%username
    cursor = con.cursor()
    cursor.execute(sqlQuery)
    row = cursor.fetchone()
    # string to Dictionary
    dictionary = ast.literal_eval(row[6])
    y =datetime.datetime.today().strftime('%d-%m-%Y')
    t = "title"
    st = "start"
    li = ["T07:00:00-05:00","T12:00:00-05:00","T17:00:00-01:00","T20:00:00-05:00"]
    list_json =[]
    for key, value in dictionary.items():
        s = key.split('-')
        d = s[2]+'-'+s[1]+'-'+s[0]
        x=0
        for i in value:
            data = {}
            data['title'] = i.capitalize()
            data['start'] = d+li[x]
            x=x+1
            list_json.append(json.dumps(data))
    con.close()
    line = re.sub("'", "", str(list_json))
    # return Response(json.dumps(list_json),  mimetype='application/json')
    # print(line)
    file_name = ".events_"+username+".json"
    with open(file_name,"w") as f:
        f.write(line)
        f.close()






########----- Refer Ipynb for more details on input and output ###############################
def updateMess(request):
    con = sql.connect("admin.db")
    
    sqlQuery = "select Admin from mess_menu where (Admin ='" + request.form['Admin'] + "')"
    cur = con.cursor()
    cur.execute(sqlQuery)
    row = cur.fetchone()
    if row:
        admin = request.form['Admin']
        day = request.form['day']

        ls = ['breakfast','lunch','snack','dinner']
        
        mess = request.form['mess']
        
        breakfast = request.form['bmenu']
        lunch = request.form['lmenu']
        snack = request.form['smenu']
        dinner = request.form['dmenu']
        

        ##---------Menu change
        menu=[breakfast,lunch,snack,dinner]  ## for a particular day
        i=0
        menu_dict = dict()
        for a in ls:
            menu_dict[a]=menu[i]
            i=i+1
            
        menu_dic = str(menu_dict)

        ##-------------
    
        breakfast_b = request.form['bb']
        lunch_b = request.form['lb']
        snack_b = request.form['sb']
        dinner_b = request.form['db']
        bill=[breakfast_b,lunch_b,snack_b,dinner_b]  ## for a particular day

        # bill change

        bill_dict = dict()
        i=0
        for a in ls:
            bill_dict[a]=bill[i]
            i=i+1
        bill_dic = str(bill_dict)

        # if day == 'Mon':
        #     cur.execute(("UPDATE mess_menu SET Bill = ?, Mon =? WHERE (Admin = ?)"),(bill_dic,menu_dic,admin))
        # elif day == 'Tue':
        #     cur.execute(("UPDATE mess_menu SET Bill = ?, Tue =? WHERE (Admin = ?)"),(bill_dic,menu_dic,admin))
        # elif day == 'Wed':
        #     cur.execute(("UPDATE mess_menu SET Bill = ?, Wed =? WHERE (Admin = ?)"),(bill_dic,menu_dic,admin))
        # elif day == 'Thu':
        #     cur.execute(("UPDATE mess_menu SET Bill = ?, Thu =? WHERE (Admin = ?)"),(bill_dic,menu_dic,admin))
        # elif day == 'Fri':
        #     cur.execute(("UPDATE mess_menu SET Bill = ?, Fri =? WHERE (Admin = ?)"),(bill_dic,menu_dic,admin))
        # elif day == 'Sat':
        #     cur.execute(("UPDATE mess_menu SET Bill = ?, Sat =? WHERE (Admin = ?)"),(bill_dic,menu_dic,admin))
        # elif day == 'Sun':
        #     cur.execute(("UPDATE mess_menu SET Bill = ?, Sun =? WHERE (Admin = ?)"),(bill_dic,menu_dic,admin))
        
        sqlq ="UPDATE mess_menu SET Bill = ?,"+day+"=? WHERE (Admin = ?)"
        cur.execute(sqlq,(bill_dic,menu_dic,admin))
        
        con.commit()
    con.close()
    return not row


#############################################################################################################


def retrieveMessMenuNorth(username):

    con = sql.connect("admin.db")
    sqlQuery = "select * from mess_menu where (mess ='" + 'North' + "')"
    cur = con.cursor()
    cur.execute(sqlQuery)
    row = cur.fetchone()
    # list_north = [[[]]]

    ###      list[Day][Meals]   Day:: 0->mon, 1->tue ... Meal:: 0->break, 1->lunch, 2->snack, 3->Dinner

    list_north = [[ [] for col in range(4)] for rows in range(7)]
    d_m = ast.literal_eval(row[2])
    d_t = ast.literal_eval(row[3])
    d_w = ast.literal_eval(row[4])
    d_th = ast.literal_eval(row[5])
    d_f = ast.literal_eval(row[6])
    d_s = ast.literal_eval(row[7])
    d_su = ast.literal_eval(row[8])
    list_north[0][0].append(d_m['breakfast'])
    list_north[0][1].append(d_m['lunch'])
    list_north[0][2].append(d_m['snack'])
    list_north[0][3].append(d_m['dinner'])

    list_north[1][0].append(d_t['breakfast'])
    list_north[1][1].append(d_t['lunch'])
    list_north[1][2].append(d_t['snack'])
    list_north[1][3].append(d_t['dinner'])

    list_north[2][0].append(d_w['breakfast'])
    list_north[2][1].append(d_w['lunch'])
    list_north[2][2].append(d_w['snack'])
    list_north[2][3].append(d_w['dinner'])

    list_north[3][0].append(d_th['breakfast'])
    list_north[3][1].append(d_th['lunch'])
    list_north[3][2].append(d_th['snack'])
    list_north[3][3].append(d_th['dinner'])

    list_north[4][0].append(d_f['breakfast'])
    list_north[4][1].append(d_f['lunch'])
    list_north[4][2].append(d_f['snack'])
    list_north[4][3].append(d_f['dinner'])

    list_north[5][0].append(d_s['breakfast'])
    list_north[5][1].append(d_s['lunch'])
    list_north[5][2].append(d_s['snack'])
    list_north[5][3].append(d_s['dinner'])

    list_north[6][0].append(d_su['breakfast'])
    list_north[6][1].append(d_su['lunch'])
    list_north[6][2].append(d_su['snack'])
    list_north[6][3].append(d_su['dinner'])
    
    con.close()    

    return list_north

#########################################################################################################


def retrieveMessMenuSouth(username):

    con = sql.connect("admin.db")
    sqlQuery = "select * from mess_menu where (mess ='" + 'South' + "')"
    cur = con.cursor()
    cur.execute(sqlQuery)
    row = cur.fetchone()
    # list_south = [[[]]]

    ###      list[Day][Meals]   Day:: 0->mon, 1->tue ... Meal:: 0->break, 1->lunch, 2->snack, 3->Dinner

    list_south = [[ [] for col in range(4)] for rows in range(7)]
    d_m = ast.literal_eval(row[2])
    d_t = ast.literal_eval(row[3])
    d_w = ast.literal_eval(row[4])
    d_th = ast.literal_eval(row[5])
    d_f = ast.literal_eval(row[6])
    d_s = ast.literal_eval(row[7])
    d_su = ast.literal_eval(row[8])
    list_south[0][0].append(d_m['breakfast'])
    list_south[0][1].append(d_m['lunch'])
    list_south[0][2].append(d_m['snack'])
    list_south[0][3].append(d_m['dinner'])

    list_south[1][0].append(d_t['breakfast'])
    list_south[1][1].append(d_t['lunch'])
    list_south[1][2].append(d_t['snack'])
    list_south[1][3].append(d_t['dinner'])

    list_south[2][0].append(d_w['breakfast'])
    list_south[2][1].append(d_w['lunch'])
    list_south[2][2].append(d_w['snack'])
    list_south[2][3].append(d_w['dinner'])

    list_south[3][0].append(d_th['breakfast'])
    list_south[3][1].append(d_th['lunch'])
    list_south[3][2].append(d_th['snack'])
    list_south[3][3].append(d_th['dinner'])

    list_south[4][0].append(d_f['breakfast'])
    list_south[4][1].append(d_f['lunch'])
    list_south[4][2].append(d_f['snack'])
    list_south[4][3].append(d_f['dinner'])

    list_south[5][0].append(d_s['breakfast'])
    list_south[5][1].append(d_s['lunch'])
    list_south[5][2].append(d_s['snack'])
    list_south[5][3].append(d_s['dinner'])

    list_south[6][0].append(d_su['breakfast'])
    list_south[6][1].append(d_su['lunch'])
    list_south[6][2].append(d_su['snack'])
    list_south[6][3].append(d_su['dinner'])
    
    con.close()    

    return list_south
#########################################################################################################


def retrieveMessMenuEast(username):

    con = sql.connect("admin.db")
    sqlQuery = "select * from mess_menu where (mess ='" + 'East' + "')"
    cur = con.cursor()
    cur.execute(sqlQuery)
    row = cur.fetchone()
    # list_east = [[[]]]

    ###      list[Day][Meals]   Day:: 0->mon, 1->tue ... Meal:: 0->break, 1->lunch, 2->snack, 3->Dinner

    list_east = [[ [] for col in range(4)] for rows in range(7)]
    d_m = ast.literal_eval(row[2])
    d_t = ast.literal_eval(row[3])
    d_w = ast.literal_eval(row[4])
    d_th = ast.literal_eval(row[5])
    d_f = ast.literal_eval(row[6])
    d_s = ast.literal_eval(row[7])
    d_su = ast.literal_eval(row[8])
    list_east[0][0].append(d_m['breakfast'])
    list_east[0][1].append(d_m['lunch'])
    list_east[0][2].append(d_m['snack'])
    list_east[0][3].append(d_m['dinner'])

    list_east[1][0].append(d_t['breakfast'])
    list_east[1][1].append(d_t['lunch'])
    list_east[1][2].append(d_t['snack'])
    list_east[1][3].append(d_t['dinner'])

    list_east[2][0].append(d_w['breakfast'])
    list_east[2][1].append(d_w['lunch'])
    list_east[2][2].append(d_w['snack'])
    list_east[2][3].append(d_w['dinner'])

    list_east[3][0].append(d_th['breakfast'])
    list_east[3][1].append(d_th['lunch'])
    list_east[3][2].append(d_th['snack'])
    list_east[3][3].append(d_th['dinner'])

    list_east[4][0].append(d_f['breakfast'])
    list_east[4][1].append(d_f['lunch'])
    list_east[4][2].append(d_f['snack'])
    list_east[4][3].append(d_f['dinner'])

    list_east[5][0].append(d_s['breakfast'])
    list_east[5][1].append(d_s['lunch'])
    list_east[5][2].append(d_s['snack'])
    list_east[5][3].append(d_s['dinner'])

    list_east[6][0].append(d_su['breakfast'])
    list_east[6][1].append(d_su['lunch'])
    list_east[6][2].append(d_su['snack'])
    list_east[6][3].append(d_su['dinner'])
    
    con.close()    

    return list_east

#########################################################################################################



def retrieveMessMenuWest(username):

    con = sql.connect("admin.db")
    sqlQuery = "select * from mess_menu where (mess ='" + 'West' + "')"
    cur = con.cursor()
    cur.execute(sqlQuery)
    row = cur.fetchone()
    # list_west = [[[]]]

    ###      list[Day][Meals]   Day:: 0->mon, 1->tue ... Meal:: 0->break, 1->lunch, 2->snack, 3->Dinner

    list_west = [[ [] for col in range(4)] for rows in range(7)]
    d_m = ast.literal_eval(row[2])
    d_t = ast.literal_eval(row[3])
    d_w = ast.literal_eval(row[4])
    d_th = ast.literal_eval(row[5])
    d_f = ast.literal_eval(row[6])
    d_s = ast.literal_eval(row[7])
    d_su = ast.literal_eval(row[8])
    list_west[0][0].append(d_m['breakfast'])
    list_west[0][1].append(d_m['lunch'])
    list_west[0][2].append(d_m['snack'])
    list_west[0][3].append(d_m['dinner'])

    list_west[1][0].append(d_t['breakfast'])
    list_west[1][1].append(d_t['lunch'])
    list_west[1][2].append(d_t['snack'])
    list_west[1][3].append(d_t['dinner'])

    list_west[2][0].append(d_w['breakfast'])
    list_west[2][1].append(d_w['lunch'])
    list_west[2][2].append(d_w['snack'])
    list_west[2][3].append(d_w['dinner'])

    list_west[3][0].append(d_th['breakfast'])
    list_west[3][1].append(d_th['lunch'])
    list_west[3][2].append(d_th['snack'])
    list_west[3][3].append(d_th['dinner'])

    list_west[4][0].append(d_f['breakfast'])
    list_west[4][1].append(d_f['lunch'])
    list_west[4][2].append(d_f['snack'])
    list_west[4][3].append(d_f['dinner'])

    list_west[5][0].append(d_s['breakfast'])
    list_west[5][1].append(d_s['lunch'])
    list_west[5][2].append(d_s['snack'])
    list_west[5][3].append(d_s['dinner'])

    list_west[6][0].append(d_su['breakfast'])
    list_west[6][1].append(d_su['lunch'])
    list_west[6][2].append(d_su['snack'])
    list_west[6][3].append(d_su['dinner'])
    
    con.close()    

    return list_west


########################################################################################################