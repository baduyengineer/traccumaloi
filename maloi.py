import streamlit as st
from datetime import datetime

# --- Cấu hình để tránh lỗi trắng trang ---
st.set_page_config(page_title="App Kỹ Thuật Ba Duy", layout="centered")

# ========================================================
# 1. QUẢN LÝ BẢN QUYỀN
# ========================================================
DANH_SACH_KHACH_HANG = {
    "PRO-DUY-2025": {"ten": "Kỹ sư Ba Duy", "han": "2026-01-05"},
    "ADMIN-888": {"ten": "Quản trị viên", "han": "2030-12-31"},
}

if 'auth' not in st.session_state:
    st.session_state['auth'] = None

if not st.session_state['auth']:
    st.title("🔐 ĐĂNG NHẬP HỆ THỐNG")
    ma_nhap = st.text_input("Nhập mã kích hoạt:", type="password").strip()
    if st.button("Kích hoạt"):
        if ma_nhap in DANH_SACH_KHACH_HANG:
            st.session_state['auth'] = DANH_SACH_KHACH_HANG[ma_nhap]
            st.session_state['ma_kich_hoat'] = ma_nhap
            try: st.rerun()
            except: st.experimental_rerun()
        else:
            st.error("Mã không đúng!")
    st.stop()

user = st.session_state['auth']
ma_khach = st.session_state.get('ma_kich_hoat', 'USER')

# ========================================================
# 2. KHO DỮ LIỆU TỔNG HỢP (MÁY GIẶT - ĐIỀU HÒA - BẾP TỪ)
# ========================================================
KHO_DATA = {
    "Máy Giặt": {
        "Electrolux": {
            "E10": "Lỗi cấp nước. Kiểm tra vòi nước, vệ sinh lưới lọc van cấp.",
            "E21": "Khó xả nước. Kiểm tra bơm xả và ống thoát nước.",
            "E52": "Lỗi Tacho motor. Kiểm tra chổi than và cuộn dây điều tốc.",
            "E58": "Inverter quá dòng. Kiểm tra chạm chập motor.",
        }
    },
    "Máy Điều Hòa": {
        "Daikin": {
            "U0": "Thiếu gas hoặc nghẹt hệ thống. Kiểm tra áp suất và rò rỉ.",
            "A6": "Lỗi motor quạt dàn lạnh. Kiểm tra motor và tụ quạt.",
        }
    },
    "Bếp Từ": {
        "Sunhouse": {
            "E0": "Lỗi nhận nồi. Kiểm tra trở 200k và tụ đường hồi tiếp.",
        }
    }
}

# ========================================================
# 3. GIAO DIỆN CHÍNH
# ========================================================
st.sidebar.title(f"👤 {user['ten']}")
menu = st.sidebar.radio("CHỨC NĂNG", ["Tra mã lỗi", "Sơ đồ thông minh", "Gia hạn tự động"])

if menu == "Tra mã lỗi":
    st.header("🔍 TRA CỨU MÃ LỖI")
    loai = st.selectbox("Chọn loại thiết bị", list(KHO_DATA.keys()))
    hang = st.selectbox("Chọn hãng", list(KHO_DATA[loai].keys()))
    ma = st.text_input("Nhập mã lỗi:").upper().strip()
    
    if st.button("Tìm kiếm"):
        if ma in KHO_DATA[loai][hang]:
            st.success(f"🛠 **Kết quả:** {KHO_DATA[loai][hang][ma]}")
        else:
            st.warning("Mã lỗi chưa có trong kho dữ liệu.")

elif menu == "Sơ đồ thông minh":
    st.header("📚 TÌM SƠ ĐỒ PDF")
    mod = st.text_input("Nhập Model/Mã Board:")
    if st.button("Tìm ngay"):
        url = f"https://www.google.com/search?q={mod}+service+manual+pdf+schematic"
        st.markdown(f"### [👉 Bấm để tải sơ đồ {mod}]({url})")

elif menu == "Gia hạn tự động":
    st.header("💳 GIA HẠN DỊCH VỤ")
    stk = "104881077679"
    ten = "TRINH BA DUY"
    nd = f"GIA HAN {ma_khach}"
    qr_url = f"https://img.vietqr.io/image/ICB-{stk}-compact2.png?amount=500000&addInfo={nd}&accountName={ten}"
    st.image(qr_url, caption="Quét để gia hạn 12 tháng")
    st.info(f"Nội dung: {nd}")

if st.sidebar.button("Đăng xuất"):
    st.session_state['auth'] = None
    try: st.rerun()
    except: st.experimental_rerun()
