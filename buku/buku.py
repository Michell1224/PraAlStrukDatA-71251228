from bs4 import BeautifulSoup
import streamlit as st
import pandas as pd
import json
import matplotlib.pyplot as plt
import requests

RATING_MAP = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
}

BASE_URL = "https://books.toscrape.com/catalogue/page-{halaman}.html"
KURS_URL = "https://api.frankfurter.dev/v1/latest?base=GBP&symbols=IDR"

st.set_page_config(page_title="Dashboard Katalog Buku", layout="wide")
st.title("Dashboard Katalog Buku")
st.write("Mengambil data buku melalui web scraping dan kurs GBP/IDR melalui REST API.")

jumlah_halaman = st.slider("Jumlah halaman katalog yang diambil", 1, 3, 2)


def scrape_buku(jumlah_halaman):
    data = []
    for halaman in range(1, jumlah_halaman + 1):
        response = requests.get(BASE_URL.format(halaman=halaman), timeout=15)
        response.raise_for_status()
        response.encoding = "utf-8"
        soup = BeautifulSoup(response.text, "html.parser")

        for buku in soup.select("article.product_pod"):
            judul = buku.h3.a["title"]

            # Bersihkan simbol mata uang (mis. "£51.77") lalu ubah ke float
            teks_harga = buku.select_one("p.price_color").get_text(strip=True)
            harga_gbp = float(teks_harga.replace("£", ""))

            # Konversi teks rating ("One"-"Five") menjadi angka 1-5
            kelas_rating = buku.select_one("p.star-rating")["class"]
            rating = next(
                (RATING_MAP[k] for k in kelas_rating if k in RATING_MAP), None
            )

            ketersediaan = buku.select_one("p.availability").get_text(strip=True)

            data.append(
                {
                    "judul": judul,
                    "harga_gbp": harga_gbp,
                    "rating": rating,
                    "ketersediaan": ketersediaan,
                }
            )
    return data


def ambil_kurs_gbp_idr():
    response = requests.get(KURS_URL, timeout=15)
    response.raise_for_status()
    return response.json()["rates"]["IDR"]


if st.button("Ambil Data dan Tampilkan Dashboard", type="primary"):
    try:
        with st.spinner("Mengambil data..."):
            data_buku = scrape_buku(jumlah_halaman)
            kurs = ambil_kurs_gbp_idr()
    except (requests.RequestException, KeyError, ValueError) as e:
        st.error(f"Gagal mengambil data: {e}")
        st.stop()

    df = pd.DataFrame(data_buku)
    df["harga_idr"] = df["harga_gbp"] * kurs

    st.subheader("Data Katalog Buku")
    st.caption(f"{len(df)} buku diambil dari {jumlah_halaman} halaman.")
    st.dataframe(df, use_container_width=True)

    st.subheader("Visualisasi")
    col1, col2 = st.columns(2)

    with col1:
        fig1, ax1 = plt.subplots()
        ax1.hist(df["harga_idr"], bins=10, edgecolor="black")
        ax1.set_title("Distribusi Harga Buku")
        ax1.set_xlabel("Harga (Rupiah)")
        ax1.set_ylabel("Jumlah Buku")
        ax1.grid(axis="y", alpha=0.3)
        st.pyplot(fig1)

    with col2:
        jumlah_per_rating = (
            df["rating"].value_counts().reindex([1, 2, 3, 4, 5], fill_value=0)
        )
        fig2, ax2 = plt.subplots()
        ax2.bar(jumlah_per_rating.index, jumlah_per_rating.values)
        ax2.set_title("Jumlah Buku Berdasarkan Rating")
        ax2.set_xlabel("Rating")
        ax2.set_ylabel("Jumlah Buku")
        ax2.set_xticks([1, 2, 3, 4, 5])
        ax2.grid(axis="y", alpha=0.3)
        st.pyplot(fig2)