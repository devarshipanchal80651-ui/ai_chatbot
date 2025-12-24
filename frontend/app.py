import streamlit as st
import os
import requests

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="AI Chatbot", layout="centered")

# ---------- LOAD CSS ----------
def load_css():
    css_path = os.path.join(os.path.dirname(__file__), "style.css")
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# ---------- SESSION STATE ----------
if "page" not in st.session_state:
    st.session_state.page = "login"

if "messages" not in st.session_state:
    st.session_state.messages = []

if "username" not in st.session_state:
    st.session_state.username = ""

# ---------- NAV FUNCTIONS ----------
def go_login():
    st.session_state.page = "login"

def go_register():
    st.session_state.page = "register"

def go_chat():
    st.session_state.page = "chat"

# ---------- LOGIN PAGE ----------
def login_page():
    st.markdown("<h2 class='center'>💬 AI Chatbot</h2>", unsafe_allow_html=True)
    st.markdown("<h4>🔐 Login</h4>", unsafe_allow_html=True)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        # ❌ OLD WRONG CODE (commented for learning)
        # res = requests.post(
        #     "http://127.0.0.1:8000/login",
        #     params={username: password, password: password},
        # )

        # ✅ CORRECT LOGIN API CALL
        res = requests.post(
            "http://127.0.0.1:8000/login",
            json={"username": username, "password": password}
        )

        if res.status_code == 200 and res.json().get("success"):
            st.session_state.username = username
            st.session_state.messages = []
            go_chat()
            st.rerun()
        else:
            st.error("❌ Invalid username or password")

    st.markdown("<p class='link'>No account?</p>", unsafe_allow_html=True)
    if st.button("Go to Register"):
        go_register()

# ---------- REGISTER PAGE ----------
def register_page():
    st.markdown("<h2 class='center'>💬 AI Chatbot</h2>", unsafe_allow_html=True)
    st.markdown("<h4>📝 Register</h4>", unsafe_allow_html=True)

    username = st.text_input("New Username")
    password = st.text_input("Create Password", type="password")

    if st.button("Create Account"):
        if username and password:

            # ❌ OLD FAKE REGISTER (commented)
            # st.success("Account created successfully")
            # go_login()

            # ✅ REAL REGISTER API CALL
            res = requests.post(
                "http://127.0.0.1:8000/register",
                json={"username": username, "password": password}
            )

            if res.status_code == 200:
                st.success("✅ Account created successfully")
                go_login()
                st.rerun()
            else:
                st.error("❌ Registration failed")

        else:
            st.error("❌ All fields required")

    if st.button("Back to Login"):
        go_login()

# ---------- CHAT PAGE ----------
def chat_page():
    st.sidebar.markdown(f"👤 **{st.session_state.username}**")

    if st.sidebar.button("🧹 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    if st.sidebar.button("🚪 Logout"):
        st.session_state.page = "login"
        st.session_state.username = ""
        st.session_state.messages = []
        st.rerun()

    st.markdown("<h2 class='center'>💬 AI Chatbot</h2>", unsafe_allow_html=True)

    # CHAT HISTORY
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"<div class='user'>{msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='bot'>{msg['content']}</div>", unsafe_allow_html=True)

    # ENTER KEY SUPPORT
    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input("Type your message...")
        submitted = st.form_submit_button("Send")

        if submitted and user_input:
            # USER MESSAGE
            st.session_state.messages.append(
                {"role": "user", "content": user_input}
            )

            # AI BACKEND CALL
            try:
                response = requests.post(
                    "http://127.0.0.1:8000/chat",
                    json={"message": user_input},
                    timeout=30
                )

                if response.status_code == 200:
                    ai_reply = response.json().get("reply", "No response")
                else:
                    ai_reply = "❌ AI server error"

            except Exception:
                ai_reply = "❌ Unable to connect to AI server"

            # AI MESSAGE
            st.session_state.messages.append(
                {"role": "assistant", "content": ai_reply}
            )

            st.rerun()

# ---------- ROUTER ----------
if st.session_state.page == "login":
    login_page()
elif st.session_state.page == "register":
    register_page()
elif st.session_state.page == "chat":
    chat_page()