"""
S-DIAG-HAMA — Sistem Pakar Diagnosis Hama & Penyakit Tanaman Padi
Backend Flask dengan Inference Engine Forward Chaining
"""

from flask import Flask, render_template, request, jsonify
import json
import os

# --- Konfigurasi Path ---
basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app = Flask(
    __name__,
    template_folder=os.path.join(basedir, 'templates'),
    static_folder=os.path.join(basedir, 'static')
)

# --- Load Knowledge Base ---
def load_knowledge_base():
    """Memuat knowledge base dari file JSON."""
    rules_path = os.path.join(basedir, 'data', 'rules.json')
    with open(rules_path, 'r', encoding='utf-8') as f:
        return json.load(f)

kb = load_knowledge_base()


# --- Inference Engine: Forward Chaining ---
def forward_chaining(user_gejala):
    """
    Mencocokkan gejala yang dipilih user dengan knowledge base.
    Menghitung tingkat keyakinan (confidence) berdasarkan persentase gejala yang cocok.
    Mengembalikan hasil terurut dari keyakinan tertinggi.
    """
    if not user_gejala:
        return []

    results = []
    for rule in kb['rules']:
        rule_gejala = set(rule['gejala'])
        user_set = set(user_gejala)

        # Gejala yang cocok
        matched = rule_gejala.intersection(user_set)

        if len(matched) == 0:
            continue

        # Hitung confidence: berapa persen gejala rule yang cocok
        confidence = round(len(matched) / len(rule_gejala) * 100, 1)

        # Hanya tampilkan jika confidence >= 40%
        if confidence >= 40:
            results.append({
                'rule': rule,
                'confidence': confidence,
                'matched_gejala': list(matched),
                'total_gejala': len(rule_gejala),
                'matched_count': len(matched)
            })

    # Urutkan berdasarkan confidence tertinggi
    return sorted(results, key=lambda x: x['confidence'], reverse=True)


def get_gejala_label(gejala_id):
    """Mendapatkan label gejala dari ID."""
    for kategori in kb['gejala_kategori'].values():
        for item in kategori['daftar']:
            if item['id'] == gejala_id:
                return item['label']
    return gejala_id


# --- Routes ---

@app.route('/')
def index():
    """Halaman utama — Form konsultasi."""
    return render_template(
        'index.html',
        gejala_kategori=kb['gejala_kategori']
    )


@app.route('/diagnosa', methods=['POST'])
def diagnosa():
    """Proses diagnosis dengan Forward Chaining."""
    user_gejala = request.form.getlist('gejala')
    hasil = forward_chaining(user_gejala)

    # Siapkan label gejala untuk ditampilkan
    gejala_labels = {}
    for gejala_id in user_gejala:
        gejala_labels[gejala_id] = get_gejala_label(gejala_id)

    return render_template(
        'result.html',
        hasil=hasil,
        user_gejala=user_gejala,
        gejala_labels=gejala_labels,
        total_dipilih=len(user_gejala)
    )


@app.route('/admin')
def admin():
    """Dashboard admin — Lihat knowledge base."""
    total_penyakit = len([r for r in kb['rules'] if r['kategori'] == 'penyakit'])
    total_hama = len([r for r in kb['rules'] if r['kategori'] == 'hama'])

    all_gejala = set()
    for rule in kb['rules']:
        all_gejala.update(rule['gejala'])

    stats = {
        'total_rules': len(kb['rules']),
        'total_penyakit': total_penyakit,
        'total_hama': total_hama,
        'total_gejala': len(all_gejala)
    }

    return render_template(
        'admin.html',
        rules=kb['rules'],
        gejala_kategori=kb['gejala_kategori'],
        stats=stats,
        get_gejala_label=get_gejala_label
    )


@app.route('/api/rules')
def api_rules():
    """API endpoint — Semua rules dalam format JSON."""
    return jsonify(kb['rules'])


@app.route('/api/gejala')
def api_gejala():
    """API endpoint — Semua gejala dalam format JSON."""
    return jsonify(kb['gejala_kategori'])
