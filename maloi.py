import streamlit as st

# 1. CẤU HÌNH HỆ THỐNG
st.set_page_config(page_title="BA DUY TECH PRO 2026", layout="centered")

# --- CSS LÀM RỰC MÀU CÁC THANH TOOL (NHÃN ĐỎ, CHỮ TRẮNG) ---
st.markdown("""
    <style>
    div.stButton > button {
        background-color: #007BFF !important;
        color: white !important;
        border-radius: 12px !important;
        font-weight: bold !important;
        height: 3.5em !important;
    }
    div.stButton > button:hover {
        background-color: #FF8C00 !important;
    }
    /* Fix màu nhãn Tool để cực kỳ dễ nhìn */
    .stSelectbox label, .stTextInput label {
        color: #FFFFFF !important;
        background-color: #D32F2F !important;
        padding: 5px 15px !important;
        border-radius: 8px !important;
        font-weight: bold !important;
    }
    .user-info {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 10px;
        border-left: 5px solid #007BFF;
        margin-bottom: 20px;
    }
    .result-card {
        background-color: #E8F5E9;
        padding: 15px;
        border-radius: 10px;
        border-left: 10px solid #2E7D32;
    }
    </style>
    """, unsafe_allow_html=True)

# Khởi tạo session state
if 'auth' not in st.session_state: st.session_state['auth'] = None
if 'page' not in st.session_state: st.session_state['page'] = "HOME"
if 'user_db' not in st.session_state: st.session_state['user_db'] = []

# --- DỮ LIỆU TỔNG HỢP ---
DATA_FULL = {
    "Điều Hòa": {
        "LG Inverter": {
            "CH01": "Hỏng cảm biến giàn lạnh", "CH05": "Lỗi kết nối giàn nóng/lạnh.",
            "CH21": "Lỗi IC Công Suất.", "CH61": "Giàn nóng không giải nhiệt được.",
            "CH65": "Hỏng IC nguồn đuôi nóng."
        },
        "Daikin": {
            "U0": "Thiếu Gas.", "U4": "Lỗi truyền tín hiệu nóng/lạnh.",
            "E7": "Lỗi moto quạt dàn nóng.", "F3": "Nhiệt độ ống đẩy bất thường."
        },
        "Panasonic": {
            "28H": "Lỗi cảm biến giàn nóng (H28). 🛠 HD: Đo trở 3KΩ ở 30°C.",
            "H11": "Lỗi truyền tín hiệu (Dây số 3).", "F91": "Rò rỉ môi chất lạnh."
        }
    },
    "Bếp Từ": {
        "Sunhouse": {
            "E0": "Lỗi mạch nhận nồi. 🛠 HD: Kiểm tra tụ 5uF, 0.33uF.",
            "E1": "Điện áp yếu.", "E2": "Nhiệt độ nồi quá cao.", "E5": "Cảm biến mặt kính hở."
        },
        "Sanaky": {
            "E0": "Không nồi/Sai nồi.", "E1": "Áp thấp.", "E2": "Áp cao.", "E3": "Quá nhiệt mặt kính."
        },
        "Midea": {
            "E1": "Bếp quá nhiệt.", "E2": "Cảm biến kính lỗi.", "E3": "Quá áp.", "E6": "Lỗi IGBT."
        },
        "Kangaroo": {
            "E0": "Không nhận nồi.", "E1": "Quá nóng.", "E2": "Lỗi cảm biến nhiệt."
        },
        "Bosch": {
            "E01": "Lỗi công suất.", "F0": "Lỗi truyền thông.", "U1": "Điện áp lỗi."
        }
    }
}

# --- ĐĂNG NHẬP ---
if st.session_state['auth'] is None:
    st.title("🔐 TRỢ LÝ BA DUY TECH")
    ma = st.text_input("Nhập mã kích hoạt:", type="password")
    if st.button("XÁC NHẬN", use_container_width=True):
        if ma == "PRO-DUY-2025": st.session_state['auth'] = {"ten": "Ba Duy"}; st.rerun()
    st.stop()

# --- GIAO DIỆN CHÍNH ---
st.markdown(f'<div class="user-info">👤 Kỹ sư: <b>{st.session_state["auth"]["ten"]}</b></div>', unsafe_allow_html=True)

c1, c2 = st.columns(2)
with c1:
    if st.button("🔍 TRA MÃ & XỬ LÝ", use_container_width=True): st.session_state.page = "TRA"
with c2:
    if st.button("🧠 CHẨN ĐOÁN AI", use_container_width=True): st.session_state.page = "AI"

# --- LOGIC TRA CỨU (FIX LỖI CHỌN HÃNG) ---
if st.session_state.page == "TRA":
    st.divider()
    # Sử dụng key để tránh xung đột dữ liệu khi chuyển đổi
    loai_chon = st.selectbox("🛠 CHỌN THIẾT BỊ:", list(DATA_FULL.keys()), key="sb_thietbi")
    
    # Danh sách hãng sẽ thay đổi tương ứng theo thiết bị
    danh_sach_hang = list(DATA_FULL[loai_chon].keys())
    hang_chon = st.selectbox(f"🏭 CHỌN HÃNG {loai_chon}:", danh_sach_hang, key="sb_hang")
    
    ma_nhap = st.text_input("🔢 NHẬP MÃ LỖI:", key="ti_ma").upper().strip()
    
    if st.button("TÌM KIẾM", use_container_width=True):
        if ma_nhap in DATA_FULL[loai_chon][hang_chon]:
            ket_qua = DATA_FULL[loai_chon][hang_chon][ma_nhap]
            st.markdown(f'<div class="result-card"><b>✅ {hang_chon} - {ma_nhap}:</b><br>{ket_qua}</div>', unsafe_allow_html=True)
        else:
            st.error("❌ Không tìm thấy mã này.")

elif st.session_state.page == "AI":
    st.divider()
    st.subheader("🧠 CHẨN ĐOÁN AI")
    st.text_area("Mô tả bệnh:")
    st.button("PHÂN TÍCH")

st.divider()
if st.button("🚪 Thoát"): st.session_state.auth = None; st.rerun()
