from langchain_google_genai import GoogleGenerativeAI


def get_llm(temperature=0.2, max_tokens=100):
    return GoogleGenerativeAI(
        model="gemini-1.0-pro", max_tokens=max_tokens, temperature=temperature
    )
