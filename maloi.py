import streamlit as st
from datetime import datetime

# ========================================================
# 1. QUẢN LÝ KHÁCH HÀNG: MỖI MÃ CHỈ DÙNG CHO 1 NGƯỜI
# Bạn thêm/sửa khách hàng mới tại đây sau khi họ mua bản quyền
# ========================================================
DANH_SACH_KHACH_HANG = {
    "dungthu7ngay": {"ten": "Khách dùng thử", "loai": "Free", "han": "2026-01-05"},
    "VIP-BADUY-88": {"ten": "Kỹ sư Ba Duy", "loai": "Pro", "han": "2030-12-31"},
    "0987973723-PR": {"ten": "Khách hàng VIP 01", "loai": "Pro", "han": "2027-01-01"},
}

# Thiết lập giao diện
st.set_page_config(page_title="Tra cứu mã lỗi Baduy@2025", layout="centered")

# Kiểm tra trạng thái đăng nhập
if 'user_info' not in st.session_state:
    st.session_state['user_info'] = None

# GIAO DIỆN MÀN HÌNH KHÓA (Kích hoạt bản quyền)
if not st.session_state['user_info']:
    st.markdown("<h2 style='text-align: center;'>🔐 KÍCH HOẠT BẢN QUYỀN</h2>", unsafe_allow_html=True)
    st.warning("⚠️ Mỗi mã kích hoạt chỉ cấp quyền cho 01 người dùng duy nhất trên thiết bị này.")
    
    ma_nhap = st.text_input("Nhập mã bản quyền cá nhân:", type="password").strip()
    
    if st.button("Xác nhận kích hoạt"):
        if ma_nhap in DANH_SACH_KHACH_HANG:
            khach = DANH_SACH_KHACH_HANG[ma_nhap]
            today = datetime.now().strftime("%Y-%m-%d")
            
            if today <= khach["han"]:
                st.session_state['user_info'] = khach
                st.success(f"✅ Chào mừng {khach['ten']}!")
                st.rerun()
            else:
                st.error("❌ Mã của bạn đã hết hạn. Vui lòng liên hệ 0987973723 để gia hạn.")
        else:
            st.error("❌ Mã không tồn tại hoặc đã bị khóa.")
            
    st.info("💡 Liên hệ Zalo: 0987973723 để nhận mã kích hoạt cá nhân.")
    st.stop()

# ========================================================
# 2. NỘI DUNG CHUYÊN SÂU (Bản Pro có hướng dẫn đo kiểm)
# ========================================================
user = st.session_state['user_info']
st.markdown(f"<h1 style='text-align: center;'>🛠️ TRA CỨU MÃ LỖI - BẢN {user['loai'].upper()}</h1>", unsafe_allow_html=True)
st.sidebar.markdown(f"👤 Khách: **{user['ten']}**")
st.sidebar.markdown(f"📅 Hạn dùng: **{user['han']}**")

data = {
    "Điều Hòa": {
        "Daikin": {
            "U0": {"Free": "Thiếu ga hoặc nghẹt hệ thống ga.", "Pro": "Thiếu ga. Kiểm tra: 1. Áp suất tĩnh và áp suất chạy. 2. Kiểm tra rò rỉ tại giắc co. 3. Đo dòng điện block."},
            "A1": {"Free": "Lỗi bo mạch dàn lạnh.", "Pro": "Lỗi bo mạch. Kiểm tra: 1. Nguồn 5V/12V trên bo. 2. Thử thay IC nhớ (EEPROM)."}
        },
        "Panasonic": {
            "H11": {"Free": "Lỗi kết nối dàn nóng/lạnh.", "Pro": "Lỗi giao tiếp. Kiểm tra: 1. Dây tín hiệu số 3. 2. Bo dàn lạnh lỗi phát tín hiệu. 3. Bo dàn nóng lỗi nhận."}
        }
    },
    "Bếp Từ": {
        "Sunhouse": {
            "E0": {"Free": "Chưa có nồi/Nồi không phù hợp.", "Pro": "Lỗi nhận nồi. Kiểm tra: 1. Tụ lọc 5uF. 2. Trở hồi tiếp cảm biến (thường 100k-470k). 3. Mâm từ."},
            "E1": {"Free": "Bếp bị quá nhiệt.", "Pro": "Quá nhiệt IGBT. Kiểm tra: 1. Quạt tản nhiệt 18V. 2. Cảm biến gắn trên nhôm tản nhiệt. 3. Khe thông gió."}
        },
        "Bosch": {
            "F0": {"Free": "Lỗi cảm biến nhiệt.", "Pro": "Lỗi cảm biến mặt kính. Kiểm tra: 1. Giắc cắm cảm biến. 2. Trị số cảm biến (thường 10k-50k ở 25°C)."}
        }
    },
    "Máy Giặt": {
        "Samsung": {
            "4C": {"Free": "Nước không cấp vào.", "Pro": "Lỗi cấp nước. Kiểm tra: 1. Van cấp nước (đo cuộn dây). 2. Lưới lọc bẩn. 3. Lệnh từ bo mạch."},
            "5C": {"Free": "Nước không thoát ra.", "Pro": "Lỗi thoát nước. Kiểm tra: 1. Bơm xả (đo 220V). 2. Tắc nghẽn ống thoát. 3. Phao áp lực."}
        }
    }
}

# Giao diện chọn loại máy và hãng
col1, col2 = st.columns(2)
with col1:
    loai_may = st.selectbox("Chọn loại máy", list(data.keys()))
with col2:
    hang = st.selectbox("Chọn hãng", list(data[loai_may].keys()))

ma_loi = st.text_input("Nhập mã lỗi:").upper().strip()

if st.button("Tra cứu nhanh"):
    if ma_loi in data[loai_may][hang]:
        ket_qua = data[loai_may][hang][ma_loi]
        if user['loai'] == "Pro":
            st.success(f"🔍 **HƯỚNG DẪN SỬA CHỮA PRO:** {ket_qua['Pro']}")
        else:
            st.warning(f"ℹ️ **THÔNG TIN:** {ket_qua['Free']}")
            st.info("👉 Để xem hướng dẫn đo kiểm linh kiện chi tiết, hãy nâng cấp bản PRO!")
    else:
        st.error("Dữ liệu cho mã này đang được cập nhật. Vui lòng gọi Hotline để hỗ trợ.")

if st.sidebar.button("Đăng xuất / Đổi thiết bị"):
    st.session_state['user_info'] = None
    st.rerun()

st.divider()
st.markdown("<p style='text-align: center; color: gray;'>Baduy@2025 - Hotline hỗ trợ kỹ thuật: 0987973723</p>", unsafe_allow_html=True)
