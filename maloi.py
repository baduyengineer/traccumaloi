import streamlit as st
from datetime import datetime, timedelta

# 1. CẤU HÌNH HỆ THỐNG - KHÔNG ĐỔI
st.set_page_config(page_title="BADUY TECH 2025", layout="wide")

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
    st.title("🔐 HỆ THỐNG KỸ THUẬT BADUY")
    st.info("💡 Mã trải nghiệm 3 ngày: DUY-FREE-3D")
    ma_nhap = st.text_input("Mã kích hoạt:", type="password", key="login_key").strip()
    if st.button("VÀO HỆ THỐNG"):
        if ma_nhap in DANH_SACH_KHACH_HANG:
            st.session_state['auth'] = DANH_SACH_KHACH_HANG[ma_nhap]
            st.session_state['ma_kich_hoat'] = ma_nhap
            st.success("✅ Thành công! Hãy bấm F5 để bắt đầu.")
        else: st.error("Mã không đúng!")
    st.stop()

# --- HEADER THÔNG TIN (DỄ NHÌN TRÊN ĐIỆN THOẠI) ---
user = st.session_state['auth']
is_expired = False

st.markdown(f"### 👤 Chào: {user['ten']}")

if user.get("loai") == "Trial":
    han_dung = user["ngay_dk"] + timedelta(days=3)
    con_lai = (han_dung - datetime.now()).days
    if con_lai < 0:
        is_expired = True
        st.error("🚫 HẾT HẠN DÙNG THỬ! VUI LÒNG GIA HẠN ĐỂ DÙNG TIẾP.")
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
        "Sunhouse": {"E0": "Lỗi nhận nồi. Kiểm tra trở 200k, tụ 5uF, 0.33uF.", "E1": "Quá nhiệt cảm biến."},
        "BIÊU_HIỆN_AI": {
            "Bếp không nhận nồi": "Kỹ thuật: Kiểm tra tụ lọc 5uF, tụ cộng hưởng 0.33uF và dàn trở hồi tiếp (240k-820k).",
            "Mất nguồn hoàn toàn": "Kỹ thuật: Kiểm tra cầu chì, IC nguồn (TNY264), diode cầu. Nếu chập IGBT phải kiểm tra tầng driver.",
            "Nhảy Aptomat": "Kỹ thuật: Chập IGBT hoặc chập diode cầu chỉnh lưu."
        }
    },
    "Máy Giặt": {
        "Electrolux": {"E10": "Lỗi cấp nước.", "E20": "Lỗi thoát nước."},
        "BIÊU_HIỆN_AI": {
            "Rung lắc mạnh khi vắt": "Kỹ thuật: Kiểm tra giảm xóc (thụt), lò xo treo lồng và mặt bằng đặt máy.",
            "Máy không quay lồng": "Kỹ thuật: Kiểm tra chổi than motor, dây curoa hoặc lệnh từ bo công suất."
        }
    }
}

# XỬ LÝ CHỨC NĂNG
if menu == "🔍 Tra mã lỗi":
    st.subheader("🔍 TRA CỨU NHANH")
    l = st.selectbox("Thiết bị", list(KHO_DATA.keys()))
    h = st.selectbox("Hãng", [x for x in KHO_DATA[l].keys() if x != "BIÊU_HIỆN_AI"])
    ma = st.text_input("Nhập mã:").upper().strip()
    if st.button("Tra"):
        if ma in KHO_DATA[l][h]: st.success(f"🛠 {KHO_DATA[l][h][ma]}")
        else: st.warning("Dữ liệu chưa có.")

elif menu == "🧠 Chẩn đoán AI":
    st.subheader("🧠 CHẨN ĐOÁN THEO BỆNH")
    l_ai = st.selectbox("Máy cần sửa:", list(KHO_DATA.keys()))
    bh = st.selectbox("Biểu hiện:", list(KHO_DATA[l_ai]["BIÊU_HIỆN_AI"].keys()))
    if st.button("Phân tích"):
        st.info(f"🤖 **Tư vấn:** {KHO_DATA[l_ai]['BIÊU_HIỆN_AI'][bh]}")

elif menu == "📚 Sơ đồ PDF":
    st.subheader("📚 TÀI LIỆU KỸ THUẬT")
    mod = st.text_input("Nhập Model:")
    if st.button("Tìm"):
        st.markdown(f"### [👉 Bấm vào đây để tải sơ đồ {mod}](https://www.google.com/search?q={mod}+service+manual+pdf)")

elif menu == "💳 Gia hạn":
    st.subheader("💳 GIA HẠN DỊCH VỤ")
    goi = st.radio("Chọn gói:", ["6 Tháng - 300k", "12 Tháng - 500k", "Vĩnh viễn - 1.5tr"])
    tien = "300000" if "6" in goi else ("500000" if "12" in goi else "1500000")
    nd = f"GIA HAN {st.session_state['ma_kich_hoat']}"
    qr = f"https://img.vietqr.io/image/ICB-104881077679-compact2.png?amount={tien}&addInfo={nd}&accountName=TRINH%20BA%20DUY"
    st.image(qr, use_container_width=True)
    st.success(f"Nội dung: {nd}")

# NÚT THOÁT - ĐÃ SỬA LỖI DÒNG CUỐI
st.divider()
if st.button("Đăng xuất / Thoát"):
    st.session_state['auth'] = None
    st.rerun() # Lệnh này đặt ở đây là an toàn vì nó nằm trong điều kiện if
