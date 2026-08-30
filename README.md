# SputumAI Workspace — End-to-End Tuberculosis Platform

Platform kesehatan komprehensif untuk deteksi, edukasi, dan penanggulangan TBC
berbasis AI (YOLOv8), dibangun dengan Streamlit multipage app.

## Menjalankan aplikasi
```bash
pip install -r requirements.txt
# letakkan file model YOLOv8 terlatih sebagai best.pt di root folder ini
streamlit run app.py
```

## Struktur
- `app.py` — landing page & hub navigasi
- `pages/` — 4 modul utama (Diagnostic Workspace, Epidemiology Dashboard,
  Smart Referral Map, Education Center) — otomatis terdeteksi Streamlit
  sebagai multipage app.
- `core/` — logic layer bersama (security/anonymization, styling, inference, pdf)
- `data/` — data layer (epidemiologi, fasilitas rujukan, konten edukasi)

## Catatan produksi
- Data epidemiologi & fasilitas rujukan pada `data/` bersifat ILUSTRATIF
  untuk demo. Ganti dengan sumber resmi (API Kemenkes/SATUSEHAT) sebelum
  produksi/komersialisasi — lihat komentar TODO pada masing-masing file.
- Salt anonimisasi (`core/security.py`) harus dipindah ke secrets manager
  (`st.secrets`, Vault, atau KMS) pada environment produksi.
