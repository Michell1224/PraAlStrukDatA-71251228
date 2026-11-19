
Soal 1: Dashboard Katalog Buku (Web Scraping & Konversi Mata Uang)

Deskripsi Kasus:
Buatlah sebuah aplikasi dashboard interaktif berbasis web menggunakan Streamlit untuk menganalisis katalog buku daring dan mengonversi harganya ke dalam mata uang Rupiah (IDR) secara langsung (real-time).
Instruksi Pengerjaan:
1. Antarmuka Pengguna (UI):
	• Atur konfigurasi halaman dengan judul "Dashboard Katalog Buku" dan tata letak lebar (layout="wide").
	• Buat komponen st.slider untuk memilih jumlah halaman katalog yang akan diambil dengan rentang nilai 1 sampai 3 (nilai default 2).
	• Sediakan tombol aksi utama (type="primary") bertuliskan "Ambil Data dan Tampilkan Dashboard" untuk memulai proses pengambilan data.
2. Web Scraping:
	• Lakukan scraping dari situs https://toscrape.com{halaman}.html sesuai jumlah halaman yang dipilih pada slider.
	• Ekstrak atribut dari setiap buku (article.product_pod), meliputi judul buku, harga dalam GBP (bersihkan simbol mata uang dan ubah ke tipe float), rating (konversi teks "One"–"Five" menjadi angka 1–5), dan status ketersediaan.
3. Integrasi REST API & Pengolahan Data:
	• Ambil nilai kurs terbaru GBP ke IDR menggunakan API https://frankfurter.dev.
	• Simpan seluruh data ke dalam Pandas DataFrame dan tambahkan kolom baru harga_idr hasil perkalian harga GBP dengan kurs terbaru.
	• Tampilkan informasi jumlah buku yang berhasil diambil beserta tabel datanya menggunakan st.dataframe.
4. Visualisasi Data:
	• Buat dua kolom berdampingan (st.columns(2)) menggunakan library Matplotlib:
		• Kolom 1: Grafik Histogram untuk menampilkan distribusi harga buku dalam Rupiah (bins=10).
		• Kolom 2: Grafik Bar Chart untuk menampilkan jumlah buku berdasarkan masing-masing kategori rating (1 sampai 5).
