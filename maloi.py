import streamlit as st

# 1. CẤU HÌNH HỆ THỐNG & GIAO DIỆN
st.set_page_config(page_title="BA DUY TECH PRO 2026", layout="centered")

# CSS tạo nhãn Đỏ, nút Xanh và khung cảnh báo Cam giống ảnh mẫu
st.markdown("""
    <style>
    /* Nút tìm kiếm xanh chuẩn */
    div.stButton > button {
        background-color: #007BFF !important;
        color: white !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        height: 3em !important;
        width: 100% !important;
    }
    /* Nhãn Tool màu đỏ rực rỡ */
    .stSelectbox label, .stTextInput label {
        color: #FFFFFF !important;
        background-color: #FF4B4B !important;
        padding: 4px 12px !important;
        border-radius: 6px !important;
        font-weight: bold !important;
        font-size: 14px !important;
        margin-bottom: 8px !important;
        display: inline-block !important;
    }
    /* Khung cảnh báo Mã lỗi chuyên sâu */
    .lock-container {
        border: 2px dashed #FF8C00;
        background-color: #FFF9F0;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        margin-top: 20px;
    }
    .lock-title {
        color: #D35400;
        font-size: 22px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. KHỞI TẠO DỮ LIỆU
if 'auth' not in st.session_state: st.session_state['auth'] = None
if 'page' not in st.session_state: st.session_state['page'] = "TRA"

# Danh sách mã lỗi cho phép xem Miễn phí (Chỉ để vài mã làm mẫu)
MA_FREE_LIST = ["E0", "E1", "28H", "CH05","C1"]

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
        "Midea": {
            "E0": "Không nhận nồi. 🛠 HD: Kiểm tra phần điện trở nhận nồi.",
            "E1": "Bếp quá nhiệt. 🛠 HD: Kiểm tra quạt, thông gió, cảm biến nhiệt",
            "E2": "Cảm biến mặt kính lỗi.",
            "E3": "Quá áp (>250V).",
            "E4": "Áp thấp (<170V).",
            "E6": "Lỗi cảm biến IGBT."
        },
        "Sunhouse": {
            "E0": "Lỗi mạch nhận nồi. 🛠 HD: Kiểm tra tụ 5uF, 0.33uF.",
            "E1": "Điện áp quá yếu.",
            "E2": "Nhiệt độ nồi quá cao.",
            "E5": "Cảm biến mặt kính hở mạch."
        },
        "Sanaky": {
            "E0": "Không có nồi/Sai nồi.",
            "E1": "Điện áp thấp.",
            "E2": "Điện áp quá cao.",
            "E3": "Quá nhiệt mặt kính."
        },
        "Kangaroo": {
            "E0": "Không nhận nồi, kiểm tra mạch nhận nồi",
            "E1": "Công suất bếp quá nóng, kiểm tra quạt làm mát hoặc mạch bảo vệ quá nhiệt.",
            "E2": "Lỗi cảm biến nhiệt."
        },
        "Bosch": {
            "E01": "Lỗi module công suất.",
            "F0": "Lỗi truyền thông board mạch.",
            "U1": "Điện áp cấp không ổn định."
        }
    },
    "Máy Giặt": {
        "Electrolux": {
            "E10": "Lỗi cấp nước. HD: Vệ sinh van cấp.",
            "E20": "Lỗi thoát nước. HD: Kiểm tra bơm xả."
        }
    }
}
# --- MÀN HÌNH ĐĂNG NHẬP ---
if st.session_state['auth'] is None:
    st.title("🔐 HỆ THỐNG TRỢ LÝ KỸ THUẬT TECH 3D")
    ma = st.text_input("Nhập mã kích hoạt (Vd: DUY-FREE):", type="password")
    if st.button("XÁC NHẬN VÀO"):
        if ma == "PRO-DUY-2026":
            st.session_state['auth'] = {"ten": "Ba Duy", "loai": "Vĩnh viễn"}
            st.rerun()
        elif ma == "DUY-FREE":
            st.session_state['auth'] = {"ten": "Khách dùng thử", "loai": "Free"}
            st.rerun()
    st.stop()

# --- GIAO DIỆN CHÍNH ---
user = st.session_state['auth']
is_pro = user['loai'] == "Vĩnh viễn"

st.markdown(f"👤 **{user['ten']}** | Gói: **{user['loai']}**")

# Tabs Menu
c1, c2, c3, c4 = st.columns(4)
with c1: 
    if st.button("🔍 TRA MÃ"): st.session_state.page = "TRA"
with c2: 
    if st.button("🧠 AI"): st.session_state.page = "AI"
with c3: 
    if st.button("➕ THÊM"): st.session_state.page = "THEM"
with c4: 
    if st.button("💳 GÓI"): st.session_state.page = "GIA"

# --- TRANG TRA CỨU & KHẮC PHỤC ---
if st.session_state.page == "TRA":
    st.markdown("### 🔍 TRA CỨU & KHẮC PHỤC")
    
    loai = st.selectbox("CHỌN THIẾT BỊ:", list(DATA_FULL.keys()), key="sel_loai")
    hang = st.selectbox(f"CHỌN HÃNG {loai}:", list(DATA_FULL[loai].keys()), key="sel_hang")
    ma_nhap = st.text_input("NHẬP MÃ LỖI:", placeholder="H11, CH05, E1...").upper().strip()
    
    if st.button("TÌM KIẾM NGAY"):
        if ma_nhap in DATA_FULL[loai][hang]:
            # LOGIC PHÂN QUYỀN
            if is_pro or (ma_nhap in MA_FREE_LIST):
                st.info(f"⚙️ **{hang} {ma_nhap}:**\n\n{DATA_FULL[loai][hang][ma_nhap]}")
            else:
                # HIỂN THỊ CÂU NHẮC NHỞ GIỐNG ẢNH MẪU
                st.markdown(f"""
                <div class="lock-container">
                    <div class="lock-title">🔒 MÃ LỖI CHUYÊN SÂU</div>
                    <p style="color: #666; margin-top:10px;">
                        Bạn cần mua gói nâng cấp để xem được nhiều mã lỗi hơn và hướng dẫn sửa chữa chi tiết.
                    </p>
                </div>
                """, unsafe_allow_html=True)
                # Chèn mã QR
                st.image("https://img.vietqr.io/image/ICB-104881077679-compact2.png?amount=299000&addInfo=NANG_CAP_PRO", 
                         caption="Quét mã QR để nâng cấp gói PRO ngay")
        else:
            st.error("Mã lỗi này chưa được cập nhật trong hệ thống.")

elif st.session_state.page == "GIA":
    st.subheader("💳 QUẢN LÝ GÓI & GIA HẠN")
    st.image("https://img.vietqr.io/image/ICB-104881077679-compact2.png?amount=299000&addInfo=GIAHAN")

# Nút Đăng xuất
st.divider()
if st.button("🚪 ĐĂNG XUẤT", use_container_width=True):
    st.session_state.auth = None
    st.rerun()

st.caption("BA DUY TECH v55.0 - DỮ LIỆU ĐÃ CẬP NHẬT LIÊN TỤC")
