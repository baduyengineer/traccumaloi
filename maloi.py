import streamlit as st
from datetime import datetime

# --- Cấu hình trang ---
st.set_page_config(page_title="Trợ lý Ba Duy 2025", layout="wide")

# ========================================================
# 1. QUẢN LÝ BẢN QUYỀN
# ========================================================
DANH_SACH_KHACH_HANG = {
    "PRO-DUY-2025": {"ten": "Kỹ sư Ba Duy", "loai": "Pro", "han": "2026-01-05"},
    "ADMIN-888": {"ten": "Quản trị viên", "loai": "Pro", "han": "2030-12-31"},
}

if 'auth' not in st.session_state:
    st.session_state['auth'] = None

if not st.session_state['auth']:
    st.markdown("<h2 style='text-align: center;'>🔐 HỆ THỐNG KỸ THUẬT BADUY@2025</h2>", unsafe_allow_html=True)
    ma_nhap = st.text_input("Nhập mã kích hoạt của bạn:", type="password").strip()
    if st.button("Kích hoạt bản quyền"):
        if ma_nhap in DANH_SACH_KHACH_HANG:
            st.session_state['auth'] = DANH_SACH_KHACH_HANG[ma_nhap]
            st.session_state['ma_kich_hoat'] = ma_nhap
            st.rerun()
        else:
            st.error("Mã không chính xác.")
    st.stop()

user = st.session_state['auth']
ma_khach = st.session_state.get('ma_kich_hoat', 'USER')
ngay_het_han = datetime.strptime(user['han'], "%Y-%m-%d")
ngay_con_lai = (ngay_het_han - datetime.now()).days

# ========================================================
# 2. KHO DỮ LIỆU TỔNG HỢP (Hết Trắng Trơn)
# ========================================================
KHO_DATA = {
    "Máy Giặt": {
        "Electrolux": {
            "E10": {"loi": "Lỗi nguồn cấp nước.", "pro": "Vệ sinh lưới lọc van cấp, kiểm tra vòi nước."},
            "E52": {"loi": "Lỗi Tacho motor.", "pro": "Kiểm tra chổi than, đo cuộn Tacho (120-180 Ohm)."},
            "E91": {"loi": "Lỗi kết nối board.", "pro": "Kiểm tra cáp bus nối giữa board nguồn và hiển thị."},
        }
    },
    "Máy Điều Hòa": {
        "Daikin": {
            "U0": {"loi": "Thiếu gas/Nghẹt hệ thống.", "pro": "Kiểm tra áp suất gas và rò rỉ."},
            "L5": {"loi": "Lỗi máy nén Inverter.", "pro": "Kiểm tra Block hoặc board công suất."},
        }
    },
    "Bếp Từ": {
        "Sunhouse": {
            "E0": {"loi": "Lỗi nhận nồi/Áp AC.", "pro": "Kiểm tra trở 200k, tụ 5uF đường hồi tiếp."},
        }
    }
}

# ========================================================
# 3. GIAO DIỆN CHÍNH
# ========================================================
st.sidebar.title(f"👤 {user['ten']}")
if ngay_con_lai <= 7:
    st.sidebar.warning(f"🕒 Bản quyền còn {ngay_con_lai} ngày!")

menu = st.sidebar.radio("CHỨC NĂNG CHÍNH", 
    ["🔍 Tra mã lỗi", "🧠 Chẩn đoán (AI)", "📚 Sơ đồ thông minh", "💳 Gia hạn tự động"])

if menu == "Tra mã lỗi":
    st.header("🔍 TRA CỨU MÃ LỖI TỔNG HỢP")
    col1, col2 = st.columns(2)
    with col1:
        loai = st.selectbox("Loại máy", list(KHO_DATA.keys()))
    with col2:
        hang = st.selectbox("Hãng máy", list(KHO_DATA[loai].keys()))
    
    ma = st.text_input("Nhập mã lỗi:").upper().strip()
    if st.button("Tra cứu ngay"):
        if ma in KHO_DATA[loai][hang]:
            res = KHO_DATA[loai][hang][ma]
            st.info(f"📌 **Mô tả:** {res['loi']}")
            st.success(f"🛠️ **Cách sửa:**\n{res['pro']}")
        else:
            st.error("Dữ liệu đang được cập nhật.")

elif menu == "Gia hạn tự động":
    st.header("💳 GIA HẠN DỊCH VỤ")
    goi = st.radio("Chọn gói:", ["6 Tháng - 300k", "12 Tháng - 500k", "Vĩnh viễn - 1.5tr"], horizontal=True)
    tien = "300000" if "6 Tháng" in goi else ("500000" if "12 Tháng" in goi else "1500000")
    
    # THÔNG TIN VIETINBANK
    stk = "104881077679"
    ten_tk = "TRINH BA DUY"
    nd = f"GIA HAN {ma_khach}"
    qr_url = f"https://img.vietqr.io/image/ICB-{stk}-compact2.png?amount={tien}&addInfo={nd}&accountName={ten_tk}"
    
    st.image(qr_url, caption="Quét mã để thanh toán")
    st.success(f"Nội dung CK: {nd}")

if st.sidebar.button("Đăng xuất"):
    st.session_state['auth'] = None
    st.rerun()
