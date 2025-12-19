import os
import json
import dashscope
from http import HTTPStatus
from src.prompt_engine import PromptEngine

class LLMClient:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("DASHSCOPE_API_KEY")
        dashscope.api_key = self.api_key
        self.model = "qwen-max" # 指定使用 Qwen-Max
        self.engine = PromptEngine()

    def optimize_prompt(self, user_input, platform="Default"):
        """
        执行 Prompt 自迭代流程
        """
        system_msg = "You are a helpful assistant that optimizes image generation prompts."
        user_msg = self.engine.get_iteration_message(user_input, platform)
        
        try:
            response = dashscope.Generation.call(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": user_msg}
                ],
                result_format='message' # 返回消息格式，方便提取
            )
            
            if response.status_code == HTTPStatus.OK:
                content = response.output.choices[0].message.content
                
                # 清洗 Markdown 标记
                if "```json" in content:
                    content = content.split("```json")[1].split("```")[0].strip()
                elif "```" in content:
                    content = content.split("```")[1].split("```")[0].strip()
                
                return json.loads(content)
            else:
                print(f"LLM Error: {response.code} - {response.message}")
                return self._fallback_response(user_input)
                
        except Exception as e:
            print(f"LLM Exception: {e}")
            return self._fallback_response(user_input)

    def adjust_prompt_with_context(self, history, last_optimized_prompt):
        """
        基于完整对话历史和上一次优化过的 Prompt 进行调整
        """
        system_msg = (
            "You are an expert in iterative image prompt engineering. "
            "Your goal is to refine an existing prompt based on user feedback while maintaining the overall context."
        )
        
        # 构建上下文描述
        context_summary = "Here is the conversation history so far:\n"
        for msg in history:
            role = "User" if msg["role"] == "user" else "Assistant"
            content = msg["content"]
            context_summary += f"{role}: {content}\n"
        
        user_msg = (
            f"{context_summary}\n"
            f"The last optimized prompt used was: `{last_optimized_prompt}`.\n\n"
            "The user just provided the latest feedback (the last User message above). "
            "Please generate a new, updated Chinese prompt for Qwen-Image that incorporates this feedback "
            "while respecting previous requirements and styles. Output ONLY the new final prompt."
        )
        
        try:
            response = dashscope.Generation.call(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": user_msg}
                ],
                result_format='message'
            )
            if response.status_code == HTTPStatus.OK:
                return response.output.choices[0].message.content
            return last_optimized_prompt
        except Exception as e:
            print(f"LLM Context Adjustment Exception: {e}")
            return last_optimized_prompt

    def _fallback_response(self, user_input):
        return {
            "analysis": "Error in LLM processing",
            "initial_draft": "",
            "critique": "",
            "final_prompt": user_input
        }