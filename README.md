# SeparationPersonFromBeat

人声与伴奏分离工具 —— 将混合音频中的人声（Person）和伴奏（Beat）分离为独立音轨。

## 功能

- 输入混合音频文件，输出分离后的人声音轨和伴奏音轨
- 支持常见音频格式（WAV、MP3、FLAC 等）

## 环境要求

- **Conda 环境**：`separation`
- **Python**：3.11.15

```bash
conda activate separation
```

## 安装

```bash
# 激活环境
conda activate separation

# 安装依赖（待补充）
pip install -r requirements.txt
```

## 使用

```bash
# 待实现
python src/main.py --input audio.wav --output ./output/
```

## 项目结构

```
SeparationPersonFromBeat/
├── src/          # 源代码
├── tests/        # 测试
├── docs/         # 文档
└── models/       # 模型文件（gitignore）
```

## 开发状态

项目处于初始化阶段。详见 [docs/PROGRESS.md](docs/PROGRESS.md)

## License

MIT
