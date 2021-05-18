from flask import Flask, render_template, request, session, url_for, redirect, jsonify, Blueprint
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
app = Flask(__name__)

UPLOAD_FOLDER = 'static/logo/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

mysql = MySQL(app)

class getDataKelas:
    def ClassX(self):
        dataKelas = []
        data = []
        cursor = mysql.connection.cursor()
        cursor.execute("""SELECT tb_kelas.id as ID, tb_kelas.nama as NamaKelas,tb_jurusan.nama as nama_jurusan,tb_guru.nama as nama_guru FROM tb_kelas 
        inner join tb_jurusan on tb_kelas.id_jurusan = tb_jurusan.id
        inner join tb_guru on tb_kelas.id_guru = tb_guru.nip where tb_kelas.kelas = 'X'""")
        kelas = cursor.fetchall()
        for x in kelas:
            dataKelas.append(x)
        return dataKelas

    def ClassXI(self):
        dataKelas = []
        data = []
        cursor = mysql.connection.cursor()
        cursor.execute("""SELECT * FROM tb_kelas where kelas = 'XI'""")
        kelas = cursor.fetchall()
        for x in kelas:
            dataKelas.append(x)
        return dataKelas

    def ClassXII(self):
        dataKelas = []
        data = []
        cursor = mysql.connection.cursor()
        cursor.execute("""SELECT * FROM tb_kelas where kelas = 'XII'""")
        kelas = cursor.fetchall()
        for x in kelas:
            dataKelas.append(x)
        return dataKelas

    def GetDetailKelasX(self, idKelas):
        dataKelas = []
        data = []
        cursor = mysql.connection.cursor()
        cursor.execute(
            """SELECT * FROM tb_kelas where id = %s 
            """, (idKelas, ))
        kelas = cursor.fetchall()
        for x in kelas:
            dataKelas.append(x)
        return dataKelas

    def GetDataSiswaList(self, idKelas):
        dataKelas = []
        data = []
        cursor = mysql.connection.cursor()
        cursor.execute(
            """SELECT tb_kelas_siswa.id_kelas as idkelas, tb_kelas_siswa.id_siswa as id, tb_siswa.nama FROM tb_kelas_siswa
            inner join tb_siswa on tb_siswa.nis = tb_kelas_siswa.id_siswa 
            where tb_kelas_siswa.id_kelas = %s 
            """, (idKelas, ))
        kelas = cursor.fetchall()
        for x in kelas:
            dataKelas.append(x)
        return dataKelas

    def GetDataPelajaran(self, idKelas):
        dataKelas = []
        data = []
        cursor = mysql.connection.cursor()
        cursor.execute(
            """SELECT tb_pelajaran_ambil.id_pelajaran_ambil as idPelajaran, tb_pelajaran.nama as nama, tb_pelajaran_ambil.id_pelajaran as IDPelajaran FROM tb_pelajaran_ambil
            inner join tb_pelajaran on tb_pelajaran_ambil.id_pelajaran = tb_pelajaran.id 
            where tb_pelajaran_ambil.id_kelas = %s 
            """, (idKelas, ))
        kelas = cursor.fetchall()
        for x in kelas:
            dataKelas.append(x)
        return dataKelas

    def UpdateKelasX(self, GetData):
        respon = {'status': True}
        try:
            cursor = mysql.connection.cursor()
            cursor.execute(
                """
            update tb_kelas set nama=%s, id_jurusan=%s,id_guru=%s
            where id = %s
            """, (
                    GetData['nama'],
                    GetData['jurusan'],
                    GetData['walikelas'],
                    GetData['id'],
                ))
            mysql.connection.commit()
            cursor.close()
            respon['status'] = True
        except Exception as e:
            print(e)
            respon['status'] = False
        return respon

    def DeleteKelasX(self, ID):
        respon = {'status': True}
        try:
            cursor = mysql.connection.cursor()
            cursor.execute(
                """
            DELETE from tb_kelas 
            where id = %s
            """, (ID, ))
            mysql.connection.commit()
            cursor.close()
            respon['status'] = True
        except Exception:
            respon['status'] = False
        return respon

    def DetailClassX(self,id):
        dataKelas = []
        data = []
        cursor = mysql.connection.cursor()
        cursor.execute("""SELECT tb_kelas.id as ID, tb_kelas.nama as NamaKelas,tb_jurusan.nama as nama_jurusan,tb_guru.nama as nama_guru, tb_kelas.kelas as kelas FROM tb_kelas 
        inner join tb_jurusan on tb_kelas.id_jurusan = tb_jurusan.id
        inner join tb_guru on tb_kelas.id_guru = tb_guru.nip where tb_kelas.id = %s""", (id,))
        kelas = cursor.fetchall()
        for x in kelas:
            dataKelas.append(x)
        return dataKelas

    def InsertSubKelasSiswaX(self, id, data):
        respon = {'status': True}
        print(data[0])
        try:
            cursor = mysql.connection.cursor()
            for x in range(len(data)):
                cursor.execute(
                    """
                insert into tb_kelas_siswa (id_kelas,id_siswa)
                values (%s,%s)
                """, (int(id), data[x]))
            mysql.connection.commit()
            cursor.close()
            respon['status'] = True
        except Exception as e:
            print(e)
            respon['status'] = False
        return respon

    def InsertSubKelasPelajaranX(self, id, data):
        respon = {'status': True}
        print(data[0])
        try:
            cursor = mysql.connection.cursor()
            for x in range(len(data)):
                cursor.execute(
                    """
                insert into tb_pelajaran_ambil (id_kelas,id_pelajaran)
                values (%s,%s)
                """, (int(id), data[x]))
            mysql.connection.commit()
            cursor.close()
            respon['status'] = True
        except Exception as e:
            print(e)
            respon['status'] = False
        return respon

    def DeleteAllData(self,idkelas):
        respon = {'status': True}
        try:
            cursor = mysql.connection.cursor()
            cursor.execute(
                """
            DELETE from tb_kelas_siswa 
            where id_kelas = %s
            """, (idkelas, ))
            mysql.connection.commit()
            cursor.close()
            respon['status'] = True
        except Exception:
            respon['status'] = False
        return respon

    def DeleteData(self,idkelas, nis):
        respon = {'status': True}
        print(idkelas,nis)
        try:
            cursor = mysql.connection.cursor()
            cursor.execute(
                """
            DELETE from tb_kelas_siswa 
            where id_kelas = %s and id_siswa = %s
            """, (idkelas, nis))
            mysql.connection.commit()
            cursor.close()
            respon['status'] = True
        except Exception:
            respon['status'] = False
        return respon

    def DetailKelasNilai(self, kelas,pelajaran):
        dataKelas = []
        data = []
        cursor = mysql.connection.cursor()
        cursor.execute("""SELECT tb_kelas.id as ID, tb_kelas.nama as NamaKelas,tb_jurusan.nama as nama_jurusan,tb_guru.nama as nama_guru, tb_kelas.kelas as kelas, tb_pelajaran.nama as namapelajaran, tb_pelajaran.id as idPelajaran FROM tb_kelas 
        inner join tb_jurusan on tb_kelas.id_jurusan = tb_jurusan.id
        inner join tb_guru on tb_kelas.id_guru = tb_guru.nip 
        inner join tb_pelajaran_ambil on tb_kelas.id = tb_pelajaran_ambil.id_kelas
        inner join tb_pelajaran on tb_pelajaran_ambil.id_pelajaran = tb_pelajaran.id where tb_kelas.id = %s and tb_pelajaran.id = %s""", (kelas,pelajaran))
        kelas = cursor.fetchall()
        for x in kelas:
            dataKelas.append(x)
        return dataKelas

    def NilaiSiswa(self, kelas, pelajaran,id_pelajaran):
        dataKelas = []
        data = []
        cursor = mysql.connection.cursor()
        cursor.execute("""SELECT tb_nilai.id_siswa as NIS, tb_siswa.nama as nama, tb_nilai.uts as uts, tb_nilai.uas as uas, tb_nilai.id_nilai as iddata from tb_nilai
        inner join tb_siswa on tb_nilai.id_siswa = tb_siswa.nis
        where tb_nilai.id_pelajaran = %s and tb_nilai.id_kelas = %s and tb_nilai.id_pelajaran_ambil = %s""", (pelajaran,kelas,id_pelajaran))
        nilai = cursor.fetchall()
        for x in nilai:
            dataKelas.append(x)
        return dataKelas

    def GetSiswaAmbil(self,kelas):
        dataKelas = []
        data = []
        cursor = mysql.connection.cursor()
        cursor.execute("""SELECT tb_kelas_siswa.id_siswa as NIS, tb_siswa.nama as nama from tb_kelas_siswa
        inner join tb_siswa on tb_kelas_siswa.id_siswa = tb_siswa.nis
        where tb_kelas_siswa.id_kelas = %s""", (kelas,))
        nilai = cursor.fetchall()
        for x in nilai:
            dataKelas.append(x)
        return dataKelas

    def InsertNilai(self, Data):
        respon = {'status': True}
        try:
            cursor = mysql.connection.cursor()
            cursor.execute(
                """
            insert into tb_nilai (id_siswa,id_pelajaran, id_kelas,uts,uas,id_pelajaran_ambil)
            values (%s,%s,%s,%s,%s,%s)
            """, (Data['SiswaKelas'], Data['Pelajaran'],
                Data['Kelas'],
                Data['uts'], Data['uas'], Data['IDNilai']))
            mysql.connection.commit()
            cursor.close()
            respon['status'] = True
        except Exception as e:
            print(e)
            respon['status'] = False
        return respon

    def GetDataNilai(self, id_nilai):
        dataKelas = []
        cursor = mysql.connection.cursor()
        cursor.execute("""
        SELECT tb_nilai.id_nilai as ID_Nilai, tb_siswa.nama as nama, tb_nilai.uts as UTS, tb_nilai.uas as UAS from tb_nilai
        inner join tb_siswa on tb_siswa.nis = tb_nilai.id_siswa 
        where tb_nilai.id_nilai = %s""", (id_nilai,))
        nilai = cursor.fetchall()
        for x in nilai:
            dataKelas.append(x)
        return dataKelas

    def UpdateTranskip(self, idkelas):
        respon = {'status': True}
        try:
            cursor = mysql.connection.cursor()
            cursor.execute(
                """
            insert into tb_transkip_nilai (id_siswa,id_pelajaran, id_kelas,uts,uas,id_pelajaran_ambil)
            select id_siswa,id_pelajaran, id_kelas,uts,uas,id_pelajaran_ambil from tb_nilai
            where id_kelas = %s
            """, (idkelas,))
            mysql.connection.commit()
            cursor.close()
            respon['status'] = True
        except Exception as e:
            print(e)
            respon['status'] = False
        return respon

    def UpdateNilai(self, GetData):
        respon = {'status': True}
        try:
            cursor = mysql.connection.cursor()
            cursor.execute(
                """
            update tb_nilai set uts=%s, uas=%s
            where id_nilai = %s
            """, (
                    GetData['uts'],
                    GetData['uas'],
                    GetData['iddata'],
                ))
            mysql.connection.commit()
            cursor.close()
            respon['status'] = True
        except Exception as e:
            print(e)
            respon['status'] = False
        return respon

    def DeleteNilai(self,idnilai):
        respon = {'status': True}
        try:
            cursor = mysql.connection.cursor()
            cursor.execute(
                """
            DELETE from tb_nilai 
            where id_nilai = %s
            """, (idnilai, ))
            mysql.connection.commit()
            cursor.close()
            respon['status'] = True
        except Exception:
            respon['status'] = False
        return respon

    def InsertJadwal(self, Data):
        respon = {'status': True}
        try:
            cursor = mysql.connection.cursor()
            cursor.execute(
                """
            insert into tb_jadwal_pelajaran (hari,kelas, pelajaran, guru,jam_awal,jam_akhir)
            values (%s,%s,%s,%s,%s,%s)
            """, (Data['Hari'], Data['IDKelas'],
                Data['namaPelajaran'],
                Data['Guru'], Data['JadwalAwal'], Data['JadwalAkhir']))
            mysql.connection.commit()
            cursor.close()
            respon['status'] = True
        except Exception as e:
            print(e)
            respon['status'] = False
        return respon

    def GetDataListJadwal(self, id_kelas):
        senin = []
        selasa = []
        rabu = []
        kamis = []
        jumat = []
        cursor = mysql.connection.cursor()
        cursor.execute("""
        SELECT tb_jadwal_pelajaran.id as id_jadwal, tb_pelajaran.nama as nama ,tb_jadwal_pelajaran.hari as hari, tb_guru.nama as namaGuru, tb_jadwal_pelajaran.jam_awal as jamAwal,
        tb_jadwal_pelajaran.jam_akhir as jamAkhir from tb_jadwal_pelajaran
        inner join tb_guru on tb_jadwal_pelajaran.guru = tb_guru.nip 
        inner join tb_pelajaran on tb_jadwal_pelajaran.pelajaran = tb_pelajaran.id
        where tb_jadwal_pelajaran.kelas = %s and tb_jadwal_pelajaran.hari = 'Senin'
        order by tb_jadwal_pelajaran.jam_awal asc""", (id_kelas,))
        jadwalSenin = cursor.fetchall()
        for x in jadwalSenin:
            senin.append(x)
        cursor.execute("""
        SELECT tb_jadwal_pelajaran.id as id_jadwal, tb_pelajaran.nama as nama ,tb_jadwal_pelajaran.hari as hari, tb_guru.nama as namaGuru, tb_jadwal_pelajaran.jam_awal as jamAwal,
        tb_jadwal_pelajaran.jam_akhir as jamAkhir from tb_jadwal_pelajaran
        inner join tb_guru on tb_jadwal_pelajaran.guru = tb_guru.nip 
        inner join tb_pelajaran on tb_jadwal_pelajaran.pelajaran = tb_pelajaran.id
        where tb_jadwal_pelajaran.kelas = %s and tb_jadwal_pelajaran.hari = 'Selasa'
        order by tb_jadwal_pelajaran.jam_awal asc""", (id_kelas,))
        jadwalSelasa = cursor.fetchall()
        for x in jadwalSelasa:
            selasa.append(x)
        cursor.execute("""
        SELECT tb_jadwal_pelajaran.id as id_jadwal, tb_pelajaran.nama as nama ,tb_jadwal_pelajaran.hari as hari, tb_guru.nama as namaGuru, tb_jadwal_pelajaran.jam_awal as jamAwal,
        tb_jadwal_pelajaran.jam_akhir as jamAkhir from tb_jadwal_pelajaran
        inner join tb_guru on tb_jadwal_pelajaran.guru = tb_guru.nip 
        inner join tb_pelajaran on tb_jadwal_pelajaran.pelajaran = tb_pelajaran.id
        where tb_jadwal_pelajaran.kelas = %s and tb_jadwal_pelajaran.hari = 'Rabu'
        order by tb_jadwal_pelajaran.jam_awal asc""", (id_kelas,))
        jadwalRabu = cursor.fetchall()
        for x in jadwalRabu:
            rabu.append(x)
        cursor.execute("""
        SELECT tb_jadwal_pelajaran.id as id_jadwal, tb_pelajaran.nama as nama ,tb_jadwal_pelajaran.hari as hari, tb_guru.nama as namaGuru, tb_jadwal_pelajaran.jam_awal as jamAwal,
        tb_jadwal_pelajaran.jam_akhir as jamAkhir from tb_jadwal_pelajaran
        inner join tb_guru on tb_jadwal_pelajaran.guru = tb_guru.nip 
        inner join tb_pelajaran on tb_jadwal_pelajaran.pelajaran = tb_pelajaran.id
        where tb_jadwal_pelajaran.kelas = %s and tb_jadwal_pelajaran.hari = 'Kamis'
        order by tb_jadwal_pelajaran.jam_awal asc""", (id_kelas,))
        jadwalKamis = cursor.fetchall()
        for x in jadwalKamis:
            kamis.append(x)
        cursor.execute("""
        SELECT tb_jadwal_pelajaran.id as id_jadwal, tb_pelajaran.nama as nama ,tb_jadwal_pelajaran.hari as hari, tb_guru.nama as namaGuru, tb_jadwal_pelajaran.jam_awal as jamAwal,
        tb_jadwal_pelajaran.jam_akhir as jamAkhir from tb_jadwal_pelajaran
        inner join tb_guru on tb_jadwal_pelajaran.guru = tb_guru.nip 
        inner join tb_pelajaran on tb_jadwal_pelajaran.pelajaran = tb_pelajaran.id
        where tb_jadwal_pelajaran.kelas = %s and tb_jadwal_pelajaran.hari = 'Jumat'
        order by tb_jadwal_pelajaran.jam_awal asc""", (id_kelas,))
        jadwalJumat = cursor.fetchall()
        for x in jadwalJumat:
            jumat.append(x)
        return senin,selasa,rabu,kamis,jumat

    def EditJadwal(self, id_jadwal):
        dataJadwal = []
        cursor = mysql.connection.cursor()
        cursor.execute("""
        SELECT * from tb_jadwal_pelajaran
        where id = %s""", (id_jadwal,))
        jadwal = cursor.fetchall()
        for x in jadwal:
            dataJadwal.append(x)
        print(dataJadwal)
        return dataJadwal

    def DeleteJadwal(self,id_jadwal):
        respon = {'status': True}
        try:
            cursor = mysql.connection.cursor()
            cursor.execute(
                """
            DELETE from tb_jadwal_pelajaran 
            where id = %s
            """, (id_jadwal, ))
            mysql.connection.commit()
            cursor.close()
            respon['status'] = True
        except Exception:
            respon['status'] = False
        return respon

    def DeleteSubKelasPelajaranX(self, id):
        respon = {'status': True}
        try:
            cursor = mysql.connection.cursor()
            cursor.execute(
                """
            DELETE from tb_pelajaran_ambil 
            where id_pelajaran_ambil = %s
            """, (id, ))
            mysql.connection.commit()
            cursor.close()
            respon['status'] = True
        except Exception:
            respon['status'] = False
        return respon

class DataGuru():
    def GetDataGuru(self):
        dataGuru = []
        cursor = mysql.connection.cursor()
        cursor.execute("""SELECT * FROM tb_guru""")
        Data = cursor.fetchall()
        for x in Data:
            dataGuru.append(x)
        return dataGuru

    def InsertDataGuru(self, Data):
        respon = {'status': True}
        try:
            cursor = mysql.connection.cursor()
            cursor.execute(
                """
            insert into tb_guru (nip,nama,password, bidang_keahlian,program_keahlian,kompetensi_keahlian)
            values (%s,%s,%s,%s,%s,%s)
            """, (Data['nip'], Data['nama'],
                generate_password_hash(Data['password']), Data['bidangKeahlian'],
                Data['programKeahlian'], Data['kompetensiKeahlian']))
            mysql.connection.commit()
            cursor.close()
            respon['status'] = True
        except Exception as e:
            print(e)
            respon['status'] = False
        return respon

    def EditData(self, nip):
        dataGuru = []
        cursor = mysql.connection.cursor()
        cursor.execute("""SELECT * FROM tb_guru where nip = %s""", (nip,))
        Data = cursor.fetchall()
        print(Data)
        for x in Data:
            dataGuru.append(x)
        return dataGuru

    def DeleteGuru(self, nip):
        respon = {'status': True}
        try:
            cursor = mysql.connection.cursor()
            cursor.execute(
                """
            DELETE from tb_guru 
            where nip = %s
            """, (nip, ))
            mysql.connection.commit()
            cursor.close()
            respon['status'] = True
        except Exception:
            respon['status'] = False
        return respon

    def UpdateDataGuru(self, Data):
        respon = {'status': True}
        PasswordNew = ''
        try:
            cursor = mysql.connection.cursor()
            cursor.execute("""SELECT password FROM tb_guru where nip = %s""", (Data['nip'],))
            PasswordOld = cursor.fetchall()
            if Data['password'] !='':
                PasswordNew = generate_password_hash(Data['password'])
            else:
                PasswordNew = PasswordOld
            cursor.execute(
                """
            update tb_guru set nama=%s,password=%s, bidang_keahlian=%s,program_keahlian=%s,kompetensi_keahlian=%s where nip=%s
            """, ( Data['nama'],
                PasswordNew, Data['bidangKeahlian'],
                Data['programKeahlian'], Data['kompetensiKeahlian'],Data['nip']))
            mysql.connection.commit()
            cursor.close()
            respon['status'] = True
        except Exception as e:
            print(e)
            respon['status'] = False
        return respon


class DataSiswa:
    def GetDataSiswa(self):
        dataSiswa = []
        cursor = mysql.connection.cursor()
        cursor.execute("""SELECT * FROM tb_siswa""")
        Data = cursor.fetchall()
        for x in Data:
            dataSiswa.append(x)
        return dataSiswa

    def InsertDataSiswa(self, Data):
        respon = {'status': True}
        try:
            cursor = mysql.connection.cursor()
            cursor.execute(
                """
            insert into tb_siswa (nis,nama,password)
            values (%s,%s,%s)
            """, (Data['nis'], Data['nama'],
                generate_password_hash(Data['password'])))
            mysql.connection.commit()
            cursor.close()
            respon['status'] = True
        except Exception as e:
            print(e)
            respon['status'] = False
        return respon

    def EditData(self, nip):
        dataSiswa = []
        cursor = mysql.connection.cursor()
        cursor.execute("""SELECT * FROM tb_siswa where nis = %s""", (nip,))
        Data = cursor.fetchall()
        for x in Data:
            dataSiswa.append(x)
        return dataSiswa

    def DeleteSiswa(self, nis):
        respon = {'status': True}
        try:
            cursor = mysql.connection.cursor()
            cursor.execute(
                """
            DELETE from tb_siswa 
            where nis = %s
            """, (nis, ))
            mysql.connection.commit()
            cursor.close()
            respon['status'] = True
        except Exception:
            respon['status'] = False
        return respon

    def UpdateDataSiswa(self, Data):
        respon = {'status': True}
        PasswordNew = ''
        try:
            cursor = mysql.connection.cursor()
            cursor.execute("""SELECT password FROM tb_siswa where nis = %s""", (Data['nis'],))
            PasswordOld = cursor.fetchall()
            if Data['password'] !='':
                PasswordNew = generate_password_hash(Data['password'])
            else:
                PasswordNew = PasswordOld
            cursor.execute(
                """
            update tb_siswa set nama=%s,password=%s where nis=%s
            """, ( Data['nama'],
                PasswordNew,Data['nis']))
            mysql.connection.commit()
            cursor.close()
            respon['status'] = True
        except Exception as e:
            print(e)
            respon['status'] = False
        return respon

class DataPelajaran:
    def GetDataPelajaran(self):
        dataPelajaran = []
        cursor = mysql.connection.cursor()
        cursor.execute("""SELECT * FROM tb_pelajaran""")
        Data = cursor.fetchall()
        for x in Data:
            dataPelajaran.append(x)
        return dataPelajaran

    def InsertDataPelajaran(self, Data):
        respon = {'status': True}
        try:
            cursor = mysql.connection.cursor()
            cursor.execute(
                """
            insert into tb_pelajaran (nama)
            values (%s)
            """, (Data['nama'],))
            mysql.connection.commit()
            cursor.close()
            respon['status'] = True
        except Exception as e:
            print(e)
            respon['status'] = False
        return respon

    def EditData(self, id):
        dataPelajaran = []
        cursor = mysql.connection.cursor()
        cursor.execute("""SELECT * FROM tb_pelajaran where id = %s""", (id,))
        Data = cursor.fetchall()
        for x in Data:
            dataPelajaran.append(x)
        return dataPelajaran

    def DeleteDataPelajaran(self, id):
        respon = {'status': True}
        try:
            cursor = mysql.connection.cursor()
            cursor.execute(
                """
            DELETE from tb_pelajaran 
            where id = %s
            """, (id, ))
            mysql.connection.commit()
            cursor.close()
            respon['status'] = True
        except Exception:
            respon['status'] = False
        return respon

    def UpdateDataPelajaran(self, Data):
        respon = {'status': True}
        PasswordNew = ''
        try:
            cursor = mysql.connection.cursor()
            cursor.execute(
                """
            update tb_pelajaran set nama=%s where id=%s
            """, ( Data['nama'],Data['id']))
            mysql.connection.commit()
            cursor.close()
            respon['status'] = True
        except Exception as e:
            print(e)
            respon['status'] = False
        return respon

class DataJurusan:
    def GetDataJurusan(self):
        dataJurusan = []
        cursor = mysql.connection.cursor()
        cursor.execute("""SELECT * FROM tb_jurusan""")
        Data = cursor.fetchall()
        for x in Data:
            dataJurusan.append(x)
        return dataJurusan

    def InsertDataJurusan(self,Data):
        respon = {'status': True}
        try:
            cursor = mysql.connection.cursor()
            cursor.execute(
                """
            insert into tb_jurusan (nama,program,bidang,logo)
            values (%s,%s,%s,%s)
            """, (Data['nama'],Data['program'],Data['bidang'],Data['logo']))
            mysql.connection.commit()
            cursor.close()
            respon['status'] = True
        except Exception as e:
            respon['status'] = False
        return respon
        
    def DeleteLogoJurusan(self,id):
        respon = {'status': True}
        try:
            cursor = mysql.connection.cursor()
            dataJurusan=[]
            cursor.execute("""SELECT * FROM tb_jurusan where id = %s""", (id,))
            Data = cursor.fetchall()
            for x in Data:
                dataJurusan.append(x)
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'],dataJurusan[0][4]))
            respon['status'] = True
        except Exception:
            respon['status'] = False
        return respon

    def DeleteDataJurusan(self, id):
        respon = {'status': True}
        try:
            cursor = mysql.connection.cursor()
            self.DeleteLogoJurusan(id)
            cursor.execute(
                """
                DELETE from tb_jurusan 
                where id = %s
            """, (id, ))
            mysql.connection.commit()
            cursor.close()
            respon['status'] = True
        except Exception:
            respon['status'] = False
        return respon

    def EditData(self, id):
        dataPelajaran = []
        cursor = mysql.connection.cursor()
        cursor.execute("""SELECT * FROM tb_jurusan where id = %s""", (id,))
        Data = cursor.fetchall()
        for x in Data:
            dataPelajaran.append(x)
        return dataPelajaran

    def UpdateDataJurusan(self, Data):
        respon = {'status': True}
        PasswordNew = ''
        try:
            cursor = mysql.connection.cursor()
            cursor.execute(
                """
            update tb_jurusan set nama=%s,program=%s, bidang=%s where id=%s
            """, ( Data['namaKelas'], Data['program'],
                Data['bidang'],Data['idjurusan']))
            mysql.connection.commit()
            cursor.close()
            respon['status'] = True
        except Exception as e:
            print(e)
            respon['status'] = False
        return respon

class DataKelasX:
    def InsertData(self, Data):
        respon = {'status': True}
        try:
            cursor = mysql.connection.cursor()
            print(Data  )
            cursor.execute(
                """
            insert into tb_kelas (nama,kelas,id_jurusan,id_guru)
            values (%s,%s,%s,%s)
            """, (Data['namaKelas'],Data['kelas'],Data['jurusan'],Data['walikelas']))
            mysql.connection.commit()
            cursor.close()
            respon['status'] = True
        except Exception as e:
            print(e)
            respon['status'] = False
        return respon

class Pengumuman():
    def GetPengumuman(self):
        Pengumuman = []
        cursor = mysql.connection.cursor()
        cursor.execute("""SELECT * FROM tb_pengumuman where id = '1'""")
        Data = cursor.fetchall()
        for x in Data:
            Pengumuman.append(x)
        return Pengumuman

    def UpdatePengumuman(self, data):
        respon = {'status': True}
        PasswordNew = ''
        try:
            cursor = mysql.connection.cursor()
            cursor.execute(
                """
            update tb_pengumuman set pengumuman=%s
            where id = '1'
            """, ( data,))
            mysql.connection.commit()
            cursor.close()
            respon['status'] = True
        except Exception as e:
            print(e)
            respon['status'] = False
        return respon

