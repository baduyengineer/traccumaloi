import streamlit as st
from datetime import datetime, timedelta

# 1. CẤU HÌNH HỆ THỐNG
st.set_page_config(page_title="BADUY TECH 2025", layout="wide")

# QUẢN LÝ NGƯỜI DÙNG
today = datetime.now()
DANH_SACH_KHACH_HANG = {
    "DUY-FREE-3D": {"ten": "Khách dùng thử", "loai": "Trial", "ngay_dk": today},
    "PRO-DUY-2025": {"ten": "Kỹ sư Ba Duy", "loai": "Pro", "han": "2026-01-05"},
}

if 'auth' not in st.session_state:
    st.session_state['auth'] = None

# --- CHỨC NĂNG ĐĂNG XUẤT (KHÔNG DÙNG RERUN) ---
def logout():
    st.session_state['auth'] = None

# --- MÀN HÌNH ĐĂNG NHẬP ---
if st.session_state['auth'] is None:
    st.title("🔐 HỆ THỐNG KỸ THUẬT BADUY")
    st.info("💡 Mã dùng thử 3 ngày: DUY-FREE-3D")
    ma_nhap = st.text_input("Nhập mã kích hoạt:", type="password").strip()
    if st.button("XÁC NHẬN VÀO HỆ THỐNG"):
        if ma_nhap in DANH_SACH_KHACH_HANG:
            st.session_state['auth'] = DANH_SACH_KHACH_HANG[ma_nhap]
            st.session_state['ma_kich_hoat'] = ma_nhap
            st.success("✅ Đã xác thực! Hãy nhấn một nút bất kỳ để bắt đầu.")
        else:
            st.error("Mã không đúng!")
    st.stop()

# --- HEADER THÔNG TIN (DỄ NHÌN TRÊN ĐIỆN THOẠI) ---
user = st.session_state['auth']
st.markdown(f"### 👤 Chào: {user['ten']}")

# Kiểm tra hạn dùng
is_expired = False
if user.get("loai") == "Trial":
    han_dung = user["ngay_dk"] + timedelta(days=3)
    con_lai = (han_dung - datetime.now()).days
    if con_lai < 0:
        is_expired = True
        st.error("🚫 HẾT HẠN DÙNG THỬ 3 NGÀY")
    else:
        st.warning(f"⏳ BẢN DÙNG THỬ: CÒN {con_lai + 1} NGÀY")
else:
    st.success(f"✅ BẢN QUYỀN PRO: Hạn dùng {user['han']}")

# --- MENU CHÍNH (TỐI ƯU MOBILE) ---
if is_expired:
    menu = "💳 Gia hạn"
else:
    menu = st.selectbox("DANH MỤC CHỨC NĂNG:", 
                       ["🔍 Tra mã lỗi", "🧠 Chẩn đoán AI", "📚 Sơ đồ PDF", "💳 Gia hạn"])

st.divider()

# --- KHO DỮ LIỆU TỔNG HỢP ---
KHO_DATA = {
    "Bếp Từ": {
        "Sunhouse": {"E0": "Lỗi nhận nồi. Kiểm tra trở 200k, tụ 5uF, 0.33uF.", "E1": "Lỗi quá nhiệt."},
        "BIÊU_HIỆN_AI": {
            "Bếp không nhận nồi": "Gợi ý: Kiểm tra tụ lọc 5uF, tụ cộng hưởng 0.33uF và dàn trở hồi tiếp cao (240k-820k).",
            "Mất nguồn hoàn toàn": "Gợi ý: Kiểm tra cầu chì, IC nguồn (TNY264), diode cầu. Nếu chập IGBT phải kiểm tra tầng driver.",
            "Nhảy Aptomat": "Gợi ý: Chập IGBT công suất hoặc chập diode cầu chỉnh lưu."
        }
    },
    "Máy Giặt": {
        "Electrolux": {"E10": "Lỗi cấp nước.", "E20": "Lỗi xả nước."},
        "BIÊU_HIỆN_AI": {
            "Rung lắc mạnh khi vắt": "Gợi ý: Kiểm tra giảm xóc, lò xo treo lồng và độ cân bằng mặt sàn.",
            "Máy không quay lồng": "Gợi ý: Kiểm tra chổi than motor hoặc dây curoa."
        }
    }
}

# 1. TRA MÃ LỖI
if menu == "🔍 Tra mã lỗi":
    st.subheader("🔍 TRA CỨU NHANH")
    l = st.selectbox("Thiết bị", list(KHO_DATA.keys()))
    h = st.selectbox("Hãng", [x for x in KHO_DATA[l].keys() if x != "BIÊU_HIỆN_AI"])
    ma = st.text_input("Nhập mã lỗi:").upper().strip()
    if st.button("Tìm giải pháp"):
        if ma in KHO_DATA[l][h]: st.success(f"🛠 {KHO_DATA[l][h][ma]}")
        else: st.warning("Dữ liệu đang cập nhật.")

# 2. CHẨN ĐOÁN AI
elif menu == "🧠 Chẩn đoán AI":
    st.subheader("🧠 CHẨN ĐOÁN THÔNG MINH")
    l_ai = st.selectbox("Loại máy:", list(KHO_DATA.keys()))
    bh = st.selectbox("Tình trạng thực tế:", list(KHO_DATA[l_ai]["BIÊU_HIỆN_AI"].keys()))
    if st.button("Phân tích AI"):
        st.info(f"🤖 **Tư vấn:** {KHO_DATA[l_ai]['BIÊU_HIỆN_AI'][bh]}")

# 3. SƠ ĐỒ PDF
elif menu == "📚 Sơ đồ PDF":
    st.subheader("📚 TÌM TÀI LIỆU")
    mod = st.text_input("Nhập Model/Board:")
    if st.button("Lấy link"):
        st.markdown(f"### [👉 Tải sơ đồ {mod} tại đây](https://www.google.com/search?q={mod}+service+manual+pdf)")

# 4. GIA HẠN (Mã QR to rõ cho điện thoại)
elif menu == "💳 Gia hạn":
    st.subheader("💳 GIA HẠN DỊCH VỤ")
    goi = st.radio("Chọn gói:", ["6 Tháng - 300k", "12 Tháng - 500k", "Vĩnh viễn - 1.5tr"])
    tien = "300000" if "6" in goi else ("500000" if "12" in goi else "1500000")
    nd = f"GIA HAN {st.session_state.get('ma_kich_hoat', 'PRO')}"
    qr = f"https://img.vietqr.io/image/ICB-104881077679-compact2.png?amount={tien}&addInfo={nd}&accountName=TRINH%20BA%20DUY"
    st.image(qr, use_container_width=True)
    st.success(f"Nội dung: {nd} | Số tiền: {int(tien):,} VNĐ")

# NÚT ĐĂNG XUẤT AN TOÀN - KHÔNG CÓ LỆNH LỖI Ở ĐÂY
st.divider()
st.button("Đăng xuất / Thoát hệ thống", on_click=logout)
