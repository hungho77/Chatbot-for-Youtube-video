from src.base import BaseFoundationModel

class GenModel(BaseFoundationModel): 
    @staticmethod
    def from_pretrained(provider, config): 
        if provider == 'gemini': 
            try:
                from langchain_google_genai import ChatGoogleGenerativeAI
            except ImportError as e: 
                raise e
            return ChatGoogleGenerativeAI(**config)
        elif provider == "ollama": 
            try:
                from langchain_community.chat_models import ChatOllama
            except ImportError as e: 
                raise e
            return ChatOllama(**config)
        elif provider == "groq": 
            try:
                from langchain_groq import ChatGroq
            except ImportError as e: 
                raise e
            return ChatGroq(**config)
        elif provider == "openai": 
            try:
                from langchain_openai import ChatOpenAI
            except ImportError as e: 
                raise e
            return ChatOpenAI(**config)
        else: 
            return None