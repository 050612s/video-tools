# 🎬 Video Tools - 短视频素材工具箱

> 一站式短视频处理工具，支持视频下载、去水印、格式转换、剪辑、字幕提取等。内置多个平台解析器，适合内容创作者和运营人员。

## ✨ 功能

- ⬇️ **多平台下载** - 支持抖音、快手、B站、小红书、视频号等平台
- 🚫 **去水印** - 一键去除视频水印
- 🔄 **格式转换** - 支持 MP4、WebM、AVI、MOV 等格式互转
- ✂️ **视频剪辑** - 剪切、合并、添加字幕
- 📝 **字幕提取** - 自动提取视频字幕/文字
- 🎵 **音频提取** - 从视频提取音频
- 🖼️ **封面提取** - 自动下载视频封面图
- 📐 **视频压缩** - 批量压缩视频文件

## 🚀 快速开始

### 安装

```bash
pip install video-tools
```

### 使用

```bash
# 下载视频
video-tools download "https://v.douyin.com/xxx"

# 去水印
video-tools unwatermark input.mp4 output.mp4

# 格式转换
video-tools convert input.avi output.mp4

# 剪辑片段
video-tools cut input.mp4 --start 10 --end 30

# 合并视频
video-tools merge file1.mp4 file2.mp4 --output merged.mp4

# 提取字幕
video-tools subtitle input.mp4

# 提取音频
video-tools audio input.mp4 --output audio.mp3
```

## 📋 环境要求

- Python 3.8+
- FFmpeg (需安装并加入 PATH)
- requests
- moviepy

## 📄 License

MIT License
