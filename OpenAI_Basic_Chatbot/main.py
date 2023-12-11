from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
import streamlit as st


st.title("💬 Basic Chatbot")
st.caption("developed using OpenAI library")


client = OpenAI()

system_prompt_content = '''
You are a helpful assistance.
'''

# Setting system prompts, for conversation context, not visible in the user UI
system_prompt = {"role" : "system", "content" : system_prompt_content}


# If 'messages' does not exist in the session state, initialize it. Include the system prompt here.
if 'messages' not in st.session_state:
    st.session_state['messages'] = [system_prompt]


# Displaying older messages in the user interface
for msg in st.session_state['messages']:
    if msg["role"] != "system":
        st.chat_message(msg['role']).write(msg['content'])


# Processing user input
if prompt := st.chat_input():
    # Adding a user message to the session state
    st.session_state['messages'].append({'role' : 'user', 'content' : prompt})
    st.chat_message('user').write(prompt)


    # Using the OPENAI model to generate responses
    completion = client.chat.completions.create(
        model = "gpt-3.5-turbo-1106",
        messages = st.session_state['messages']
        )

    print(completion)

    # Extracting response messages
    output = completion.choices[0].message

    # Adding AI responses to session state and display them in the user interface
    st.session_state['messages'].append({"role" : "assistant", "content" : output.content})
    st.chat_message("assistant").write(output.content)

print(st.session_state)
