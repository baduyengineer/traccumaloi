import streamlit as st
from datetime import datetime, timedelta

# 1. CẤU HÌNH GIAO DIỆN
st.set_page_config(page_title="BA DUY TECH 2025", layout="wide")

# QUẢN LÝ NGƯỜI DÙNG
today = datetime.now()
DANH_SACH_KHACH_HANG = {
    "DUY-FREE-3D": {"ten": "Khách dùng thử", "loai": "Trial", "ngay_dk": today},
    "PRO-DUY-2025": {"ten": "Kỹ sư Ba Duy", "loai": "Pro", "han": "2026-01-05"},
}

if 'auth' not in st.session_state: st.session_state['auth'] = None
if 'page' not in st.session_state: st.session_state['page'] = "🔍 Tra mã"

# --- MÀN HÌNH ĐĂNG NHẬP ---
if st.session_state['auth'] is None:
    st.title("🔐 HỆ THỐNG BA DUY")
    ma_nhap = st.text_input("Mã kích hoạt:", type="password").strip()
    if st.button("XÁC NHẬN VÀO"):
        if ma_nhap in DANH_SACH_KHACH_HANG:
            st.session_state['auth'] = DANH_SACH_KHACH_HANG[ma_nhap]
            st.rerun()
        else: st.error("Sai mã!")
    st.stop()

# --- HEADER ---
user = st.session_state['auth']
st.write(f"👤 Kỹ sư: **{user['ten']}**")

# --- KHO DỮ LIỆU ---
KHO_DATA = {
    "Bếp Từ": {
        "Sunhouse": {"E0": "Lỗi nhận nồi. Kiểm tra tụ 5uF, 0.33uF.", "E1": "Quá nhiệt cảm biến."},
        "Kangaroo": {"E1": "Lỗi cảm biến.", "E2": "Quá nhiệt IGBT."},
        "Midea": {"E1": "Lỗi cảm biến.", "E3": "Áp cao."}
    },
    "Máy Giặt": {
        "Electrolux": {"E10": "Lỗi nước vào.", "E20": "Lỗi nước xả.", "E40": "Lỗi khóa cửa."},
        "LG": {"IE": "Lỗi cấp nước.", "OE": "Lỗi xả nước."},
        "Samsung": {"4E": "Lỗi nước.", "5E": "Lỗi bơm xả."}
    }
}

# --- MENU NÚT BẤM (HIỂN THỊ TRỰC DIỆN) ---
st.divider()
c1, c2 = st.columns(2)
with c1:
    if st.button("🔍 TRA MÃ LỖI", use_container_width=True): st.session_state['page'] = "🔍 Tra mã"
with c2:
    if st.button("💳 GIA HẠN", use_container_width=True): st.session_state['page'] = "💳 Gia hạn"

# --- XỬ LÝ TRANG ---
page = st.session_state['page']

if page == "🔍 Tra mã":
    st.subheader("🔍 TRA CỨU NHANH")
    # HIỂN THỊ CHỌN THIẾT BỊ VÀ HÃNG NGAY TRÊN MÀN HÌNH
    loai = st.radio("1. Chọn máy:", list(KHO_DATA.keys()), horizontal=True)
    hang = st.selectbox(f"2. Chọn hãng {loai}:", list(KHO_DATA[loai].keys()))
    ma = st.text_input("3. Nhập mã lỗi:").upper().strip()
    
    if st.button("TÌM GIẢI PHÁP"):
        if ma in KHO_DATA[loai][hang]:
            st.success(f"🛠 **{hang} {ma}:** {KHO_DATA[loai][hang][ma]}")
        else: st.warning("Chưa có dữ liệu mã này.")

elif page == "💳 Gia hạn":
    st.subheader("💳 GIA HẠN DỊCH VỤ")
    st.image("https://img.vietqr.io/image/ICB-104881077679-compact2.png?amount=500000&addInfo=GIAHAN")
    st.info("Nội dung: GIA HAN - TRINH BA DUY")

# --- DÒNG CUỐI CÙNG (AN TOÀN TUYỆT ĐỐI) ---
st.divider()
if st.button("🚪 Đăng xuất"):
    st.session_state['auth'] = None
    st.write("Đã thoát. Hãy F5 trang.")
