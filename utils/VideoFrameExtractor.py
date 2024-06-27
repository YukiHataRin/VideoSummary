import cv2
import os
import shutil

class VideoFrameExtractor:
    def __init__(self, video_path, output_folder='frames'):
        self.video_path = video_path
        self.output_folder = output_folder
        if os.path.exists(output_folder):
            # 刪除資料夾內的所有檔案
            for filename in os.listdir(output_folder):
                file_path = os.path.join(output_folder, filename)
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
        else:
            os.makedirs(output_folder)

    def resize_frame(self, frame):
        height, width = frame.shape[:2]
        if width < height:
            new_height = 100
            new_width = int((new_height / height) * width)
        else:
            new_width = 100
            new_height = int((new_width / width) * height)
        return cv2.resize(frame, (new_width, new_height))

    def extract_frames(self):
        cap = cv2.VideoCapture(self.video_path)
        frame_rate = cap.get(cv2.CAP_PROP_FPS)
        all_frame = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        success, frame = cap.read()
        frame_count = 0
        frame_interval = int(frame_rate)  # 一秒提取一個幀

        while success:
            if frame_count % frame_interval == 0:
                frame = self.resize_frame(frame)
                time_in_seconds = frame_count / frame_rate
                minutes = int(time_in_seconds // 60)
                seconds = int(time_in_seconds % 60)
                milliseconds = int((time_in_seconds * 1000) % 1000)

                filename = f'{minutes}m{seconds}s.png'
                filepath = os.path.join(self.output_folder, filename)
                cv2.imwrite(filepath, frame)

            frame_count += 1
            success, frame = cap.read()

        cap.release()
        print("Frames extracted successfully.")
        print(f'Total frames: {all_frame}')

# 使用範例
# video_path = 'video1.mp4'
# extractor = VideoFrameExtractor(video_path)
# extractor.extract_frames()
