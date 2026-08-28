from pydantic import BaseModel, Field
from typing import List

class ChatResponse(BaseModel):
    """Response schema for the chatbot's main answer."""
    answer: str = Field(description="The detailed answer to the user's query.")
    confidence: str = Field(description="Confidence level of the answer (e.g., High, Medium, Low).")
    category: str = Field(description="The category of the question (Programming, Math, or General).")
    keywords: List[str] = Field(description="A list of important keywords related to the answer.")
