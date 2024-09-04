from src.base import BaseFoundationModel

class VisionModel(BaseFoundationModel): 

    @staticmethod
    def from_pretrained(provider, config): 
        from sentence_transformers import SentenceTransformer

        model = SentenceTransformer(model_name_or_path=config)
        return model
    
class EmbeddingModel(BaseFoundationModel): 
    @staticmethod
    def from_pretrained(provider, config): 
        if provider == 'gemini': 
            try:
                from langchain_google_genai import GoogleGenerativeAIEmbeddings
            except ImportError as e: 
                raise e
            return GoogleGenerativeAIEmbeddings(**config)
        elif provider == "ollama": 
            try:
                from langchain_community.embeddings import OllamaEmbeddings
            except ImportError as e: 
                raise e
            return OllamaEmbeddings(**config)
        elif provider == "openai": 
            try:
                from langchain_openai import OpenAIEmbeddings
            except ImportError as e: 
                raise e
            return OpenAIEmbeddings(**config)
        else: 
            return None