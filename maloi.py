import streamlit as st
from datetime import datetime

# 1. CAU HINH HE THONG
st.set_page_config(page_title="BA DUY TECH PRO 2025", layout="wide")

if 'auth' not in st.session_state:
    st.session_state['auth'] = None

DANH_SACH_KHACH_HANG = {
    "PRO-DUY-2025": {"ten": "Ky su Ba Duy", "han": "2026-01-05"},
    "DUY-FREE-3D": {"ten": "Khach dung thu", "han": "2025-12-30"},
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
    menu = st.radio("MENU CHINH", ["🔍 Tra ma loi", "💳 Gia han"])
    st.divider()
    if st.button("🚪 Dang xuat"):
        st.session_state['auth'] = None
        st.rerun()

# --- KHO DU LIEU MA LOI CHI TIET (PANASONIC & DAIKIN) ---
DATA_LOI = {
    "Dieu Hoa": {
        "Panasonic": {
            "00H": "Binh thuong, khong co loi.",
            "11H": "Loi duong truyen tin hieu giua dan lanh va dan nong.",
            "12H": "Loi khac biet cong suat giua dan lanh va dan nong.",
            "15H": "Loi cam bien nhiet do may nen (dau day).",
            "16H": "Dong tai may nen qua thap (thieu gas hoac hong block).",
            "19H": "Loi quat dan lanh (quat khong quay hoac hong hall).",
            "23H": "Loi cam bien nhiet do dan lanh.",
            "90F": "Loi mach tang ap PFC ra may nen.",
            "91F": "Dong tai may nen qua thap.",
            "93F": "Loi toc do quay may nen (bat thuong xung).",
            "95F": "Nhiet do dan nong qua cao.",
            "96F": "Qua nhiet bo Transistor cong suat may nen (IPM).",
            "97F": "Nhiet do may nen qua cao.",
            "98F": "Dong tai may nen qua cao.",
            "99F": "Xung DC ra may nen qua cao.",
            "H11": "Loi ket noi giua khoi trong va khoi ngoai."
        },
        "Daikin": {
            "A1": "Loi bo mach dan lanh.",
            "A3": "Loi he thong dieu khien muc nuoc xa (bom xa).",
            "A6": "Loi motor quat dan lanh (qua tai/hong).",
            "C4": "Loi cam bien nhiet do dan trao doi nhiet (R2T).",
            "E1": "Loi bo mach dan nong.",
            "E5": "Loi dong co may nen Inverter (ket/ro dien).",
            "E7": "Loi motor quat dan nong.",
            "F3": "Nhiet do duong ong day bat thuong.",
            "J3": "Loi cam bien nhiet do ong day (R31T-R33T).",
            "L5": "Loi may nen bien tan (qua dong dau ra).",
            "U0": "Canh bao thieu gas hoac nghet duong ong.",
            "U2": "Nguon dien ap khong du hoac sut ap nhanh.",
            "U4": "Loi duong truyen tin hieu giua dan nong va dan lanh.",
            "UA": "Loi cai dat he thong (khong tuong thich dan nong/lanh).",
            "UF": "Loi he thong lanh chua duoc lap dung/khong tuong thich."
        }
    }
}

# --- XU LY NOI DUNG ---
if menu == "🔍 Tra ma loi":
    st.header("🔍 TRA CUU MA LOI CHUYEN NGHIEP")
    
    # BƯỚC 1: CHỌN THIẾT BỊ
    loai = st.selectbox("👉 1. Chon loai thiet bi:", list(DATA_LOI.keys()))
    
    # BƯỚC 2: CHỌN HÃNG
    hang = st.selectbox(f"👉 2. Chon hang {loai}:", list(DATA_LOI[loai].keys()))
    
    # BƯỚC 3: NHẬP MÃ LỖI
    ma_loi = st.text_input("👉 3. Nhap ma loi (Vidu: H11, U4, 15H...):").upper().strip()
    
    if st.button("XEM KET QUA"):
        if ma_loi in DATA_LOI[loai][hang]:
            st.success(f"🛠 **Giai phap cho {hang} {ma_loi}:**\n\n{DATA_LOI[loai][hang][ma_loi]}")
        else:
            st.warning(f"Ma loi '{ma_loi}' chua co trong kho {hang}. Duy hay lien he Admin!")

elif menu == "💳 Gia han":
    st.header("💳 GIA HAN DICH VU")
    st.image("https://img.vietqr.io/image/ICB-104881077679-compact2.png?amount=500000&addInfo=GIAHAN")
    st.info("Noi dung: GIA HAN BA DUY")

# --- DONG CUOI CUNG CHOT FILE ---
st.divider()
st.caption("He thong ky thuat Ba Duy v27.0 - Chot file an toan")
