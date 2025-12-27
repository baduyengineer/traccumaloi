import streamlit as st

# Thiết lập giao diện
st.set_page_config(page_title="Tra cứu mã lỗi - Baduy@2025", layout="centered")

# Tiêu đề chính
st.markdown("<h1 style='text-align: center;'>🛠️ KHO MÃ LỖI ĐIỆN TỬ VIỆT NAM</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Design by baduy@2025 | Hotline: 0987973723</h3>", unsafe_allow_html=True)

# Dữ liệu mã lỗi tổng hợp
data = {
    "Máy Giặt": {
        "Samsung": {
            "4C": "Lỗi không cấp nước. Kiểm tra van cấp và lưới lọc.",
            "5C": "Lỗi không thoát nước. Kiểm tra bơm xả và ống thoát.",
            "DC": "Lỗi cửa mở khi máy đang chạy.",
        },
        "LG": {
            "DE": "Lỗi cửa máy chưa đóng chặt.",
            "IE": "Nước không vào máy.",
            "OE": "Lỗi thoát nước (kiểm tra bơm xả).",
        }
    },
    "Điều Hòa": {
        "Daikin": {
            "A1": "Lỗi bo mạch dàn lạnh.",
            "U0": "Lỗi thiếu ga hoặc nghẹt hệ thống dẫn ga.",
        },
        "Panasonic": {
            "H11": "Lỗi giao tiếp giữa dàn lạnh và dàn nóng.",
            "F95": "Lỗi nhiệt độ dàn nóng quá cao.",
        }
    },
    "Bếp Từ": {
        "Sunhouse": {
            "E0": "Chưa có nồi hoặc nồi không phù hợp.",
            "E1": "Bếp quá nóng hoặc lỗi quạt tản nhiệt.",
            "E2": "Điện áp quá cao (trên 240V).",
            "E3": "Điện áp quá thấp (dưới 170V).",
        },
        "Bosch": {
            "E0": "Lỗi truyền thông nội bộ giữa các bo mạch.",
            "F0": "Lỗi cảm biến nhiệt độ mặt kính.",
            "F2": "Bo mạch bị quá nhiệt, bếp tự ngắt bảo vệ.",
            "F4": "Lỗi hệ thống điều khiển cảm ứng.",
        },
        "Elmich": {
            "E1": "Lỗi cảm biến nhiệt mâm từ bị hở.",
            "E2": "Lỗi cảm biến nhiệt mâm từ bị ngắn mạch.",
            "E3": "Điện áp cung cấp quá cao.",
            "E4": "Điện áp cung cấp quá thấp.",
        },
        "Munchen": {
            "E1": "Lỗi cảm biến nhiệt độ trên mâm từ.",
            "E2": "Lỗi nguồn điện không ổn định.",
        }
    }
}

# Giao diện tra cứu
loai_may = st.selectbox("Chọn loại máy", list(data.keys()))
hang = st.selectbox("Chọn hãng", list(data[loai_may].keys()))
ma_loi = st.text_input("Nhập mã lỗi").upper().strip()

if st.button("Tra cứu"):
    if ma_loi:
        ket_qua = data[loai_may][hang].get(ma_loi)
        if ket_qua:
            st.success(f"**Kết quả cho mã {ma_loi}:** {ket_qua}")
        else:
            st.error("Chưa có dữ liệu cho mã lỗi này.")

st.info("💡 Hotline hỗ trợ kỹ thuật: 0987973723 - Kỹ sư Ba Duy luôn sẵn sàng!")
