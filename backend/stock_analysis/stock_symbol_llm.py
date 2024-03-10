from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
import os

from dotenv import load_dotenv

load_dotenv('.env')
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

llm = ChatGoogleGenerativeAI(model="gemini-pro")

def llm_stock_symbol(company):
    
    input_data = {
        "company": company,
    }
    
    prompt = [
        """
        Give me the stock symbol for the company: {company}
        
        Example: "AAPL" for Apple Inc.
        Give output in a single string format.
        
        """
    ]

    template = PromptTemplate(
            template=prompt[0],
            input_variables=[
                "company",
            ],
        )

    chain = template | llm | StrOutputParser()

    result = chain.invoke(input_data)
    print(result)
    
    return result

result = llm_stock_symbol("Tata Sons")
print(result)