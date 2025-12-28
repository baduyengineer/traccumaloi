Chào Duy, mình hiểu rồi. Để có đầy đủ chức năng chọn Thiết bị (Bếp từ, Máy giặt...) và Hãng (Sunhouse, Electrolux...) hiện ngay trên màn hình mà không bị ẩn, mình đã cập nhật lại bản v17.0.

Lưu ý quan trọng để không bị lỗi:

Xóa sạch file cũ: Duy hãy xóa hết nội dung trong file maloi.py.

Chỉ dán code: Chỉ copy phần trong khung đen bên dưới. Không dán lời chào hay giải thích này vào file vì sẽ bị lỗi SyntaxError (lỗi cú pháp) như trong ảnh bạn gửi.

Lỗi dòng cuối: Mình đã loại bỏ hoàn toàn lệnh st.rerun() ở cuối file để tránh lỗi đỏ.

Bản Code v17.0: Đầy đủ Thiết bị & Hãng - Nút bấm lớn cho Mobile
Python

import streamlit as st
from datetime import datetime, timedelta

# 1. CẤU HÌNH HỆ THỐNG
st.set_page_config(page_title="BA DUY TECH 2025", layout="wide")

# QUẢN LÝ NGƯỜI DÙNG
today = datetime.now()
DANH_SACH_KHACH_HANG = {
    "DUY-FREE-3D": {"ten": "Khách dùng thử", "loai": "Trial", "ngay_dk": today},
    "PRO-DUY-2025": {"ten": "Kỹ sư Ba Duy", "loai": "Pro", "han": "2026-01-05"},
}

if 'auth' not in st.session_state: st.session_state['auth'] = None
if 'page' not in st.session_state: st.session_state['page'] = "🏠 Trang chủ"

# --- MÀN HÌNH ĐĂNG NHẬP ---
if st.session_state['auth'] is None:
    st.title("🔐 HỆ THỐNG BA DUY")
    ma_nhap = st.text_input("Nhập mã kích hoạt:", type="password").strip()
    if st.button("XÁC NHẬN VÀO"):
        if ma_nhap in DANH_SACH_KHACH_HANG:
            st.session_state['auth'] = DANH_SACH_KHACH_HANG[ma_nhap]
            st.rerun()
        else: st.error("Mã không đúng!")
    st.stop()

# --- HEADER THÔNG TIN ---
user = st.session_state['auth']
st.write(f"👤 Kỹ sư: **{user['ten']}**")

# --- KHO DỮ LIỆU TỔNG HỢP ---
KHO_DATA = {
    "Bếp Từ": {
        "Sunhouse": {"E0": "Lỗi nhận nồi. Kiểm tra tụ 5uF, 0.33uF, trở hồi tiếp.", "E1": "Lỗi quá nhiệt cảm biến."},
        "Kangaroo": {"E1": "Lỗi cảm biến mặt kính.", "E2": "Quá nhiệt IGBT."},
        "Midea": {"E1": "Lỗi cảm biến.", "E3": "Điện áp cao."}
    },
    "Máy Giặt": {
        "Electrolux": {"E10": "Lỗi cấp nước.", "E20": "Lỗi thoát nước.", "E40": "Lỗi công tắc cửa."},
        "LG": {"IE": "Lỗi nước vào.", "OE": "Lỗi thoát nước.", "DE": "Lỗi cửa."},
        "Samsung": {"4E": "Lỗi cấp nước.", "5E": "Lỗi xả nước."}
    },
    "Điều Hòa": {
        "Panasonic": {"H11": "Lỗi kết nối cục nóng/lạnh.", "F95": "Quá nhiệt dàn nóng."},
        "Daikin": {"A6": "Lỗi motor quạt.", "U4": "Lỗi đường truyền tín hiệu."}
    }
}

# --- GIAO DIỆN NÚT CHỌN CHỨC NĂNG (HIỂN THỊ NGAY TRÊN MÀN HÌNH) ---
st.divider()
col1, col2 = st.columns(2)
with col1:
    if st.button("🔍 TRA MÃ LỖI", use_container_width=True): st.session_state['page'] = "🔍 Tra mã"
with col2:
    if st.button("🧠 CHẨN ĐOÁN AI", use_container_width=True): st.session_state['page'] = "🧠 AI"

# --- NỘI DUNG CHI TIẾT THEO TỪNG TRANG ---
page = st.session_state['page']

if page == "🔍 Tra mã":
    st.subheader("🔍 TRA CỨU MÃ LỖI CHI TIẾT")
    
    # 1. Chọn Thiết bị
    loai_may = st.radio("Bước 1: Chọn loại thiết bị", list(KHO_DATA.keys()), horizontal=True)
    
    # 2. Chọn Hãng (Chỉ hiện hãng của thiết bị đã chọn)
    hang_may = st.selectbox(f"Bước 2: Chọn hãng {loai_may}", list(KHO_DATA[loai_may].keys()))
    
    # 3. Nhập mã lỗi
    ma_loi = st.text_input("Bước 3: Nhập mã lỗi (Ví dụ: E0, E10...):").upper().strip()
    
    if st.button("XEM GIẢI PHÁP"):
        if ma_loi in KHO_DATA[loai_may][hang_may]:
            st.success(f"🛠 **Kết quả cho {hang_may} {ma_loi}:**\n\n{KHO_DATA[loai_may][hang_may][ma_loi]}")
        else:
            st.warning(f"Chưa có dữ liệu cho mã lỗi {ma_loi} của hãng {hang_may}. Duy hãy cập nhật thêm!")

elif page == "🧠 AI":
    st.subheader("🧠 CHẨN ĐOÁN THEO BIỂU HIỆN")
    l_ai = st.selectbox("Chọn loại máy:", list(KHO_DATA.keys()))
    tinh_trang = st.selectbox("Tình trạng thực tế:", [
        "Mất nguồn hoàn toàn", "Rung lắc mạnh khi vắt", "Bếp không nóng/không nhận nồi", "Máy lạnh không mát"
    ])
    if st.button("PHÂN TÍCH NGAY"):
        st.info("🤖 **Gợi ý kỹ thuật:** Kiểm tra khối nguồn xung và các tụ lọc nguồn chính.")

# --- DÒNG CUỐI: THOÁT HỆ THỐNG AN TOÀN ---
st.divider()
if st.button("🚪 Đăng xuất"):
    st.session_state['auth'] = None
    st.write("Đã thoát. Hãy tải lại trang (F5).")
