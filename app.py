import streamlit as st
from groq import Groq

# --- CONFIGURATION ---
API_KEY = "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" 
MY_SECRET_PASS = "PINTU_PASWAN_DEEPAK_KUMAR_DAKSH_PASWAN_JYOTI_PASWAN_URMILA_DEVI_SWEET_FAMILY"

st.set_page_config(page_title="My Private AI", layout="centered")

# --- LOGIN LOGIC ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🔒 Private Access")
    password_input = st.text_input("Enter Passphrase to Unlock:", type="password")
    if st.button("Unlock"):
        if password_input == MY_SECRET_PASS:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Wrong Passphrase! Access Denied.")
else:
    # --- CHAT INTERFACE ---
    st.title("🤖 My Personal AI")
    client = Groq(api_key=API_KEY)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Kaise madad karun?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            response = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=st.session_state.messages
            )
            full_response = response.choices[0].message.content
            st.markdown(full_response)
        
        st.session_state.messages.append({"role": "assistant", "content": full_response})
