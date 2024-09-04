import os
from dotenv import load_dotenv

from langchain import hub

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from sentence_transformers import util

from src.models import GenModel

load_dotenv()

def get_rag_pipeline(gen_config, 
                     retriever): 
    
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)
    
    prompt = hub.pull("rlm/rag-prompt")
    llm = GenModel.from_pretrained(provider=gen_config['provider'], 
                                   config=gen_config['settings'])
    
    rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
    )
    return rag_chain

def image_sim(model, query, img_emb, k=3):
    # First, we encode the query (which can either be an image or a text string)
    query_emb = model.encode([query], convert_to_tensor=True, show_progress_bar=False)
    
    # Then, we use the util.semantic_search function, which computes the cosine-similarity
    # between the query embedding and all image embeddings.
    hits = util.semantic_search(query_emb, img_emb, top_k=k)[0]
    
    return hits