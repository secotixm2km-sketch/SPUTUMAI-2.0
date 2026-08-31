"""
core/pdf_report.py
===================
Generator laporan medis PDF (FPDF2). Gambar dituliskan lewat
tempfile.NamedTemporaryFile lalu file handle DITUTUP sebelum dibaca oleh
pdf.image(), dan file temporary dihapus (os.remove) setelahnya untuk
mencegah "FPDF error: Missing or incorrect image file".

Privasi: laporan mencantumkan Anonymous Patient ID (APID) hasil hashing,
bukan Nomor Rekam Medis asli, sesuai modul core.security.
"""

import os
import tempfile
from datetime import datetime

from fpdf import FPDF
from PIL import Image

from core.inference import get_diagnosis_class, get_referral_recommendation
from core.security import anonymize_id, mask_identifier

_COLOR_MAP = {
    "negative": (34, 197, 94),
    "scanty": (245, 158, 11),
    "positive": (239, 68, 68),
}


def generate_pdf_report(patient_info: dict, result_image: Image.Image, count: int, avg_conf: float) -> bytes:
    category, css_class, label, description = get_diagnosis_class(count)
    referral = get_referral_recommendation(category)
    apid = anonymize_id(patient_info.get("rm_number", ""))
    masked_rm = mask_identifier(patient_info.get("rm_number", ""))

    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # ---------- Header Klinik ----------
    pdf.set_fill_color(15, 23, 42)
    pdf.rect(0, 0, 210, 28, style="F")
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 17)
    pdf.set_xy(10, 7)
    pdf.cell(0, 8, "SputumAI Workspace", ln=1)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_x(10)
    pdf.cell(0, 6, "Laporan Hasil Pemeriksaan BTA Berbasis Kecerdasan Buatan (YOLOv8)", ln=1)
    pdf.set_text_color(30, 41, 59)
    pdf.ln(14)

    # ---------- Data Pasien (Anonim) ----------
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Data Pasien & Pemeriksaan (Anonim)", ln=1)
    pdf.set_draw_color(226, 232, 240)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(3)

    pdf.set_font("Helvetica", "", 10.5)
    exam_time = datetime.now().strftime("%d %B %Y, %H:%M:%S")
    info_rows = [
        ("Anonymous Patient ID (APID)", apid),
        ("Ref. Rekam Medis (masked)", masked_rm),
        ("Usia Pasien", f"{patient_info.get('age', '-')} tahun"),
        ("Jenis Kelamin", patient_info.get("gender", "-")),
        ("Analis / Petugas", patient_info.get("examiner", "-")),
        ("Waktu Pemeriksaan", exam_time),
    ]
    for label_txt, value_txt in info_rows:
        pdf.set_font("Helvetica", "B", 10.5)
        pdf.cell(65, 7, f"{label_txt}", border=0)
        pdf.set_font("Helvetica", "", 10.5)
        pdf.cell(0, 7, f": {value_txt}", ln=1)
    pdf.ln(4)

    # ---------- Gambar Hasil Deteksi ----------
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Citra Hasil Deteksi AI", ln=1)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(3)

    tmp_path = None
    try:
        tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        tmp_path = tmp_file.name
        tmp_file.close()  # tutup handle sebelum ditulis ulang oleh PIL

        rgb_image = result_image.convert("RGB")
        rgb_image.save(tmp_path, format="PNG")  # proses tulis selesai & file ditutup otomatis oleh PIL

        img_w_px, img_h_px = rgb_image.size
        max_width_mm = 130
        ratio = max_width_mm / img_w_px
        display_h = img_h_px * ratio
        x_center = (210 - max_width_mm) / 2

        pdf.image(tmp_path, x=x_center, y=pdf.get_y(), w=max_width_mm, h=display_h)
        pdf.set_y(pdf.get_y() + display_h + 6)
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)

    # ---------- Hasil Kuantitatif ----------
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Hasil Kuantitatif", ln=1)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(3)
    pdf.set_font("Helvetica", "B", 10.5)
    pdf.cell(65, 7, "Jumlah BTA Terdeteksi", border=0)
    pdf.set_font("Helvetica", "", 10.5)
    pdf.cell(0, 7, f": {count} basil", ln=1)
    pdf.set_font("Helvetica", "B", 10.5)
    pdf.cell(65, 7, "Rata-rata Confidence Score", border=0)
    pdf.set_font("Helvetica", "", 10.5)
    pdf.cell(0, 7, f": {avg_conf:.1f}%", ln=1)
    pdf.ln(4)

    # ---------- Interpretasi Medis ----------
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Interpretasi Medis (Kesimpulan)", ln=1)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(3)
    r, g, b = _COLOR_MAP.get(css_class, (100, 116, 139))
    pdf.set_fill_color(r, g, b)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 9, f"  {label}", ln=1, fill=True)
    pdf.set_text_color(30, 41, 59)
    pdf.set_font("Helvetica", "", 10)
    pdf.ln(2)
    pdf.multi_cell(0, 6, description)
    pdf.ln(3)

    # ---------- Rekomendasi Rujukan Otomatis ----------
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Rekomendasi Tindak Lanjut / Rujukan", ln=1)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(3)
    pdf.set_font("Helvetica", "B", 10.5)
    pdf.cell(0, 6, f"Tingkat Urgensi: {referral['urgency']}  |  Tujuan: {referral['specialist_filter']}", ln=1)
    pdf.set_font("Helvetica", "", 10)
    pdf.ln(1)
    for action in referral["actions"]:
        effective_width = pdf.w - pdf.l_margin - pdf.r_margin
        pdf.multi_cell(effective_width, 5.5, f"- {action}")
    pdf.ln(6)

    pdf.set_font("Helvetica", "I", 8.5)
    pdf.set_text_color(148, 163, 184)
    pdf.multi_cell(
        0, 5,
        "Disclaimer: Laporan ini dihasilkan oleh sistem bantu diagnosis berbasis kecerdasan buatan (Clinical "
        "Decision Support System) dan WAJIB dikonfirmasi serta divalidasi oleh Dokter Spesialis Patologi Klinik "
        "(Sp.PK) atau tenaga medis berwenang sebelum digunakan sebagai dasar diagnosis final. Identitas pasien "
        "pada laporan ini telah dianonimkan sesuai standar etika perlindungan data kesehatan."
    )

    return bytes(pdf.output(dest="S"))
