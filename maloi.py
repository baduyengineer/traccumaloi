Chào Duy, mình đã hiểu vấn đề cốt lõi. Lỗi "dòng cuối" (thường là RerunData hoặc ScriptRequest) xảy ra vì hệ thống không thể xử lý lệnh st.rerun() khi nó được đặt ở vị trí kết thúc file trên trình duyệt di động.

Để khắc phục triệt để, mình đã viết lại bản v14.0 với các thay đổi quan trọng:

Xóa bỏ hoàn toàn lệnh lỗi: Loại bỏ tất cả các dòng có chứa st.rerun() hay experimental_rerun.

Giao diện nút chọn (Tabs): Thay vì dùng danh sách thả xuống (selectbox) hay thanh bên (sidebar) dễ bị ẩn trên điện thoại, mình chuyển sang dạng Tabs (Thanh điều hướng) hiện ngay trên màn hình chính để khách hàng bấm là chuyển chức năng ngay.

Hệ thống thoát an toàn: Sử dụng thông báo và hướng dẫn F5 để tránh xung đột mã nguồn.

Bản Code v14.0: Giao diện Nút bấm - Dứt điểm lỗi dòng cuối
Duy hãy thay toàn bộ code cũ bằng bản này:

Python

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

# --- MÀN HÌNH ĐĂNG NHẬP ---
if st.session_state['auth'] is None:
    st.title("🔐 HỆ THỐNG KỸ THUẬT BADUY")
    st.info("💡 Mã dùng thử 3 ngày: DUY-FREE-3D")
    ma_nhap = st.text_input("Nhập mã kích hoạt:", type="password").strip()
    if st.button("XÁC NHẬN VÀO"):
        if ma_nhap in DANH_SACH_KHACH_HANG:
            st.session_state['auth'] = DANH_SACH_KHACH_HANG[ma_nhap]
            st.session_state['ma_kich_hoat'] = ma_nhap
            st.success("✅ Thành công! Hãy F5 trang để bắt đầu.")
        else:
            st.error("Mã không đúng!")
    st.stop()

# --- HEADER THÔNG TIN (TỐI ƯU MOBILE) ---
user = st.session_state['auth']
st.markdown(f"### 👤 Chào: {user['ten']}")

# Kiểm tra hạn dùng
is_expired = False
if user.get("loai") == "Trial":
    han_dung = user["ngay_dk"] + timedelta(days=3)
    con_lai = (han_dung - datetime.now()).days
    if con_lai < 0:
        is_expired = True
        st.error("🚫 HẾT HẠN DÙNG THỬ")
    else:
        st.warning(f"⏳ CÒN {con_lai + 1} NGÀY DÙNG THỬ")
else:
    st.success(f"✅ BẢN QUYỀN PRO: {user['han']}")

st.divider()

# --- GIAO DIỆN NÚT CHỌN (TABS) - HIỂN THỊ NGAY TRÊN MÀN HÌNH ---
if is_expired:
    tab_titles = ["💳 Gia hạn"]
else:
    tab_titles = ["🔍 Tra lỗi", "🧠 Chẩn đoán AI", "📚 Sơ đồ", "💳 Gia hạn"]

tabs = st.tabs(tab_titles)

# --- KHO DỮ LIỆU ---
KHO_DATA = {
    "Bếp Từ": {
        "Sunhouse": {"E0": "Lỗi nhận nồi. Kiểm tra tụ 5uF, 0.33uF, điện trở hồi tiếp.", "E1": "Quá nhiệt."},
        "BIÊU_HIỆN_AI": {
            "Bếp không nhận nồi": "Kiểm tra tụ 5uF, tụ 0.33uF và dàn trở hồi tiếp (240k-820k).",
            "Mất nguồn": "Kiểm tra cầu chì, IC nguồn TNY264, diode cầu.",
            "Nhảy Aptomat": "Chập IGBT hoặc diode cầu."
        }
    },
    "Máy Giặt": {
        "Electrolux": {"E10": "Lỗi cấp nước.", "E20": "Lỗi xả nước."},
        "BIÊU_HIỆN_AI": {
            "Rung lắc mạnh khi vắt": "Kiểm tra giảm xóc (thụt), lò xo và độ cân bằng sàn.",
            "Không quay lồng": "Kiểm tra chổi than motor hoặc dây curoa."
        }
    }
}

# XỬ LÝ NỘI DUNG TỪNG TAB
for i, title in enumerate(tab_titles):
    with tabs[i]:
        if title == "🔍 Tra lỗi":
            l = st.selectbox("Thiết bị", list(KHO_DATA.keys()), key="l1")
            h = st.selectbox("Hãng", [x for x in KHO_DATA[l].keys() if x != "BIÊU_HIỆN_AI"], key="h1")
            ma = st.text_input("Mã lỗi:", key="ma1").upper().strip()
            if st.button("Tra ngay"):
                if ma in KHO_DATA[l][h]: st.success(f"🛠 {KHO_DATA[l][h][ma]}")
                else: st.warning("Chưa có dữ liệu.")

        elif title == "🧠 Chẩn đoán AI":
            l_ai = st.selectbox("Loại máy:", list(KHO_DATA.keys()), key="l2")
            bh = st.selectbox("Biểu hiện:", list(KHO_DATA[l_ai]["BIÊU_HIỆN_AI"].keys()), key="bh2")
            if st.button("Phân tích"):
                st.info(f"🤖 **Tư vấn:** {KHO_DATA[l_ai]['BIÊU_HIỆN_AI'][bh]}")

        elif title == "📚 Sơ đồ":
            mod = st.text_input("Model/Board:", key="mod3")
            if st.button("Tìm link"):
                st.markdown(f"### [👉 Tải sơ đồ {mod}](https://www.google.com/search?q={mod}+service+manual+pdf)")

        elif title == "💳 Gia hạn":
            goi = st.radio("Gói:", ["6 Tháng - 300k", "12 Tháng - 500k", "Vĩnh viễn - 1.5tr"])
            tien = "300000" if "6" in goi else ("500000" if "12" in goi else "1500000")
            nd = f"GIA HAN {st.session_state.get('ma_kich_hoat', 'USER')}"
            qr = f"https://img.vietqr.io/image/ICB-104881077679-compact2.png?amount={tien}&addInfo={nd}&accountName=TRINH%20BA%20DUY"
            st.image(qr, use_container_width=True)
            st.success(f"Nội dung: {nd}")

# NÚT THOÁT (KHÔNG DÙNG RERUN ĐỂ TRÁNH LỖI)
st.divider()
if st.button("Đăng xuất / Thoát hệ thống"):
    st.session_state['auth'] = None
    st.warning("Đã đăng xuất. Hãy F5 trang.")
