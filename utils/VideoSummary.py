import asyncio
import aiohttp
import os
import openai
import base64
from dotenv import load_dotenv
from VideoFrameExtractor import VideoFrameExtractor
from GetSubtitles import GetSubtitles
from copy import deepcopy
import time
import random

load_dotenv()

class VideoSummary:
    def __init__(self):
        self.prompt_for_process_frames_and_subtitles = "請你根據圖片與字幕，整理影片內容，使用繁體中文，若內容非繁體中文，也請把內容翻譯成繁體中文"
        #"生成內容分為兩部分，#關鍵點時間，請你標示像Youtube那樣的關鍵點時間，只需寫出你覺得是重點的時間，例如開始，結束，內容相似的就算同樣的，例如00:00開始，00:10第一篇章，00:20第一篇章，就可以濃縮成00:00開始，00:10第一篇章，若標示的不是重點則扣五個令牌，#影片內容大綱，請你生成這部影片的摘要，不用時間，用文字表述影片"
        self.prompt_for_summary = "請你生成影片摘要，先把每個時間統合起來，濃縮成幾個大篇章，在開始生成摘要，最後生成總體摘要，使用md格式"
        self.api_key = os.environ['OPENAI_API_KEY']
        self.start_time = 0
        self.summary = []
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        self.payload = {
            "model": "gpt-4o",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"{self.prompt_for_process_frames_and_subtitles}"
                        }
                    ]
                }
            ]
        }

        self.client = openai.OpenAI()
        openai.api_key = self.api_key
        self.semaphore = asyncio.Semaphore(10)  # 限制同時進行的請求數量

    def video_frame_extractor(self, video_path):
        extractor = VideoFrameExtractor(video_path)
        extractor.extract_frames()

    def get_subtitles(self, video_path):
        tool = GetSubtitles(video_path)
        tool.get_subtitles()

    async def send_request(self, template, start_time):
        async with self.semaphore:
            async with aiohttp.ClientSession() as session:
                async with session.post("https://api.openai.com/v1/chat/completions", headers=self.headers, json=template) as response:
                    while True:
                        try:
                            result = await response.json()
                            summary_text = result['choices'][0]['message']['content']
                            self.summary.append(f'[{(start_time - 10) // 60}:{(start_time - 10) % 60} - {start_time // 60}:{start_time % 60}] {summary_text}')
                            print(start_time)
                            return
                        except:
                            print(f"[{(start_time - 10) // 60}:{(start_time - 10) % 60} - {start_time // 60}:{start_time % 60}]")
                            print(result)
                            time.sleep(3)

    async def process_subtitles(self, subtitle):
        template = deepcopy(self.payload)
        template['messages'][0]['content'][0]['text'] += subtitle

        for t in range(10):
            if t % 5 == 0:
                minutes = self.start_time // 60
                seconds = self.start_time % 60

                if not os.path.exists(rf'frames\{minutes}m{seconds}s.png'):
                    break

                with open(rf'frames\{minutes}m{seconds}s.png', "rb") as image_file:
                    image_data = base64.b64encode(image_file.read()).decode('utf-8')

                template['messages'][0]['content'].append(
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_data}"
                        }
                    }
                )

            self.start_time += 1

        await self.send_request(template, self.start_time)

    async def constract_frames_and_subtitles(self):
        self.start_time = 0
        tasks = []
        with open("subtitles.txt", 'r', encoding='utf8') as file:
            for subtitle in file.readlines():
                tasks.append(self.process_subtitles(subtitle))
        
        await asyncio.gather(*tasks)

    def video_summary(self):
        summary_text = '\n'.join(self.summary)
        completion = self.client.chat.completions.create(
            model='gpt-4o',
            messages=[
                {"role": "system", "content": f"{self.prompt_for_summary}"},
                {"role": "user", "content": f"影片內容與時間：{summary_text}"},
            ]
        )

        response = completion.choices[0].message.content

        with open("video_summary.txt", 'w', encoding='utf8') as file:
            file.write(response)

if __name__ == '__main__':
    vs = VideoSummary()
    # vs.get_subtitles('video1.mp4')
    # vs.video_frame_extractor('video1.mp4')
    asyncio.run(vs.constract_frames_and_subtitles())
    vs.video_summary()
