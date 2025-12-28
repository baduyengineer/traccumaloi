import streamlit as st
from datetime import datetime

# 1. CẤU HÌNH HỆ THỐNG
st.set_page_config(page_title="TRỢ LÝ KỸ THUẬT TECH PRO v30", layout="centered")

if 'auth' not in st.session_state: st.session_state['auth'] = None
if 'page' not in st.session_state: st.session_state['page'] = "🏠 Trang chủ"
if 'user_data' not in st.session_state: st.session_state['user_data'] = []

DANH_SACH_KHACH = {
    "PRO-DUY-2025": {"ten": "Kỹ sư Ba Duy", "han": "2026-01-05"},
    "DUY-FREE-3D": {"ten": "Khách dùng thử", "han": "2025-12-30"},
}

# --- MÀN HÌNH ĐĂNG NHẬP ---
if st.session_state['auth'] is None:
    st.title("🔐 HỆ THỐNG BA DUY PRO")
    ma = st.text_input("Nhập mã kích hoạt:", type="password").strip()
    if st.button("XÁC NHẬN VÀO", use_container_width=True):
        if ma in DANH_SACH_KHACH:
            st.session_state['auth'] = DANH_SACH_KHACH[ma]
            st.rerun()
        else: st.error("Mã không đúng!")
    st.stop()

# --- HEADER ---
user = st.session_state['auth']
st.success(f"👤 {user['ten']} | 📅 Hạn: {user['han']}")

# KHO DỮ LIỆU CÓ HƯỚNG DẪN CHI TIẾT
DATA_PRO = {
    "Điều Hòa": {
        "Panasonic": {
            "H11": "Lỗi kết nối lạnh/nóng. \nHD: 1. Kiểm tra dây tín hiệu số 3. \n2. Đo điện áp giao tiếp (dao động 15-30VDC). \n3. Kiểm tra bo mạch dàn nóng.",
            "H16": "Dòng tải máy nén thấp. \nHD: 1. Kiểm tra áp suất gas (có thể thiếu gas). \n2. Kiểm tra biến dòng trên bo nóng. \n3. Kiểm tra Block.",
        },
        "Daikin": {
            "U4": "Lỗi tín hiệu nóng/lanh. \nHD: 1. Kiểm tra dây truyền tín hiệu. \n2. Kiểm tra cầu chì bo nóng/lanh. \n3. Thay thử bo mạch nếu dây tốt.",
            "L5": "Quá dòng máy nén Inverter. \nHD: 1. Rút giắc máy nén đo điện trở 3 pha (phải bằng nhau). \n2. Kiểm tra độ cách điện block. \n3. Hỏng IPM Bo nóng.",
        }
    }
}

# --- MENU CHÍNH ---
st.divider()
c1, c2 = st.columns(2)
with c1:
    if st.button("🔍 TRA MÃ & HƯỚNG DẪN", use_container_width=True): st.session_state.page = "TRA_MA"
with c2:
    if st.button("➕ THÊM MÃ MỚI", use_container_width=True): st.session_state.page = "THEM_MA"

c3, c4 = st.columns(2)
with c3:
    if st.button("🧠 CHẨN ĐOÁN AI", use_container_width=True): st.session_state.page = "AI"
with c4:
    if st.button("💳 GIA HẠN", use_container_width=True): st.session_state.page = "GIA_HAN"

# --- XỬ LÝ TRANG ---
if st.session_state.page == "TRA_MA":
    st.header("🔍 TRA CỨU & HƯỚNG DẪN")
    loai = st.selectbox("Thiết bị:", list(DATA_PRO.keys()))
    hang = st.selectbox(f"Hãng {loai}:", list(DATA_PRO[loai].keys()))
    ma = st.text_input("Nhập mã lỗi:").upper().strip()
    
    if st.button("XEM CÁCH SỬA", use_container_width=True):
        if ma in DATA_PRO[loai][hang]:
            st.info(f"🛠 **{hang} {ma}:**\n\n{DATA_PRO[loai][hang][ma]}")
        else:
            # Tìm trong dữ liệu thợ tự thêm
            found = False
            for item in st.session_state.user_data:
                if item['ma'] == ma and item['hang'] == hang:
                    st.success(f"📌 **Kinh nghiệm lưu trữ:**\n\n{item['cach_sua']}")
                    found = True
            if not found: st.warning("Mã này chưa có. Duy hãy dùng mục 'Thêm mã mới' để lưu lại!")

elif st.session_state.page == "THEM_MA":
    st.header("➕ ĐÓNG GÓP MÃ LỖI MỚI")
    t_loai = st.selectbox("Loại máy:", ["Điều Hòa", "Máy Giặt", "Bếp Từ", "Tủ Lạnh"])
    t_hang = st.text_input("Hãng máy:")
    t_ma = st.text_input("Mã lỗi:").upper().strip()
    t_cach = st.text_area("Hướng dẫn sửa chữa (Kinh nghiệm của bạn):")
    
    if st.button("LƯU VÀO KHO DỮ LIỆU", use_container_width=True):
        if t_ma and t_cach:
            st.session_state.user_data.append({'loai': t_loai, 'hang': t_hang, 'ma': t_ma, 'cach_sua': t_cach})
            st.success("✅ Đã lưu kinh nghiệm thành công! Duy có thể tra lại mã này ngay bây giờ.")
        else: st.error("Vui lòng nhập đủ thông tin!")

elif st.session_state.page == "AI":
    st.header("🧠 CHẨN ĐOÁN AI")
    benh = st.text_area("Biểu hiện bệnh:")
    if st.button("PHÂN TÍCH"):
        st.warning("🤖 Gợi ý: Kiểm tra ngay tụ lọc nguồn và cảm biến nhiệt độ.")

elif st.session_state.page == "GIA_HAN":
    st.subheader("💳 GIA HẠN")
    st.image("https://img.vietqr.io/image/ICB-104881077679-compact2.png?amount=500000&addInfo=GIAHAN")

# NÚT THOÁT
st.divider()
if st.button("🚪 Thoát hệ thống", use_container_width=True):
    st.session_state.auth = None
    st.rerun()

st.caption("BA DUY TECH v30.0 - Nền tảng kỹ thuật thông minh")
