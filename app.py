import streamlit as st
from backend import get_chat_response

st.set_page_config(page_title="Study ChatBot", layout="wide")
st.title("📚 Study ChatBot")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Chat container
chat_container = st.container()

# User input area with columns for better layout
col1, col2 = st.columns([5, 1])
with col1:
    user_input = st.text_input("Ask me anything related to studies:", key="user_input")
with col2:
    send_button = st.button("Send")

# Process input
if (send_button or user_input) and user_input:
    # Get response from backend
    response = get_chat_response(user_input, st.session_state.chat_history)
    
    # Add to chat history
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    st.session_state.chat_history.append({"role": "assistant", "content": response})
    
    # Clear the input field after sending
    st.session_state.user_input = ""
    
    # Rerun to update the UI immediately
    st.rerun()

# Display chat history in the container
with chat_container:
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.chat_message("user").markdown(message["content"])
        else:
            st.chat_message("assistant").markdown(message["content"])

# Add a bit of space at the bottom for better appearance
st.markdown("<br><br>", unsafe_allow_html=True)
