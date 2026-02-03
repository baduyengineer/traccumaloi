import streamlit as st

# 1. CẤU HÌNH GIAO DIỆN
st.set_page_config(page_title="BA DUY TECH PRO 2026", layout="centered")

# CSS làm rực màu các thanh Tool và Menu
st.markdown("""
    <style>
    /* Nút Menu chính 4 ô */
    div.stButton > button {
        background-color: #007BFF !important;
        color: white !important;
        border-radius: 12px !important;
        border: 2px solid #0056b3 !important;
        font-weight: bold !important;
        height: 4em !important;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    div.stButton > button:hover {
        background-color: #FF8C00 !important;
        border: 2px solid #e67e00 !important;
    }
    /* Làm rực màu nhãn của các Tool tra cứu */
    .stSelectbox label, .stTextInput label, .stTextArea label {
        color: #FFFFFF !important;
        background-color: #D32F2F !important;
        padding: 5px 15px !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        font-size: 16px !important;
    }
    .user-info-box {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        border-left: 8px solid #007BFF;
        margin-bottom: 20px;
    }
    .result-card {
        background-color: #E8F5E9;
        padding: 20px;
        border-radius: 12px;
        border-left: 10px solid #2E7D32;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. KHỞI TẠO DỮ LIỆU HỆ THỐNG
if 'auth' not in st.session_state: st.session_state['auth'] = None
if 'page' not in st.session_state: st.session_state['page'] = "HOME"
if 'user_db' not in st.session_state: st.session_state['user_db'] = []

# DANH SÁCH TÀI KHOẢN (BẢN CŨ)
USERS = {
    "PRO-DUY-2025": {"ten": "Kỹ sư Ba Duy", "loai": "Vĩnh viễn", "han": "Vô hạn"},
    "DUY-FREE": {"ten": "Khách dùng thử", "loai": "Free", "han": "3 ngày"}
}

# --- MÀN HÌNH ĐĂNG NHẬP ---
if st.session_state['auth'] is None:
    st.title("🔐 HỆ THỐNG TRỢ LÝ KỸ THUẬT BA DUY")
    ma_input = st.text_input("Nhập mã kích hoạt:", type="password").strip()
    if st.button("XÁC NHẬN VÀO HỆ THỐNG", use_container_width=True):
        if ma_input in USERS:
            st.session_state['auth'] = USERS[ma_input]
            st.rerun()
        else: st.error("Mã không đúng! Vui lòng liên hệ Admin.")
    st.stop()

# --- KHO DỮ LIỆU TỔNG HỢP (TÁCH RIÊNG HÃNG) ---
DATA_FULL = {
    "Điều Hòa": {
        "Panasonic": {
            "28H": "Lỗi cảm biến giàn nóng (H28). 🛠 HD: Kiểm tra jack; đo trở (3KΩ ở 30°C); hơ nóng xem trở có giảm không.",
            "H11": "Lỗi truyền tín hiệu giữa dàn nóng/lạnh. 🛠 HD: Kiểm tra dây số 3.",
            "F91": "Rò rỉ môi chất lạnh. 🛠 HD: Kiểm tra Gas.",
            "F97": "Nhiệt độ máy nén cao bất thường."
        },
        "LG Inverter": {
            "CH05": "Lỗi kết nối giàn nóng/lạnh. 🛠 HD: Kiểm tra dây tín hiệu.",
            "CH21": "Lỗi IC Công Suất (IPM). 🛠 HD: Kiểm tra Block.",
            "CH61": "Giàn nóng không giải nhiệt được. 🛠 HD: Vệ sinh dàn nóng."
        },
        "Daikin": {
            "U4": "Lỗi truyền tín hiệu nóng/lạnh. 🛠 HD: Kiểm tra dây F1-F2.",
            "U0": "Thiếu Gas. 🛠 HD: Kiểm tra rò rỉ.",
            "E7": "Lỗi moto quạt dàn nóng."
        }
    },
    "Bếp Từ": {
        "Sunhouse": {
            "E0": "Lỗi mạch nhận nồi. 🛠 HD: Kiểm tra tụ 5uF, 0.33uF và điện trở hồi tiếp.",
            "E1": "Điện áp yếu. 🛠 HD: Kiểm tra nguồn cấp.",
            "E2": "Nhiệt độ nồi quá cao. 🛠 HD: Vệ sinh quạt, thông gió."
        },
        "Sanaky": {
            "E0": "Không nồi/Sai nồi.",
            "E1": "Áp thấp.",
            "E3": "Quá nhiệt mặt kính."
        },
        "Midea": {
            "E1": "Bếp quá nhiệt.",
            "E3": "Quá áp (>250V).",
            "E6": "Lỗi cảm biến công suất IGBT."
        },
        "Kangaroo": {
            "E0": "Không nhận nồi.",
            "E2": "Lỗi cảm biến nhiệt."
        }
    }
}

# --- GIAO DIỆN CHÍNH ---
user = st.session_state['auth']
st.markdown(f"""
    <div class="user-info-box">
        👤 <b>{user['ten']}</b> | 📦 Gói: <b>{user['loai']}</b> | 📅 Hạn: <b>{user['han']}</b>
    </div>
""", unsafe_allow_html=True)

# MENU 4 NÚT LỚN (GIỮ NGUYÊN BẢN CŨ)
c1, c2 = st.columns(2)
with c1:
    if st.button("🔍 TRA MÃ & XỬ LÝ", use_container_width=True): st.session_state.page = "TRA"
with c2:
    if st.button("🧠 CHẨN ĐOÁN AI", use_container_width=True): st.session_state.page = "AI"

c3, c4 = st.columns(2)
with c3:
    if st.button("➕ THÊM MÃ MỚI", use_container_width=True): st.session_state.page = "THEM"
with c4:
    if st.button("💳 MUA GÓI / GIA HẠN", use_container_width=True): st.session_state.page = "GIA"

# --- LOGIC CÁC TRANG ---
if st.session_state.page == "TRA":
    st.divider()
    # Fix lỗi chọn thiết bị/hãng bằng key riêng
    loai = st.selectbox("🛠 CHỌN LOẠI MÁY:", list(DATA_FULL.keys()), key="fix_loai")
    hang = st.selectbox(f"🏭 CHỌN HÃNG {loai}:", list(DATA_FULL[loai].keys()), key="fix_hang")
    ma = st.text_input("🔢 NHẬP MÃ LỖI:").upper().strip()
    
    if st.button("TÌM KIẾM NGAY", use_container_width=True):
        if ma in DATA_FULL[loai][hang]:
            st.markdown(f'<div class="result-card"><b>✅ {hang} {ma}:</b><br><br>{DATA_FULL[loai][hang][ma]}</div>', unsafe_allow_html=True)
        else:
            # Kiểm tra trong kho người dùng tự thêm
            found = [x for x in st.session_state.user_db if x['ma']==ma and x['hang']==hang]
            if found: st.success(f"📌 **Kinh nghiệm cá nhân:**\n\n{found[0]['hd']}")
            else: st.error("❌ Mã lỗi này chưa có trong dữ liệu.")

elif st.session_state.page == "AI":
    st.divider()
    st.subheader("🧠 CHẨN ĐOÁN AI CHUYÊN SÂU")
    benh = st.text_area("Mô tả bệnh (Vd: Quạt chạy nhưng block không rung...):")
    if st.button("PHÂN TÍCH BỆNH", use_container_width=True):
        st.info("🤖 AI Gợi ý: Kiểm tra khối nguồn, tụ khởi động và các cảm biến liên quan.")

elif st.session_state.page == "THEM":
    st.divider()
    st.subheader("➕ LƯU KHO KINH NGHIỆM")
    t_loai = st.selectbox("Thiết bị:", ["Điều Hòa", "Bếp Từ", "Máy Giặt"])
    t_hang = st.text_input("Hãng máy:")
    t_ma = st.text_input("Mã lỗi:").upper().strip()
    t_hd = st.text_area("Cách bạn đã sửa thành công:")
    if st.button("LƯU VÀO KHO CỦA TÔI", use_container_width=True):
        st.session_state.user_db.append({'loai': t_loai, 'hang': t_hang, 'ma': t_ma, 'hd': t_hd})
        st.success("✅ Đã lưu thành công!")

elif st.session_state.page == "GIA":
    st.divider()
    st.subheader("💳 GIA HẠN GÓI DỊCH VỤ")
    st.warning("Quét mã QR để nâng cấp hoặc gia hạn gói PRO")
    st.image("https://img.vietqr.io/image/ICB-104881077679-compact2.png?amount=299000&addInfo=GIAHAN_BADUY")
    st.info("Nội dung chuyển khoản: GIA HAN [TEN CUA BAN]")

# NÚT ĐĂNG XUẤT
st.divider()
if st.button("🚪 Đăng xuất", use_container_width=True):
    st.session_state.auth = None
    st.rerun()

st.caption("BA DUY TECH v45.2 - ĐẦY ĐỦ TÍNH NĂNG PRO")
