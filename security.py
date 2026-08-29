"""
core/security.py
=================
Modul privasi & keamanan data pasien.

Prinsip etika medis yang diterapkan:
- Nomor Rekam Medis (RM) ASLI tidak pernah disimpan dalam bentuk plain-text
  ke dalam artefak yang dapat diekspor/dibagikan (laporan, log, cache).
- Sistem menghasilkan "Anonymous Patient ID" (APID) berbasis hashing satu-arah
  (SHA-256 + salt harian) sehingga:
    a. Data pasien tidak bisa direkonstruksi dari APID (irreversible).
    b. APID tetap konsisten untuk RM yang sama dalam satu hari kerja
       (berguna untuk pelacakan sesi tanpa menyimpan identitas asli).
- RM asli hanya ditampilkan secara terbatas di UI internal (masked),
  tidak pernah dicetak penuh pada laporan yang bisa dibawa keluar sistem.
"""

import hashlib
import re
from datetime import date

# Salt harian sederhana. Pada implementasi produksi, salt WAJIB disimpan
# di secrets manager (mis. st.secrets / Vault / KMS), bukan hardcoded.
_DAILY_SALT_SEED = "SPUTUMAI-CLINICAL-SALT-2026"


def _daily_salt() -> str:
    return f"{_DAILY_SALT_SEED}-{date.today().isoformat()}"


def anonymize_id(raw_identifier: str) -> str:
    """
    Mengubah Nomor Rekam Medis asli menjadi Anonymous Patient ID (APID).
    Format keluaran: APID-XXXXXXXXXXXX (12 karakter hex dari SHA-256).
    """
    if not raw_identifier:
        raw_identifier = "UNKNOWN"
    payload = f"{raw_identifier.strip().upper()}::{_daily_salt()}"
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    return f"APID-{digest[:12].upper()}"


def mask_identifier(raw_identifier: str) -> str:
    """
    Menyamarkan RM asli untuk tampilan UI internal, contoh:
    'RM-00231458' -> 'RM-0023****'
    """
    if not raw_identifier or raw_identifier == "-":
        return "-"
    raw_identifier = raw_identifier.strip()
    if len(raw_identifier) <= 4:
        return "*" * len(raw_identifier)
    visible = raw_identifier[: max(4, len(raw_identifier) - 4)]
    hidden = "*" * (len(raw_identifier) - len(visible))
    return f"{visible}{hidden}"


def is_valid_rm_format(raw_identifier: str) -> bool:
    """Validasi ringan format nomor rekam medis (alfanumerik + tanda hubung, 4-20 char)."""
    if not raw_identifier:
        return False
    return bool(re.fullmatch(r"[A-Za-z0-9\-]{4,20}", raw_identifier.strip()))


def consent_gate(consent_given: bool) -> bool:
    """
    Gerbang persetujuan (informed consent) sebelum data citra & metadata
    diproses oleh model AI. Mengembalikan True jika pemrosesan diizinkan.
    """
    return bool(consent_given)
