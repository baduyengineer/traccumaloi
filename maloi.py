import streamlit as st

# 1. CẤU HÌNH GIAO DIỆN
st.set_page_config(page_title="BA DUY TECH PRO v32", layout="centered")

# KHỞI TẠO DỮ LIỆU
if 'auth' not in st.session_state: st.session_state['auth'] = None
if 'page' not in st.session_state: st.session_state['page'] = "HOME"
if 'user_db' not in st.session_state: st.session_state['user_db'] = []

USERS = {"PRO-DUY-2025": "Kỹ sư Ba Duy", "DUY-FREE": "Khách dùng thử"}

# --- ĐĂNG NHẬP ---
if st.session_state['auth'] is None:
    st.title("🔐 HỆ THỐNG BA DUY PRO")
    ma = st.text_input("Mã kích hoạt:", type="password").strip()
    if st.button("XÁC NHẬN VÀO", use_container_width=True):
        if ma in USERS:
            st.session_state['auth'] = USERS[ma]
            st.rerun()
        else: st.error("Mã không đúng!")
    st.stop()

# --- KHO DỮ LIỆU CHUYÊN SÂU ---
DATA_PRO = {
    "Điều Hòa": {
        "Panasonic": {
            "H11": "Lỗi kết nối lạnh/nóng. \nHD: Kiểm tra dây số 3, đo áp giao tiếp 15-30VDC.",
            "H16": "Dòng máy nén thấp. \nHD: Kiểm tra gas, biến dòng bo nóng, block.",
            "F95": "Quá nhiệt dàn nóng. \nHD: Vệ sinh dàn, kiểm tra quạt dàn nóng."
        },
        "Daikin": {
            "U4": "Lỗi tín hiệu lạnh/nóng. \nHD: Kiểm tra dây tín hiệu, cầu chì bo mạch.",
            "L5": "Quá dòng máy nén. \nHD: Kiểm tra IPM bo nóng, đo điện trở 3 pha block.",
            "U0": "Thiếu gas. \nHD: Kiểm tra rò rỉ và áp suất gas."
        }
    },
    "Máy Giặt": {
        "Electrolux": {
            "E10": "Lỗi cấp nước. \nHD: Vệ sinh van cấp, kiểm tra áp lực nước.",
            "E40": "Lỗi khóa cửa. \nHD: Thay khóa cửa, kiểm tra lệnh bo mạch."
        },
        "LG": {
            "IE": "Không vào nước. \nHD: Kiểm tra van cấp và bo mạch điều khiển.",
            "OE": "Không thoát nước. \nHD: Kiểm tra bơm xả và ống thoát."
        }
    },
    "Bếp Từ": {
        "Sunhouse": {"E0": "Không nhận nồi. \nHD: Kiểm tra tụ 5uF, điện trở hồi tiếp.", "E1": "Quá nhiệt cảm biến."},
        "Kangaroo": {"E1": "Lỗi cảm biến kính.", "E2": "Quá nhiệt IGBT. Kiểm tra quạt."}
    }
}

# --- MENU CHÍNH ---
st.success(f"👤 Chào {st.session_state['auth']}")
c1, c2 = st.columns(2)
with c1:
    if st.button("🔍 TRA MÃ & HD", use_container_width=True): st.session_state.page = "TRA"
with c2:
    if st.button("🧠 CHẨN ĐOÁN AI", use_container_width=True): st.session_state.page = "AI"

c3, c4 = st.columns(2)
with c3:
    if st.button("➕ THÊM MÃ MỚI", use_container_width=True): st.session_state.page = "THEM"
with c4:
    if st.button("🚪 ĐĂNG XUẤT", use_container_width=True):
        st.session_state.auth = None
        st.rerun()

# --- XỬ LÝ CHỨC NĂNG ---
if st.session_state.page == "TRA":
    st.divider()
    st.subheader("🔍 TRA CỨU NHANH")
    loai = st.selectbox("Chọn thiết bị:", list(DATA_PRO.keys()), key="tra_loai")
    hang = st.selectbox(f"Chọn hãng {loai}:", list(DATA_PRO[loai].keys()), key="tra_hang")
    ma = st.text_input("Nhập mã lỗi:").upper().strip()
    if st.button("XEM HƯỚNG DẪN", use_container_width=True):
        if ma in DATA_PRO[loai][hang]:
            st.info(f"🛠 **Giải pháp:**\n\n{DATA_PRO[loai][hang][ma]}")
        else:
            # Tra cứu trong kho thợ tự thêm
            found = [x for x in st.session_state.user_db if x['ma']==ma and x['hang']==hang]
            if found: st.success(f"📌 **Kinh nghiệm cá nhân:**\n\n{found[0]['hd']}")
            else: st.warning("Mã này chưa có. Hãy dùng mục 'Thêm mã mới'!")

elif st.session_state.page == "AI":
    st.divider()
    st.subheader("🧠 CHẨN ĐOÁN AI THEO HÃNG")
    # Khắc phục lỗi thiếu phân loại hãng ở ảnh image_e19055
    loai_ai = st.selectbox("Loại máy:", list(DATA_PRO.keys()), key="ai_loai")
    hang_ai = st.selectbox(f"Hãng sản xuất:", list(DATA_PRO[loai_ai].keys()), key="ai_hang")
    benh = st.text_area("Mô tả biểu hiện (Vd: Mất nguồn, quạt không quay...):")
    if st.button("AI PHÂN TÍCH", use_container_width=True):
        if "nguồn" in benh.lower():
            st.error(f"🤖 AI {hang_ai}: Kiểm tra Cầu chì, IC nguồn, Tụ lọc nguồn.")
        elif "lạnh" in benh.lower() or "nóng" in benh.lower():
            st.warning(f"🤖 AI {hang_ai}: Kiểm tra Gas, Sensor và Block.")
        else:
            st.info(f"🤖 AI {hang_ai}: Cần kiểm tra bo mạch điều khiển và các rơ-le.")

elif st.session_state.page == "THEM":
    st.divider()
    st.subheader("➕ LƯU KINH NGHIỆM SỬA CHỮA")
    t_loai = st.selectbox("Loại máy:", ["Điều Hòa", "Máy Giặt", "Bếp Từ"])
    t_hang = st.text_input("Hãng máy:")
    t_ma = st.text_input("Mã lỗi:").upper().strip()
    t_hd = st.text_area("Hướng dẫn sửa (Kinh nghiệm thợ):")
    if st.button("LƯU VÀO KHO", use_container_width=True):
        st.session_state.user_db.append({'loai': t_loai, 'hang': t_hang, 'ma': t_ma, 'hd': t_hd})
        st.success("Đã lưu! Duy có thể tra lại mã này ngay lập tức.")

st.divider()
st.caption("BA DUY TECH v32.0 - Hệ thống chẩn đoán chuyên nghiệp")
