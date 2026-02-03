import streamlit as st

# 1. CẤU HÌNH HỆ THỐNG & GIAO DIỆN NỔI BẬT
st.set_page_config(page_title="BA DUY TECH PRO 2026", layout="centered")

# CSS làm rực màu các thanh Tool và Nút bấm
st.markdown("""
    <style>
    /* Làm nổi bật các nút Menu chính */
    div.stButton > button {
        background-color: #007BFF !important;
        color: white !important;
        border-radius: 12px !important;
        border: 2px solid #0056b3 !important;
        font-weight: bold !important;
        height: 3.5em !important;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    div.stButton > button:hover {
        background-color: #FF8C00 !important;
        border: 2px solid #e67e00 !important;
    }
    /* Làm rực màu thanh chọn Selectbox và Input để dễ nhận diện */
    .stSelectbox label, .stTextInput label, .stTextArea label {
        color: #FFFFFF !important;
        background-color: #FF4B4B !important; /* Màu nền đỏ cho nhãn Tool */
        padding: 5px 15px !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        font-size: 16px !important;
        width: fit-content !important;
        margin-bottom: 10px !important;
    }
    /* Làm nổi bật khung thông tin người dùng */
    .user-info {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 10px;
        border-left: 5px solid #007BFF;
        margin-bottom: 20px;
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
    st.title("🔐 HỆ THỐNG TRỢ LÝ KỸ THUẬT BA DUY")
    ma = st.text_input("Nhập mã kích hoạt:", type="password").strip()
    if st.button("XÁC NHẬN VÀO", use_container_width=True):
        if ma in USERS:
            st.session_state['auth'] = USERS[ma]
            st.rerun()
        else: st.error("Mã không đúng! Vui lòng liên hệ Admin.")
    st.stop()

# --- DỮ LIỆU TỔNG HỢP SIÊU KHỦNG (ĐÃ BỔ SUNG BẾP TỪ) ---
DATA_FULL = {
    "Điều Hòa LG Inverter": {
        "CH01": "Hỏng cảm biến giàn lạnh ",
        "CH02": "Hỏng cảm biến giàn lạnh ",
        "CH05": "Lỗi kết nối giàn nóng và giàn lạnh inverter ",
        "CH06": "Hỏng cảm biến đường đi của giàn nóng inverter ",
        "CH09": "Lỗi chức năng board mạch giàn nóng inverter ",
        "CH10": "Quạt giàn lạnh inverter ",
        "CH21": "Lỗi IC Công Suất ",
        "CH22": "Cao dòng, cao điện áp trên cuộn seo, board ",
        "CH23": "Điện áp quá thấp ",
        "CH26": "Hỏng máy nén inverter ",
        "CH27": "Lỗi quá tải dàn nóng, board Inverter ",
        "CH29": "Pha máy nén inverter ",
        "CH32": "Nhiệt độ cao đường đẩy máy nén inverter ",
        "CH33": "Quá tải máy nén inverter ",
        "CH41": "Cảm biến máy nén 200k inverter ",
        "CH44": "Hỏng cảm biến gió giàn nóng 10k inverter ",
        "CH45": "Hỏng cảm biến gió giàn nóng 5k inverter ",
        "CH46": "Cảm biến đường về của máy nén inverter ",
        "CH47": "Máy nén không hoạt động cảm biến 200k ",
        "CH53": "Liên lạc giữa giàn nóng và giàn lạnh ",
        "CH60": "IC cắm trên mạch giàn nóng inverter ",
        "CH61": "Giàn nóng không giải nhiệt được ",
        "CH62": "Nhiệt độ cao ic nguồn đuôi nóng inverter ",
        "CH65": "Hỏng ic nguồn đuôi nóng inverter "
    },
    "Điều Hòa Daikin": {
        "C1": "Lỗi bo mạch dàn lạnh hoặc bo mạch quạt ",
        "C3": "Lỗi hệ thống cảm biến nước xả (dàn lạnh) ",
        "C4": "Lỗi nhiệt điện trở đường ống lỏng dàn lạnh hoặc lỏng kết nối ",
        "C5": "Lỗi nhiệt điện trở đường ống hơi dàn lạnh hoặc lỏng kết nối ",
        "C9": "Lỗi nhiệt điện trở gió hồi dàn lạnh hoặc lỏng kết nối ",
        "E0": "Thiết bị bảo vệ dàn nóng tác động (Công tắc cao áp, Moto quạt/máy nén quá tải...) ",
        "E1": "Lỗi bo mạch dàn nóng ",
        "E7": "Lỗi moto quạt dàn nóng hoặc bo mạch moto quạt ",
        "F3": "Nhiệt độ ống đẩy dàn nóng bất thường, thiếu môi chất lạnh hoặc lỗi nhiệt điện trở ống đẩy ",
        "U0": "Thiếu môi chất lạnh, hư van tiết lưu điện tử hoặc ống dẫn môi chất lạnh bị nghẹt ",
        "U4": "Lỗi truyền tín hiệu giữa dàn nóng và dàn lạnh hoặc lỏng kết nối F1/F2 "
    },
    "Điều Hòa Panasonic": {
        "11H": "Lỗi đường dữ liệu giữa khối trong và ngoài ",
        "14H": "Lỗi cảm biến nhiệt độ phòng ",
        "16H": "Dòng điện tải máy nén quá thấp ",
        "19H": "Lỗi quạt dàn lạnh ",
        "28H": "Lỗi cảm biến giàn nóng. \n🛠 XỬ LÝ: Kiểm tra jack cắm; Đo điện trở (Khoảng 3KΩ ở 30°C); Hơ nóng cảm biến xem trị số có giảm không ",
        "H11": "Lỗi truyền tín hiệu giữa khối trong và ngoài nhà ",
        "H97": "Động cơ moto quạt khối ngoài trời bị khoá, kẹt ",
        "F91": "Rò rỉ môi chất lạnh, chu kỳ làm lạnh kém ",
        "F97": "Nhiệt độ máy nén cao bất thường, máy nén tự tắt ",
        "28H": "Lỗi cảm biến giàn nóng (H28). \n🛠 HD: Kiểm tra jack cắm; đo điện trở (khoảng 3KΩ ở 30°C); hơ nóng cảm biến xem điện trở giảm không.",
        "H11": "Lỗi truyền tín hiệu giữa khối trong và ngoài nhà. \n🛠 HD: Kiểm tra dây số 3.",
        "F91": "Rò rỉ môi chất lạnh, chu kỳ làm lạnh kém.",
        "F97": "Nhiệt độ máy nén cao bất thường, máy nén tự tắt."
    },
    "Bếp Từ": {
        "Midea/Kangaroo": {
            "E0": "Chưa có nồi hoặc nồi không phù hợp. \n🛠 HD: Đổi nồi có đáy nhiễm từ (hít nam châm).",
            "E1": "Quá nhiệt hoặc bếp quá tải. \n🛠 HD: Kiểm tra quạt gió, để bếp nghỉ 10 phút.",
            "E2": "Cảm biến nhiệt độ mặt kính lỗi. \n🛠 HD: Kiểm tra Sensor nhiệt trung tâm mặt kính.",
            "E3": "Điện áp quá cao (>250V). \n🛠 HD: Kiểm tra nguồn điện lưới.",
            "E4": "Điện áp quá thấp (<170V). \n🛠 HD: Sử dụng ổn áp.",
            "E6": "Lỗi cảm biến IGBT (Quá nhiệt công suất). \n🛠 HD: Thay keo tản nhiệt hoặc kiểm tra quạt."
        },
        "Sunhouse/Sanaky": {
            "E1": "Điện áp yếu. \n🛠 HD: Kiểm tra nguồn cấp.",
            "E2": "Nhiệt độ bếp quá cao. \n🛠 HD: Vệ sinh quạt, lỗ thông gió.",
            "E5": "Hở mạch cảm biến nhiệt mặt bếp. \n🛠 HD: Thay Sensor nhiệt.",
            "E0": "Lỗi nhận nồi. \n🛠 HD: Kiểm tra tụ 5uF hoặc điện trở hồi tiếp."
        },
        "Bosch/Hãng Âu": {
            "E01/E02": "Lỗi module công suất. \n🛠 HD: Kiểm tra IGBT và cầu chỉnh lưu.",
            "F0": "Lỗi truyền thông. \n🛠 HD: Kiểm tra cáp nối giữa các board mạch."
        }
    },
    "Máy Giặt": {
        "Electrolux": {
            "E10": "Lỗi cấp nước. HD: Vệ sinh van cấp.",
            "E20": "Lỗi thoát nước. HD: Kiểm tra bơm xả."
        }
    }
}

# --- GIAO DIỆN CHÍNH ---
user = st.session_state['auth']
st.markdown(f"""
    <div class="user-info">
        👤 <b>{user['ten']}</b> | 📦 Gói: <b>{user['loai']}</b> | 📅 Hạn: <b>{user['han']}</b>
    </div>
""", unsafe_allow_html=True)

# MENU NÚT BẤM LỚN
c1, c2 = st.columns(2)
with c1:
    if st.button("🔍 TRA MÃ & HƯỚNG DẪN", use_container_width=True): st.session_state.page = "TRA"
with c2:
    if st.button("🧠 CHẨN ĐOÁN AI", use_container_width=True): st.session_state.page = "AI"

c3, c4 = st.columns(2)
with c3:
    if st.button("➕ THÊM MÃ MỚI", use_container_width=True): st.session_state.page = "THEM"
with c4:
    if st.button("💳 GIA HẠN / MUA GÓI", use_container_width=True): st.session_state.page = "GIA"

# --- XỬ LÝ CHỨC NĂNG ---
if st.session_state.page == "TRA":
    st.divider()
    st.subheader("🔍 TRA CỨU & KHẮC PHỤC")
    loai = st.selectbox("CHỌN THIẾT BỊ:", list(DATA_FULL.keys()))
    hang = st.selectbox(f"CHỌN HÃNG {loai}:", list(DATA_FULL[loai].keys()))
    ma = st.text_input("NHẬP MÃ LỖI:").upper().strip()
    
    if st.button("TÌM KIẾM NGAY", use_container_width=True):
        if ma in DATA_FULL[loai][hang]:
            st.warning(f"🛠 **{hang} {ma}:**")
            st.success(DATA_FULL[loai][hang][ma])
        else:
            found = [x for x in st.session_state.user_db if x['ma']==ma and x['hang']==hang]
            if found: st.success(f"📌 **Kinh nghiệm cá nhân:**\n\n{found[0]['hd']}")
            else: st.error("Chưa có mã này trong kho dữ liệu!")

elif st.session_state.page == "AI":
    st.divider()
    st.subheader("🧠 CHẨN ĐOÁN AI CHUYÊN SÂU")
    benh = st.text_area("Mô tả bệnh (Vd: Bếp từ không nhận nồi, Điều hòa không mát...):")
    if st.button("AI PHÂN TÍCH", use_container_width=True):
        st.info("🤖 AI Gợi ý: Hãy kiểm tra linh kiện công suất (IGBT/Block) và các cảm biến nhiệt độ liên quan.")

elif st.session_state.page == "THEM":
    st.divider()
    st.subheader("➕ LÀM GIÀU DỮ LIỆU KỸ THUẬT")
    t_loai = st.selectbox("Thiết bị:", ["Điều Hòa", "Bếp Từ", "Máy Giặt"])
    t_hang = st.text_input("Hãng máy:")
    t_ma = st.text_input("Mã lỗi:").upper().strip()
    t_hd = st.text_area("Hướng dẫn sửa thực tế:")
    if st.button("LƯU VÀO KHO DỮ LIỆU", use_container_width=True):
        st.session_state.user_db.append({'loai': t_loai, 'hang': t_hang, 'ma': t_ma, 'hd': t_hd})
        st.success("✅ Đã lưu thành công!")

elif st.session_state.page == "GIA":
    st.divider()
    st.subheader("💳 CHỌN GÓI BẢN QUYỀN")
    st.image("https://img.vietqr.io/image/ICB-104881077679-compact2.png?amount=299000&addInfo=GIAHAN")

# NÚT ĐĂNG XUẤT
st.divider()
if st.button("🚪 Đăng xuất", use_container_width=True):
    st.session_state.auth = None
    st.rerun()

st.caption("BA DUY TECH v40.0 - CHUYÊN GIA SỬA CHỮA ĐIỆN LẠNH & NHÀ BẾP")

