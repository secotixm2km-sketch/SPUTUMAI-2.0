"""
app.py
=======
Entry point utama SputumAI Workspace — End-to-End Tuberculosis Platform.
Berfungsi sebagai landing page yang merangkum 3 pilar fitur platform dan
menjadi hub navigasi menuju setiap modul (Streamlit multipage app via
folder `pages/`).
"""

import streamlit as st

from core.styling import inject_global_css, render_page_header, render_sidebar_brand

st.set_page_config(
    page_title="SputumAI Workspace | End-to-End TB Platform",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
)
inject_global_css()

with st.sidebar:
    render_sidebar_brand()
    st.markdown('<div class="sidebar-section-label">Navigasi Platform</div>', unsafe_allow_html=True)
    # Catatan: tidak membuat page_link ke app.py itu sendiri (halaman utama yang
    # sedang berjalan) karena beberapa versi Streamlit melempar KeyError saat
    # sebuah skrip mereferensikan dirinya sendiri sebagai "page" terdaftar.
    st.caption("🏠 Anda sedang berada di halaman Beranda")
    st.page_link("pages/1_Diagnostic_Workspace.py", label="🩺 Diagnostic Workspace")
    st.page_link("pages/2_Epidemiology_Dashboard.py", label="📊 Dashboard Epidemiologi")
    st.page_link("pages/3_Smart_Referral_Map.py", label="🗺️ Rujukan Cerdas & Peta RS")
    st.page_link("pages/4_Education_Center.py", label="📚 Pusat Edukasi TBC")

    st.markdown("<br>", unsafe_allow_html=True)
    st.caption("© 2026 SputumAI Workspace — Clinical Decision Support Platform. Bukan pengganti diagnosis dokter Sp.PK.")

render_page_header(
    "SputumAI Workspace",
    "Platform Kesehatan End-to-End untuk Deteksi, Edukasi, dan Penanggulangan Tuberkulosis berbasis "
    "Kecerdasan Buatan — dari diagnosis mikroskopis hingga rujukan dan edukasi pasien.",
    badges=["⚙️ AI-Powered Diagnostics", "📊 Epidemiology Intelligence", "🗺️ Smart Referral", "📚 Digital Health Literacy"],
)

st.markdown(
    """
    <div class="card">
        <div class="card-title">👋 Selamat Datang di SputumAI Workspace</div>
        <div class="card-subtitle" style="font-size:13.5px; line-height:1.7; color:#334155;">
            SputumAI Workspace adalah <b>Clinical Decision Support System (CDSS)</b> yang menggabungkan
            deteksi otomatis Basil Tahan Asam (BTA) berbasis YOLOv8, intelijen epidemiologi nasional,
            sistem rujukan cerdas, dan pusat edukasi interaktif dalam satu platform terpadu — dirancang
            untuk mendukung tenaga kesehatan, laboratorium, dan pasien dalam alur penanggulangan TBC
            secara end-to-end.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

col1, col2, col3, col4 = st.columns(4, gap="medium")

pillar_cards = [
    {
        "icon": "🩺",
        "title": "1. Diagnostic Workspace",
        "desc": "Unggah citra dahak mikroskopis, jalankan deteksi AI YOLOv8, dan hasilkan laporan klinis PDF dengan identitas pasien yang dianonimkan.",
        "page": "pages/1_Diagnostic_Workspace.py",
        "cta": "Mulai Diagnosis",
    },
    {
        "icon": "📊",
        "title": "2. Dashboard Epidemiologi",
        "desc": "Pantau prevalensi, angka kesembuhan, dan zona risiko TBC di seluruh provinsi Indonesia melalui peta dan grafik tren interaktif.",
        "page": "pages/2_Epidemiology_Dashboard.py",
        "cta": "Lihat Statistik",
    },
    {
        "icon": "🗺️",
        "title": "3. Rujukan Cerdas",
        "desc": "Dapatkan rekomendasi tindak lanjut otomatis berdasarkan hasil AI, lengkap dengan peta RS/dokter rujukan dan kontak cepat.",
        "page": "pages/3_Smart_Referral_Map.py",
        "cta": "Cari Fasilitas",
    },
    {
        "icon": "📚",
        "title": "4. Pusat Edukasi",
        "desc": "Pelajari pencegahan penularan, panduan pasien baru terdiagnosis, repositori jurnal ilmiah, dan uji pemahaman lewat Smart Quiz.",
        "page": "pages/4_Education_Center.py",
        "cta": "Mulai Belajar",
    },
]

for col, pillar in zip([col1, col2, col3, col4], pillar_cards):
    with col:
        st.markdown(
            f"""
            <div class="card" style="min-height:230px;">
                <div style="font-size:32px; margin-bottom:8px;">{pillar['icon']}</div>
                <div class="card-title">{pillar['title']}</div>
                <div class="card-subtitle" style="min-height:90px;">{pillar['desc']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.page_link(pillar["page"], label=pillar["cta"], use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

st.markdown(
    """
    <div class="card">
        <div class="card-title">🔒 Komitmen Privasi & Etika Data</div>
        <div class="card-subtitle" style="font-size:13px; line-height:1.7; color:#334155;">
            Seluruh Nomor Rekam Medis pasien diproses melalui mekanisme <b>hashing satu-arah (SHA-256 + salt)</b>
            menjadi <b>Anonymous Patient ID (APID)</b> sebelum disertakan dalam laporan atau ekspor data apa pun.
            Data asli pasien tidak pernah disimpan dalam bentuk yang dapat diidentifikasi ulang pada
            artefak yang dibagikan, sejalan dengan prinsip etika perlindungan data kesehatan.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
