from flask import Flask
from flask import session
from flask import redirect, url_for
from flask import render_template
from flask import request
import models as dbHandler
from flask import Response
import sqlite3 as sql
import ast
import datetime
import json
from flask import jsonify
import re
from flask import session as login_session
import os
app = Flask(__name__)
# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = 'MKhJHJH798798kjhkjhkjGHh'

##########################################################################################

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate,post-check=0, pre-check=0'"
    return response


###################### clender ##################################################

@app.route('/calendar', methods=['GET','POST'])
def calendar():
    if 'username' in session:
        return render_template("json.html")

    return redirect(url_for('login'))
#-----------------------------------------------------------------------------------
@app.route('/data',methods=['GET','POST'])
def return_data():
    start_date = request.args.get('start', '')
    end_date = request.args.get('end', '')
    file_name = ".events_"+session['username']+".json"
    print(file_name)
    with open(file_name, "r") as input_data:
        return input_data.read()

###################################################################################
    
@app.route('/ptry', methods=['GET','POST'])
def ptry():

    return render_template("try.html")

# return redirect(url_for('login'))

###################### root ##################################################
@app.route('/')
def index():
   if 'username' in session:
      return redirect(url_for('login'))
   else:
      return render_template("login.html", logged_in = False,  username=None)

 
####################### login #################################################
@app.route('/login', methods=['GET','POST'])
def login():
    if 'username' in session:
        return redirect(url_for('home'))
    elif request.method == 'POST':
        if dbHandler.authenticate(request): 
            session['username'] = request.form['username']
            
            msg = "successful login"
            rows = dbHandler.retrievePerson(session['username'])
            print(rows)
            return render_template("home.html",row=rows)
        else: 
            msg ="login failed"
    return(render_template("login.html"))
############################# home/change_registration ##################
@app.route('/home/change_registration',methods=['GET','POST'])
def change_registration():
    if 'username' in session:
        return render_template('change_registration.html')
    else:
        return redirect(url_for('login'))
############################# home/change_registration ##################
@app.route('/home/view_registration',methods=['GET','POST'])
def view_registration():
    if 'username' in session:
        return render_template('view_registration.html')
    else:
        return redirect(url_for('login'))

############################# home/change_registration ##################
@app.route('/home/view_bill',methods=['GET','POST'])
def view_bill():
    if 'username' in session:
        return render_template('view_bill.html')
    else:
        return redirect(url_for('login'))

############################# home/change_registration ##################
@app.route('/home/feedback',methods=['GET','POST'])
def feedback():
    if 'username' in session:
        return render_template('feedback.html')
    else:
        return redirect(url_for('login'))

####################### home #################################################
@app.route('/home', methods=['GET','POST'])
def home():
    rowss = []
    if 'username' in session:
        print "yolo"
        dbHandler.calendarGenerate(session['username'])
        rows = dbHandler.retrievePerson(session['username'])
        mess = dbHandler.retrieveTodaysMess(session['username'])
        north = dbHandler.retrieveMessMenuNorth(session['username'])
        south = dbHandler.retrieveMessMenuSouth(session['username'])
        east = dbHandler.retrieveMessMenuEast(session['username'])
        west = dbHandler.retrieveMessMenuWest(session['username'])

        # print rows 
        return render_template("home.html", row=rows, tbf = mess[0].capitalize()
                                                    , tlu = mess[1].capitalize()
                                                    , tsn = mess[2].capitalize()
                                                    , tdn = mess[3].capitalize(),north=north,south=south,east=east,west=west)
    if request.method=='POST':
        if dbHandler.authenticate(request): 
            session['username'] = request.form['username']
            msg = "successful login"
            dbHandler.calendarGenerate(session['username'])
            rows = dbHandler.retrievePerson(session['username'])
            mess = dbHandler.retrieveTodaysMess(session['username'])
            north = dbHandler.retrieveMessMenuNorth(session['username'])
            south = dbHandler.retrieveMessMenuSouth(session['username'])
            east = dbHandler.retrieveMessMenuEast(session['username'])
            west = dbHandler.retrieveMessMenuWest(session['username'])
            # print rows
            # print rows
            rowss = rows 
            return render_template("home.html", row=rows, tbf = mess[0].capitalize()
                                                    , tlu = mess[1].capitalize()
                                                    , tsn = mess[2].capitalize()
                                                    , tdn = mess[3].capitalize(),north=north,south=south,east=east,west=west)
        # return render_template("home.html", row=rowss, tbf = mess[0].capitalize()
        #                                             , tlu = mess[1].capitalize()
        #                                             , tsn = mess[2].capitalize()
        #                                             , tdn = mess[3].capitalize(),north=north,south=south)
    else: 
        msg ="login failed"
        return render_template("login.html", message=msg)
    
    return redirect(url_for('login'))

	
                                                        

######################## logout #################################################
@app.route('/logout', methods=['POST', 'GET'])
def logout():
    if 'username' in session:
        file_name = ".events_"+session['username']+".json"
        # session.clear()
        session.pop('username')
        for key in session.keys():
            session.pop(key)

        os.remove(file_name)
    return redirect(url_for('login'))

######################### register ################################################
@app.route('/register', methods=['POST', 'GET'])
def register():

    if 'username' in session:
        return redirect(url_for('home'))
    elif request.method=='POST':
        if dbHandler.insertUser(request):
            msg = "success in adding user"
            return render_template("login.html",message=msg)
        else:
            msg = "failed to add user"
	    

    return render_template("register.html")
    

######################### secret page: a password protected page ################################################ 
@app.route('/secret_page')
def secret_page():

    #only logged in user is allowed see other users' details.
    if 'username' in session :
       rows = dbHandler.retrievePerson(session['username'])
       print rows
       return render_template("showall.html", rows = rows)
    else:
       return redirect(url_for('login'))

###########################################################################

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')

