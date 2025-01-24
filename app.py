from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

class Tugas:
    def __init__(self, deskripsi, prioritas):
        self.deskripsi = deskripsi
        self.prioritas = prioritas  # Menyimpan status prioritas sebagai boolean
        self.selesai = False

# Daftar untuk menyimpan tugas
tugas_list = []

@app.route('/')
def index():
    # Mengurutkan tugas berdasarkan prioritas (tugas prioritas di atas)
    tugas_list_sorted = sorted(tugas_list, key=lambda x: x.prioritas, reverse=True)
    return render_template('index.html', tugas=tugas_list_sorted)

@app.route('/tambah', methods=['POST'])
def tambah_tugas():
    deskripsi = request.form.get('deskripsi')
    prioritas = 'prioritas' in request.form  # Menggunakan checkbox untuk prioritas
    
    if deskripsi:
        tugas = Tugas(deskripsi, prioritas)
        tugas_list.append(tugas)
    return redirect(url_for('index'))

@app.route('/hapus/<int:tugas_id>')
def hapus_tugas(tugas_id):
    if 0 <= tugas_id < len(tugas_list):
        del tugas_list[tugas_id]
    return redirect(url_for('index'))

@app.route('/edit/<int:tugas_id>', methods=['GET', 'POST'])
def edit_tugas(tugas_id):
    if request.method == 'POST':
        deskripsi = request.form.get('deskripsi')
        prioritas = 'prioritas' in request.form  # Menggunakan checkbox untuk prioritas
        if 0 <= tugas_id < len(tugas_list):
            tugas_list[tugas_id].deskripsi = deskripsi
            tugas_list[tugas_id].prioritas = prioritas
        return redirect(url_for('index'))
    
    tugas = tugas_list[tugas_id]
    return render_template('edit.html', tugas=tugas, tugas_id=tugas_id)

@app.route('/tandai/<int:tugas_id>')
def tandai_tugas(tugas_id):
    if 0 <= tugas_id < len(tugas_list):
        tugas_list[tugas_id].selesai = not tugas_list[tugas_id].selesai
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)