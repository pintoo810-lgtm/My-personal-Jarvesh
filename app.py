import streamlit as st
from groq import Groq

# 1. Page Setup
st.set_page_config(page_title="Jarvis AI", page_icon="🤖")

# 2. Authentication Logic
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.title("🔒 Private Access")
    pwd = st.text_input("Enter Passphrase:", type="password")
    if st.button("Unlock"):
        # Aapka family password
        if pwd == "PINTU_PASWAN_DEEPAK_KUMAR_DAKSH_PASWAN_JYOTI_PASWAN_URMILA_DEVI_SWEET_FAMILY":
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("Ghalat Password!")
else:
    st.title("🤖 My Jarvis")
    
    # 3. Direct API Client (Secrets bypass kar diya hai)
    # Yeh wahi key hai jo aapne generate ki hai
    client = Groq(api_key="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")

    # 4. Chat History
    if "msgs" not in st.session_state:
        st.session_state.msgs = []

    for m in st.session_state.msgs:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    # 5. Chat Input
    if p := st.chat_input("Hukum karein Boss..."):
        st.session_state.msgs.append({"role": "user", "content": p})
        with st.chat_message("user"):
            st.markdown(p)

        with st.chat_message("assistant"):
            try:
                # Humne Playground wala model hi use kiya hai
                response = client.chat.completions.create(
                    model="llama3-8b-8192",
                    messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.msgs]
                )
                answer = response.choices[0].message.content
                st.markdown(answer)
                st.session_state.msgs.append({"role": "assistant", "content": answer})
            except Exception as e:
                st.error(f"Error: {e}")
