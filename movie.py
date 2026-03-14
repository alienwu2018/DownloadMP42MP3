#coding=utf-8
import os
import subprocess
import time

# 语言选择
language = int(input('Choose your language (Chinese: 0, English: 1): '))

translation = [
    {   # 中文
        "error_dir": "目录已存在",
        "choice": "是否转换成mp3格式(Y/N): ",
        "complete": "视频下载完成",
        "conversion": "开始转换...",
        "success": "转换成功！",
        "fail": "转换失败！",
        "no_video": "未找到视频文件！",
        "invalid_choice": "无效选择！",
        "cleanup": "已清理多余文件（仅保留MP3）",
        "file_exists": "文件已存在，自动重命名为: {}"
    },
    {   # English
        "error_dir": "Directory already exists",
        "choice": "Convert to mp3 format (Y/N): ",
        "complete": "Video download completed",
        "conversion": "Starting conversion...",
        "success": "Conversion successful!",
        "fail": "Conversion failed!",
        "no_video": "No video file found!",
        "invalid_choice": "Invalid choice!",
        "cleanup": "Cleaned up extra files (MP3 only)",
        "file_exists": "File exists, auto-renamed to: {}"
    }
]

lang = translation[language]

if __name__ == '__main__':
    # 创建 MP3 目录
    try:
        os.mkdir("./MP3")
    except FileExistsError:
        print(lang["error_dir"])

    os.chdir("./MP3")

    # 记录下载前的文件列表
    before_download = set(os.listdir('.'))

    # 输入视频 URL
    target = input("请输入要下载的视频地址: ")
    command = "you-get " + target
    os.system(command)

    # 下载后的文件列表
    after_download = set(os.listdir('.'))
    new_files = after_download - before_download  # 本次下载新增的文件

    if not new_files:
        print("没有下载到新文件，请检查 URL 或网络。")
        exit()

    choice = input(lang["choice"])
    if choice.upper() == 'Y':
        # 在新增文件中查找视频文件
        video_file = None
        for f in new_files:
            if os.path.splitext(f)[1].lower() in [".mp4", ".webm", ".flv", ".mkv", ".avi"]:
                video_file = f
                print("找到视频文件:", f)
                break

        if video_file is None:
            print(lang["no_video"])
            # 可选：是否删除这些新增文件？
            exit()

        print(lang["complete"])
        print("=" * 55)
        print(lang["conversion"])

        # 生成音频文件名（避免覆盖已有文件）
        base_name = os.path.splitext(video_file)[0]
        audio_file = base_name + ".mp3"
        counter = 1
        while os.path.exists(audio_file):
            audio_file = f"{base_name}_{counter}.mp3"
            counter += 1
        if counter > 1:
            print(lang["file_exists"].format(audio_file))

        # 调用 ffmpeg 提取音频
        ffmpeg_cmd = f'ffmpeg -i "{video_file}" -vn -acodec mp3 "{audio_file}" -y'
        result = subprocess.run(
            ffmpeg_cmd,
            shell=True,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace'
        )

        if result.returncode == 0:
            print(lang["success"], audio_file)

            # 删除本次下载的新增文件中，除最终音频文件外的所有文件
            deleted = []
            for f in new_files:
                if f != audio_file:   # audio_file 可能不在 new_files 中，但条件仍然安全
                    try:
                        os.remove(f)
                        deleted.append(f)
                    except Exception as e:
                        print(f"删除文件 {f} 时出错: {e}")
            if deleted:
                print(lang["cleanup"], f"({', '.join(deleted)})")
        else:
            print(lang["fail"])
            print("错误信息:", result.stderr)

    elif choice.upper() == 'N':
        print(lang["complete"])
        # 不转换则保留所有下载的文件（包括视频、弹幕等）
    else:
        print(lang["invalid_choice"])