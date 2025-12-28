import streamlit as st
from datetime import datetime

# 1. CẤU HÌNH HỆ THỐNG - TỐI ƯU MOBILE
st.set_page_config(page_title="BA DUY TECH PRO 2025", layout="centered")

if 'auth' not in st.session_state: st.session_state['auth'] = None
if 'page' not in st.session_state: st.session_state['page'] = "🏠 Trang chủ"

# DANH SÁCH NGƯỜI DÙNG
USERS = {
    "PRO-DUY-2025": {"ten": "Kỹ sư Ba Duy", "han": "2026-01-05"},
    "DUY-FREE-3D": {"ten": "Khách dùng thử", "han": "2025-12-30"},
}

# --- MÀN HÌNH ĐĂNG NHẬP ---
if st.session_state['auth'] is None:
    st.title("🔐 HỆ THỐNG BA DUY")
    ma = st.text_input("Nhập mã kích hoạt:", type="password").strip()
    if st.button("XÁC NHẬN VÀO", use_container_width=True):
        if ma in USERS:
            st.session_state['auth'] = USERS[ma]
            st.rerun()
        else: st.error("Sai mã kích hoạt!")
    st.stop()

# --- HEADER & NAVIGATION ---
user = st.session_state['auth']
st.success(f"👤 {user['ten']} | 📅 Hạn: {user['han']}")

# KHO DỮ LIỆU TỔNG HỢP SIÊU KHỦNG
DATA_TECH = {
    "Điều Hòa": {
        "Panasonic": {
            "H11": "Lỗi kết nối dàn nóng/lạnh. Kiểm tra dây tín hiệu, bo mạch.",
            "H15": "Lỗi cảm biến nhiệt máy nén. Kiểm tra cảm biến đầu đẩy.",
            "H16": "Dòng tải thấp. Kiểm tra gas, block.",
            "F91": "Lỗi dòng tải máy nén. Kiểm tra bo công suất.",
            "F93": "Lỗi tốc độ máy nén. Kiểm tra block hoặc bo Inverter.",
            "F95": "Quá nhiệt dàn nóng. Kiểm tra quạt hoặc dàn bẩn."
        },
        "Daikin": {
            "U4": "Lỗi truyền tín hiệu nóng/lạnh. Kiểm tra dây số 3.",
            "U0": "Thiếu gas hoặc nghẹt hệ thống lạnh.",
            "E7": "Lỗi motor quạt dàn nóng. Kiểm tra quạt, bo nóng.",
            "L5": "Lỗi máy nén Inverter (quá dòng). Kiểm tra block.",
            "F3": "Nhiệt độ ống đẩy cao. Kiểm tra gas, van tiết lưu."
        }
    },
    "Máy Giặt": {
        "Electrolux": {
            "E10": "Không cấp nước. Kiểm tra van cấp, lưới lọc.",
            "E20": "Không thoát nước. Kiểm tra bơm xả, đường ống.",
            "E40": "Lỗi công tắc cửa. Kiểm tra khóa hoặc chốt cửa.",
            "E90": "Lỗi phần mềm/bo mạch hiển thị.",
            "EH0": "Nguồn điện không ổn định. Kiểm tra điện áp."
        },
        "LG": {
            "IE": "Lỗi cấp nước. Kiểm tra áp lực nước.",
            "OE": "Lỗi thoát nước. Kiểm tra bơm hoặc ống tắc.",
            "DE": "Lỗi cửa mở. Kiểm tra công tắc cửa.",
            "PE": "Lỗi cảm biến áp lực phao nước.",
            "AE": "Lỗi rò rỉ nước bên trong máy."
        }
    },
    "Bếp Từ": {
        "Sunhouse": {"E0": "Không nhận nồi.", "E1": "Quá nhiệt cảm biến.", "E2": "Điện áp quá cao."},
        "Kangaroo": {"E1": "Hỏng cảm biến mặt kính.", "E2": "Quá nhiệt IGBT. Kiểm tra quạt."}
    }
}

# --- GIAO DIỆN CHÍNH (NÚT BẤM TO) ---
st.divider()
c1, c2 = st.columns(2)
with c1:
    if st.button("🔍 TRA MÃ LỖI", use_container_width=True): st.session_state.page = "TRA_MA"
with c2:
    if st.button("🧠 CHẨN ĐOÁN AI", use_container_width=True): st.session_state.page = "AI"

c3, c4 = st.columns(2)
with c3:
    if st.button("📚 SƠ ĐỒ PDF", use_container_width=True): st.session_state.page = "PDF"
with c4:
    if st.button("💳 GIA HẠN", use_container_width=True): st.session_state.page = "GIA_HAN"

# --- XỬ LÝ TRANG ---
if st.session_state.page == "TRA_MA":
    st.header("🔍 TRA CỨU CHI TIẾT")
    loai = st.selectbox("Chọn thiết bị:", list(DATA_TECH.keys()))
    hang = st.selectbox(f"Chọn hãng {loai}:", list(DATA_TECH[loai].keys()))
    ma = st.text_input("Nhập mã lỗi:").upper().strip()
    if st.button("TÌM KIẾM", use_container_width=True):
        if ma in DATA_TECH[loai][hang]:
            st.success(f"🛠 **{hang} {ma}:** {DATA_TECH[loai][hang][ma]}")
        else: st.warning("Mã này chưa cập nhật.")

elif st.session_state.page == "AI":
    st.header("🧠 CHẨN ĐOÁN AI CHUYÊN NGHIỆP")
    st.info("Nhập biểu hiện bệnh để AI phân tích nguyên nhân tiềm ẩn.")
    loai_ai = st.selectbox("Máy đang hỏng:", list(DATA_TECH.keys()))
    benh = st.text_area("Mô tả biểu hiện (Vd: Quạt chạy nhưng block không rung, có mùi khét...):")
    
    if st.button("PHÂN TÍCH CHUYÊN SÂU", use_container_width=True):
        # MÔ PHỎNG LOGIC CHẨN ĐOÁN CHUYÊN NGHIỆP
        if "nguồn" in benh.lower():
            st.warning("🤖 AI Gợi ý: Kiểm tra cầu chì, biến áp xung và IC nguồn (thường hỏng TNY264/VIPER12A).")
        elif "nóng" in benh.lower() or "lạnh" in benh.lower():
            st.warning("🤖 AI Gợi ý: Kiểm tra tụ ngậm, block hoặc cảm biến nhiệt độ (Sensor).")
        else:
            st.info("🤖 AI Gợi ý: Cần kiểm tra bo mạch điều khiển trung tâm và các rơ-le lệnh.")

elif st.session_state.page == "GIA_HAN":
    st.subheader("💳 GIA HẠN BẢN QUYỀN")
    st.image("https://img.vietqr.io/image/ICB-104881077679-compact2.png?amount=500000&addInfo=GIAHAN")

# NÚT THOÁT
st.divider()
if st.button("🚪 Đăng xuất", use_container_width=True):
    st.session_state.auth = None
    st.rerun()
