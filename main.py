import os 
from dotenv import load_dotenv
import requests

from PIL import Image
import streamlit as st

from controller.pre_processing import get_retriever
from controller.features import get_rag_pipeline, image_sim

from src.embedding import VisionModel
from src.utils import read_yaml

load_dotenv()
config = read_yaml('./config.yaml')
loader_config = config['loader']
gen_config = config['gen_model']
os.environ['GOOGLE_API_KEY'] = os.getenv('GEMINI_API_KEY')
os.environ['GROQ_API_KEY'] = os.getenv("GROQ_API_KEY")

embedding_model = VisionModel.from_pretrained(provider=None,
                                                config=loader_config['image']['settings']['model'])

# =====================
# ===== UI DEFINE =====
# =====================

st.header("Video Chat")

# ===== Define input's URL or MP4
if "chatbot_is_ready" not in st.session_state:
    st.session_state.chatbot_is_ready = False



option = st.selectbox(
"How would you like to be contacted?",
("Youtube's URL", ".MP4"),
index=None,
placeholder="Select contact method...",
)

match option:
    case ".MP4": 
        st.info("This function would be back soon! Stay tuned!")
    case "Youtube's URL":
        payload  = st.text_input("Please input valid Youtube Video")
        try: 
            if "youtube" not in payload: 
                st.error("Invalid Youtube's URL")

            with st.status(label="Please wait ..."): 
                retriever = get_retriever(payload, 
                                        loader_config=loader_config)
            st.success("Done!")

            rag = get_rag_pipeline(gen_config=gen_config, 
                                retriever=retriever['text_retriever'])
        except: 
            st.error("Something wrong during the process")

# Chat history
if "history" not in st.session_state:
    st.session_state.history = []
    
# Display chats
for message in st.session_state.history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

#Ask a question
if question := st.chat_input("Ask a question"):
    # Append user question to history
    st.session_state.history.append({"role": "user", "content": question})
    # Add user question
    with st.chat_message("user"):
        st.markdown(question)

    # Answer the question
    answer = rag.invoke(question)
    with st.chat_message("assistant"):
        st.write(answer)
    # Append assistant answer to history
    st.session_state.history.append({"role": "assistant", "content": answer})
