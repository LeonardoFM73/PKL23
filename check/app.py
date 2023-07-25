from flask import Flask,render_template,url_for,request,session,logging,redirect,flash
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session,sessionmaker
import os
from flask_paginate import Pagination, get_page_parameter

from passlib.hash import sha256_crypt

engine=create_engine("mysql+pymysql://root:@localhost:3306/leafo")
#mysql+pymysql://username:password@localhost/databasename
db=scoped_session(sessionmaker(bind=engine))


app = Flask(__name__)
app.secret_key = "LeonardoFM"

@app.route('/dashboard', methods=['GET'])
def dashboard():
    if session["log"]:
        jumlah_kebun = db.execute(text("Select COUNT(*) from kebun")).fetchone()
        jumlah_operator = db.execute(text("Select COUNT(*) from operator")).fetchone()
        jumlah_data = db.execute(text("Select COUNT(*) from data_prediksi")).fetchone()
        waktu = db.execute(text("Select Waktu from data_prediksi")).fetchall()
        ID_kebun = db.execute(text("Select  ID_Kebun from data_prediksi")).fetchall()
        User_ID = db.execute(text("Select UserID from data_prediksi")).fetchall()
        Nama_File = db.execute(text("Select Nama_File from data_prediksi")).fetchall()
        Hasil_Prediksi = db.execute(text("Select Hasil_Prediksi from data_prediksi")).fetchall()

        waktu = tuple(item[0] for item in waktu)
        ID_kebun = tuple(item[0] for item in ID_kebun)
        User_ID = tuple(item[0] for item in User_ID)
        Nama_File = tuple(item[0] for item in Nama_File)
        Hasil_Prediksi = tuple(item[0] for item in Hasil_Prediksi)

        data = [
            {
                'jumlah': jumlah_kebun[0],
                'operator': jumlah_operator[0],
                'prediksi': jumlah_data[0],
                'waktu': waktu,
                'ID_Kebun': ID_kebun,
                'User_ID': User_ID,
                'Nama_File': Nama_File,
                'Hasil_Prediksi': Hasil_Prediksi
            }
        ]
        new_data = [
            {
                'waktu': waktu,
                'ID_Kebun': kebun,
                'User_ID': user,
                'Nama_File': file,
                'Hasil_Prediksi': hasil
            }
            for item in data
            for waktu, kebun, user, file, hasil in zip(item['waktu'], item['ID_Kebun'], item['User_ID'], item['Nama_File'], item['Hasil_Prediksi'])
        ]

        # Pagination settings
        page = request.args.get(get_page_parameter(), type=int, default=1)
        per_page = 5  # Adjust the number of items per page as needed
        offset = (page - 1) * per_page
        total = len(new_data)

        pagination_data = new_data[offset: offset + per_page]
        pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

        return render_template('index.html', data=pagination_data,data2=data, page=page, per_page=per_page, pagination=pagination, user=session['foto'])


if __name__ == '__main__':
    app.run(debug=True)