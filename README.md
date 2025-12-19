# 🎨 AI Image Curator

这是一个基于对话的智能生图系统，能够理解用户意图、自动迭代 Prompt，并适配不同社交平台（如小红书、抖音）的视觉风格。

## ✨ 核心功能

1.  **对话式生图与修改**：用户可以通过自然语言描述需求，并在生成后通过反馈（如“颜色再亮一点”、“背景换成森林”）直接修改图片。
2.  **Prompt 自迭代工作流**：内置“意图分析 -> 初稿 -> 自我批判 -> 最终优化”的 Prompt 工程链条，确保即使简单的输入也能得到高质量的输出。
3.  **社交平台风格适配**：预设小红书（氛围感、精致生活）、抖音（高视觉冲击、电影感）等风格模版。
4.  **透明的思考过程**：在生成图片时，用户可以查看 AI 是如何一步步优化 Prompt 的。

## 🛠️ 技术栈

-   **Frontend**: Streamlit
-   **LLM**: OpenAI GPT-4o (用于意图理解和 Prompt 优化)
-   **Image Gen**: OpenAI DALL-E 3
-   **Language**: Python

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

### 3. 配置环境变量
创建一个 `.env` 文件并填入你的阿里云 DashScope API Key：
1. 访问 [阿里云百炼 DashScope 控制台](https://dashscope.console.aliyun.com/apiKey)。
2. 获取 API Key。

```env
DASHSCOPE_API_KEY=your_sk_...
```

### 4. 运行应用
```bash
streamlit run app.py
```

## 📖 使用指南

1.  在侧边栏输入 **DashScope API Key**。
2.  选择 **Target Social Platform**。
3.  开始对话生图！系统将自动调用 `qwen-max` 优化提示词，并调用 `wanx-v1` 生成图片。
