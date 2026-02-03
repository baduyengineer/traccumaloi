import streamlit as st

# 1. CẤU HÌNH GIAO DIỆN
st.set_page_config(page_title="BA DUY TECH PRO 2026", layout="centered")

# CSS làm rực màu các thanh Tool và Menu
st.markdown("""
    <style>
    div.stButton > button {
        background-color: #007BFF !important;
        color: white !important;
        border-radius: 12px !important;
        font-weight: bold !important;
        height: 3.8em !important;
    }
    div.stButton > button:hover {
        background-color: #FF8C00 !important;
    }
    /* Tool nhãn rực rỡ (Nền đỏ chữ trắng) */
    .stSelectbox label, .stTextInput label, .stTextArea label {
        color: #FFFFFF !important;
        background-color: #D32F2F !important;
        padding: 6px 15px !important;
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
    .lock-box {
        background-color: #FFF3E0;
        padding: 20px;
        border-radius: 10px;
        border: 2px dashed #FF9800;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. KHỞI TẠO DỮ LIỆU
if 'auth' not in st.session_state: st.session_state['auth'] = None
if 'page' not in st.session_state: st.session_state['page'] = "HOME"
if 'user_db' not in st.session_state: st.session_state['user_db'] = []

USERS = {
    "PRO-DUY-2025": {"ten": "Kỹ sư Ba Duy", "loai": "Vĩnh viễn", "han": "Vô hạn"},
    "DUY-FREE": {"ten": "Khách dùng thử", "loai": "Free", "han": "3 ngày"}
}

# --- DỮ LIỆU MÃ LỖI (VÍ DỤ TẬP HỢP) ---
DATA_FULL = {
    "Điều Hòa": {
        "Panasonic": {
            "00H": "Bình thường", "28H": "Lỗi cảm biến giàn nóng.", "H11": "Lỗi truyền tín hiệu.", "F97": "Quá nhiệt máy nén."
        },
        "LG Inverter": {
            "CH05": "Lỗi kết nối.", "CH21": "Lỗi IC Công Suất.", "CH61": "Giàn nóng không giải nhiệt."
        },
        "Daikin": {
            "U0": "Thiếu Gas.", "U4": "Lỗi truyền tín hiệu.", "E7": "Lỗi quạt dàn nóng."
        }
    },
    "Bếp Từ": {
        "Sunhouse": {"E0": "Lỗi nhận nồi.", "E1": "Điện áp yếu.", "E5": "Lỗi cảm biến kính."},
        "Sanaky": {"E1": "Áp thấp.", "E2": "Áp cao.", "E3": "Quá nhiệt."},
        "Midea": {"E1": "Quá nhiệt.", "E6": "Lỗi IGBT."}
    }
}

# DANH SÁCH MÃ LỖI CHO PHÉP XEM Ở BẢN FREE
MA_FREE_ALLOWED = ["00H", "28H", "CH05", "U4", "E0", "E1"]

# --- ĐĂNG NHẬP ---
if st.session_state['auth'] is None:
    st.title("🔐 HỆ THỐNG TRỢ LÝ KỸ THUẬT BA DUY")
    ma_input = st.text_input("Nhập mã kích hoạt:", type="password").strip()
    if st.button("XÁC NHẬN VÀO HỆ THỐNG", use_container_width=True):
        if ma_input in USERS:
            st.session_state['auth'] = USERS[ma_input]; st.rerun()
        else: st.error("Mã sai!")
    st.stop()

# --- GIAO DIỆN CHÍNH ---
user = st.session_state['auth']
is_pro = user['loai'] == "Vĩnh viễn"

st.markdown(f'<div class="user-info-box">👤 <b>{user["ten"]}</b> | Gói: <b style="color:{"green" if is_pro else "red"}">{user["loai"]}</b></div>', unsafe_allow_html=True)

c1, c2 = st.columns(2); c3, c4 = st.columns(2)
with c1: 
    if st.button("🔍 TRA MÃ LỖI", use_container_width=True): st.session_state.page = "TRA"
with c2: 
    if st.button("🧠 CHẨN ĐOÁN AI", use_container_width=True): st.session_state.page = "AI"
with c3: 
    if st.button("➕ THÊM MÃ MỚI", use_container_width=True): st.session_state.page = "THEM"
with c4: 
    if st.button("💳 GIA HẠN", use_container_width=True): st.session_state.page = "GIA"

# --- XỬ LÝ TRA CỨU ---
if st.session_state.page == "TRA":
    st.divider()
    loai = st.selectbox("🛠 THIẾT BỊ:", list(DATA_FULL.keys()), key="l1")
    hang = st.selectbox(f"🏭 HÃNG {loai}:", list(DATA_FULL[loai].keys()), key="h1")
    ma = st.text_input("🔢 MÃ LỖI:").upper().strip()
    
    if st.button("TÌM KIẾM", use_container_width=True):
        if ma in DATA_FULL[loai][hang]:
            if is_pro or (ma in MA_FREE_ALLOWED):
                st.success(f"✅ **{hang} {ma}:** {DATA_FULL[loai][hang][ma]}")
            else:
                st.markdown(f"""
                <div class="lock-box">
                    <h3 style="color:#E65100;">🔒 MÃ LỖI CHUYÊN SÂU</h3>
                    <p>Bạn cần mua gói nâng cấp để xem được nhiều mã lỗi hơn và hướng dẫn sửa chữa chi tiết.</p>
                </div>
                """, unsafe_allow_html=True)
                st.image("https://img.vietqr.io/image/ICB-104881077679-compact2.png?amount=299000&addInfo=NANG_CAP_PRO")
        else: st.error("Mã chưa có trong kho.")

elif st.session_state.page == "AI":
    if not is_pro: st.warning("🔒 Chức năng AI yêu cầu gói PRO."); st.image("https://img.vietqr.io/image/ICB-104881077679-compact2.png?amount=299000&addInfo=MUA_AI")
    else: st.subheader("🧠 CHẨN ĐOÁN AI"); st.text_area("Mô tả bệnh:"); st.button("PHÂN TÍCH")

elif st.session_state.page == "GIA":
    st.subheader("💳 GIA HẠN GÓI")
    st.image("https://img.vietqr.io/image/ICB-104881077679-compact2.png?amount=299000&addInfo=GIAHAN_BADUY")

st.divider()
if st.button("🚪 Đăng xuất"): st.session_state.auth = None; st.rerun()
