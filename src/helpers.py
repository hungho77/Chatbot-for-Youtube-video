from typing import Union

def get_model_tokens(provider:Union[str, None]=None): 
    models_tokens = {
        "openai": {
            "gpt-3.5-turbo-0125": 16385,
            "gpt-3.5": 4096,
            "gpt-3.5-turbo": 16385,
            "gpt-3.5-turbo-1106": 16385,
            "gpt-3.5-turbo-instruct": 4096,
            "gpt-4-0125-preview": 128000,
            "gpt-4-turbo-preview": 128000,
            "gpt-4-turbo": 128000,
            "gpt-4-turbo-2024-04-09": 128000,
            "gpt-4-1106-preview": 128000,
            "gpt-4-vision-preview": 128000,
            "gpt-4": 8192,
            "gpt-4-0613": 8192,
            "gpt-4-32k": 32768,
            "gpt-4-32k-0613": 32768,
            "gpt-4o": 128000,
            "gpt-4o-mini":128000,

        },
        "gemini": {
            "gemini-pro": 128000,
            "gemini-1.5-flash-latest": 128000,
            "gemini-1.5-pro-latest": 128000,

            # Embedding model
            "models/embedding-001": 2048
        },
        "ollama": { "command-r": 12800, 
                "codellama": 16000, 
                "dbrx": 32768, 
                "deepseek-coder:33b": 16000, 
                "falcon": 2048, 
                "llama2": 4096, 
                "llama3": 8192, 
                "llama3:70b": 8192,
                "llama3.1":128000,
                "llama3.1:70b": 128000,
                "lama3.1:405b": 128000,
                "llava": 4096, 
                "mixtral:8x22b-instruct": 65536, 
                "mistral-openorca": 32000, 
                "nomic-embed-text": 8192, 
                "nous-hermes2:34b": 4096, 
                "orca-mini": 2048, 
                "phi3:3.8b": 12800, 
                "qwen:0.5b": 32000, 
                "qwen:1.8b": 32000, 
                "qwen:4b": 32000, 
                "qwen:14b": 32000, 
                "qwen:32b": 32000, 
                "qwen:72b": 32000, 
                "qwen:110b": 32000, 
                "stablelm-zephyr": 8192, 
                "wizardlm2:8x22b": 65536, 

                # embedding models
                "shaw/dmeta-embedding-zh-small-q4": 8192,
                "shaw/dmeta-embedding-zh-q4": 8192,
                "chevalblanc/acge_text_embedding": 8192,
                "martcreation/dmeta-embedding-zh": 8192,
                "snowflake-arctic-embed": 8192, 
                "mxbai-embed-large": 512 
        },
        
        "groq": {
            "llama3-8b-8192": 8192,
            "llama3-70b-8192": 8192,
            "mixtral-8x7b-32768": 32768,
            "gemma-7b-it": 8192,
            "claude-3-haiku-20240307'": 8192
        },
    }
    if not provider: 
        return models_tokens
    else: 
        return models_tokens['provider']