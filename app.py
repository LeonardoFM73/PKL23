from flask import Flask,render_template,url_for,request,session,logging,redirect,flash
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session,sessionmaker

from passlib.hash import sha256_crypt

engine=create_engine("mysql+pymysql://root:@localhost:3306/Test")
#mysql+pymysql://username:password@localhost/databasename
db=scoped_session(sessionmaker(bind=engine))


app = Flask(__name__)
app.secret_key = "LeonardoFM"

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/register',methods=['POST'  ,'GET'])
def register():
    if request.method=="POST":
        name=request.form.get("name")
        username=request.form.get("username")
        password=request.form.get("password")
        confirm=request.form.get("confirm")
        secure_password=sha256_crypt.encrypt(str(password))
        

        usernamedata=db.execute(text("SELECT username FROM users WHERE username=:username"),{"username":username}).fetchone()
        #usernamedata=str(usernamedata)
        if usernamedata==None:
            if password==confirm:
                db.execute(text("INSERT INTO users(name,username,password) VALUES(:name,:username,:password)"),
        {"name":name,"username":username,"password":secure_password})
                db.commit()
                flash("You are registered and can now login","success")
                return redirect(url_for('login'))
            else:
                flash("password does not match","danger")
                return render_template('register.html')
        else:
            flash("user already existed, please login or contact admin","danger")
            return redirect(url_for('login'))
        
    return render_template('register.html')

@app.route('/login',methods=["POST","GET"])
def login():
        if request.method=="POST":
            username=request.form.get("username")
            password=request.form.get("password")
            
            usernamedata=db.execute(text("SELECT username FROM users WHERE username=:username"),{"username":username}).fetchone()
            passworddata=db.execute(text("SELECT password FROM users WHERE username=:username"),{"username":username}).fetchone()
            
            if usernamedata is None:
                flash("No username","danger")
                return render_template('login.html')
            else:
                for passwor_data in passworddata:
                    if sha256_crypt.verify(password,passwor_data):
                        session["log"]=True
                        
                        flash("You are now logged in!!","success")
                        return redirect(url_for('dashboard')) #to be edited from here do redict to either svm or home
                    else:
                        flash("incorrect password","danger")
                        return render_template('login.html')

        return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('ltr/dashboard.html')
if __name__ == '__main__':
    app.run(debug=True) 