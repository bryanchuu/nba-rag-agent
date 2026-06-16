import streamlit as st
from rag_agent import create_nba_agent

@st.cache_resource
def load_agent():
    return create_nba_agent()

agent, config = create_nba_agent()

st.title('NBA Chat Agent 🏀', text_alignment='center')

# Initialise chat history
if 'messages' not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])


prompt = st.chat_input('Ask something related to NBA players!')

if prompt:
    with st.chat_message('user'):
        st.markdown(prompt)
    st.session_state.messages.append({'role': 'user', 'content': prompt})

    # Build list of all messages so the agent remembers the full conversation
    all_messages = []
    for message in st.session_state.messages:
        all_messages.append((message ["role"], message ["content"]))

    response = agent.invoke({"messages": all_messages}, config=config)
    answer = (response["messages"][-1].content)
    with st.chat_message("assistant"):
        st.markdown(answer)
    st.session_state.messages.append({'role': 'assistant', 'content': answer})

