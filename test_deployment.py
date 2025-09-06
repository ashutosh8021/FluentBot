# Simple test script to verify FluentBot deployment
# Run this to test if your API key is working

import streamlit as st
import os

st.title("🔧 FluentBot Deployment Test")

# Try to load dotenv
try:
    from dotenv import load_dotenv
    load_dotenv()
    st.success("✅ dotenv loaded successfully")
except ImportError:
    st.info("ℹ️ dotenv not available (normal for cloud deployment)")

# Check environment variable
env_key = os.environ.get("OPENROUTER_API_KEY")
st.write("**Environment Variable Check:**")
if env_key:
    st.success(f"✅ Found in environment: {env_key[:10]}...{env_key[-4:]}")
else:
    st.warning("⚠️ Not found in environment")

# Check Streamlit secrets
st.write("**Streamlit Secrets Check:**")
try:
    secrets_key = st.secrets["OPENROUTER_API_KEY"]
    st.success(f"✅ Found in secrets: {secrets_key[:10]}...{secrets_key[-4:]}")
except Exception as e:
    st.error(f"❌ Not found in secrets: {str(e)}")

# Final result
final_key = env_key or (st.secrets.get("OPENROUTER_API_KEY") if hasattr(st, 'secrets') else None)
if final_key:
    st.success("🚀 FluentBot should work! API key is available.")
    
    # Test backend import
    try:
        from backend import get_chat_response
        st.success("✅ Backend imported successfully")
        
        # Test API call
        if st.button("Test API Call"):
            try:
                response = get_chat_response("Hello, test message")
                st.success("✅ API call successful!")
                st.write("Response preview:", response[:100] + "...")
            except Exception as e:
                st.error(f"❌ API call failed: {str(e)}")
                
    except Exception as e:
        st.error(f"❌ Backend import failed: {str(e)}")
else:
    st.error("❌ No API key found. FluentBot won't work until you add the key.")

st.markdown("---")
st.markdown("**Instructions:**")
st.markdown("1. Add your OpenRouter API key to Streamlit Cloud secrets")
st.markdown("2. Format: `OPENROUTER_API_KEY = \"your_key_here\"`")
st.markdown("3. Reboot the app")
st.markdown("4. Get your key at: https://openrouter.ai/")
