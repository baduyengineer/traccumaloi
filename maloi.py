import streamlit as st
from datetime import datetime

# ========================================================
# 1. QUẢN LÝ KHÁCH HÀNG (Mỗi mã 1 người - 3 ngày dùng thử)
# ========================================================
# Bạn chỉ cần sửa danh sách này trên GitHub để cấp mã mới
DANH_SACH_KHACH_HANG = {
    "dungthu3ngay": {"ten": "Khách dùng thử", "loai": "Free", "han": "2025-12-30"},
    "baduypro": {"ten": "Kỹ sư Ba Duy", "loai": "Pro", "han": "2030-12-31"},
    "BINH-0912": {"ten": "Anh Bình Thủ Đức", "loai": "Pro", "han": "2027-01-01"},
}

st.set_page_config(page_title="Baduy@2025 - Tra cứu mã lỗi", layout="centered")

# Khởi tạo trạng thái đăng nhập
if 'auth' not in st.session_state:
    st.session_state['auth'] = None

# GIAO DIỆN MÀN HÌNH KHÓA
if not st.session_state['auth']:
    st.markdown("<h2 style='text-align: center;'>🔐 ĐĂNG NHẬP HỆ THỐNG</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Mỗi mã kích hoạt chỉ sử dụng cho 01 khách hàng duy nhất.</p>", unsafe_allow_html=True)
    
    ma_nhap = st.text_input("Nhập mã của bạn:", type="password").strip()
    
    if st.button("Kích hoạt ngay"):
        if ma_nhap in DANH_SACH_KHACH_HANG:
            khach = DANH_SACH_KHACH_HANG[ma_nhap]
            today = datetime.now().strftime("%Y-%m-%d")
            
            if today <= khach["han"]:
                st.session_state['auth'] = khach
                st.session_state['ma_dang_nhap'] = ma_nhap
                st.success(f"✅ Chào mừng {khach['ten']}!")
                st.rerun()
            else:
                st.error("❌ Mã đã hết hạn (Giới hạn 3 ngày dùng thử). Vui lòng mua bản PRO.")
        else:
            st.error("❌ Mã không chính xác hoặc đã bị khóa do dùng chung.")
            
    st.info("💡 Liên hệ mua bản PRO (Mã riêng chủ): 0987973723 (Kỹ sư Ba Duy)")
    st.stop()

# ========================================================
# 2. KIỂM TRA CHỐNG DÙNG LẬU (Đá người dùng nếu sai mã)
# ========================================================
user = st.session_state['auth']
st.sidebar.markdown(f"👤 Khách hàng: **{user['ten']}**")
st.sidebar.markdown(f"🏷️ Phiên bản: **{user['loai']}**")
st.sidebar.markdown(f"📅 Hạn dùng: {user['han']}")

if st.sidebar.button("Đăng xuất (Thoát mã)"):
    st.session_state['auth'] = None
    st.rerun()

# ========================================================
# 3. KHO DỮ LIỆU MÃ LỖI & HƯỚNG DẪN PRO
# ========================================================
st.markdown(f"<h2 style='text-align: center;'>🛠️ KHO MÃ LỖI - BẢN {user['loai'].upper()}</h2>", unsafe_allow_html=True)

data = {
    "Bếp Từ": {
        "Sunhouse": {
            "E0": {"loi": "Chưa có nồi hoặc nồi không phù hợp.", "pro": "1. Kiểm tra tụ lọc 5uF. 2. Đo trở hồi tiếp nhận nồi (100k-470k). 3. Kiểm tra biến áp xung."},
            "E1": {"loi": "Quá nhiệt IGBT.", "pro": "1. Kiểm tra quạt 18V. 2. Đo cảm biến nhiệt lưng IGBT. 3. Vệ sinh khe gió."},
        },
        "Bosch": {
            "F0": {"loi": "Lỗi cảm biến mặt kính.", "pro": "1. Đo trị số cảm biến (thường 50k-100k). 2. Kiểm tra giắc cắm trên bo."},
        }
    },
    "Điều Hòa": {
        "Daikin": {
            "U0": {"loi": "Thiếu ga/Nghẹt ga.", "pro": "1. Kiểm tra áp suất ga tĩnh/chạy. 2. Kiểm tra đầu giắc co. 3. Đo dòng block."},
            "A1": {"loi": "Lỗi bo mạch dàn lạnh.", "pro": "1. Kiểm tra nguồn 5V/12V. 2. Thử thay IC nhớ EEPROM."},
        }
    }
}

# Giao diện tra cứu
loai_may = st.selectbox("Chọn loại máy", list(data.keys()))
hang = st.selectbox("Chọn hãng", list(data[loai_may].keys()))
ma = st.text_input("Nhập mã lỗi:").upper().strip()

if st.button("Tra cứu nhanh"):
    if ma in data[loai_may][hang]:
        ket_qua = data[loai_may][hang][ma]
        st.warning(f"📌 **Mô tả lỗi:** {ket_qua['loi']}")
        
        st.markdown("---")
        st.subheader("🛠️ HƯỚNG DẪN KHẮC PHỤC CHUYÊN SÂU:")
        
        if user['loai'] == "Pro":
            st.success(f"**Các bước xử lý dành cho thợ:**\n{ket_qua['pro']}")
        else:
            st.error("🔒 Tính năng hướng dẫn đo kiểm linh kiện chỉ dành cho bản PRO.")
            st.info("👉 Vui lòng liên hệ 0987973723 để nhận mã PRO cá nhân (Dùng riêng cho bạn).")
    else:
        st.error("Dữ liệu đang được cập nhật...")

st.divider()
st.markdown("<p style='text-align: center; color: gray;'>Thiết kế bởi Baduy@2025 - Hotline: 0987973723</p>", unsafe_allow_html=True)

