"""
pages/2_Epidemiology_Dashboard.py
==================================
Dashboard Epidemiologi & Statistik TBC nasional: kartu statistik SaaS,
peta sebaran interaktif per provinsi, dan grafik tren tahunan.
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from core.styling import inject_global_css, render_page_header, render_sidebar_brand
from app_data.epidemiology import load_epidemiology_data, load_national_trend, national_summary

st.set_page_config(page_title="Dashboard Epidemiologi | SputumAI", page_icon="📊", layout="wide")
inject_global_css()

with st.sidebar:
    render_sidebar_brand()
    st.markdown('<div class="sidebar-section-label">Tentang Data</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="privacy-note">
        📎 Data pada dashboard ini bersifat ilustratif untuk keperluan demo,
        disusun menyerupai pola publikasi Kemenkes RI (SITB) & WHO Global TB Report.
        Untuk produksi, sambungkan ke API resmi data.kemkes.go.id / SATUSEHAT.
        </div>
        """,
        unsafe_allow_html=True,
    )

render_page_header(
    "Dashboard Epidemiologi TBC",
    "Visualisasi interaktif sebaran, prevalensi, dan tren penanggulangan Tuberkulosis di Indonesia.",
    badges=["📡 Sumber: Kemenkes/WHO (ilustratif)", "🔄 Update Berkala"],
    icon="📊",
)

df = load_epidemiology_data()
trend_df = load_national_trend()
summary = national_summary(df)

# ---------------------- Kartu Statistik SaaS ----------------------
c1, c2, c3, c4 = st.columns(4)
with c1:
    total_str = f'{summary["total_kasus"]:,}'.replace(",", ".")
    st.markdown(
        f'<div class="stat-card accent-red"><div class="stat-icon">🦠</div>'
        f'<div class="stat-value">{total_str}</div>'
        f'<div class="stat-label">Total Kasus Terkonfirmasi</div></div>',
        unsafe_allow_html=True,
    )
with c2:
    st.markdown(
        f'<div class="stat-card accent-green"><div class="stat-icon">✅</div>'
        f'<div class="stat-value">{summary["avg_kesembuhan"]}%</div>'
        f'<div class="stat-label">Rata-rata Angka Kesembuhan</div></div>',
        unsafe_allow_html=True,
    )
with c3:
    st.markdown(
        f'<div class="stat-card accent-amber"><div class="stat-icon">⚠️</div>'
        f'<div class="stat-value">{summary["zona_merah_count"]}</div>'
        f'<div class="stat-label">Provinsi Zona Merah</div></div>',
        unsafe_allow_html=True,
    )
with c4:
    st.markdown(
        f'<div class="stat-card accent-blue"><div class="stat-icon">📍</div>'
        f'<div class="stat-value">{summary["prevalensi_tertinggi"]}</div>'
        f'<div class="stat-label">Prevalensi Tertinggi/100rb ({summary["provinsi_tertinggi"]})</div></div>',
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------- Peta Sebaran & Tren ----------------------
col_map, col_trend = st.columns([1.3, 1], gap="medium")

with col_map:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">🗺️ Peta Sebaran Prevalensi TBC per Provinsi</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-subtitle">Ukuran & warna titik merepresentasikan tingkat prevalensi dan zona risiko</div>', unsafe_allow_html=True)

    zone_color_map = {"merah": "#ef4444", "kuning": "#f59e0b", "hijau": "#22c55e"}
    fig_map = px.scatter_mapbox(
        df, lat="lat", lon="lon", size="prevalensi_per_100k", color="zona",
        color_discrete_map=zone_color_map,
        hover_name="provinsi",
        hover_data={"lat": False, "lon": False, "prevalensi_per_100k": True, "angka_kesembuhan": True, "zona": True},
        size_max=38, zoom=3.6, height=430,
    )
    fig_map.update_layout(
        mapbox_style="carto-positron",
        margin=dict(l=0, r=0, t=0, b=0),
        legend=dict(title="Zona Risiko", orientation="h", yanchor="bottom", y=0.01, x=0.01),
        paper_bgcolor="#ffffff",
    )
    st.plotly_chart(fig_map, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col_trend:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">📈 Tren Nasional (2019–2025)</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-subtitle">Kasus ternotifikasi vs angka kesembuhan tahunan</div>', unsafe_allow_html=True)

    fig_trend = go.Figure()
    fig_trend.add_trace(go.Bar(
        x=trend_df["tahun"], y=trend_df["kasus_ternotifikasi"],
        name="Kasus Ternotifikasi", marker_color="#0ea5e9", yaxis="y1",
    ))
    fig_trend.add_trace(go.Scatter(
        x=trend_df["tahun"], y=trend_df["angka_kesembuhan_persen"],
        name="Angka Kesembuhan (%)", mode="lines+markers",
        line=dict(color="#1e3a8a", width=3), yaxis="y2",
    ))
    fig_trend.update_layout(
        height=430,
        margin=dict(l=0, r=0, t=10, b=0),
        paper_bgcolor="#ffffff", plot_bgcolor="#ffffff",
        yaxis=dict(title="Kasus", showgrid=False),
        yaxis2=dict(title="Kesembuhan (%)", overlaying="y", side="right", range=[60, 100], showgrid=False),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0),
        font=dict(color="#1e293b"),
    )
    st.plotly_chart(fig_trend, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------- Tabel Detail per Provinsi ----------------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="card-title">📋 Rincian Data per Provinsi</div>', unsafe_allow_html=True)
st.markdown('<div class="card-subtitle">Klik header kolom untuk mengurutkan data</div>', unsafe_allow_html=True)

display_df = df.copy()
display_df["Zona Risiko"] = display_df["zona"].map({"merah": "🔴 Merah", "kuning": "🟡 Kuning", "hijau": "🟢 Hijau"})
display_df = display_df.rename(columns={
    "provinsi": "Provinsi",
    "prevalensi_per_100k": "Prevalensi /100rb",
    "angka_kesembuhan": "Angka Kesembuhan (%)",
    "kasus_terkonfirmasi": "Kasus Terkonfirmasi",
})[["Provinsi", "Prevalensi /100rb", "Angka Kesembuhan (%)", "Kasus Terkonfirmasi", "Zona Risiko"]]

st.dataframe(display_df, use_container_width=True, hide_index=True)
st.markdown("</div>", unsafe_allow_html=True)
