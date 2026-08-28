from langchain_core.prompts import PromptTemplate

classifier_prompt = PromptTemplate(
    template=(
        "Classify the user's intent into ONE word: 'programming', 'math', or 'general'.\n\n"
        "User input: {input}"
    ),
    input_variables=["input"]
)

programming_prompt = PromptTemplate(
    template="You are an expert Programming Assistant. Answer the following programming question clearly and concisely.\n\nQuestion: {input}",
    input_variables=["input"]
)

math_prompt = PromptTemplate(
    template="You are a Math Tutor. Solve the following math problem step-by-step.\n\nProblem: {input}",
    input_variables=["input"]
)

general_prompt = PromptTemplate(
    template="You are a General Assistant. Answer the following question politely.\n\nQuestion: {input}",
    input_variables=["input"]
)

summary_prompt = PromptTemplate(
    template="Provide a very brief 1-sentence summary/answer for the following query:\n\nQuery: {input}",
    input_variables=["input"]
)
