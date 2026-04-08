"""PydanticAI + Streamlit 챗봇

Gemini 모델을 사용한 스트리밍 멀티턴 챗봇입니다.
API 키는 .streamlit/secrets.toml에서 관리합니다.

실행: streamlit run 3_streamlit_응용/02_api_connection/app.py
"""

import os

import streamlit as st
from pydantic_ai import Agent

# secrets.toml의 API 키를 환경변수로 설정 (PydanticAI가 자동 인식)
os.environ["GEMINI_API_KEY"] = st.secrets["GEMINI_API_KEY"]

MODEL_ID = f"google-gla:{st.secrets['GEMINI_MODEL']}"
INSTRUCTIONS = "당신은 친절한 한국어 AI 어시스턴트입니다. 질문에 명확하고 도움이 되는 답변을 해주세요."

st.title("💬 Gemini 챗봇")
st.caption(f"모델: {MODEL_ID}")

# 대화 기록 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []  # UI 표시용
if "message_history" not in st.session_state:
    st.session_state.message_history = []  # PydanticAI 멀티턴용

# 이전 대화 표시 (UI 표시용)
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): 
        st.markdown(msg["content"])

# 사용자 입력
if prompt := st.chat_input("메시지를 입력하세요"):
    # 사용자 메시지 표시 및 저장
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI 응답 (실시간 스트리밍)
    # Streamlit rerun 시 이벤트 루프 충돌이 발생할 수 있어 최대 3회 재시도합니다.
    with st.chat_message("assistant"):
        for attempt in range(3):
            try:
                agent = Agent(MODEL_ID, instructions=INSTRUCTIONS)
                result = agent.run_stream_sync(prompt, message_history=st.session_state.message_history)
                response_text = st.write_stream(result.stream_text(delta=True))
                break
            except RuntimeError as e:
                print(e)
                pass
             

    # 대화 기록 업데이트
    st.session_state.messages.append({"role": "assistant", "content": response_text})
    st.session_state.message_history = result.all_messages()
