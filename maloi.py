
import streamlit as st
from datetime import datetime

# ========================================================
# 1. QUẢN LÝ BẢN QUYỀN & KHÁCH HÀNG
# ========================================================
DANH_SACH_KHACH_HANG = {
    "PRO-DUY-2025": {"ten": "Kỹ sư Ba Duy", "loai": "Pro", "han": "2026-01-05"},
    "ADMIN-888": {"ten": "Quản trị viên", "loai": "Pro", "han": "2030-12-31"},
}

if 'auth' not in st.session_state:
    st.session_state['auth'] = None

if not st.session_state['auth']:
    st.markdown("<h2 style='text-align: center;'>🔐 HỆ THỐNG TRỢ LÝ KỸ THUẬT BADUY@2025</h2>", unsafe_allow_html=True)
    ma_nhap = st.text_input("Nhập mã cá nhân của bạn:", type="password").strip()
    if st.button("Kích hoạt bản quyền"):
        if ma_nhap in DANH_SACH_KHACH_HANG:
            st.session_state['auth'] = DANH_SACH_KHACH_HANG[ma_nhap]
            st.session_state['ma_kich_hoat'] = ma_nhap
            st.rerun()
        else:
            st.error("Mã không hợp lệ hoặc đã hết hạn!")
    st.stop()

user = st.session_state['auth']
ma_kich_hoat = st.session_state.get('ma_kich_hoat', '')
ngay_het_han = datetime.strptime(user['han'], "%Y-%m-%d")
ngay_con_lai = (ngay_het_han - datetime.now()).days

# ========================================================
# 2. KHO DỮ LIỆU TỔNG HỢP (MÁY GIẶT & BẾP TỪ)
# ========================================================
DATA_ALL = {
    "Máy Giặt": {
        "Electrolux/Common": {
            "E10": {"loi": "Lỗi nguồn cấp nước (Vòi đóng, bộ lọc tắc).", "pro": "Kiểm tra vòi nước, vệ sinh lưới lọc van cấp, đo điện áp cấp van."},
            "E20": {"loi": "Lỗi xả nước (Ống xả tắc, bơm hỏng).", "pro": "Kiểm tra bơm xả, vệ sinh hố bơm, đo cuộn dây bơm."},
            "E21": {"loi": "Khó xả nước trong chu trình giặt.", "pro": "Kiểm tra bộ lọc bơm, ống thoát, thay bơm xả nếu cần."},
            "E23": {"loi": "Hư Triac bơm nước trên mạch.", "pro": "Đo Triac điều khiển bơm trên main PCB, kiểm tra chạm chập dây."},
            "E41": {"loi": "Lỗi cửa mở (Quá 15 giây).", "pro": "Đóng lại cửa, kiểm tra khóa cửa/công tắc cửa."},
            "E52": {"loi": "Không có tín hiệu từ bộ điều tốc (Tacho).", "pro": "Kiểm tra chổi than motor, đo cuộn Tacho (120-180 Ohm)."},
            "E57": {"loi": "Inverter hút dòng quá lớn (>15A).", "pro": "Kiểm tra chạm motor, đo 3 pha motor, thay board Inverter."},
            "E58": {"loi": "Inverter hút dòng quá nhiều (>4.5A).", "pro": "Kiểm tra dây dẫn động cơ, đo điện trở cuộn dây, thay mô-đun."},
            "E59": {"loi": "Không có tín hiệu điều tốc trong 3 giây.", "pro": "Kiểm tra dây kết nối motor và board điều khiển."},
            "E91": {"loi": "Lỗi kết nối giữa PCB nguồn và PCB hiển thị.", "pro": "Kiểm tra cáp bus tín hiệu, vệ sinh giắc cắm hoặc sửa board."},
        }
    },
    "Bếp Từ": {
        "Bosch": {
            "E22": {"loi": "Lỗi bo cảm ứng do ẩm hoặc chập chân IC phím.", "pro": "Sấy bo mạch, vệ sinh sạch vùng phím cảm ứng."},
            "F0": {"loi": "Lỗi đường truyền dẫn, cáp hoặc dây tín hiệu.", "pro": "Kiểm tra cáp nối bo công suất và hiển thị."},
            "Er26": {"loi": "Lỗi relay chuyển tiếp hoặc mạch điều khiển.", "pro": "Thay rơ-le trên bo chính, kiểm tra lệnh từ vi xử lý."},
            "F1": {"loi": "Lỗi cảm biến nhiệt độ (NTC) hoặc bo cảm ứng.", "pro": "Đo cảm biến mâm từ (thường 100k), kiểm tra giắc cắm."},
        },
        "Sunhouse": {
            "E0": {"loi": "Chưa có nồi hoặc nồi không phù hợp.", "pro": "Thử nồi chuẩn, kiểm tra mạch nhận nồi (trở hồi tiếp)."},
            "E1": {"loi": "Điện áp quá cao hoặc mạch bảo vệ lỗi.", "pro": "Kiểm tra điện lưới, đo trở đường AC báo về."},
        }
    }
}

DATA_AI = {
    "Bếp Từ": {
        "Bếp không nhận nồi (không báo lỗi)": "Kiểm tra tụ 0.33uF, mạch Driver và trở hồi tiếp (470k-820k).",
        "Mất nguồn hoàn toàn": "Kiểm tra cầu chì, IC nguồn (Viper12A), diode cầu nắn 300Vdc.",
    },
    "Máy Giặt": {
        "Vắt rung lắc mạnh": "Kiểm tra ty treo lồng, cân bằng máy, bi phớt trục.",
        "Nước vào liên tục": "Kiểm tra van cấp bị kẹt rác hoặc hỏng phao áp lực.",
    }
}

# ========================================================
# 3. GIAO DIỆN ĐIỀU HƯỚNG
# ========================================================
st.sidebar.title(f"👤 {user['ten']}")
if ngay_con_lai <= 7:
    st.sidebar.warning(f"🕒 Hạn dùng còn {ngay_con_lai} ngày!")

menu = st.sidebar.radio("CHỨC NĂNG CHÍNH", 
    ["🔍 Tra mã lỗi", "🧠 Chẩn đoán (AI)", "📚 Sơ đồ thông minh", "💳 Gia hạn tự động"])

# --- MENU: TRA MÃ LỖI ---
if menu == "Tra mã lỗi":
    st.header("🔍 TRA CỨU MÃ LỖI CHI TIẾT")
    loai = st.selectbox("Loại thiết bị", list(DATA_ALL.keys()))
    hang = st.selectbox("Hãng sản xuất", list(DATA_ALL[loai].keys()))
    ma = st.text_input("Nhập mã lỗi (Ví dụ: E52, E22, E0...):").upper().strip()
    
    if st.button("Tra cứu ngay"):
        if ma in DATA_ALL[loai][hang]:
            res = DATA_ALL[loai][hang][ma]
            st.info(f"📌 **Mô tả:** {res['loi']}")
            st.success(f"🛠️ **Hướng dẫn sửa:**\n{res['pro']}")
        else:
            st.error("Mã lỗi chưa có trong hệ thống.")

# --- MENU: CHẨN ĐOÁN (AI) ---
elif menu == "Chẩn đoán (AI)":
    st.header("🧠 CHẨN ĐOÁN THEO BIỂU HIỆN")
    l_ai = st.selectbox("Thiết bị:", list(DATA_AI.keys()))
    b_ai = st.selectbox("Tình trạng máy:", list(DATA_AI[l_ai].keys()))
    if st.button("Phân tích"):
        st.success(f"📋 Gợi ý từ Trợ lý Duy: {DATA_AI[l_ai][b_ai]}")

# --- MENU: SƠ ĐỒ THÔNG MINH ---
elif menu == "Sơ đồ thông minh":
    st.header("📚 TRỢ LÝ TÌM SƠ ĐỒ PDF")
    mod = st.text_input("Nhập Model máy hoặc Mã Board (Ví dụ: EWP85742, K2012...):")
    if st.button("Tìm tài liệu"):
        url = f"https://www.google.com/search?q={mod}+service+manual+pdf+schematic"
        st.markdown(f"### [👉 Bấm vào đây để tải sơ đồ {mod}]({url})")

# --- MENU: GIA HẠN TỰ ĐỘNG ---
elif menu == "Gia hạn tự động":
    st.header("💳 GIA HẠN DỊCH VỤ")
    st.write(f"Tài khoản: **{user['ten']}** | Hết hạn: **{user['han']}**")
    
    goi = st.radio("Chọn gói gia hạn:", ["6 Tháng - 199k", "12 Tháng - 299k", "Vĩnh viễn - 999k"], horizontal=True)
    tien = "199000" if "6 Tháng" in goi else ("299000" if "12 Tháng" in goi else "999000")
    
    # Tạo mã QR VietQR tự động
    stk = "104881077679" # Thay bằng STK của Duy
    bank = "Vietin" # Thay bằng ngân hàng của Duy
    nd = f"GIAHAN {ma_kich_hoat}"
    qr_url = f"https://img.vietqr.io/image/{bank}-{stk}-compact2.png?amount={tien}&addInfo={nd}&accountName=NGUYEN BA DUY"
    
    col1, col2 = st.columns([1, 1.5])
    with col1: st.image(qr_url, caption="Quét để thanh toán")
    with col2:
        st.info(f"Nội dung: **{nd}**\n\nSau khi chuyển khoản, hệ thống sẽ tự động cộng hạn sau khi Duy xác nhận tiền về.")
        if st.button("Xác nhận đã chuyển tiền"):
            st.success("Thông báo đã gửi tới Duy. Cảm ơn bạn!")

if st.sidebar.button("Đăng xuất"):
    st.session_state['auth'] = None
    st.rerun()
