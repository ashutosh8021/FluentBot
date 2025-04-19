import streamlit as st

# Try to import the backend module
try:
    from backend import get_chat_response
    backend_available = True
except ImportError:
    backend_available = False

st.set_page_config(page_title="Study ChatBot", layout="wide")
st.title("📚 Study ChatBot")

# Display warning if backend is not available
if not backend_available:
    st.warning("Backend module not found. Make sure 'backend.py' is in the same directory as 'app.py'.")

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
    # Store the user input
    user_message = user_input
    
    # Add user message to chat history
    st.session_state.chat_history.append({"role": "user", "content": user_message})
    
    # Get response from backend if available
    if backend_available:
        try:
            response = get_chat_response(user_message, st.session_state.chat_history[:-1])
        except Exception as e:
            response = f"An error occurred: {str(e)}"
    else:
        response = "Backend service is not available. Please check if backend.py exists and all dependencies are installed."
    
    # Add assistant response to chat history
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
