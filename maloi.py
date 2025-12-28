import streamlit as st
from datetime import datetime

# ========================================================
# 1. QUẢN LÝ TÀI KHOẢN (Đã sửa giao diện theo ảnh image_90cf49)
# ========================================================
DANH_SACH_KHACH_HANG = {
    "PRO-DUY-2025": {"ten": "Kỹ sư Ba Duy", "loai": "Pro", "han": "2030-12-31"},
    "ADMIN-888": {"ten": "Quản trị viên", "loai": "Pro", "han": "2030-12-31"},
}

if 'auth' not in st.session_state:
    st.session_state['auth'] = None

if not st.session_state['auth']:
    st.markdown("<h2 style='text-align: center;'>🔐 ĐĂNG NHẬP tra cứu mã lỗi thiết bị điện tử - BADUY@2025</h2>", unsafe_allow_html=True)
    st.warning("⚠️ Mỗi mã kích hoạt chỉ sử dụng cho 01 thiết bị duy nhất. Dùng chung mã sẽ bị khóa.")
    ma_nhap = st.text_input("Nhập mã cá nhân của bạn:", type="password").strip()
    
    if st.button("Kích hoạt bản quyền"):
        if ma_nhap in DANH_SACH_KHACH_HANG:
            st.session_state['auth'] = DANH_SACH_KHACH_HANG[ma_nhap]
            st.rerun()
        else:
            st.error("Mã kích hoạt không chính xác.")
    st.stop()

# ========================================================
# 2. KHO DỮ LIỆU TỔNG HỢP (Cập nhật từ ảnh & Video)
# ========================================================
user = st.session_state['auth']

data = {
    "Bếp Từ": {
        "Sunhouse": {
            "E0": {
                "loi": "Lỗi nhận biết điện áp đầu vào (Thường báo ngay khi cắm điện).", 
                "pro": "1. Kiểm tra cặp điện trở 200k (tổng 400k) đường AC báo về. \n2. Kiểm tra tụ lọc 4.7uF và diode bảo vệ 5V. \n3. Kiểm tra các điện trở dán 13k, 15k.",
                "video": "https://www.youtube.com/watch?v=J_iBHlMdcmk" # LINK VIDEO ĐÃ NẰM Ở ĐÂY
            },
            "E1": {"loi": "Quá nhiệt IGBT.", "pro": "Kiểm tra quạt làm mát, thay mỡ tản nhiệt IGBT, kiểm tra cảm biến NTC dưới lưng IGBT."},
            "E2": {"loi": "Quá nhiệt mặt kính.", "pro": "Kiểm tra cảm biến nhiệt mâm từ (100k), vệ sinh cửa lấy gió."},
        },
        },
        "Bosch": {
            "E22": {"loi": "Lỗi bo cảm ứng do độ ẩm, nước xâm nhập hoặc chập chân IC phím.", "pro": "Sấy khô bo mạch, kiểm tra cách điện vùng phím."},
            "F0": {"loi": "Lỗi đường truyền dẫn, cáp hoặc dây tín hiệu.", "pro": "Kiểm tra cáp kết nối giữa bo công suất và bo hiển thị."},
            "Er26": {"loi": "Lỗi relay chuyển tiếp, mạch điều khiển hoặc dây kết nối.", "pro": "Thay thế rơ-le trên bo mạch chính."},
        }
    },
    "Máy Giặt": {
        "Electrolux": {
            "E10": {"loi": "Lỗi nguồn cấp nước (Vòi đóng, bộ lọc tắc hoặc đường ống hỏng).", "pro": "Vệ sinh lưới lọc, kiểm tra van cấp nước."},
            "E20": {"loi": "Lỗi xả nước (Ống tắc, bơm hỏng hoặc hoạt động quá công suất).", "pro": "Kiểm tra bơm xả, vệ sinh hố bơm."},
            "E41": {"loi": "Cửa mở hoặc khóa cửa bị lỗi.", "pro": "Kiểm tra công tắc cửa, dây dẫn từ mạch đến khóa."},
            "E52": {"loi": "Không có tín hiệu từ bộ điều tốc (Tacho).", "pro": "Đo cuộn dây Tacho (cảm biến tốc độ) (120-180Ω), kiểm tra chổi than motor."},
            "E57": {"loi": "Inverter hút dòng quá nhiều (>15A).", "pro": "Kiểm tra motor, đo 3 cuộn dây motor, thay board Inverter nếu chập công suất."},
        }
    }
}

# ========================================================
# 3. GIAO DIỆN TRA CỨU (Cập nhật hiển thị VIDEO)
# ========================================================
st.markdown("<h1 style='text-align: center;'>🛠️ TRA CỨU MÃ LỖI - BẢN PRO</h1>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    loai_may = st.selectbox("Chọn loại thiết bị", list(data.keys()))
with col2:
    hang = st.selectbox("Chọn hãng", list(data[loai_may].keys()))

ma_input = st.text_input("Nhập mã lỗi (Ví dụ: E0, E41, E52...):").upper().strip()

if st.button("Tra cứu chuyên sâu"):
    if ma_input in data[loai_may][hang]:
        res = data[loai_may][hang][ma_input]
        
        # 1. Hiển thị mô tả lỗi (Giống ảnh image_91acdd)
        st.info(f"📌 **Mô tả lỗi:** {res['loi']}")
        
        st.divider()
        
        # 2. Hiển thị hướng dẫn PRO
        st.subheader("🛠️ HƯỚNG DẪN KHẮC PHỤC (PRO):")
        st.success(res['pro'])
        
        # 3. PHẦN QUAN TRỌNG: HIỂN THỊ VIDEO
        if "video" in res:
            st.markdown("---")
            st.markdown("### 📺 Video hướng dẫn sửa chữa thực tế:")
            st.video(res['video'])
        else:
            st.info("ℹ️ Mã lỗi này hiện đang được cập nhật video thực tế.")
            
    else:
        st.error("Mã lỗi chưa có trong hệ thống hoặc bạn nhập sai.")

st.divider()
st.markdown("<p style='text-align: center; color: gray;'>Hỗ trợ kỹ thuật: 0987973723</p>", unsafe_allow_html=True)

