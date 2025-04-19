import streamlit as st
from backend import get_chat_response

st.set_page_config(page_title="Study ChatBot", layout="wide")
st.title("📚 Study ChatBot")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# User input
user_input = st.text_input("Ask me anything related to studies:", key="user_input")

if st.button("Send") and user_input:
    # Get response from backend
    response = get_chat_response(user_input, st.session_state.chat_history)

    # Add to chat history
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    st.session_state.chat_history.append({"role": "assistant", "content": response})

# Display chat history
for message in st.session_state.chat_history:
    if message["role"] == "user":
        st.markdown(f"**You:** {message['content']}")
    else:
        st.markdown(f"**Bot:** {message['content']}")
