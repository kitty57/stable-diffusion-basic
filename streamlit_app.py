import streamlit as st
import requests
import io
from PIL import Image

def query_stabilitydiff(payload, headers):
    API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.content

st.title("💬 Chatbot - Text to Image")
st.caption("🚀 A chatbot that uses Stable Diffusion")
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "What do you want to see? (example: a working women)"}]
for message in st.session_state.messages:
    st.chat_message(message["role"]).write(message["content"])
    if "image" in message:
        st.chat_message("assistant").image(message["image"], caption=message["prompt"], use_column_width=True)
    
if prompt := st.chat_input():

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    headers = {"Authorization": f"Bearer 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"}
    image_bytes = query_stabilitydiff({
        "inputs": prompt,
    }, headers)

    image = Image.open(io.BytesIO(image_bytes))
    msg = f'here is your image related to "{prompt}"'

    st.session_state.messages.append({"role": "assistant", "content": msg, "prompt": prompt, "image": image})
    st.chat_message("assistant").write(msg)
    st.chat_message("assistant").image(image, caption=prompt,width=400)
