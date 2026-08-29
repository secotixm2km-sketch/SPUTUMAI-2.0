"""
pages/3_Smart_Referral_Map.py
===============================
Fitur Rujukan Cerdas & Interactive Hospital Map.
Menampilkan peta Folium dengan marker RS/Dokter, popup interaktif
(foto/profil, biodata, alamat, jam operasional, tombol call & WhatsApp),
serta filter otomatis berdasarkan kategori hasil AI terakhir (jika ada).
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import folium
from streamlit_folium import st_folium

from core.styling import inject_global_css, render_page_header, render_sidebar_brand
from core.inference import get_referral_recommendation
from data.hospitals import FACILITIES, filter_facilities_by_category

st.set_page_config(page_title="Rujukan Cerdas & Peta RS | SputumAI", page_icon="🗺️", layout="wide")
inject_global_css()

with st.sidebar:
    render_sidebar_brand()
    st.markdown('<div class="sidebar-section-label">Filter Fasilitas</div>', unsafe_allow_html=True)

    auto_category = st.session_state.get("referral_filter_category")
    category_options = {
        "Semua Fasilitas": None,
        "Hasil Negatif": "negative",
        "Hasil Scanty": "scanty",
        "Hasil Positif Aktif": "positive",
    }
    default_index = 0
    if auto_category:
        reverse_map = {v: k for k, v in category_options.items() if v is not None}
        default_label = reverse_map.get(auto_category, "Semua Fasilitas")
        default_index = list(category_options.keys()).index(default_label)

    selected_label = st.selectbox("Tampilkan sesuai kategori hasil AI", list(category_options.keys()), index=default_index)
    selected_category = category_options[selected_label]

    facility_type_filter = st.multiselect(
        "Jenis Fasilitas", ["Rumah Sakit", "Dokter", "Puskesmas"],
        default=["Rumah Sakit", "Dokter", "Puskesmas"],
    )

    if auto_category:
        st.markdown(
            f'<div class="privacy-note">🔗 Filter otomatis diterapkan dari hasil pemindaian terakhir: '
            f'<b>{auto_category.upper()}</b></div>',
            unsafe_allow_html=True,
        )

render_page_header(
    "Rujukan Cerdas & Peta Fasilitas TBC",
    "Temukan Rumah Sakit rujukan dan Dokter Spesialis Paru/Sp.PK terdekat berdasarkan rekomendasi sistem AI.",
    badges=["🩺 Rujukan Otomatis", "🗺️ Peta Interaktif", "📞 Kontak Cepat"],
    icon="🗺️",
)

# ---------------------- Rekomendasi Otomatis (jika tersedia) ----------------------
if selected_category:
    rec = get_referral_recommendation(selected_category)
    urgency_color = rec["urgency_color"]
    st.markdown(
        f"""
        <div class="card">
            <div class="card-title">🚑 {rec['action_title']}</div>
            <div class="card-subtitle">
                Urgensi: <span class="zone-badge {urgency_color}">{rec['urgency']}</span>
                &nbsp;|&nbsp; Fasilitas dituju: <b>{rec['specialist_filter']}</b>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ---------------------- Data terfilter ----------------------
if selected_category:
    facilities = filter_facilities_by_category(selected_category)
else:
    facilities = FACILITIES

facilities = [f for f in facilities if f["type"] in facility_type_filter]

col_map, col_list = st.columns([1.4, 1], gap="medium")

# ---------------------- Peta Folium ----------------------
with col_map:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">🗺️ Peta Fasilitas Rujukan</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-subtitle">Klik marker untuk melihat profil, kontak, dan jam operasional</div>', unsafe_allow_html=True)

    if facilities:
        center_lat = sum(f["lat"] for f in facilities) / len(facilities)
        center_lon = sum(f["lon"] for f in facilities) / len(facilities)
    else:
        center_lat, center_lon = -2.5489, 118.0149  # tengah Indonesia

    fmap = folium.Map(location=[center_lat, center_lon], zoom_start=5 if facilities else 4.3, tiles="CartoDB positron")

    type_icon_map = {"Rumah Sakit": ("hospital-o", "red"), "Dokter": ("user-md", "blue"), "Puskesmas": ("plus-square", "green")}

    for f in facilities:
        icon_name, icon_color = type_icon_map.get(f["type"], ("info-sign", "gray"))
        popup_html = f"""
        <div style="font-family:'Segoe UI',sans-serif; width:230px;">
            <div style="font-size:28px; text-align:center;">{f['photo']}</div>
            <div style="font-weight:700; font-size:14px; color:#0f172a; text-align:center; margin-bottom:2px;">{f['name']}</div>
            <div style="font-size:11px; color:#0ea5e9; font-weight:600; text-align:center; margin-bottom:8px;">{f['type']}</div>
            <div style="font-size:11.5px; color:#334155; line-height:1.5; margin-bottom:6px;">{f['bio']}</div>
            <div style="font-size:11px; color:#64748b; margin-bottom:2px;">📍 {f['address']}</div>
            <div style="font-size:11px; color:#64748b; margin-bottom:8px;">🕒 {f['hours']}</div>
            <a href="tel:{f['phone']}" style="display:inline-block;background:#e0f2fe;color:#0369a1;padding:5px 10px;border-radius:8px;font-size:11px;font-weight:700;text-decoration:none;margin-right:6px;">📞 Telepon</a>
            <a href="https://wa.me/{f['whatsapp']}" target="_blank" style="display:inline-block;background:#dcfce7;color:#15803d;padding:5px 10px;border-radius:8px;font-size:11px;font-weight:700;text-decoration:none;">💬 WhatsApp</a>
        </div>
        """
        folium.Marker(
            location=[f["lat"], f["lon"]],
            tooltip=f["name"],
            popup=folium.Popup(popup_html, max_width=260),
            icon=folium.Icon(color=icon_color, icon=icon_name, prefix="fa"),
        ).add_to(fmap)

    st_folium(fmap, use_container_width=True, height=480, returned_objects=[])
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------- Daftar Kartu Fasilitas ----------------------
with col_list:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">📇 Daftar Fasilitas & Kontak</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="card-subtitle">{len(facilities)} fasilitas ditemukan sesuai filter</div>', unsafe_allow_html=True)

    if not facilities:
        st.info("Tidak ada fasilitas yang cocok dengan filter saat ini.")

    for f in facilities:
        st.markdown(
            f"""
            <div class="referral-card">
                <div class="referral-avatar">{f['photo']}</div>
                <div style="flex:1;">
                    <div class="referral-name">{f['name']}</div>
                    <div class="referral-sub">{f['type']}</div>
                    <div class="referral-meta">
                        📍 {f['address']}<br>
                        🕒 {f['hours']}
                    </div>
                    <a class="action-link action-call" href="tel:{f['phone']}">📞 Telepon</a>
                    <a class="action-link action-wa" href="https://wa.me/{f['whatsapp']}" target="_blank">💬 WhatsApp</a>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)
