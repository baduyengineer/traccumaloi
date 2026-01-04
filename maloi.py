import streamlit as st

# --- CẤU HÌNH GIAO DIỆN NỔI BẬT ---
st.set_page_config(page_title="BA DUY TECH PRO", layout="centered")

# CSS làm nổi bật các thanh Tool và nút bấm
st.markdown("""
    <style>
    .stButton>button {
        background-color: #FF4B4B !important; /* Màu đỏ nổi bật */
        color: white !important;
        font-weight: bold !important;
        border-radius: 10px !important;
        height: 3em !important;
    }
    .stSelectbox label, .stTextInput label {
        color: #007BFF !important; /* Màu xanh dương cho tiêu đề nhập liệu */
        font-weight: bold !important;
    }
    .main-title {
        color: #E65100;
        text-align: center;
        font-size: 28px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- DỮ LIỆU TỪ FILE "MÃ LỖI TỔNG HỢP.DOCX" ---
# Tích hợp toàn bộ nội dung từ file của bạn 
DATA = {
    "LG Inverter": {
        "CH01": "Hỏng cảm biến giàn lạnh.",
        "CH02": "Hỏng cảm biến giàn lạnh.",
        "CH05": "Lỗi kết nối giàn nóng và giàn lạnh inverter. 🛠 HD: Kiểm tra dây tín hiệu kết nối giữa 2 khối.",
        "CH06": "Hỏng cảm biến đường đi của giàn nóng inverter.",
        "CH09": "Lỗi chức năng board mạch giàn nóng inverter.",
        "CH10": "Lỗi quạt giàn lạnh inverter.",
        "CH21": "Lỗi IC Công Suất. 🛠 HD: Kiểm tra khối công suất hoặc máy nén.",
        "CH22": "Cao dòng, cao điện áp trên cuộn seo, board.",
        "CH23": "Điện áp quá thấp.",
        "CH26": "Hỏng máy nén inverter.",
        "CH27": "Lỗi quá tải dàn nóng, board Inverter.",
        "CH29": "Pha máy nén inverter.",
        "CH32": "Nhiệt độ cao đường đẩy máy nén inverter.",
        "CH33": "Quá tải máy nén inverter.",
        "CH41": "Cảm biến máy nén 200k inverter.",
        "CH44": "Hỏng cảm biến gió giàn nóng 10k inverter.",
        "CH45": "Hỏng cảm biến gió giàn nóng 5k inverter.",
        "CH46": "Cảm biến đường về của máy nén inverter.",
        "CH47": "Máy nén không hoạt động cảm biến 200k.",
        "CH53": "Liên lạc giữa giàn nóng và giàn lạnh.",
        "CH60": "IC cắm trên mạch giàn nóng inverter.",
        "CH61": "Giàn nóng không giải nhiệt được. 🛠 HD: Vệ sinh dàn nóng.",
        "CH62": "Nhiệt độ cao ic nguồn đuôi nóng inverter.",
        "CH65": "Hỏng ic nguồn đuôi nóng inverter."
    },
    "Daikin": {
        "C1": "Lỗi bo mạch dàn lạnh hoặc bo mạch quạt.",
        "C4": "Lỗi nhiệt điện trở đường ống lỏng dàn lạnh hoặc lỏng kết nối.",
        "C9": "Lỗi nhiệt điện trở gió hồi dàn lạnh hoặc lỏng kết nối.",
        "E0": "Thiết bị bảo vệ dàn nóng tác động (Công tắc cao áp, moto quạt/máy nén quá tải).",
        "E1": "Lỗi bo mạch dàn nóng.",
        "E7": "Lỗi moto quạt dàn nóng hoặc bo mạch moto quạt.",
        "F3": "Nhiệt độ ống đẩy dàn nóng bất thường / Thiếu môi chất lạnh / Lỗi nhiệt điện trở ống đẩy.",
        "U0": "Thiếu môi chất lạnh / Hư van tiết lưu điện tử / Ống dẫn bị nghẹt.",
        "U2": "Lỗi nguồn điện hoặc mất điện tức thời.",
        "U4": "Lỗi truyền tín hiệu giữa dàn nóng và dàn lạnh. 🛠 HD: Kiểm tra dây F1-F2 hoặc bo mạch.",
        "UA": "Dàn nóng và lạnh không tương thích."
    },
    "Panasonic": {
        "00H": "Bình thường, không bị lỗi.",
        "11H": "Lỗi đường dữ liệu giữa khối trong và ngoài.",
        "14H": "Lỗi cảm biến nhiệt độ phòng.",
        "15H": "Lỗi cảm biến nhiệt độ máy nén.",
        "16H": "Dòng điện tải máy nén quá thấp.",
        "19H": "Lỗi quạt dàn lạnh.",
        "23H": "Lỗi cảm biến nhiệt độ dàn lạnh.",
        "25H": "Mạch E-on lỗi.",
        "28H": "Lỗi cảm biến giàn nóng. 🛠 HD: Kiểm tra jack cắm, đo điện trở (khoảng 3KΩ ở 30°C). Nếu cảm biến tốt thì hỏng board mạch.",
        "F91": "Rò rỉ môi chất lạnh, chu kỳ làm lạnh kém.",
        "F97": "Nhiệt độ máy nén cao bất thường, máy nén tự tắt.",
        "H11": "Lỗi truyền tín hiệu giữa khối trong và ngoài nhà.",
        "H19": "Động cơ moto quạt khối trong nhà bị kẹt, hỏng động cơ.",
        "H97": "Động cơ moto quạt khối ngoài trời bị khoá, kẹt.",
        "H98": "Nhiệt độ giàn trong nhà quá cao (Chế độ sưởi).",
        "H99": "Nhiệt độ dàn lạnh giảm quá thấp (Đóng băng)."
    }
}

# --- GIAO DIỆN NGƯỜI DÙNG ---
st.markdown('<p class="main-title">🛠 TRỢ LÝ SỬA CHỮA BA DUY TECH</p>', unsafe_allow_html=True)

# Thanh Tool chọn hãng (Làm nổi màu xanh)
hang_chon = st.selectbox("BƯỚC 1: CHỌN HÃNG MÁY", list(DATA.keys()))

# Thanh Tool nhập mã (Làm nổi màu xanh)
ma_nhap = st.text_input("BƯỚC 2: NHẬP MÃ LỖI (Ví dụ: CH05, U4, 28H...)").upper().strip()

# Nút tra cứu (Màu đỏ nổi bật)
if st.button("TRA CỨU CÁCH KHẮC PHỤC", use_container_width=True):
    if ma_nhap:
        if ma_nhap in DATA[hang_chon]:
            st.success(f"🔍 **KẾT QUẢ CHO {hang_chon.upper()} - {ma_nhap}:**")
            st.info(DATA[hang_chon][ma_nhap])
        else:
            st.error(f"❌ Không tìm thấy mã lỗi '{ma_nhap}' cho hãng {hang_chon}. Vui lòng kiểm tra lại.")
    else:
        st.warning("Vui lòng nhập mã lỗi trước khi tìm kiếm!")

st.divider()
st.caption("Dữ liệu được cập nhật từ tài liệu kỹ thuật tổng hợp 2026.")
