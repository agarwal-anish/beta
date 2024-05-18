import streamlit as st
import requests

# App title
st.set_page_config(page_title="🦙💬 Llama 3 Chatbot")

# Define llm based on the selected model
selected_model = 'Llama3-7B'  # You can change this to the desired default model
model_mapping = {
    'Llama3-7B': 'llama3-7b',
    'Llama3-13B': 'llama3-13b',
    'Llama3-70B': 'llama3-70b'
}
llm = model_mapping[selected_model]

# Function for generating LLaMA3 response
def generate_llama3_response(prompt_input, string_dialogue, temperature, top_p, max_length):
    # Prepare the dialogue history
    dialogue_history = ""
    for dict_message in string_dialogue:
        if dict_message["role"] == "user":
            dialogue_history += "User: " + dict_message["content"] + "\n\n"
        else:
            dialogue_history += "Assistant: " + dict_message["content"] + "\n\n"

    # Make a request to your Llama 3 API endpoint
    api_endpoint = "https://your-llama3-api.com/generate"
    headers = {"Authorization": f"Bearer {your_api_token}", "Content-Type": "application/json"}
    payload = {
        "model": llm,
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

# Generate a new response if the last message is not from the assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.spinner("Thinking..."):
        response = generate_llama3_response(prompt, st.session_state.messages, temperature, top_p, max_length)
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.write(response)
