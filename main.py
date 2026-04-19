#!/usr/bin/env python3
"""
Video Tools - 短视频处理工具箱
支持视频下载、去水印、格式转换、剪辑、字幕提取等
"""
import argparse
import sys
import subprocess
import os
from pathlib import Path

def run_cmd(cmd, desc=""):
    """执行命令"""
    print(f"🔧 {desc or cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ 失败: {result.stderr[:200]}")
        return False
    print(f"✅ 完成")
    return True

def check_ffmpeg():
    """检查 FFmpeg 是否安装"""
    try:
        subprocess.run("ffmpeg -version", shell=True, capture_output=True)
        return True
    except FileNotFoundError:
        print("⚠️  FFmpeg 未安装！请先安装 FFmpeg: https://ffmpeg.org/download.html")
        return False

def download(url: str, output: str = None):
    """下载视频"""
    if not url:
        print("❌ 请提供视频 URL")
        return
    if not output:
        output = "video.mp4"
    print(f"⬇️  下载视频: {url}")

    # 优先使用 yt-dlp
    cmd = f'yt-dlp -o "{output}" "{url}"'
    if subprocess.run(f"yt-dlp --version", shell=True, capture_output=True).returncode != 0:
        # 回退到直接下载
        import requests
        print("⚠️  yt-dlp 未安装，将尝试直接下载...")
        try:
            r = requests.get(url, stream=True, timeout=30)
            with open(output, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"✅ 已保存为 {output}")
        except Exception as e:
            print(f"❌ 下载失败: {e}")
            print("💡 建议安装 yt-dlp: pip install yt-dlp")
    else:
        run_cmd(cmd, "下载中")

def unwatermark(input_file: str, output_file: str = None):
    """去水印"""
    if not Path(input_file).exists():
        print(f"❌ 文件不存在: {input_file}")
        return
    if not output_file:
        p = Path(input_file)
        output_file = str(p.parent / f"{p.stem}_no_watermark{p.suffix}")
    if not check_ffmpeg():
        return
    # 简单去水印：裁剪掉水印区域（需根据实际调整坐标）
    cmd = f'ffmpeg -i "{input_file}" -vf "delogo=x=0:y=0:w=iw:h=40" -c:a copy "{output_file}"'
    run_cmd(cmd, "去水印处理")

def convert(input_file: str, output_file: str):
    """格式转换"""
    if not Path(input_file).exists():
        print(f"❌ 文件不存在: {input_file}")
        return
    if not check_ffmpeg():
        return
    cmd = f'ffmpeg -i "{input_file}" -c copy "{output_file}"'
    run_cmd(cmd, f"转换为 {Path(output_file).suffix}")

def cut(input_file: str, start: float, end: float, output_file: str = None):
    """剪辑片段"""
    if not Path(input_file).exists():
        print(f"❌ 文件不存在: {input_file}")
        return
    if not output_file:
        p = Path(input_file)
        output_file = str(p.parent / f"{p.stem}_clip{p.suffix}")
    if not check_ffmpeg():
        return
    duration = end - start
    cmd = f'ffmpeg -i "{input_file}" -ss {start} -t {duration} -c copy "{output_file}"'
    run_cmd(cmd, f"剪辑 {start}s -> {end}s")

def merge(files: list, output_file: str = "merged.mp4"):
    """合并视频"""
    if not files:
        print("❌ 请提供要合并的文件列表")
        return
    if not check_ffmpeg():
        return
    # 创建临时文件列表
    list_file = "filelist.txt"
    with open(list_file, "w") as f:
        for fpath in files:
            f.write(f"file '{fpath}'\n")
    cmd = f'ffmpeg -f concat -safe 0 -i "{list_file}" -c copy "{output_file}"'
    if run_cmd(cmd, "合并视频"):
        os.remove(list_file)

def extract_audio(input_file: str, output_file: str = None):
    """提取音频"""
    if not Path(input_file).exists():
        print(f"❌ 文件不存在: {input_file}")
        return
    if not output_file:
        p = Path(input_file)
        output_file = str(p.parent / f"{p.stem}.mp3")
    if not check_ffmpeg():
        return
    cmd = f'ffmpeg -i "{input_file}" -vn -acodec libmp3lame -q:a 2 "{output_file}"'
    run_cmd(cmd, "提取音频")

def extract_subtitle(input_file: str, output_file: str = None):
    """提取字幕（需 ffmpeg 内置 ass/srt 支持）"""
    if not Path(input_file).exists():
        print(f"❌ 文件不存在: {input_file}")
        return
    if not output_file:
        p = Path(input_file)
        output_file = str(p.parent / f"{p.stem}.srt")
    if not check_ffmpeg():
        return
    cmd = f'ffmpeg -i "{input_file}" -map 0:s:0? "{output_file}"'
    run_cmd(cmd, "提取字幕")

def main():
    parser = argparse.ArgumentParser(description="🎬 Video Tools - 短视频处理工具箱")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("download", help="下载视频").add_argument("url")
    p_unwm = sub.add_parser("unwatermark", help="去水印")
    p_unwm.add_argument("input")
    p_unwm.add_argument("-o", "--output")

    p_conv = sub.add_parser("convert", help="格式转换")
    p_conv.add_argument("input")
    p_conv.add_argument("output")

    p_cut = sub.add_parser("cut", help="剪辑片段")
    p_cut.add_argument("input")
    p_cut.add_argument("--start", type=float, required=True)
    p_cut.add_argument("--end", type=float, required=True)
    p_cut.add_argument("-o", "--output")

    p_merge = sub.add_parser("merge", help="合并视频")
    p_merge.add_argument("files", nargs="+")
    p_merge.add_argument("-o", "--output", default="merged.mp4")

    p_audio = sub.add_parser("audio", help="提取音频")
    p_audio.add_argument("input")
    p_audio.add_argument("-o", "--output")

    p_sub = sub.add_parser("subtitle", help="提取字幕")
    p_sub.add_argument("input")
    p_sub.add_argument("-o", "--output")

    args = parser.parse_args()

    if args.cmd == "download":
        download(args.url)
    elif args.cmd == "unwatermark":
        unwatermark(args.input, args.output)
    elif args.cmd == "convert":
        convert(args.input, args.output)
    elif args.cmd == "cut":
        cut(args.input, args.start, args.end, args.output)
    elif args.cmd == "merge":
        merge(args.files, args.output)
    elif args.cmd == "audio":
        extract_audio(args.input, args.output)
    elif args.cmd == "subtitle":
        extract_subtitle(args.input, args.output)

if __name__ == "__main__":
    main()
