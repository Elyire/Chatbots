
from itertools import zip_longest
import streamlit as st
from langchain_openai.chat_models import ChatOpenAI
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)


# Side bar
with st.sidebar:
   
    api_key_input = st.text_input(
    "OpenAI API Key를 입력해 주세요", 
    key="chatbot_api_key", 
    type="password",
    value=st.session_state.get("OPENAI_API_KEY", "YOUR_TEMP_API_KEY"),
    )

    ":green[OpenAI API Key가 없으시다면, [**챗GPT의 개발사인 OpenAI의 홈페이지**](https://platform.openai.com/account/api-keys)에서 발급받으실 수 있습니다.]"

    st.write("---")
    st.caption('오른쪽 상단 X를 누르면 사이드바가 들어갑니다')



st.title("simple chatbot")


# Initialize session state variables
if 'generated' not in st.session_state:
    st.session_state['generated'] = []  # Store AI generated responses

if 'past' not in st.session_state:
    st.session_state['past'] = []  # Store past user inputs



# TRY EXCEPT FOR KEY VALIDATION
try:
    # Initialize the ChatOpenAI model
    chat = ChatOpenAI(
        openai_api_key=api_key_input,
        model_name="gpt-4o",
        temperature=0,
        max_tokens=4000,
    )


    def build_message_list():
        """
        Build a list of messages including system, human and AI messages.
        """
        # Start zipped_messages with the SystemMessage
        zipped_messages = [SystemMessage(
            content="""
            You are a helpful assistant.
            """)]

        # Zip together the past and generated messages
        for human_msg, ai_msg in zip_longest(st.session_state['past'], st.session_state['generated']):
            if human_msg is not None:
                zipped_messages.append(HumanMessage(
                    content=human_msg))  # Add user messages
            if ai_msg is not None:
                zipped_messages.append(
                    AIMessage(content=ai_msg))  # Add AI messages

        return zipped_messages


    def generate_response():
        """
        Generate AI response using the ChatOpenAI model.
        """
        # Build the list of messages
        zipped_messages = build_message_list()

        # Generate response using the chat model
        ai_response = chat(zipped_messages)

        return ai_response.content




    if not api_key_input or api_key_input == "YOUR_TEMP_API_KEY":
        st.error("**계속 진행하기 위해서는 👈사이드바에 OpenAI API key를 입력해 주세요**")
        st.stop()


    entered_prompt = st.chat_input('메시지 입력', key='prompt_input')


    with st.spinner('대화 생성 중..⏳'):
        if entered_prompt:        
            # Get user query
            user_query = entered_prompt
            # Append user query to past queries
            st.session_state.past.append(user_query)
            # Generate response
            output = generate_response()
            # Append AI response to generated responses
            st.session_state.generated.append(output)


    #Display the chat history
    if st.session_state['generated']:
        for human_msg, ai_msg in zip(st.session_state['past'], st.session_state['generated']):
            with st.chat_message("user"):
                st.markdown(f"**You:** {human_msg}", unsafe_allow_html=True)
            with st.chat_message("ai"):
                st.markdown(f"**Assistant:** {ai_msg}", unsafe_allow_html=True)

except:
    st.error("유효한 API KEY를 넣어주세요")


