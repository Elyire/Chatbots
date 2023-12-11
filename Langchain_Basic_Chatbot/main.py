from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chains import LLMChain
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
import streamlit as st
import time


st.header(':gray[_Langchain Basic Bot_]')
st.caption('powered by OpenAI')

# Initialization
if "messages" not in st.session_state:
    st.session_state.messages = []

for messages in st.session_state.messages:
    with st.chat_message(messages["role"]):
        st.markdown(messages["content"])



# Creating a list to store user and chatbot messages separately
user_inputs = []
ai_responses = []

for msg in st.session_state.messages:
    if msg['role'] == 'user':
        user_inputs.append(msg['content'])
    elif msg['role'] == 'assistant':
        ai_responses.append(msg['content'])



# With an input of user,
if prompt := st.chat_input("your message"):
     
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
     
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        llm = ChatOpenAI(model_name='gpt-3.5-turbo-1106')

        # Prompt
        custom_prompt = ChatPromptTemplate(
            messages=[
                SystemMessagePromptTemplate.from_template(
                    '''You are a nice chatbot having a conversation with a human. Give long answers to user input. 
                    '''
                ),
                MessagesPlaceholder(variable_name="chat_history"),    
                HumanMessagePromptTemplate.from_template("{question}"),
            ]
        )

        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
       
        for user_input, ai_response in zip(user_inputs, ai_responses):
            memory.chat_memory.add_user_message(user_input)
            memory.chat_memory.add_ai_message(ai_response)

        chat_history = memory.load_memory_variables({})['chat_history']

        conversation = LLMChain(llm=llm, prompt=custom_prompt, verbose=True, memory=memory)
        
        result = conversation({"question": prompt})
        
        
        paragraphs = result['text'].split('\n\n')
        for paragraph in paragraphs:
            words = paragraph.split()  
            for word in words:
                full_response += word + " "
                time.sleep(0.05)
                message_placeholder.markdown(full_response.replace('\n\n', '<br><br>') + "▌", unsafe_allow_html=True)
            full_response += '\n\n'  
        message_placeholder.markdown(full_response, unsafe_allow_html=True)
        
    st.session_state.messages.append({"role": "assistant", "content": full_response})

    print(st.session_state)
    print(memory)
