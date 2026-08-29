"""
data/epidemiology.py
=====================
Dataset epidemiologi TBC tingkat provinsi untuk keperluan DEMO dashboard.

CATATAN PENTING (kejujuran data):
Angka-angka pada tabel ini adalah data ILUSTRATIF yang disusun menyerupai
pola publikasi Kemenkes RI (SATUSEHAT/SITB) & WHO Global TB Report agar
dashboard dapat berfungsi penuh saat demo/pitching. Sebelum penggunaan
produksi/komersial, modul `load_epidemiology_data()` ini WAJIB diganti
dengan koneksi ke sumber data resmi (API SATUSEHAT, dataset resmi
data.kemkes.go.id, atau WHO Global TB Report) — lihat TODO di bawah.
"""

import pandas as pd

# TODO(produksi): Ganti fungsi ini dengan pemanggilan API resmi, contoh:
#   df = pd.read_csv("https://data.kemkes.go.id/dataset/tbc/prevalensi.csv")
# atau integrasi SATUSEHAT Platform (FHIR) untuk data real-time per faskes.

_RAW_DATA = [
    # provinsi, lat, lon, prevalensi_per_100k, angka_kesembuhan_persen, kasus_terkonfirmasi, zona
    ("DKI Jakarta", -6.2088, 106.8456, 412, 82.1, 47500, "merah"),
    ("Jawa Barat", -6.9147, 107.6098, 385, 84.5, 96200, "merah"),
    ("Jawa Timur", -7.5361, 112.2384, 356, 85.2, 88900, "merah"),
    ("Jawa Tengah", -7.1500, 110.1403, 298, 86.7, 61200, "kuning"),
    ("Sumatera Utara", 2.1154, 99.5451, 274, 81.9, 40100, "kuning"),
    ("Banten", -6.4058, 106.0640, 331, 80.4, 33200, "merah"),
    ("Sulawesi Selatan", -3.6688, 119.9741, 265, 83.0, 24700, "kuning"),
    ("Papua", -4.2699, 138.0804, 501, 68.3, 15600, "merah"),
    ("Sumatera Selatan", -3.3194, 103.9144, 231, 84.1, 18900, "kuning"),
    ("Bali", -8.4095, 115.1889, 156, 91.2, 6400, "hijau"),
    ("DI Yogyakarta", -7.7956, 110.3695, 143, 92.5, 3100, "hijau"),
    ("Kalimantan Timur", 0.5387, 116.4194, 219, 85.9, 8200, "kuning"),
    ("Nusa Tenggara Timur", -8.6574, 121.0794, 287, 77.5, 9700, "kuning"),
    ("Aceh", 4.6951, 96.7494, 198, 83.3, 8900, "kuning"),
    ("Riau", 0.2933, 101.7068, 176, 85.0, 8100, "hijau"),
]

_COLUMNS = ["provinsi", "lat", "lon", "prevalensi_per_100k", "angka_kesembuhan", "kasus_terkonfirmasi", "zona"]

_TREND_YEARS = [2019, 2020, 2021, 2022, 2023, 2024, 2025]
_TREND_KASUS_NASIONAL = [845000, 824000, 969000, 1060000, 1090000, 1050000, 1005000]
_TREND_KESEMBUHAN = [83.1, 80.4, 79.8, 82.6, 85.0, 86.2, 87.0]


def load_epidemiology_data() -> pd.DataFrame:
    """Mengembalikan DataFrame prevalensi TBC per provinsi (data ilustratif demo)."""
    return pd.DataFrame(_RAW_DATA, columns=_COLUMNS)


def load_national_trend() -> pd.DataFrame:
    """Mengembalikan tren kasus & angka kesembuhan nasional per tahun (data ilustratif demo)."""
    return pd.DataFrame({
        "tahun": _TREND_YEARS,
        "kasus_ternotifikasi": _TREND_KASUS_NASIONAL,
        "angka_kesembuhan_persen": _TREND_KESEMBUHAN,
    })


def national_summary(df: pd.DataFrame) -> dict:
    """Menghitung ringkasan statistik nasional dari DataFrame provinsi."""
    total_kasus = int(df["kasus_terkonfirmasi"].sum())
    avg_kesembuhan = round(float(df["angka_kesembuhan"].mean()), 1)
    zona_merah = int((df["zona"] == "merah").sum())
    prevalensi_tertinggi = df.loc[df["prevalensi_per_100k"].idxmax()]
    return {
        "total_kasus": total_kasus,
        "avg_kesembuhan": avg_kesembuhan,
        "zona_merah_count": zona_merah,
        "provinsi_tertinggi": prevalensi_tertinggi["provinsi"],
        "prevalensi_tertinggi": int(prevalensi_tertinggi["prevalensi_per_100k"]),
    }
