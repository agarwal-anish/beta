import streamlit as st
import requests

# App title
st.set_page_config(page_title="🦙💬 Llama 3 Chatbot")

# Function for generating LLaMA3 response
def generate_llama3_response(prompt_input, string_dialogue, llm, temperature, top_p, max_length):
    # Prepare the dialogue history
    dialogue_history = ""
    for dict_message in string_dialogue:
        if dict_message["role"] == "user":
            dialogue_history += "User: " + dict_message["content"] + "\n\n"
        else:
            dialogue_history += "Assistant: " + dict_message["content"] + "\n\n"

    # Make a request to your Llama 3 API endpoint
    api_endpoint = "https://your-llama3-api.com/generate"
    headers = {"Authorization": f"Bearer {r8_DGy0l9PV88MnLqZxdpCgsboWhPDcQKI3IgPyW}", "Content-Type": "application/json"}
    payload = {
        "prompt": dialogue_history + prompt_input + " Assistant:",
        "temperature": temperature,
        "top_p": top_p,
        "max_length": max_length
    }
    response = requests.post(api_endpoint, headers=headers, json=payload)

    # Check if the request was successful
    if response.status_code == 200:
        return response.json()["output"]
    else:
        return "Error: Failed to generate response from Llama 3 API"

# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

# Display or clear chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
st.button('Clear Chat History', on_click=clear_chat_history)

# User-provided prompt
if prompt := st.text_input('Enter your message here:', key='user_input'):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Function to generate a response
def generate_response(prompt):
    if st.session_state.messages[-1]["role"] == "assistant":
        dialogue_history = st.session_state.messages[:-1]
    else:
        dialogue_history = st.session_state.messages

    # Generate response using Llama 3
    response = generate_llama3_response(prompt, dialogue_history, llm, temperature, top_p, max_length)

    return response

# Generate a new response if the last message is not from the assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.spinner("Thinking..."):
        response = generate_response(prompt)
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.write(response)
