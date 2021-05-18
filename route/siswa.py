from flask import Flask, render_template, request, session, url_for, redirect, jsonify, Blueprint
from flask_mysqldb import MySQL
from controller.kelas.kelas import getDataKelas, DataGuru,DataSiswa,DataPelajaran,DataJurusan,DataKelasX
from controller.siswa.siswa import ClassSiswa
siswa = Blueprint('siswa', __name__, url_prefix='/siswa')
app = Flask(__name__)

app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'siasat'
mysql = MySQL(app)

@siswa.before_request
def before_request_func():
    if session['status'] !='siswa':
        return redirect('/')

@siswa.route('/jadwal', methods=['GET', 'POST'])
def ListJadwal():
    Siswa = ClassSiswa()
    Senin,Selasa,Rabu,Kamis,Jumat = Siswa.GetDataListJadwal(session['id'])
    return render_template('siswa/tablejadwal.html',Senin= Senin,Selasa= Selasa,Rabu= Rabu,Kamis= Kamis,Jumat= Jumat,)

@siswa.route('/nilai', methods=['GET', 'POST'])
def ListNilai():
    Siswa = ClassSiswa()
    getDataNilai = Siswa.NilaiSiswa(session['id'])
    return render_template('siswa/tablenilai.html', Nilai=getDataNilai)

@siswa.route('/transkip', methods=['GET', 'POST'])
def ListTranskip():
    Siswa = ClassSiswa()
    getDataNilai = Siswa.TranskipSiswa(session['id'])
    return render_template('siswa/tablenilai.html', Nilai=getDataNilai)

    