import streamlit as st

# Thương hiệu baduy@2025
st.title("🛠️ KHO MÃ LỖI ĐIỆN TỬ VIỆT NAM")
st.subheader("Design by baduy@2025 | Hotline: 0987973723")

# Dữ liệu tổng hợp các hãng thông dụng
data = {
    "Bếp Từ": {
        "Sunhouse": {"E0": "Nồi không phù hợp, hoặc không có nồi, mạch nhận nồi", "E1": "Quá nhiệt, quạt quay yếu hoặc không quay", "E2": "Lỗi cảm biến mâm"},
        "Kangaroo": {"E1": "Lỗi quạt", "E2": "Cảm biến nhiệt lỗi"},
        "Bosch": {"E0513": "Lỗi giao tiếp", "F0": "Lỗi bo nguồn"}
    },
    "Máy Giặt": {
        "LG": {"DE": "Lỗi cửa", "IE": "Lỗi cấp nước", "OE": "Lỗi thoát nước"},
        "Samsung": {"4E": "Không cấp nước", "5E": "Lỗi bơm xả", "UE": "Mất cân bằng"},
        "Toshiba": {"E1": "Xả nước chậm", "E23": "Hỏng khóa cửa"}
    },
    "Điều Hòa": {
        "Daikin": {"A1": "Lỗi bo dàn lạnh", "U4": "Lỗi tín hiệu", "L5": "Quá tải máy nén"},
        "Panasonic": {"H11": "Lỗi kết nối cục nóng/lạnh", "F95": "Nhiệt độ cục nóng cao"}
    }
}

# Giao diện tra cứu
cat = st.selectbox("Chọn loại máy", list(data.keys()))
brand = st.selectbox("Chọn hãng", list(data[cat].keys()))
code = st.text_input("Nhập mã lỗi").upper()

if st.button("Tra cứu"):
    if code in data[cat][brand]:
        st.success(f"Kết quả: {data[cat][brand][code]}")
        st.write("---")
        st.write("📞 Liên hệ hỗ trợ: 0987973723")
    else:
        st.error("Chưa có dữ liệu cho mã lỗi này.")