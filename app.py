import streamlit as st
from groq import Groq
from gtts import gTTS
import base64
import os

# Page Configuration - Tab name aur logo
st.set_page_config(page_title="Jarvis - Pintu Kumar's AI", page_icon="🎙️")

# Authentication Logic - Password setup
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🔒 Private Access")
    pwd = st.text_input("Apna Khash Passphrase Daalein:", type="password")
    if st.button("Unlock Jarvis"):
        if pwd == "PINTU_PASWAN_DEEPAK_KUMAR_DAKSH_PASWAN_JYOTI_PASWAN_URMILA_DEVI_SWEET_FAMILY":
            st.session_state.authenticated = True
            st.rerun()
else:
    # --- Main App Interface ---
    st.title("🤖 My Jarvis")
    
    # Text-to-Speech Function (Speaker feature)
    def text_to_speech(text):
        tts = gTTS(text=text, lang='hi', slow=False)
        filename = "temp_audio.mp3"
        tts.save(filename)
        with open(filename, "rb") as f:
            audio_bytes = f.read()
            audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
            audio_html = f'<audio controls autoplay style="width: 100%;"><source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3"></audio>'
            st.markdown(audio_html, unsafe_allow_html=True)
        os.remove(filename)

    # Initialize Groq Client (DIRECT API KEY)
    # Galti is line mein pehle thi, ab maine sahi key daal di hai:
    client = Groq(api_key="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")

    # Chat Messages Setup
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat UI (Keyboard mic icon already integrates with this input box)
    if prompt := st.chat_input("Hukum karein Boss..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                # Naya Model jo decommissioned nahi hai:
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",  # Ye naya model hai
                    messages=st.session_state.messages
                )
                ans = response.choices[0].message.content
                st.markdown(ans)
                st.session_state.messages.append({"role": "assistant", "content": ans})
                
                # Jawab bol kar sunayein (Audio component will play automatically)
                if st.checkbox("Audio Reply Sunein?", value=True):
                    text_to_speech(ans)

            except Exception as e:
                st.error(f"Error: {e}")
