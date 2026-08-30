"""
app_data/hospitals.py
==================
Dataset ILUSTRATIF fasilitas rujukan TBC (rumah sakit) dan dokter spesialis
Paru/Sp.PK untuk keperluan DEMO fitur peta interaktif.

CATATAN: Nama fasilitas & profil dokter di bawah ini adalah CONTOH generik
untuk keperluan pengujian UI, BUKAN data riil. Untuk produksi, sambungkan
ke direktori resmi Kemenkes (data faskes rujukan TBC nasional) atau
database internal rumah sakit mitra, lalu perbarui nomor kontak & lokasi
sesuai sumber terverifikasi.
"""

FACILITIES = [
    {
        "id": "RS001",
        "type": "Rumah Sakit",
        "name": "RSUP Rujukan TBC Nasional (Contoh)",
        "specialist_for": ["negative", "scanty", "positive"],
        "photo": "🏥",
        "bio": "Rumah sakit rujukan tersier dengan fasilitas TCM/GeneXpert dan layanan rawat inap TBC-MDR.",
        "address": "Jl. Kesehatan Raya No. 10, Jakarta Pusat",
        "hours": "24 Jam (IGD) | Poli Paru: Senin-Sabtu 08.00-14.00",
        "phone": "+62215551234",
        "whatsapp": "6281234567890",
        "lat": -6.1864,
        "lon": 106.8317,
    },
    {
        "id": "DOC001",
        "type": "Dokter",
        "name": "dr. Ratna Suminar, Sp.P",
        "specialist_for": ["scanty", "positive"],
        "photo": "👩‍⚕️",
        "bio": "Dokter Spesialis Paru dengan pengalaman 12 tahun dalam penanganan TBC & TBC Resisten Obat.",
        "address": "Klinik Paru Sehat, Jl. Diponegoro No. 5, Jakarta Selatan",
        "hours": "Senin-Jumat 09.00-16.00, Sabtu 09.00-12.00",
        "phone": "+6281111222333",
        "whatsapp": "6281111222333",
        "lat": -6.2297,
        "lon": 106.8253,
    },
    {
        "id": "RS002",
        "type": "Rumah Sakit",
        "name": "RSUD Rujukan Paru Regional (Contoh)",
        "specialist_for": ["negative", "scanty", "positive"],
        "photo": "🏥",
        "bio": "Rumah sakit rujukan regional program penanggulangan TBC dengan layanan DOTS lengkap.",
        "address": "Jl. Merdeka No. 88, Bandung",
        "hours": "24 Jam (IGD) | Poli Paru: Senin-Jumat 07.30-13.00",
        "phone": "+62225557890",
        "whatsapp": "6285678901234",
        "lat": -6.9175,
        "lon": 107.6191,
    },
    {
        "id": "DOC002",
        "type": "Dokter",
        "name": "dr. Bagas Wirawan, Sp.PK",
        "specialist_for": ["scanty", "positive"],
        "photo": "🧑‍⚕️",
        "bio": "Spesialis Patologi Klinik, fokus pada konfirmasi laboratorium & interpretasi hasil mikrobiologi TBC.",
        "address": "Laboratorium Klinik Utama, Jl. Sudirman No. 21, Surabaya",
        "hours": "Senin-Sabtu 08.00-15.00",
        "phone": "+6231555678",
        "whatsapp": "6287890123456",
        "lat": -7.2575,
        "lon": 112.7521,
    },
    {
        "id": "PKM001",
        "type": "Puskesmas",
        "name": "Puskesmas Rujukan TBC Kecamatan (Contoh)",
        "specialist_for": ["negative"],
        "photo": "🏨",
        "bio": "Fasilitas kesehatan tingkat pertama dengan layanan skrining & pengobatan TBC program DOTS.",
        "address": "Jl. Kenanga No. 3, Yogyakarta",
        "hours": "Senin-Sabtu 07.30-14.00",
        "phone": "+62274556677",
        "whatsapp": "6289900112233",
        "lat": -7.7972,
        "lon": 110.3688,
    },
]


def filter_facilities_by_category(category: str):
    """
    Menyaring fasilitas relevan berdasarkan kategori hasil AI
    ('negative' / 'scanty' / 'positive').
    """
    return [f for f in FACILITIES if category in f["specialist_for"]]
