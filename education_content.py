"""
data/education_content.py
==========================
Konten Pusat Edukasi TBC: panduan pencegahan, patient journey pasien baru
terdiagnosis, repositori jurnal ilmiah, dan bank soal Smart Quiz.
"""

PREVENTION_TIPS = [
    {
        "title": "Terapkan Etika Batuk",
        "desc": "Tutup mulut & hidung dengan tisu atau lengan bagian dalam saat batuk/bersin, "
                "lalu buang tisu ke tempat sampah tertutup dan cuci tangan segera.",
        "icon": "😷",
    },
    {
        "title": "Ventilasi & Sinar Matahari",
        "desc": "Buka jendela rumah setiap pagi agar sirkulasi udara baik dan sinar matahari masuk, "
                "karena kuman TBC mudah mati oleh sinar UV dan sulit bertahan di ruangan terbuka.",
        "icon": "☀️",
    },
    {
        "title": "Gunakan Masker",
        "desc": "Pasien TBC aktif disarankan menggunakan masker terutama pada 2 minggu pertama pengobatan "
                "saat risiko penularan masih tinggi.",
        "icon": "🩹",
    },
    {
        "title": "Pisahkan Alat Makan & Tidur",
        "desc": "Selama masa pengobatan awal, sebaiknya gunakan alat makan terpisah dan hindari berbagi "
                "kamar tidur dengan anggota keluarga rentan (anak-anak, lansia, ibu hamil).",
        "icon": "🍽️",
    },
    {
        "title": "Skrining Kontak Erat",
        "desc": "Anggota keluarga serumah dan kontak erat lainnya perlu diperiksa untuk deteksi dini "
                "penularan, termasuk pemeriksaan TCM/foto rontgen bila diperlukan.",
        "icon": "👨‍👩‍👧‍👦",
    },
    {
        "title": "Nutrisi Seimbang",
        "desc": "Konsumsi makanan bergizi tinggi protein untuk mendukung sistem imun tubuh melawan infeksi "
                "dan mempercepat proses penyembuhan.",
        "icon": "🥗",
    },
]

PATIENT_JOURNEY = [
    {
        "title": "Diagnosis & Konfirmasi",
        "desc": "Setelah hasil pemeriksaan dahak (mikroskopis/TCM) menunjukkan positif, dokter akan "
                "melakukan pemeriksaan klinis lanjutan untuk menentukan klasifikasi dan rejimen pengobatan.",
    },
    {
        "title": "Registrasi Program TBC Nasional",
        "desc": "Pasien didaftarkan ke dalam Sistem Informasi TBC (SITB) Kemenkes untuk pemantauan "
                "pengobatan terstandar dan mendapatkan akses Obat Anti Tuberkulosis (OAT) gratis.",
    },
    {
        "title": "Fase Intensif (2 Bulan Pertama)",
        "desc": "Minum OAT setiap hari secara teratur di bawah pengawasan Pengawas Menelan Obat (PMO), "
                "biasanya anggota keluarga terdekat, untuk memastikan kepatuhan pengobatan.",
    },
    {
        "title": "Evaluasi Tengah Pengobatan",
        "desc": "Pemeriksaan dahak ulang pada akhir bulan ke-2 untuk menilai respons pengobatan sebelum "
                "melanjutkan ke fase lanjutan.",
    },
    {
        "title": "Fase Lanjutan (4 Bulan Berikutnya)",
        "desc": "Dosis obat disesuaikan dan diminum lebih jarang namun tetap wajib teratur hingga masa "
                "pengobatan total 6 bulan selesai.",
    },
    {
        "title": "Evaluasi Akhir & Dinyatakan Sembuh",
        "desc": "Pemeriksaan dahak akhir pengobatan menentukan status sembuh. Pasien tetap disarankan "
                "kontrol berkala untuk memantau potensi kekambuhan.",
    },
]

# Repositori tautan jurnal ilmiah — judul & sumber ditampilkan sebagai referensi,
# tautan mengarah ke halaman resmi jurnal/organisasi (bukan reproduksi isi artikel).
JOURNAL_REPOSITORY = [
    {
        "title": "WHO Global Tuberculosis Report",
        "source": "World Health Organization",
        "url": "https://www.who.int/teams/global-tuberculosis-programme/tb-reports",
        "desc": "Laporan tahunan global mengenai beban penyakit TBC, capaian pengobatan, dan strategi eliminasi.",
    },
    {
        "title": "Profil & Data Program Penanggulangan TBC",
        "source": "Kementerian Kesehatan RI",
        "url": "https://tbindonesia.or.id/",
        "desc": "Portal data & sumber daya resmi program penanggulangan TBC nasional Indonesia.",
    },
    {
        "title": "The Lancet Respiratory Medicine — Tuberculosis Collection",
        "source": "The Lancet",
        "url": "https://www.thelancet.com/journals/lanres/home",
        "desc": "Kumpulan publikasi ilmiah terbaru mengenai diagnosis, tata laksana, dan riset TBC.",
    },
    {
        "title": "International Journal of Tuberculosis and Lung Disease",
        "source": "IUATLD",
        "url": "https://www.theunion.org/what-we-do/journals/ijtld",
        "desc": "Jurnal resmi The Union yang menjadi rujukan skala semi-kuantitatif BTA (IUATLD scale).",
    },
    {
        "title": "PLOS ONE — Tuberculosis Research",
        "source": "PLOS",
        "url": "https://journals.plos.org/plosone/",
        "desc": "Publikasi akses terbuka terkait penelitian epidemiologi dan teknologi deteksi TBC berbasis AI.",
    },
]

# Bank soal Smart Quiz: setiap soal punya opsi, indeks jawaban benar, dan feedback edukatif.
QUIZ_BANK = [
    {
        "question": "Apa penyebab utama penyakit Tuberkulosis (TBC)?",
        "options": ["Virus Influenza", "Bakteri Mycobacterium tuberculosis", "Jamur Candida", "Parasit malaria"],
        "answer_index": 1,
        "feedback_correct": "Tepat! TBC disebabkan oleh bakteri *Mycobacterium tuberculosis* yang menyerang paru-paru.",
        "feedback_incorrect": "Belum tepat. TBC disebabkan oleh bakteri Mycobacterium tuberculosis, bukan virus, jamur, atau parasit.",
    },
    {
        "question": "Berapa lama umumnya durasi pengobatan TBC standar (kategori 1)?",
        "options": ["1 minggu", "1 bulan", "6 bulan", "2 tahun"],
        "answer_index": 2,
        "feedback_correct": "Benar! Pengobatan TBC standar berlangsung sekitar 6 bulan (2 bulan fase intensif + 4 bulan fase lanjutan).",
        "feedback_incorrect": "Kurang tepat. Pengobatan TBC standar umumnya berlangsung 6 bulan agar bakteri benar-benar tuntas dan mencegah resistensi obat.",
    },
    {
        "question": "Bagaimana cara utama penularan TBC antar manusia?",
        "options": ["Melalui percikan dahak (droplet) saat batuk/bersin", "Melalui gigitan nyamuk", "Melalui makanan basi", "Melalui sentuhan kulit"],
        "answer_index": 0,
        "feedback_correct": "Tepat sekali! TBC menular lewat droplet pernapasan saat penderita batuk, bersin, atau berbicara.",
        "feedback_incorrect": "Belum tepat. TBC menular lewat udara (droplet) dari batuk/bersin penderita, bukan gigitan serangga atau makanan.",
    },
    {
        "question": "Apa risiko utama jika pasien TBC berhenti minum obat sebelum waktunya?",
        "options": ["Tidak ada risiko", "Rambut rontok", "Resistensi obat (TBC-MDR)", "Alergi kulit"],
        "answer_index": 2,
        "feedback_correct": "Benar! Penghentian obat sebelum tuntas berisiko memicu TBC resisten obat (MDR-TB) yang jauh lebih sulit diobati.",
        "feedback_incorrect": "Kurang tepat. Risiko terbesarnya adalah resistensi obat (TBC-MDR), yang membuat pengobatan jauh lebih lama dan kompleks.",
    },
    {
        "question": "Apa langkah pertama yang disarankan bila hasil skrining AI menunjukkan kategori 'Scanty'?",
        "options": ["Mengabaikan hasil karena jumlahnya sedikit", "Konfirmasi laboratorium lanjutan (mis. TCM/GeneXpert)", "Langsung operasi paru", "Vaksinasi ulang BCG"],
        "answer_index": 1,
        "feedback_correct": "Tepat! Hasil Scanty perlu dikonfirmasi dengan pemeriksaan lanjutan seperti TCM/GeneXpert sebelum diagnosis final.",
        "feedback_incorrect": "Belum tepat. Hasil Scanty tetap perlu ditindaklanjuti dengan konfirmasi laboratorium lanjutan, tidak boleh diabaikan.",
    },
]
