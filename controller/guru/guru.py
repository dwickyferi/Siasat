from flask import Flask, render_template, request, session, url_for, redirect, jsonify, Blueprint
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__)
mysql = MySQL(app)

class ClassGuru():
    def GetDetailGuru(self,id):
        dataGuru = []
        cursor = mysql.connection.cursor()
        cursor.execute("""SELECT * FROM tb_guru where nip = %s""", (id,))
        kelas = cursor.fetchall()
        for x in kelas:
            dataGuru.append(x)
        return dataGuru

    def GetDataListJadwal(self, id_guru):
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
        where tb_jadwal_pelajaran.guru = %s and tb_jadwal_pelajaran.hari = 'Senin'
        order by tb_jadwal_pelajaran.jam_awal asc""", (id_guru,))
        jadwalSenin = cursor.fetchall()
        for x in jadwalSenin:
            senin.append(x)
        cursor.execute("""
        SELECT tb_jadwal_pelajaran.id as id_jadwal, tb_pelajaran.nama as nama ,tb_jadwal_pelajaran.hari as hari, tb_guru.nama as namaGuru, tb_jadwal_pelajaran.jam_awal as jamAwal,
        tb_jadwal_pelajaran.jam_akhir as jamAkhir from tb_jadwal_pelajaran
        inner join tb_guru on tb_jadwal_pelajaran.guru = tb_guru.nip 
        inner join tb_pelajaran on tb_jadwal_pelajaran.pelajaran = tb_pelajaran.id
        where tb_jadwal_pelajaran.guru = %s and tb_jadwal_pelajaran.hari = 'Selasa'
        order by tb_jadwal_pelajaran.jam_awal asc""", (id_guru,))
        jadwalSelasa = cursor.fetchall()
        for x in jadwalSelasa:
            selasa.append(x)
        cursor.execute("""
        SELECT tb_jadwal_pelajaran.id as id_jadwal, tb_pelajaran.nama as nama ,tb_jadwal_pelajaran.hari as hari, tb_guru.nama as namaGuru, tb_jadwal_pelajaran.jam_awal as jamAwal,
        tb_jadwal_pelajaran.jam_akhir as jamAkhir from tb_jadwal_pelajaran
        inner join tb_guru on tb_jadwal_pelajaran.guru = tb_guru.nip 
        inner join tb_pelajaran on tb_jadwal_pelajaran.pelajaran = tb_pelajaran.id
        where tb_jadwal_pelajaran.guru = %s and tb_jadwal_pelajaran.hari = 'Rabu'
        order by tb_jadwal_pelajaran.jam_awal asc""", (id_guru,))
        jadwalRabu = cursor.fetchall()
        for x in jadwalRabu:
            rabu.append(x)
        cursor.execute("""
        SELECT tb_jadwal_pelajaran.id as id_jadwal, tb_pelajaran.nama as nama ,tb_jadwal_pelajaran.hari as hari, tb_guru.nama as namaGuru, tb_jadwal_pelajaran.jam_awal as jamAwal,
        tb_jadwal_pelajaran.jam_akhir as jamAkhir from tb_jadwal_pelajaran
        inner join tb_guru on tb_jadwal_pelajaran.guru = tb_guru.nip 
        inner join tb_pelajaran on tb_jadwal_pelajaran.pelajaran = tb_pelajaran.id
        where tb_jadwal_pelajaran.guru = %s and tb_jadwal_pelajaran.hari = 'Kamis'
        order by tb_jadwal_pelajaran.jam_awal asc""", (id_guru,))
        jadwalKamis = cursor.fetchall()
        for x in jadwalKamis:
            kamis.append(x)
        cursor.execute("""
        SELECT tb_jadwal_pelajaran.id as id_jadwal, tb_pelajaran.nama as nama ,tb_jadwal_pelajaran.hari as hari, tb_guru.nama as namaGuru, tb_jadwal_pelajaran.jam_awal as jamAwal,
        tb_jadwal_pelajaran.jam_akhir as jamAkhir from tb_jadwal_pelajaran
        inner join tb_guru on tb_jadwal_pelajaran.guru = tb_guru.nip 
        inner join tb_pelajaran on tb_jadwal_pelajaran.pelajaran = tb_pelajaran.id
        where tb_jadwal_pelajaran.guru = %s and tb_jadwal_pelajaran.hari = 'Jumat'
        order by tb_jadwal_pelajaran.jam_awal asc""", (id_guru,))
        jadwalJumat = cursor.fetchall()
        for x in jadwalJumat:
            jumat.append(x)
        return senin,selasa,rabu,kamis,jumat