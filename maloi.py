# Thiết lập giao diện
st.set_page_config(page_title="Tra cứu mã lỗi - Baduy@2025", layout="centered")
# Tiêu đề chính
st.markdown("<h1 style='text-align: center;'>🛠️ KHO MÃ LỖI ĐIỆN TỬ VIỆT NAM</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Design by baduy@2025 | Hotline: 0987973723</h3>", unsafe_allow_html=True)
# Dữ liệu mã lỗi mở rộng
data = {
    "Máy Giặt": {
        "Samsung": {
            "4C": "Lỗi không cấp nước. Kiểm tra van cấp và lưới lọc.",
            "4E": "Lỗi không cấp nước. Kiểm tra van cấp và lưới lọc.",
            "5C": "Lỗi thoát nước. Kiểm tra bơm xả và ống thoát.",
            "5E": "Lỗi thoát nước. Kiểm tra bơm xả và ống thoát.",
            "DC": "Lỗi cửa mở. Đóng lại cửa máy.",
            "UD": "Lỗi cảm biến mực nước (Phao áp lực).",
        },
        "LG": {
            "DE": "Lỗi cửa máy giặt chưa đóng chặt.",
            "IE": "Nước không vào máy giặt.",
            "OE": "Lỗi thoát nước (kiểm tra bơm xả).",
            "PE": "Lỗi cảm biến áp lực phao nước.",
        }
    },
    "Điều Hòa": {
        "Daikin": {
            "A1": "Lỗi bo mạch dàn lạnh.",
            "A6": "Lỗi động cơ quạt dàn lạnh.",
            "C4": "Lỗi cảm biến nhiệt độ trao đổi nhiệt dàn lạnh.",
            "E7": "Lỗi kết nối giữa quạt dàn nóng và bo mạch.",
            "U0": "Lỗi thiếu ga hoặc nghẹt hệ thống dẫn ga.",
        },
        "Panasonic": {
            "H11": "Lỗi giao tiếp giữa dàn lạnh và dàn nóng.",
            "H14": "Lỗi cảm biến nhiệt độ phòng.",
            "H19": "Lỗi khối quạt dàn lạnh bị kẹt.",
            "F95": "Lỗi nhiệt độ dàn nóng quá cao.",
        }
    },
    "Bếp Từ": {
        "Sunhouse": {
            "E0": "Chưa có nồi trên bếp hoặc nồi không phù hợp, mạch nhận biết nồi.",
            "E1": "Bếp quá nóng do đun nấu quá lâu.",
            "E2": "Điện lưới quá mạnh (trên 240V).",
            "E3": "Điện lưới quá yếu (dưới 170V).",
            "E5": "Trở cảm biến bị quá nhiệt.",
            "E6": "Cảm biến nhiệt có vấn đề hoặc đáy nồi quá nóng.",
        },
        "Bosch": {
            "E0": "Lỗi truyền thông nội bộ.",
            "F0": "Lỗi cảm biến nhiệt độ.",
            "F2": "Mạch điện tử quá nóng, bếp sẽ tự ngắt.",
            "F4": "Lỗi hệ thống điều khiển.",
        },
        "Media": {
            "E1": "Quá dòng hoặc lỗi mạch công suất.",
            "E2": "Lỗi cảm biến nhiệt độ đáy nồi.",
            "E3": "Điện áp cao hơn mức cho phép.",
            "E4": "Điện áp thấp hơn mức cho phép.",
        }
    }
}

# Giao diện chọn loại máy và hãng
col1, col2 = st.columns(2)
with col1:
    loai_may = st.selectbox("Chọn loại máy", list(data.keys()))
with col2:
    hang = st.selectbox("Chọn hãng", list(data[loai_may].keys()))

# Nhập mã lỗi
ma_loi = st.text_input("Nhập mã lỗi (Ví dụ: E0, E1, U0, 4C...)", "").upper().strip()

if st.button("Tra cứu"):
    if ma_loi:
        ket_qua = data[loai_may][hang].get(ma_loi)
        if ket_qua:
            st.success(f"**Kết quả cho mã {ma_loi}:** {ket_qua}")
        else:
            st.error("Chưa có dữ liệu cho mã lỗi này.")
    else:
        st.warning("Vui lòng nhập mã lỗi cần tra cứu.")

st.info("💡 Hotline hỗ trợ kỹ thuật: 0987973723 - Kỹ sư Ba Duy sẵn sàng hỗ trợ!")
