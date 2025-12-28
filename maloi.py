import streamlit as st
from datetime import datetime, timedelta

# 1. CẤU HÌNH HỆ THỐNG
st.set_page_config(page_title="Hệ thống Ba Duy v9.0", layout="wide")

# QUẢN LÝ NGƯỜI DÙNG (Cập nhật ngày kích hoạt để tính hạn dùng thử)
# Giả sử khách hàng mới kích hoạt ngày hôm nay
today = datetime.now()
DANH_SACH_KHACH_HANG = {
    "DUY-FREE-3D": {"ten": "Khách dùng thử", "loai": "Trial", "ngay_dk": today},
    "PRO-DUY-2025": {"ten": "Kỹ sư Ba Duy", "loai": "Pro", "han": "2026-01-05"},
}

if 'auth' not in st.session_state:
    st.session_state['auth'] = None

# --- MÀN HÌNH ĐĂNG NHẬP ---
if st.session_state['auth'] is None:
    st.title("🔐 HỆ THỐNG TRỢ LÝ KỸ THUẬT BADUY@2025")
    st.info("💡 Mẹo: Nhập 'FREE3D' để dùng thử miễn phí 3 ngày.")
    ma_nhap = st.text_input("Nhập mã kích hoạt:", type="password").strip()
    if st.button("Kích hoạt ngay"):
        if ma_nhap in DANH_SACH_KHACH_HANG:
            st.session_state['auth'] = DANH_SACH_KHACH_HANG[ma_nhap]
            st.session_state['ma_kich_hoat'] = ma_nhap
            st.success("✅ Thành công! Hãy Refresh (F5) trang để bắt đầu trải nghiệm.")
        else: st.error("Mã không đúng!")
    st.stop()

# --- KIỂM TRA HẠN DÙNG THỬ ---
user = st.session_state['auth']
is_expired = False
if user.get("loai") == "Trial":
    han_dung = user["ngay_dk"] + timedelta(days=3)
    con_lai = (han_dung - datetime.now()).days
    if con_lai < 0:
        is_expired = True
    else:
        thong_bao_han = f"Bản dùng thử còn {con_lai + 1} ngày!"
else:
    thong_bao_han = f"Bản quyền Pro: {user['han']}"

# --- GIAO DIỆN CHÍNH ---
st.sidebar.title(f"👤 {user['ten']}")
st.sidebar.warning(f"⏳ {thong_bao_han}")

if is_expired:
    st.error("🚫 Hết hạn dùng thử! Vui lòng vào mục 'Gia hạn' để tiếp tục sử dụng.")
    menu = st.sidebar.radio("CHỨC NĂNG", ["💳 Gia hạn tự động"])
else:
    menu = st.sidebar.radio("CHỨC NĂNG CHÍNH", 
        ["🔍 Tra mã lỗi", "🧠 Chẩn đoán (AI)", "📚 Sơ đồ thông minh", "💳 Gia hạn tự động"])

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

# 1. CHỨC NĂNG TRA MÃ LỖI
if menu == "🔍 Tra mã lỗi":
    st.header("🔍 TRA CỨU MÃ LỖI")
    col1, col2 = st.columns(2)
    with col1: loai = st.selectbox("Loại thiết bị", list(KHO_DATA.keys()))
    with col2: hang = st.selectbox("Hãng máy", [h for h in KHO_DATA[loai].keys() if h != "BIÊU_HIỆN_AI"])
    ma = st.text_input("Mã lỗi:").upper().strip()
    if st.button("Tra cứu"):
        if ma in KHO_DATA[loai][hang]:
            st.success(f"🛠 **Giải pháp:** {KHO_DATA[loai][hang][ma]}")
        else: st.warning("Dữ liệu đang được cập nhật.")

# 2. CHẨN ĐOÁN (AI) - PHÂN LOẠI CHUẨN
elif menu == "🧠 Chẩn đoán (AI)":
    st.header("🧠 CHẨN ĐOÁN AI THEO TỪNG LOẠI MÁY")
    l_ai = st.selectbox("Chọn loại máy:", list(KHO_DATA.keys()))
    list_bieu_hien = list(KHO_DATA[l_ai]["BIÊU_HIỆN_AI"].keys())
    tinh_trang = st.selectbox("Tình trạng thực tế:", list_bieu_hien)
    if st.button("Phân tích giải pháp"):
        st.info(f"🤖 **Kết quả chẩn đoán {l_ai}:**\n\n{KHO_DATA[l_ai]['BIÊU_HIỆN_AI'][tinh_trang]}")

# 3. SƠ ĐỒ THÔNG MINH
elif menu == "📚 Sơ đồ thông minh":
    st.header("📚 TÌM SƠ ĐỒ PDF")
    mod = st.text_input("Nhập Model/Mã Board:")
    if st.button("Tìm ngay"):
        url = f"https://www.google.com/search?q={mod}+service+manual+pdf+schematic"
        st.markdown(f"### [👉 Bấm để tải sơ đồ {mod}]({url})")

# 4. GIA HẠN (GIỮ NGUYÊN VIETINBANK)
elif menu == "💳 Gia hạn tự động":
    st.header("💳 NÂNG CẤP BẢN QUYỀN PRO")
    goi = st.radio("Gói gia hạn:", ["6 Tháng - 199k", "12 Tháng - 299k", "Vĩnh viễn - 499k"], horizontal=True)
    tien = "199000" if "6" in goi else ("299000" if "12" in goi else "499000")
    nd = f"GIA HAN {st.session_state['ma_kich_hoat']}"
    qr = f"https://img.vietqr.io/image/ICB-104881077679-compact2.png?amount={tien}&addInfo={nd}&accountName=TRINH%20BA%20DUY"
    st.image(qr, caption="Quét mã QR để nâng cấp")
    st.success(f"Số tiền: {int(tien):,} VNĐ | Nội dung: {nd}")

if st.sidebar.button("Đăng xuất"):
    st.session_state['auth'] = None
    st.warning("Đã đăng xuất. Hãy F5 trang.")
