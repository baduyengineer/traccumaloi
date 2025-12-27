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
            "4C": "Lỗi không cấp nước vào máy. Kiểm tra van cấp và lưới lọc.",
            "5C": "Lỗi không thoát nước. Kiểm tra bơm xả và ống thoát.",
            "DC": "Lỗi mở cửa khi máy đang chạy.",
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
        "Munchen": {
            "E1": "Lỗi cảm biến nhiệt độ trên mâm từ.",
            "E2": "Lỗi nguồn điện cung cấp không ổn định.",
            "E3": "Lỗi quạt tản nhiệt không hoạt động.",
        },
        "Chefs": {
            "E1": "Quá nhiệt bo mạch hoặc mặt kính.",
            "E2": "Điện áp quá cao (trên 240V).",
            "E4": "Cảm biến nhiệt độ bị hở hoặc lỗi.",
        },
        "Midea": {
            "E1": "Lỗi quá dòng (kiểm tra phần công suất).",
            "E3": "Điện áp cao vượt mức cho phép.",
            "E4": "Điện áp thấp dưới mức cho phép.",
        },
        "Barcher": {
            "E1": "Không có nồi hoặc nồi không phù hợp.",
            "E5": "Lỗi quá nhiệt IGBT (phần công suất).",
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

st.info("💡 Hotline hỗ trợ kỹ thuật: 0987973723 - Kỹ sư Ba Duy.")

