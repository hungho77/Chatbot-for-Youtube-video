import os
from typing import Union, Any, List
from abc import ABC, abstractmethod

import cv2

class BaseFoundationModel(ABC): 

    @staticmethod
    @abstractmethod
    def from_pretrained(provider, config): 
        ...

class BaseMediaReader(ABC): 
    SUPPORTED_FORMAT= {
        "URL": ["https://www.youtube.com/watch?"], 
        "MEDIA": ["mp4", "MP4"]
    }


    def __init__(self, 
                lang:str='en',  # Get caption based on language
                to_local_dir: Union[str, None]='./storage', # Save to local dir
                save_frames:bool=True, 
                save_document:bool=True): 
        self.lang = lang

        if to_local_dir is not None:
            if not os.path.exists(to_local_dir): 
                os.makedirs(to_local_dir)

            self.to_local_dir = to_local_dir
        else: 
            self.to_local_dir = './'

        self.save_frames = save_frames
        self.save_document = save_document

    @abstractmethod
    def get_metadata(self, payload): 
        ...

    @abstractmethod
    def get_audio(self, payload): 
        ...

    @abstractmethod
    def get_transcript(self, payload) -> str: 
        ...

    @abstractmethod
    def lazy_read(self, payload): 
        ...

    def get_frames(self, 
                   payload, 
                   selected_points:Union[List[int], None]=None, 
                   time_interval:int=1,
                   ): 
    
        frames = []
        points = selected_points
        cap = cv2.VideoCapture(payload)

        # Used as counter variable 
        match points:
            case None: 
                while True:
                    
                    ret, frame = cap.read()
                    if not ret:
                        break

                    # Calculate the current timestamp (assuming FPS = 30)
                    timestamp = int(cap.get(cv2.CAP_PROP_POS_MSEC) / 1000)

                    # Check if the current timestamp matches the desired interval
                    if timestamp % time_interval == 0:
                            frames.append(frame)

            case List:
                while True:
                    
                    ret, frame = cap.read()
                    if not ret:
                        break

                    # Calculate the current timestamp (assuming FPS = 30)
                    timestamp = int(cap.get(cv2.CAP_PROP_POS_MSEC) / 1000)

                    # Check if the current timestamp matches the desired interval and selected_points
                    if timestamp % time_interval == 0:
                        try: 
                            now = points[0]
                            if timestamp == now: 
                                frames.append(frame)
                                points.pop(0)
                        except: 
                            break
        return frames     
    
class BaseLoader(ABC): 

    def __init__(self, 
                config,
                to_local_dir: Union[str, None]='./storage', # Save to local dir
                  ): 
        self.config = config

        if to_local_dir is not None:
            if not os.path.exists(to_local_dir): 
                os.makedirs(to_local_dir)

            self.to_local_dir = to_local_dir
        else: 
            self.to_local_dir = './'

    @abstractmethod
    def set_vectordb(self, payload, config): 
        ...

    # def get_vectordb(self): 
    #     ...

    @abstractmethod
    def set_retrieval(self, vectorstore): 
        ...

    @abstractmethod
    def loading_data(self, payload): 
        ...

    @abstractmethod
    def set_embedding(self, config): 
        ...

    @abstractmethod
    def get_pipeline(self, payload, config): 
        ...
