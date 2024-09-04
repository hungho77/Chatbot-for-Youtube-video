from typing import Dict
from langchain.pydantic_v1 import BaseModel, validator
from pytubefix.captions import Caption

class Media(BaseModel): 
    name: str

class YoutubeMedia(Media): 
    author: str
    description: str
    length: int             # in second
    thumbnail_url: str
    channel_url: str
    age_retricted: bool
    captions_lang: Dict[str, str]

    @validator('captions_lang',  pre=True, allow_reuse=True)
    @classmethod
    def convert_to_dict(cls, caption_tracks: list[Caption]): 
        caption_lang = {}
        for caption in caption_tracks: 
            caption_lang[caption.name] = caption.code

        return caption_lang
    
class MP4Media(Media): 
    
    @validator('name', pre=True, allow_reuse=True)
    @classmethod
    def extract_filename(cls, payload): 
        """
            Assume the almost mp4 file is : ../../NAME.mp4
        """
        payload = payload.split('/')[-1] 
        payload = payload.split('.')[0]
        return payload