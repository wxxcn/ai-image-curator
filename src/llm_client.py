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
        
        return self._call_llm_json(system_msg, user_msg, user_input)

    def adjust_prompt_with_context(self, history, last_optimized_prompt):
        """
        基于完整对话历史和上一次优化过的 Prompt 进行调整 (返回 JSON)
        """
        system_msg = (
            "You are an expert in iterative image prompt engineering. "
            "Your goal is to refine an existing prompt based on user feedback while maintaining the overall context."
        )
        
        # 构建上下文描述
        context_summary = "Here is the conversation history so far:\n"
        for msg in history:
            role = "User" if msg["role"] == "user" else "Assistant"
            content = msg.get("content", "")
            # 如果是 Assistant 消息，尝试提取其中的 final_prompt，减少 Token 消耗
            if msg["role"] == "assistant" and "iteration_details" in msg:
                final_p = msg["iteration_details"].get("final_prompt", "")
                if final_p:
                    content = f"[Generated Image Prompt]: {final_p}"
            
            context_summary += f"{role}: {content}\n"
        
        # 获取包含 JSON 要求的 Prompt
        last_msg_content = history[-1]["content"] if history else ""
        user_msg = self.engine.get_feedback_adjustment_prompt(context_summary, last_msg_content)
        
        return self._call_llm_json(system_msg, user_msg, last_optimized_prompt)

    def _call_llm_json(self, system_msg, user_msg, fallback_prompt):
        """
        通用 LLM 调用方法，处理 JSON 解析和错误
        """
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
                content = response.output.choices[0].message.content
                
                # 清洗 Markdown 标记
                if "```json" in content:
                    content = content.split("```json")[1].split("```")[0].strip()
                elif "```" in content:
                    content = content.split("```")[1].split("```")[0].strip()
                
                return json.loads(content)
            else:
                print(f"LLM Error: {response.code} - {response.message}")
                return self._fallback_response(fallback_prompt)
                
        except Exception as e:
            print(f"LLM Exception: {e}")
            return self._fallback_response(fallback_prompt)

    def _fallback_response(self, user_input):
        return {
            "analysis": "Error in LLM processing or Network issue.",
            "initial_draft": "N/A",
            "critique": "Fallback triggered.",
            "final_prompt": user_input
        }
