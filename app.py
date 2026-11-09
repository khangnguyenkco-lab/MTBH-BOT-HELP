import os
import streamlit as st
from google import genai

# Tiêu đề ứng dụng
st.set_page_config(page_title="Trợ lý Nhân sự Shop", page_icon="🤖")
st.title("🤖 Trợ lý Quản lý Nhân sự & Nội quy Shop")
st.markdown("Hệ thống AI hỗ trợ tra cứu nội quy, quy trình và giải đáp thắc mắc nội bộ.")

# Nhập API Key của Gemini
api_key = st.sidebar.text_input("Nhập Google Gemini API Key của bạn:", type="password")

if not api_key:
    st.warning("Vui lòng nhập Gemini API Key ở thanh bên trái để bắt đầu sử dụng.")
else:
    client = genai.Client(api_key=api_key)

    # Khu vực nhập nội quy mẫu hoặc tài liệu của shop
    st.subheader("📁 Dữ liệu / Nội quy cơ sở của Shop")
    shop_knowledge = st.text_area(
        "Dán nội quy hoặc quy chế của shop vào đây:",
        value="1. Giờ làm việc: Ca sáng từ 8h00 - 12h00, Ca chiều từ 13h30 - 18h00.\n2. Quy định nghỉ phép: Phải báo trước ít nhất 2 ngày cho quản lý.\n3. Đi muộn: Phạt 50.000đ cho mỗi lần trễ quá 15 phút.",
        height=150
    )

    st.divider()

    # Khung chat với AI
    st.subheader("💬 Hỏi đáp cùng Trợ lý AI")
    user_question = st.text_input("Nhân viên hoặc Quản lý muốn hỏi gì?")

    if st.button("Gửi câu hỏi"):
        if user_question:
            with st.spinner("AI đang xử lý dựa trên nội quy của shop..."):
                prompt = f"""
                Dựa vào nội quy cửa hàng sau đây:
                {shop_knowledge}
                
                Hãy trả lời câu hỏi của nhân viên một cách chính xác, ngắn gọn và lịch sự:
                {user_question}
                """
                try:
                  response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt,
)
                    st.success("Kết quả từ trợ lý AI:")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Đã xảy ra lỗi: {e}")
        else:
            st.warning("Vui lòng nhập câu hỏi.")
