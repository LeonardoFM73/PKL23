from flask import Flask,render_template,url_for,request,session,logging,redirect,flash
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session,sessionmaker

from passlib.hash import sha256_crypt

engine=create_engine("mysql+pymysql://root:@localhost:3306/leafo")
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
        

        usernamedata=db.execute(text("SELECT username FROM admin WHERE username=:username"),{"username":username}).fetchone()
        #usernamedata=str(usernamedata)
        if usernamedata==None:
            if password==confirm:
                db.execute(text("INSERT INTO admin(Nama,username,password) VALUES(:Nama,:username,:password)"),
        {"Nama":name,"username":username,"password":secure_password})
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
            
            usernamedata=db.execute(text("SELECT username FROM admin WHERE username=:username"),{"username":username}).fetchone()
            passworddata=db.execute(text("SELECT password FROM admin WHERE username=:username"),{"username":username}).fetchone()
            
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

@app.route('/add_data',methods=['POST','GET'])
def add_data():
    ID_Kebun=db.execute(text("Select ID_Kebun from kebun")).fetchall()
    User_ID=db.execute(text("Select UserID from operator")).fetchall()
    ID_Kebun=tuple(item[0] for item in ID_Kebun)
    User_ID=tuple(item[0] for item in User_ID)

    data=[
        {
            'ID_Kebun':ID_Kebun,
            'User_ID':User_ID
        }
    ]
    new_data=[
        {
            'ID_Kebun':ID_Kebun,
            'User_ID':User_ID        
        }
        for item in data
        for ID_Kebun,User_ID in zip(item['ID_Kebun'],item['User_ID'])
    ]
    if request.method=="POST":
        Waktu=request.form.get("Waktu")
        ID_Kebun=request.form.get("ID_Kebun")
        User_ID=request.form.get("User_ID")
        Nama_file=request.form.get("Nama_File")
        Hasil_prediksi=request.form.get("Hasil_Prediksi")

        db.execute(text("INSERT INTO data_prediksi(Waktu,ID_Kebun,UserID,Nama_File,Hasil_Prediksi) VALUES(:Waktu,:ID_Kebun,:UserID,:Nama_File,:Hasil_Prediksi)"),
        {"Waktu":Waktu,"ID_Kebun":ID_Kebun,"UserID":User_ID,"Nama_File":Nama_file,"Hasil_Prediksi":Hasil_prediksi})
        db.commit()
        return redirect(url_for('data'))  


    return render_template('/ltr/data_prediksi/add.html',data=new_data)


@app.route('/add_kebun',methods=["POST","GET"])
def add_kebun():
    if request.method=="POST":
        Latitude=request.form.get("Latitude")
        Longitude=request.form.get("Longitude")
        Alamat=request.form.get("Alamat")
        Blok=request.form.get("Blok")

        db.execute(text("INSERT INTO kebun(Latitude,Longitude,Alamat,Blok) VALUES(:Latitude,:Longitude,:Alamat,:Blok)"),
        {"Latitude":Latitude,"Longitude":Longitude,"Alamat":Alamat,"Blok":Blok})
        db.commit()
        return redirect(url_for('kebun'))              

    return render_template('/ltr/kebun/add.html')

@app.route('/add_operator',methods=['POST','GET'])
def add_operator():
    ID_Kebun=db.execute(text("Select ID_Kebun from kebun")).fetchall()
    ID_Kebun=tuple(item[0] for item in ID_Kebun)

    data=[
        {
            'ID_Kebun':ID_Kebun
        }
    ]
    new_data=[
        {
            'ID_Kebun':ID_Kebun,        
        }
        for item in data
        for ID_Kebun in zip(item['ID_Kebun'])
    ]
    if request.method=='POST':
        User_ID=request.form.get('UserID')
        operator=request.form.get('Operator')
        NoHP=request.form.get('NoHP')
        ID_Kebun=request.form.get('ID_Kebun')
        Alamat=request.form.get('Alamat')

        db.execute(text("INSERT INTO operator(UserID,Nama_Operator,No_HP,ID_Kebun,Alamat) VALUES(:UserID,:Name_Operator,:NoHP,:ID_Kebun,:Alamat)"),
        {"UserID":User_ID,"Name_Operator":operator,"NoHP":NoHP,"ID_Kebun":ID_Kebun,"Alamat":Alamat})
        db.commit()
        return redirect(url_for('operator'))  


    return render_template('/ltr/operator/add.html',data=new_data)

@app.route('/dashboard', methods=['GET'])
def dashboard():
    jumlah_kebun=db.execute(text("Select COUNT(*) from kebun")).fetchone()
    jumlah_operator=db.execute(text("Select COUNT(*) from operator")).fetchone()
    jumlah_data=db.execute(text("Select COUNT(*) from data_prediksi")).fetchone()
    waktu=db.execute(text("Select Waktu from data_prediksi")).fetchall()
    ID_kebun=db.execute(text("Select  ID_Kebun from data_prediksi")).fetchall()
    User_ID=db.execute(text("Select   UserID from data_prediksi")).fetchall()
    Nama_File=db.execute(text("Select Nama_File from data_prediksi")).fetchall()
    Hasil_Prediksi=db.execute(text("Select Hasil_Prediksi from data_prediksi")).fetchall()
    
    waktu = tuple(item[0] for item in waktu)
    ID_kebun = tuple(item[0] for item in ID_kebun)
    User_ID = tuple(item[0] for item in User_ID)
    Nama_File = tuple(item[0] for item in Nama_File)
    Hasil_Prediksi = tuple(item[0] for item in Hasil_Prediksi)
    
    data=[
        {
            'jumlah':jumlah_kebun[0],
            'operator':jumlah_operator[0],
            'prediksi':jumlah_data[0],
            'waktu':waktu,
            'ID_Kebun':ID_kebun,
            'User_ID':User_ID,
            'Nama_File':Nama_File,
            'Hasil_Prediksi':Hasil_Prediksi
        }
    ]
    new_data = [
    {

        'waktu':waktu,
        'ID_Kebun': kebun,
        'User_ID': user,
        'Nama_File': file,
        'Hasil_Prediksi': hasil
    }
        for item in data
        for waktu, kebun, user, file, hasil in zip(item['waktu'],item['ID_Kebun'], item['User_ID'], item['Nama_File'], item['Hasil_Prediksi'])
    ]

    return render_template('ltr/dashboard.html',data=data,data2=new_data)

@app.route('/kebun', methods=['GET'])
def kebun():
    jumlah_kebun=db.execute(text("Select COUNT(*) from kebun")).fetchone()
    ID_Kebun=db.execute(text("Select  ID_Kebun from kebun")).fetchall()
    Latitude=db.execute(text("Select  Latitude from kebun")).fetchall()
    Longitude=db.execute(text("Select  Longitude from kebun")).fetchall()
    Alamat=db.execute(text("Select  Alamat from kebun")).fetchall()
    #db.execute(text("Select IFNULL(blok, 'N/A') from kebun"))
    blok=db.execute(text("Select Blok from kebun")).fetchall()

    ID_Kebun = tuple(item[0] for item in ID_Kebun)
    Latitude = tuple(item[0] for item in Latitude)
    Longitude = tuple(item[0] for item in Longitude)
    Alamat = tuple(item[0] for item in Alamat)
    blok = tuple(item[0] for item in blok)

    data=[
        {
            'jumlah':jumlah_kebun[0],
            'ID_Kebun':ID_Kebun,
            'Latitude':Latitude,
            'Longitude':Longitude,
            'Alamat':Alamat,
            'blok':blok
        }
    ]
    new_data=[
        {
            'ID_Kebun':ID_Kebun,
            'Latitude':Latitude,
            'Longitude':Longitude,
            'Alamat':Alamat,
            'blok':blok            
        }
        for item in data
        for ID_Kebun, Latitude, Longitude, Alamat, blok in zip(item['ID_Kebun'],item['Latitude'],item['Longitude'],item['Alamat'],item['blok'])
    ]

    return render_template('ltr/kebun.html', data=data, data2=new_data)

@app.route('/data', methods=['GET'])
def data():
    waktu=db.execute(text("Select Waktu from data_prediksi")).fetchall()
    ID_kebun=db.execute(text("Select  ID_Kebun from data_prediksi")).fetchall()
    User_ID=db.execute(text("Select   UserID from data_prediksi")).fetchall()
    Nama_File=db.execute(text("Select Nama_File from data_prediksi")).fetchall()
    Hasil_Prediksi=db.execute(text("Select Hasil_Prediksi from data_prediksi")).fetchall()
    
    waktu = tuple(item[0] for item in waktu)
    ID_kebun = tuple(item[0] for item in ID_kebun)
    User_ID = tuple(item[0] for item in User_ID)
    Nama_File = tuple(item[0] for item in Nama_File)
    Hasil_Prediksi = tuple(item[0] for item in Hasil_Prediksi)
    
    data=[
        {
            'waktu':waktu,
            'ID_Kebun':ID_kebun,
            'User_ID':User_ID,
            'Nama_File':Nama_File,
            'Hasil_Prediksi':Hasil_Prediksi
        }
    ]
    new_data = [
    {

        'waktu':waktu,
        'ID_Kebun': kebun,
        'User_ID': user,
        'Nama_File': file,
        'Hasil_Prediksi': hasil
    }
        for item in data
        for waktu, kebun, user, file, hasil in zip(item['waktu'],item['ID_Kebun'], item['User_ID'], item['Nama_File'], item['Hasil_Prediksi'])
    ]
    return render_template('ltr/data_prediksi.html',data=new_data)

@app.route('/operator', methods=['GET'])
def operator():
    User_ID=db.execute(text("Select   UserID from operator")).fetchall()
    Nama_Operator=db.execute(text("Select  Nama_Operator from operator")).fetchall()
    No_HP=db.execute(text("Select  No_HP from operator")).fetchall()
    ID_Kebun=db.execute(text("Select ID_Kebun from operator")).fetchall()
    Alamat=db.execute(text("Select Alamat from operator")).fetchall()

    User_ID = tuple(item[0] for item in User_ID)
    Nama_Operator = tuple(item[0] for item in Nama_Operator)
    No_HP = tuple(item[0] for item in No_HP)
    ID_Kebun = tuple(item[0] for item in ID_Kebun)
    Alamat = tuple(item[0] for item in Alamat)
    
    data=[
        {
            'User_ID':User_ID,
            'Nama_Operator':Nama_Operator,
            'No_HP':No_HP,
            'ID_Kebun':ID_Kebun,
            'Alamat':Alamat
        }
    ]
    new_data=[
        {
            'User_ID':User_ID,
            'Nama_Operator':Nama_Operator,
            'No_HP':No_HP,
            'ID_Kebun':ID_Kebun,
            'Alamat':Alamat
        }
        for item in data
        for User_ID, Nama_Operator, No_HP, ID_Kebun, Alamat in zip(item['User_ID'],item['Nama_Operator'], item['No_HP'], item['ID_Kebun'], item['Alamat'])
    ]

    return render_template('ltr/operator.html',data=new_data)

@app.route('/profile')
def profile():
    return render_template('ltr/profile.html')

if __name__ == '__main__':
    app.run(debug=True) 