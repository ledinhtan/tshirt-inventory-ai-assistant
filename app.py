import os
import streamlit as st
from dotenv import load_dotenv
from src.text_to_sql_chain import create_sql_chain

# ------------------------- Configuration -------------------------
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# Cache engine to avoid reloading VectorDB every time a query is made 
@st.cache_resource
def get_engine(key):
    return create_sql_chain(key)

def main():
    # 1. Page configuration
    st.set_page_config(page_title="T-shirt AI Admin", layout="wide", page_icon="👕")

    if not api_key:
        st.error("🔑 Missing GOOGLE_API_KEY in .env file! / Thiếu mã API trong file .env!")
        st.stop()

    engine = get_engine(api_key)

    # ------------------------- Sidebar / Thanh bên -------------------------
    with st.sidebar:
        st.title("⚙️ System settings / Cài đặt hệ thống")
        st.markdown("---")
        if st.button("🔄 Clear cache / Làm mới hệ thống"):
            st.cache_resource.clear()
            st.rerun()
        st.caption("v1.0 • Stable release 2026")

    # ------------------------- Main Interface / Giao diện chính -------------------------
    st.title("👕 T-shirt shop smart assistant")
    st.subheader("Trợ lý cửa hàng thông minh")
    
    st.markdown("Ask anything about stock, prices, or revenue / Hỏi bất cứ điều gì về tồn kho, giá cả hoặc doanh thu.")

    user_query = st.text_input(
        "Enter your question / Nhập câu hỏi của bạn:", 
        placeholder="e.g. How many white Nike shirts left? / Ví dụ: Còn bao nhiêu áo Nike trắng?"
    )

    if user_query:
        with st.spinner("Processing... / Đang xử lý..."):
            try:
                # Step 1: Generate SQL
                sql_query = engine["sql_gen"].invoke({"question": user_query})
                
                # Step 2: Run the SQL query to retrieve the data
                raw_result = engine["db_exec"].invoke(sql_query)
                
                # Step 3: Compile the answers
                final_answer = engine["answer_chain"].invoke({
                    "question": user_query,
                    "query": sql_query,
                    "result": raw_result
                })
                
                # Display main results
                st.markdown("### 🤖 Answer / Trả lời:")
                st.success(final_answer)
                
                # --- Debug cho Admin (Song ngữ & Sentence case) ---
                with st.expander("🛠️ Technical details (Admin only) / Chi tiết kỹ thuật (Dành cho quản trị viên)"):
                    st.write("**Generated SQL query / Câu lệnh SQL đã tạo:**")
                    st.code(sql_query, language="sql")
                    
                    st.write("**Raw database result / Dữ liệu thô từ DB:**")
                    st.info(f"Result: {raw_result}")
                    
            except Exception as e:
                st.error(f"❌ An error occurred / Có lỗi xảy ra: {e}")

# ------------------------- Entry Point -------------------------
if __name__ == "__main__":
    main()