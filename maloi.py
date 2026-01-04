import streamlit as st

# 1. CẤU HÌNH HỆ THỐNG
st.set_page_config(page_title="BA DUY TECH PRO 2026", layout="centered")

if 'auth' not in st.session_state: st.session_state['auth'] = None
if 'page' not in st.session_state: st.session_state['page'] = "HOME"
if 'user_db' not in st.session_state: st.session_state['user_db'] = []

# DANH SÁCH TÀI KHOẢN
USERS = {
    "PRO-DUY-2025": {"ten": "Kỹ sư Ba Duy", "loai": "Vĩnh viễn", "han": "Vô hạn"},
    "DUY-FREE": {"ten": "Khách dùng thử", "loai": "Free", "han": "3 ngày"}
}

# --- MÀN HÌNH ĐĂNG NHẬP ---
if st.session_state['auth'] is None:
    st.title("🔐 HỆ THỐNG TRỢ LÝ KỸ THUẬT BA DUY")
    ma = st.text_input("Nhập mã kích hoạt (Vd: DUY-FREE):", type="password").strip()
    if st.button("XÁC NHẬN VÀO", use_container_width=True):
        if ma in USERS:
            st.session_state['auth'] = USERS[ma]
            st.rerun()
        else: st.error("Mã không đúng! Vui lòng liên hệ Admin để mua gói.")
    st.stop()

# --- DỮ LIỆU TỔNG HỢP CẬP NHẬT TỪ FILE ---
DATA_FULL = {
    "Điều Hòa": {
        "Panasonic": {
            "00H": "Bình thường, không bị lỗi ",
            "11H": "Lỗi đường dữ liệu giữa khối trong và ngoài ",
            "12H": "Khối trong và ngoài khác công suất ",
            "14H": "Lỗi cảm biến nhiệt độ phòng ",
            "15H": "Lỗi cảm biến nhiệt độ máy nén ",
            "16H": "Dòng điện tải máy nén quá thấp ",
            "19H": "Lỗi quạt dàn lạnh ",
            "23H": "Lỗi cảm biến nhiệt độ dàn lạnh ",
            "25H": "Mạch E-on lỗi ",
            "27H": "Lỗi cảm biến nhiệt độ ngoài trời ",
            "28H": "Lỗi cảm biến giàn nóng (H28). HD: Kiểm tra jack cắm; đo điện trở (3KΩ ở 30°C); hơ nóng cảm biến nếu điện trở giảm là tốt, lỗi do board ",
            "30H": "Lỗi cảm biến nhiệt độ ống ra máy nén (CU-S18xx) ",
            "98H": "Nhiệt độ giàn trong quá cao (Sưởi ấm) ",
            "99H": "Nhiệt độ dàn lạnh giảm thấp (Đóng băng) ",
            "11F": "Lỗi chuyển đổi chế độ Lạnh/Sưởi ",
            "90F": "Lỗi trên mạch PFC ra máy nén ",
            "91F": "Dòng tải máy nén quá thấp ",
            "93F": "Lỗi tốc độ quay máy nén ",
            "95F": "Nhiệt độ dàn nóng quá cao ",
            "96F": "Quá nhiệt bộ transistor công suất máy nén (IPM) ",
            "97F": "Nhiệt độ máy nén quá cao ",
            "98F": "Dòng tải máy nén quá cao ",
            "99F": "Xung DC ra máy nén quá cao ",
            "H11": "Lỗi truyền tín hiệu giữa khối trong và ngoài nhà ",
            "H14": "Lỗi cảm biến nhiệt độ hút khối trong nhà ",
            "H15": "Lỗi cảm biến lưu lượng/nhiệt độ máy nén ",
            "H19": "Động cơ quạt trong nhà bị kẹt/hỏng ",
            "H24": "Cảm biến trao đổi nhiệt trong nhà bất thường ",
            "H25": "Lỗi bộ lọc không khí ",
            "H59": "Lỗi cảm biến hồng ngoại ",
            "H67": "Lỗi chức năng Nanoe ",
            "H70": "Lỗi cảm biến bức xạ mặt trời ",
            "H96": "Van 2, 3 ngã bị hở ",
            "H97": "Động cơ quạt ngoài trời bị khóa/kẹt ",
            "H98": "Lỗi bảo vệ quá nhiệt dưới áp suất cao (nghẹt/rò gas) ",
            "H99": "Lỗi bảo vệ làm lạnh (nghẹt/rò gas) ",
            "F11": "Bộ chuyển đổi hoạt động không bình thường ",
            "F13": "Mất kết nối/Lỗi bo khối làm ẩm trong nhà ",
            "F14": "Điện áp bất thường khối trong nhà ",
            "F16": "Lỗi chuyển đổi chế độ làm mát/tạo ẩm ",
            "F17": "Dàn lạnh lạnh bất thường ",
            "F18": "Lỗi mạch làm khô ",
            "F19": "Môi chất lạnh làm nóng ",
            "F83": "Nhiệt độ làm lạnh/nóng vượt mức cho phép ",
            "F90": "Lỗi kết nối bảng điều khiển PFC khối ngoài ",
            "F91": "Rò rỉ môi chất lạnh, chu kỳ kém ",
            "F93": "Máy nén hoạt động bất thường ",
            "F95": "Lỗi chức năng hoạt động và hút ẩm ",
            "F97": "Nhiệt độ máy nén cao, máy tự tắt ",
            "F99": "Dòng DC cao bất thường ",
            "E02": "Lỗi mạch bơm thoát nước trong nhà ",
            "E03": "Lỗi cảm biến nhiệt độ phòng trong nhà ",
            "E05": "Lỗi bộ điều khiển từ xa ",
            "E06": "Lỗi truyền tín hiệu trong và ngoài nhà ",
            "E09": "Lỗi moto quạt dàn lạnh ",
            "E10": "Lỗi cảm biến bức xạ trong nhà ",
            "E11": "Lỗi bo mạch tạo ẩm trong nhà ",
            "E13": "Lỗi quá dòng bảo vệ/mất pha/máy nén ",
            "E15": "Áp suất cao bất thường, tắc bộ trao đổi nhiệt ",
            "E16": "Lỗi chống mất pha/nguồn/bo cục nóng ",
            "E17": "Lỗi cảm biến không khí ngoài bảng mạch nóng ",
            "E18": "Lỗi cảm biến nhiệt đường ống bo khối ngoài "
        },
        "Daikin": {
            "C1": "Lỗi bo dàn lạnh hoặc bo quạt ",
            "C3": "Lỗi hệ thống cảm biến nước xả ",
            "C4": "Lỗi nhiệt điện trở ống lỏng/lỏng kết nối ",
            "C5": "Lỗi nhiệt điện trở ống hơi/lỏng kết nối ",
            "C6": "Lỗi cảm biến moto quạt, quá tải ",
            "C7": "Lỗi moto đảo gió/vật liệu kín dày/hư cuộn dây ",
            "C8": "Cảm biến dàn lạnh quá dòng đầu vào ",
            "C9": "Lỗi nhiệt điện trở gió hồi/lỏng kết nối ",
            "CA": "Lỗi nhiệt điện trở gió thổi/lỏng kết nối ",
            "CC": "Lỗi cảm biến độ ẩm ",
            "CE": "Lỗi cảm biến tản nhiệt dàn lạnh ",
            "CF": "Lỗi công tắc cao áp dàn lạnh ",
            "CH": "Cảm biến dàn lạnh bị dơ ",
            "CJ": "Lỗi nhiệt điện trở remote/đứt dây ",
            "E0": "Thiết bị bảo vệ dàn nóng tác động (Cao áp, quá tải, đứt dây) ",
            "E1": "Lỗi bo mạch dàn nóng ",
            "E2": "Lỗi bo mạch bộ BP unit ",
            "E3": "Lỗi cao áp/dư gas/mất điện tức thời ",
            "E4": "Lỗi hạ áp/thiếu gas/hỏng cảm biến hạ áp ",
            "E5": "Máy nén Inverter quá tải/Lỗi van 4 ngả/bo nóng ",
            "E6": "Lỗi máy nén hoặc khởi động từ ",
            "E7": "Lỗi moto quạt dàn nóng hoặc bo quạt ",
            "E8": "Quá dòng đầu vào dàn nóng/Lỗi block/bo mạch ",
            "E9": "Lỗi van tiết lưu điện tử/lỏng kết nối ",
            "EA": "Lỗi van 4 ngả/nhiệt điện trở/thân van ",
            "F3": "Nhiệt độ ống đẩy bất thường/thiếu gas ",
            "U0": "Thiếu gas/nghẹt ống dẫn/lỏng cảm biến ",
            "U1": "Ngược pha/lỗi nguồn cấp ",
            "U2": "Lỗi nguồn điện hoặc mất điện tức thời ",
            "U4": "Lỗi tín hiệu truyền thông giữa nóng/lạnh hoặc bộ BS ",
            "U5": "Lỗi điều khiển từ xa (RC) ",
            "UA": "Dàn nóng và lạnh không tương thích "
        },
        "LG": {
            "CH01": "Hỏng cảm biến giàn lạnh ",
            "CH02": "Hỏng cảm biến giàn lạnh ",
            "CH05": "Lỗi kết nối giàn nóng và giàn lạnh inverter ",
            "CH06": "Hỏng cảm biến đường đi giàn nóng ",
            "CH09": "Lỗi bo mạch giàn nóng ",
            "CH10": "Quạt giàn lạnh inverter lỗi ",
            "CH21": "Lỗi IC Công Suất ",
            "CH22": "Cao dòng/cao áp trên cuộn seo, board ",
            "CH23": "Điện áp quá thấp ",
            "CH26": "Hỏng máy nén inverter ",
            "CH27": "Lỗi quá tải dàn nóng/board inverter ",
            "CH29": "Pha máy nén inverter lỗi ",
            "CH32": "Nhiệt độ cao đường đẩy máy nén ",
            "CH33": "Quá tải máy nén inverter ",
            "CH41": "Cảm biến máy nén 200k lỗi ",
            "CH44": "Hỏng cảm biến gió giàn nóng 10k ",
            "CH45": "Hỏng cảm biến gió giàn nóng 5k ",
            "CH46": "Cảm biến đường về máy nén lỗi ",
            "CH53": "Lỗi liên lạc giữa nóng và lạnh ",
            "CH61": "Giàn nóng không giải nhiệt được ",
            "CH65": "Hỏng IC nguồn đuôi nóng inverter "
        }
    },
    "Máy Giặt": {
        "Electrolux": {
            "E10": "Lỗi cấp nước. HD: Vệ sinh van cấp, kiểm tra áp lực.",
            "E20": "Lỗi thoát nước. HD: Kiểm tra bơm xả, ống thoát.",
            "E40": "Lỗi cửa. HD: Thay khóa cửa, kiểm tra bo."
        },
        "LG": {
            "IE": "Không vào nước. HD: Kiểm tra van cấp.",
            "OE": "Không thoát nước. HD: Kiểm tra bơm xả."
        }
    },
    "Bếp Từ": {
        "Sunhouse": {"E0": "Không nhận nồi.", "E1": "Quá nhiệt cảm biến."},
        "Kangaroo": {"E1": "Lỗi cảm biến kính.", "E2": "Quá nhiệt IGBT."}
    }
}

# --- GIAO DIỆN CHÍNH ---
user = st.session_state['auth']
st.success(f"👤 {user['ten']} | 📦 Gói: {user['loai']} | 📅 Hạn: {user['han']}")

# MENU NÚT BẤM LỚN
c1, c2 = st.columns(2)
with c1:
    if st.button("🔍 TRA MÃ & HƯỚNG DẪN", use_container_width=True): st.session_state.page = "TRA"
with c2:
    if st.button("🧠 CHẨN ĐOÁN AI", use_container_width=True): st.session_state.page = "AI"

c3, c4 = st.columns(2)
with c3:
    if st.button("➕ THÊM MÃ MỚI", use_container_width=True): st.session_state.page = "THEM"
with c4:
    if st.button("💳 GIA HẠN / MUA GÓI", use_container_width=True): st.session_state.page = "GIA"

# --- XỬ LÝ CHỨC NĂNG ---
if st.session_state.page == "TRA":
    st.divider()
    st.subheader("🔍 TRA CỨU & KHẮC PHỤC")
    loai = st.selectbox("Chọn thiết bị:", list(DATA_FULL.keys()))
    hang = st.selectbox(f"Chọn hãng {loai}:", list(DATA_FULL[loai].keys()))
    ma = st.text_input("Nhập mã lỗi (Vd: H11, CH21, U4...):").upper().strip()
    if st.button("TÌM KIẾM", use_container_width=True):
        if ma in DATA_FULL[loai][hang]:
            st.info(f"🛠 **{hang} {ma}:**\n\n{DATA_FULL[loai][hang][ma]}")
        else:
            found = [x for x in st.session_state.user_db if x['ma']==ma and x['hang']==hang]
            if found: st.success(f"📌 **Kinh nghiệm cá nhân:**\n\n{found[0]['hd']}")
            else: st.warning("Chưa có mã này. Hãy dùng AI hoặc tự thêm mã mới!")

elif st.session_state.page == "AI":
    st.divider()
    st.subheader("🧠 CHẨN ĐOÁN AI CHUYÊN SÂU")
    l_ai = st.selectbox("Loại máy:", list(DATA_FULL.keys()), key="ai_l")
    h_ai = st.selectbox("Hãng máy:", list(DATA_FULL[l_ai].keys()), key="ai_h")
    benh = st.text_area("Mô tả bệnh (Vd: Quạt không quay, có tiếng kêu lạ...):")
    if st.button("AI PHÂN TÍCH", use_container_width=True):
        if "nguồn" in benh.lower(): st.error(f"🤖 AI {h_ai}: Kiểm tra Cầu chì, IC nguồn, Biến áp xung.")
        elif "lạnh" in benh.lower(): st.warning(f"🤖 AI {h_ai}: Kiểm tra Gas, Sensor, Block và Tụ ngậm.")
        else: st.info(f"🤖 AI {h_ai}: Kiểm tra lệnh từ Bo mạch điều khiển chính.")

elif st.session_state.page == "THEM":
    st.divider()
    st.subheader("➕ LÀM GIÀU DỮ LIỆU KỸ THUẬT")
    t_loai = st.selectbox("Thiết bị:", ["Điều Hòa", "Máy Giặt", "Bếp Từ", "Tủ Lạnh"])
    t_hang = st.text_input("Hãng máy:")
    t_ma = st.text_input("Mã lỗi:").upper().strip()
    t_hd = st.text_area("Hướng dẫn sửa thực tế (Kinh nghiệm thợ):")
    if st.button("LƯU VÀO KHO DỮ LIỆU", use_container_width=True):
        st.session_state.user_db.append({'loai': t_loai, 'hang': t_hang, 'ma': t_ma, 'hd': t_hd})
        st.success("✅ Đã lưu thành công vào kho dữ liệu của bạn!")

elif st.session_state.page == "GIA":
    st.divider()
    st.subheader("💳 CHỌN GÓI BẢN QUYỀN PRO")
    goi = st.radio("Chọn gói muốn mua:", ["6 Tháng (199k)", "12 Tháng (299k)", "Vĩnh Viễn (499k)"])
    tien = "199000" if "6" in goi else "299000" if "12" in goi else "499000"
    st.image(f"https://img.vietqr.io/image/ICB-104881077679-compact2.png?amount={tien}&addInfo=GIAHAN%20{goi}")
    st.success(f"Dòng máy nhận tiền: Ngân hàng Công Thương (VietinBank)")

# NÚT ĐĂNG XUẤT
st.divider()
if st.button("🚪 Đăng xuất", use_container_width=True):
    st.session_state.auth = None
    st.rerun()

st.caption("BA DUY TECH v35.0 - NỀN TẢNG KỸ THUẬT SỐ 1 VIỆT NAM")
