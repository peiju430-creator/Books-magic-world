import streamlit as st
import plotly.graph_objects as go
from openai import OpenAI

# 1. 安全讀取 API Key
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="越讀不可思議", layout="wide")

# 2. 初始化資料
if 'learning_data' not in st.session_state:
    st.session_state.learning_data = {
        "what": "", "why": "", "expectation": "", "prior_knowledge": "", "bias": "",
        "white": "", "green": "", "black": "", "yellow": "",
        "feynman_sentence": ""
    }
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 3. 側邊導覽
st.sidebar.title("🌀 螺旋學習導航")
phase = st.sidebar.radio("切換階段", ["越讀定位", "四色思維", "費曼轉譯", "後設共鳴", "AI 教練對話"])

# --- 第一階段：定位 ---
if phase == "越讀定位":
    st.header("📍 第一階段：越讀定位")
    st.session_state.learning_data["what"] = st.text_input("📚 主題/書名", value=st.session_state.learning_data["what"])
    st.session_state.learning_data["why"] = st.text_area("🎯 為什麼選擇它？", value=st.session_state.learning_data["why"])
    st.session_state.learning_data["prior_knowledge"] = st.text_area("🧠 我已知的是...", value=st.session_state.learning_data["prior_knowledge"])
    st.session_state.learning_data["bias"] = st.text_area("⚖️ 我的偏見是...", value=st.session_state.learning_data["bias"])

# --- 第二階段：四色思維 ---
elif phase == "四色思維":
    st.header("🧪 四色思維實驗室")
    c1, c2 = st.columns(2)
    with c1:
        st.session_state.learning_data["white"] = st.text_area("⚪ 白色思考 (事實數據)", value=st.session_state.learning_data["white"])
        st.session_state.learning_data["black"] = st.text_area("⚫ 黑色思考 (風險挑戰)", value=st.session_state.learning_data["black"])
    with c2:
        st.session_state.learning_data["green"] = st.text_area("🟢 綠色思考 (創意變革)", value=st.session_state.learning_data["green"])
        st.session_state.learning_data["yellow"] = st.text_area("🟡 黃色思考 (正面價值)", value=st.session_state.learning_data["yellow"])

# --- 第三階段：費曼轉譯 ---
elif phase == "費曼轉譯":
    st.header("🗣️ 第三階段：不可思議轉譯")
    st.session_state.learning_data["feynman_sentence"] = st.text_area("✍️ 嘗試用一句話整合四色思考...", value=st.session_state.learning_data["feynman_sentence"])

# --- 第四階段：後設共鳴 ---
elif phase == "後設共鳴":
    st.header("📊 第四階段：後設共鳴")
    d = st.session_state.learning_data
    scores = [len(d["white"]), len(d["green"]), len(d["yellow"]), len(d["black"])]
    fig = go.Figure(data=go.Scatterpolar(r=scores+[scores[0]], theta=['白色','綠色','黃色','黑色','白色'], fill='toself'))
    st.plotly_chart(fig)
    st.download_button("📂 下載學習報告", data=f"主題：{d['what']}\n結果：{d['feynman_sentence']}", file_name="report.txt")

# --- AI 教練對話 ---
elif phase == "AI 教練對話":
    st.header("🤖 AI 思維園丁")
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])
    
    if prompt := st.chat_input("跟園丁聊聊你的發現..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        with st.chat_message("assistant"):
            res = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "system", "content": "你是一位溫暖創意的思維教練，請根據學生的四色思考給予鼓勵與引導。"}] + st.session_state.chat_history
            )
            ans = res.choices[0].message.content
            st.markdown(ans)
        st.session_state.chat_history.append({"role": "assistant", "content": ans})
