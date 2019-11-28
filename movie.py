#coding=utf-8
from moviepy.editor import *
import os

if __name__ == '__main__':
    try:
        os.mkdir("./downloadFile")
    except:
        print("文件已经存在")
        pass
    remember = ""
    os.chdir("./downloadFile")
    target = input("请输入要下载的视频地址:")
    command = "you-get "+target
    os.system(command)
    filenames=os.listdir(os.getcwd())
    for file in filenames:
        print(file)
        if os.path.splitext(file)[1] in [".mp4",".webm",".flv",]:
            remember = file
    print("视频下载完成!!!")
    print("=======================================================")
    print("开始转换....")
    video = VideoFileClip(remember)
    audio = video.audio
    audio.write_audiofile(os.path.splitext(remember)[0]+'.mp3')
    print("转换完毕！")