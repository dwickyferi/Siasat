from flask import Flask, render_template, request, session, url_for, redirect, jsonify, Blueprint
from flask_mysqldb import MySQL
from controller.kelas.kelas import getDataKelas, DataGuru,DataSiswa,DataPelajaran,DataJurusan,DataKelasX,Pengumuman
from werkzeug.utils import secure_filename
import os
import json
import datetime


admin = Blueprint('admin', __name__, url_prefix='/admin')
app = Flask(__name__)

app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'siasat'
UPLOAD_FOLDER = 'static/logo/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
mysql = MySQL(app)

@admin.before_request
def before_request_func():
    if session['status'] !='admin':
        return redirect('/')

@admin.route('/kelasxi', methods=['GET', 'POST'])
def KelasXI():
    getDataKelasX = getDataKelas()
    getData = getDataKelasX.ClassXI()
    return render_template('admin/tablekelasxi.html', dataKelas=getData)


@admin.route('/kelasxii', methods=['GET', 'POST'])
def KelasXII():
    getDataKelasX = getDataKelas()
    getData = getDataKelasX.ClassXII()
    return render_template('admin/tablekelasxii.html', dataKelas=getData)

# CRUD Data Kelas X
@admin.route('/kelasx', methods=['GET', 'POST'])
def KelasX():
    getDataKelasX = getDataKelas()
    getData = getDataKelasX.ClassX()
    return render_template('admin/tablekelasx.html', dataKelas=getData)

@admin.route('/editkelasx/<id_kelas>', methods=['GET', 'POST'])
def EditKelasX(id_kelas):
    getDataKelasX = getDataKelas()
    getData = getDataKelasX.GetDetailKelasX(id_kelas)
    return jsonify({"data": getData})

@admin.route('/update/kelasx', methods=['GET', 'POST'])
def UpdateKelasX():
    _json = request.json
    IDKelas = _json['EditID']
    namaKelas = _json['namaKelas']
    jurusan = _json['jurusan']
    walikelas = _json['walikelas']
    dataUpdate = {
        'id': IDKelas,
        'nama': namaKelas,
        'jurusan': jurusan,
        'walikelas': walikelas
    }
    getDataKelasX = getDataKelas()
    Respon = getDataKelasX.UpdateKelasX(dataUpdate)
    return jsonify({"respon": Respon})


@admin.route('/delete/kelasx', methods=['GET', 'POST'])
def DeleteKelasX():
    _json = request.json
    IDKelas = _json['id']
    DeleteKelas = getDataKelas()
    Respon = DeleteKelas.DeleteKelasX(IDKelas)
    return jsonify({"respon": Respon})


@admin.route('/input/kelasx', methods=['GET', 'POST'])
def InpuKelas():
    _json = request.json
    namaKelas = _json['namaKelas']
    jurusan = _json['jurusan']
    walikelas = _json['walikelas']
    kelas = _json['kelas']
    dataInsert = {
        'namaKelas': namaKelas,
        'jurusan': jurusan,
        'walikelas': walikelas,
        'kelas': kelas
    }
    resp = DataKelasX()
    Respon = resp.InsertData(dataInsert)
    return jsonify({"data": Respon})

@admin.route('/subkelasx/<id_kelas>', methods=['GET', 'POST'])
def SubKelasX(id_kelas):
    getDataKelasX = getDataKelas()
    getDataDetail = getDataKelasX.DetailClassX(id_kelas)
    ListData = getDataKelasX.GetDataSiswaList(id_kelas)
    ListPelajaran = getDataKelasX.GetDataPelajaran(id_kelas)
    Senin,Selasa,Rabu,Kamis,Jumat = getDataKelasX.GetDataListJadwal(id_kelas)
    return render_template('admin/subkelasx.html', dataKelas=getDataDetail, 
    Senin= Senin,Selasa= Selasa,Rabu= Rabu,Kamis= Kamis,Jumat= Jumat,
    Detail=getDataDetail, List=ListData, Pelajaran=ListPelajaran)

@admin.route('/subkelasx/siswa', methods=['GET', 'POST'])
def SiswaSubKelasX():
    getDataSiswa = DataSiswa()
    Respon = getDataSiswa.GetDataSiswa()
    return jsonify({"data": Respon})

@admin.route('/subkelasx/pelajaran', methods=['GET', 'POST'])
def PelajaranSubKelasX():
    getData = DataPelajaran()
    Respon = getData.GetDataPelajaran()
    print(Respon)
    return jsonify({"data": Respon})

@admin.route('/subsiswa/deleteAll', methods=['GET', 'POST'])
def DeleteAllSubSiswa():
    _json = request.json
    IDKelas = _json['id']
    getDataSiswa = getDataKelas()
    Respon = getDataSiswa.DeleteAllData(IDKelas)
    return jsonify({"respon": Respon})

@admin.route('/subsiswa/delete', methods=['GET', 'POST'])
def DeleteSubSiswa():
    _json = request.json
    IDKelas = _json['id']
    NIS = _json['nis']
    DeleteData = getDataKelas()
    Respon = DeleteData.DeleteData(IDKelas,NIS)
    return jsonify({"respon": Respon})

@admin.route('/input/subkelasx/siswa', methods=['GET', 'POST'])
def InsertSiswaSubKelasX():
    _json = request.json
    dataSiswa = _json['dataSiswa']
    IDKelas = _json['IDKelas']
    getDataSiswa = getDataKelas()
    Respon = getDataSiswa.InsertSubKelasSiswaX(IDKelas, dataSiswa)
    return jsonify({"data": Respon})

@admin.route('/input/subkelasx/pelajaran', methods=['GET', 'POST'])
def InsertPelajaranSubKelasX():
    _json = request.json
    dataPelajaran = _json['dataPelajaran']
    IDKelas = _json['IDKelas']
    getDataSiswa = getDataKelas()
    Respon = getDataSiswa.InsertSubKelasPelajaranX(IDKelas, dataPelajaran)
    return jsonify({"data": Respon})

@admin.route('/delete/subkelasx/pelajaran', methods=['GET', 'POST'])
def DeletePelajaranSubKelasX():
    _json = request.json
    id_pelajaran = _json['id']
    getDataSiswa = getDataKelas()
    Respon = getDataSiswa.DeleteSubKelasPelajaranX(id_pelajaran)
    return jsonify({"data": Respon})

@admin.route('/subkelas/<kelas>/<pelajaran>/<id_pelajaran>', methods=['GET', 'POST'])
def ViewNilai(kelas,pelajaran,id_pelajaran):
    getDataKelasX = getDataKelas()
    getDataDetail = getDataKelasX.DetailKelasNilai(kelas, pelajaran)
    getDataNilai = getDataKelasX.NilaiSiswa(kelas, pelajaran,id_pelajaran)
    return render_template('admin/tablenilai.html', Detail=getDataDetail, Nilai=getDataNilai, IDNilai = id_pelajaran)

@admin.route('/subkelasx/siswakelas/<kelas>', methods=['GET', 'POST'])
def Siswa(kelas):
    getDataKelasX = getDataKelas()
    Respon =getDataKelasX.GetSiswaAmbil(kelas)
    print(Respon)
    return jsonify({"data": Respon})

@admin.route('/nilai/input', methods=['GET', 'POST'])
def SiswaInputNilai():
    _json = request.json
    SiswaKelas = _json['SiswaKelas']
    Kelas = _json['Kelas']
    uts = _json['uts']
    uas = _json['uas']
    Pelajaran = _json['Pelajaran']
    IDNilai = _json['IDNilai']
    dataInsert = {
        'SiswaKelas': SiswaKelas,
        'Kelas': Kelas,
        'uts': uts,
        'uas': uas,
        'Pelajaran':Pelajaran,
        'IDNilai':IDNilai
    }
    getDataKelasX = getDataKelas()
    Respon =getDataKelasX.InsertNilai(dataInsert)
    return jsonify({"data": Respon})

@admin.route('/nilai/getnilai/<id_nilai>', methods=['GET', 'POST'])
def EditNilai(id_nilai):
    getDataKelasX = getDataKelas()
    print(id_nilai)
    Respon = getDataKelasX.GetDataNilai(id_nilai)
    return jsonify({"data": Respon})

@admin.route('/nilai/update', methods=['GET', 'POST'])
def UpdateNilai():
    _json = request.json
    iddata = _json['id']
    uas = _json['uas']
    uts = _json['uts']
    dataUpdate = {
        'iddata': iddata,
        'uts': uts,
        'uas': uas
    }
    getDataKelasX = getDataKelas()
    Respon =getDataKelasX.UpdateNilai(dataUpdate)
    return jsonify({"data": Respon})

@admin.route('/nilai/transkip', methods=['GET', 'POST'])
def UpdateTranskip():
    _json = request.json
    iddata = _json['id']
    getDataKelasX = getDataKelas()
    Respon =getDataKelasX.UpdateTranskip(iddata)
    return jsonify({"data": Respon})

@admin.route('/nilai/delete', methods=['GET', 'POST'])
def DeleteNilai():
    _json = request.json
    iddata = _json['id']
    getDataKelasX = getDataKelas()
    Respon =getDataKelasX.DeleteNilai(iddata)
    return jsonify({"data": Respon})

@admin.route('/jadwal/input', methods=['GET', 'POST'])
def InputJadwal():
    _json = request.json
    namaPelajaran = _json['namaPelajaran']
    JadwalAwal = _json['JadwalAwal']
    JadwalAkhir = _json['JadwalAkhir']
    Hari = _json['Hari']
    Guru = _json['Guru']
    IDKelas =  _json['IDKelas']
    dataInsert = {
        'namaPelajaran': namaPelajaran,
        'JadwalAwal': JadwalAwal,
        'Hari': Hari,
        'Guru': Guru,
        'JadwalAkhir':JadwalAkhir,
        'IDKelas':IDKelas
    }
    print(dataInsert)
    getDataKelasX = getDataKelas()
    Respon =getDataKelasX.InsertJadwal(dataInsert)
    return jsonify({"data": Respon})

@admin.route('/jadwal/edit/<id_jadwal>', methods=['GET', 'POST'])
def EditJadwal(id_jadwal):
    getDataKelasX = getDataKelas()
    Respon =getDataKelasX.EditJadwal(id_jadwal)
    return jsonify({"data": Respon})

@admin.route('/jadwal/delete', methods=['GET', 'POST'])
def DeleteJadwal():
    _json = request.json
    idJadwal = _json['id']
    print(idJadwal)
    getDataKelasX = getDataKelas()
    Respon =getDataKelasX.DeleteJadwal(idJadwal)
    print(Respon)
    return jsonify({"data": Respon})


# Proses CRUD Guru
@admin.route('/dataguru', methods=['GET', 'POST'])
def GetDataGuru():
    getDataGuru = DataGuru()
    Respon = getDataGuru.GetDataGuru()
    return render_template('admin/tableguru.html', dataGuru=Respon)


@admin.route('/input/guru', methods=['GET', 'POST'])
def InsertGuru():
    _json = request.json
    nip = _json['nip']
    nama = _json['nama']
    password = _json['password']
    bidangKeahlian = _json['bidangKeahlian']
    programKeahlian = _json['programKeahlian']
    kompetensiKeahlian = _json['kompetensiKeahlian']
    dataUpdate = {
        'nip': nip,
        'nama': nama,
        'password': password,
        'bidangKeahlian': bidangKeahlian,
        'programKeahlian': programKeahlian,
        'kompetensiKeahlian': kompetensiKeahlian
    }
    InsertData = DataGuru()
    Respon = InsertData.InsertDataGuru(dataUpdate)
    return jsonify({"respon": Respon})

@admin.route('/edit/guru/<nip>', methods=['GET', 'POST'])
def EditGuru(nip):
    GetDataGuru = DataGuru()
    Respon = GetDataGuru.EditData(nip)
    return jsonify({"data": Respon})

@admin.route('/delete/guru', methods=['GET', 'POST'])
def DeleteGuru():
    _json = request.json
    NIP = _json['id']
    GetDataGuru = DataGuru()
    Respon = GetDataGuru.DeleteGuru(NIP)
    return jsonify({"data": Respon})

@admin.route('/update/guru', methods=['GET', 'POST'])
def UpdateDataGuru():
    _json = request.json
    nip = _json['nip']
    nama = _json['nama']
    password = _json['password']
    bidangKeahlian = _json['bidangKeahlian']
    programKeahlian = _json['programKeahlian']
    kompetensiKeahlian = _json['kompetensiKeahlian']
    dataUpdate = {
        'nip': nip,
        'nama': nama,
        'password': password,
        'bidangKeahlian': bidangKeahlian,
        'programKeahlian': programKeahlian,
        'kompetensiKeahlian': kompetensiKeahlian
    }
    InsertData = DataGuru()
    Respon = InsertData.UpdateDataGuru(dataUpdate)
    return jsonify({"data": Respon})

# Proses Data Siswa
@admin.route('/datasiswa', methods=['GET', 'POST'])
def GetDataSiswa():
    getDataSiswa = DataSiswa()
    Respon = getDataSiswa.GetDataSiswa()
    return render_template('admin/tablesiswa.html', dataSiswa=Respon)

@admin.route('/input/siswa', methods=['GET', 'POST'])
def InsertSiswa():
    _json = request.json
    nis = _json['nis']
    nama = _json['nama']
    password = _json['password']
    dataUpdate = {
        'nis': nis,
        'nama': nama,
        'password': password,
    }
    InsertData = DataSiswa()
    Respon = InsertData.InsertDataSiswa(dataUpdate)
    return jsonify({"data": Respon})

@admin.route('/edit/siswa/<nis>', methods=['GET', 'POST'])
def EditSiswa(nis):
    GetDataGuru = DataSiswa()
    Respon = GetDataGuru.EditData(nis)
    return jsonify({"data": Respon})

@admin.route('/delete/siswa', methods=['GET', 'POST'])
def DeleteSiswa():
    _json = request.json
    NIP = _json['id']
    GetDataSiswa = DataSiswa()
    Respon = GetDataSiswa.DeleteSiswa(NIP)
    return jsonify({"data": Respon})

@admin.route('/update/siswa', methods=['GET', 'POST'])
def UpdateDataSiswa():
    _json = request.json
    nis = _json['nis']
    nama = _json['nama']
    password = _json['password']
    dataUpdate = {
        'nis': nis,
        'nama': nama,
        'password': password,
    }
    InsertData = DataSiswa()
    Respon = InsertData.UpdateDataSiswa(dataUpdate)
    return jsonify({"data": Respon})


# Proses Pelajaran
@admin.route('/data/pelajaran', methods=['GET', 'POST'])
def GetDataPelajaran():
    getDataPelajaran = DataPelajaran()
    Respon = getDataPelajaran.GetDataPelajaran()
    return render_template('admin/tablepelajaran.html', dataPelajaran=Respon)

@admin.route('/input/pelajaran', methods=['GET', 'POST'])
def InsertPelajaran():
    _json = request.json
    nama = _json['nama']
    dataUpdate = {
        'nama': nama,
    }
    InsertData = DataPelajaran()
    Respon = InsertData.InsertDataPelajaran(dataUpdate)
    return jsonify({"respon": Respon})

@admin.route('/edit/pelajaran/<id>', methods=['GET', 'POST'])
def EditPelajaran(id):
    GetDataPelajaran = DataPelajaran()
    Respon = GetDataPelajaran.EditData(id)
    return jsonify({"data": Respon})

@admin.route('/delete/pelajaran', methods=['GET', 'POST'])
def DeletePelajaran():
    _json = request.json
    id = _json['id']
    GetDataPelajaran = DataPelajaran()
    Respon = GetDataPelajaran.DeleteDataPelajaran(id)
    return jsonify({"data": Respon})

@admin.route('/update/pelajaran', methods=['GET', 'POST'])
def UpdateDataPelajaran():
    _json = request.json
    id = _json['id']
    nama = _json['nama']
    dataUpdate = {
        'id': id,
        'nama': nama,
    }
    InsertData = DataPelajaran()
    Respon = InsertData.UpdateDataPelajaran(dataUpdate)
    return jsonify({"data": Respon})

# Proses Pelajaran
@admin.route('/data/jurusan', methods=['GET', 'POST'])
def GetDataJurusan():
    getDataJurusan = DataJurusan()
    Respon = getDataJurusan.GetDataJurusan()
    return render_template('admin/tablejurusan.html', dataJurusan=Respon)

@admin.route('/input/jurusan', methods=['GET', 'POST'])
def InsertJurusan():
    # nama = request.json['objArr']
    generateNameFile=''
    dataValue = request.form['objArr']
    dataDict = json.loads(dataValue)[0]
    namaKelas = dataDict["namaKelas"]
    program= dataDict["program"]
    bidang= dataDict["bidang"]
    logo = request.files['logo']
    splitData = os.path.splitext(logo.filename)
    now = datetime.datetime.now()
    generateNameFile = str(now.hour)+str(now.minute)+str(now.second)+splitData[1]
    logo.save(os.path.join(app.config['UPLOAD_FOLDER'], generateNameFile))
    filename = secure_filename(logo.filename)
    dataUpdate = {
        'nama': namaKelas,
        'program': program,
        'bidang': bidang,
        'logo':generateNameFile
    }
    InsertData = DataJurusan()
    Respon = InsertData.InsertDataJurusan(dataUpdate)
    return jsonify({"respon": Respon})

@admin.route('/delete/jurusan', methods=['GET', 'POST'])
def DeleteJurusan():
    _json = request.json
    id = _json['id']
    GetDataJurusan = DataJurusan()
    Respon = GetDataJurusan.DeleteDataJurusan(id)
    return jsonify({"data": Respon})

@admin.route('/edit/jurusan/<id>', methods=['GET', 'POST'])
def EditJurusan(id):
    GetDataJurusan = DataJurusan()
    Respon = GetDataJurusan.EditData(id)
    return jsonify({"data": Respon})

@admin.route('/update/jurusan', methods=['GET', 'POST'])
def UpdateDataJurusan():
    _json = request.json
    idjurusan = _json['idkelas']
    namaKelas = _json['namaKelas']
    program = _json['program']
    bidang = _json['bidang']
    dataUpdate = {
        'idjurusan': idjurusan,
        'namaKelas': namaKelas,
        'program': program,
        'bidang': bidang
    }
    InsertData = DataJurusan()
    Respon = InsertData.UpdateDataJurusan(dataUpdate)
    return jsonify({"data": Respon})

@admin.route('/data/select/jurusan', methods=['GET', 'POST'])
def GetDataJurusanSelect():
    getDataJurusan = DataJurusan()
    Respon = getDataJurusan.GetDataJurusan()
    return jsonify({"data": Respon})

@admin.route('/data/select/guru', methods=['GET', 'POST'])
def GetDataGuruSelect():
    getDataGuru = DataGuru()
    Respon = getDataGuru.GetDataGuru()
    return jsonify({"data": Respon})

@admin.route('/pengumuman', methods=['GET', 'POST'])
def PengumumanData():
    Detail = Pengumuman()
    data = Detail.GetPengumuman()
    return render_template('admin/tablepengumuman.html',data=data[0][1], idpengumuman=data[0][0])

@admin.route('/update/pengumuman', methods=['GET', 'POST'])
def PengumumanDataUpdate():
    _json = request.json
    data = _json['data']
    Detail = Pengumuman()
    data = Detail.UpdatePengumuman(data)
    return jsonify({"data": data})


