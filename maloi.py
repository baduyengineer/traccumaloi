import streamlit as st

# 1. CẤU HÌNH HỆ THỐNG
st.set_page_config(page_title="BA DUY TECH PRO 2026", layout="centered")

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
    ma = st.text_input("Nhập mã kích hoạt (Vd: DUY-FREE):", type="password").strip()
    if st.button("XÁC NHẬN VÀO", use_container_width=True):
        if ma in USERS:
            st.session_state['auth'] = USERS[ma]
            st.rerun()
        else: st.error("Mã không đúng! Vui lòng liên hệ Admin để mua gói.")
    st.stop()

# --- DỮ LIỆU TỔNG HỢP SIÊU KHỦNG ---
DATA_FULL = {
    "Điều Hòa": {
        "Panasonic": {
            "H11": "Lỗi kết nối lạnh/nóng. HD: Kiểm tra dây tín hiệu số 3, bo nóng.",
            "H16": "Dòng tải thấp. HD: Kiểm tra gas, block, biến dòng bo nóng.",
            "F95": "Quá nhiệt dàn nóng. HD: Vệ sinh dàn, kiểm tra quạt nóng."
        },
        "Daikin": {
            "U4": "Lỗi tín hiệu truyền thông. HD: Kiểm tra dây số 3, bo mạch.",
            "L5": "Quá dòng máy nén. HD: Kiểm tra IPM, block.",
            "U0": "Thiếu gas. HD: Kiểm tra rò rỉ và áp suất."
        }
    },
    "Máy Giặt": {
        "Electrolux": {
            "E10": "Lỗi cấp nước. HD: Vệ sinh van cấp, kiểm tra áp lực.",
            "E20": "Lỗi thoát nước. HD: Kiểm tra bơm xả, ống thoát.",
            "E40": "Lỗi cửa. HD: Thay khóa cửa, kiểm tra bo."
        },
        "LG": {
            "IE": "Không vào nước. HD: Kiểm tra van cấp.",
            "OE": "Không thoát nước. HD: Kiểm tra bơm xả."
        }
    },
    "Bếp Từ": {
        "Sunhouse": {"E0": "Không nhận nồi.", "E1": "Quá nhiệt cảm biến."},
        "Kangaroo": {"E1": "Lỗi cảm biến kính.", "E2": "Quá nhiệt IGBT."}
    }
}

# --- GIAO DIỆN CHÍNH ---
user = st.session_state['auth']
st.success(f"👤 {user['ten']} | 📦 Gói: {user['loai']} | 📅 Hạn: {user['han']}")

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
    loai = st.selectbox("Chọn thiết bị:", list(DATA_FULL.keys()))
    hang = st.selectbox(f"Chọn hãng {loai}:", list(DATA_FULL[loai].keys()))
    ma = st.text_input("Nhập mã lỗi:").upper().strip()
    if st.button("TÌM KIẾM", use_container_width=True):
        if ma in DATA_FULL[loai][hang]:
            st.info(f"🛠 **{hang} {ma}:**\n\n{DATA_FULL[loai][hang][ma]}")
        else:
            # Tra cứu trong dữ liệu thợ tự thêm
            found = [x for x in st.session_state.user_db if x['ma']==ma and x['hang']==hang]
            if found: st.success(f"📌 **Kinh nghiệm cá nhân:**\n\n{found[0]['hd']}")
            else: st.warning("Chưa có mã này. Hãy dùng AI hoặc tự thêm mã mới!")

elif st.session_state.page == "AI":
    st.divider()
    st.subheader("🧠 CHẨN ĐOÁN AI CHUYÊN SÂU")
    l_ai = st.selectbox("Loại máy:", list(DATA_FULL.keys()), key="ai_l")
    h_ai = st.selectbox("Hãng máy:", list(DATA_FULL[l_ai].keys()), key="ai_h")
    benh = st.text_area("Mô tả bệnh (Vd: Quạt không quay, có tiếng kêu lạ...):")
    if st.button("AI PHÂN TÍCH", use_container_width=True):
        if "nguồn" in benh.lower(): st.error(f"🤖 AI {h_ai}: Kiểm tra Cầu chì, IC nguồn, Biến áp xung.")
        elif "lạnh" in benh.lower(): st.warning(f"🤖 AI {h_ai}: Kiểm tra Gas, Sensor, Block và Tụ ngậm.")
        else: st.info(f"🤖 AI {h_ai}: Kiểm tra lệnh từ Bo mạch điều khiển chính.")

elif st.session_state.page == "THEM":
    st.divider()
    st.subheader("➕ LÀM GIÀU DỮ LIỆU KỸ THUẬT")
    t_loai = st.selectbox("Thiết bị:", ["Điều Hòa", "Máy Giặt", "Bếp Từ", "Tủ Lạnh"])
    t_hang = st.text_input("Hãng máy:")
    t_ma = st.text_input("Mã lỗi:").upper().strip()
    t_hd = st.text_area("Hướng dẫn sửa thực tế (Kinh nghiệm thợ):")
    if st.button("LƯU VÀO KHO DỮ LIỆU", use_container_width=True):
        st.session_state.user_db.append({'loai': t_loai, 'hang': t_hang, 'ma': t_ma, 'hd': t_hd})
        st.success("✅ Đã lưu thành công vào kho dữ liệu của bạn!")

elif st.session_state.page == "GIA":
    st.divider()
    st.subheader("💳 CHỌN GÓI BẢN QUYỀN PRO")
    goi = st.radio("Chọn gói muốn mua:", ["6 Tháng (199k)", "12 Tháng (299k)", "Vĩnh Viễn (499k)"])
    tien = "199000" if "6" in goi else "299000" if "12" in goi else "499000"
    st.image(f"https://img.vietqr.io/image/ICB-104881077679-compact2.png?amount={tien}&addInfo=GIAHAN%20{goi}")
    st.success(f"Dòng máy nhận tiền: Ngân hàng Công Thương (VietinBank)")

# NÚT ĐĂNG XUẤT
st.divider()
if st.button("🚪 Đăng xuất", use_container_width=True):
    st.session_state.auth = None
    st.rerun()

st.caption("BA DUY TECH v35.0 - NỀN TẢNG KỸ THUẬT SỐ 1 VIỆT NAM")
