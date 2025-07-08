# chatbot.py
import streamlit as st
import os
from dotenv import load_dotenv
import gpts_prompt
from openai import OpenAI  # 최신 방식 사용

# 🔑 환경 변수 로드 및 OpenAI 클라이언트 생성
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 🎨 페이지 설정
st.set_page_config(page_title="스쿱메이트 🍨", page_icon="🍧")
st.title("🍨 젤또라또 - 나만의 젤라또 찾기")

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.started = False

    # 인삿말 출력
    st.markdown(
        """
        <div style='text-align: center; font-size: 20px; padding: 1.5rem;'>
            👋 안녕하세요!<br>
            <strong>🍦 스쿱메이트</strong>에 오신 걸 환영합니다.<br><br>
            아래 버튼을 눌러 나만의 젤라또 조합을 찾아보세요!
        </div>
        """,
        unsafe_allow_html=True
    )

# 이전 대화 출력 (system은 제외)
for msg in st.session_state.messages:
    if msg["role"] != "system":
        st.chat_message(msg["role"]).markdown(msg["content"])

# 🍨 버튼 표시
if not st.session_state.started:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🍨 젤라또 조합 시작하기"):
            st.session_state.started = True

            # SYSTEM 메시지는 GPT에게만 전달
            st.session_state.messages.append({
                "role": "system",
                "content": gpts_prompt.SYSTEM_PROMPT
            })

            # GPT가 자연스럽게 시작하도록 유도
            st.session_state.messages.append({
                "role": "assistant",
                "content": "안녕하세요, 젤라또 마스터 젤또라또 입니다"
            })

            st.rerun()

# 👤 사용자 입력 처리
else:
    user_input = st.chat_input("번호 또는 내용을 입력해 주세요")

    if user_input:
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })
        st.chat_message("user").markdown(user_input)

        with st.spinner("젤또라또가 고민 중이에요... 🍦💬"):
            try:
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=st.session_state.messages,
                    temperature=0.7
                )
                reply = response.choices[0].message.content

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": reply
                })
                st.chat_message("assistant").markdown(reply)

            except Exception as e:
                st.error(f"에러 발생: {e}")
