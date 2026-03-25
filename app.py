import streamlit as st
from groq import Groq

# Page Setup
st.set_page_config(page_title="Jarvis AI", page_icon="🤖", layout="centered")

# Password Protection
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.title("🔒 Private Access")
    # Aapka wahi purana password
    pwd = st.text_input("Enter Passphrase:", type="password")
    if st.button("Unlock"):
        if pwd == "PINTU_PASWAN_DEEPAK_KUMAR_DAKSH_PASWAN_JYOTI_PASWAN_URMILA_DEVI_SWEET_FAMILY":
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("Ghalat Password! Dubara koshish karein.")
else:
    st.title("🤖 My Jarvis")
    
    # Nayi API Key Setup
    try:
        client = Groq(api_key="Gsk_8JBxLU8WlAT5BvGAH80nWGdyb3FY0AE00X1Kdv1640LTSpo1As36")
    except Exception as e:
        st.error(f"Client setup error: {e}")

    # Chat history initialize karna
    if "msgs" not in st.session_state:
        st.session_state.msgs = []

    # Purani chat history screen par dikhana
    for m in st.session_state.msgs:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    # Naya input lena
    if p := st.chat_input("Hukum karein Boss..."):
        # User ka message save aur display karna
        st.session_state.msgs.append({"role": "user", "content": p})
        with st.chat_message("user"):
            st.markdown(p)

        # Assistant ka response generate karna
        with st.chat_message("assistant"):
            try:
                # API Call - Llama 3 model ke saath
                res = client.chat.completions.create(
                    model="llama3-8b-8192",
                    messages=[
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.msgs
                    ],
                )
                
                txt = res.choices[0].message.content
                st.markdown(txt)
                
                # Response ko history mein save karna
                st.session_state.msgs.append({"role": "assistant", "content": txt})
