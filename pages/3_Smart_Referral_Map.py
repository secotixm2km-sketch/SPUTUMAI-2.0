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

import math

import streamlit as st
import streamlit.components.v1 as components
import folium
from streamlit_folium import st_folium

from core.styling import inject_global_css, render_page_header, render_sidebar_brand
from core.inference import get_referral_recommendation
from app_data.hospitals import FACILITIES, filter_facilities_by_category

st.set_page_config(page_title="Rujukan Cerdas & Peta RS | SputumAI", page_icon="🗺️", layout="wide")
inject_global_css()

# Titik referensi kota besar sebagai fallback jika pengguna tidak mengizinkan
# akses GPS browser (mis. dibuka lewat desktop tanpa GPS, atau izin ditolak).
CITY_REFERENCE_POINTS = {
    "Jakarta": (-6.2088, 106.8456),
    "Surabaya": (-7.2575, 112.7521),
    "Bandung": (-6.9175, 107.6191),
    "Medan": (3.5952, 98.6722),
    "Semarang": (-6.9932, 110.4203),
    "Yogyakarta": (-7.7956, 110.3695),
    "Makassar": (-5.1477, 119.4327),
    "Denpasar": (-8.6705, 115.2126),
    "Palembang": (-2.9761, 104.7754),
    "Malang": (-7.9666, 112.6326),
}


def haversine_km(lat1, lon1, lat2, lon2):
    """Menghitung jarak garis lurus (great-circle) antara dua koordinat dalam km."""
    r = 6371.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


with st.sidebar:
    render_sidebar_brand()
    st.markdown('<div class="sidebar-section-label">📍 Lokasi Anda (GPS)</div>', unsafe_allow_html=True)

    geo_widget_html = """
    <div style="font-family:'Segoe UI',sans-serif;">
      <button id="geoBtn" style="background:linear-gradient(135deg,#0ea5e9,#1e3a8a);color:#fff;
        border:none;border-radius:10px;padding:9px 16px;font-weight:600;font-size:13px;
        cursor:pointer;width:100%;">📍 Gunakan Lokasi Saya (GPS)</button>
      <div id="geoStatus" style="font-size:11.5px;color:#64748b;margin-top:6px;"></div>
    </div>
    <script>
    document.getElementById("geoBtn").addEventListener("click", function() {
      const status = document.getElementById("geoStatus");
      if (!navigator.geolocation) {
        status.innerText = "Browser tidak mendukung GPS.";
        return;
      }
      status.innerText = "Meminta izin lokasi...";
      navigator.geolocation.getCurrentPosition(function(pos) {
        status.innerText = "Lokasi ditemukan, memuat ulang halaman...";
        const url = new URL(window.top.location.href);
        url.searchParams.set("lat", pos.coords.latitude);
        url.searchParams.set("lon", pos.coords.longitude);
        window.top.location.href = url.toString();
      }, function(err) {
        status.innerText = "Gagal mengambil lokasi: " + err.message;
      });
    });
    </script>
    """
    components.html(geo_widget_html, height=80)

    query_params = st.query_params
    user_lat = user_lon = None
    if "lat" in query_params and "lon" in query_params:
        try:
            user_lat = float(query_params["lat"])
            user_lon = float(query_params["lon"])
            st.caption(f"✅ Lokasi GPS aktif: {user_lat:.4f}, {user_lon:.4f}")
        except (TypeError, ValueError):
            user_lat = user_lon = None

    if user_lat is None:
        fallback_city = st.selectbox("Atau pilih kota Anda (fallback tanpa GPS)", ["- Tidak dipilih -"] + list(CITY_REFERENCE_POINTS.keys()))
        if fallback_city != "- Tidak dipilih -":
            user_lat, user_lon = CITY_REFERENCE_POINTS[fallback_city]

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
        "Jenis Fasilitas", ["Rumah Sakit", "Klinik", "Puskesmas"],
        default=["Rumah Sakit", "Klinik", "Puskesmas"],
    )

    if auto_category:
        st.markdown(
            f'<div class="privacy-note">🔗 Filter otomatis diterapkan dari hasil pemindaian terakhir: '
            f'<b>{auto_category.upper()}</b></div>',
            unsafe_allow_html=True,
        )

render_page_header(
    "Rujukan Cerdas & Peta Fasilitas TBC",
    "Temukan Rumah Sakit rujukan, Klinik spesialis paru, dan Puskesmas terdekat berdasarkan rekomendasi sistem AI.",
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

# ---------------------- Urutkan berdasarkan jarak dari lokasi pengguna ----------------------
if user_lat is not None and user_lon is not None:
    for f in facilities:
        f["_distance_km"] = haversine_km(user_lat, user_lon, f["lat"], f["lon"])
    facilities = sorted(facilities, key=lambda f: f["_distance_km"])
    st.success(f"📍 Fasilitas diurutkan dari yang **TERDEKAT** dari lokasi Anda ({len(facilities)} ditemukan).")
else:
    st.info("💡 Aktifkan GPS di sidebar (atau pilih kota) untuk melihat fasilitas terurut dari yang terdekat.")

col_map, col_list = st.columns([1.4, 1], gap="medium")

# ---------------------- Peta Folium ----------------------
with col_map:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">🗺️ Peta Fasilitas Rujukan</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-subtitle">Klik marker untuk melihat profil, kontak, dan jam operasional</div>', unsafe_allow_html=True)

    if user_lat is not None and user_lon is not None:
        center_lat, center_lon = user_lat, user_lon
        zoom_level = 11
    elif facilities:
        center_lat = sum(f["lat"] for f in facilities) / len(facilities)
        center_lon = sum(f["lon"] for f in facilities) / len(facilities)
        zoom_level = 5
    else:
        center_lat, center_lon = -2.5489, 118.0149  # tengah Indonesia
        zoom_level = 4.3

    fmap = folium.Map(location=[center_lat, center_lon], zoom_start=zoom_level, tiles="CartoDB positron")

    if user_lat is not None and user_lon is not None:
        folium.Marker(
            location=[user_lat, user_lon],
            tooltip="Lokasi Anda",
            icon=folium.Icon(color="darkblue", icon="user", prefix="fa"),
        ).add_to(fmap)

    type_icon_map = {"Rumah Sakit": ("hospital-o", "red"), "Klinik": ("stethoscope", "blue"), "Puskesmas": ("plus-square", "green")}

    for f in facilities:
        icon_name, icon_color = type_icon_map.get(f["type"], ("info-sign", "gray"))
        distance_html = (
            f'<div style="font-size:11px;color:#0ea5e9;font-weight:700;margin-bottom:4px;">📏 ~{f["_distance_km"]:.1f} km dari lokasi Anda</div>'
            if "_distance_km" in f else ""
        )
        phone_html = (
            f'<a href="tel:{f["phone"]}" style="display:inline-block;background:#e0f2fe;color:#0369a1;padding:5px 10px;border-radius:8px;font-size:11px;font-weight:700;text-decoration:none;">📞 {f["phone"]}</a>'
            if f.get("phone")
            else '<span style="font-size:11px;color:#94a3b8;">Nomor telepon belum tersedia — cari nama fasilitas ini di Google untuk info terkini.</span>'
        )
        popup_html = f"""
        <div style="font-family:'Segoe UI',sans-serif; width:230px;">
            <div style="font-size:28px; text-align:center;">{f['photo']}</div>
            <div style="font-weight:700; font-size:14px; color:#0f172a; text-align:center; margin-bottom:2px;">{f['name']}</div>
            <div style="font-size:11px; color:#0ea5e9; font-weight:600; text-align:center; margin-bottom:8px;">{f['type']}</div>
            {distance_html}
            <div style="font-size:11.5px; color:#334155; line-height:1.5; margin-bottom:6px;">{f['bio']}</div>
            <div style="font-size:11px; color:#64748b; margin-bottom:2px;">📍 {f['address']}</div>
            <div style="font-size:11px; color:#64748b; margin-bottom:8px;">🕒 {f['hours']}</div>
            {phone_html}
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
        phone_link = (
            f'<a class="action-link action-call" href="tel:{f["phone"]}">📞 {f["phone"]}</a>'
            if f.get("phone")
            else '<span style="font-size:11.5px;color:#94a3b8;">Nomor telepon belum tersedia</span>'
        )
        distance_badge = (
            f'<span class="zone-badge hijau" style="margin-left:6px;">📏 ~{f["_distance_km"]:.1f} km</span>'
            if "_distance_km" in f else ""
        )
        st.markdown(
            f"""
            <div class="referral-card">
                <div class="referral-avatar">{f['photo']}</div>
                <div style="flex:1;">
                    <div class="referral-name">{f['name']}{distance_badge}</div>
                    <div class="referral-sub">{f['type']}</div>
                    <div class="referral-meta">
                        📍 {f['address']}<br>
                        🕒 {f['hours']}
                    </div>
                    {phone_link}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)
