# 技术决策记录

> 记录所有重要的技术决策，确保项目方向一致

---

## 2026-06-02

### 决策 1：环境管理使用 Conda
**为什么**：用户已创建 `separation` 虚拟环境，方便隔离项目依赖，便于在不同机器上复现环境。

### 决策 2：GitHub 远程仓库命名 SeparationPersonFromBeat
**为什么**：项目核心目标是从音乐中分离人声（Person）和伴奏（Beat），名称直观反映了功能定位。

### 决策 3：使用 Conventional Commits 提交规范
**为什么**：CLAUDE.md 已明确要求，确保提交历史可读性和可维护性。

### 决策 4：选用 Meta Demucs (HTDemucs) 作为核心模型
**为什么**：
- Meta (Facebook Research) 开源的成熟方案，社区活跃
- HTDemucs (Hybrid Transformer Demucs) 是 Demucs v4 的默认模型
- 支持 4 音源分离（vocals/drums/bass/other）和 6 音源版本
- PyTorch 原生支持，与 GPU 加速无缝集成
- pip install demucs 一行安装，依赖清晰

### 决策 5：PyTorch 使用 CUDA 12.8 编译版本 (cu128) 配合 CUDA 12.9 运行时
**为什么**：
- 用户的 RTX 5070 需要 CUDA 12.8+ (sm_120 Blackwell 架构)
- PyTorch 稳定版最新 CUDA 编译为 cu128
- CUDA 运行时向下兼容：12.9 驱动可运行 12.8 编译的 CUDA 代码
- 避免 nightly 版本的不稳定性
- 实际验证：torch.cuda.is_available() = True, GPU 识别正常

### 决策 6：在调用 Demucs 之前强制执行 GPU 检查
**为什么**：
- 用户明确要求：代码逻辑必须在调用 Demucs 前打印 torch.cuda.is_available()
- 统一入口 `separator.check_gpu()` -> `separator.separate()` 保证不论何种调用方式
  都先执行 GPU 检查
- 避免静默回退到 CPU 导致性能问题

---
