# AI Chatbot

A LangChain-powered chatbot built with Streamlit and Google Gemini, demonstrating **RunnableBranch**, **RunnableParallel**, and **Pydantic Structured Output**.

## Features

- **Dynamic Routing** — Routes queries to domain-specific prompts (Programming, Math, General) using `RunnableBranch`
- **Parallel Execution** — Generates a structured answer and summary simultaneously using `RunnableParallel`
- **Structured Output** — Validates responses with `Pydantic` schema (`answer`, `confidence`, `category`, `keywords`)

## Tech Stack

- [LangChain](https://python.langchain.com/)
- [Google Gemini](https://ai.google.dev/)
- [Streamlit](https://streamlit.io/)
- [Pydantic](https://docs.pydantic.dev/)

## Project Structure

```
app.py       # Streamlit UI
chatbot.py   # LangChain pipeline (RunnableBranch, RunnableParallel)
prompts.py   # Prompt templates
schemas.py   # Pydantic schema
```

## Setup

1. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

2. Create a `.env` file and add your API key:

    ```
    GOOGLE_API_KEY=your_key_here
    ```

3. Run the app:

    ```bash
    streamlit run app.py
    ```

## How to Use

| Intent      | Example Prompt                                |
| ----------- | --------------------------------------------- |
| Programming | `Write a Python function to reverse a string` |
| Math        | `Solve: 2x + 5 = 15`                          |
| General     | `What is machine learning?`                   |
