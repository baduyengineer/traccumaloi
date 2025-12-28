import streamlit as st
from datetime import datetime

# ========================================================
# 1. QUẢN LÝ BẢN QUYỀN (MỤC 4)
# ========================================================
DANH_SACH_KHACH_HANG = {
    "PRO-DUY-2025": {"ten": "Kỹ sư Ba Duy", "loai": "Pro", "han": "2026-01-05"}, # Gần hết hạn để test
    "ADMIN-888": {"ten": "Quản trị viên", "loai": "Pro", "han": "2030-12-31"},
}

if 'auth' not in st.session_state:
    st.session_state['auth'] = None

if not st.session_state['auth']:
    st.markdown("<h2 style='text-align: center;'>🔐 HỆ THỐNG TRA CỨU KỸ THUẬT BADUY@2025</h2>", unsafe_allow_html=True)
    ma_nhap = st.text_input("Nhập mã kích hoạt của bạn:", type="password").strip()
    if st.button("Kích hoạt bản quyền"):
        if ma_nhap in DANH_SACH_KHACH_HANG:
            st.session_state['auth'] = DANH_SACH_KHACH_HANG[ma_nhap]
            st.rerun()
        else:
            st.error("Mã không chính xác hoặc đã bị khóa.")
    st.stop()

user = st.session_state['auth']
ngay_het_han = datetime.strptime(user['han'], "%Y-%m-%d")
ngay_con_lai = (ngay_het_han - datetime.now()).days

# ========================================================
# 2. DỮ LIỆU CHUẨN HÓA (DATA)
# ========================================================
data_ma_loi = {
    "Bếp Từ": {
        "Sunhouse": {
            "E0": {
                "loi": "Lỗi mạch nhận biết điện áp đầu vào AC.", 
                "pro": "Đo cặp trở 200k đường AC. Kiểm tra tụ 4.7uF và diode bảo vệ 5V.",
                "video": "https://www.youtube.com/watch?v=J_iBHlMdcmk"
            },
        },
        "Bosch": {
            "E22": {"loi": "Lỗi bo cảm ứng (ẩm/nước).", "pro": "Sấy bo, kiểm tra IC phím."},
        }
    }
}

data_chan_doan = {
    "Bếp Từ": {
        "Bếp không nhận nồi (không báo lỗi)": "Kiểm tra tụ 0.33uF, mạch Driver (8050/8550) và trở hồi tiếp.",
        "Bếp nổ cầu chì/chập IGBT": "Thay IGBT, cầu diode. Kiểm tra mạch lái trước khi thử điện.",
        "Mất nguồn hoàn toàn": "Kiểm tra IC nguồn, trở cầu chì và diode nắn 300V."
    },
    "Máy Giặt": {
        "Máy rung lắc mạnh khi vắt": "Kiểm tra giảm xóc, cân bằng lồng, bi/trục.",
        "Nước chảy vào không ngừng": "Kiểm tra van cấp (bị kẹt rác) hoặc chập Triac cấp nước."
    }
}

# ========================================================
# 3. GIAO DIỆN ĐIỀU HƯỚNG
# ========================================================
st.sidebar.title(f"Chào, {user['ten']}")
if ngay_con_lai <= 7:
    st.sidebar.warning(f"⚠️ Bản quyền còn {ngay_con_lai} ngày!")

menu = st.sidebar.radio("CHỨC NĂNG CHÍNH", 
    ["🔍 Tra mã lỗi", "🧠 Chẩn đoán bệnh (AI)", "📚 Sơ đồ thông minh", "💳 Gia hạn"])

# --- MENU: TRA MÃ LỖI ---
if menu == "Tra mã lỗi":
    st.header("🔍 TRA CỨU MÃ LỖI NHANH")
    col1, col2 = st.columns(2)
    with col1:
        loai = st.selectbox("Thiết bị", list(data_ma_loi.keys()))
    with col2:
        hang = st.selectbox("Hãng", list(data_ma_loi[loai].keys()))
    
    ma = st.text_input("Nhập mã lỗi:").upper().strip()
    if st.button("Tra cứu ngay"):
        if ma in data_ma_loi[loai][hang]:
            res = data_ma_loi[loai][hang][ma]
            st.info(f"📌 **Mô tả:** {res['loi']}")
            st.success(f"🛠️ **Hướng dẫn Pro:** {res['pro']}")
            if "video" in res:
                st.video(res['video'])
        else:
            st.error("Mã lỗi đang cập nhật...")

# --- MENU: CHẨN ĐOÁN (MỤC 3) ---
elif menu == "Chẩn đoán bệnh (AI)":
    st.header("🧠 CHẨN ĐOÁN THEO BIỂU HIỆN")
    st.write("Dành cho các ca bệnh khó **không hiện mã lỗi**.")
    loai_ai = st.selectbox("Chọn thiết bị", list(data_chan_doan.keys()))
    bieu_hien = st.selectbox("Biểu hiện của máy?", list(data_chan_doan[loai_ai].keys()))
    if st.button("Phân tích lỗi"):
        st.subheader("📋 Kết quả phân tích:")
        st.success(data_chan_doan[loai_ai][bieu_hien])

# --- MENU: SƠ ĐỒ THÔNG MINH (TÍNH NĂNG MỚI) ---
elif menu == "Sơ đồ thông minh":
    st.header("📚 TRỢ LÝ TÌM SƠ ĐỒ PDF")
    st.write("Hệ thống tự động lọc sơ đồ (Schematic) từ kho dữ liệu quốc tế.")
    model_may = st.text_input("Nhập Model máy hoặc Mã board (VD: K2012, Electrolux EWP85742...):")
    if st.button("Tìm sơ đồ chuẩn"):
        # Tạo câu lệnh tìm kiếm chuyên gia
        google_url = f"https://www.google.com/search?q={model_may}+service+manual+pdf+schematic+diagram"
        st.info(f"🔍 Đang tạo liên kết tải file cho Model: {model_may}")
        st.markdown(f"### [👉 Bấm vào đây để tải Sơ đồ/Tài liệu PDF]({google_url})")
        st.warning("Mẹo: Hãy tìm các kết quả có đuôi .pdf hoặc từ trang ManualsLib.")

# --- MENU: GIA HẠN ---
elif menu == "Gia hạn":
    st.header("💳 QUẢN LÝ BẢN QUYỀN")
    st.write(f"Tên khách hàng: **{user['ten']}**")
    st.write(f"Ngày hết hạn: **{user['han']}** (Còn {ngay_con_lai} ngày)")
    st.divider()
    st.write("Liên hệ Duy để gia hạn hoặc mua bản quyền vĩnh viễn:")
    st.success("📞 Zalo/SĐT: 0987973723")

if st.sidebar.button("Đăng xuất"):
    st.session_state['auth'] = None
    st.rerun()
