"""
core/inference.py
==================
Wrapper inferensi YOLOv8 + logika interpretasi klinis (skala IUATLD) +
mesin rekomendasi rujukan otomatis berbasis hasil klasifikasi AI.
"""

import streamlit as st
from PIL import Image

try:
    from ultralytics import YOLO
    ULTRALYTICS_AVAILABLE = True
except ImportError:
    ULTRALYTICS_AVAILABLE = False

MODEL_PATH = "best.pt"


@st.cache_resource(show_spinner=False)
def load_model(path: str = MODEL_PATH):
    import os
    if not ULTRALYTICS_AVAILABLE or not os.path.exists(path):
        return None
    return YOLO(path)


def run_inference(model, image: Image.Image):
    """Menjalankan prediksi YOLOv8 dan mengembalikan (annotated_image, count, avg_conf, confidences)."""
    results = model.predict(source=image, conf=0.1, imgsz=640, verbose=False)
    result = results[0]
    boxes = result.boxes
    count = len(boxes) if boxes is not None else 0

    confidences = []
    if boxes is not None and count > 0:
        confidences = [float(c) for c in boxes.conf.tolist()]
    avg_conf = (sum(confidences) / len(confidences) * 100) if confidences else 0.0

    annotated_array = result.plot()
    annotated_image = Image.fromarray(annotated_array[:, :, ::-1])
    return annotated_image, count, avg_conf, confidences


def get_diagnosis_class(count: int):
    """
    Mengembalikan (kategori, css_class, label, deskripsi) berdasarkan skala semi-kuantitatif IUATLD:
      0     -> Negatif
      1-9   -> Scanty
      >9    -> Positif
    """
    if count == 0:
        return (
            "negative", "negative", "NEGATIF (Tidak Ditemukan BTA)",
            "Tidak ditemukan Basil Tahan Asam pada seluruh lapang pandang yang dianalisis oleh sistem AI. "
            "Disarankan pemeriksaan ulang pada 2-3 sampel dahak (Sewaktu-Pagi-Sewaktu) sesuai protokol "
            "untuk konfirmasi klinis lebih lanjut.",
        )
    elif 1 <= count <= 9:
        return (
            "scanty", "scanty", "SCANTY (BTA Positif Rendah / 1-9 per LP)",
            "Ditemukan sejumlah kecil Basil Tahan Asam. Hasil ini termasuk kategori Scanty menurut skala "
            "semi-kuantitatif. Direkomendasikan korelasi dengan gejala klinis dan pemeriksaan penunjang "
            "lanjutan (mis. TCM/GeneXpert) untuk konfirmasi diagnosis.",
        )
    else:
        return (
            "positive", "positive", "POSITIF (BTA Ditemukan > 9 per Lapang Pandang)",
            "Ditemukan jumlah Basil Tahan Asam yang signifikan, mengindikasikan kemungkinan tinggi infeksi "
            "aktif Mycobacterium tuberculosis. Segera rujuk pasien untuk evaluasi klinis lanjutan oleh "
            "Dokter Spesialis Paru / Sp.PK dan pertimbangkan inisiasi tata laksana sesuai pedoman nasional TBC.",
        )


# =============================================================================
# MESIN REKOMENDASI RUJUKAN OTOMATIS
# =============================================================================
REFERRAL_RULES = {
    "negative": {
        "urgency": "Rutin",
        "urgency_color": "hijau",
        "specialist_filter": "Puskesmas / Dokter Umum",
        "action_title": "Observasi & Pemeriksaan Ulang",
        "actions": [
            "Ulangi pengambilan sampel dahak (metode SPS) bila gejala klinis TBC tetap ada.",
            "Konsultasi ke Puskesmas terdekat untuk evaluasi gejala penyerta.",
            "Tidak diperlukan rujukan spesialistik segera pada tahap ini.",
        ],
    },
    "scanty": {
        "urgency": "Prioritas Sedang",
        "urgency_color": "kuning",
        "specialist_filter": "Dokter Sp.PK / Puskesmas Rujukan TBC",
        "action_title": "Konfirmasi Laboratorium Lanjutan",
        "actions": [
            "Rujuk ke fasilitas dengan pemeriksaan TCM/GeneXpert untuk konfirmasi.",
            "Jadwalkan kontrol ulang dalam 3-7 hari.",
            "Edukasi pasien mengenai etika batuk & pencegahan penularan sambil menunggu hasil konfirmasi.",
        ],
    },
    "positive": {
        "urgency": "Segera / Urgent",
        "urgency_color": "merah",
        "specialist_filter": "Rumah Sakit Rujukan TBC / Dokter Sp.P",
        "action_title": "Rujukan Spesialistik Segera",
        "actions": [
            "Rujuk SEGERA ke Rumah Sakit Rujukan TBC terdekat atau Dokter Spesialis Paru (Sp.P).",
            "Inisiasi Program Penanggulangan TBC Nasional (OAT Kategori 1) sesuai indikasi dokter.",
            "Lakukan pelacakan kontak erat (contact tracing) di lingkungan rumah/kerja pasien.",
            "Terapkan isolasi respiratorik mandiri sementara hingga evaluasi dokter.",
        ],
    },
}


def get_referral_recommendation(category: str) -> dict:
    """Mengembalikan aturan rujukan berdasarkan kategori hasil AI ('negative'/'scanty'/'positive')."""
    return REFERRAL_RULES.get(category, REFERRAL_RULES["negative"])
