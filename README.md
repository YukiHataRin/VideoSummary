
# Video Summarization Application

這個應用程序使用 Gradio 和 Whisper 來處理視頻並生成文字總結。你可以上傳視頻，並得到視頻的文字總結。

## 目錄

- [Video Summarization Application](#video-summarization-application)
  - [目錄](#目錄)
  - [需求](#需求)
  - [環境變數](#環境變數)
  - [安裝](#安裝)
  - [使用方法](#使用方法)
  - [文件結構](#文件結構)

## 需求

- Python 3.7+
- moviepy
- whisper
- gradio

## 環境變數

在開始之前，你需要在項目根目錄下創建一個 `.env` 文件，並添加你的 OpenAI API 金鑰和模型名稱。

```dotenv
OPENAI_API_KEY=你的OpenAI API金鑰
MODEL=gpt-4o
```

## 安裝

1. 克隆此存儲庫：
    ```sh
    git clone https://github.com/YukiHataRin/VideoSummary.git
    cd 你的項目名
    ```

2. 安裝所需的 Python 庫：
    ```sh
    pip install -r requirements.txt
    ```

## 使用方法

1. 確保你已經設置了 `.env` 文件中的環境變數。

2. 運行應用程序：
    ```sh
    python main.py
    ```

3. 在瀏覽器中打開顯示的本地 URL，然後上傳你想要總結的視頻。

## 文件結構

- `utils` - 輔助工具
- `main.py` - 主程序入口，包含 Gradio 應用的設置和啟動。
- `requirements.txt` - 包含所有需要安裝的 Python 庫。
- `.env` - 環境變數文件，包含 OpenAI API 金鑰和模型名稱。

```
VideoSummarization
│── utils
│── main.py
│── utils
│── requirements.txt
└── .env
