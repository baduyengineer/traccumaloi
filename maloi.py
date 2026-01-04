import streamlit as st

# 1. CẤU HÌNH HỆ THỐNG
st.set_page_config(page_title="BA DUY TECH PRO 2026", layout="centered")

# Tùy chỉnh CSS để làm các nút và thanh công cụ nổi bật hơn
st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: #007BFF;
        color: white;
        border-radius: 10px;
        border: 2px solid #0056b3;
        font-weight: bold;
        height: 3em;
    }
    div.stButton > button:hover {
        background-color: #0056b3;
        color: white;
    }
    .stSelectbox label, .stTextInput label {
        color: #FF4B4B;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

if 'auth' not in st.session_state: st.session_state['auth'] = None
if 'page' not in st.session_state: st.session_state['page'] = "HOME"
if 'user_db' not in st.session_state: st.session_state['user_db'] = []

# DANH SÁCH TÀI KHOẢN
USERS = {
    "PRO-DUY-2025": {"ten": "Kỹ sư Ba Duy", "loai": "Vĩnh viễn", "han": "Vô hạn"},
    "DUY-FREE": {"ten": "Khách dùng thử", "loai": "Free", "han": "3 ngày"}
}

# --- MÀN HÌNH ĐĂNG NHẬP ---
if st.session_state['auth'] is None:
    st.title("🔐 TRỢ LÝ TRA CỨU KỸ THUẬT BA DUY")
    ma = st.text_input("Nhập mã kích hoạt:", type="password").strip()
    if st.button("XÁC NHẬN VÀO HỆ THỐNG", use_container_width=True):
        if ma in USERS:
            st.session_state['auth'] = USERS[ma]
            st.rerun()
        else: st.error("Mã không đúng! Vui lòng liên hệ Admin.")
    st.stop()

# --- DỮ LIỆU TỔNG HỢP (Đã bổ sung cách khắc phục) ---
DATA_FULL = {
    "Điều Hòa": {
        "Panasonic": {
            "28H": "📍 Lỗi cảm biến giàn nóng (H28).\n\n🛠 **KHẮC PHỤC:** Kiểm tra jack cắm; đo điện trở (chuẩn 3KΩ ở 30°C). Nếu hơ nóng điện trở giảm là cảm biến tốt -> Lỗi board mạch cục nóng.",
            "H11": "📍 Lỗi truyền tín hiệu nóng/lạnh.\n\n🛠 **KHẮC PHỤC:** Kiểm tra dây số 3 (dây tín hiệu), kiểm tra bo mạch cục nóng.",
            "H16": "📍 Dòng tải máy nén thấp.\n\n🛠 **KHẮC PHỤC:** Kiểm tra thiếu Gas, block yếu hoặc hỏng biến dòng trên bo.",
            "H19": "📍 Lỗi quạt dàn lạnh.\n\n🛠 **KHẮC PHỤC:** Kiểm tra motor quạt kẹt, hỏng cuộn dây hoặc lỗi bo điều khiển quạt.",
            "F91": "📍 Rò rỉ môi chất lạnh.\n\n🛠 **KHẮC PHỤC:** Kiểm tra độ kín hệ thống, đầu tán, nạp lại gas đúng định lượng.",
            "F97": "📍 Máy nén quá nhiệt.\n\n🛠 **KHẮC PHỤC:** Vệ sinh dàn nóng, kiểm tra quạt giải nhiệt, kiểm tra block ăn dòng.",
            "H98": "📍 Bảo vệ áp suất cao.\n\n🛠 **KHẮC PHỤC:** Vệ sinh lưới lọc, dàn lạnh dơ, kiểm tra sensor đồng.",
            "00H": "📍 Trạng thái bình thường.",
            "11H": "📍 Lỗi truyền thông nóng/lạnh.",
            "14H": "📍 Lỗi cảm biến phòng.",
            "23H": "📍 Lỗi cảm biến dàn lạnh.",
            "H97": "📍 Quạt dàn nóng kẹt/hỏng motor."
        },
        "Daikin": {
            "U4": "📍 Lỗi tín hiệu truyền thông.\n\n🛠 **KHẮC PHỤC:** Kiểm tra dây F1-F2 kết nối nóng lạnh, kiểm tra bo mạch chính.",
            "L5": "📍 Quá dòng máy nén.\n\n🛠 **KHẮC PHỤC:** Kiểm tra block, đo module công suất IPM.",
            "U0": "📍 Cảnh báo thiếu gas.\n\n🛠 **KHẮC PHỤC:** Tìm vị trí rò rỉ, xử lý và nạp lại gas.",
            "E7": "📍 Lỗi motor quạt dàn nóng.\n\n🛠 **KHẮC PHỤC:** Kiểm tra quạt kẹt, đo điện trở motor, thay bo quạt.",
            "F3": "📍 Nhiệt độ ống đẩy cao.\n\n🛠 **KHẮC PHỤC:** Kiểm tra cảm biến, kiểm tra tắc ẩm/tắc bẩn hệ thống lạnh."
        },
        "LG": {
            "CH05": "📍 Lỗi kết nối Inverter.\n\n🛠 **KHẮC PHỤC:** Kiểm tra dây truyền tín hiệu, kiểm tra bo mạch đuôi nóng.",
            "CH21": "📍 Lỗi IC Công suất (IPM).\n\n🛠 **KHẮC PHỤC:** Đo kiểm block, thay board hoặc thay IC công suất.",
            "CH61": "📍 Dàn nóng quá nhiệt.\n\n🛠 **KHẮC PHỤC:** Vệ sinh dàn nóng ngay, kiểm tra quạt giải nhiệt.",
            "CH33": "📍 Quá tải máy nén inverter.\n\n🛠 **KHẮC PHỤC:** Kiểm tra áp suất gas, dòng làm việc của block."
        }
    },
    "Máy Giặt": {
        "Electrolux": {
            "E10": "📍 Lỗi cấp nước.\n\n🛠 **KHẮC PHỤC:** Vệ sinh lọc van cấp, kiểm tra van điện từ.",
            "E20": "📍 Lỗi thoát nước.\n\n🛠 **KHẮC PHỤC:** Vệ sinh hố bơm xả, kiểm tra motor bơm."
        }
    }
}

# --- GIAO DIỆN CHÍNH ---
user = st.session_state['auth']
st.info(f"👤 **{user['ten']}** | 📦 Gói: **{user['loai']}** | 📅 Hạn: **{user['han']}**")

# MENU CHÍNH NỔI BẬT
st.write("### 🛠 CÔNG CỤ KỸ THUẬT")
c1, c2 = st.columns(2)
with c1:
    if st.button("🔍 TRA MÃ & XỬ LÝ", use_container_width=True): st.session_state.page = "TRA"
with c2:
    if st.button("🧠 CHẨN ĐOÁN AI", use_container_width=True): st.session_state.page = "AI"

c3, c4 = st.columns(2)
with c3:
    if st.button("➕ THÊM KINH NGHIỆM", use_container_width=True): st.session_state.page = "THEM"
with c4:
    if st.button("💳 MUA GÓI / GIA HẠN", use_container_width=True): st.session_state.page = "GIA"

# --- LOGIC XỬ LÝ ---
if st.session_state.page == "TRA":
    st.markdown("---")
    st.subheader("🔍 TRA CỨU MÃ LỖI CHI TIẾT")
    
    # Thanh công cụ chọn loại nổi bật bằng màu sắc mặc định của Streamlit
    loai = st.selectbox("1. Chọn thiết bị:", list(DATA_FULL.keys()))
    hang = st.selectbox(f"2. Chọn hãng {loai}:", list(DATA_FULL[loai].keys()))
    ma = st.text_input("3. Nhập mã lỗi cần tra:").upper().strip()
    
    if st.button("TÌM KIẾM NGAY", use_container_width=True):
        if ma in DATA_FULL[loai][hang]:
            # Hiển thị thanh màu vàng (Warning) để làm nổi bật nội dung khắc phục
            st.warning(f"**KẾT QUẢ TRA CỨU CHO {hang} {ma}:**")
            st.success(DATA_FULL[loai][hang][ma])
        else:
            found = [x for x in st.session_state.user_db if x['ma']==ma and x['hang']==hang]
            if found:
                st.warning("**KINH NGHIỆM CÁ NHÂN ĐÃ LƯU:**")
                st.success(found[0]['hd'])
            else:
                st.error("❌ Mã lỗi này chưa có trong thư viện. Bạn hãy dùng AI hoặc tự thêm mã mới!")

elif st.session_state.page == "THEM":
    st.markdown("---")
    st.subheader("➕ LÀM GIÀU DỮ LIỆU")
    t_loai = st.selectbox("Loại máy:", ["Điều Hòa", "Máy Giặt", "Bếp Từ"])
    t_hang = st.text_input("Hãng máy:")
    t_ma = st.text_input("Mã lỗi mới:").upper()
    t_hd = st.text_area("Hướng dẫn xử lý thực tế:")
    if st.button("LƯU VÀO KHO CÁ NHÂN"):
        st.session_state.user_db.append({'loai': t_loai, 'hang': t_hang, 'ma': t_ma, 'hd': t_hd})
        st.balloons()
        st.success("✅ Đã lưu kinh nghiệm thành công!")

elif st.session_state.page == "GIA":
    st.markdown("---")
    st.subheader("💳 GIA HẠN DỊCH VỤ")
    st.warning("Gói của bạn sẽ được kích hoạt ngay sau khi chuyển khoản thành công!")
    st.image("https://img.vietqr.io/image/ICB-104881077679-compact2.png?amount=199000&addInfo=GIAHAN")

# NÚT ĐĂNG XUẤT
st.markdown("---")
if st.button("🚪 Đăng xuất hệ thống", use_container_width=True):
    st.session_state.auth = None
    st.rerun()

st.caption("BA DUY TECH v35.2 - TRA CỨU KỸ THUẬT CHUYÊN NGHIỆP")


