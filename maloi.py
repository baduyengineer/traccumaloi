import streamlit as st
from datetime import datetime, timedelta

# 1. CẤU HÌNH HỆ THỐNG
st.set_page_config(page_title="Hệ thống Ba Duy v10.0", layout="wide")

# QUẢN LÝ NGƯỜI DÙNG
today = datetime.now()
DANH_SACH_KHACH_HANG = {
    "DUY-FREE-3D": {"ten": "Khách dùng thử", "loai": "Trial", "ngay_dk": today},
    "PRO-DUY-2025": {"ten": "Kỹ sư Ba Duy", "loai": "Pro", "han": "2026-01-05"},
}

if 'auth' not in st.session_state:
    st.session_state['auth'] = None

# --- MÀN HÌNH ĐĂNG NHẬP ---
if st.session_state['auth'] is None:
    st.title("🔐 HỆ THỐNG KỸ THUẬT BADUY@2025")
    st.info("💡 Mã dùng thử: DUY-FREE-3D")
    ma_nhap = st.text_input("Nhập mã kích hoạt:", type="password").strip()
    if st.button("Kích hoạt ngay"):
        if ma_nhap in DANH_SACH_KHACH_HANG:
            st.session_state['auth'] = DANH_SACH_KHACH_HANG[ma_nhap]
            st.session_state['ma_kich_hoat'] = ma_nhap
            st.success("✅ Thành công! Hãy F5 trang.")
        else: st.error("Mã không đúng!")
    st.stop()

# --- XỬ LÝ HẠN DÙNG (HIỂN THỊ LÊN TRÊN CÙNG ĐỂ DỄ NHÌN TRÊN ĐIỆN THOẠI) ---
user = st.session_state['auth']
is_expired = False

# Tạo một Header nổi bật cho Mobile
st.markdown(f"### 👤 Chào: {user['ten']}")

if user.get("loai") == "Trial":
    han_dung = user["ngay_dk"] + timedelta(days=3)
    con_lai = (han_dung - datetime.now()).days
    if con_lai < 0:
        is_expired = True
        st.error("🚫 ĐÃ HẾT HẠN DÙNG THỬ 3 NGÀY")
    else:
        st.warning(f"⏳ BẠN ĐANG DÙNG THỬ (CÒN {con_lai + 1} NGÀY)")
else:
    st.success(f"✅ BẢN QUYỀN PRO: Hạn dùng đến {user['han']}")

# --- MENU CHÍNH (Dạng nút bấm to cho dễ chạm trên điện thoại) ---
if is_expired:
    menu = "💳 Gia hạn tự động"
else:
    menu = st.selectbox("CHỌN CHỨC NĂNG:", 
                       ["🔍 Tra mã lỗi", "🧠 Chẩn đoán (AI)", "📚 Sơ đồ thông minh", "💳 Gia hạn tự động"])

st.divider()

# --- KHO DỮ LIỆU TỔNG HỢP ---
KHO_DATA = {
    "Bếp Từ": {
        "Sunhouse": {"E0": "Lỗi nhận nồi. Kiểm tra trở 200k, tụ 5uF, 0.33uF.", "E1": "Quá nhiệt."},
        "BIÊU_HIỆN_AI": {
            "Bếp không nhận nồi": "Giải pháp: Kiểm tra tụ lọc nguồn 5uF, tụ cộng hưởng 0.33uF và các điện trở hồi tiếp (240k, 330k, 470k, 820k).",
            "Mất nguồn hoàn toàn": "Giải pháp: Kiểm tra cầu chì, cầu điốt. Nếu chập IGBT thường do driver hỏng hoặc tụ cộng hưởng yếu.",
            "Nhảy Aptomat": "Giải pháp: Chập IGBT hoặc chập cầu điốt chỉnh lưu."
        }
    },
    "Máy Giặt": {
        "Electrolux": {"E10": "Lỗi cấp nước.", "E20": "Lỗi xả nước."},
        "BIÊU_HIỆN_AI": {
            "Rung lắc mạnh khi vắt": "Giải pháp: Kiểm tra giảm xóc (thụt), lò xo lồng giặt và độ cân bằng mặt sàn.",
            "Máy không quay lồng": "Giải pháp: Kiểm tra chổi than motor hoặc dây curoa bị tuột/đứt."
        }
    }
}

# 1. TRA MÃ LỖI
if menu == "🔍 Tra mã lỗi":
    st.subheader("🔍 TRA CỨU MÃ LỖI")
    loai = st.selectbox("Thiết bị", list(KHO_DATA.keys()))
    hang = st.selectbox("Hãng", [h for h in KHO_DATA[loai].keys() if h != "BIÊU_HIỆN_AI"])
    ma = st.text_input("Nhập mã lỗi:").upper().strip()
    if st.button("Xem kết quả"):
        if ma in KHO_DATA[loai][hang]:
            st.success(f"🛠 {KHO_DATA[loai][hang][ma]}")
        else: st.warning("Chưa có dữ liệu.")

# 2. CHẨN ĐOÁN AI (Chuyên sâu & Tổng hợp)
elif menu == "🧠 Chẩn đoán (AI)":
    st.subheader("🧠 CHẨN ĐOÁN THÔNG MINH")
    l_ai = st.selectbox("Loại máy:", list(KHO_DATA.keys()))
    tinh_trang = st.selectbox("Biểu hiện:", list(KHO_DATA[l_ai]["BIÊU_HIỆN_AI"].keys()))
    if st.button("Phân tích ngay"):
        st.info(f"🤖 **Tư vấn kỹ thuật:**\n\n{KHO_DATA[l_ai]['BIÊU_HIỆN_AI'][tinh_trang]}")

# 3. SƠ ĐỒ THÔNG MINH
elif menu == "📚 Sơ đồ thông minh":
    st.subheader("📚 TÌM SƠ ĐỒ PDF")
    mod = st.text_input("Model/Mã Board:")
    if st.button("Tìm link tải"):
        url = f"https://www.google.com/search?q={mod}+service+manual+pdf+schematic"
        st.markdown(f"### [👉 Bấm để tải sơ đồ]({url})")

# 4. GIA HẠN (ĐƯA LÊN TRANG CHÍNH CHO DỄ NHÌN)
elif menu == "💳 Gia hạn tự động":
    st.subheader("💳 GIA HẠN DỊCH VỤ")
    goi = st.radio("Chọn gói:", ["6 Tháng - 300k", "12 Tháng - 500k", "Vĩnh viễn - 1.5tr"])
    tien = "300000" if "6" in goi else ("500000" if "12" in goi else "1500000")
    nd = f"GIA HAN {st.session_state['ma_kich_hoat']}"
    qr = f"https://img.vietqr.io/image/ICB-104881077679-compact2.png?amount={tien}&addInfo={nd}&accountName=TRINH%20BA%20DUY"
    st.image(qr, use_container_width=True)
    st.success(f"Nội dung: {nd}")

# NÚT ĐĂNG XUẤT (Dưới cùng trang cho Mobile)
st.divider()
if st.button("Thoát hệ thống"):
    st.session_state['auth'] = None
    st.warning("Đã thoát. Hãy F5.")
