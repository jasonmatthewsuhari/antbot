# Streamlit frontend (Zhuoyang), can use any framework ur comfy with tho!

import streamlit as st
import requests

st.title("Antbot") # name of the bot

user_input = st.text_input("Enter your message:")

if st.button("Send"):
    if user_input:
        # Send message to FastAPI backend
        response = requests.post("http://localhost:8000/chat", json={"message": user_input})
        if response.status_code == 200:
            data = response.json()
            st.write(data["response"])
        else:
            st.error("Failed to get response from backend.")
    else:
        st.warning("Please enter a message.")