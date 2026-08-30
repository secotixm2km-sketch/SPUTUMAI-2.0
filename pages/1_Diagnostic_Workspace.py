"""
pages/1_Diagnostic_Workspace.py
================================
Modul Diagnostik AI: unggah citra dahak -> inferensi YOLOv8 -> interpretasi
klinis -> rekomendasi rujukan otomatis -> laporan PDF (identitas dianonimkan).
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from PIL import Image

from core.styling import inject_global_css, render_page_header, render_sidebar_brand, safe_switch_page, safe_image
from core.security import anonymize_id, mask_identifier, is_valid_rm_format, consent_gate
from core.inference import (
    load_model, run_inference, get_diagnosis_class, get_referral_recommendation,
    ULTRALYTICS_AVAILABLE, ULTRALYTICS_IMPORT_ERROR, MODEL_PATH,
)
from core.pdf_report import generate_pdf_report

st.set_page_config(page_title="Diagnostic Workspace | SputumAI", page_icon="🩺", layout="wide")
inject_global_css()


def init_state():
    defaults = {
        "input_image": None, "result_image": None, "bta_count": None,
        "avg_confidence": None, "scan_done": False, "detections": [],
        "last_category": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def render_progress_bar(label: str, percentage: float):
    percentage = max(0, min(100, percentage))
    st.markdown(
        f"""
        <div class="progress-wrap">
            <div class="progress-label-row" style="display:flex;justify-content:space-between;font-size:12.5px;font-weight:600;color:#334155;margin-bottom:6px;">
                <span>{label}</span><span>{percentage:.1f}%</span>
            </div>
            <div style="width:100%;height:16px;background:#e2e8f0;border-radius:999px;overflow:hidden;box-shadow:inset 0 1px 3px rgba(0,0,0,0.08);">
                <div style="height:100%;border-radius:999px;background:linear-gradient(90deg,#0ea5e9,#1e3a8a);width:{percentage:.1f}%;transition:width 1s ease-in-out;"></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


init_state()

with st.sidebar:
    render_sidebar_brand()
    st.markdown('<div class="sidebar-section-label">Data Pasien</div>', unsafe_allow_html=True)
    rm_number = st.text_input("Nomor Rekam Medis", placeholder="Contoh: RM-00231458")
    patient_age = st.number_input("Usia Pasien (tahun)", min_value=0, max_value=120, value=30, step=1)
    patient_gender = st.selectbox("Jenis Kelamin", ["Laki-laki", "Perempuan"])
    examiner_name = st.text_input("Nama Analis / Petugas Lab", placeholder="Contoh: dr. Andi Wijaya, Sp.PK")

    st.markdown('<div class="sidebar-section-label">Privasi Data</div>', unsafe_allow_html=True)
    consent = st.checkbox("Pasien/petugas menyetujui pemrosesan citra oleh AI untuk tujuan diagnostik.", value=False)
    if rm_number:
        st.markdown(
            f'<div class="privacy-note">🔒 ID Anonim (APID): <b>{anonymize_id(rm_number)}</b><br>'
            f'RM tersamarkan: {mask_identifier(rm_number)}</div>',
            unsafe_allow_html=True,
        )

    st.markdown('<div class="sidebar-section-label">Panduan Kualitas Citra</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="guidance-box" style="background:#f0f9ff;border:1px solid #bae6fd;border-radius:12px;padding:14px 16px;font-size:12.5px;color:#0c4a6e;line-height:1.6;">
            <b>📌 Standar Preparat Mikroskopis</b>
            <ul style="margin:6px 0 0 0;padding-left:18px;">
                <li>Pembesaran objektif <b>100x</b> (minyak imersi).</li>
                <li>Pencahayaan merata, tidak overexposed.</li>
                <li>Fokus tajam pada lapang pandang BTA.</li>
                <li>Format file JPG/PNG, resolusi ≥ 640px.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

patient_info = {
    "rm_number": rm_number if rm_number else "-",
    "age": patient_age,
    "gender": patient_gender,
    "examiner": examiner_name if examiner_name else "-",
}

render_page_header(
    "Diagnostic Workspace",
    "Unggah citra sediaan dahak mikroskopis untuk deteksi otomatis Basil Tahan Asam (BTA) menggunakan YOLOv8.",
    badges=["⚙️ Model: YOLOv8", "🔬 Mode: Klinis", "🔒 Privasi: Data Anonim"],
)

model = load_model(MODEL_PATH)

col_input, col_workspace = st.columns([1, 1.4], gap="medium")

with col_input:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">📥 Sumber Citra</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-subtitle">Pilih metode input citra sediaan dahak mikroskopis</div>', unsafe_allow_html=True)

    input_mode = st.radio("Metode Input", ["Unggah File (Drag & Drop)", "Kamera Mikroskop"], label_visibility="collapsed")

    uploaded_image = None
    if input_mode == "Unggah File (Drag & Drop)":
        uploaded_file = st.file_uploader("Seret & lepas citra di sini, atau klik untuk memilih file", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            uploaded_image = Image.open(uploaded_file).convert("RGB")
    else:
        camera_file = st.camera_input("Ambil citra langsung dari kamera mikroskop")
        if camera_file is not None:
            uploaded_image = Image.open(camera_file).convert("RGB")

    if uploaded_image is not None:
        st.session_state.input_image = uploaded_image
        st.session_state.scan_done = False

    st.markdown("</div>", unsafe_allow_html=True)

    if not ULTRALYTICS_AVAILABLE:
        st.warning("⚠️ Modul `ultralytics` belum terpasang di environment ini.")
        if ULTRALYTICS_IMPORT_ERROR:
            st.code(ULTRALYTICS_IMPORT_ERROR, language="text")
    elif model is None:
        st.warning(f"⚠️ Model `{MODEL_PATH}` tidak ditemukan di direktori aplikasi.")
    if not rm_number or not is_valid_rm_format(rm_number):
        st.info("ℹ️ Masukkan Nomor Rekam Medis dengan format valid (4-20 karakter alfanumerik) di sidebar.")

with col_workspace:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">🔬 Ruang Kerja Analisis</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-subtitle">Pratinjau citra dan eksekusi pemindaian AI</div>', unsafe_allow_html=True)

    if st.session_state.input_image is None:
        st.markdown(
            """
            <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;padding:70px 20px;text-align:center;border:2px dashed #cbd5e1;border-radius:16px;background:#f8fafc;">
                <div style="width:72px;height:72px;border-radius:50%;background:linear-gradient(135deg,#e0f2fe,#dbeafe);display:flex;align-items:center;justify-content:center;font-size:34px;margin-bottom:16px;">🩺</div>
                <h4 style="color:#334155;font-size:16px;margin:0 0 4px 0;">Belum Ada Citra Dimuat</h4>
                <p style="color:#94a3b8;font-size:13px;max-width:280px;">Unggah atau ambil citra sediaan dahak melalui panel di sebelah kiri untuk memulai analisis.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        safe_image(st.session_state.input_image, caption="Citra Input — Belum Dianalisis")
        can_run = consent_gate(consent) and is_valid_rm_format(rm_number) and model is not None
        run_scan = st.button("🚀 Jalankan Pemindaian AI", use_container_width=True, disabled=not can_run)

        if not consent and st.session_state.input_image is not None:
            st.caption("⚠️ Centang persetujuan pemrosesan data di sidebar untuk mengaktifkan tombol pemindaian.")

        if run_scan:
            with st.spinner("Menganalisis citra mikroskopis... AI sedang mendeteksi BTA."):
                annotated_image, count, avg_conf, confidences = run_inference(model, st.session_state.input_image)
            st.session_state.result_image = annotated_image
            st.session_state.bta_count = count
            st.session_state.avg_confidence = avg_conf
            st.session_state.detections = confidences
            st.session_state.scan_done = True
            category, _, _, _ = get_diagnosis_class(count)
            st.session_state.last_category = category
            st.toast("✅ Pemindaian AI selesai! Hasil siap ditinjau.", icon="✅")
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


if st.session_state.scan_done and st.session_state.result_image is not None:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">📊 Hasil Pemeriksaan</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-subtitle">Tinjau hasil deteksi visual, laporan klinis, dan rekomendasi rujukan</div>', unsafe_allow_html=True)

    tab_visual, tab_report, tab_referral = st.tabs(["🖼️ Analisis Visual", "📋 Laporan Klinis", "🚑 Rekomendasi Rujukan"])

    count = st.session_state.bta_count
    avg_conf = st.session_state.avg_confidence
    category, css_class, label, description = get_diagnosis_class(count)
    referral = get_referral_recommendation(category)

    with tab_visual:
        col_a, col_b = st.columns(2, gap="medium")
        with col_a:
            safe_image(st.session_state.input_image)
            st.caption("Citra Asli (Original)")
        with col_b:
            safe_image(st.session_state.result_image)
            st.caption("Hasil Deteksi AI (Annotated)")

        st.markdown("<br>", unsafe_allow_html=True)
        m1, m2, m3 = st.columns(3)
        with m1:
            st.markdown(f'<div class="stat-card accent-blue"><div class="stat-value">{count}</div><div class="stat-label">Total BTA Terdeteksi</div></div>', unsafe_allow_html=True)
        with m2:
            st.markdown(f'<div class="stat-card accent-blue"><div class="stat-value">{avg_conf:.1f}%</div><div class="stat-label">Rata-rata Confidence</div></div>', unsafe_allow_html=True)
        with m3:
            st.markdown(f'<div class="stat-card accent-blue"><div class="stat-value">{category.upper()}</div><div class="stat-label">Kategori Sementara</div></div>', unsafe_allow_html=True)

    with tab_report:
        box_bg = {"negative": "#f0fdf4", "scanty": "#fffbeb", "positive": "#fef2f2"}[css_class]
        box_border = {"negative": "#22c55e", "scanty": "#f59e0b", "positive": "#ef4444"}[css_class]
        title_color = {"negative": "#15803d", "scanty": "#b45309", "positive": "#b91c1c"}[css_class]
        st.markdown(
            f"""
            <div style="border-radius:14px;padding:22px 24px;margin-bottom:18px;border-left:6px solid {box_border};background:{box_bg};">
                <div style="font-size:19px;font-weight:800;color:{title_color};margin-bottom:4px;">{label}</div>
                <div style="font-size:13.5px;color:#334155;line-height:1.6;">{description}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("##### Visualisasi Confidence Score Model AI")
        render_progress_bar("Rata-rata Confidence Score Deteksi", avg_conf)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("##### Ringkasan Data Pemeriksaan (Anonim)")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"**Anonymous Patient ID:** `{anonymize_id(rm_number)}`")
            st.markdown(f"**Usia Pasien:** {patient_age} tahun")
        with c2:
            st.markdown(f"**Jenis Kelamin:** {patient_gender}")
            st.markdown(f"**RM (tersamarkan):** {mask_identifier(rm_number)}")

        st.markdown("<br>", unsafe_allow_html=True)
        pdf_bytes = generate_pdf_report(patient_info, st.session_state.result_image, count, avg_conf)
        file_name = f"Laporan_SputumAI_{anonymize_id(rm_number)}.pdf"
        st.download_button("⬇️ Unduh Laporan Medis (PDF)", data=pdf_bytes, file_name=file_name, mime="application/pdf", use_container_width=True)

    with tab_referral:
        urgency_color = referral["urgency_color"]
        st.markdown(
            f"""
            <div class="card" style="margin-bottom:14px;">
                <div class="card-title">🚑 {referral['action_title']}</div>
                <div class="card-subtitle">
                    Urgensi: <span class="zone-badge {urgency_color}">{referral['urgency']}</span>
                    &nbsp;|&nbsp; Tujuan Rujukan: <b>{referral['specialist_filter']}</b>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("**Langkah tindak lanjut yang direkomendasikan sistem:**")
        for action in referral["actions"]:
            st.markdown(f"- {action}")

        st.markdown("<br>", unsafe_allow_html=True)
        st.info("💡 Buka halaman **Rujukan Cerdas & Peta RS** di menu sidebar untuk melihat fasilitas & dokter terdekat sesuai kategori hasil ini.")
        if st.button("🗺️ Lihat Peta Rujukan Sesuai Hasil Ini", use_container_width=True):
            st.session_state["referral_filter_category"] = category
            safe_switch_page(
                "pages/3_Smart_Referral_Map.py",
                fallback_message="Buka halaman 'Rujukan Cerdas & Peta RS' lewat menu navigasi di sidebar sebelah kiri atas.",
            )

    st.markdown("</div>", unsafe_allow_html=True)
