"""
Objects in this file is in charge of two things: 
    1. Digesting document.
    2. Embedding data with relevant model. 
    3. Store data with relevant vector database. 

"""

import glob
from PIL import Image
import faiss

from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from src.base import BaseLoader
from src.embedding import EmbeddingModel, VisionModel

class DocLoader(BaseLoader): 

    def __init__(self, config): 
        super().__init__(config=config)

    def loading_data(self, payload):
        loader = TextLoader(str(payload))
        text_documents = loader.load()
        print(text_documents)
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=self.config['chunk_size'], 
                                                    chunk_overlap=self.config['chunk_overlap'])
        documents = text_splitter.split_documents(text_documents)
        return documents
    
    def set_embedding(self, config):
        emb_model = EmbeddingModel.from_pretrained(provider=config['provider'], 
                                                   config=config['settings'])
        return emb_model
    
    def set_vectordb(self, payload, config):
        from langchain_community.vectorstores import Chroma
        embedding_model = self.set_embedding(config=self.config['embedding'])
        vectorstore = Chroma.from_documents(
            documents=payload,
            collection_name="rag-chroma",
            embedding=embedding_model,
            persist_directory="./chroma_db"
        )
        return vectorstore
    
    def set_retrieval(self, vectorstore):
        retriever = vectorstore.as_retriever()
        return retriever
    
    def get_pipeline(self, payload, config):
        loaded_data = self.loading_data(payload=payload)
        vectorstore = self.set_vectordb(loaded_data, config)
        retriever = self.set_retrieval (vectorstore)
        return retriever
    
class ImageLoader(BaseLoader):

    def __init__(self, config): 
        super().__init__(config=config)

    def loading_data(self, payload):
        """
            Check if the payload is a list of frames or a dir contains frames
        """
        if isinstance(payload, list):
            data = [Image.fromarray(p) for p in payload]
        else: 
            img_names = list(glob.glob(f"./{payload}/**.jpg"))

            data = [Image.open(p) for p in img_names]
        return data
    
    def set_embedding(self, config):
        embedding_model = VisionModel.from_pretrained(provider=None,
                                                      config=config['model'])
        return embedding_model
    
    def set_vectordb(self, payload, config):
        embedding_model = self.set_embedding(config)
        img_emb = embedding_model.encode(payload, 
                                         batch_size=config['batch_size'], 
                                         convert_to_tensor=config['convert_to_tensor'])
        return img_emb
    
    def set_retrieval(self, vectorstore):
        # TODO: Store in FAISS
        return super().set_retrieval(vectorstore)
    

    def get_pipeline(self, payload, config):
        config = config['settings']
        loaded_data = self.loading_data(payload=payload)
        vectorstore = self.set_vectordb(loaded_data, config)
        return vectorstore