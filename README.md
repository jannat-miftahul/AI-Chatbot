# AI Chatbot

A LangChain-powered chatbot built with Streamlit and Google Gemini, demonstrating **RunnableBranch**, **RunnableParallel**, and **Pydantic Structured Output**.

## Features

- **General Chat** — Conversational AI with memory
- **Text Analysis** — Generates a summary and questions in parallel using `RunnableParallel`
- **Info Extraction** — Extracts structured job application data using Pydantic via `RunnableBranch`

## Tech Stack

- [LangChain](https://python.langchain.com/)
- [Google Gemini](https://ai.google.dev/)
- [Streamlit](https://streamlit.io/)
- [Pydantic](https://docs.pydantic.dev/)

## Setup

1. Clone the repo and install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

2. Create a `.env` file and add your API key:

    ```
    GEMINI_API_KEY=your_key_here
    ```

3. Run the app:
    ```bash
    streamlit run app.py
    ```

## How to Use

| Intent       | Example Prompt                                                                       |
| ------------ | ------------------------------------------------------------------------------------ |
| General chat | `What is machine learning?`                                                          |
| Analyze text | `Analyze this: Deep learning is a subset of ML...`                                   |
| Extract info | `Extract: My name is Arif, 3 years ML experience, applying for Data Scientist role.` |
