import streamlit as st
from groq import Groq
import speech_recognition as sr
import pyttsx3
from streamlit_webrtc import webrtc_streamer
client = Groq(api_key="Gsk_qdabF41X56cADuYVKlJjWGdyb3FYOL52oANDMA0iQFqwJ7JLeNem")

# Speaker Setup
engine = pyttsx3.init()
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Mic Setup
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.toast("Listening... Boliye!")
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
            query = r.recognize_google(audio, language='en-IN')
            return query
        except:
            return None

# --- UI SETUP ---
st.set_page_config(page_title="Jarvis Pro", layout="wide")
st.title("🤖 My Jarvis: Vision & Voice")

if "messages" not in st.session_state:
    st.session_state.messages = []

col_left, col_right = st.columns([1, 1.5])

with col_left:
    st.subheader("📸 Live Vision")
    webrtc_streamer(key="jarvis-camera")
    st.divider()
    if st.button("🎤 Activate Mic", use_container_width=True):
        voice_query = listen()
        if voice_query:
            st.session_state.messages.append({"role": "user", "content": voice_query})
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": voice_query}]
            )
            res = completion.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": res})
            st.rerun()

with col_right:
    st.subheader("💬 Chat")
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    text_input = st.chat_input("Hukum karein Boss...")
    if text_input:
        st.session_state.messages.append({"role": "user", "content": text_input})
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": text_input}]
        )
        res = completion.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": res})
        st.rerun()

if len(st.session_state.messages) > 0:
    last_msg = st.session_state.messages[-1]
    if last_msg["role"] == "assistant":
        speak(last_msg["content"])

