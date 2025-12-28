import streamlit as st
from datetime import datetime

# 1. CẤU HÌNH HỆ THỐNG
st.set_page_config(page_title="BA DUY TECH PRO 2025", layout="wide")

# QUẢN LÝ NGƯỜI DÙNG
if 'auth' not in st.session_state: st.session_state['auth'] = None

DANH_SACH_KHACH_HANG = {
    "PRO-DUY-2025": {"ten": "Kỹ sư Ba Duy", "loai": "Pro", "han": "2026-01-05"},
    "DUY-FREE-3D": {"ten": "Khách dùng thử", "loai": "Trial", "han": "2025-12-30"},
}

# --- MÀN HÌNH ĐĂNG NHẬP ---
if st.session_state['auth'] is None:
    st.title("🔐 HỆ THỐNG KỸ THUẬT BA DUY")
    ma = st.text_input("Nhập mã kích hoạt:", type="password").strip()
    if st.button("XÁC NHẬN VÀO"):
        if ma in DANH_SACH_KHACH_HANG:
            st.session_state['auth'] = DANH_SACH_KHACH_HANG[ma]
            st.rerun()
        else: st.error("Mã không đúng!")
    st.stop()

# --- SIDEBAR MENU ---
user = st.session_state['auth']
with st.sidebar:
    st.header(f"👤 {user['ten']}")
    st.write(f" loại: {user['loai']} | Hạn: {user['han']}")
    menu = st.radio("MENU CHÍNH", ["🔍 Tra mã lỗi", "🧠 Chẩn đoán nhanh", "💳 Gia hạn"])
    st.divider()
    if st.button("🚪 Đăng xuất"):
        st.session_state['auth'] = None
        st.rerun()

# --- KHO DỮ LIỆU MÃ LỖI CHI TIẾT ---
DATA_LOI = {
    "Điều Hòa": {
        "Panasonic": {
            "00H": "Bình thường, không có lỗi.",
            "11H": "Lỗi đường truyền tín hiệu giữa dàn lạnh và dàn nóng.",
            "12H": "Lỗi khác biệt công suất giữa dàn lạnh và dàn nóng.",
            "14H": "Lỗi cảm biến nhiệt độ phòng.",
            "15H": "Lỗi cảm biến nhiệt độ máy nén (đầu đẩy).",
            "16H": "Dòng tải máy nén quá thấp (thiếu gas hoặc hỏng block).",
            "19H": "Lỗi quạt dàn lạnh (quạt không quay hoặc hỏng hall).",
            "23H": "Lỗi cảm biến nhiệt độ dàn lạnh.",
            "27H": "Lỗi cảm biến nhiệt độ ngoài trời.",
            "28H": "Lỗi cảm biến nhiệt độ dàn nóng.",
            "33H": "Lỗi kết nối khối trong và khối ngoài.",
            "38H": "Lỗi khối trong và ngoài không đồng bộ.",
            "58H": "Lỗi mạch ECO PATROL.",
            "97H": "Lỗi quạt dàn nóng.",
            "99H": "Nhiệt độ dàn lạnh quá thấp (đóng băng dàn).",
            "11F": "Lỗi chuyển đổi chế độ Lạnh/Sưởi (van 4 ngả).",
            "90F": "Lỗi mạch tăng áp PFC ra máy nén.",
            "91F": "Dòng tải máy nén quá thấp.",
            "93F": "Lỗi tốc độ quay máy nén (bất thường xung).",
            "95F": "Nhiệt độ dàn nóng quá cao.",
            "96F": "Quá nhiệt bộ Transistor công suất máy nén (IPM).",
            "97F": "Nhiệt độ máy nén quá cao.",
            "98F": "Dòng tải máy nén quá cao.",
            "99F": "Xung DC ra máy nén quá cao.",
            "E2": "Bất thường mức nước ngưng (bơm xả/phao).",
            "E5": "Lỗi điều khiển từ xa (Remote).",
            "E6": "Lỗi truyền tín hiệu giữa dàn lạnh và dàn nóng.",
        },
        "Daikin": {
            "A0": "Lỗi thiết bị bảo vệ bên ngoài.",
            "A1": "Lỗi bo mạch dàn lạnh.",
            "A3": "Lỗi hệ thống điều khiển mức nước xả (bơm xả).",
            "A6": "Lỗi motor quạt dàn lạnh (quá tải/hỏng).",
            "A7": "Lỗi motor cánh đảo gió.",
            "AF": "Lỗi mực thoát nước xả (tắc máng nước).",
            "C4": "Lỗi cảm biến nhiệt độ dàn trao đổi nhiệt (R2T).",
            "C5": "Lỗi cảm biến nhiệt độ đường ống gas hơi (R3T).",
            "C9": "Lỗi cảm biến nhiệt độ gió hồi (R1T).",
            "CJ": "Lỗi cảm biến nhiệt độ trên điều khiển.",
            "E1": "Lỗi bo mạch dàn nóng.",
            "E3": "Lỗi tác động của công tắc cao áp.",
            "E4": "Lỗi cảm biến hạ áp.",
            "E5": "Lỗi động cơ máy nén Inverter (kẹt/rò điện).",
            "E6": "Máy nén thường bị quá dòng hoặc kẹt cơ.",
            "E7": "Lỗi motor quạt dàn nóng.",
            "F3": "Nhiệt độ đường ống đẩy bất thường.",
            "H7": "Tín hiệu motor quạt nóng bất thường.",
            "H9": "Lỗi cảm biến nhiệt độ gió bên ngoài (R1T).",
            "J3": "Lỗi cảm biến nhiệt độ ống đẩy (R31T-R33T).",
            "J5": "Lỗi cảm biến nhiệt độ ống hút.",
            "J6": "Lỗi cảm biến nhiệt độ dàn trao đổi nhiệt.",
            "L5": "Lỗi máy nén biến tần (quá dòng đầu ra).",
            "U0": "Cảnh báo thiếu gas hoặc nghẹt đường ống.",
            "U1": "Ngược pha hoặc mất pha nguồn điện.",
            "U2": "Nguồn điện áp không đủ hoặc sụt áp nhanh.",
            "U4": "Lỗi đường truyền tín hiệu giữa dàn nóng và dàn lạnh.",
            "U5": "Lỗi truyền tín hiệu giữa dàn lạnh và Remote.",
            "UA": "Lỗi cài đặt hệ thống (không tương thích dàn nóng/lạnh).",
            "UF": "Lỗi hệ thống lạnh chưa được lắp đúng/không tương thích.",
        }
    },
    "Bếp Từ": {
        "Sunhouse": {"E0": "Không nhận nồi.", "E1": "Quá nhiệt.", "E2": "Điện áp cao."},
        "Kangaroo": {"E1": "Lỗi cảm biến kính.", "E2": "Quá nhiệt IGBT."}
    }
}

# --- XỬ LÝ NỘI DUNG ---
if menu == "🔍 Tra mã lỗi":
    st.header("🔍 HỆ THỐNG TRA CỨU ĐA NĂNG")
    
    # BƯỚC 1: CHỌN THIẾT BỊ
    loai = st.selectbox("👉 1. Chọn loại thiết bị:", list(DATA_LOI.keys()))
    
    # BƯỚC 2: CHỌN HÃNG (Tự động lọc theo thiết bị)
    hang = st.selectbox(f"👉 2. Chọn hãng {loai}:", list(DATA_LOI[loai].keys()))
    
    # BƯỚC 3: NHẬP MÃ LỖI
    ma_loi = st.text_input("👉 3. Nhập mã lỗi (Ví dụ: H11, U4, E1...):").upper().strip()
    
    if st.button("XEM KẾT QUẢ"):
        if ma_loi in DATA_LOI[loai][hang]:
            st.success(f"🛠 **Giải pháp cho {hang} {ma_loi}:**\n\n{DATA_LOI[loai][hang][ma_loi]}")
        else:
            st.warning(f"Mã lỗi '{ma_loi}' chưa có trong kho {hang}. Duy hãy liên hệ Admin để cập nhật!")

elif menu == "🧠 Chẩn đoán nhanh":
    st.header("🧠 TRỢ LÝ AI KỸ THUẬT")
    chon_may = st.selectbox("Máy đang hỏng:", ["Điều hòa", "Máy giặt", "Bếp từ"])
    bieu_hien = st.text_area("Mô tả biểu hiện (Vd: Quạt chạy nhưng block không rung):")
    if st.button("Phân tích"):
        st.info("🤖 Gợi ý: Kiểm tra tụ ngậm máy nén hoặc rơ-le trên bo mạch chính.")

elif menu == "💳 Gia hạn":
    st.header("💳 GIA HẠN DỊCH VỤ")
    st.image("https://img.vietqr.io/image/ICB-104881077679-compact2.png?amount=500000&addInfo=GIAHAN")
    st.write("Nội dung chuyển khoản: **GIA HAN BA DUY**")

# --- CHỐT FILE AN TOÀN ---
st.divider()
st.caption("© 2025 TRINH BA DUY - Nền tảng hỗ trợ kỹ thuật số 1 Việt Nam")

