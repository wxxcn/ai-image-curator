# 🎨 AI Image Curator (Qwen Edition)

这是一个基于对话的智能生图系统，能够理解用户意图、自动迭代 Prompt，并适配不同社交平台（如小红书、抖音）的视觉风格。

本项目全面驱动于 **阿里云 DashScope (灵积平台)**，使用通义千问系列模型提供强大的逻辑理解和图像生成能力。

## ✨ 核心功能

1.  **对话式生图与无限修图**：
    *   通过自然语言描述需求，支持连续对话修改（如“把背景换成雪山”，“猫咪改成白色的”）。
    *   **上下文感知**：AI 会记忆整个会话历史，确保修改指令能精准保留之前的细节。
    
2.  **Prompt 自迭代工作流**：
    *   内置“意图分析 -> 初稿 -> 自我批判 -> 最终优化”的 Prompt 工程链条。
    *   即使输入简单的“一只猫”，也能自动扩展为电影级的高质量 Prompt。

3.  **社交平台风格 & 尺寸适配**：
    *   **小红书 / 抖音**：自动使用 `928x1664` 竖屏分辨率，优化为高对比度、氛围感强的视觉风格。
    *   **电商 / 默认**：使用 `1328x1328` 高清方图，强调细节和布光。

4.  **历史记录管理**：
    *   支持创建新对话，自动保存历史记录到本地，随时回溯查看。
    *   API Key 本地持久化存储，无需重复输入。

## 🛠️ 技术栈

-   **Frontend**: Streamlit
-   **Reasoning LLM**: Alibaba **Qwen-Max** (通义千问-Max)
-   **Image Generation**: Alibaba **Qwen-Image-Plus** (通义千问生图加强版)
-   **SDK**: DashScope Python SDK

## 🚀 快速开始

### 1. 克隆仓库
```bash
git clone <your-repo-url>
cd ai-image-curator
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 配置 API Key
1.  访问 [阿里云百炼 DashScope 控制台](https://dashscope.console.aliyun.com/apiKey)。
2.  获取您的 **API Key**。
3.  确保您的账户已开通 **通义千问 (Qwen-Max)** 和 **通义万相/Qwen-Image** 服务。

### 4. 运行应用
```bash
streamlit run app.py
```

## 📖 使用指南

1.  **初始化**：在侧边栏输入 API Key 并点击 `💾 Save Key`。
2.  **选择模式**：选择目标平台（如 `Xiaohongshu`）。
3.  **开始创作**：输入“帮我画一个在海边喝椰子的女孩”。
4.  **修改**：不满意？直接说“把椰子换成西瓜”，AI 会自动根据上下文重新生成。
5.  **管理**：点击 `➕ New Chat` 开启新话题，或在侧边栏查看历史记录。

## 🔒 隐私说明
*   您的 API Key 仅存储在本地 `.user_config.json` 文件中。
*   该文件已包含在 `.gitignore` 中，**绝不会**被上传到 GitHub。