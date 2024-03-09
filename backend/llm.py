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

def llm_response(title, link_to_article, snippet, tags, source):
    
    input_data = {
        "title": title,
        "link_to_article": link_to_article,
        "snippet": snippet,
        "tags": tags,
        "source": source,
    }
    
    prompt = [
        """
        Data:
        Title of the News: {title}
        Link to the News Article: {link_to_article}
        A small summary of the News Article: {snippet}
        Source of the News Article: {source}
        
        Given the above data, I want you to figure out the city this news is from and the company it is about.
        
        If you dont think it is about a company, replace company with the word "None" in the output format given below.
        If you can't figure out which city the news is from, try and figure out which country is from and give the name of the country.
        
        If you can't figure out the country, replace location with the word "None" in the output format given below.
        Give your output in a single string format: "company; location"
        
        If you think multiple companies are involved, give multiple values separated by commas as company.
        If you think multiple cities or countries are involved, give multiple values separated by commas as location.
        
        """
    ]

    template = PromptTemplate(
            template=prompt[0],
            input_variables=[
                "title",
                "link_to_article",
                "snippet",
                "tags",
                "source",
            ],
        )

    chain = template | llm | StrOutputParser()

    result = chain.invoke(input_data)
    # print(result)
    
    company, location = map(str.strip, result.split(';'))
    
    return (company, location)

# sample_data = {
#         "position": 3,
#         "link": "https://www.livemint.com/market/stock-market-news/dividend-stocks-sbi-life-insurance-iifl-securities-among-others-to-trade-ex-dividend-next-week-check-full-list-11709924677208.html",
#         "title": "Dividend Stocks: SBI Life Insurance, IIFL Securities, among others to trade ex-dividend next week; check full list | Mint",
#         "source": "mint",
#         "date": "38 minutes ago",
#         "snippet": "Dividend Stocks: Shares of several companies, including Wonder Electricals, \nISMT Ltd and others will trade ex-dividend in the coming week,...",
#         "thumbnail": "https://serpapi.com/searches/65ec54b0eb690f0ac9d90113/images/96d3aaa266e5f38fe8e4ad72ce12474948a7c81f40742e86fb1174852ba3508b.jpeg"
#     }

# company, location = llm_response(sample_data)

# print(company,"+",location)