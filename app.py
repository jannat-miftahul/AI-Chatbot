import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os

load_dotenv()

st.set_page_config(page_title="AI Chatbot")

st.title("AI Chatbot Version: 1.0")
st.markdown("LangChain Chatbot using RunnableBranch & RunnableParallel")

model = ChatGoogleGenerativeAI(model="gemini-3.7-flash")


if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display chat messages 
for msg in st.session_state.chat_history:
    role = "assistant" if isinstance(msg, AIMessage) else "user"
    with st.chat_message(role):
        st.write(msg.content)

# Display chat history
with st.sidebar:
    st.header("Chat History")
    if not st.session_state.chat_history:
        st.write("(empty)")
    else:
        for msg in st.session_state.chat_history:
            role = "AI" if isinstance(msg, AIMessage) else "Human"
            st.markdown(f"**{role}:** {msg.content}")
            
    if st.button("Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()

user_input = st.chat_input("Type your message here...")

if user_input:
    if user_input.strip().lower() == 'exit':
        st.stop()

    st.session_state.chat_history.append(HumanMessage(content=user_input))
    with st.chat_message("user"):
        st.write(user_input)

    with st.spinner("Thinking..."):
        try:
            chain = model | StrOutputParser()
            result = chain.invoke(st.session_state.chat_history)
            
            st.session_state.chat_history.append(AIMessage(content=result))
            with st.chat_message("assistant"):
                st.write(result)
                
        except Exception as e:
            st.error(f"Failed to generate response. Please check your connection or API key. Error: {e}")
