import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableParallel, RunnableBranch, RunnableLambda
from pydantic import BaseModel, Field
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

# model setup
model = ChatGoogleGenerativeAI(model="gemini-3.7-flash")
parser = StrOutputParser()


# pydantic schema
class JobApplication(BaseModel):
    name: str = "Unknown"
    experience: Optional[int] = None
    skills: str = Field(description="Key skills mentioned by the candidate")
    expected_role: str = Field(description="The job role the candidate is applying for")

structured_model = model.with_structured_output(JobApplication)


# parallel chain - summary + questions
prompt_summary = PromptTemplate(
    template="Summarize the following text in 3 short lines:\n{input}",
    input_variables=["input"]
)
prompt_questions = PromptTemplate(
    template="Write 3 simple questions from the following text:\n{input}",
    input_variables=["input"]
)

parallel_chain = RunnableParallel(
    {
        "Summary": prompt_summary | model | parser,
        "Questions": prompt_questions | model | parser
    }
)


# general conversation chain
general_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI assistant."),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}")
])
general_chain = general_prompt | model | parser


# classifier chain
classify_prompt = PromptTemplate(
    template=(
        "Classify the user's intent into ONE word:\n"
        "- 'analyze' (wants summary or questions about a text)\n"
        "- 'extract' (wants to extract job/resume info)\n"
        "- 'general' (anything else)\n\n"
        "User input: {input}"
    ),
    input_variables=["input"]
)
classifier_chain = classify_prompt | model | parser


# RunnableBranch router
branch = RunnableBranch(
    (
        lambda x: "analyze" in x["topic"].lower(),
        RunnableLambda(lambda x: (
            lambda r: f"**Summary:**\n{r['Summary']}\n\n**Questions:**\n{r['Questions']}"
        )(parallel_chain.invoke({"input": x["input"]}))
        )
    ),
    (
        lambda x: "extract" in x["topic"].lower(),
        RunnableLambda(lambda x: (
            lambda r: f"**Extracted Job Application:**\n\n- **Name:** {r.name}\n- **Experience:** {r.experience} years\n- **Skills:** {r.skills}\n- **Expected Role:** {r.expected_role}"
        )(structured_model.invoke(x["input"]))
        )
    ),
    RunnableLambda(lambda x: general_chain.invoke({
        "input": x["input"],
        "chat_history": x["chat_history"]
    }))
)


# streamlit UI
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
            topic = classifier_chain.invoke({"input": user_input})

            result = branch.invoke({
                "topic": topic,
                "input": user_input,
                "chat_history": st.session_state.chat_history
            })

            st.session_state.chat_history.append(AIMessage(content=result))
            with st.chat_message("assistant"):
                st.markdown(result)

        except Exception as e:
            st.error(f"Failed to generate response. Please check your connection or API key. Error: {e}")
