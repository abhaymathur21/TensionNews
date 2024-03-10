from typing import Literal

from chatbot.llm import get_llm
from langchain.output_parsers.pydantic import PydanticOutputParser
from langchain.prompts import PromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnableLambda, RunnableSequence
from langchain_core.pydantic_v1 import BaseModel

llm = get_llm(max_tokens=10)


class Classification(BaseModel):
    classification: Literal["yes", "no"]
    "Classification of the input text as an event. Either 'yes' or 'no'."


parser = PydanticOutputParser(pydantic_object=Classification)


classify_prompt = PromptTemplate(
    template="""
Classify the input as one of the operations below:

{input}
    
Use the following chat history as a guide to respond:
{context}

Options:
- SEARCH: Search for a specific topic
- HELP: Request for assistance
- GENERAL: General conversation

Response:
""",
    input_variables=["input", "context"],
)

classify_chain: RunnableSequence = (
    classify_prompt
    | llm
    | StrOutputParser()
    | RunnableLambda(lambda x: x.strip().lower())
)
