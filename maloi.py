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

# Khởi tạo trạng thái ứng dụng
if 'auth' not in st.session_state: st.session_state['auth'] = None
if 'page' not in st.session_state: st.session_state['page'] = "Home"

# --- MÀN HÌNH ĐĂNG NHẬP ---
if st.session_state['auth'] is None:
    st.title("🔐 HỆ THỐNG KỸ THUẬT BADUY")
    ma_nhap = st.text_input("Nhập mã kích hoạt:", type="password").strip()
    if st.button("XÁC NHẬN VÀO"):
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
        st.error("🚫 ĐÃ HẾT HẠN DÙNG THỬ")
    else: st.warning(f"⏳ CÒN {con_lai + 1} NGÀY DÙNG THỬ")
else:
    st.success(f"✅ BẢN QUYỀN PRO: {user['han']}")

st.divider()

# --- GIAO DIỆN NÚT CHỌN CHÍNH (HIỂN THỊ TRỰC DIỆN TRÊN MÀN HÌNH) ---
# Sử dụng các nút bấm lớn thay vì menu ẩn để khách dùng điện thoại thấy ngay
if is_expired:
    st.session_state['page'] = "💳 Gia hạn"
else:
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔍 TRA MÃ LỖI", use_container_width=True): st.session_state['page'] = "🔍 Tra mã"
        if st.button("📚 SƠ ĐỒ THÔNG MINH", use_container_width=True): st.session_state['page'] = "📚 Sơ đồ"
    with col2:
        if st.button("🧠 CHẨN ĐOÁN AI", use_container_width=True): st.session_state['page'] = "🧠 AI"
        if st.button("💳 GIA HẠN DỊCH VỤ", use_container_width=True): st.session_state['page'] = "💳 Gia hạn"

st.divider()

# --- XỬ LÝ NỘI DUNG TỪNG TRANG ---
page = st.session_state['page']

if page == "🔍 Tra mã":
    st.subheader("🔍 TRA CỨU NHANH")
    ma = st.text_input("Nhập mã lỗi cần tra:").upper().strip()
    if st.button("Bắt đầu tìm"):
        st.info("🛠 Đang kết nối kho dữ liệu...")

elif page == "🧠 AI":
    st.subheader("🧠 CHẨN ĐOÁN THÔNG MINH")
    loai = st.radio("Loại máy:", ["Bếp Từ", "Máy Giặt", "Điều Hòa"], horizontal=True)
    st.selectbox("Biểu hiện:", ["Không lên nguồn", "Báo lỗi trên màn hình", "Rung lắc/Kêu to"])
    st.button("Phân tích bệnh")

elif page == "📚 Sơ đồ":
    st.subheader("📚 KHO SƠ ĐỒ KỸ THUẬT")
    mod = st.text_input("Nhập Model máy/Mã Board:")
    if st.button("Tìm link sơ đồ"):
        st.markdown(f"### [👉 Bấm để tải tài liệu {mod}](https://google.com/search?q={mod}+service+manual+pdf)")

elif page == "💳 Gia hạn":
    st.subheader("💳 GIA HẠN BẢN QUYỀN")
    goi = st.radio("Chọn gói nâng cấp:", ["6 Tháng - 300k", "12 Tháng - 500k", "Vĩnh viễn - 1.5tr"])
    nd = f"GIA HAN {st.session_state.get('ma_kich_hoat')}"
    qr = f"https://img.vietqr.io/image/ICB-104881077679-compact2.png?amount=500000&addInfo={nd}"
    st.image(qr, use_container_width=True, caption="Quét mã để gia hạn tự động")
    st.success(f"Nội dung chuyển khoản: {nd}")

# DÒNG CUỐI CÙNG - KHÔNG SỬ DỤNG RERUN ĐỂ TRÁNH LỖI TRÌNH DUYỆT
st.divider()
if st.button("🔐 Đăng xuất"):
    st.session_state['auth'] = None
    st.info("Đã đăng xuất an toàn. Hãy tải lại trang (F5).")
