import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI
import gpts_prompt  # SYSTEM_PROMPT 정의된 파일

# 🔑 OpenAI API 키 로드
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 🎨 페이지 설정 및 CSS
st.set_page_config(page_title="스쿱메이트 🍨", page_icon="🍧")

st.markdown("""
<style>
body, .stApp {
    background: linear-gradient(to bottom right, #ffffff, #f1f3f5);
}
.chat-container {
    display: flex;
    flex-direction: column;
}
.chat-box {
    padding: 1rem;
    margin: 0.5rem 0;
    border-radius: 12px;
    font-size: 1.05rem;
    line-height: 1.6;
    display: flex;
    align-items: flex-end;
    gap: 0.6rem;
    white-space: pre-wrap;
    word-break: break-word;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}
.user-msg {
    max-width: 65%;
    background-color: #fff9db;
    color: #333;
    flex-direction: row-reverse;
    justify-content: flex-end;
    align-self: flex-end;
    margin-left: auto;
}
.assistant-msg {
    max-width: 80%;
    background-color: #e7f5ff;
    color: #222;
    align-self: flex-start;
}
.chat-avatar {
    width: 38px;
    height: 38px;
    border-radius: 50%;
    background: #fff;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    box-shadow: 0 1px 4px #e3e3e3;
}
.chat-avatar img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}
</style>
""", unsafe_allow_html=True)

# 🌟 페이지 제목
st.title("🍨 젤또라또 - 나만의 젤라또 찾기")

# 🔗 프로필 이미지 링크
USER_IMG_URL = "https://i.imgur.com/Hq44U7n.png"
ASSISTANT_IMG_URL = "https://i.imgur.com/5UMNbxO.png"  # ✅ 변경된 이미지

# 🧠 세션 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.started = False

    # 인삿말
    st.markdown("""
        <div style='text-align: center; font-size: 18px; padding: 1rem 0 0.5rem 0; line-height: 1.4;'>
            👋 안녕하세요!<br>
            <strong>🍦 스쿱메이트</strong>에 오신 걸 환영합니다.<br><br>
            아래 버튼을 눌러 나만의 젤라또 조합을 찾아보세요!
        </div>
    """, unsafe_allow_html=True)

# 💬 이전 대화 출력
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"""
            <div class="chat-box user-msg">
                <div class="chat-avatar"><img src="{USER_IMG_URL}"/></div>
                <div>{msg["content"]}</div>
            </div>
        """, unsafe_allow_html=True)
    elif msg["role"] == "assistant":
        st.markdown(f"""
            <div class="chat-box assistant-msg">
                <div class="chat-avatar"><img src="{ASSISTANT_IMG_URL}"/></div>
                <div>{msg["content"]}</div>
            </div>
        """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# 🍨 시작 버튼
if not st.session_state.started:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🍨 젤라또 조합 시작하기", use_container_width=True):
            st.session_state.started = True
            st.session_state.messages.append({
                "role": "system",
                "content": gpts_prompt.SYSTEM_PROMPT
            })
            st.session_state.messages.append({
                "role": "assistant",
                "content": "안녕하세요, 젤라또 마스터 젤또라또입니다! 🍦\n당신만의 젤라또 조합을 찾아드릴게요. 시작해볼까요?"
            })
            st.rerun()

# 💬 사용자 입력
else:
    user_input = st.chat_input("젤또라또에게 물어보세요!")

    if user_input:
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })

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
                st.rerun()
            except Exception as e:
                st.error(f"에러 발생: {e}")
