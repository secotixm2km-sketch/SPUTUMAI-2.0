"""
core/styling.py
================
CSS terpusat & komponen UI bersama (Design System) untuk seluruh halaman
SputumAI Workspace. Dipanggil di setiap file pages/*.py dan app.py agar
konsistensi visual (Navy Blue / Sky Blue / Light Mode enforced) terjaga
di seluruh platform.
"""

import streamlit as st

PRIMARY_NAVY = "#0f172a"
PRIMARY_BLUE = "#1e3a8a"
ACCENT_SKY = "#0ea5e9"
BG_LIGHT = "#f1f5f9"
TEXT_SLATE = "#1e293b"


def inject_global_css():
    st.markdown(
        """
        <style>
        /* ---- Force Light Mode di seluruh platform ---- */
        html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
            color-scheme: light only;
            background-color: #f1f5f9 !important;
            color: #1e293b !important;
        }
        [data-testid="stAppViewContainer"] * { color: #1e293b; }
        [data-testid="stHeader"] { background-color: rgba(0,0,0,0) !important; }

        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        [data-testid="stToolbar"] {visibility: hidden;}
        [data-testid="stDecoration"] {display: none;}

        html, body, [class*="css"] {
            font-family: 'Segoe UI', 'Inter', -apple-system, sans-serif;
        }
        .block-container {
            padding-top: 1.2rem;
            padding-bottom: 3rem;
            max-width: 1300px;
        }

        /* ---- Header Banner ---- */
        .clinical-header {
            background: linear-gradient(120deg, #0f172a 0%, #1e3a8a 55%, #0ea5e9 130%);
            padding: 26px 34px;
            border-radius: 18px;
            margin-bottom: 22px;
            box-shadow: 0 10px 30px rgba(15, 23, 42, 0.25);
            position: relative;
            overflow: hidden;
        }
        .clinical-header::after {
            content: "";
            position: absolute; top: -60px; right: -60px;
            width: 220px; height: 220px;
            background: rgba(14, 165, 233, 0.25);
            border-radius: 50%;
        }
        .clinical-header h1 {
            color: #ffffff !important;
            font-size: 27px; font-weight: 800; margin: 0; letter-spacing: -0.4px;
        }
        .clinical-header p {
            color: #dbeafe !important;
            font-size: 14px; margin: 6px 0 0 0; max-width: 760px;
        }
        .badge-row { margin-top: 12px; display: flex; gap: 8px; flex-wrap: wrap; }
        .header-badge {
            background: rgba(255,255,255,0.12);
            border: 1px solid rgba(255,255,255,0.25);
            color: #e0f2fe !important;
            padding: 4px 12px; border-radius: 999px;
            font-size: 12px; font-weight: 600;
        }

        /* ---- Card ---- */
        .card {
            background: #ffffff;
            border-radius: 16px;
            padding: 22px 24px;
            box-shadow: 0 4px 18px rgba(30, 41, 59, 0.07);
            border: 1px solid #e2e8f0;
            margin-bottom: 20px;
        }
        .card-title {
            font-size: 15.5px; font-weight: 700; color: #0f172a !important;
            margin-bottom: 4px; display: flex; align-items: center; gap: 8px;
        }
        .card-subtitle { font-size: 12.5px; color: #64748b !important; margin-bottom: 16px; }

        /* ---- Sidebar branding ---- */
        [data-testid="stSidebar"] { background-color: #ffffff !important; border-right: 1px solid #e2e8f0; }
        [data-testid="stSidebar"] * { color: #1e293b !important; }
        .sidebar-brand {
            display: flex; align-items: center; gap: 10px;
            padding: 6px 0 18px 0; border-bottom: 1px solid #e2e8f0; margin-bottom: 14px;
        }
        .sidebar-brand-icon {
            background: linear-gradient(135deg, #0f172a, #0ea5e9);
            width: 38px; height: 38px; border-radius: 10px;
            display: flex; align-items: center; justify-content: center; font-size: 19px;
        }
        .sidebar-brand-text b { font-size: 15px; color: #0f172a !important; }
        .sidebar-brand-text span { font-size: 11px; color: #64748b !important; }
        .sidebar-section-label {
            font-size: 11.5px; font-weight: 700; color: #0ea5e9 !important;
            text-transform: uppercase; letter-spacing: 0.6px; margin: 16px 0 8px 0;
        }

        /* ---- Stat / Metric Cards ---- */
        .stat-card {
            background: #ffffff; border: 1px solid #e2e8f0; border-radius: 14px;
            padding: 18px 20px; box-shadow: 0 4px 14px rgba(30,41,59,0.06);
            position: relative; overflow: hidden;
        }
        .stat-card .stat-icon { font-size: 22px; margin-bottom: 6px; }
        .stat-card .stat-value { font-size: 26px; font-weight: 800; color: #0f172a !important; }
        .stat-card .stat-label { font-size: 12px; color: #64748b !important; font-weight: 600; }
        .stat-card .stat-delta { font-size: 11.5px; font-weight: 700; margin-top: 4px; }
        .stat-card .stat-delta.up { color: #dc2626 !important; }
        .stat-card .stat-delta.down { color: #16a34a !important; }
        .stat-card.accent-red { border-left: 4px solid #ef4444; }
        .stat-card.accent-amber { border-left: 4px solid #f59e0b; }
        .stat-card.accent-green { border-left: 4px solid #22c55e; }
        .stat-card.accent-blue { border-left: 4px solid #0ea5e9; }

        /* ---- Zone Badge ---- */
        .zone-badge {
            display: inline-block; padding: 3px 10px; border-radius: 999px;
            font-size: 11px; font-weight: 700;
        }
        .zone-badge.merah { background: #fee2e2; color: #b91c1c !important; }
        .zone-badge.kuning { background: #fef3c7; color: #b45309 !important; }
        .zone-badge.hijau { background: #dcfce7; color: #15803d !important; }

        /* ---- Buttons ---- */
        .stButton > button {
            background: linear-gradient(135deg, #0ea5e9, #1e3a8a);
            color: #ffffff !important; border: none; border-radius: 10px;
            padding: 0.6rem 1.2rem; font-weight: 600; font-size: 14.5px;
            box-shadow: 0 4px 12px rgba(14, 165, 233, 0.35);
            width: 100%;
        }
        .stButton > button:hover { transform: translateY(-1px); color: #ffffff !important; }
        .stDownloadButton > button {
            background: #ffffff; color: #0f172a !important; border: 1.5px solid #0f172a;
            border-radius: 10px; font-weight: 600; width: 100%;
        }
        .stDownloadButton > button:hover { background: #0f172a; color: #ffffff !important; }

        /* ---- Tabs ---- */
        .stTabs [data-baseweb="tab-list"] {
            gap: 4px; background-color: #e2e8f0; padding: 4px; border-radius: 10px;
        }
        .stTabs [data-baseweb="tab"] { border-radius: 8px; color: #475569 !important; font-weight: 600; font-size: 13.5px; }
        .stTabs [aria-selected="true"] { background-color: #ffffff !important; color: #0f172a !important; }

        /* ---- Referral card (hospital/doctor) ---- */
        .referral-card {
            background: #ffffff; border: 1px solid #e2e8f0; border-radius: 14px;
            padding: 16px 18px; margin-bottom: 12px; display: flex; gap: 14px; align-items: flex-start;
            box-shadow: 0 3px 10px rgba(30,41,59,0.05);
        }
        .referral-avatar {
            width: 50px; height: 50px; border-radius: 50%;
            background: linear-gradient(135deg, #dbeafe, #e0f2fe);
            display: flex; align-items: center; justify-content: center; font-size: 24px; flex-shrink: 0;
        }
        .referral-name { font-weight: 700; font-size: 14.5px; color: #0f172a !important; }
        .referral-sub { font-size: 12px; color: #0ea5e9 !important; font-weight: 600; margin-bottom: 4px; }
        .referral-meta { font-size: 12px; color: #64748b !important; line-height: 1.6; }
        .action-link {
            display: inline-block; margin-top: 8px; margin-right: 8px;
            padding: 5px 12px; border-radius: 8px; font-size: 12px; font-weight: 700;
            text-decoration: none !important;
        }
        .action-call { background: #e0f2fe; color: #0369a1 !important; }
        .action-wa { background: #dcfce7; color: #15803d !important; }

        /* ---- Learning / Journey Step ---- */
        .journey-step {
            display: flex; gap: 14px; padding: 14px 0; border-bottom: 1px dashed #e2e8f0;
        }
        .journey-step:last-child { border-bottom: none; }
        .journey-number {
            width: 32px; height: 32px; border-radius: 50%; flex-shrink: 0;
            background: linear-gradient(135deg, #0ea5e9, #1e3a8a); color: #fff !important;
            display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 13px;
        }
        .journey-title { font-weight: 700; font-size: 14px; color: #0f172a !important; margin-bottom: 2px; }
        .journey-desc { font-size: 12.5px; color: #475569 !important; line-height: 1.6; }

        /* ---- Quiz feedback bubble ---- */
        .quiz-feedback {
            border-radius: 12px; padding: 12px 16px; font-size: 13px; margin-top: 8px; line-height: 1.6;
        }
        .quiz-feedback.correct { background: #f0fdf4; border-left: 4px solid #22c55e; color: #15803d !important; }
        .quiz-feedback.incorrect { background: #fef2f2; border-left: 4px solid #ef4444; color: #b91c1c !important; }

        .privacy-note {
            background: #f0f9ff; border: 1px solid #bae6fd; border-radius: 10px;
            padding: 8px 12px; font-size: 11.5px; color: #0c4a6e !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_page_header(title: str, subtitle: str, badges: list[str] | None = None, icon: str = "🩺"):
    badges = badges or []
    badge_html = "".join(f'<span class="header-badge">{b}</span>' for b in badges)
    st.markdown(
        f"""
        <div class="clinical-header">
            <h1>{icon} {title}</h1>
            <p>{subtitle}</p>
            <div class="badge-row">{badge_html}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar_brand():
    st.markdown(
        """
        <div class="sidebar-brand">
            <div class="sidebar-brand-icon">🧬</div>
            <div class="sidebar-brand-text">
                <b>SputumAI</b><br><span>End-to-End TB Platform</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_stat_card(icon: str, value: str, label: str, delta: str = "", delta_dir: str = "", accent: str = "blue"):
    delta_html = f'<div class="stat-delta {delta_dir}">{delta}</div>' if delta else ""
    st.markdown(
        f"""
        <div class="stat-card accent-{accent}">
            <div class="stat-icon">{icon}</div>
            <div class="stat-value">{value}</div>
            <div class="stat-label">{label}</div>
            {delta_html}
        </div>
        """,
        unsafe_allow_html=True,
    )
