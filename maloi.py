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
    ma_nhap = st.text_input("Nhập mã kích hoạt:", type="password", key="login_pass").strip()
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
    }
}

# --- GIAO DIỆN NÚT CHỌN CHỨC NĂNG (HIỂN THỊ NGAY TRÊN MÀN HÌNH) ---
st.divider()
col1, col2 = st.columns(2)
with col1:
    if st.button("🔍 TRA MÃ LỖI", use_container_width=True): st.session_state['page'] = "🔍 Tra mã"
with col2:
    if st.button("💳 GIA HẠN", use_container_width=True): st.session_state['page'] = "💳 Gia hạn"

# --- XỬ LÝ NỘI DUNG TỪNG TRANG ---
page = st.session_state['page']

if page == "🔍 Tra mã":
    st.subheader("🔍 TRA CỨU MÃ LỖI")
    
    # CHỨC NĂNG CHỌN THIẾT BỊ VÀ HÃNG
    loai_may = st.radio("1. Chọn thiết bị:", list(KHO_DATA.keys()), horizontal=True)
    hang_may = st.selectbox(f"2. Chọn hãng {loai_may}:", list(KHO_DATA[loai_may].keys()))
    
    ma_loi = st.text_input("3. Nhập mã lỗi:").upper().strip()
    
    if st.button("XEM KẾT QUẢ"):
        if ma_loi in KHO_DATA[loai_may][hang_may]:
            st.success(f"🛠 **Giải pháp:** {KHO_DATA[loai_may][hang_may][ma_loi]}")
        else:
            st.warning("Chưa có mã lỗi này. Duy hãy cập nhật thêm.")

elif page == "💳 Gia hạn":
    st.subheader("💳 GIA HẠN DỊCH VỤ")
    st.image(f"https://img.vietqr.io/image/ICB-104881077679-compact2.png?amount=500000&addInfo=GIAHAN")
    st.info("Quét mã QR để nâng cấp bản quyền.")

# --- DÒNG CUỐI CÙNG (KHÔNG DÙNG RERUN ĐỂ TRÁNH LỖI) ---
st.divider()
if st.button("🚪 Đăng xuất"):
    st.session_state['auth'] = None
    st.write("Đã thoát. Hãy nhấn F5 để quay lại màn hình chính.")
