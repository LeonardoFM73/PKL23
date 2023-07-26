from flask import Flask,render_template,url_for,request,session,logging,redirect,flash
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session,sessionmaker
import os
from flask_paginate import Pagination, get_page_parameter

from passlib.hash import sha256_crypt

from datetime import datetime


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
            
            session['password']=password
            usernamedata=db.execute(text("SELECT username FROM admin WHERE username=:username"),{"username":username}).fetchone()
            passworddata=db.execute(text("SELECT password FROM admin WHERE username=:username"),{"username":username}).fetchone()
            
            if usernamedata is None:
                flash("No username","danger")
                return render_template('login.html')
            else:
                for passwor_data in passworddata:
                    if sha256_crypt.verify(password,passwor_data):
                        session["log"]=True
                        session['username']=username


                        if os.path.isfile('static/assets/images/users/'+session['username']+'.jpg'):
                                foto=session['username']
                        else:
                                foto='1'

                        session['foto']=foto
                        flash("You are now logged in!!","success")
                        return redirect(url_for('dashboard')) #to be edited from here do redict to either svm or home
                    else:
                        flash("incorrect password","danger")
                        return render_template('login.html')

        return render_template('login.html')

@app.route('/add_data',methods=['POST','GET'])
def add_data():
    currentDateAndTime = datetime.now()
    if session["log"] is True:
        ID_Kebun=db.execute(text("Select * from kebun")).fetchall()
        User_ID=db.execute(text("Select * from operator")).fetchall()
        
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


        return render_template('/ltr/data_prediksi/add.html',data=ID_Kebun,data2=User_ID,user=session['foto'])


@app.route('/add_kebun',methods=["POST","GET"])
def add_kebun():
    if session["log"] is True:
        if request.method=="POST":
            Latitude=request.form.get("Latitude")
            Longitude=request.form.get("Longitude")
            Alamat=request.form.get("Alamat")
            Blok=request.form.get("Blok")

            db.execute(text("INSERT INTO kebun(Latitude,Longitude,Alamat,Blok) VALUES(:Latitude,:Longitude,:Alamat,:Blok)"),
            {"Latitude":Latitude,"Longitude":Longitude,"Alamat":Alamat,"Blok":Blok})
            db.commit()
            return redirect(url_for('kebun'))              

        return render_template('/ltr/kebun/add.html',user=session['foto'])

@app.route('/add_operator',methods=['POST','GET'])
def add_operator():
    if session["log"] is True:
        ID_Kebun=db.execute(text("Select * from kebun")).fetchall()

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


        return render_template('/ltr/operator/add.html',data=ID_Kebun,user=session['foto'])


@app.route('/delete_data/<int:id>',methods=['POST','GET'])
def delete_data_(id):
    if session["log"] is True:
        data=db.execute(text("SELECT * FROM data_prediksi")).fetchall()
        
        keys = ['ID', 'Waktu', 'ID_Kebun', 'UserID','Nama_File', 'Hasil_Prediksi']

        # Create a list of dictionaries
        new_data = [dict(zip(keys, item)) for item in data]

        found_indexes = 0

        for i, item in enumerate(data):
            if item.ID == id:
                found_indexes=i

        if request.method == 'POST':
            checkbox_list= request.form.getlist('checkbox')
            if checkbox_list:
                # The list is not empty, so it is safe to access its first element
                checkbox = checkbox_list[0]
            else:
                # The list is empty, handle this situation accordingly (e.g., set a default value or show an error message)
                # For example, if you want to set a default value:
                checkbox = 'No'
            if request.form.getlist('options')[0] == "Yes":
                if checkbox=="Yes":
                    db.execute(text("DELETE FROM data_prediksi WHERE data_prediksi.ID = :id"),{"id":id})
                    db.commit()
                    return redirect(url_for('data'))
                else:
                    flash("Please check the box","danger")
                    return redirect(url_for('delete_data_',id=id))
            else:
                return redirect(url_for('data'))

        return render_template('/ltr/data_prediksi/deletedata.html',data=new_data,id=found_indexes,user=session['foto'])


@app.route('/delete_kebun/<int:id>',methods=['POST','GET'])
def delete_kebun_(id):
    if session["log"] is True:
        data=db.execute(text("Select * FROM kebun")).fetchall()

        # Define the keys for each dictionary
        keys = ['ID_Kebun', 'Latitude', 'Longitude', 'Alamat', 'Blok']

        # Create a list of dictionaries
        new_data = [dict(zip(keys, item)) for item in data]
        
        found_indexes = 0

        for i, item in enumerate(new_data):
            if item['ID_Kebun'] == id:
                found_indexes=i

        if request.method == 'POST':
            checkbox_list= request.form.getlist('checkbox')
            if checkbox_list:
                # The list is not empty, so it is safe to access its first element
                checkbox = checkbox_list[0]
            else:
                # The list is empty, handle this situation accordingly (e.g., set a default value or show an error message)
                # For example, if you want to set a default value:
                checkbox = 'No'
            if request.form.getlist('options')[0] == "Yes":
                if checkbox=="Yes":
                    db.execute(text("DELETE FROM kebun WHERE kebun.ID_Kebun = :id"),{"id":id})
                    db.commit()
                    return redirect(url_for('kebun'))
                else:
                    flash("Please check the box","danger")
                    return redirect(url_for('delete_kebun_',id=id))
            else:
                return redirect(url_for('kebun'))

        return render_template('/ltr/kebun/deletekebun.html',data=new_data,id=found_indexes,user=session['foto'])

@app.route('/delete_operator/<userid>',methods=['POST','GET'])
def delete_operator_(userid):
    if session["log"] is True:
        data=db.execute(text("SELECT * FROM operator"))

        keys = ['UserID', 'Nama_Operator', 'No_HP', 'ID_Kebun', 'Alamat']

        # Create a list of dictionaries
        new_data = [dict(zip(keys, item)) for item in data]
        
        found_indexes = 0

        for i, item in enumerate(new_data):
            if item['UserID'] == userid:
                found_indexes=i

        if request.method == 'POST':
            checkbox_list= request.form.getlist('checkbox')
            if checkbox_list:
                # The list is not empty, so it is safe to access its first element
                checkbox = checkbox_list[0]
            else:
                # The list is empty, handle this situation accordingly (e.g., set a default value or show an error message)
                # For example, if you want to set a default value:
                checkbox = 'No'
            if request.form.getlist('options')[0] == "Yes":
                if checkbox =="Yes":
                    db.execute(text("DELETE FROM operator WHERE operator.UserID = :userid"),{"userid":userid})
                    db.commit()
                    return redirect(url_for('operator'))
                else:
                    flash("Please check the box","danger")
                    return redirect(url_for('delete_operator_',userid=userid))
            else:
                return redirect(url_for('operator'))
            
        return render_template('/ltr/operator/deleteoperator.html',data=new_data,id=found_indexes,user=session['foto'])

    if session["log"] is True:
        if request.method == 'POST':
            search = request.form.get('search')
            result = getdata(search)
        else:
            result=[]
        return render_template('/ltr/data_prediksi/edit.html',data=result,user=session['foto'])

@app.route('/edit_data/<int:id>',methods=['POST','GET'])
def edit_data_(id):
    if session["log"] is True:
        data=db.execute(text("Select * from data_prediksi")).fetchall()
        keys = ['ID', 'Waktu', 'ID_Kebun', 'UserID','Nama_File', 'Hasil_Prediksi']

        # Create a list of dictionaries
        new_data = [dict(zip(keys, item)) for item in data]
        
        data2=db.execute(text("Select * from kebun")).fetchall()
        keys2 = ['ID_Kebun', 'Latitude', 'Longitude', 'Alamat', 'Blok']

        # Create a list of dictionaries
        new_data2 = [dict(zip(keys2, item)) for item in data2]

        data3=db.execute(text("Select * from operator")).fetchall()
        keys3 = ['UserID', 'Nama_Operator', 'No_HP', 'ID_Kebun', 'Alamat']

        # Create a list of dictionaries
        new_data3 = [dict(zip(keys3, item)) for item in data3]


        # Update values in new_data
        
        
        found_indexes = 0

        for i, item in enumerate(new_data):
            if item['ID'] == id:
                found_indexes=i

        if request.method == 'POST':
            Waktu=request.form.get("Waktu")
            ID_Kebun=request.form.get("ID_Kebun")
            User_ID=request.form.get("User_ID")
            Nama_File=request.form.get("Nama_File")
            Hasil_Prediksi=request.form.get("Hasil_Prediksi")

            db.execute(text("UPDATE data_prediksi SET Waktu=:Waktu, ID_Kebun=:ID_Kebun, UserID=:User_ID, Nama_File=:Nama_File, Hasil_Prediksi=:Hasil_Prediksi WHERE ID=:id"), 
            {"Waktu": Waktu, "ID_Kebun": ID_Kebun, "User_ID": User_ID, "Nama_File": Nama_File, "Hasil_Prediksi": Hasil_Prediksi, "id": id})

            db.commit()
            return redirect(url_for('data'))  
        
        return render_template('/ltr/data_prediksi/editdata.html',data=new_data,data2=new_data2,data3=new_data3,id=found_indexes,user=session['foto'])

@app.route('/edit_kebun/<int:id>',methods=['POST','GET'])
def edit_kebun_(id):
    if session["log"] is True:
        data=db.execute(text("Select * FROM kebun")).fetchall()

        # Define the keys for each dictionary
        keys = ['ID_Kebun', 'Latitude', 'Longitude', 'Alamat', 'Blok']

        # Create a list of dictionaries
        new_data = [dict(zip(keys, item)) for item in data]
        
        
        found_indexes = 0

        for i, item in enumerate(new_data):
            if item['ID_Kebun'] == id:
                found_indexes=i

        if request.method == 'POST':
            Latitude=request.form.get("Latitude")
            Longitude=request.form.get("Longitude")
            Alamat=request.form.get("Alamat")
            Blok=request.form.get("Blok")

            db.execute(text("UPDATE kebun SET Latitude=:Latitude, Longitude=:Longitude, Alamat=:Alamat, Blok=:Blok WHERE ID_Kebun=:id"), 
            {"Latitude": Latitude, "Longitude": Longitude, "Alamat": Alamat, "Blok": Blok, "id": id})

            db.commit()
            return redirect(url_for('kebun'))  
        
        return render_template('/ltr/kebun/editkebun.html',data=new_data,id=found_indexes,user=session['foto'])


@app.route('/edit_operator/<userid>',methods=['POST','GET'])
def edit_operator_(userid):
    if session["log"] is True:
        data=db.execute(text("Select * FROM operator")).fetchall()


        # Define the keys for each dictionary
        keys = ['UserID', 'Nama_Operator', 'No_HP', 'ID_Kebun', 'Alamat']

        # Create a list of dictionaries
        new_data = [dict(zip(keys, item)) for item in data]

        data2=db.execute(text("Select * FROM kebun")).fetchall()

        # Define the keys for each dictionary
        keys2 = ['ID_Kebun', 'Latitude', 'Longitude', 'Alamat', 'Blok']

        # Create a list of dictionaries
        new_data2 = [dict(zip(keys2, item)) for item in data2]
        
        found_indexes = 0

        for i, item in enumerate(new_data):
            if item['UserID'] == userid:
                found_indexes=i

        if request.method == 'POST':
            Nama_Operator=request.form.get("Nama_Operator")
            No_HP=request.form.get("No_HP")
            ID_Kebun=request.form.get("ID_Kebun")
            Alamat=request.form.get("Alamat")

            db.execute(text("UPDATE operator SET Nama_Operator=:Nama_Operator, No_HP=:No_HP, ID_Kebun=:ID_Kebun, Alamat=:Alamat WHERE UserID=:userid"), 
            {"Nama_Operator": Nama_Operator, "No_HP": No_HP, "ID_Kebun": ID_Kebun, "Alamat": Alamat, "userid": userid})

            db.commit()
            return redirect(url_for('operator'))  
    
        return render_template('/ltr/operator/editoperator.html',data=new_data,data2=new_data2,id=found_indexes,user=session['foto'])

def getdata(search):
    ID = db.execute(text("SELECT * FROM data_prediksi WHERE ID = :search"), {"search": search}).fetchall()

    return ID

def getkebun(search):
    ID_Kebun=db.execute(text('SELECT * FROM kebun WHERE ID_KEBUN = :search'),{'search':search}).fetchall()

    return ID_Kebun

def getoperator(search):
    results=db.execute(text("SELECT * FROM operator where UserID LIKE '%' :search '%' "),{'search':search}).fetchall()

    return results

@app.route('/dashboard', methods=['GET'])
def dashboard():
    if session["log"]:
        jumlah_kebun = db.execute(text("Select COUNT(*) from kebun")).fetchone()
        jumlah_operator = db.execute(text("Select COUNT(*) from operator")).fetchone()
        jumlah_data = db.execute(text("Select COUNT(*) from data_prediksi")).fetchone()
        Waktu = db.execute(text("Select Waktu from data_prediksi")).fetchall()
        ID_kebun = db.execute(text("Select  ID_Kebun from data_prediksi")).fetchall()
        User_ID = db.execute(text("Select UserID from data_prediksi")).fetchall()
        Nama_File = db.execute(text("Select Nama_File from data_prediksi")).fetchall()
        Hasil_Prediksi = db.execute(text("Select Hasil_Prediksi from data_prediksi")).fetchall()

        Waktu = tuple(item[0] for item in Waktu)
        ID_kebun = tuple(item[0] for item in ID_kebun)
        User_ID = tuple(item[0] for item in User_ID)
        Nama_File = tuple(item[0] for item in Nama_File)
        Hasil_Prediksi = tuple(item[0] for item in Hasil_Prediksi)

        data = [
            {
                'jumlah': jumlah_kebun[0],
                'operator': jumlah_operator[0],
                'prediksi': jumlah_data[0],
                'Waktu': Waktu,
                'ID_Kebun': ID_kebun,
                'User_ID': User_ID,
                'Nama_File': Nama_File,
                'Hasil_Prediksi': Hasil_Prediksi
            }
        ]
        new_data = [
            {
                'Waktu': Waktu,
                'ID_Kebun': kebun,
                'User_ID': user,
                'Nama_File': file,
                'Hasil_Prediksi': hasil
            }
            for item in data
            for Waktu, kebun, user, file, hasil in zip(item['Waktu'], item['ID_Kebun'], item['User_ID'], item['Nama_File'], item['Hasil_Prediksi'])
        ]

        # Pagination settings
        page = request.args.get(get_page_parameter(), type=int, default=1)
        per_page = 5  # Adjust the number of items per page as needed
        offset = (page - 1) * per_page
        total = len(new_data)

        pagination_data = new_data[offset: offset + per_page]
        pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

        return render_template('ltr/dashboard.html', data=pagination_data,data2=data, page=page, per_page=per_page, pagination=pagination, user=session['foto'])

@app.route('/kebun', methods=['POST','GET'])
def kebun():
    if session["log"] is True:
        # jumlah_kebun=db.execute(text("Select COUNT(*) from kebun")).fetchone()
        # ID_Kebun=db.execute(text("Select  ID_Kebun from kebun")).fetchall()
        # Latitude=db.execute(text("Select  Latitude from kebun")).fetchall()
        # Longitude=db.execute(text("Select  Longitude from kebun")).fetchall()
        # Alamat=db.execute(text("Select  Alamat from kebun")).fetchall()
        # #db.execute(text("Select IFNULL(blok, 'N/A') from kebun"))
        # blok=db.execute(text("Select Blok from kebun")).fetchall()

        # ID_Kebun = tuple(item[0] for item in ID_Kebun)
        # Latitude = tuple(item[0] for item in Latitude)
        # Longitude = tuple(item[0] for item in Longitude)
        # Alamat = tuple(item[0] for item in Alamat)
        # blok = tuple(item[0] for item in blok)

        # data=[
        #     {
        #         'jumlah':jumlah_kebun[0],
        #         'ID_Kebun':ID_Kebun,
        #         'Latitude':Latitude,
        #         'Longitude':Longitude,
        #         'Alamat':Alamat,
        #         'blok':blok
        #     }
        # ]
        # new_data=[
        #     {
        #         'ID_Kebun':ID_Kebun,
        #         'Latitude':Latitude,
        #         'Longitude':Longitude,
        #         'Alamat':Alamat,
        #         'blok':blok            
        #     }
        #     for item in data
        #     for ID_Kebun, Latitude, Longitude, Alamat, blok in zip(item['ID_Kebun'],item['Latitude'],item['Longitude'],item['Alamat'],item['blok'])
        # ]

        data=db.execute(text("Select * FROM kebun")).fetchall()


        # Define the keys for each dictionary
        keys = ['ID_Kebun', 'Latitude', 'Longitude', 'Alamat', 'Blok']

        # Create a list of dictionaries
        new_data = [dict(zip(keys, item)) for item in data]

        if request.method == 'POST':
            search = request.form.get('search')
            new_data = getkebun(search)

        page = request.args.get(get_page_parameter(), type=int, default=1)
        per_page = 5  # Adjust the number of items per page as needed
        offset = (page - 1) * per_page
        total = len(new_data)

        pagination_data = new_data[offset: offset + per_page]
        pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

        return render_template('ltr/kebun.html', data=pagination_data,page=page, per_page=per_page, pagination=pagination, user=session['foto'])

@app.route('/data', methods=['POST','GET'])
def data():
    if session["log"] is True:
        # ID=db.execute(text("Select ID from data_prediksi")).fetchall()
        # Waktu=db.execute(text("Select Waktu from data_prediksi")).fetchall()
        # ID_kebun=db.execute(text("Select  ID_Kebun from data_prediksi")).fetchall()
        # User_ID=db.execute(text("Select   UserID from data_prediksi")).fetchall()
        # Nama_File=db.execute(text("Select Nama_File from data_prediksi")).fetchall()
        # Hasil_Prediksi=db.execute(text("Select Hasil_Prediksi from data_prediksi")).fetchall()
        
        
        # ID = tuple(item[0] for item in ID)
        # Waktu = tuple(item[0] for item in Waktu)
        # ID_kebun = tuple(item[0] for item in ID_kebun)
        # UserID = tuple(item[0] for item in User_ID)
        # Nama_File = tuple(item[0] for item in Nama_File)
        # Hasil_Prediksi = tuple(item[0] for item in Hasil_Prediksi)
        
        # data=[
        #     {
        #         'ID':ID,
        #         'Waktu':Waktu,
        #         'ID_Kebun':ID_kebun,
        #         'UserID':UserID,
        #         'Nama_File':Nama_File,
        #         'Hasil_Prediksi':Hasil_Prediksi
        #     }
        # ]
        # new_data = [
        # {

        #     'ID':ID,
        #     'Waktu':Waktu,
        #     'ID_Kebun': kebun,
        #     'UserID': UserID,
        #     'Nama_File': file,
        #     'Hasil_Prediksi': hasil
        # }
        #     for item in data
        #     for ID,Waktu, kebun, UserID, file, hasil in zip(item['ID'],item['Waktu'],item['ID_Kebun'], item['UserID'], item['Nama_File'], item['Hasil_Prediksi'])
        # ]

        data=db.execute(text("Select * FROM data_prediksi")).fetchall()


        # Define the keys for each dictionary
        keys = ['ID', 'Waktu', 'ID_Kebun', 'UserID','Nama_File', 'Hasil_Prediksi']

        # Create a list of dictionaries
        new_data = [dict(zip(keys, item)) for item in data]

        if request.method == 'POST':
            search = request.form.get('search')
            new_data = getdata(search)


        page = request.args.get(get_page_parameter(), type=int, default=1)
        per_page = 5  # Adjust the number of items per page as needed
        offset = (page - 1) * per_page
        total = len(new_data)

        pagination_data = new_data[offset: offset + per_page]
        pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

        return render_template('ltr/data_prediksi.html',data=pagination_data,per_page=per_page,pagination=pagination,user=session['foto'])

@app.route('/operator', methods=['POST','GET'])
def operator():
    if session["log"] is True:
        # User_ID=db.execute(text("Select   UserID from operator")).fetchall()
        # Nama_Operator=db.execute(text("Select  Nama_Operator from operator")).fetchall()
        # No_HP=db.execute(text("Select  No_HP from operator")).fetchall()
        # ID_Kebun=db.execute(text("Select ID_Kebun from operator")).fetchall()
        # Alamat=db.execute(text("Select Alamat from operator")).fetchall()

        # User_ID = tuple(item[0] for item in User_ID)
        # Nama_Operator = tuple(item[0] for item in Nama_Operator)
        # No_HP = tuple(item[0] for item in No_HP)
        # ID_Kebun = tuple(item[0] for item in ID_Kebun)
        # Alamat = tuple(item[0] for item in Alamat)
        
        # data=[
        #     {
        #         'User_ID':User_ID,
        #         'Nama_Operator':Nama_Operator,
        #         'No_HP':No_HP,
        #         'ID_Kebun':ID_Kebun,
        #         'Alamat':Alamat
        #     }
        # ]
        # new_data=[
        #     {
        #         'User_ID':User_ID,
        #         'Nama_Operator':Nama_Operator,
        #         'No_HP':No_HP,
        #         'ID_Kebun':ID_Kebun,
        #         'Alamat':Alamat
        #     }
        #     for item in data
        #     for User_ID, Nama_Operator, No_HP, ID_Kebun, Alamat in zip(item['User_ID'],item['Nama_Operator'], item['No_HP'], item['ID_Kebun'], item['Alamat'])
        # ]

        data=db.execute(text("Select * FROM operator")).fetchall()


        # Define the keys for each dictionary
        keys = ['UserID', 'Nama_Operator', 'No_HP', 'ID_Kebun', 'Alamat']

        # Create a list of dictionaries
        new_data = [dict(zip(keys, item)) for item in data]

        if request.method == 'POST':
            search = "%"+request.form.get('search')+"%"
            new_data = getoperator(search)

        page = request.args.get(get_page_parameter(), type=int, default=1)
        per_page = 5  # Adjust the number of items per page as needed
        offset = (page - 1) * per_page
        total = len(new_data)

        pagination_data = new_data[offset: offset + per_page]
        pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

        return render_template('ltr/operator.html',data=pagination_data,per_page=per_page,pagination=pagination,user=session['foto'])

@app.route('/profile',methods=['POST','GET'])
def profile():
    if session['log'] == True:
        nama=db.execute(text("SELECT Nama from admin WHERE username= :username"),{"username":session["username"]}).fetchall()
        username=db.execute(text("SELECT username from admin WHERE username= :username"),{"username":session["username"]}).fetchall()
        password= session['password'] #db.execute(text("SELECT password from admin WHERE username= :username"),{"username":session["username"]}).fetchall()
        email=db.execute(text("SELECT email from admin WHERE username= :username"),{"username":session["username"]}).fetchall()
        Nohp=db.execute(text("SELECT No_HP from admin WHERE username= :username"),{"username":session["username"]}).fetchall()

        nama=tuple(item[0] for item in nama)
        username=tuple(item[0] for item in username)
        #password=tuple(item[0] for item in password)
        email=tuple(item[0] for item in email)
        Nohp=tuple(item[0] for item in Nohp)

        data=[
            {
                'nama':nama,
                'username':username,
                'password':password,
                'email':email,
                'Nohp':Nohp
            }
        ]
        new_data=[
            {
                'nama':nama,
                'username':username,
                'password':password,
                'email':email,
                'Nohp':Nohp       
            }
                for item in data
                for nama,username,email,Nohp in zip(item['nama'],item['username'],item['email'],item['Nohp'])
        ]
        if request.method == 'POST':
            nama=request.form.get('nama')
            email=request.form.get('email')
            password=request.form.get('password')
            secure_password=sha256_crypt.encrypt(str(password))
            Nohp=request.form.get('Nohp')

            image = request.files['foto']
            if image.filename !='':
                image.save('static/assets/images/users/'+session['username']+".jpg")

            db.execute(text("UPDATE admin SET Nama=:nama, email=:email, password=:password, No_Hp=:Nohp WHERE username=:userid"), 
            {"nama": nama, "email": email, "password": secure_password, "Nohp": Nohp, "userid": session['username']})
            db.commit()
            session['foto']=session['username']

            return redirect(url_for('profile'))



        #if request.method == "POST":
        
        return render_template('ltr/profile.html',data=new_data,user=session['foto'])


@app.route('/logout')
def logout():
    session["log"]=False
    session.pop('username')
    flash('You are Logged Out',"danger")
    return redirect(url_for('login'))

@app.route('/check')
def check():

    return render_template("check.html")

if __name__ == '__main__':
    app.run(debug=True)