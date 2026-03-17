import streamlit as st
import requests

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="AI Policy Hub", page_icon="🏛️", layout="centered")

st.title("🏛️ AI Policy Hub Agent")
st.write("Ask any questions about policies, and the AI agent will assist you.")

# URL of your Render backend
API_URL = "https://gov-ai-backend-frt0.onrender.com/ask"

# --- SESSION STATE INITIALIZATION ---
# This keeps track of the chat history so it doesn't disappear when the page reloads
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- CHAT INPUT & API CALL ---
# st.chat_input creates the text box at the bottom of the screen
if prompt := st.chat_input("Ask a policy question..."):
    
    # 1. Display user's prompt in the UI
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # 2. Add user's prompt to session state
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 3. Call your Render Backend and display the AI's response
    with st.chat_message("assistant"):
        with st.spinner("The AI is thinking..."):
            try:
                # MAKE SURE: "query" matches what your backend expects (could be "message", "prompt", etc.)
                payload = {"query": prompt} 
                response = requests.post(API_URL, json=payload, timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    # MAKE SURE: "answer" matches what your backend returns (could be "response", "reply", etc.)
                    ai_response = data.get("answer", data.get("response", str(data)))
                else:
                    ai_response = f"⚠️ Server returned an error: {response.status_code}. Is the Render server awake?"
            
            except requests.exceptions.Timeout:
                ai_response = "⚠️ Request timed out. The Render server might be waking up from sleep mode (takes ~50 seconds)."
            except Exception as e:
                ai_response = f"⚠️ Connection error: {e}"
            
            # Display the AI response
            st.markdown(ai_response)
            
    # 4. Add the AI's response to session state history
    st.session_state.messages.append({"role": "assistant", "content": ai_response})
