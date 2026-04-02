import streamlit as st
import datetime

# 페이지 제목
st.title("나의 첫 번째 Streamlit 앱")

# 간단한 텍스트 작성
st.write("데이터 분석 11기")

# 현재 시간 표시
st.write(f"현재 시간: {datetime.datetime.now()}")

# 이미지 작성
st.image(
    "https://i.imgur.com/JWYdPlR.jpeg",
    caption="데이터 분석 중인 포켓몬",
)