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
    ma_nhap = st.text_input("Nhập mã kích hoạt:", type="password", key="pwd").strip()
    if st.button("XÁC NHẬN VÀO"):
        if ma_nhap in DANH_SACH_KHACH_HANG:
            st.session_state['auth'] = DANH_SACH_KHACH_HANG[ma_nhap]
            st.rerun()
        else: st.error("Sai mã rồi Duy ơi!")
    st.stop()

# --- HEADER ---
user = st.session_state['auth']
st.info(f"👤 Kỹ sư: **{user['ten']}**")

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

# --- MENU CHÍNH ---
st.divider()
c1, c2 = st.columns(2)
with c1:
    if st.button("🔍 TRA MÃ LỖI", use_container_width=True): st.session_state['page'] = "🔍 Tra mã"
with c2:
    if st.button("💳 GIA HẠN", use_container_width=True): st.session_state['page'] = "💳 Gia hạn"

# --- HIỂN THỊ NỘI DUNG ---
page = st.session_state['page']

if page == "🔍 Tra mã":
    st.subheader("🔍 HỆ THỐNG TRA CỨU")
    
    # CHỨC NĂNG CHỌN THIẾT BỊ VÀ HÃNG (HIỂN THỊ NGAY)
    loai_chon = st.radio("1. Chọn loại máy:", list(KHO_DATA.keys()), horizontal=True)
    hang_chon = st.selectbox(f"2. Chọn hãng {loai_chon}:", list(KHO_DATA[loai_chon].keys()))
    ma_loi = st.text_input("3. Nhập mã lỗi:").upper().strip()
    
    if st.button("TÌM GIẢI PHÁP"):
        if ma_loi in KHO_DATA[loai_chon][hang_chon]:
            st.success(f"🛠 **Kết quả:** {KHO_DATA[loai_chon][hang_chon][ma_loi]}")
        else: st.warning("Chưa có mã này trong kho dữ liệu.")

elif page == "💳 Gia hạn":
    st.subheader("💳 THÔNG TIN GIA HẠN")
    st.image("https://img.vietqr.io/image/ICB-104881077679-compact2.png?amount=500000&addInfo=GIAHAN")
    st.write("Nội dung: GIA HAN - BA DUY")

# --- DÒNG CUỐI CÙNG: TUYỆT ĐỐI KHÔNG DÙNG RERUN ---
st.divider()
if st.button("🚪 Thoát ứng dụng"):
    st.session_state['auth'] = None
    st.write("Đã đăng xuất. Vui lòng làm mới trang (F5).")
