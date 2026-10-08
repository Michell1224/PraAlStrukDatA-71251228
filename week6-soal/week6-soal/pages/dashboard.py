import streamlit as st
from user import user_data_by_username

st.set_page_config(page_title="DwTix - Dashboard")

# cek apakah sudah login -> JIKA BELUM ALIHKAN KE app.py
if "logged_in" not in st.session_state or not st.session_state.logged_in == True:
    st.switch_page("app.py")

# JANGAN PERNAH RAGU UNTUK CEK DATA PAKAI st.write() ya dari pada ngawang
data = user_data_by_username()
# ambil role yang login dari data
# role = ??
username = st.session_state.username
role = data[username]["role"]

# JIKA YANG LOGIN PESERTA -> ALIHKAN KE PAGE EVENT
if role == "Peserta":
    st.switch_page("pages/event.py")

st.title(f"Welcome, {role} 👋")

# JIKA YANG LOGIN ADMIN TAMPILKAN SELURUH DATA TERSERAH MAU BENTUKNYA APAPUN st.table, st.write boleh aja
st.subheader("Data Seluruh Pengguna")
st.table(data)
st.diver()
st.subheader("Informasi Admin")
st.write(f"Username sedang login:**{username}**")
st.write(f"role: **{role}")