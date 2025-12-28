import streamlit as st
from datetime import datetime, timedelta

# 1. CẤU HÌNH GIAO DIỆN
st.set_page_config(page_title="BADUY TECH 2025", layout="wide")

# QUẢN LÝ NGƯỜI DÙNG
today = datetime.now()
DANH_SACH_KHACH_HANG = {
    "DUY-FREE-3D": {"ten": "Khách dùng thử", "loai": "Trial", "ngay_dk": today},
    "PRO-DUY-2025": {"ten": "Kỹ sư Ba Duy", "loai": "Pro", "han": "2026-01-05"},
}

# Khởi tạo trạng thái
if 'auth' not in st.session_state: st.session_state['auth'] = None
if 'page' not in st.session_state: st.session_state['page'] = "Home"

# --- MÀN HÌNH ĐĂNG NHẬP ---
if st.session_state['auth'] is None:
    st.title("🔐 HỆ THỐNG KỸ THUẬT BADUY")
    ma_nhap = st.text_input("Nhập mã kích hoạt:", type="password").strip()
    if st.button("VÀO HỆ THỐNG"):
        if ma_nhap in DANH_SACH_KHACH_HANG:
            st.session_state['auth'] = DANH_SACH_KHACH_HANG[ma_nhap]
            st.session_state['ma_kich_hoat'] = ma_nhap
            st.rerun()
        else: st.error("Mã không đúng!")
    st.stop()

# --- HEADER THÔNG TIN ---
user = st.session_state['auth']
st.markdown(f"### 👤 Chào: {user['ten']}")

is_expired = False
if user.get("loai") == "Trial":
    con_lai = (user["ngay_dk"] + timedelta(days=3) - datetime.now()).days
    if con_lai < 0:
        is_expired = True
        st.error("🚫 HẾT HẠN DÙNG THỬ")
    else: st.warning(f"⏳ CÒN {con_lai + 1} NGÀY DÙNG THỬ")
else:
    st.success(f"✅ BẢN QUYỀN PRO: {user['han']}")

st.divider()

# --- GIAO DIỆN NÚT CHỌN CHÍNH (HIỂN THỊ NGAY TRÊN MÀN HÌNH) ---
if is_expired:
    st.session_state['page'] = "💳 Gia hạn"
else:
    # Tạo các nút bấm to cho điện thoại
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔍 TRA MÃ LỖI", use_container_width=True): st.session_state['page'] = "🔍 Tra mã"
        if st.button("📚 SƠ ĐỒ PDF", use_container_width=True): st.session_state['page'] = "📚 Sơ đồ"
    with col2:
        if st.button("🧠 CHẨN ĐOÁN AI", use_container_width=True): st.session_state['page'] = "🧠 AI"
        if st.button("💳 GIA HẠN", use_container_width=True): st.session_state['page'] = "💳 Gia hạn"

st.divider()

# --- XỬ LÝ NỘI DUNG ---
page = st.session_state['page']

if page == "🔍 Tra mã":
    st.subheader("🔍 TRA CỨU NHANH")
    ma = st.text_input("Nhập mã lỗi:").upper().strip()
    if st.button("Tìm ngay"):
        st.info("🛠 Đang tra cứu dữ liệu...")

elif page == "🧠 AI":
    st.subheader("🧠 CHẨN ĐOÁN THÔNG MINH")
    loai = st.radio("Chọn máy:", ["Bếp Từ", "Máy Giặt", "Điều Hòa"], horizontal=True)
    st.selectbox("Tình trạng:", ["Không nguồn", "Không nhận nồi", "Rung lắc mạnh"])
    st.button("Phân tích lỗi")

elif page == "📚 Sơ đồ":
    mod = st.text_input("Model máy:")
    if st.button("Lấy link tải"):
        st.markdown(f"[👉 Bấm để tải sơ đồ {mod}](https://google.com/search?q={mod}+pdf)")

elif page == "💳 Gia hạn":
    st.subheader("💳 GIA HẠN DỊCH VỤ")
    tien = st.radio("Chọn gói:", ["300k/6th", "500k/12th", "1.5tr/Vĩnh viễn"])
    nd = f"GIA HAN {st.session_state.get('ma_kich_hoat')}"
    qr = f"https://img.vietqr.io/image/ICB-104881077679-compact2.png?amount=500000&addInfo={nd}"
    st.image(qr, use_container_width=True)

# NÚT THOÁT - CÁCH LÀM MỚI AN TOÀN KHÔNG GÂY LỖI DÒNG CUỐI
st.divider()
if st.sidebar.button("Đăng xuất"):
    st.session_state['auth'] = None
    st.write("Đang thoát... Hãy tải lại trang (F5).")
