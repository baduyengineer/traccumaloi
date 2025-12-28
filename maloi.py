import streamlit as st
from datetime import datetime

# ========================================================
# 1. QUẢN LÝ KHÁCH HÀNG & BẢN QUYỀN
# ========================================================
DANH_SACH_KHACH_HANG = {
    "PRO-DUY-2025": {"ten": "Kỹ sư Ba Duy", "loai": "Pro", "han": "2026-01-05"},
    "ADMIN-888": {"ten": "Quản trị viên", "loai": "Pro", "han": "2030-12-31"},
}

if 'auth' not in st.session_state:
    st.session_state['auth'] = None

if not st.session_state['auth']:
    st.markdown("<h2 style='text-align: center;'>🔐 HỆ THỐNG TRỢ LÝ BADUY@2025</h2>", unsafe_allow_html=True)
    ma_nhap = st.text_input("Nhập mã kích hoạt của bạn:", type="password").strip()
    if st.button("Kích hoạt ngay"):
        if ma_nhap in DANH_SACH_KHACH_HANG:
            st.session_state['auth'] = DANH_SACH_KHACH_HANG[ma_nhap]
            st.rerun()
        else:
            st.error("Mã không chính xác!")
    st.stop()

user = st.session_state['auth']
ngay_het_han = datetime.strptime(user['han'], "%Y-%m-%d")
ngay_con_lai = (ngay_het_han - datetime.now()).days

# ========================================================
# 2. DỮ LIỆU CHI TIẾT (ĐÃ NẠP TỪ ẢNH CỦA BẠN)
# ========================================================
data_ma_loi = {
    "Máy Giặt": {
        "Electrolux": {
            "E10": {"loi": "Lỗi nguồn cấp nước (Vòi đóng, bộ lọc tắc, đường ống vôi hóa).", "pro": "Kiểm tra vòi nước, vệ sinh sạch lưới lọc van cấp, kiểm tra điện áp cấp cho van."},
            "E21": {"loi": "Khó xả nước (Chu trình giặt).", "pro": "Kiểm tra bộ lọc máy bơm, ống thoát nước, hệ thống dây điện và bơm xả."},
            "E23": {"loi": "Hư Triac bơm nước trên mạch.", "pro": "Đo kiểm Triac điều khiển bơm trên main PCB, kiểm tra chạm chập dây dẫn."},
            "E41": {"loi": "Lỗi cửa mở (Quá 15 giây).", "pro": "Kiểm tra khóa cửa bị hỏng hoặc tiếp điểm cửa không ăn."},
            "E52": {"loi": "Không có tín hiệu từ bộ điều tốc (Tacho).", "pro": "Kiểm tra chổi than motor, đo cuộn dây Tacho (120-180 Ohm), kiểm tra board điều khiển."},
            "E57": {"loi": "Inverter hút dòng quá lớn (>15A).", "pro": "Kiểm tra chạm chập cuộn dây motor, đo 3 pha motor, kiểm tra board Inverter."},
            "E58": {"loi": "Inverter hút dòng quá nhiều (>4.5A).", "pro": "Kiểm tra hệ thống dây dẫn, đo điện trở cuộn dây động cơ, thay mô-đun điều khiển."},
            "E59": {"loi": "Không có tín hiệu điều tốc trong 3 giây.", "pro": "Kiểm tra dây dẫn, đo cuộn dây động cơ và Tacho."},
            "E91": {"loi": "Lỗi kết nối giữa PCB nguồn và PCB hiển thị.", "pro": "Kiểm tra cáp tín hiệu (bus), vệ sinh giắc cắm hoặc sửa board."},
            "E92": {"loi": "Sự không tương thích giữa PCB chính và PCB hiển thị.", "pro": "Thay main PCB hoặc kiểm tra mã cấu hình board."},
        }
    },
    "Bếp Từ": {
        "Sunhouse": {
            "E0": {
                "loi": "Lỗi mạch nhận biết điện áp đầu vào AC.", 
                "pro": "Kiểm tra trở 200k, tụ 4.7uF đường AC báo về vi xử lý.",
                "video": "https://www.youtube.com/watch?v=J_iBHlMdcmk"
            },
        },
        "Bosch": {
            "E22": {"loi": "Lỗi bo cảm ứng do ẩm, nước vào hoặc chập chân IC phím.", "pro": "Sấy khô bo mạch, vệ sinh sạch vùng phím."},
            "F0": {"loi": "Lỗi đường truyền dẫn, cáp hoặc dây tín hiệu.", "pro": "Kiểm tra cáp nối giữa bo công suất và bo hiển thị."},
            "Er26": {"loi": "Lỗi Relay chuyển tiếp hoặc mạch điều khiển rơ-le.", "pro": "Thay rơ-le trên bo mạch chính hoặc kiểm tra lệnh từ VXL."},
            "F1": {"loi": "Lỗi cảm biến nhiệt độ (NTC) hoặc bo cảm ứng.", "pro": "Đo cảm biến nhiệt mâm từ, kiểm tra bo mạch."},
        }
    }
}

data_chan_doan = {
    "Bếp Từ": {
        "Bếp không nhận nồi (không báo lỗi)": "Kiểm tra tụ cộng hưởng 0.33uF, mạch Driver và điện trở hồi tiếp 470k-820k.",
        "Mất nguồn hoàn toàn": "Kiểm tra cầu chì, diode cầu, IC nguồn (Viper12A/22A).",
        "Bếp nổ IGBT": "Thay IGBT và phải kiểm tra mạch lái (Driver) trước khi cắm điện lại."
    },
    "Máy Giặt": {
        "Rung lắc mạnh khi vắt": "Kiểm tra ty treo, thụt giảm xóc, hoặc lồng giặt bị lệch tâm.",
        "Nước chảy vào liên tục": "Vệ sinh van cấp hoặc thay van nếu bị hỏng màng cao su, kiểm tra phao áp lực."
    }
}

# ========================================================
# 3. GIAO DIỆN CHÍNH
# ========================================================
st.sidebar.title(f"👤 {user['ten']}")
if ngay_con_lai <= 7:
    st.sidebar.warning(f"🕒 Bản quyền còn {ngay_con_lai} ngày!")

menu = st.sidebar.radio("CHỨC NĂNG CHÍNH", ["Tra mã lỗi", "Chẩn đoán bệnh (AI)", "Sơ đồ thông minh", "Gia hạn"])

if menu == "Tra mã lỗi":
    st.header("🔍 TRA CỨU MÃ LỖI CHI TIẾT")
    c1, c2 = st.columns(2)
    with c1: loai = st.selectbox("Thiết bị", list(data_ma_loi.keys()))
    with c2: hang = st.selectbox("Hãng", list(data_ma_loi[loai].keys()))
    ma = st.text_input("Nhập mã lỗi (Ví dụ: E52, E41, E0...):").upper().strip()
    
    if st.button("Tra cứu chuyên sâu"):
        if ma in data_ma_loi[loai][hang]:
            res = data_ma_loi[loai][hang][ma]
            st.info(f"📌 **Mô tả:** {res['loi']}")
            st.success(f"🛠️ **Hướng dẫn sửa:**\n{res['pro']}")
            if "video" in res: st.video(res['video'])
        else: st.error("Mã lỗi chưa có dữ liệu.")

elif menu == "Chẩn đoán bệnh (AI)":
    st.header("🧠 CHẨN ĐOÁN THEO BIỂU HIỆN")
    l = st.selectbox("Loại máy:", list(data_chan_doan.keys()))
    b = st.selectbox("Tình trạng máy:", list(data_chan_doan[l].keys()))
    if st.button("Phân tích"):
        st.success(f"📋 Gợi ý: {data_chan_doan[l][b]}")

elif menu == "Sơ đồ thông minh":
    st.header("📚 TRỢ LÝ TÌM SƠ ĐỒ PDF")
    mod = st.text_input("Nhập Model máy hoặc Mã Board:")
    if st.button("Tìm ngay"):
        url = f"https://www.google.com/search?q={mod}+service+manual+pdf+schematic"
        st.markdown(f"### [👉 Bấm để tải sơ đồ máy {mod}]({url})")

elif menu == "Gia hạn":
    st.header("💳 GIA HẠN DỊCH VỤ")
    st.write(f"Hạn dùng hiện tại: **{user['han']}**")
    st.info("Liên hệ Duy (0987973723) để gia hạn.")

if st.sidebar.button("Đăng xuất"):
    st.session_state['auth'] = None
    st.rerun()
