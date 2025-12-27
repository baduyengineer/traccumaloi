import streamlit as st
from datetime import datetime, timedelta
import random
import string

# ========================================================
# 1. QUẢN LÝ KHÁCH HÀNG & MÃ KÍCH HOẠT
# ========================================================
# Bạn thêm mã khách hàng Pro vào danh sách này
DANH_SACH_KHACH_HANG = {
    "free3day": {"ten": "Khách dùng thử", "loai": "Free", "han": "2025-12-31"},
    "PRO-DUY-2025": {"ten": "Kỹ sư Ba Duy", "loai": "Pro", "han": "2030-12-31"},
    "ADMIN-888": {"ten": "Quản trị viên", "loai": "Pro", "han": "2030-12-31"},
}

st.set_page_config(page_title="Baduy@2025 - Kho Mã Lỗi Việt Nam", layout="centered")

if 'auth' not in st.session_state:
    st.session_state['auth'] = None

# GIAO DIỆN ĐĂNG NHẬP
if not st.session_state['auth']:
    st.markdown("<h2 style='text-align: center;'>🔐 ĐĂNG NHẬP HỆ THỐNG BADUY@2025</h2>", unsafe_allow_html=True)
    st.warning("⚠️ Mỗi mã kích hoạt chỉ sử dụng cho 01 thiết bị duy nhất. Dùng chung mã sẽ bị khóa.")
    
    ma_nhap = st.text_input("Nhập mã cá nhân của bạn:", type="password").strip()
    
    if st.button("Kích hoạt bản quyền"):
        if ma_nhap in DANH_SACH_KHACH_HANG:
            khach = DANH_SACH_KHACH_HANG[ma_nhap]
            today = datetime.now().strftime("%Y-%m-%d")
            
            if today <= khach["han"]:
                st.session_state['auth'] = khach
                st.success(f"✅ Chào mừng {khach['ten']}!")
                st.rerun()
            else:
                st.error("❌ Mã đã hết hạn (Giới hạn 3 ngày dùng thử). Liên hệ 0987973723 để mua bản PRO.")
        else:
            st.error("❌ Mã không tồn tại hoặc đã bị thu hồi.")
    st.info("💡 Liên hệ Zalo mua bản PRO: 0987973723")
    st.stop()

# ========================================================
# 2. DỮ LIỆU TỔNG HỢP (Bếp Từ, Máy Giặt, Điều Hòa)
# ========================================================
user = st.session_state['auth']

data = {
    "Bếp Từ": {
        "Sunhouse": {
            "E0": {"loi": "Chưa có nồi/Nồi không hợp.", "pro": "Kiểm tra tụ lọc 5uF; Đo trở hồi tiếp nhận nồi (100k-470k); Kiểm tra biến áp xung."},
            "E1": {"loi": "Quá nhiệt IGBT.", "pro": "Kiểm tra quạt 18V; Thay mỡ tản nhiệt; Đo cảm biến NTC (10k-100k)."},
            "E2": {"loi": "Cảm biến mặt kính lỗi.", "pro": "Đo trị số cảm biến (thường 100k); Kiểm tra giắc cắm; Thay cảm biến mới."},
        },
        "Bosch": {
            "F0": {"loi": "Lỗi truyền thông.", "pro": "Kiểm tra kết nối giữa bo điều khiển và bo công suất; Kiểm tra nguồn 5V."},
            "E": {"loi": "Lỗi phần mềm/Phím bấm.", "pro": "Vệ sinh mặt kính khu vực phím; Kiểm tra lò xo phím cảm ứng."},
        },
        "Chefs": {
            "E1": {"loi": "Lỗi quá nhiệt.", "pro": "Kiểm tra quạt làm mát; Kiểm tra cảm biến nhiệt đáy nồi."},
            "E2": {"loi": "Điện áp không ổn định.", "pro": "Kiểm tra nguồn cấp AC; Đo mạch nhận diện điện áp trên bo."},
        }
    },
    "Máy Giặt": {
        "Samsung": {
            "4C": {"loi": "Nước không cấp.", "pro": "Đo cuộn dây van cấp (3k-4k Ohm); Kiểm tra lệnh từ bo; Vệ sinh lưới lọc."},
            "5C": {"loi": "Nước không thoát.", "pro": "Kiểm tra bơm xả (đo 220V); Vệ sinh hố bơm; Kiểm tra phao áp lực."},
            "DC": {"loi": "Lỗi cửa mở.", "pro": "Kiểm tra công tắc cửa; Kiểm tra dây dẫn từ công tắc về bo mạch."},
        },
        "LG": {
            "IE": {"loi": "Không vào nước.", "pro": "Kiểm tra van cấp; Kiểm tra phao áp lực; Đo dây tín hiệu từ phao về bo."},
            "OE": {"loi": "Không thoát nước.", "pro": "Kiểm tra bơm xả; Thông tắc ống thoát; Kiểm tra lệnh xả từ bo mạch."},
            "PE": {"loi": "Lỗi phao áp lực.", "pro": "Đo tần số phao; Kiểm tra giắc cắm phao bị oxy hóa."},
        },
        "Electrolux": {
            "E10": {"loi": "Lỗi cấp nước.", "pro": "Kiểm tra áp lực nước đầu vào; Kiểm tra van cấp nước và mạch điều khiển."},
            "E20": {"loi": "Lỗi xả nước.", "pro": "Kiểm tra bơm xả; Kiểm tra tắc nghẽn đường ống thoát nước."},
        }
    },
    "Điều Hòa": {
        "Daikin": {
            "U0": {"loi": "Thiếu ga / Nghẹt ga.", "pro": "Kiểm tra áp suất ga; Kiểm tra đầu giắc co; Kiểm tra van tiết lưu điện từ."},
            "A6": {"loi": "Lỗi quạt dàn lạnh.", "pro": "Đo cuộn dây motor quạt; Kiểm tra tụ quạt; Kiểm tra lệnh từ bo lạnh."},
            "L5": {"loi": "Lỗi block (máy nén).", "pro": "Đo điện trở cuộn dây block; Kiểm tra bo công suất dàn nóng."},
        },
        "Panasonic": {
            "H11": {"loi": "Lỗi giao tiếp nội bộ.", "pro": "Đo thông mạch dây số 3; Kiểm tra Opto phát/nhận trên bo lạnh và nóng."},
            "F95": {"loi": "Quá nhiệt dàn nóng.", "pro": "Kiểm tra quạt dàn nóng; Kiểm tra ga; Vệ sinh dàn nóng."},
        }
    }
}

# ========================================================
# 3. GIAO DIỆN CHÍNH
# ========================================================
st.sidebar.markdown(f"👤 Khách: **{user['ten']}**")
st.sidebar.markdown(f"🏷️ Loại: **{user['loai']}**")
st.sidebar.markdown(f"📅 Hạn: {user['han']}")

st.markdown(f"<h2 style='text-align: center;'>🛠️ TRA CỨU MÃ LỖI - BẢN {user['loai'].upper()}</h2>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    loai_may = st.selectbox("Chọn loại thiết bị", list(data.keys()))
with col2:
    hang = st.selectbox("Chọn hãng", list(data[loai_may].keys()))

ma_input = st.text_input("Nhập mã lỗi (Ví dụ: E0, H11, 4C...):").upper().strip()

if st.button("Tra cứu chuyên sâu"):
    if ma_input in data[loai_may][hang]:
        res = data[loai_may][hang][ma_input]
        st.warning(f"📌 **Mô tả lỗi:** {res['loi']}")
        
        st.markdown("---")
        st.subheader("🛠️ HƯỚNG DẪN KHẮC PHỤC (PRO):")
        
        if user['loai'] == "Pro":
            st.success(f"✅ **Dành cho thợ:**\n{res['pro']}")
        else:
            st.error("🔒 Hướng dẫn đo kiểm linh kiện chi tiết bị khóa.")
            st.info("👉 Vui lòng liên hệ 0987973723 để nâng cấp bản PRO.")
    else:
        st.error("Mã lỗi chưa có trong kho dữ liệu. Vui lòng liên hệ hỗ trợ.")

# ========================================================
# 4. TÍNH NĂNG ADMIN: TẠO MÃ NHANH (Chỉ Admin thấy)
# ========================================================
if user['ten'] == "Quản trị viên":
    st.divider()
    with st.expander("🔑 CÔNG CỤ TẠO MÃ DÙNG THỬ (ADMIN ONLY)"):
        if st.button("Tạo mã dùng thử 3 ngày"):
            random_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            exp_date = (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d")
            st.code(f"Mã: {random_code} | Hạn: {exp_date}")
            st.write("Hãy copy mã này và dán vào danh sách DANH_SACH_KHACH_HANG trên GitHub.")

if st.sidebar.button("Đăng xuất"):
    st.session_state['auth'] = None
    st.rerun()

st.divider()
st.markdown("<p style='text-align: center; color: gray;'>Thiết kế bởi Baduy@2025 - Hotline: 0987973723</p>", unsafe_allow_html=True)
