import streamlit as st
from datetime import datetime, timedelta
import random
import string

# ========================================================
# 1. QUẢN LÝ KHÁCH HÀNG
# ========================================================
DANH_SACH_KHACH_HANG = {
    "free3day": {"ten": "Thợ dùng thử", "loai": "Free", "han": "2025-12-31"},
    "PRO-DUY-2025": {"ten": "Kỹ sư Ba Duy", "loai": "Pro", "han": "2030-12-31"},
    "ADMIN-888": {"ten": "Quản trị viên", "loai": "Pro", "han": "2030-12-31"},
}

st.set_page_config(page_title="Baduy@2025 - Kho Mã Lỗi Việt Nam", layout="centered")

if 'auth' not in st.session_state:
    st.session_state['auth'] = None

# GIAO DIỆN ĐĂNG NHẬP
if not st.session_state['auth']:
    st.markdown("<h2 style='text-align: center;'>🔐 ĐĂNG NHẬP TRA CỨU MÃ LỖI THIẾT BỊ ĐIỆN TỬ - BADUY@2025</h2>", unsafe_allow_html=True)
    ma_nhap = st.text_input("Nhập mã kích hoạt:", type="password").strip()
    if st.button("Kích hoạt ngay"):
        if ma_nhap in DANH_SACH_KHACH_HANG:
            khach = DANH_SACH_KHACH_HANG[ma_nhap]
            if datetime.now().strftime("%Y-%m-%d") <= khach["han"]:
                st.session_state['auth'] = khach
                st.success(f"✅ Chào mừng {khach['ten']}!")
                st.rerun()
            else: st.error("❌ Mã hết hạn.")
        else: st.error("❌ Mã sai hoặc bị khóa.")
    st.info("📲 Mua bản PRO (Full Video/Ảnh): 0987973723")
    st.stop()

# ========================================================
# 2. TỔNG HỢP DỮ LIỆU TẤT CẢ CÁC HÃNG (CẬP NHẬT ĐẦY ĐỦ)
# ========================================================
user = st.session_state['auth']

data = {
    "Bếp Từ": {
        "Sunhouse": {
            "E0": {
                "loi": "Lỗi nhận biết điện áp đầu vào (báo ngay khi cắm điện).", 
                "pro": "Đứt/trị số sai 2 con điện trở 200k (mắc nối tiếp đường AC). Kiểm tra tụ lọc 4.7uF và diode bảo vệ 5V.",
                "video": "https://www.youtube.com/watch?v=J_iBHlMdcmk"
            },
            "E1": {"loi": "Quá nhiệt IGBT.", "pro": "Kiểm tra quạt 18V, thay mỡ tản nhiệt, đo cảm biến NTC 100k."},
            "E2": {"loi": "Quá nhiệt mặt kính.", "pro": "Kiểm tra cảm biến nhiệt mâm từ, vệ sinh khe gió."},
        },
        "Midea": {
            "E0": {"loi": "Lỗi mạch nhận nồi hoặc cảm biến IGBT.", "pro": "Kiểm tra tụ 0.33uF, trở hồi tiếp nhận nồi 470k-820k."},
            "E1": {"loi": "Không nồi/Nồi không hợp.", "pro": "Kiểm tra mạch driver kích IGBT."},
            "E3": {"loi": "Điện áp cao (>260V).", "pro": "Kiểm tra mạch bảo vệ OVP về vi xử lý."},
            "E4": {"loi": "Điện áp thấp (<160V).", "pro": "Kiểm tra tụ lọc nguồn 5uF, cầu diode."},
        },
        "Elmich": {
            "E1": {"loi": "Quá nhiệt.", "pro": "Kiểm tra quạt, cảm biến mâm dây."},
            "E2": {"loi": "Áp cao.", "pro": "Đo mạch chia áp hồi tiếp."},
            "E3": {"loi": "Áp thấp.", "pro": "Kiểm tra nguồn cấp AC, tụ nguồn."},
            "E6": {"loi": "Lỗi cảm biến.", "pro": "Thay cảm biến 100k, vệ sinh giắc cắm."},
        },
        "Bosch": {
            "E22": {"loi": "Lỗi bo cảm ứng (ẩm/chập).", "pro": "Sấy bo, kiểm tra IC phím."},
            "F0": {"loi": "Lỗi truyền thông cáp.", "pro": "Thay cáp nối bo công suất và hiển thị."},
            "Er26": {"loi": "Lỗi Relay.", "pro": "Kiểm tra rơ-le trên bo công suất."},
        }
    },
    "Máy Giặt": {
        "Electrolux": {
            "E10": {"loi": "Nước không cấp.", "pro": "Kiểm tra cuộn dây van cấp, vệ sinh lưới lọc."},
            "E20": {"loi": "Không thoát nước.", "pro": "Vệ sinh bơm xả, đo cuộn dây bơm (150-200 Ohm)."},
            "E23": {"loi": "Hư Triac bơm xả.", "pro": "Đo Triac trên board mạch chính, thay board nếu cần."},
            "E41": {"loi": "Lỗi khóa cửa.", "pro": "Kiểm tra tiếp điểm khóa cửa, thay khóa mới."},
            "E52": {"loi": "Lỗi Tacho motor.", "pro": "Đo cuộn Tacho (hay cuộn dây sensor tốc độ) (120-180 Ohm), kiểm tra chổi than."},
            "E57": {"loi": "Inverter quá dòng (>15A).", "pro": "Kiểm tra motor, đo 3 cuộn dây motor phải bằng nhau."},
            "E91": {"loi": "Lỗi liên lạc board.", "pro": "Kiểm tra cáp kết nối giữa board nguồn và board hiển thị."},
        },
        "Samsung": {
            "4C": {"loi": "Lỗi cấp nước.", "pro": "Đo van cấp, kiểm tra mạch điều khiển van."},
            "5C": {"loi": "Lỗi thoát nước.", "pro": "Kiểm tra bơm xả, ống xả bị tắc."},
            "DC": {"loi": "Cửa mở.", "pro": "Kiểm tra công tắc cửa, dây tín hiệu từ công tắc cửa về mạch điều khiển."},
        }
    },
    "Điều Hòa": {
        "Daikin": {
            "U0": {"loi": "Thiếu ga/Nghẹt ga.", "pro": "Kiểm tra giắc co, áp suất ga chạy."},
            "A6": {"loi": "Lỗi quạt dàn lạnh.", "pro": "Đo motor quạt, kiểm tra tụ quạt."},
            "L5": {"loi": "Lỗi máy nén (Inverter).", "pro": "Đo điện trở block, kiểm tra bo công suất dàn nóng."},
        }
    }
}

# ========================================================
# 3. GIAO DIỆN CHÍNH & HIỂN THỊ
# ========================================================
st.sidebar.markdown(f"👤 **{user['ten']}** ({user['loai']})")
st.markdown(f"<h2 style='text-align: center;'>🛠️ PHẦN MỀM TRA CỨU MÃ LỖI - BADUY@2025</h2>", unsafe_allow_html=True)

loai_may = st.selectbox("Chọn loại thiết bị", list(data.keys()))
hang = st.selectbox("Chọn hãng", list(data[loai_may].keys()))
ma_input = st.text_input("Nhập mã lỗi:").upper().strip()

if st.button("Tra cứu chuyên sâu"):
    if ma_input in data[loai_may][hang]:
        res = data[loai_may][hang][ma_input]
        st.warning(f"📌 **Mô tả:** {res['loi']}")
        
        if user['loai'] == "Pro":
            st.success(f"🛠️ **HƯỚNG DẪN PRO:** {res['pro']}")
            if 'video' in res:
                st.markdown("📺 **Video hướng dẫn:**")
                st.video(res['video'])
            if 'anh' in res:
                st.image(res['anh'], caption="Hình ảnh đo kiểm thực tế")
        else:
            st.error("🔒 Hướng dẫn đo kiểm & Video bị khóa. Vui lòng nâng cấp PRO.")
    else:
        st.error("Mã lỗi này chưa có trong hệ thống.")

# Admin Tool
if user['ten'] == "Quản trị viên":
    with st.expander("🔑 Quản trị (Tạo mã)"):
        if st.button("Tạo mã mới"):
            st.code(''.join(random.choices(string.ascii_uppercase + string.digits, k=6)))

st.divider()
st.markdown("<p style='text-align: center;'>Hotline: 0987973723</p>", unsafe_allow_html=True)
