"""
pages/4_Education_Center.py
=============================
Pusat Edukasi & Interactive Learning TBC: pencegahan, patient journey,
repositori jurnal medis, dan Smart Quiz dengan umpan balik edukatif
bergaya chatbot sederhana (rule-based, bukan LLM eksternal).
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st

from core.styling import inject_global_css, render_page_header, render_sidebar_brand
from data.education_content import PREVENTION_TIPS, PATIENT_JOURNEY, JOURNAL_REPOSITORY, QUIZ_BANK

st.set_page_config(page_title="Pusat Edukasi TBC | SputumAI", page_icon="📚", layout="wide")
inject_global_css()

with st.sidebar:
    render_sidebar_brand()
    st.markdown('<div class="sidebar-section-label">Progres Belajar</div>', unsafe_allow_html=True)
    quiz_score = st.session_state.get("quiz_score")
    quiz_total = st.session_state.get("quiz_total")
    if quiz_score is not None:
        st.markdown(
            f'<div class="privacy-note">🏆 Skor Smart Quiz terakhir: <b>{quiz_score}/{quiz_total}</b></div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown('<div class="privacy-note">📘 Selesaikan Smart Quiz untuk melihat skor Anda di sini.</div>', unsafe_allow_html=True)

render_page_header(
    "Pusat Edukasi TBC",
    "Modul edukasi interaktif: pencegahan penularan, panduan pasien baru terdiagnosis, repositori jurnal, dan kuis kesehatan.",
    badges=["📖 4 Modul", "🧠 Smart Quiz", "🔬 Rujukan Ilmiah"],
    icon="📚",
)

tab_prevent, tab_journey, tab_journal, tab_quiz = st.tabs(
    ["🛡️ Pencegahan Penularan", "🧭 Patient Journey", "📑 Repositori Jurnal", "🧠 Smart Quiz"]
)

# ============================================================================
# TAB 1: PENCEGAHAN PENULARAN
# ============================================================================
with tab_prevent:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">🛡️ Cara Mencegah Penularan TBC di Rumah & Lingkungan Sosial</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-subtitle">Praktik sederhana namun terbukti efektif menurunkan risiko penularan</div>', unsafe_allow_html=True)

    cols = st.columns(3)
    for i, tip in enumerate(PREVENTION_TIPS):
        with cols[i % 3]:
            st.markdown(
                f"""
                <div class="stat-card accent-blue" style="min-height:190px; margin-bottom:14px;">
                    <div class="stat-icon">{tip['icon']}</div>
                    <div style="font-weight:700; font-size:14px; color:#0f172a; margin-bottom:6px;">{tip['title']}</div>
                    <div style="font-size:12.5px; color:#475569; line-height:1.6;">{tip['desc']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================================
# TAB 2: PATIENT JOURNEY
# ============================================================================
with tab_journey:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">🧭 Panduan Langkah demi Langkah Pasien Baru Terdiagnosis TBC</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-subtitle">Perjalanan pengobatan standar selama 6 bulan program TBC Nasional</div>', unsafe_allow_html=True)

    for i, step in enumerate(PATIENT_JOURNEY, start=1):
        st.markdown(
            f"""
            <div class="journey-step">
                <div class="journey-number">{i}</div>
                <div>
                    <div class="journey-title">{step['title']}</div>
                    <div class="journey-desc">{step['desc']}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.info("💡 Pedoman ini bersifat edukatif umum. Rejimen dan durasi pengobatan aktual ditentukan oleh dokter berdasarkan kondisi klinis masing-masing pasien.")
    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================================
# TAB 3: REPOSITORI JURNAL
# ============================================================================
with tab_journal:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">📑 Repositori Jurnal & Sumber Ilmiah TBC</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-subtitle">Tautan resmi menuju publikasi dan organisasi kesehatan terpercaya</div>', unsafe_allow_html=True)

    for j in JOURNAL_REPOSITORY:
        st.markdown(
            f"""
            <div class="referral-card">
                <div class="referral-avatar">📄</div>
                <div style="flex:1;">
                    <div class="referral-name">{j['title']}</div>
                    <div class="referral-sub">{j['source']}</div>
                    <div class="referral-meta">{j['desc']}</div>
                    <a class="action-link action-call" href="{j['url']}" target="_blank">🔗 Buka Sumber</a>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================================
# TAB 4: SMART QUIZ (rule-based feedback, gaya chatbot edukatif)
# ============================================================================
with tab_quiz:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">🧠 Smart Quiz — Uji Pemahaman Anda tentang TBC</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-subtitle">Jawab seluruh pertanyaan, sistem akan memberi umpan balik edukatif secara otomatis</div>', unsafe_allow_html=True)

    if "quiz_answers" not in st.session_state:
        st.session_state.quiz_answers = [None] * len(QUIZ_BANK)
    if "quiz_submitted" not in st.session_state:
        st.session_state.quiz_submitted = False

    with st.form("smart_quiz_form"):
        for idx, q in enumerate(QUIZ_BANK):
            st.markdown(f"**{idx + 1}. {q['question']}**")
            choice = st.radio(
                f"quiz_q_{idx}", q["options"], index=None,
                key=f"quiz_radio_{idx}", label_visibility="collapsed",
            )
            st.session_state.quiz_answers[idx] = choice
            st.markdown("<br>", unsafe_allow_html=True)

        submitted = st.form_submit_button("✅ Kumpulkan Jawaban & Lihat Hasil", use_container_width=True)

    if submitted:
        st.session_state.quiz_submitted = True

    if st.session_state.quiz_submitted:
        unanswered = sum(1 for a in st.session_state.quiz_answers if a is None)
        if unanswered > 0:
            st.warning(f"⚠️ Masih ada {unanswered} pertanyaan yang belum dijawab. Silakan lengkapi lalu kumpulkan kembali.")
        else:
            score = 0
            st.markdown("#### 🤖 Umpan Balik Edukatif")
            for idx, q in enumerate(QUIZ_BANK):
                user_choice = st.session_state.quiz_answers[idx]
                correct_option = q["options"][q["answer_index"]]
                is_correct = user_choice == correct_option
                if is_correct:
                    score += 1

                feedback_class = "correct" if is_correct else "incorrect"
                feedback_text = q["feedback_correct"] if is_correct else q["feedback_incorrect"]
                icon = "✅" if is_correct else "❌"
                st.markdown(f"**{idx + 1}. {q['question']}**")
                st.markdown(
                    f"""
                    <div class="quiz-feedback {feedback_class}">
                        {icon} <b>Jawaban Anda:</b> {user_choice}<br>
                        🤖 <b>SputumAI Tutor:</b> {feedback_text}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.markdown("<br>", unsafe_allow_html=True)

            st.session_state.quiz_score = score
            st.session_state.quiz_total = len(QUIZ_BANK)

            percentage = (score / len(QUIZ_BANK)) * 100
            if percentage >= 80:
                grade_msg, grade_color = "Pemahaman Sangat Baik! 🎉", "accent-green"
            elif percentage >= 50:
                grade_msg, grade_color = "Pemahaman Cukup Baik, Terus Belajar! 👍", "accent-amber"
            else:
                grade_msg, grade_color = "Perlu Belajar Lebih Lanjut. Yuk baca modul di tab lain! 📖", "accent-red"

            st.markdown(
                f"""
                <div class="stat-card {grade_color}">
                    <div class="stat-value">{score} / {len(QUIZ_BANK)}</div>
                    <div class="stat-label">{grade_msg}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            if st.button("🔄 Ulangi Kuis", use_container_width=True):
                st.session_state.quiz_answers = [None] * len(QUIZ_BANK)
                st.session_state.quiz_submitted = False
                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
