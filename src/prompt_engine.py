import json

class PromptEngine:
    """
    负责 Prompt 的自迭代优化和社交平台风格适配
    适配目标：通义万相 (Wanx) & 通义千问 (Qwen)
    """
    
    PLATFORM_TEMPLATES = {
        "Default": "通用高画质，光影细腻，细节丰富。",
        "Xiaohongshu (小红书)": (
            "风格偏好：柔美光影，生活感强，ins风，构图精致，色彩清新自然，氛围感。"
            "适用场景：好物分享、生活记录。尺寸通常为竖屏。"
        ),
        "Douyin (抖音)": (
            "风格偏好：强视觉冲击，高对比度，赛博或国潮风格，电影级调色，动态感。"
            "适用场景：短视频封面，吸睛。尺寸通常为竖屏。"
        ),
        "E-commerce (电商)": "风格偏好：纯净背景，专业布光，商品细节清晰，无噪点，4k级高清。"
    }

    ITERATION_PROMPT_TEMPLATE = """
    你是一位精通“通义千问生图 (Qwen-Image)”模型的提示词专家。
    
    [用户任务]: {user_input}
    [目标平台]: {platform}
    [平台风格指南]: {style_guide}
    
    你的任务是利用“思维链”优化用户的简短指令，生成适用于 Qwen-Image 的高质量**中文提示词**。
    
    步骤 1: 分析用户意图，确定主体、环境、艺术风格（如写实、插画、3D等）和色调。
    步骤 2: 结合[平台风格指南]进行风格化调整。
    步骤 3: 编写最终的中文生图 Prompt。Qwen-Image 能够极好地理解长句和细节，请使用丰富的形容词（如“电影质感”、“8k分辨率”、“丁达尔效应”等）。
    
    请严格按照以下 JSON 格式输出：
    {{
        "analysis": "简要分析意图...",
        "initial_draft": "...",
        "critique": "...",
        "final_prompt": "最终优化的中文提示词"
    }}
    """

    def get_iteration_message(self, user_input, platform="Default"):
        style_guide = self.PLATFORM_TEMPLATES.get(platform, self.PLATFORM_TEMPLATES["Default"])
        return self.ITERATION_PROMPT_TEMPLATE.format(
            user_input=user_input,
            platform=platform,
            style_guide=style_guide
        )

    def get_feedback_adjustment_prompt(self, history, feedback):
        """
        基于历史记录和用户反馈调整 Prompt
        """
        return f"基于此前的生图历史: {history}。用户反馈: {feedback}。请生成一个新的、经过优化的 Qwen-Image **中文提示词**。"