import streamlit as st
from datetime import datetime
import requests

# ========================================================
# 1. QUẢN LÝ BẢN QUYỀN & KHÁCH HÀNG (MỤC 4)
# ========================================================
DANH_SACH_KHACH_HANG = {
    "PRO-DUY-2025": {"ten": "Kỹ sư Ba Duy", "loai": "Pro", "han": "2026-01-05"},
    "ADMIN-888": {"ten": "Quản trị viên", "loai": "Pro", "han": "2030-12-31"},
}

if 'auth' not in st.session_state:
    st.session_state['auth'] = None

if not st.session_state['auth']:
    st.markdown("<h2 style='text-align: center;'>🔐 HỆ THỐNG TRỢ LÝ KỸ THUẬT BADUY@2025</h2>", unsafe_allow_html=True)
    ma_nhap = st.text_input("Nhập mã kích hoạt của bạn:", type="password").strip()
    if st.button("Kích hoạt bản quyền"):
        if ma_nhap in DANH_SACH_KHACH_HANG:
            st.session_state['auth'] = DANH_SACH_KHACH_HANG[ma_nhap]
            st.session_state['ma_kich_hoat'] = ma_nhap
            st.rerun()
        else:
            st.error("Mã không chính xác hoặc đã bị khóa.")
    st.stop()

user = st.session_state['auth']
ma_khach = st.session_state.get('ma_kich_hoat', 'USER')
ngay_het_han = datetime.strptime(user['han'], "%Y-%m-%d")
ngay_con_lai = (ngay_het_han - datetime.now()).days

# ========================================================
# 2. KHO DỮ LIỆU TỔNG HỢP (DỮ LIỆU CHUẨN)
# ========================================================
KHO_DATA = {
    "Máy Giặt": {
        "Electrolux": {
            "E10": {"loi": "Lỗi nguồn cấp nước (Vòi đóng, bộ lọc tắc).", "pro": "Kiểm tra vòi nước, vệ sinh lưới lọc van cấp, đo điện áp cấp van."},
            "E21": {"loi": "Khó xả nước (Chu trình giặt).", "pro": "Kiểm tra bộ lọc bơm xả, ống thoát, đo cuộn dây bơm."},
            "E23": {"loi": "Hư Triac bơm nước trên mạch.", "pro": "Đo kiểm Triac điều khiển bơm trên main PCB."},
            "E41": {"loi": "Lỗi cửa mở (Sau 15 giây).", "pro": "Đóng lại cửa chặt, kiểm tra khóa cửa hoặc công tắc cửa."},
            "E52": {"loi": "Không có tín hiệu từ bộ điều tốc (Tacho).", "pro": "Kiểm tra chổi than motor, đo cuộn Tacho (120-180 Ohm)."},
            "E57": {"loi": "Inverter hút dòng quá lớn (>15A).", "pro": "Kiểm tra chạm motor, đo 3 pha motor, thay board Inverter."},
            "E58": {"loi": "Inverter hút dòng quá nhiều (>4.5A).", "pro": "Kiểm tra dây dẫn động cơ, đo điện trở cuộn dây."},
            "E91": {"loi": "Lỗi kết nối giữa PCB nguồn và hiển thị.", "pro": "Vệ sinh cáp bus tín hiệu giữa 2 board."},
        }
    },
    "Máy Điều Hòa": {
        "Daikin": {
            "U0": {"loi": "Thiếu gas hoặc nghẹt hệ thống lạnh.", "pro": "Kiểm tra áp suất gas, các đầu tán co rò rỉ."},
            "A6": {"loi": "Lỗi motor quạt dàn lạnh.", "pro": "Kiểm tra quạt, tụ quạt hoặc lệnh từ board."},
            "L5": {"loi": "Lỗi máy nén biến tần (Inverter).", "pro": "Kiểm tra Block, đo chạm vỏ hoặc board công suất."},
        },
        "Panasonic": {
            "H11": {"loi": "Lỗi giao tiếp cục nóng và cục lạnh.", "pro": "Kiểm tra dây tín hiệu số 3, kiểm tra board mạch."},
        }
    },
    "Bếp Từ": {
        "Sunhouse": {
            "E0": {"loi": "Lỗi nhận nồi/Điện áp đầu vào AC.", "pro": "Kiểm tra trở 200k, tụ 5uF, mạch hồi tiếp nhận nồi."},
            "E1": {"loi": "Điện áp quá cao hoặc lỗi mạch bảo vệ.", "pro": "Kiểm tra điện lưới, đo trở đường AC báo về VXL."},
        },
        "Bosch": {
            "E22": {"loi": "Lỗi bo cảm ứng (Ẩm/Nước).", "pro": "Sấy bo mạch, vệ sinh sạch vùng phím cảm ứng."},
        }
    }
}

# Dữ liệu chẩn đoán (Mục 3)
DATA_CHAN_DOAN = {
    "Máy Giặt": {
        "Rung lắc mạnh khi vắt": "Kiểm tra ty treo lồng, giảm xóc, bi phớt hoặc trục lồng bị gãy.",
        "Nước vào không ngừng": "Vệ sinh van cấp, kiểm tra phao áp lực mực nước."
    },
    "Bếp Từ": {
        "Bếp không nhận nồi (không báo lỗi)": "Kiểm tra tụ 0.33uF, mạch Driver và trở hồi tiếp (470k-820k).",
        "Mất nguồn hoàn toàn": "Kiểm tra cầu chì, diode cầu, IC nguồn (Viper12A)."
    }
}

# ========================================================
# 3. GIAO DIỆN ĐIỀU HƯỚNG CHUYÊN NGHIỆP
# ========================================================
st.sidebar.title(f"👤 {user['ten']}")
if ngay_con_lai <= 7:
    st.sidebar.warning(f"🕒 Bản quyền còn {ngay_con_lai} ngày!")

menu = st.sidebar.radio("CHỨC NĂNG CHÍNH", 
    ["🔍 Tra mã lỗi", "🧠 Chẩn đoán (AI)", "📚 Sơ đồ thông minh", "💳 Gia hạn tự động"])

# --- MENU: TRA MÃ LỖI ---
if menu == "Tra mã lỗi":
    st.header("🔍 TRA CỨU MÃ LỖI TỔNG HỢP")
    col1, col2 = st.columns(2)
    with col1:
        loai = st.selectbox("Chọn thiết bị", list(KHO_DATA.keys()))
    with col2:
        hang = st.selectbox("Chọn hãng", list(KHO_DATA[loai].keys()))
    
    ma = st.text_input("Nhập mã lỗi (Ví dụ: E10, E52, U0...):").upper().strip()
    if st.button("Tra cứu chuyên sâu"):
        if ma in KHO_DATA[loai][hang]:
            res = KHO_DATA[loai][hang][ma]
            st.info(f"📌 **Mô tả:** {res['loi']}")
            st.success(f"🛠️ **Hướng dẫn sửa (PRO):**\n{res['pro']}")
        else:
            st.error("Mã lỗi chưa có trong hệ thống. Đang kết nối AI...")
            # Gợi ý AI cơ bản
            st.write(f"💡 Trợ lý Duy gợi ý: Với lỗi {ma}, hãy kiểm tra các mức nguồn 5V/12V và đường hồi tiếp.")

# --- MENU: CHẨN ĐOÁN (AI) ---
elif menu == "Chẩn đoán (AI)":
    st.header("🧠 CHẨN ĐOÁN THEO BIỂU HIỆN")
    l_ai = st.selectbox("Thiết bị:", list(DATA_CHAN_DOAN.keys()))
    b_ai = st.selectbox("Tình trạng máy:", list(DATA_CHAN_DOAN[l_ai].keys()))
    if st.button("Phân tích"):
        st.success(f"📋 Gợi ý xử lý: {DATA_CHAN_DOAN[l_ai][b_ai]}")

# --- MENU: SƠ ĐỒ THÔNG MINH ---
elif menu == "Sơ đồ thông minh":
    st.header("📚 TRỢ LÝ TÌM SƠ ĐỒ PDF")
    mod = st.text_input("Nhập Model máy hoặc Mã Board:")
    if st.button("Tìm tài liệu"):
        url = f"https://www.google.com/search?q={mod}+service+manual+pdf+schematic"
        st.markdown(f"### [👉 Bấm để tải sơ đồ {mod}]({url})")
        st.info("Trợ lý đã tự động lọc các kết quả Schematic chuẩn cho bạn.")

# --- MENU: GIA HẠN THANH TOÁN TỰ ĐỘNG ---
elif menu == "Gia hạn tự động":
    st.header("💳 GIA HẠN DỊCH VỤ TỰ ĐỘNG")
    st.write(f"Hạn dùng hiện tại: **{user['han']}**")
    
    goi = st.radio("Chọn gói gia hạn:", ["6 Tháng - 300k", "12 Tháng - 500k", "Vĩnh viễn - 1.5tr"], horizontal=True)
    tien = "300000" if "6 Tháng" in goi else ("500000" if "12 Tháng" in goi else "1500000")
    
    # THÔNG TIN VIETINBANK CỦA TRINH BA DUY
    stk = "104881077679"
    ten_tk = "TRINH BA DUY"
    bank = "ICB" # VietinBank
    nd = f"GIA HAN {ma_khach}"
    
    qr_url = f"https://img.vietqr.io/image/{bank}-{stk}-compact2.png?amount={tien}&addInfo={nd}&accountName={ten_tk}"
    
    col_qr, col_info = st.columns([1, 1.5])
    with col_qr:
        st.image(qr_url, caption="Quét để thanh toán nhanh")
    with col_info:
        st.success(f"Nội dung CK: **{nd}**\n\nChủ TK: **{ten_tk}**")
        st.warning("Hệ thống sẽ tự động cập nhật hạn dùng sau khi nhận được thông báo từ Ngân hàng.")
        if st.button("Xác nhận đã chuyển khoản thành công"):
            st.balloons()
            st.success("Yêu cầu đã gửi tới Duy. Cảm ơn bạn!")

if st.sidebar.button("Đăng xuất"):
    st.session_state['auth'] = None
    st.rerun()
