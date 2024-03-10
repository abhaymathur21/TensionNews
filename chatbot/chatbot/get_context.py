from langchain.prompts import PromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnableSequence

from chatbot.llm import get_llm

llm = get_llm()

context_prompt = PromptTemplate(
    template="""
You are a chatbot that can perform various operations on a web app about business and finance news analysis.
You should highlight the most important information relevant to the user's query.

chat history:
{history}

Latest message from user:
{input}

The response should be in short 1-3 sentences.
It should summarize the context of the conversation and the user's intention.
It should highlight the most important information relevant to the user's query.
Response:                   
""",
    input_variables=["input", "history"],
)

context_chain: RunnableSequence = context_prompt | llm | StrOutputParser()
