import streamlit as st

# 1. CẤU HÌNH GIAO DIỆN (TỐI ƯU CHO ĐIỆN THOẠI)
st.set_page_config(page_title="BA DUY TECH PRO v31", layout="centered")

# KHỞI TẠO BỘ NHỚ TỰ THÊM MÃ
if 'auth' not in st.session_state: st.session_state['auth'] = None
if 'page' not in st.session_state: st.session_state['page'] = "HOME"
if 'user_data' not in st.session_state: st.session_state['user_data'] = []

# DANH SÁCH NGƯỜI DÙNG
USERS = {"PRO-DUY-2025": "Kỹ sư Ba Duy", "DUY-FREE": "Khách dùng thử"}

# --- MÀN HÌNH ĐĂNG NHẬP ---
if st.session_state['auth'] is None:
    st.title("🔐 TRỢ LÝ KỸ THUẬT BA DUY PRO")
    ma = st.text_input("Nhập mã kích hoạt:", type="password").strip()
    if st.button("XÁC NHẬN VÀO", use_container_width=True):
        if ma in USERS:
            st.session_state['auth'] = USERS[ma]
            st.rerun()
        else: st.error("Sai mã!")
    st.stop()

# --- DỮ LIỆU TỔNG HỢP & HƯỚNG DẪN SỬA ---
DATA_HUONG_DAN = {
    "Điều Hòa": {
        "Panasonic": {
            "H11": "Lỗi kết nối lạnh/nóng. \nHD: 1. Kiểm tra dây số 3. 2. Đo áp giao tiếp (15-30VDC). 3. Kiểm tra bo nóng.",
            "H16": "Dòng máy nén thấp. \nHD: 1. Kiểm tra thiếu gas. 2. Kiểm tra biến dòng bo nóng. 3. Kiểm tra block.",
            "F95": "Quá nhiệt dàn nóng. \nHD: 1. Vệ sinh dàn nóng. 2. Kiểm tra quạt dàn nóng. 3. Kiểm tra cảm biến dàn.",
            "H97": "Lỗi quạt dàn nóng. \nHD: 1. Kiểm tra kẹt cánh quạt. 2. Kiểm tra motor quạt. 3. Kiểm tra nguồn cấp quạt."
        },
        "Daikin": {
            "U4": "Lỗi tín hiệu nóng/lạnh. \nHD: 1. Kiểm tra dây truyền tín hiệu. 2. Kiểm tra cầu chì bo. 3. Thay bo mạch.",
            "L5": "Quá dòng máy nén. \nHD: 1. Đo điện trở 3 pha block. 2. Kiểm tra block kẹt cơ. 3. Hỏng IPM bo nóng.",
            "U0": "Thiếu gas/Nghẹt hệ thống. \nHD: 1. Kiểm tra rò rỉ gas. 2. Kiểm tra van tiết lưu. 3. Kiểm tra phin lọc.",
            "E7": "Lỗi motor quạt nóng. \nHD: 1. Kiểm tra quạt có quay tay được không. 2. Kiểm tra tụ quạt hoặc bo mạch."
        }
    },
    "Máy Giặt": {
        "Electrolux": {
            "E10": "Không cấp nước. \nHD: 1. Kiểm tra vòi nước. 2. Vệ sinh lưới lọc van cấp. 3. Thay van cấp.",
            "E20": "Lỗi xả nước. \nHD: 1. Vệ sinh hố bơm xả. 2. Kiểm tra bơm xả. 3. Kiểm tra ống thoát.",
            "E40": "Lỗi khóa cửa. \nHD: 1. Đóng lại cửa. 2. Thay khóa cửa. 3. Kiểm tra lệnh bo mạch."
        },
        "LG": {
            "IE": "Lỗi cấp nước. \nHD: Kiểm tra van cấp và áp lực nước nhà khách.",
            "OE": "Lỗi xả nước. \nHD: Kiểm tra bơm xả và đường ống xả xem có tắc không."
        }
    },
    "Bếp Từ": {
        "Sunhouse": {"E0": "Không nhận nồi. \nHD: Kiểm tra đáy nồi, tụ 5uF, điện trở hồi tiếp.", "E1": "Quá nhiệt cảm biến."},
        "Kangaroo": {"E1": "Lỗi cảm biến kính. \nHD: Thay cảm biến mặt kính.", "E2": "Quá nhiệt IGBT."}
    }
}

# --- GIAO DIỆN ĐIỀU HƯỚNG ---
st.success(f"👤 Chào {st.session_state['auth']}")

c1, c2 = st.columns(2)
with c1:
    if st.button("🔍 TRA MÃ & HD", use_container_width=True): st.session_state.page = "TRA"
with c2:
    if st.button("➕ THÊM MÃ MỚI", use_container_width=True): st.session_state.page = "THEM"

c3, c4 = st.columns(2)
with c3:
    if st.button("🧠 CHẨN ĐOÁN AI", use_container_width=True): st.session_state.page = "AI"
with c4:
    if st.button("💳 GIA HẠN", use_container_width=True): st.session_state.page = "GIA"

# --- XỬ LÝ TRANG ---
if st.session_state.page == "TRA":
    st.divider()
    loai = st.selectbox("Chọn máy:", list(DATA_HUONG_DAN.keys()))
    hang = st.selectbox(f"Chọn hãng {loai}:", list(DATA_HUONG_DAN[loai].keys()))
    ma = st.text_input("Nhập mã lỗi:").upper().strip()
    if st.button("XEM CÁCH SỬA", use_container_width=True):
        if ma in DATA_HUONG_DAN[loai][hang]:
            st.info(f"🛠 **Giải pháp:**\n\n{DATA_HUONG_DAN[loai][hang][ma]}")
        else:
            # Tra cứu trong kho thợ tự thêm
            found = [x for x in st.session_state.user_data if x['ma']==ma and x['hang']==hang]
            if found: st.success(f"📌 **Kinh nghiệm cá nhân:**\n\n{found[0]['hd']}")
            else: st.warning("Mã này chưa có. Duy hãy dùng mục 'Thêm mã mới' để lưu lại.")

elif st.session_state.page == "THEM":
    st.divider()
    t_loai = st.selectbox("Loại máy:", ["Điều Hòa", "Máy Giặt", "Bếp Từ"])
    t_hang = st.text_input("Hãng:")
    t_ma = st.text_input("Mã lỗi:").upper().strip()
    t_hd = st.text_area("Hướng dẫn sửa (Kinh nghiệm):")
    if st.button("LƯU KINH NGHIỆM", use_container_width=True):
        st.session_state.user_data.append({'loai': t_loai, 'hang': t_hang, 'ma': t_ma, 'hd': t_hd})
        st.success("Đã lưu! Duy có thể tra lại mã này ngay.")

elif st.session_state.page == "AI":
    st.divider()
    st.subheader("🧠 CHẨN ĐOÁN THÔNG MINH")
    benh = st.text_area("Mô tả bệnh (Vd: Mất nguồn, không lạnh...):")
    if st.button("AI PHÂN TÍCH", use_container_width=True):
        if "nguồn" in benh.lower(): st.error("🤖 Kiểm tra: Cầu chì, IC nguồn, Tụ lọc nguồn.")
        else: st.warning("🤖 Kiểm tra: Hệ thống cảm biến và các Rơ-le động lực.")

elif st.session_state.page == "GIA":
    st.image("https://img.vietqr.io/image/ICB-104881077679-compact2.png?amount=500000&addInfo=GIAHAN")

# NÚT ĐĂNG XUẤT (KHÔNG DÙNG RERUN CUỐI CÙNG)
st.divider()
if st.button("🚪 Đăng xuất", use_container_width=True):
    st.session_state.auth = None
    st.write("Đã thoát. Hãy F5 trang.")

