import streamlit as st 
from agent_controller import handle_user_input
from browser_driver import send_email, perform_google_search
from dotenv import load_dotenv
import os
import glob

# --- 🌱 Load environment ---
load_dotenv()

# --- 🖥️ Page Config ---
st.set_page_config(page_title="Browser Agent", layout="wide", initial_sidebar_state="expanded")

# --- 💅 Purple-White ChatGPT UI ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');

body {
    background-color: #f7f6ff;
    font-family: 'Inter', sans-serif;
}
header, footer { visibility: hidden; }

h1, h2, h3 {
    color: #4b0082;
}

.stChatMessage {
    background-color: white;
    border-radius: 16px;
    padding: 1rem;
    margin-bottom: 0.5rem;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}
.stChatMessage.user {
    border-left: 5px solid #9f7aea;
}
.stChatMessage.assistant {
    border-left: 5px solid #6b46c1;
}
img {
    border-radius: 12px;
    margin-top: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}
.stSidebar {
    background-color: #f0ebff !important;
    color: #4b0082;
    border-right: 1px solid #e0d5ff;
}
.css-1d391kg {
    background-color: #f0ebff !important;
}
</style>
""", unsafe_allow_html=True)

# --- 🟣 Sidebar ---
with st.sidebar:
    st.markdown("## 🟣 Browser Agent")
    st.markdown("### 🔍 Recent Trends")
    st.markdown("- 📈 AI Email Automation")
    st.markdown("- 🔎 Natural Language Search")
    st.markdown("- 📤 Auto Web Interaction")
    st.markdown("---")
    st.markdown("### 🧠 Session Info")
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    st.write(f"Total messages: {len(st.session_state['messages'])}")

# --- 🟪 Title & Intro ---
st.markdown("## 💬 Browser Agent")
st.markdown("Talk to your browser: send emails, search Google, or just chat 💜")

# --- 🧠 Chat Memory ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 🪵 Display Chat History ---
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).markdown(msg["content"])

# --- 💬 Chat Input ---
if user_input := st.chat_input("Ask me to send email, search Google, or anything else..."):
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # ✨ AI handles intent
    response, state = handle_user_input(user_input)

    st.chat_message("assistant").markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})

    # --- ✉️ Email Flow ---
    if state and state.get("subject") and state.get("recipient"):
        screenshot_path = send_email(state)
        st.success("✅ Email Sent Successfully!")

        st.markdown("### 📸 Gmail Steps:")
        email_paths = sorted(glob.glob("screenshots/*email_*.png"))
        if email_paths:
            for path in email_paths:
                label = os.path.basename(path).replace("_", " ").replace(".png", "")
                st.markdown(f"**{label.capitalize()}**")
                st.image(path, use_column_width=True)
        else:
            st.warning("⚠️ No screenshots found for Gmail process.")

    # --- 🔎 Google Search Flow ---
    elif state and state.get("query"):
        screenshot_path = perform_google_search(state)
        st.success("🔍 Google search completed!")

        st.markdown("### 📸 Google Search Screenshots:")
        search_paths = sorted(glob.glob("screenshots/*google_*.png"))
        if search_paths:
            for path in search_paths:
                label = os.path.basename(path).replace("_", " ").replace(".png", "")
                st.markdown(f"**{label.capitalize()}**")
                st.image(path, use_column_width=True)
        else:
            st.warning("⚠️ No screenshots found for Google search.")
