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


query_prompt = PromptTemplate(
    template="""
Generate a google search query on the basis of the following user query:

{input}
    
Use the following chat history as a guide to respond:
{context}

It should be as precise as possible
Response:
""",
    input_variables=["input", "context"],
)

query_chain: RunnableSequence = (
    query_prompt
    | llm
    | StrOutputParser()
    | RunnableLambda(lambda x: x.strip().lower())
)
