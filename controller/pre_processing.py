import os
import tempfile

from src.media import YoutubeReader, MP4Reader
from src.loader import DocLoader, ImageLoader

def process_youtube(url): 
    try: 
        yt_reader = YoutubeReader()
        info = yt_reader.lazy_read(url)
        return info
    except Exception: 
        raise Exception

def process_mp4(file): 
    try: 
        mp4_reader = MP4Reader()
        info = mp4_reader.lazy_read(file)
        return info
    except Exception: 
        raise Exception

def get_retriever(payload, loader_config, mode:str='youtube'): 
    match mode: 
        case "youtube": 
            info = process_youtube(payload)

        case "mp4": 
            info = process_mp4(payload)


    text_loader = DocLoader(config=loader_config['text'])
    img_loader = ImageLoader(config=loader_config['image'])
    with tempfile.TemporaryDirectory() as tmp_dir: 
        tmp_filename = os.path.join(tmp_dir, "tempfile.txt")
        with open(tmp_filename, 'w') as f: 
            f.writelines(info['document'])
        text_retriever = text_loader.get_pipeline(payload=tmp_filename, 
                                              config=loader_config['text'])
    img_retriever = img_loader.get_pipeline(payload=info['frames'], 
                                           config=loader_config['image'])
    return {
        "text_retriever": text_retriever, 
        "img_retriever": img_retriever
    }