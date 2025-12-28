import streamlit as st
from datetime import datetime, timedelta

# 1. CẤU HÌNH HỆ THỐNG
st.set_page_config(page_title="Hệ thống Ba Duy v11.0", layout="wide")

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
    st.title("🔐 KỸ THUẬT BADUY@2025")
    st.info("💡 Mã dùng thử 3 ngày: DUY-FREE-3D")
    ma_nhap = st.text_input("Nhập mã kích hoạt:", type="password").strip()
    if st.button("Kích hoạt ngay"):
        if ma_nhap in DANH_SACH_KHACH_HANG:
            st.session_state['auth'] = DANH_SACH_KHACH_HANG[ma_nhap]
            st.session_state['ma_kich_hoat'] = ma_nhap
            st.success("✅ Thành công! Hãy làm mới (F5) trình duyệt.")
        else: st.error("Mã không đúng!")
    st.stop()

# --- KIỂM TRA HẠN (HIỂN THỊ TRÊN CÙNG CHO MOBILE) ---
user = st.session_state['auth']
is_expired = False

st.markdown(f"### 👤 Chào: {user['ten']}")

if user.get("loai") == "Trial":
    han_dung = user["ngay_dk"] + timedelta(days=3)
    con_lai = (han_dung - datetime.now()).days
    if con_lai < 0:
        is_expired = True
        st.error("🚫 HẾT HẠN DÙNG THỬ! VUI LÒNG GIA HẠN.")
    else:
        st.warning(f"⏳ TRẢI NGHIỆM CÒN {con_lai + 1} NGÀY")
else:
    st.success(f"✅ BẢN QUYỀN PRO: {user['han']}")

# --- MENU CHÍNH DẠNG THẢ XUỐNG (DỄ NHÌN TRÊN ĐIỆN THOẠI) ---
if is_expired:
    menu = "💳 Gia hạn dịch vụ"
else:
    menu = st.selectbox("CHỌN CHỨC NĂNG:", 
                       ["🔍 Tra mã lỗi", "🧠 Chẩn đoán AI", "📚 Sơ đồ PDF", "💳 Gia hạn dịch vụ"])

st.divider()

# --- KHO DỮ LIỆU TỔNG HỢP ---
KHO_DATA = {
    "Bếp Từ": {
        "Sunhouse": {"E0": "Lỗi nhận nồi. Kiểm tra trở 200k, tụ 5uF, 0.33uF.", "E1": "Quá nhiệt."},
        "BIÊU_HIỆN_AI": {
            "Bếp không nhận nồi": "Giải pháp: Kiểm tra tụ lọc nguồn 5uF, tụ cộng hưởng 0.33uF và các điện trở hồi tiếp cao (240k-820k).",
            "Mất nguồn hoàn toàn": "Giải pháp: Kiểm tra cầu chì, cầu điốt. Nếu đứt cầu chì thường do chập IGBT. Kiểm tra IC nguồn (TNY264, VIPer12A).",
            "Nhảy Aptomat": "Giải pháp: Chập IGBT công suất hoặc chập cầu điốt chỉnh lưu."
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
    if st.button("Tra cứu"):
        if ma in KHO_DATA[loai][hang]:
            st.success(f"🛠 {KHO_DATA[loai][hang][ma]}")
        else: st.warning("Dữ liệu đang cập nhật.")

# 2. CHẨN ĐOÁN AI
elif menu == "🧠 Chẩn đoán AI":
    st.subheader("🧠 CHẨN ĐOÁN THÔNG MINH")
    l_ai = st.selectbox("Loại máy:", list(KHO_DATA.keys()))
    tinh_trang = st.selectbox("Tình trạng:", list(KHO_DATA[l_ai]["BIÊU_HIỆN_AI"].keys()))
    if st.button("Phân tích ngay"):
        st.info(f"🤖 **Kết quả:**\n\n{KHO_DATA[l_ai]['BIÊU_HIỆN_AI'][tinh_trang]}")

# 3. SƠ ĐỒ PDF
elif menu == "📚 Sơ đồ PDF":
    st.subheader("📚 TÌM TÀI LIỆU KỸ THUẬT")
    mod = st.text_input("Model/Mã Board:")
    if st.button("Tìm link"):
        url = f"https://www.google.com/search?q={mod}+service+manual+pdf+schematic"
        st.markdown(f"### [👉 Bấm để tải sơ đồ {mod}]({url})")

# 4. GIA HẠN (DỄ NHÌN NHẤT TRÊN ĐIỆN THOẠI)
elif menu == "💳 Gia hạn dịch vụ":
    st.subheader("💳 NÂNG CẤP BẢN QUYỀN")
    goi = st.radio("Chọn gói gia hạn:", ["6 Tháng - 300k", "12 Tháng - 500k", "Vĩnh viễn - 1.5tr"])
    tien = "300000" if "6" in goi else ("500000" if "12" in goi else "1500000")
    nd = f"GIA HAN {st.session_state['ma_kich_hoat']}"
    qr = f"https://img.vietqr.io/image/ICB-104881077679-compact2.png?amount={tien}&addInfo={nd}&accountName=TRINH%20BA%20DUY"
    
    st.image(qr, use_container_width=True, caption="Quét mã để nâng cấp ngay")
    st.success(f"Nội dung: {nd} | Số tiền: {int(tien):,} VNĐ")

# NÚT ĐĂNG XUẤT AN TOÀN (KHÔNG DÙNG RERUN)
st.divider()
if st.button("Thoát hệ thống"):
    st.session_state['auth'] = None
    st.info("Đã đăng xuất thành công. Hãy làm mới (F5) trang để quay lại.")
