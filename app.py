import streamlit as st
from groq import Groq
import speech_recognition as sr
import pyttsx3
import cv2
from streamlit_webrtc import webrtc_streamer

# --- CONFIG ---
client = Groq(api_key="Gsk_qdabF41X56cADuYVKlJjWGdyb3FYOL52oANDMA0iQFqwJ7JLeNem") 

# Speaker Setup (Text-to-Speech)
engine = pyttsx3.init()
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Mic Setup (Speech-to-Text)
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening... Hukum karein Boss!")
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
            query = r.recognize_google(audio, language='en-IN')
            return query
        except:
            return None

# --- UI DESIGN ---
st.set_page_config(page_title="Jarvis Pro", layout="wide")
st.title("🤖 My Jarvis: Full Access")

# Layout: Left for Camera, Right for Chat
col_cam, col_chat = st.columns([1, 1.5])

with col_cam:
    st.subheader("📸 Live Camera")
    # Real-time camera stream
    webrtc_streamer(key="jarvis-vision")
    
    st.divider()
    
    # Mic Activation Button
    if st.button("🎤 Activate Voice Command", use_container_width=True):
        command = listen()
        if command:
            st.session_state.messages.append({"role": "user", "content": command})
            
            # API Call
            chat_completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": command}]
            )
            response = chat_completion.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": response})
            speak(response)
            st.rerun()

with col_chat:
    st.subheader("💬 Chat Hub")
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display Chat History
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Manual Text Input
    user_input = st.chat_input("Yahan type karein...")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        chat_completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": user_input}]
        )
        response = chat_completion.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": response})
        speak(response)
        st.rerun()
