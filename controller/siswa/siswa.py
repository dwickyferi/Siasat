from flask import Flask, render_template, request, session, url_for, redirect, jsonify, Blueprint
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__)
mysql = MySQL(app)

class ClassSiswa():
    def GetDetailSiswa(self, nis):
        dataSiswa = []
        cursor = mysql.connection.cursor()
        cursor.execute("""SELECT tb_siswa.nis as nis, tb_siswa.nama as nama, tb_kelas.nama as kelas FROM tb_siswa 
        inner join tb_kelas_siswa on tb_siswa.nis = tb_kelas_siswa.id_siswa
        inner join tb_kelas on tb_kelas_siswa.id_kelas = tb_kelas.id
        where nis = %s""", (nis,))
        kelas = cursor.fetchall()
        for x in kelas:
            dataSiswa.append(x)
        return dataSiswa

    def GetDataListJadwal(self, id_siswa):
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
        inner join tb_kelas_siswa on tb_jadwal_pelajaran.kelas = tb_kelas_siswa.id_kelas
        where tb_kelas_siswa.id_siswa = %s and tb_jadwal_pelajaran.hari = 'Senin'
        order by tb_jadwal_pelajaran.jam_awal asc""", (id_siswa,))
        jadwalSenin = cursor.fetchall()
        for x in jadwalSenin:
            senin.append(x)
        cursor.execute("""
        SELECT tb_jadwal_pelajaran.id as id_jadwal, tb_pelajaran.nama as nama ,tb_jadwal_pelajaran.hari as hari, tb_guru.nama as namaGuru, tb_jadwal_pelajaran.jam_awal as jamAwal,
        tb_jadwal_pelajaran.jam_akhir as jamAkhir from tb_jadwal_pelajaran
        inner join tb_guru on tb_jadwal_pelajaran.guru = tb_guru.nip 
        inner join tb_pelajaran on tb_jadwal_pelajaran.pelajaran = tb_pelajaran.id
        inner join tb_kelas_siswa on tb_jadwal_pelajaran.kelas = tb_kelas_siswa.id_kelas
        where tb_kelas_siswa.id_siswa = %s and tb_jadwal_pelajaran.hari = 'Selasa'
        order by tb_jadwal_pelajaran.jam_awal asc""", (id_siswa,))
        jadwalSelasa = cursor.fetchall()
        for x in jadwalSelasa:
            selasa.append(x)
        cursor.execute("""
        SELECT tb_jadwal_pelajaran.id as id_jadwal, tb_pelajaran.nama as nama ,tb_jadwal_pelajaran.hari as hari, tb_guru.nama as namaGuru, tb_jadwal_pelajaran.jam_awal as jamAwal,
        tb_jadwal_pelajaran.jam_akhir as jamAkhir from tb_jadwal_pelajaran
        inner join tb_guru on tb_jadwal_pelajaran.guru = tb_guru.nip 
        inner join tb_pelajaran on tb_jadwal_pelajaran.pelajaran = tb_pelajaran.id
        inner join tb_kelas_siswa on tb_jadwal_pelajaran.kelas = tb_kelas_siswa.id_kelas
        where tb_kelas_siswa.id_siswa = %s and tb_jadwal_pelajaran.hari = 'Rabu'
        order by tb_jadwal_pelajaran.jam_awal asc""", (id_siswa,))
        jadwalRabu = cursor.fetchall()
        for x in jadwalRabu:
            rabu.append(x)
        cursor.execute("""
        SELECT tb_jadwal_pelajaran.id as id_jadwal, tb_pelajaran.nama as nama ,tb_jadwal_pelajaran.hari as hari, tb_guru.nama as namaGuru, tb_jadwal_pelajaran.jam_awal as jamAwal,
        tb_jadwal_pelajaran.jam_akhir as jamAkhir from tb_jadwal_pelajaran
        inner join tb_guru on tb_jadwal_pelajaran.guru = tb_guru.nip 
        inner join tb_pelajaran on tb_jadwal_pelajaran.pelajaran = tb_pelajaran.id
        inner join tb_kelas_siswa on tb_jadwal_pelajaran.kelas = tb_kelas_siswa.id_kelas
        where tb_kelas_siswa.id_siswa = %s and tb_jadwal_pelajaran.hari = 'Kamis'
        order by tb_jadwal_pelajaran.jam_awal asc""", (id_siswa,))
        jadwalKamis = cursor.fetchall()
        for x in jadwalKamis:
            kamis.append(x)
        cursor.execute("""
        SELECT tb_jadwal_pelajaran.id as id_jadwal, tb_pelajaran.nama as nama ,tb_jadwal_pelajaran.hari as hari, tb_guru.nama as namaGuru, tb_jadwal_pelajaran.jam_awal as jamAwal,
        tb_jadwal_pelajaran.jam_akhir as jamAkhir from tb_jadwal_pelajaran
        inner join tb_guru on tb_jadwal_pelajaran.guru = tb_guru.nip 
        inner join tb_pelajaran on tb_jadwal_pelajaran.pelajaran = tb_pelajaran.id
        inner join tb_kelas_siswa on tb_jadwal_pelajaran.kelas = tb_kelas_siswa.id_kelas
        where tb_kelas_siswa.id_siswa = %s and tb_jadwal_pelajaran.hari = 'Jumat'
        order by tb_jadwal_pelajaran.jam_awal asc""", (id_siswa,))
        jadwalJumat = cursor.fetchall()
        for x in jadwalJumat:
            jumat.append(x)
        return senin,selasa,rabu,kamis,jumat

    def NilaiSiswa(self, nis):
        dataKelas = []
        data = []
        cursor = mysql.connection.cursor()
        cursor.execute("""SELECT tb_pelajaran.nama as nama, tb_nilai.uts as uts, tb_nilai.uas as uas, tb_nilai.id_nilai as iddata from tb_nilai
        inner join tb_siswa on tb_nilai.id_siswa = tb_siswa.nis
        inner join tb_pelajaran on tb_nilai.id_pelajaran = tb_pelajaran.id
        where tb_nilai.id_siswa = %s""", (nis,))
        nilai = cursor.fetchall()
        for x in nilai:
            dataKelas.append(x)
        return dataKelas

    def TranskipSiswa(self, nis):
        dataKelas = []
        data = []
        cursor = mysql.connection.cursor()
        cursor.execute("""SELECT tb_pelajaran.nama as nama, tb_transkip_nilai.uts as uts, tb_transkip_nilai.uas as uas, tb_transkip_nilai.id_transkip as iddata from tb_transkip_nilai
        inner join tb_siswa on tb_transkip_nilai.id_siswa = tb_siswa.nis
        inner join tb_pelajaran on tb_transkip_nilai.id_pelajaran = tb_pelajaran.id
        where tb_transkip_nilai.id_siswa = %s""", (nis,))
        nilai = cursor.fetchall()
        for x in nilai:
            dataKelas.append(x)
        return dataKelas