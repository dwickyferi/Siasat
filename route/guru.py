from flask import Flask, render_template, request, session, url_for, redirect, jsonify, Blueprint
from flask_mysqldb import MySQL
from controller.kelas.kelas import getDataKelas, DataGuru,DataSiswa,DataPelajaran,DataJurusan,DataKelasX
from controller.guru.guru import ClassGuru
guru = Blueprint('guru', __name__, url_prefix='/guru')
app = Flask(__name__)

app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'siasat'
mysql = MySQL(app)

@guru.before_request
def before_request_func():
    if session['status'] !='guru':
        return redirect('/')

@guru.route('/jadwal', methods=['GET', 'POST'])
def ListJadwal():
    Guru = ClassGuru()
    Senin,Selasa,Rabu,Kamis,Jumat = Guru.GetDataListJadwal(session['id'])
    return render_template('guru/tablejadwal.html',Senin= Senin,Selasa= Selasa,Rabu= Rabu,Kamis= Kamis,Jumat= Jumat,)