import streamlit as st

# 1. CẤU HÌNH HỆ THỐNG & UI MÀU SẮC NỔI BẬT
st.set_page_config(page_title="BA DUY TECH PRO 2026", layout="centered")

st.markdown("""
    <style>
    /* Màu nền tiêu đề */
    .header-box {
        background-color: #FF4B4B;
        padding: 15px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 20px;
    }
    /* Nút bấm Menu chính */
    div.stButton > button {
        background-color: #007BFF !important;
        color: white !important;
        border-radius: 12px !important;
        font-weight: bold !important;
        height: 3.5em !important;
        border: 2px solid #0056b3 !important;
    }
    div.stButton > button:hover {
        background-color: #FF8C00 !important;
        border: 2px solid #e67e00 !important;
    }
    /* Làm nổi bật thanh chọn */
    .stSelectbox label { color: #1E90FF !important; font-weight: bold !important; }
    .stTextInput label { color: #FF1493 !important; font-weight: bold !important; }
    </style>
    """, unsafe_allow_html=True)

if 'auth' not in st.session_state: st.session_state['auth'] = None
if 'page' not in st.session_state: st.session_state['page'] = "HOME"
if 'user_db' not in st.session_state: st.session_state['user_db'] = []

# --- QUẢN LÝ TÀI KHOẢN ---
USERS = {
    "PRO-DUY-2025": {"ten": "Kỹ sư Ba Duy", "loai": "Vĩnh viễn", "han": "Vô hạn"},
    "DUY-FREE": {"ten": "Khách dùng thử", "loai": "Free", "han": "3 ngày"}
}

# --- ĐĂNG NHẬP ---
if st.session_state['auth'] is None:
    st.markdown('<div class="header-box"><h1>🔐 HỆ THỐNG KỸ THUẬT BA DUY</h1></div>', unsafe_allow_html=True)
    ma = st.text_input("NHẬP MÃ KÍCH HOẠT:", type="password").strip()
    if st.button("ĐĂNG NHẬP HỆ THỐNG", use_container_width=True):
        if ma in USERS:
            st.session_state['auth'] = USERS[ma]
            st.rerun()
        else: st.error("Mã không chính xác!")
    st.stop()

# --- DỮ LIỆU TỔNG HỢP TOÀN BỘ MÃ LỖI (UPDATE TỪ FILE) ---
DATA_FULL = {
    "Điều Hòa": {
        "Panasonic": {
            "00H": "Bình thường, máy không lỗi.",
            "11H": "Lỗi đường dữ liệu giữa khối trong và ngoài. 🛠 HD: Kiểm tra dây tín hiệu, bo mạch.",
            "12H": "Khối trong và ngoài khác công suất.",
            "14H": "Lỗi cảm biến nhiệt độ phòng. 🛠 HD: Thay Sensor phòng.",
            "15H": "Lỗi cảm biến nhiệt độ máy nén. 🛠 HD: Kiểm tra sensor đầu block.",
            "16H": "Dòng tải máy nén quá thấp. 🛠 HD: Kiểm tra gas, block.",
            "19H": "Lỗi quạt dàn lạnh. 🛠 HD: Kiểm tra motor quạt, tụ quạt.",
            "23H": "Lỗi cảm biến nhiệt độ dàn lạnh.",
            "25H": "Mạch E-on lỗi.",
            "27H": "Lỗi cảm biến nhiệt độ ngoài trời.",
            "28H": "Lỗi cảm biến giàn nóng (H28). 🛠 HD: Đo điện trở (3KΩ ở 30°C). Kiểm tra jack cắm hoặc thay board.",
            "30H": "Lỗi cảm biến ống ra máy nén.",
            "H11": "Lỗi truyền tín hiệu nóng/lạnh. 🛠 HD: Kiểm tra dây số 3.",
            "H14": "Lỗi cảm biến hút trong nhà.",
            "H19": "Motor quạt trong nhà bị kẹt/hỏng.",
            "H25": "Lỗi bộ lọc Nanoe.",
            "H97": "Motor quạt dàn nóng bị kẹt. 🛠 HD: Vệ sinh, kiểm tra motor quạt nóng.",
            "H98": "Quá nhiệt áp suất cao. 🛠 HD: Vệ sinh dàn lạnh.",
            "H99": "Dàn lạnh đóng băng. 🛠 HD: Kiểm tra gas, quạt lạnh.",
            "F91": "Rò rỉ môi chất lạnh. 🛠 HD: Kiểm tra chỗ hở, nạp lại gas.",
            "F93": "Máy nén hoạt động bất thường. 🛠 HD: Kiểm tra block/board.",
            "F97": "Nhiệt độ máy nén cao. 🛠 HD: Kiểm tra giải nhiệt dàn nóng.",
            "E13": "Lỗi quá dòng/mất pha.",
            "E15": "Áp suất cao bất thường.",
            "E18": "Lỗi cảm biến đường ống bo mạch nóng."
        },
        "Daikin": {
            "C1": "Lỗi bo mạch dàn lạnh hoặc bo quạt.",
            "C4": "Lỗi nhiệt điện trở ống lỏng dàn lạnh.",
            "C9": "Lỗi nhiệt điện trở gió hồi.",
            "E0": "Thiết bị bảo vệ dàn nóng tác động (Cao áp, quá tải).",
            "E1": "Lỗi bo mạch dàn nóng.",
            "E7": "Lỗi motor quạt dàn nóng. 🛠 HD: Kiểm tra quạt kẹt/cháy.",
            "F3": "Nhiệt độ ống đẩy bất thường. 🛠 HD: Kiểm tra thiếu gas/tắc cáp.",
            "U0": "Thiếu môi chất lạnh (Thiếu Gas).",
            "U2": "Lỗi nguồn điện/mất điện tức thời.",
            "U4": "Lỗi truyền tín hiệu nóng lạnh. 🛠 HD: Kiểm tra dây F1-F2.",
            "L5": "Quá dòng máy nén Inverter. 🛠 HD: Kiểm tra Block, IPM.",
            "UA": "Dàn nóng và lạnh không tương thích."
        },
        "LG Inverter": {
            "CH01": "Hỏng cảm biến giàn lạnh.",
            "CH05": "Lỗi kết nối nóng/lạnh. 🛠 HD: Kiểm tra dây tín hiệu.",
            "CH21": "Lỗi IC Công suất (IPM). 🛠 HD: Kiểm tra block, thay bo.",
            "CH22": "Cao dòng, cao điện áp.",
            "CH23": "Điện áp quá thấp.",
            "CH26": "Hỏng máy nén Inverter.",
            "CH32": "Nhiệt độ đường đẩy quá cao.",
            "CH61": "Dàn nóng quá nhiệt. 🛠 HD: Vệ sinh dàn nóng.",
            "CH65": "Hỏng IC nguồn đuôi nóng."
        }
    }
}

# --- GIAO DIỆN CHÍNH ---
user = st.session_state['auth']
st.info(f"👤 **{user['ten']}** | 📦 Gói: **{user['loai']}**")

# MENU TOOL NỔI BẬT
st.write("### 🛠 CÔNG CỤ KỸ THUẬT CHUYÊN NGHIỆP")
c1, c2 = st.columns(2)
with c1:
    if st.button("🔍 TRA MÃ & XỬ LÝ", use_container_width=True): st.session_state.page = "TRA"
with c2:
    if st.button("🧠 CHẨN ĐOÁN AI", use_container_width=True): st.session_state.page = "AI"

c3, c4 = st.columns(2)
with c3:
    if st.button("➕ THÊM MÃ MỚI", use_container_width=True): st.session_state.page = "THEM"
with c4:
    if st.button("💳 GIA HẠN GÓI", use_container_width=True): st.session_state.page = "GIA"

# --- LOGIC TRA CỨU ---
if st.session_state.page == "TRA":
    st.markdown("---")
    st.subheader("🔎 TRA CỨU CHI TIẾT")
    loai = st.selectbox("CHỌN THIẾT BỊ:", list(DATA_FULL.keys()))
    hang = st.selectbox(f"CHỌN HÃNG {loai}:", list(DATA_FULL[loai].keys()))
    ma = st.text_input("NHẬP MÃ LỖI (Vd: H11, U4, CH21...):").upper().strip()
    
    if st.button("TÌM KIẾM NGAY", use_container_width=True):
        if ma in DATA_FULL[loai][hang]:
            st.warning(f"✅ **MÃ LỖI: {ma}**")
            st.success(f"📌 **NỘI DUNG & KHẮC PHỤC:**\n\n {DATA_FULL[loai][hang][ma]}")
        else:
            found = [x for x in st.session_state.user_db if x['ma']==ma and x['hang']==hang]
            if found:
                st.warning("📌 **KINH NGHIỆM CÁ NHÂN:**")
                st.success(found[0]['hd'])
            else:
                st.error("❌ Mã lỗi này chưa được cập nhật!")

elif st.session_state.page == "THEM":
    st.subheader("➕ LƯU KINH NGHIỆM MỚI")
    t_loai = st.selectbox("Loại máy:", ["Điều Hòa", "Máy Giặt", "Bếp Từ"])
    t_hang = st.text_input("Hãng:")
    t_ma = st.text_input("Mã lỗi:").upper()
    t_hd = st.text_area("Cách xử lý thực tế:")
    if st.button("LƯU DỮ LIỆU"):
        st.session_state.user_db.append({'loai': t_loai, 'hang': t_hang, 'ma': t_ma, 'hd': t_hd})
        st.success("Đã lưu!")

elif st.session_state.page == "GIA":
    st.subheader("💳 GIA HẠN")
    st.image("https://img.vietqr.io/image/ICB-104881077679-compact2.png?amount=299000&addInfo=GIAHAN")

# NÚT ĐĂNG XUẤT
st.markdown("---")
if st.button("🚪 ĐĂNG XUẤT", use_container_width=True):
    st.session_state.auth = None
    st.rerun()

st.caption("BA DUY TECH v35.5 - DỮ LIỆU ĐÃ CẬP NHẬT ĐẦY ĐỦ")
