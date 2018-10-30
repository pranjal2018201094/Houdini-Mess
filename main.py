from flask import Flask
from flask import session
from flask import redirect, url_for
from flask import render_template
from flask import request
import models as dbHandler

app = Flask(__name__)
# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = 'MKhJHJH798798kjhkjhkjGHh'

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
            print rows
            return render_template("home.html", row=rows)
        else: 
            msg ="login failed"
    return(render_template("login.html"))


@app.route('/home', methods=['GET','POST'])
def home():
    if 'username' in session:
        print "yolo"
        rows = dbHandler.retrievePerson(session['username'])
        print rows 
        return render_template("home.html", row=rows)
    if request.method=='POST':
        if dbHandler.authenticate(request): 
            session['username'] = request.form['username']
            msg = "successful login"
            rows = dbHandler.retrievePerson(session['username'])
            print rows 
            return render_template("home.html", row=rows)
        else: 
            msg ="login failed"
            return render_template("result.html", message=msg)
    
    return redirect(url_for('login'))

	
                                                        

######################## logout #################################################
@app.route('/logout', methods=['POST', 'GET'])
def logout():
    if 'username' in session:
        session.pop('username')
    
    return render_template("login.html", message="You are already logged out.")

######################### register ################################################
@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method=='POST':
        if dbHandler.insertUser(request):
            msg = "success in adding user"
        else:
            msg = "failed to add user"

	return render_template("result.html", message=msg)
    
    return render_template('register.html')

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

