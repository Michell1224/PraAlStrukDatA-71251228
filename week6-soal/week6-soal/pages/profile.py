import streamlit as st
from user import user_data_by_username

# CEK APAKAH SUDAH LOGIN
if "logged_in" not in st.session_state or not st.session_state.logged_in == True:
    st.switch_page("app.py")
    
user = user_data_by_username()

# hint untuk mematikan text input ada di -> https://docs.streamlit.io/develop/api-reference/widgets/st.text_input
# BUAT 2 INPUT TEXT 1 Username 1 Password namun disable/matikan field Username dan yang password harus tipe password
st.title("Profile")
username = st.text_input(
    label ="Username",
    value = st.session_state.username,
    disabled = True
)
password_baru = st.text_input(
    label = "Password baru",
    type="password"
)

# Silahkan kalau mau baca baca ini hehe ga wajib ya-> https://discuss.streamlit.io/t/buttons-alignment/51929
col1, space, col2 = st.columns([1,3,1])
with col1:
    # Buat tombol logout st.button("logout", type="primary") keluar ke app.py
    if st.button("Logout", type = "primary"):
        st.session_state.logged_in = False
        st.session_state.username = "" 
        st.session_state.password = "" 
        st.session_state.role = "" 
        st.switch_page("app.py")
        
with col2:
    pass
    # Ini untuk ubah password st.button("Ganti Data", type="secondary", width=400)
    if st.button(
        "Ganti data",
        type = "secondary",
        width = 400
    ):
        if password_baru == st.session_state.password:
            st.erroe("gaboleh sama wok")
        else:
            st.session_state.password = password_baru
            user[st.session_state.username]["Password"]= password_baru
            st.success("Berhasil")
    # Kondisi -> Password baru dan lama ga boleh sama 
    # Jika sama -> st.error("ga boleh sama wok")
    # jika beda ubah melalui variabel 'user' lalu tampilkan st.success("Berhasil")
    st.divider()
    if st.button("kembali"):
        if user["role"]== "Admin:":
            st.switch_page("pages/dasboard.py")
        else:
            st.switch_page("pages/dasboard.py")
