# 会话日志

> 每次会话结束前追加一条记录

---

## 2026-06-02 会话 (第 2 次)

**做了什么**：
- 配置 conda 环境 separation 的 GPU 依赖
- 卸载 CPU 版 PyTorch，安装 PyTorch 2.11.0+cu128 (CUDA 12.8)
- 安装 Demucs 4.0.1 及所有依赖 (torchaudio, openunmix, lameenc, julius 等)
- 验证 GPU: RTX 5070 Laptop GPU (8GB VRAM), CUDA available = True
- 创建 `src/separator.py` - 核心分离引擎 (GPU 检查 → 模型加载 → 推理 → 保存)
- 创建 `src/main.py` - CLI 命令行接口
- 创建 `requirements.txt`
- 更新所有 docs/ 记忆文件
- Git 提交并推送到 GitHub
- commit: 待提交

**下次继续**：
- 用实际音频文件测试分离效果
- 编写测试用例
- 添加批处理支持

---

## 2026-06-02 会话 (第 1 次)

**做了什么**：
- 初始化项目记忆系统
- 创建 docs/ 目录及所有记忆文件
- 初始化 Git 仓库（main 分支）
- 创建 .gitignore 和 README.md
- 创建 GitHub 远程仓库 SeparationPersonFromBeat
- 确认 conda 环境 `separation` (Python 3.11.15)
- 首次提交并推送到 GitHub: `0a440d2`
