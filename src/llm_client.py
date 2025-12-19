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

    def adjust_prompt_with_feedback(self, feedback, last_prompt):
        """
        基于用户反馈调整 Prompt
        """
        system_msg = "You are an expert in adjusting image prompts based on feedback."
        user_msg = f"Last prompt used: {last_prompt}\nUser feedback: {feedback}\nGenerate a new optimized prompt."
        
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
            return last_prompt
        except Exception as e:
            print(f"LLM Feedback Exception: {e}")
            return last_prompt

    def _fallback_response(self, user_input):
        return {
            "analysis": "Error in LLM processing",
            "initial_draft": "",
            "critique": "",
            "final_prompt": user_input
        }