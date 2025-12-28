import streamlit as st

# 1. Cấu hình hệ thống
st.set_page_config(page_title="Siêu Trợ Lý Kỹ thuật Ba Duy 2026", layout="wide")

# Quản lý người dùng
DANH_SACH_KHACH_HANG = {
    "PRO-DUY-2025": {"ten": "Kỹ sư Ba Duy", "han": "2026-01-05"},
    "ADMIN-888": {"ten": "Quản trị viên", "han": "2030-12-31"},
}

if 'auth' not in st.session_state:
    st.session_state['auth'] = None

if st.session_state['auth'] is None:
    st.title("🔐 HỆ THỐNG KỸ THUẬT BADUY@2025")
    ma_nhap = st.text_input("Nhập mã kích hoạt:", type="password").strip()
    if st.button("Kích hoạt bản quyền"):
        if ma_nhap in DANH_SACH_KHACH_HANG:
            st.session_state['auth'] = DANH_SACH_KHACH_HANG[ma_nhap]
            st.session_state['ma_kich_hoat'] = ma_nhap
            st.rerun()
        else:
            st.error("Mã không đúng!")
    st.stop()

# --- GIAO DIỆN CHÍNH ---
user = st.session_state['auth']
st.sidebar.title(f"👤 {user['ten']}")
menu = st.sidebar.radio("CHỨC NĂNG CHÍNH", 
    ["🔍 Tra mã lỗi", "🧠 Chẩn đoán bệnh (AI)", "📚 Sơ đồ thông minh", "💳 Gia hạn dịch vụ"])

# --- KHO DỮ LIỆU ---
KHO_DATA = {
    "Bếp Từ": {
        "Sunhouse": {"E0": "Lỗi nhận nồi. Kiểm tra trở 200k, tụ 5uF.", "E1": "Quá áp/Lỗi cảm biến."},
        "Bosch": {"E22": "Lỗi ẩm bo cảm ứng. Sấy khô bo mạch."},
    },
    "Máy Giặt": {
        "Electrolux": {"E10": "Lỗi cấp nước.", "E52": "Lỗi Tacho motor.", "E21": "Lỗi xả nước."},
        "LG": {"IE": "Lỗi cấp nước.", "OE": "Lỗi thoát nước.", "DE": "Lỗi cửa."}
    },
    "Điều Hòa": {
        "Daikin": {"U0": "Thiếu gas.", "A6": "Lỗi quạt dàn lạnh.", "L5": "Lỗi Block Inverter."},
        "Panasonic": {"H11": "Lỗi giao tiếp cục nóng-lạnh."}
    }
}

# 1. TRA MÃ LỖI
if menu == "🔍 Tra mã lỗi":
    st.header("🔍 TRA CỨU MÃ LỖI CHUYÊN SÂU")
    col1, col2 = st.columns(2)
    with col1: loai = st.selectbox("Loại thiết bị", list(KHO_DATA.keys()))
    with col2: hang = st.selectbox("Hãng máy", list(KHO_DATA[loai].keys()))
    ma = st.text_input("Mã lỗi:").upper().strip()
    if st.button("Tìm giải pháp"):
        if ma in KHO_DATA[loai][hang]:
            st.success(f"🛠 **Cách sửa:** {KHO_DATA[loai][hang][ma]}")
        else: st.warning("Dữ liệu đang cập nhật.")

# 2. CHẨN ĐOÁN BỆNH (AI)
elif menu == "🧠 Chẩn đoán bệnh (AI)":
    st.header("🧠 CHẨN ĐOÁN THEO BIỂU HIỆN")
    loai_ai = st.selectbox("Loại máy:", list(KHO_DATA.keys()))
    bieu_hien = st.selectbox("Tình trạng máy:", [
        "Bếp không nhận nồi (không báo lỗi)", 
        "Mất nguồn hoàn toàn", 
        "Rung lắc mạnh khi vắt",
        "Máy lạnh không lạnh/yếu lạnh"
    ])
    if st.button("Phân tích"):
        st.info("🤖 **Gợi ý kỹ thuật:** Kiểm tra các linh kiện công suất (IGBT/Block) và các đường hồi tiếp cảm biến.")

# 3. SƠ ĐỒ THÔNG MINH
elif menu == "📚 Sơ đồ thông minh":
    st.header("📚 TÌM SƠ ĐỒ KỸ THUẬT (PDF)")
    mod = st.text_input("Nhập Model/Mã Board:")
    if st.button("Lọc tài liệu"):
        url = f"https://www.google.com/search?q={mod}+service+manual+pdf+schematic"
        st.markdown(f"### [👉 Bấm để tải sơ đồ máy {mod}]({url})")

# 4. GIA HẠN DỊCH VỤ (KHÔI PHỤC CÁC GÓI)
elif menu == "💳 Gia hạn dịch vụ":
    st.header("💳 GIA HẠN TỰ ĐỘNG QUA VIETINBANK")
    st.write(f"Hạn dùng hiện tại: **{user['han']}**")
    
    # Chọn gói gia hạn
    goi = st.radio("Chọn gói ưu đãi:", ["6 Tháng - 300k", "12 Tháng - 500k", "Vĩnh viễn - 1.5tr"], horizontal=True)
    
    # Tính toán tiền và nội dung
    tien = "300000" if "6 Tháng" in goi else ("500000" if "12 Tháng" in goi else "1500000")
    ma_kh = st.session_state.get('ma_kich_hoat', 'PRO')
    nd = f"GIA HAN {ma_kh}"
    
    # Thông tin VietinBank của Duy
    stk = "104881077679"
    ten_tk = "TRINH BA DUY"
    qr_url = f"https://img.vietqr.io/image/ICB-{stk}-compact2.png?amount={tien}&addInfo={nd}&accountName={ten_tk}"
    
    col_qr, col_txt = st.columns([1, 1.5])
    with col_qr:
        st.image(qr_url, caption="Quét mã QR để thanh toán")
    with col_txt:
        st.success(f"Số tiền: **{int(tien):,} VNĐ**")
        st.info(f"Nội dung: **{nd}**")
        st.warning("Hệ thống sẽ tự động cộng thêm thời hạn ngay sau khi nhận được tiền.")

if st.sidebar.button("Đăng xuất"):
    st.session_state['auth'] = None
    st.rerun()
