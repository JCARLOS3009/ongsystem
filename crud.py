from flask import Flask, Blueprint, render_template, url_for, request, redirect
import sqlite3

app_crud = Blueprint('app_crud',__name__)

@app_crud.route("/")
def index():
    return render_template('index.html')

# Route untuk halaman utama / tampil data
@app_crud.route('/view')
def view():
    koneksi = sqlite3.connect('dapodik.db')
    buka_koneksi = koneksi.cursor()
    buka_koneksi.execute('select * from siswa order by field2 asc')
    data = buka_koneksi.fetchall()
    buka_koneksi.close()
    koneksi.close()
    keterangan = "View Data From SQLite"
    return render_template('viewdata.html',data=data)

# Route untuk halaman penghapusan data
@app_crud.route('/delete/<int:nis>', methods=['GET', 'POST'])
def delete(nis):
    nis_siswa = nis
    # Koneksi ke database
    koneksi = sqlite3.connect('dapodik.db')
    buka_koneksi = koneksi.cursor()
    # Hapus data berdasarkan nis
    buka_koneksi.execute('DELETE FROM siswa WHERE field1=?', (nis_siswa,))
    koneksi.commit()
    # Tutup koneksi database
    buka_koneksi.close()
    koneksi.close()
    # Redirect ke halaman utama
    return redirect(url_for('app_crud.view'))

# Route untuk halaman edit data
@app_crud.route('/edit/<int:nis>', methods=['GET', 'POST'])
def edit(nis):
    nis_siswa = nis
    koneksi = sqlite3.connect('dapodik.db')
    buka_koneksi = koneksi.cursor()
    buka_koneksi.execute('select * from siswa WHERE field1=?', (nis_siswa,))
    data = buka_koneksi.fetchone()
    buka_koneksi.close()
    koneksi.close()
    return render_template('editdata.html',data=data)

# Route untuk halaman update data
@app_crud.route('/update/<int:nis>', methods=['GET', 'POST'])
def update(nis):
    nis_siswa = nis
    nama = request.form['nama']
    kelas = request.form['kelas']
    koneksi = sqlite3.connect('dapodik.db')
    buka_koneksi = koneksi.cursor()
    buka_koneksi.execute('UPDATE siswa SET field2=?, field3=? WHERE field1=?', (nama, kelas,nis_siswa))
    koneksi.commit()
    buka_koneksi.close()
    koneksi.close()
    return redirect(url_for('app_crud.view'))