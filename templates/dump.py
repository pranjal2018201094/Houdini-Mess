

def changeRegistrationDaywise(request,username):
    # drange = (request.form['daterange'].encode("ascii"))
    # dates = drange.split('-')
    # start = dates[0].strip()
    # start = start.replace('/','-')
    # end =  dates[1].strip()
    # end = end.replace('/','-')
    # print start
    change = []
    try :
        request.form['b']
        change.append(0)
    except :
        pass
    try :
        request.form['l']
        change.append(1)
    except :
        pass
    try :
        request.form['s']
        change.append(2)
    except :
        pass
    try :
        request.form['d']
        change.append(3)
    except :
        pass
    # print change
    sdate =datetime.datetime.today()
    week = int(request.form['day'].encode("ascii"))
    while sdate.weekday() != week: #0 for monday
        sdate += datetime.timedelta(days=1)
    mess_val = request.form['options']
    con = sql.connect("user.db")
    sqlQuery = "select * from user_info where username = '%s'"%username
    cursor = con.cursor()
    cursor.execute(sqlQuery)
    row = cursor.fetchone()
    dictionary = ast.literal_eval(row[6])
    sdate = datetime.datetime.strptime(start,"%d-%m-%Y")
    edate = datetime.datetime(2019,8,31,12,4,5)
    print type(sdate)
    i =0
    print start
    print end
    while (edate-sdate).days >=0:
        dstr = sdate.strftime("%d-%m-%Y")
        sdate += datetime.timedelta(weeks=1)
        prev = dictionary[dstr]
        for x in change:
            prev[x] = mess_val
        dictionary[dstr]=prev
        print(dictionary[dstr])
        i=i+1

    con = sql.connect("user.db")
    cur=con.cursor()
    sqlq ="UPDATE user_info SET mess_reg = ? WHERE (username = ?)"
    cur.execute(sqlq,(str(dictionary),username))
    con.commit()
    con.close()
    calendarGenerate(username)
    