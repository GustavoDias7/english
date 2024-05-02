import argparse
import os
import webvtt
from moviepy.editor import *

parser = argparse.ArgumentParser()
parser.add_argument('--video', help='Path of video file')
parser.add_argument('--subtitle', help='Path of subtitle file')
parser.add_argument('--remove_sec', help='Remove seconds from subtitles')
parser.add_argument('--export_first', help='Export the first n clips')
parser.add_argument('--mode', help="Mode exclude to the user choice subtitles to be excluded from the audio output")
args = parser.parse_args()

if not (
    args.video and 
    os.path.isfile(args.video) and 
    args.video.endswith(('.mp4'))
): quit()

if not (
    args.subtitle and 
    os.path.isfile(args.subtitle) and 
    args.subtitle.endswith(('.vtt'))
): quit()

export_first = len(webvtt.read(args.subtitle))
if args.export_first and args.export_first.isnumeric():
    export_first = int(args.export_first)

if not os.path.exists("./audio-output"):
    os.makedirs("./audio-output")


def get_sec(time_str):
    h, m, s = time_str.split(':')
    return float("{:.3f}".format(int(h) * 3600 + int(m) * 60 + float(s)))

def is_float(element: any) -> bool:
    if element is None: 
        return False
    try:
        float(element)
        return True
    except ValueError:
        return False

captions = webvtt.read(args.subtitle)[:export_first]

to_exclude = []
if args.mode and args.mode == "exclude":
    answer_2 = "y"
    while answer_2 == "y":
        for index, caption in enumerate(captions):
            text = caption.text.replace("\n", " ")
            check = ' '
            if str(index) in to_exclude:
                check = "x"
            print(f"[{check}] {index} - {text}")
        answer = input("Which does subtitles you want to exclude? ")
        
        to_exclude = to_exclude + answer.split(" ")

        for index, caption in enumerate(captions):
            text = caption.text.replace("\n", " ")
            check = ' '
            if str(index) in to_exclude:
                check = "x"
            print(f"[{check}] {index} - {text}")

        answer_2 = input("Do you want to exclude another subtitles?[y/n] ")
    


video_file = VideoFileClip(args.video)
for index, caption in enumerate(captions):
    if str(index) in to_exclude: continue
    
    text = caption.text.replace("\n", " ")

    if args.remove_sec and is_float(args.remove_sec):
        video_clip = video_file.subclip(
            get_sec(caption.start) - float(args.remove_sec),
            get_sec(caption.end)- float(args.remove_sec),
        )
    else:
        video_clip = video_file.subclip(
            get_sec(caption.start),
            get_sec(caption.end),
        )

    audio_clip = video_clip.audio
    audio_clip.write_audiofile(f"./audio-output/{text}.mp3")