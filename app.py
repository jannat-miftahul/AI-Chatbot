import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from chatbot import generate_response

st.set_page_config(page_title="AI Chatbot")

st.title("AI Chatbot Version: 1.0")
st.markdown("LangChain Chatbot using RunnableBranch & RunnableParallel")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# display chat messages
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
            content = msg.content if isinstance(msg.content, str) else "Structured Output"
            st.markdown(f"**{role}:** {content[:80]}...")
            
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
            result = generate_response(user_input)
            
            main_answer = result["main_answer"]
            summary = result["summary"]
            
            formatted_response = (
                f"**Answer:**\n{main_answer.answer}\n\n"
                f"---\n"
                f"**Summary:** {summary}\n"
                f"**Category:** {main_answer.category} | **Confidence:** {main_answer.confidence}\n"
                f"**Keywords:** {', '.join(main_answer.keywords)}"
            )
            
            st.session_state.chat_history.append(AIMessage(content=formatted_response))
            with st.chat_message("assistant"):
                st.markdown(formatted_response)
                
        except Exception as e:
            st.error(f"Failed to generate response. Please check your connection or API key. Error: {e}")
