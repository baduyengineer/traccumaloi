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

# --- MÀN HÌNH ĐĂNG NHẬP ---
if st.session_state['auth'] is None:
    st.title("🔐 HỆ THỐNG BA DUY")
    ma_nhap = st.text_input("Mã kích hoạt:", type="password").strip()
    if st.button("XÁC NHẬN VÀO"):
        if ma_nhap in DANH_SACH_KHACH_HANG:
            st.session_state['auth'] = DANH_SACH_KHACH_HANG[ma_nhap]
            st.rerun()
        else: st.error("Mã không đúng!")
    st.stop()

# --- SIDEBAR: CHỌN CHỨC NĂNG (Giao diện cũ Duy thích) ---
user = st.session_state['auth']
with st.sidebar:
    st.title(f"👤 {user['ten']}")
    menu = st.radio("CHỨC NĂNG CHÍNH:", 
                    ["🔍 Tra mã lỗi", "🧠 Chẩn đoán AI", "📚 Sơ đồ PDF", "💳 Gia hạn"])
    
    st.divider()
    if st.button("Đăng xuất"):
        st.session_state['auth'] = None
        st.rerun()

# --- KHO DỮ LIỆU ---
KHO_DATA = {
    "Bếp Từ": {
        "Sunhouse": {"E0": "Lỗi nhận nồi. Kiểm tra tụ 5uF, 0.33uF.", "E1": "Quá nhiệt cảm biến."},
        "Kangaroo": {"E1": "Lỗi cảm biến.", "E2": "Quá nhiệt IGBT."},
    },
    "Máy Giặt": {
        "Electrolux": {"E10": "Lỗi nước vào.", "E20": "Lỗi xả nước."},
        "LG": {"IE": "Lỗi nước.", "OE": "Lỗi xả."},
    }
}

# --- NỘI DUNG CHÍNH ---
if menu == "🔍 Tra mã lỗi":
    st.header("🔍 TRA CỨU MÃ LỖI")
    # Đầy đủ Chọn thiết bị và Chọn hãng
    loai = st.selectbox("1. Chọn loại thiết bị:", list(KHO_DATA.keys()))
    hang = st.selectbox(f"2. Chọn hãng {loai}:", list(KHO_DATA[loai].keys()))
    ma = st.text_input("3. Nhập mã lỗi:").upper().strip()
    
    if st.button("TÌM GIẢI PHÁP"):
        if ma in KHO_DATA[loai][hang]:
            st.success(f"🛠 **Kết quả:** {KHO_DATA[loai][hang][ma]}")
        else: st.warning("Chưa có mã này.")

elif menu == "🧠 Chẩn đoán AI":
    st.header("🧠 CHẨN ĐOÁN THÔNG MINH")
    l_ai = st.selectbox("Loại máy:", list(KHO_DATA.keys()))
    benh = st.selectbox("Biểu hiện:", ["Mất nguồn", "Rung lắc", "Không nóng"])
    if st.button("Phân tích"):
        st.info("🤖 Gợi ý: Kiểm tra khối nguồn xung và tụ lọc.")

elif menu == "📚 Sơ đồ PDF":
    st.header("📚 KHO SƠ ĐỒ")
    model = st.text_input("Nhập Model:")
    st.button("Tìm link tải")

elif menu == "💳 Gia hạn":
    st.header("💳 GIA HẠN")
    st.image("https://img.vietqr.io/image/ICB-104881077679-compact2.png?amount=500000&addInfo=GIAHAN")

# --- DÒNG CUỐI CÙNG: KHÔNG DÙNG LỆNH GÂY LỖI ---
st.divider()
st.caption("Hệ thống kỹ thuật Ba Duy v22.0")
