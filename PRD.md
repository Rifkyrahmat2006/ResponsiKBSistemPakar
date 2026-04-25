# PRD: S-DIAG-HAMA (Expert System)

## 1. Ringkasan Produk
Sistem pakar berbasis web untuk membantu petani atau penyuluh lapangan mendiagnosis hama dan penyakit tanaman padi secara cepat berdasarkan gejala fisik yang teramati.

## 2. Target Pengguna
* Petani mandiri.
* Penyuluh Pertanian Lapangan (PPL).
* Mahasiswa Pertanian/Informatika (sebagai referensi).

## 3. Fitur Utama (MVP)
1.  **Konsultasi Interaktif:** Form dinamis berisi pertanyaan "Ya/Tidak" mengenai gejala (daun menguning, batang busuk, adanya bercak brown spot, dll).
2.  **Inference Engine:** Logika **Forward Chaining** untuk mencocokkan gejala dengan basis pengetahuan (*knowledge base*).
3.  **Diagnosis & Solusi:** Menampilkan nama penyakit/hama, tingkat keyakinan, dan langkah penanganan (organik/kimia).
4.  **Dashboard Admin Sederhana:** Untuk menambah atau mengubah aturan (*rules*) diagnosa tanpa menyentuh kode program.

## 4. Struktur Data (Knowledge Base)
Kamu bisa menggunakan struktur JSON sederhana untuk menyimpan aturan:
```json
{
  "penyakit": "Wereng Coklat",
  "gejala": ["daun_kuning", "batang_kering", "tanaman_kerdil"],
  "solusi": "Gunakan pestisida organik ekstrak daun mimba atau agens hayati Beauveria bassiana."
}
```

---

# Arsitektur Teknis & Implementasi

### 1. Stack Teknologi
* **Backend:** Python (Flask).
* **Frontend:** HTML5, Tailwind CSS (agar tampilan modern dan responsif di HP petani).
* **Deployment:** Vercel.

### 2. Struktur Folder
```text
s-diag-hama/
├── api/
│   └── index.py      # Entry point utama untuk Flask di Vercel
├── templates/
│   └── index.html    # Tampilan form konsultasi
├── static/           # CSS/JS
├── data/
│   └── rules.json    # Basis pengetahuan pakar
├── vercel.json       # Konfigurasi deployment Vercel
└── requirements.txt
```

### 3. Contoh Kode Logika (Flask)
Di `api/index.py`, kamu bisa membuat fungsi sederhana untuk mencocokkan input user:

```python
from flask import Flask, render_template, request

app = Flask(__name__)

# Contoh Knowledge Base sederhana
knowledge_base = [
    {
        "id": "P01",
        "nama": "Penyakit Blas (Pyricularia oryzae)",
        "gejala": ["bercak_belah_ketupat", "ujung_daun_kering"],
        "solusi": "Kurangi pupuk Nitrogen, gunakan fungisida berbahan aktif trisiklazol."
    }
]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_gejala = request.form.getlist('gejala')
        # Logika Forward Chaining sederhana
        hasil = []
        for rule in knowledge_base:
            if set(rule['gejala']).issubset(set(user_gejala)):
                hasil.append(rule)
        return render_template('result.html', hasil=hasil)
    return render_template('index.html')

# Penting untuk Vercel
app = app
```

---

# Panduan Deployment ke Vercel

Agar Flask bisa berjalan di Vercel, kamu butuh file `vercel.json`:

```json
{
  "rewrites": [
    { "source": "/(.*)", "destination": "/api/index.py" }
  ]
}
```

**Langkah-langkah:**
1.  Buat repository di GitHub.
2.  Push kode kamu ke sana.
3.  Buka [Vercel](https://vercel.com/), hubungkan dengan GitHub.
4.  Pilih folder proyekmu, Vercel akan otomatis mendeteksi Flask dan melakukan build.

### Tips Tambahan:
Karena kamu suka **bahasa Indonesia** tapi tidak ingin semuanya diterjemahkan, gunakan istilah teknis seperti *Inference Engine*, *Forward Chaining*, dan *Deployment* tetap dalam bahasa Inggris di dokumentasimu, sementara interface webnya menggunakan bahasa Indonesia yang ramah petani.

Apakah kamu ingin saya buatkan draf kode HTML (Frontend) dengan Tailwind agar tampilannya langsung terlihat profesional?