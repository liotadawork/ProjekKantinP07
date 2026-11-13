from flask import Flask, render_template, request, jsonify
try:
    import requests
except ImportError:
    requests = None

app = Flask(__name__)

# ====================================================================
# DATA IN-MEMORY (DATABASE SEMENTARA)
# Daftar menu awal kantin kampus
# ====================================================================
menu_kantin = [
    {
        "id": 1,
        "nama": "Nasi Goreng Spesial",
        "harga": 15000,
        "kategori": "Makanan",
        "stok": 20
    },
    {
        "id": 2,
        "nama": "Mie Ayam Bakso",
        "harga": 13000,
        "kategori": "Makanan",
        "stok": 15
    },
    {
        "id": 3,
        "nama": "Es Teh Manis Jumbo",
        "harga": 5000,
        "kategori": "Minuman",
        "stok": 50
    },
    {
        "id": 4,
        "nama": "Kopi Susu Gula Aren",
        "harga": 10000,
        "kategori": "Minuman",
        "stok": 30
    }
]


# ====================================================================
# FUNGSI BANTUAN (HELPER)
# ====================================================================
def cari_menu_by_id(item_id):
    """Mencari dictionary menu berdasarkan ID, return None jika tidak ada."""
    for item in menu_kantin:
        if item["id"] == item_id:
            return item
    return None


# ====================================================================
# ROUTE VIEW: HALAMAN DASHBOARD FRONTEND
# ====================================================================
@app.route('/')
@app.route('/dashboard')
def dashboard():
    return render_template('index.html')


# ====================================================================
# LIVE CODING PRAKTIKUM 07 - LANGKAH 1:
# Buat Endpoint GET /api/menu (Semua Menu) & /api/menu/<int:item_id> (Detail)
# ====================================================================
# TULIS KODE LANGKAH 1 (GET SEMUA & GET BY ID) DI SINI
# ====================================================================
# Sisipkan tepat di bawah: # TULIS KODE LANGKAH 1 (GET) DI SINI

@app.route('/api/menu', methods=['GET'])

def get_all_menu():
    return jsonify({
        "status": "success",
        "total": len(menu_kantin),
        "data": menu_kantin
    }), 200

# Endpoint Ambil Menu Berdasarkan ID

@app.route('/api/menu/<int:item_id>', methods=['GET'])

def get_menu_by_id(item_id):
    item = cari_menu_by_id(item_id)
    if not item:
        return jsonify({"status": "error", "pesan": "Menu tidak ditemukan!"}), 404

    return jsonify({"status": "success", "data": item}), 200

# ====================================================================
# LIVE CODING PRAKTIKUM 07 - LANGKAH 2:
# Buat Endpoint POST /api/menu (Tambah Menu Baru dengan Validasi)
# ====================================================================
# TULIS KODE LANGKAH 2 (POST MENU) DI SINI
# ====================================================================
# Sisipkan tepat di bawah: # TULIS KODE LANGKAH 2 (POST MENU) DI SINI

@app.route('/api/menu', methods=['POST'])

def tambah_menu():
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "pesan": "Body JSON wajib ada!"}), 400

    nama = data.get('nama', '').strip()
    harga = data.get('harga')
    kategori = data.get('kategori', 'Makanan')
    stok = data.get('stok', 0)

    # Validasi field
    if not nama or not isinstance(harga, (int, float)) or harga <= 0:
        return jsonify({"status": "error", "pesan": "Nama wajib diisi & harga > 0!"}), 400

    # Auto-generate ID unik (ID tertinggi + 1)
    new_id = max([i['id'] for i in menu_kantin], default=0) + 1
    menu_baru = {"id": new_id, "nama": nama, "harga": int(harga), "kategori": kategori, "stok": int(stok)}
    menu_kantin.append(menu_baru)

    return jsonify({"status": "success", "pesan": "Menu berhasil ditambahkan!", "data": menu_baru}), 201

# ====================================================================
# LIVE CODING PRAKTIKUM 07 - LANGKAH 3:
# Buat Endpoint PUT /api/menu/<int:item_id> & DELETE /api/menu/<int:item_id>
# ====================================================================
# TULIS KODE LANGKAH 3 (PUT & DELETE) DI SINI
# ====================================================================
# Sisipkan tepat di bawah: # TULIS KODE LANGKAH 3 (PUT & DELETE) DI SINI

@app.route('/api/menu/<int:item_id>', methods=['PUT'])

def update_menu(item_id):
    item = cari_menu_by_id(item_id)
    if not item:
        return jsonify({"status": "error", "pesan": "Menu tidak ditemukan!"}), 404

    data = request.get_json() or {}
    if 'nama' in data: item['nama'] = data['nama']
    if 'harga' in data and data['harga'] > 0: item['harga'] = int(data['harga'])
    if 'stok' in data: item['stok'] = int(data['stok'])

    return jsonify({"status": "success", "pesan": "Menu diperbarui!", "data": item}), 200

# 5. Hapus Menu (DELETE)

@app.route('/api/menu/<int:item_id>', methods=['DELETE'])

def hapus_menu(item_id):
    item = cari_menu_by_id(item_id)
    if not item:
        return jsonify({"status": "error", "pesan": "Menu tidak ditemukan!"}), 404

    menu_kantin.remove(item)
    return jsonify({"status": "success", "pesan": f"Menu '{item['nama']}' dihapus!"}), 200

# ====================================================================
# LIVE CODING PRAKTIKUM 07 - LANGKAH 4:
# Integrasi API Eksternal: GET /api/cuaca-kampus via Open-Meteo
# ====================================================================
# TULIS KODE LANGKAH 4 (EXTERNAL WEATHER API) DI SINI
# ====================================================================
# Sisipkan tepat di bawah: # TULIS KODE LANGKAH 4 (EXTERNAL WEATHER API) DI SINI

@app.route('/api/cuaca-kampus', methods=['GET'])

def get_cuaca_kampus():
    url = "https://api.open-meteo.com/v1/forecast?latitude=-7.8014&longitude=110.3647&current_weather=true&timezone=Asia%2FBangkok"
    try:
        res = requests.get(url, timeout=5)
        res.raise_for_status()
        current = res.json().get('current_weather', {})
        suhu = current.get('temperature', 28.0)

        # Logika bisnis rekomendasi menu
        if suhu >= 30.0:
            saran = "Cuaca terik! Rekomendasi: Es Teh Manis Jumbo!"
        elif suhu <= 25.0:
            saran = "Cuaca sejuk/hujan! Rekomendasi: Mie Ayam Bakso Kuah!"
        else:
            saran = "Cuaca nyaman! Semua menu kantin siap dinikmati."

        return jsonify({"status": "success", "suhu_celcius": suhu, "rekomendasi_menu": saran}), 200
    except requests.RequestException:
        # Graceful fallback jika internet lab offline
        return jsonify({"status": "fallback", "suhu_celcius": 28.5, "rekomendasi_menu": "Es Teh Manis Jumbo selalu aman!"}), 200

if __name__ == '__main__':
    print("🚀 Starter Kit Kantin Kampus REST API siap dijalankan di http://127.0.0.1:5000/")
    app.run(debug=True, port=5000)
