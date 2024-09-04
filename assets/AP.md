# Exercise 1

**Problem Statement:** Build a chabot that can handle videos allowing users search whatever they concern that related to those videos.

**Input:**
+ Youtube's URL. 
+ `.mp4` file.

**Goal:**

- Enhance user's experience. -> Friendly-chat, Speed, (User Interface).

## Features

- Search any specific moments in a video. -> Image, Time
- Chat with video -> Text

## Solutions
The system processes user-provided video URLs (specifically MP4 files and YouTube links). 

+ For YouTube URLs, the video is downloaded (via `pytubefix`) and temporarily stored (via `tempfile`). Metadata like title, author, and URL are extracted, followed by frame extraction. 
+ For direct MP4 files, only frame extraction is performed. 

Captions or transcripts are also obtained to power a Retrieval Augmented Generation (RAG)-based chatbot.


Both the selected frames and the text data go through a similar process: they are transformed into numerical representations (vectors) and then structured for efficient searches (indexed), named as Vector Store. I favor models that offer speed and lightweight while still ensuring quality. I use Vision Transformer for the former format, and Gemini, a third-party tool, for the latter. 

After the user's input video(s) is processed, user's can query for interacting with his/her(them) data: 
+ For image data, the image would be inserted using the Vision Transformer and then searched for similarity in the Vector Store. The user would receive the image that is believed to be the most comparable to the original image.
+ For text data, the flow would be little more complicated. I use two services: Gemini as embedding models and Groq as a third-party LLM provider. The data would be incorporated by the Gemini model, which would look for the most appropriate documents in the Vector Store for text. The relevant documents and the user's inquiry would be loaded into the Groq model to generate the final result. 

_Note:_ 
+ Choice of keyframes: 
    +  **Shot Boundary Detection:** This approach extracts individual shots and selects representative frames within each. While ideal for capturing relevant content, the computational cost of using deep learning models for shot detection proved prohibitive due to my limited GPU resources.
    + **Traditional Keyframe Extraction:** I evaluated two traditional methods:
        * **Fixed Number of Frames:**  This approach risks insufficiently capturing the content of longer videos, potentially missing important shots or key moments.
        * **Fixed Time Interval:** While adaptive to video length, this method can lead to an overwhelming number of frames for longer videos, significantly increasing storage and processing costs.
    + **Chosen appoach:** I implemented a caption-guided fixed time interval approach, specifically for YouTube videos. This method leverages the timestamps associated with captions, assuming minimal scene changes occur within the duration of a single caption.  Therefore, keyframes are extracted at fixed time intervals, ensuring alignment with the caption timestamps.  This approach balances the need for comprehensive coverage with resource constraints.

```
,from,to,content
0,0.0,2.0,I've built a massive isolation chamber
1,3.0,6.0,and we're going to see if these two strangers
2,6.0,9.0,can survive in this cube for the next 100 days.
3,9.0,11.0,They have never met each other ever.
4,11.0,13.0,Bailey. This is Suzie.
5,13.0,15.0,"- Suzie, this is Bailey. - Nice to meet you."
6,15.0,16.0,Hi! Nice to meet you.
7,16.0,19.0,If the two of you can survive the next 100 days in here.
8,19.0,22.0,I will give you the half a million dollars inside of this vault.
9,22.0,26.0,"But if one of you leaves before the 100 days is up, you both get nothing."
10,27.0,29.0,All right. I think you guys understand the rules.
11,29.0,32.0,- Have fun. - Okay. Bye.
12,32.0,34.0,This is going to be crazy.
13,39.0,40.0,Yeah.
14,40.0,42.0,This is actually like an insane asylum.
15,43.0,45.0,They're currently looking at all the stuff we put in there.
16,45.0,46.0,"We gave them enough food for 100 days,"
17,46.0,49.0,"which is healthy, but basically the exact same thing"
18,49.0,50.0,over and over again.
19,50.0,51.0,We also gave them their own
20,51.0,53.0,"private bathroom, which comes with the shower"
21,53.0,56.0,and obviously has no cameras inside and a bed to sleep on.
22,56.0,59.0,They have everything they need to survive 100 days.
23,59.0,61.0,It's just a question of do they want it?
24,61.0,64.0,I got a comb. I don't know if I've ever combed my hair in my life.
25,65.0,66.0,Interesting.
26,66.0,68.0,See how they're both standing on different sides of the room?
27,68.0,69.0,They're so awkward.
28,69.0,71.0,When I had them take their blindfolds off.
29,71.0,74.0,That was legitimately the first time they had ever met.
30,75.0,77.0,I just keep thinking of the feeling like
31,77.0,79.0,of exiting.

=> I only get the "from" column. 
```
+ Captions/Transcripts of Youtube's videos are easily captured via `pytubefix`. However, getting those information for the mp4 files, considering the diversity of the content and languages, using DL-based approach can be powerful enough to "overcome" the problem. Suggest: `whisper`. 
+ I choose third-party like Gemini and Groq because: high quality inference (fast, accurate), and economic. 
+ Prompt Engineering for a More Conversational Experience.
+ Implementation of a Memory Buffer for Extended Conversations
    * **User Interactions:**  The expected length and nature of user interactions influence the buffer size.
    * **Computational Cost:** Storing and processing conversation history has computational implications.
    * **Response Quality:** The impact of the buffer size on the quality of the chatbot's responses.
    * **System Efficiency:** Balancing performance with maintaining context.

# Exercise 2

**Problem Statement:** Deploying an open-source LLM ([model BLOOMZ 1b1](https://huggingface.co/bigscience/bloomz-1b1)) while considering several factors: 

+ VRAM
+ Speed
+ Performance
+ Feature support: token completions, log proabilities, ...

**Goal:**

- Test LLM knowledge and deployment skills, ...