
import streamlit as st
from groq import Groq

# 1. Page Configuration
st.set_page_config(page_title="Jarvis AI", page_icon="🤖", layout="centered")

# 2. Authentication Logic
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.title("🔒 Private Access")
    # Using your specific family passphrase
    pwd = st.text_input("Enter Passphrase:", type="password")
    if st.button("Unlock"):
        if pwd == "PINTU_PASWAN_DEEPAK_KUMAR_DAKSH_PASWAN_JYOTI_PASWAN_URMILA_DEVI_SWEET_FAMILY":
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("Access Denied: Incorrect Passphrase")
else:
    # 3. Main Interface
    st.title("🤖 My Jarvis")
    
    # 4. Initialize Groq Client with your new Key
    # GSK Key updated as requested
    client = Groq(api_key="Gsk_8JBxLU8WlAT5BvGAH80nWGdyb3FY0AE00X1Kdv1640LTSpo1As36")

    # 5. Initialize Chat History
    if "msgs" not in st.session_state:
        st.session_state.msgs = []

    # 6. Display Chat History
    for m in st.session_state.msgs:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    # 7. Chat Input & Processing
    if p := st.chat_input("Hukum karein Boss..."):
        # Append user message
        st.session_state.msgs.append({"role": "user", "content": p})
        with st.chat_message("user"):
            st.markdown(p)

        # Generate Assistant Response
        with st.chat_message("assistant"):
            try:
                # API request using Llama 3
                response = client.chat.completions.create(
                    model="llama3-8b-8192",
                    messages=[
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.msgs
                    ]
                )
                
                answer = response.choices[0].message.content
                st.markdown(answer)
                
                # Save assistant response to history
                st.session_state.msgs.append({"role": "assistant", "content": answer})
                
            except Exception as e:
                st.error(f"System Error: {e}")
