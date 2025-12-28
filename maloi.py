import streamlit as st
from datetime import datetime

# 1. CAU HINH HE THONG
st.set_page_config(page_title="BA DUY TECH PRO 2025", layout="wide")

if 'auth' not in st.session_state: 
    st.session_state['auth'] = None

DANH_SACH_KHACH_HANG = {
    "PRO-DUY-2025": {"ten": "Ky su Ba Duy", "loai": "Pro", "han": "2026-01-05"},
    "DUY-FREE-3D": {"ten": "Khach dung thu", "loai": "Trial", "han": "2025-12-30"},
}

# --- MAN HINH DANG NHAP ---
if st.session_state['auth'] is None:
    st.title("🔐 HE THONG KY THUAT BA DUY")
    ma = st.text_input("Nhap ma kich hoat:", type="password").strip()
    if st.button("XAC NHAN VAO"):
        if ma in DANH_SACH_KHACH_HANG:
            st.session_state['auth'] = DANH_SACH_KHACH_HANG[ma]
            st.rerun()
        else: 
            st.error("Ma khong dung!")
    st.stop()

# --- SIDEBAR MENU ---
user = st.session_state['auth']
with st.sidebar:
    st.header(f"👤 {user['ten']}")
    menu = st.radio("MENU CHINH", ["Tra ma loi", "Chan doan nhanh", "Gia han"])
    st.divider()
    if st.button("Dang xuat"):
        st.session_state['auth'] = None
        st.rerun()

# --- KHO DU LIEU MA LOI ---
DATA_LOI = {
    "Dieu Hoa": {
        "Panasonic": {
            "11H": "Loi duong truyen tin hieu giua dan lanh va dan nong.",
            "12H": "Loi khac biet cong suat giua dan lanh va dan nong.",
            "15H": "Loi cam bien nhiet do may nen (dau day).",
            "16H": "Dong tai may nen qua thap (thieu gas hoac hong block).",
            "19H": "Loi quat dan lanh (quat khong quay hoac hong hall).",
            "91F": "Dong tai may nen qua thap.",
            "93F": "Loi toc do quay may nen (bat thuong xung).",
            "95F": "Nhiet do dan nong qua cao.",
            "97F": "Nhiet do may nen qua cao.",
            "E6": "Loi truyen tin hieu giua dan lanh va dan nong.",
        },
        "Daikin": {
            "A1": "Loi bo mach dan lanh.",
            "A6": "Loi motor quat dan lanh (qua tai/hong).",
            "E1": "Loi bo mach dan nong.",
            "E5": "Loi dong co may nen Inverter (ket/ro dien).",
            "E7": "Loi motor quat dan nong.",
            "F3": "Nhiet do duong ong day bat thuong.",
            "U0": "Canh bao thieu gas hoac nghet duong ong.",
            "U4": "Loi duong truyen tin hieu giua dan nong va dan lanh.",
            "L5": "Loi may nen bien tan (qua dong dau ra).",
        }
    },
    "Bep Tu": {
        "Sunhouse": {"E0": "Khong nhan noi.", "E1": "Qua nhiet.", "E2": "Dien ap cao."},
        "Kangaroo": {"E1": "Loi cam bien kinh.", "E2": "Qua nhiet IGBT."}
    }
}

# --- XU LY NOI DUNG ---
if menu == "Tra ma loi":
    st.header("🔍 TRA CUU MA LOI")
    loai = st.selectbox("1. Chon thiet bi:", list(DATA_LOI.keys()))
    hang = st.selectbox(f"2. Chon hang {loai}:", list(DATA_LOI[loai].keys()))
    ma_loi = st.text_input("3. Nhap ma loi:").upper().strip()
    
    if st.button("XEM KET QUA"):
        if ma_loi in DATA_LOI[loai][hang]:
            st.success(f"KET QUA: {DATA_LOI[loai][hang][ma_loi]}")
        else:
            st.warning("Ma nay chua co trong kho du lieu.")

elif menu == "Chan doan nhanh":
    st.header("🧠 CHAN DOAN")
    st.write("Chuc nang dang cap nhat...")

elif menu == "Gia han":
    st.header("💳 GIA HAN")
    st.write("Lien he Admin de gia han.")

# --- DONG CUOI CUNG ---
st.divider()
st.caption("He thong Ba Duy v25.0")

