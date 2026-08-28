from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableBranch, RunnableParallel

from schemas import ChatResponse
from prompts import (
    classifier_prompt,
    programming_prompt,
    math_prompt,
    general_prompt,
    summary_prompt
)

load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-3.5-flash")
parser = StrOutputParser()

structured_model = model.with_structured_output(ChatResponse)

classifier_chain = classifier_prompt | model | parser

# RunnableBranch
prompt_branch = RunnableBranch(
    (lambda x: "programming" in x["topic"].lower(), programming_prompt),
    (lambda x: "math" in x["topic"].lower(), math_prompt),
    general_prompt
)

# RunnableParallel
parallel_chain = RunnableParallel(
    main_answer=prompt_branch | structured_model,
    summary=summary_prompt | model | parser
)


def generate_response(user_input: str):
    """Processes the user input through the full LangChain pipeline."""
    
    topic = classifier_chain.invoke({"input": user_input})
    
    result = parallel_chain.invoke({
        "topic": topic,
        "input": user_input
    })
    
    return result
