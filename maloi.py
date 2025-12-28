import streamlit as st
from datetime import datetime, timedelta

# ========================================================
# 4. QUẢN LÝ BẢN QUYỀN CHUYÊN NGHIỆP (Mục 4)
# ========================================================
# Giả sử hôm nay là 2025-12-28
DANH_SACH_KHACH_HANG = {
    "PRO-DUY-2025": {"ten": "Kỹ sư Ba Duy", "loai": "Pro", "han": "2026-01-05"}, # Sắp hết hạn để test
    "ADMIN-888": {"ten": "Quản trị viên", "loai": "Pro", "han": "2030-12-31"},
}

if 'auth' not in st.session_state:
    st.session_state['auth'] = None

if not st.session_state['auth']:
    st.markdown("<h2 style='text-align: center;'>🔐 KÍCH HOẠT TRA CỨU MÃ LỖI -  BADUY@2025</h2>", unsafe_allow_html=True)
    ma_nhap = st.text_input("Nhập mã cá nhân của bạn:", type="password").strip()
    if st.button("Kích hoạt ngay"):
        if ma_nhap in DANH_SACH_KHACH_HANG:
            st.session_state['auth'] = DANH_SACH_KHACH_HANG[ma_nhap]
            st.rerun()
        else:
            st.error("Mã không hợp lệ.")
    st.stop()

# --- Kiểm tra thời hạn bản quyền và thông báo (Mục 4) ---
user = st.session_state['auth']
ngay_het_han = datetime.strptime(user['han'], "%Y-%m-%d")
ngay_con_lai = (ngay_het_han - datetime.now()).days

if ngay_con_lai <= 7:
    st.sidebar.warning(f"⚠️ Bản quyền còn {ngay_con_lai} ngày. Liên hệ Duy (0987973723) để gia hạn!")

# ========================================================
# 2. DỮ LIỆU TRA CỨU (Giữ nguyên các phần đã chuẩn hóa)
# ========================================================
data = {
    "Bếp Từ": {
        "Sunhouse": {
            "E0": {
                "loi": "Lỗi mạch nhận biết điện áp đầu vào.", 
                "pro": "Kiểm tra trở 200k, tụ lọc 4.7uF đường AC.",
                "video": "https://www.youtube.com/watch?v=J_iBHlMdcmk"
            },
        }
    }
}

# Dữ liệu cho Chẩn đoán theo biểu hiện (Mục 3)
CHUC_NANG_AI = {
    "Bếp Từ": {
        "Bếp không nhận nồi (không báo lỗi)": "Kiểm tra tụ cộng hưởng 0.33uF, kiểm tra mạch Driver và trở hồi tiếp.",
        "Bếp nổ cầu chì/chập IGBT": "Kiểm tra cầu diode, thay IGBT mới và phải kiểm tra kỹ mạch lái trước khi cắm điện.",
        "Mất nguồn hoàn toàn": "Kiểm tra IC nguồn (Viper12A/22A), trở cầu chì và diode nắn nguồn 300V."
    },
    "Máy Giặt": {
        "Máy rung lắc mạnh khi vắt": "Kiểm tra 4 thụt giảm xóc, kiểm tra cân bằng lồng hoặc hỏng bi/trục.",
        "Nước chảy vào liên tục": "Vệ sinh hoặc thay van cấp nước (bị kẹt rác), kiểm tra triac điều khiển cấp nước trên mạch."
    }
}

# ========================================================
# 3. GIAO DIỆN CHÍNH (Tích hợp Mục 3)
# ========================================================
st.sidebar.title(f"Chào, {user['ten']}")
menu = st.sidebar.radio("CHỨC NĂNG", ["Tra mã lỗi", "Chẩn đoán bệnh (AI)", "Gia hạn bản quyền"])

if menu == "Tra mã lỗi":
    st.header("🔍 TRA CỨU MÃ LỖI NHANH")
    # ... (Giữ nguyên code tra cứu mã lỗi cũ ở đây) ...
    loai = st.selectbox("Thiết bị", list(data.keys()))
    hang = st.selectbox("Hãng", list(data[loai].keys()))
    ma = st.text_input("Mã lỗi:").upper().strip()
    if st.button("Tra cứu"):
        if ma in data[loai][hang]:
            res = data[loai][hang][ma]
            st.info(f"📌 {res['loi']}")
            st.success(f"🛠️ Hướng dẫn: {res['pro']}")
            if "video" in res: st.video(res['video'])

elif menu == "Chẩn đoán bệnh (AI)":
    st.header("🧠 CHẨN ĐOÁN THEO BIỂU HIỆN")
    st.write("Dành cho các trường hợp máy hỏng nhưng **không hiện mã lỗi**.")
    
    loai_ai = st.selectbox("Chọn loại thiết bị", list(CHUC_NANG_AI.keys()))
    bieu_hien = st.selectbox("Máy đang bị làm sao?", list(CHUC_NANG_AI[loai_ai].keys()))
    
    if st.button("Phân tích nguyên nhân"):
        st.subheader("📋 Kết quả phân tích kỹ thuật:")
        st.success(CHUC_NANG_AI[loai_ai][bieu_hien])
        st.info("💡 Lưu ý: Đây là kinh nghiệm thực tế, hãy đo đạc kỹ trước khi thay linh kiện.")

elif menu == "Gia hạn bản quyền":
    st.header("💳 GIA HẠN DỊCH VỤ")
    st.write(f"Gói hiện tại: **{user['loai']}**")
    st.write(f"Ngày hết hạn: **{user['han']}**")
    st.divider()
    st.write("Để gia hạn hoặc nâng cấp lên bản PRO vĩnh viễn, vui lòng chuyển khoản theo thông tin:")
    st.code("STK: 104881077679 - Ngân hàng: VietinBank\Chủ TK: TRINH BA DUY\Nội dung: GIA HAN [MÃ CỦA BẠN]")
    st.success("Sau khi chuyển khoản, hệ thống sẽ tự động cập nhật sau 5 phút.")

if st.sidebar.button("Đăng xuất"):
    st.session_state['auth'] = None
    st.rerun()
