from openai import OpenAI
from dotenv import load_dotenv
import json
import math

load_dotenv()

class GetSubtitles:
    def __init__(self, video_path):
        self.client = OpenAI()
        self.video_path = video_path

    def get_subtitles(self):
        audio_file = open(self.video_path, "rb")
        transcript = self.client.audio.transcriptions.create(
            file=audio_file,
            model="whisper-1",
            response_format="verbose_json",
            timestamp_granularities=["segment"]
        )

        txt_output = []
        segments = transcript.to_dict()["segments"]
        max_duration = segments[-1]["end"]

        for i in range(0, math.ceil(max_duration / 10)):
            start_time = i * 10
            end_time = (i + 1) * 10
            text_segments = [segment["text"] for segment in segments if start_time <= segment["start"] < end_time]
            if text_segments:
                start_minutes = start_time // 60
                start_seconds = start_time % 60
                end_minutes = end_time // 60
                end_seconds = end_time % 60
                txt_output.append(f"[{start_minutes}:{start_seconds:02} - {end_minutes}:{end_seconds:02}] {' '.join(text_segments)}")

        # 將結果寫入 txt 文件
        with open("subtitles.txt", "w", encoding="utf-8") as file:
            file.write("\n".join(txt_output))

        print("轉換完成，已將結果寫入 subtitles.txt")

if __name__ == '__main__':
    tool = GetSubtitles('video1.mp4')
    tool.get_subtitles()