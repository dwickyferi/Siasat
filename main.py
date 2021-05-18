from flask import Flask, render_template, request, session, url_for, redirect, jsonify
from flask_mysqldb import MySQL
from route.admin import admin
from controller.guru.guru import ClassGuru
from controller.siswa.siswa import ClassSiswa
from werkzeug.security import generate_password_hash, check_password_hash
from route.siswa import siswa
from route.guru import guru
from controller.kelas.kelas import Pengumuman



app = Flask(__name__)
app.secret_key = "siasat"
app.register_blueprint(admin)
app.register_blueprint(siswa)
app.register_blueprint(guru)

app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'siasat'
mysql = MySQL(app)

@app.route('/login', methods=['GET', 'POST'])
def Login():
    return render_template('login.html')

@app.route('/loginuser', methods=['GET', 'POST'])
def LoginUser():
    _json = request.json
    username = _json['email']
    password = _json['pass']
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM tb_admin WHERE email = %s AND password = %s', (username, password,))
    account = cursor.fetchone()
    cursor2 = mysql.connection.cursor()
    cursor2.execute('SELECT * FROM tb_guru WHERE nip = %s', (username,))
    account2 = cursor2.fetchone()
    cursor3 = mysql.connection.cursor()
    cursor3.execute('SELECT * FROM tb_siswa WHERE nis = %s', (username,))
    account3 = cursor3.fetchone()
    # Fetch one record and return result
    if account:
        session['nama']=account[3]
        session['status']="admin"
        resp = {'status':200}
    elif account2:
        if check_password_hash(account2[2],password):
            session['nama']=account2[1]
            session['status']="guru"
            session['id']=account2[0]
            resp = {'status':200}
        else:
            return redirect('/login')
    elif account3:
        if check_password_hash(account3[2],password):
            session['nama']=account3[1]
            session['status']="siswa"
            session['id']=account3[0]
            resp = {'status':200}
        else:
            return redirect('/login')
    else:
        return redirect('/login')
    return resp
    
@app.route('/logout', methods=['GET', 'POST'])
def LogoutData():
    return redirect('/login')

@app.route('/', methods=['GET', 'POST'])
def Dashboard():
    if 'nama' in session:
        if session['status']=="admin":
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT count(id) FROM tb_kelas')
            kelas = cursor.fetchone()
            cursor.execute('SELECT count(nis) FROM tb_siswa')
            siswa = cursor.fetchone()
            cursor.execute('SELECT count(nip) FROM tb_guru')
            guru = cursor.fetchone()
            return render_template('admin/dashboard.html', dataUser =session['nama'], kelas=kelas[0], guru=guru[0], siswa=siswa[0])
        elif session['status']=="guru":
            getDetail = ClassGuru()
            detail = getDetail.GetDetailGuru(session['id'])
            return render_template('guru/dashboard.html', dataUser =session['nama'], detail=detail)
        else:
            Detail = Pengumuman()
            data = Detail.GetPengumuman()
            getDetail = ClassSiswa()
            detail = getDetail.GetDetailSiswa(session['id'])
            return render_template('siswa/dashboard.html', dataUser =session['nama'], detail=detail,pengumuman=data[0][1])
    else:
        return redirect('/login')

if __name__ == '__main__':
	app.run(port=5000, debug=True)