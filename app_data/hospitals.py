"""
app_data/hospitals.py
======================
Direktori fasilitas rujukan TBC & spesialis paru untuk fitur peta interaktif.

SUMBER DATA: Nama, alamat, koordinat, dan nomor telepon berikut diambil dari
data tempat publik (Google Places) per kota-kota besar Indonesia — bukan data
karangan. Nomor telepon yang ditampilkan adalah nomor RESMI institusi
(customer service/pendaftaran rumah sakit), BUKAN nomor pribadi dokter,
karena nomor pribadi tenaga medis tidak dipublikasikan secara resmi dan
tidak etis untuk dicantumkan tanpa persetujuan langsung.

CATATAN PENTING UNTUK PRODUKSI/KOMERSIALISASI:
- Tombol "WhatsApp" SENGAJA tidak disediakan di sini karena tidak ada nomor
  WhatsApp resmi rujukan TBC yang terverifikasi publik untuk sebagian besar
  fasilitas ini. Menambahkan nomor WA tanpa verifikasi berisiko menyesatkan
  pasien. Tombol yang tersedia hanya "Telepon" ke nomor resmi institusi.
- Sebelum go-live, sebaiknya data ini diverifikasi ulang / diperbarui secara
  berkala (nomor telepon & jam operasional bisa berubah), idealnya lewat
  kerja sama resmi dengan pihak rumah sakit atau dinas kesehatan setempat.
- "specialist_for" adalah pengelompokan bantu (bukan jaminan resmi bahwa
  fasilitas tsb punya program TBC aktif) — dibuat berdasarkan jenis fasilitas
  (RS Paru/RS Rujukan besar vs Puskesmas/klinik umum). Rujukan medis final
  tetap harus lewat keputusan dokter penanggung jawab pasien.
"""

FACILITIES = [
    # ------------------------- JAKARTA -------------------------
    {
        "id": "JKT001",
        "type": "Rumah Sakit",
        "name": "RSUD Tarakan Jakarta",
        "specialist_for": ["negative", "scanty", "positive"],
        "photo": "🏥",
        "bio": "Rumah sakit umum daerah dengan layanan rawat inap 24 jam dan poli spesialis lengkap.",
        "address": "Jl. Kyai Caringin No.7, Cideng, Kec. Gambir, Jakarta Pusat",
        "hours": "24 Jam",
        "phone": "+622150900303",
        "lat": -6.1717069,
        "lon": 106.8102737,
    },
    {
        "id": "JKT002",
        "type": "Rumah Sakit",
        "name": "Siloam Hospitals TB Simatupang",
        "specialist_for": ["scanty", "positive"],
        "photo": "🏥",
        "bio": "Rumah sakit swasta dengan layanan spesialis penyakit dalam & paru, buka 24 jam.",
        "address": "Jl. R.A. Kartini No.8, Cilandak Barat, Jakarta Selatan",
        "hours": "24 Jam",
        "phone": "+62211500911",
        "lat": -6.2926338,
        "lon": 106.7842909,
    },
    {
        "id": "JKT003",
        "type": "Klinik",
        "name": "Klinik JRC - PPTI (Perhimpunan Pemberantasan Tuberkulosis Indonesia)",
        "specialist_for": ["scanty", "positive"],
        "photo": "🩺",
        "bio": "Klinik yang berfokus pada diagnosis & pengobatan TBC, termasuk layanan tes cepat (TCM) untuk TB/TB-RO.",
        "address": "Jl. Sultan Iskandar Muda No.66A, Kebayoran Lama Utara, Jakarta Selatan",
        "hours": "Senin–Sabtu 08.00–20.00, Minggu tutup",
        "phone": "+6287784172731",
        "lat": -6.240267,
        "lon": 106.783423,
    },
    # ------------------------- SURABAYA -------------------------
    {
        "id": "SBY001",
        "type": "Rumah Sakit",
        "name": "RSUD Husada Prima Surabaya",
        "specialist_for": ["negative", "scanty", "positive"],
        "photo": "🏥",
        "bio": "Rumah sakit umum daerah dengan layanan rawat inap 24 jam.",
        "address": "Jl. Karang Tembok No.39, Pegirian, Kec. Semampir, Surabaya",
        "hours": "24 Jam",
        "phone": "+62313713836",
        "lat": -7.2241491,
        "lon": 112.7465067,
    },
    {
        "id": "SBY002",
        "type": "Rumah Sakit",
        "name": "RS Royal Surabaya",
        "specialist_for": ["scanty", "positive"],
        "photo": "🏥",
        "bio": "Rumah sakit swasta dengan layanan emergensi dan spesialis penyakit dalam/paru.",
        "address": "Jl. Rungkut Industri I No.1, Kendangsari, Surabaya",
        "hours": "24 Jam",
        "phone": "+62318476111",
        "lat": -7.3289542,
        "lon": 112.7508810,
    },
    # ------------------------- BANDUNG -------------------------
    {
        "id": "BDG001",
        "type": "Rumah Sakit",
        "name": "RS Paru Dr. H. A. Rotinsulu",
        "specialist_for": ["negative", "scanty", "positive"],
        "photo": "🏥",
        "bio": "Rumah sakit khusus paru dengan fasilitas lengkap untuk penanganan penyakit paru termasuk TBC.",
        "address": "Jl. Bukit Jarian No.40, Hegarmanah, Kec. Cidadap, Kota Bandung",
        "hours": "24 Jam",
        "phone": "+62222034446",
        "lat": -6.877792,
        "lon": 107.606201,
    },
    # ------------------------- MEDAN -------------------------
    {
        "id": "MDN001",
        "type": "Rumah Sakit",
        "name": "RSU Mitra Sejati Medan",
        "specialist_for": ["negative", "scanty", "positive"],
        "photo": "🏥",
        "bio": "Rumah sakit umum dengan layanan rawat inap 24 jam dan berbagai poli spesialis.",
        "address": "Jl. Jenderal Besar A.H. Nasution No.7, Pangkalan Masyhur, Medan Johor",
        "hours": "24 Jam",
        "phone": "+62617875967",
        "lat": 3.5409601,
        "lon": 98.6798975,
    },
    {
        "id": "MDN002",
        "type": "Rumah Sakit",
        "name": "RSU Haji Medan",
        "specialist_for": ["negative", "scanty", "positive"],
        "photo": "🏥",
        "bio": "Rumah sakit umum daerah dengan layanan rawat inap 24 jam.",
        "address": "Jl. Rumah Sakit H. No.47, Kenangan Baru, Percut Sei Tuan, Deli Serdang",
        "hours": "24 Jam",
        "phone": "+62616619520",
        "lat": 3.61338,
        "lon": 98.7145484,
    },
    # ------------------------- SEMARANG -------------------------
    {
        "id": "SMG001",
        "type": "Rumah Sakit",
        "name": "Balai Kesehatan Paru Masyarakat Semarang",
        "specialist_for": ["negative", "scanty", "positive"],
        "photo": "🏥",
        "bio": "Fasilitas kesehatan yang berfokus pada layanan penyakit paru masyarakat, termasuk program TBC.",
        "address": "Jl. Kh Ahmad Dahlan No.35, Karangkidul, Kec. Semarang Tengah, Semarang",
        "hours": "Hubungi fasilitas untuk jam operasional terkini",
        "phone": None,
        "lat": -6.9879999,
        "lon": 110.4272956,
    },
    {
        "id": "SMG002",
        "type": "Puskesmas",
        "name": "Pusat Kesehatan Masyarakat Regional Semarang",
        "specialist_for": ["negative"],
        "photo": "🏨",
        "bio": "Fasilitas kesehatan tingkat pertama yang melayani skrining & rujukan awal, termasuk program vaksinasi dan kesehatan masyarakat.",
        "address": "Jl. Kh Ahmad Dahlan No.39, Karangkidul, Kec. Semarang Tengah, Semarang",
        "hours": "Senin–Kamis 07.00–11.00, Jumat 07.00–10.00, Sabtu 07.00–10.30, Minggu tutup",
        "phone": "+62248316758",
        "lat": -6.9877627,
        "lon": 110.4275581,
    },
    # ------------------------- YOGYAKARTA -------------------------
    {
        "id": "YGY001",
        "type": "Rumah Sakit",
        "name": "RS Bethesda Lempuyangwangi Yogyakarta",
        "specialist_for": ["negative", "scanty", "positive"],
        "photo": "🏥",
        "bio": "Rumah sakit umum dengan layanan rawat inap 24 jam dan poli spesialis.",
        "address": "Jl. Hayam Wuruk No.6, Bausasran, Kec. Danurejan, Yogyakarta",
        "hours": "24 Jam",
        "phone": "+62274512257",
        "lat": -7.796848,
        "lon": 110.373175,
    },
    # ------------------------- MAKASSAR -------------------------
    {
        "id": "MKS001",
        "type": "Rumah Sakit",
        "name": "Balai Besar Kesehatan Paru Masyarakat Makassar",
        "specialist_for": ["negative", "scanty", "positive"],
        "photo": "🏥",
        "bio": "Fasilitas kesehatan paru masyarakat yang menangani skrining & pengobatan penyakit paru termasuk TBC.",
        "address": "Jl. A. P. Pettarani No.43, Masale, Kec. Panakkukang, Makassar",
        "hours": "Senin–Jumat 08.00–16.00, Sabtu–Minggu tutup",
        "phone": "+62411441497",
        "lat": -5.1498246,
        "lon": 119.4383775,
    },
    # ------------------------- DENPASAR / BALI -------------------------
    {
        "id": "DPS001",
        "type": "Rumah Sakit",
        "name": "RSU Bhakti Rahayu Denpasar",
        "specialist_for": ["negative", "scanty", "positive"],
        "photo": "🏥",
        "bio": "Rumah sakit umum dengan layanan rawat inap 24 jam.",
        "address": "Jl. Gatot Subroto II No.11, Dangin Puri Kaja, Denpasar Utara",
        "hours": "24 Jam",
        "phone": "+62361430270",
        "lat": -8.6370905,
        "lon": 115.2209371,
    },
    # ------------------------- PALEMBANG -------------------------
    {
        "id": "PLB001",
        "type": "Rumah Sakit",
        "name": "Rumah Sakit Khusus Paru Palembang",
        "specialist_for": ["negative", "scanty", "positive"],
        "photo": "🏥",
        "bio": "Rumah sakit khusus penyakit paru, melayani pasien BPJS maupun umum dengan IGD 24 jam.",
        "address": "Jl. Merdeka No.10, Talang Semut, Kec. Bukit Kecil, Palembang",
        "hours": "24 Jam (IGD)",
        "phone": "+62711352010",
        "lat": -2.9902166,
        "lon": 104.750498,
    },
    # ------------------------- MALANG -------------------------
    {
        "id": "MLG001",
        "type": "Klinik",
        "name": "Klinik Respirasi dr. Koentjahja, Sp.P",
        "specialist_for": ["scanty", "positive"],
        "photo": "🩺",
        "bio": "Klinik spesialis paru (pulmonologi) yang melayani konsultasi penyakit pernapasan termasuk asma, bronkitis, dan gangguan paru lainnya.",
        "address": "Jl. Wilis Indah No.A-6B, Gading Kasri, Kec. Klojen, Malang",
        "hours": "Senin, Rabu, Jumat 09.00–10.00 & 16.00–20.00; Selasa, Kamis 09.00–10.00 & 16.00–18.00; Sabtu 09.00–10.00; Minggu tutup",
        "phone": "+62818568711",
        "lat": -7.9713268,
        "lon": 112.6191798,
    },
]


def filter_facilities_by_category(category: str):
    """
    Menyaring fasilitas relevan berdasarkan kategori hasil AI
    ('negative' / 'scanty' / 'positive').
    """
    return [f for f in FACILITIES if category in f["specialist_for"]]
