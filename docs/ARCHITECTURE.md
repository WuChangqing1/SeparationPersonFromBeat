# 项目架构

> 最后更新：2026-06-02

## 系统概览
人声与伴奏分离工具（SeparationPersonFromBeat），基于 Meta Demucs (Hybrid Transformer Demucs)
实现音频源分离，将混合音频中的 vocals, drums, bass, other 分离为独立音轨。

## 技术栈
| 层级 | 技术 | 用途 |
|---|---|---|
| 语言 | Python 3.11.15 | 主要开发语言 |
| 环境管理 | Conda (separation) | 虚拟环境与依赖隔离 |
| AI/ML | PyTorch 2.11.0+cu128 | 深度学习框架 (GPU) |
| 模型 | Demucs 4.0.1 (HTDemucs) | Hybrid Transformer 音源分离 |
| 音频 I/O | torchaudio + ffmpeg | 音频文件读写 |
| GPU | NVIDIA RTX 5070 Laptop (8GB) | CUDA 12.9 运行时 / CUDA 12.8 编译 |

## 目录结构
```
Separation/
├── CLAUDE.md           # 项目规则与 Agent 配置
├── README.md           # 项目说明
├── requirements.txt    # Python 依赖
├── .gitignore          # Git 忽略规则
├── docs/               # 项目记忆系统
│   ├── ARCHITECTURE.md # 项目架构
│   ├── PROGRESS.md     # 项目进度
│   ├── DECISIONS.md    # 技术决策记录
│   ├── ISSUES.md       # 问题记录
│   ├── LOG.md          # 会话日志
│   └── CHANGELOG.md    # 变更日志
├── src/                # 源代码
│   ├── __init__.py     # 包初始化
│   ├── main.py         # CLI 入口
│   └── separator.py    # 分离核心逻辑
├── demucs-main/        # Demucs 源码参考 (不提交)
└── tests/              # 测试代码 (待创建)
```

## 核心模块关系

```
输入音频 (WAV/MP3/FLAC)
    │
    ▼
src/main.py (CLI 参数解析)
    │
    ▼
src/separator.py
    ├── check_gpu()          ← 验证 GPU 就绪 (torch.cuda.is_available)
    ├── build_model_args()   ← 构建 Demucs 模型参数
    ├── load_track()         ← 音频加载 (ffmpeg/torchaudio)
    ├── get_model_from_args()← 加载预训练模型 (HTDemucs)
    ├── apply_model()        ← 核心推理 (CUDA/CPU)
    └── save_audio()         ← 输出保存
    │
    ▼
输出目录/{model_name}/{track_name}/
    ├── vocals.wav
    ├── drums.wav
    ├── bass.wav
    └── other.wav
```

## 当前支持的模型

| 模型 | 说明 |
|---|---|
| htdemucs (默认) | Hybrid Transformer Demucs, 4 音源 (vocals/drums/bass/other) |
| htdemucs_ft | 微调版 HTDemucs |
| htdemucs_6s | 6 音源版 (vocals/drums/bass/other/guitar/piano) |
