import streamlit as st

# 1. Cấu hình giao diện
st.set_page_config(page_title="Hệ thống Ba Duy 2025", layout="centered")

# 2. Dữ liệu khách hàng
DANH_SACH_KHACH_HANG = {
    "PRO-DUY-2025": {"ten": "Kỹ sư Ba Duy", "han": "2026-01-05"},
    "ADMIN-888": {"ten": "Quản trị viên", "han": "2030-12-31"},
}

# Khởi tạo trạng thái đăng nhập
if 'auth' not in st.session_state:
    st.session_state['auth'] = None

# --- VÒNG LẶP ĐĂNG NHẬP ---
if st.session_state['auth'] is None:
    st.title("🔐 ĐĂNG NHẬP HỆ THỐNG")
    ma_nhap = st.text_input("Nhập mã kích hoạt:", type="password").strip()
    if st.button("Kích hoạt ngay"):
        if ma_nhap in DANH_SACH_KHACH_HANG:
            st.session_state['auth'] = DANH_SACH_KHACH_HANG[ma_nhap]
            st.session_state['ma_kich_hoat'] = ma_nhap
            st.success("Đã xác thực! Hãy bấm nút 'Vào ứng dụng' bên dưới.")
            st.button("Vào ứng dụng") # Nút này dùng để ép Streamlit refresh giao diện
        else:
            st.error("Mã không đúng!")
else:
    # --- GIAO DIỆN CHÍNH KHI ĐÃ ĐĂNG NHẬP ---
    user = st.session_state['auth']
    st.sidebar.title(f"👤 {user['ten']}")
    
    menu = st.sidebar.radio("CHỨC NĂNG CHÍNH", ["Tra mã lỗi", "Gia hạn tự động"])

    if menu == "Tra mã lỗi":
        st.header("🔍 TRA CỨU MÃ LỖI")
        # Dữ liệu nạp trực tiếp để tránh trắng trang
        kho = {
            "Máy Giặt": {"Electrolux": {"E10": "Lỗi cấp nước", "E52": "Lỗi Tacho motor"}},
            "Điều Hòa": {"Daikin": {"U0": "Thiếu gas/Nghẹt", "A6": "Lỗi quạt dàn lạnh"}}
        }
        loai = st.selectbox("Loại máy", list(kho.keys()))
        hang = st.selectbox("Hãng", list(kho[loai].keys()))
        ma = st.text_input("Mã lỗi:").upper().strip()
        if st.button("Tìm"):
            if ma in kho[loai][hang]:
                st.success(f"🛠 Giải pháp: {kho[loai][hang][ma]}")
            else: st.warning("Chưa có dữ liệu.")

    elif menu == "Gia hạn tự động":
        st.header("💳 GIA HẠN DỊCH VỤ")
        st.write(f"Hạn dùng: {user['han']}")
        # QR VietinBank chuẩn của Duy
        qr = f"https://img.vietqr.io/image/ICB-104881077679-compact2.png?amount=500000&addInfo=GIA%20HAN%20{st.session_state['ma_kich_hoat']}&accountName=TRINH%20BA%20DUY"
        st.image(qr, caption="Quét mã QR để gia hạn")

    # Nút đăng xuất an toàn không gây lỗi dòng 99/105
    if st.sidebar.button("Đăng xuất"):
        st.session_state['auth'] = None
        st.info("Đã đăng xuất. Hãy F5 hoặc bấm nút 'Xác nhận thoát' để quay lại màn hình khóa.")
        st.button("Xác nhận thoát")
