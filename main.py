import gradio as gr
import VideoSummary as v
import asyncio


def fn(path):
    summary_path = "video_summary.txt"
    vs = v.VideoSummary()
    vs.get_subtitles(path)
    vs.video_frame_extractor(path)
    asyncio.run(vs.constract_frames_and_subtitles())
    vs.video_summary()
    
    return [f.read() for f in [open(summary_path, 'r', encoding="utf-8")]][0]



demo = gr.Interface(
    fn = fn, 
    inputs = gr.Video(sources="upload"),
    outputs = gr.Text()
)


if __name__ == '__main__':
    demo.launch()