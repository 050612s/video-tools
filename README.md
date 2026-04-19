# 🎬 视频处理工具箱

> 轻量命令行视频处理工具，支持格式转换、剪辑、压缩等。

[![Stars](https://img.shields.io/github/stars/050612s/video-tools?style=flat-square)](https://github.com/050612s/video-tools)

## 功能

- 🔄 视频格式转换（MP4/AVI/MKV/MOV）
- ✂️ 视频剪辑（截取片段）
- 📦 视频压缩
- 🎵 提取音频
- 🖼️ 视频转 GIF

## 快速开始

`ash
git clone https://github.com/050612s/video-tools.git
cd video-tools
pip install -r requirements.txt
python main.py --help
`

## 使用示例

`ash
# 格式转换
python main.py convert input.mp4 output.avi

# 压缩
python main.py compress input.mp4 --quality 70

# 截取片段
python main.py cut input.mp4 --start 0 --end 30 --output clip.mp4
`

## 📄 License

MIT