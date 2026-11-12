import random

import requests
import streamlit as st

# ---------- Konfigurasi ----------
BASE_URL = "https://ghibliapi.dev"


def ke_int(teks):
    """'1,000' -> 1000, '124' -> 124. Kembalikan None jika bukan angka ('', 'NA', None)."""
    try:
        return int(str(teks).replace(",", "").strip())
    except ValueError:
        return None


# ---------- Bagian 1: Mengambil data dari API ----------
def ambil_semua_film():
    """GET https://ghibliapi.dev/films -> list berisi 25 film (dict). None jika gagal."""
    # TODO 1: Ambil semua film dari API (pola sama seperti contoh PokeAPI di modul).
    # 1. Buat url: f"{BASE_URL}/films"  ->  https://ghibliapi.dev/films
    # 2. Kirim request: response = requests.get(url)
    # 3. Jika response.status_code == 200, kembalikan response.json() (hasilnya list berisi dict film).
    # 4. Selain itu, kembalikan None.
    url = f"{BASE_URL}/films"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None


def ambil_detail_film(id_film):
    """GET https://ghibliapi.dev/films/{id_film} -> 1 film (dict). None jika gagal / tidak ditemukan.
    Catatan: id yang salah tetap dibalas status 200, tetapi isinya {"status": 404}."""
    # TODO 2: Ambil 1 film berdasarkan id_film.
    # 1. Buat url: f"{BASE_URL}/films/{id_film}"
    # 2. Kirim request dengan requests.get(url).
    # 3. Jika status_code == 200, ubah ke JSON: data = response.json()
    #    PERHATIAN: id yang salah tetap dibalas status 200, tetapi isinya {"status": 404}.
    #    Jadi jika key "status" ada di data ("status" in data), kembalikan None.
    #    Jika tidak ada, kembalikan data (dict film).
    # 4. Jika status_code bukan 200, kembalikan None.
    url = f"{BASE_URL}/films/{id_film}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if "status" in data:
            return None
        return data
    return None


# ---------- Bagian 2: Mengolah JSON menjadi dict ----------
def ringkas_film(film):
    """Ambil field yang ditampilkan dari 1 film (dict JSON); angka (string) diubah menjadi int."""
    # TODO 3: Kembalikan dict dengan key berikut (kiri) dari field API (kanan):
    # id <- id, judul <- title, judul_asli <- original_title, judul_romaji <- original_title_romanised,
    # sutradara <- director, produser <- producer, tahun <- release_date, durasi <- running_time,
    # rt_score <- rt_score, poster <- image, banner <- movie_banner, sinopsis <- description.
    # tahun, durasi, dan rt_score dikirim API sebagai string: ubah ke int memakai ke_int().
    return {
        "id": film["id"],
        "judul": film["title"],
        "judul_asli": film["original_title"],
        "judul_romaji": film["original_title_romanised"],
        "sutradara": film["director"],
        "produser": film["producer"],
        "tahun": ke_int(film["release_date"]),
        "durasi": ke_int(film["running_time"]),
        "rt_score": ke_int(film["rt_score"]),
        "poster": film["image"],
        "banner": film["movie_banner"],
        "sinopsis": film["description"],
    }


def label_rating(rt_score):
    """>= 95 'Wajib Tonton', >= 85 'Sangat Bagus', >= 70 'Bagus', selain itu 'Biasa Saja'."""
    # TODO 4: Kembalikan label sesuai rt_score (int) memakai if / elif / else:
    # >= 95 'Wajib Tonton', >= 85 'Sangat Bagus', >= 70 'Bagus', selain itu 'Biasa Saja'.
    if rt_score >= 95:
        return "Wajib Nonton"
    elif rt_score >= 85:
        return "Sangat Bagus"
    elif rt_score >= 70:
        return "Bagus"
    else:
        return "Biasa Saja"


# ---------- Bagian 3: Rekomendasi ----------
def filter_film(daftar, sutradara, rt_min, tahun_min, tahun_max):
    """Film yang sutradaranya cocok ('Semua' = semua sutradara), rt_score >= rt_min,
    dan tahun_min <= tahun <= tahun_max."""
    # TODO 5: Buat list kosong hasil, lalu periksa setiap film di daftar.
    # Film dimasukkan ke hasil (append) jika memenuhi KETIGA syarat:
    #   - sutradara == "Semua", ATAU film["sutradara"] sama dengan sutradara
    #   - film["rt_score"] >= rt_min
    #   - tahun_min <= film["tahun"] <= tahun_max
    # Kembalikan hasil.
    hasil = []
    for film in daftar:
        if (sutradara == "Semua" or film["sutradara"] == sutradara) \
                and film["rt_score"] >= rt_min \
                and tahun_min <= film["tahun"] <= tahun_max:
            hasil.append(film)
    return hasil


def rekomendasi_acak(kandidat, id_sebelumnya):
    """Pilih 1 film acak dari kandidat, selain film dengan id id_sebelumnya
    (kecuali hanya film itu satu-satunya kandidat). None jika kandidat kosong."""
    # TODO 6: Pilih 1 film secara acak.
    # 1. Jika kandidat kosong (len(kandidat) == 0), kembalikan None.
    # 2. Buat list pilihan berisi film di kandidat yang film["id"]-nya TIDAK sama dengan id_sebelumnya
    #    (supaya rekomendasi tidak sama dengan sebelumnya).
    # 3. Jika pilihan kosong (kandidat cuma berisi film sebelumnya), isi pilihan = kandidat.
    # 4. Kembalikan random.choice(pilihan). random.choice(list) mengambil 1 elemen acak dari list.
    if len(kandidat) == 0:
        return None
    pilihan = [f for f in kandidat if f["id"] != id_sebelumnya]
    if len(pilihan) == 0:
        pilihan = kandidat
    return random.choice(pilihan)


# ---------- Tampilan Streamlit (tidak perlu diubah) ----------
@st.cache_data(ttl=600, show_spinner="Mengambil data dari API...")
def muat_semua_film():
    try:
        return ambil_semua_film()
    except requests.exceptions.RequestException:
        return None


@st.cache_data(ttl=600, show_spinner="Mengambil detail film...")
def muat_detail_film(id_film):
    try:
        return ambil_detail_film(id_film)
    except requests.exceptions.RequestException:
        return None


def tampilkan_film(film):
    st.image(film["banner"], width="stretch")
    col_poster, col_info = st.columns([1, 2])
    col_poster.image(film["poster"], caption=film["judul"], width="stretch")
    with col_info:
        st.header(film["judul"])
        st.caption(f"{film['judul_asli']} · {film['judul_romaji']}")
        label = label_rating(film["rt_score"])
        if label is None:
            st.warning("Selesaikan TODO 4 (label_rating) dulu.")
        else:
            st.markdown(f"**🏷️ {label}**")
        m1, m2, m3 = st.columns(3)
        m1.metric("Tahun", film["tahun"])
        m2.metric("Durasi", f"{film['durasi']} menit")
        m3.metric("RT Score", f"{film['rt_score']}%")
        st.write(f"**Sutradara**: {film['sutradara']}")
        st.write(f"**Produser**: {film['produser']}")
        st.subheader("📖 Sinopsis")
        st.write(film["sinopsis"])


def main():
    st.set_page_config(page_title="Ghibli Movie Recommender", page_icon="🎲", layout="wide")
    st.title("🎲 Ghibli Movie Recommender")
    st.caption(f"Bingung mau nonton apa? Biar aplikasi yang memilihkan. Sumber data: {BASE_URL}")

    films = muat_semua_film()
    if not films:
        st.error("Gagal mengambil data film. Cek koneksi internet atau TODO 1 (ambil_semua_film).")
        st.stop()

    daftar = [ringkas_film(f) for f in films]
    if daftar[0] is None:
        st.warning("Selesaikan TODO 3 (ringkas_film) dulu.")
        st.stop()

    # Filter di sidebar
    st.sidebar.header("🎛️ Filter")
    semua_sutradara = sorted({f["sutradara"] for f in daftar})
    sutradara = st.sidebar.selectbox("Sutradara", ["Semua"] + semua_sutradara)
    rt_min = st.sidebar.slider("RT Score minimal", 0, 100, 0, step=5)
    semua_tahun = [f["tahun"] for f in daftar]
    tahun_min, tahun_max = st.sidebar.slider(
        "Rentang tahun rilis", min(semua_tahun), max(semua_tahun), (min(semua_tahun), max(semua_tahun))
    )
    kandidat = filter_film(daftar, sutradara, rt_min, tahun_min, tahun_max)
    if kandidat is None:
        st.warning("Selesaikan TODO 5 (filter_film) dulu.")
        st.stop()
    st.sidebar.caption(f"{len(kandidat)} dari {len(daftar)} film cocok dengan filter.")

    if st.button("🎲 Rekomendasikan Film", type="primary"):
        pilih = rekomendasi_acak(kandidat, st.session_state.get("film_id"))
        if pilih is None:
            st.session_state.pop("film_id", None)
            st.warning("Tidak ada film yang cocok dengan filter (atau TODO 6 belum selesai).")
        else:
            st.session_state["film_id"] = pilih["id"]

    if "film_id" in st.session_state:
        detail = muat_detail_film(st.session_state["film_id"])
        if not detail:
            st.error("Gagal mengambil detail film. Cek TODO 2 (ambil_detail_film).")
        else:
            tampilkan_film(ringkas_film(detail))


if __name__ == "__main__":
    main()
