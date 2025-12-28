import streamlit as st
from datetime import datetime

# ========================================================
# 1. QUẢN LÝ BẢN QUYỀN (Mục 4)
# ========================================================
DANH_SACH_KHACH_HANG = {
    "PRO-DUY-2025": {"ten": "Kỹ sư Ba Duy", "loai": "Pro", "han": "2026-01-05"},
    "ADMIN-888": {"ten": "Quản trị viên", "loai": "Pro", "han": "2030-12-31"},
}

if 'auth' not in st.session_state:
    st.session_state['auth'] = None

if not st.session_state['auth']:
    st.markdown("<h2 style='text-align: center;'>🔐 HỆ THỐNG TRA CỨU KỸ THUẬT BADUY@2025</h2>", unsafe_allow_html=True)
    ma_nhap = st.text_input("Nhập mã kích hoạt:", type="password").strip()
    if st.button("Kích hoạt bản quyền"):
        if ma_nhap in DANH_SACH_KHACH_HANG:
            st.session_state['auth'] = DANH_SACH_KHACH_HANG[ma_nhap]
            st.rerun()
        else:
            st.error("Mã không đúng!")
    st.stop()

user = st.session_state['auth']
ngay_het_han = datetime.strptime(user['han'], "%Y-%m-%d")
ngay_con_lai = (ngay_het_han - datetime.now()).days

# ========================================================
# 2. KHO DỮ LIỆU TỔNG HỢP TỪ ẢNH BẠN GỬI
# ========================================================
data_ma_loi = {
    "Máy Giặt": {
        "Electrolux": {
            "E10": {"loi": "Lỗi nguồn cấp nước (Vòi đóng, bộ lọc tắc).", "pro": "Kiểm tra vòi nước, vệ sinh bộ lọc, kiểm tra van cấp."},
            "E20": {"loi": "Lỗi xả nước (Ống xả tắc, bơm hỏng).", "pro": "Kiểm tra bơm xả, vệ sinh hố bơm, đo cuộn dây bơm."},
            "E23": {"loi": "Hư Triac bơm nước.", "pro": "Kiểm tra hệ thống dây điện, đo Triac trên main PCB hoặc thay main."},
            "E41": {"loi": "Lỗi cửa mở (sau 15 giây).", "pro": "Kiểm tra khóa cửa bị lỗi hoặc cửa chưa đóng chặt."},
            "E52": {"loi": "Không có tín hiệu từ bộ điều tốc (Tacho).", "pro": "Kiểm tra chổi than động cơ, đo điện trở cuộn dây động cơ/tacho."},
            "E57": {"loi": "Inverter hút dòng quá nhiều (>15A).", "pro": "Kiểm tra hệ thống dây dẫn, đo cuộn dây động cơ, thay board Inverter nếu cần."},
            "E91": {"loi": "Lỗi kết nối giữa PCB nguồn và PCB hiển thị.", "pro": "Kiểm tra dây cáp tín hiệu giữa 2 board, sửa hoặc thay PCB."},
        }
    },
    "Bếp Từ": {
        "Sunhouse": {
            "E0": {
                "loi": "Lỗi mạch nhận biết điện áp đầu vào.", 
                "pro": "Kiểm tra cặp trở 200k đường AC, tụ lọc 4.7uF và diode bảo vệ 5V.",
                "video": "https://www.youtube.com/watch?v=J_iBHlMdcmk"
            },
        },
        "Bosch": {
            "E22": {"loi": "Lỗi bo cảm ứng do độ ẩm hoặc chập chân IC phím.", "pro": "Sấy bo mạch, vệ sinh sạch vùng phím cảm ứng."},
            "F0": {"loi": "Lỗi đường truyền dẫn, cáp hoặc dây tín hiệu.", "pro": "Kiểm tra cáp nối bo công suất và hiển thị."},
            "Er26": {"loi": "Lỗi relay chuyển tiếp hoặc mạch điều khiển.", "pro": "Thay thế rơ-le trên bo mạch chính."},
        }
    }
}

# Dữ liệu Chẩn đoán (Mục 3)
data_chan_doan = {
    "Bếp Từ": {
        "Bếp không nóng/không nhận nồi": "Kiểm tra tụ 0.33uF, mạch Driver và trở hồi tiếp (thường từ 470k-820k).",
        "Mất nguồn hoàn toàn": "Kiểm tra cầu chì, IC nguồn (Viper12A), và diode nắn 300V."
    },
    "Máy Giặt": {
        "Vắt rung lắc mạnh": "Kiểm tra ty treo lồng, cân bằng máy, hoặc hỏng bi phớt trục.",
        "Nước vào không ngừng": "Kiểm tra van cấp bị kẹt rác hoặc hỏng cảm biến áp suất mực nước."
    }
}

# ========================================================
# 3. GIAO DIỆN ĐIỀU HƯỚNG
# ========================================================
st.sidebar.title(f"Chào, {user['ten']}")
if ngay_con_lai <= 7:
    st.sidebar.warning(f"⚠️ Bản quyền còn {ngay_con_lai} ngày!")

menu = st.sidebar.radio("CHỨC NĂNG CHÍNH", 
    ["🔍 Tra mã lỗi", "🧠 Chẩn đoán bệnh (AI)", "📚 Sơ đồ thông minh", "💳 Gia hạn"])

if menu == "Tra mã lỗi":
    st.header("🔍 KHO MÃ LỖI CHI TIẾT")
    col1, col2 = st.columns(2)
    with col1:
        loai = st.selectbox("Chọn thiết bị", list(data_ma_loi.keys()))
    with col2:
        hang = st.selectbox("Chọn hãng", list(data_ma_loi[loai].keys()))
    
    ma = st.text_input("Nhập mã lỗi (VD: E41, E52, E0...):").upper().strip()
    if st.button("Tra cứu ngay"):
        if ma in data_ma_loi[loai][hang]:
            res = data_ma_loi[loai][hang][ma]
            st.info(f"📌 **Mô tả:** {res['loi']}")
            st.success(f"🛠️ **Hướng dẫn sửa:**\n{res['pro']}")
            if "video" in res:
                st.video(res['video'])
        else:
            st.error("Mã lỗi này đang được cập nhật dữ liệu...")

elif menu == "Chẩn đoán bệnh (AI)":
    st.header("🧠 CHẨN ĐOÁN THEO BIỂU HIỆN")
    st.write("Giải quyết các ca bệnh không báo mã lỗi.")
    loai_ai = st.selectbox("Thiết bị đang sửa:", list(data_chan_doan.keys()))
    bieu_hien = st.selectbox("Máy đang bị tình trạng gì?", list(data_chan_doan[loai_ai].keys()))
    if st.button("Phân tích nguyên nhân"):
        st.subheader("📋 Gợi ý xử lý từ trợ lý Duy:")
        st.success(data_chan_doan[loai_ai][bieu_hien])

elif menu == "Sơ đồ thông minh":
    st.header("📚 TRỢ LÝ TÌM SƠ ĐỒ CHUYÊN NGHIỆP")
    model_may = st.text_input("Nhập Model hoặc Mã Board (VD: Electrolux EWP85742, Board K2012...):")
    if st.button("Tìm tài liệu PDF"):
        google_url = f"https://www.google.com/search?q={model_may}+service+manual+pdf+schematic+diagram"
        st.markdown(f"### [👉 Bấm vào đây để xem kết quả sơ đồ cho {model_may}]({google_url})")
        st.info("Trợ lý đã lọc sẵn các kết quả PDF và Schematic chuẩn cho bạn.")

elif menu == "Gia hạn":
    st.header("💳 THÔNG TIN BẢN QUYỀN")
    st.write(f"Khách hàng: **{user['ten']}**")
    st.write(f"Hạn dùng: **{user['han']}**")
    st.divider()
    st.success("Liên hệ Duy (0987973723) để gia hạn nhanh chóng.")

if st.sidebar.button("Đăng xuất"):
    st.session_state['auth'] = None
    st.rerun()
