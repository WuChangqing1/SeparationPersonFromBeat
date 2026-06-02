# 项目架构

> 最后更新：2026-06-02
> 本文件由 Agent 自动初始化，请根据实际情况补充

## 系统概览
人声与伴奏分离工具（SeparationPersonFromBeat），基于 Python 实现音频源分离，
将混合音频中的人声和伴奏分离为独立音轨。

## 技术栈
| 层级 | 技术 | 用途 |
|---|---|---|
| 语言 | Python | 主要开发语言 |
| 环境管理 | Conda (separation) | 虚拟环境与依赖隔离 |
| AI/ML | [待补充] | 人声分离模型 |
| 音频处理 | [待补充] | 音频 I/O 与处理 |

## 目录结构
```
Separation/
├── CLAUDE.md           # 项目规则与 Agent 配置
├── README.md           # 项目说明
├── .gitignore          # Git 忽略规则
├── docs/               # 项目记忆系统
│   ├── ARCHITECTURE.md # 项目架构
│   ├── PROGRESS.md     # 项目进度
│   ├── DECISIONS.md    # 技术决策记录
│   ├── ISSUES.md       # 问题记录
│   ├── LOG.md          # 会话日志
│   └── CHANGELOG.md    # 变更日志
├── src/                # 源代码（待创建）
├── tests/              # 测试代码（待创建）
└── models/             # 模型文件（待创建）
```

## 核心模块关系
[待补充：输入 → 预处理 → 模型推理 → 后处理 → 输出]
