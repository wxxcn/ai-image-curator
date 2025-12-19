import os
import threading
import dashscope
from dashscope import ImageSynthesis
from http import HTTPStatus

class ImageGenerator:
    # 类级别的全局锁，确保并发数为 1
    _lock = threading.Lock()

    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("DASHSCOPE_API_KEY")
        dashscope.api_key = self.api_key
        # 使用 Qwen-Image 系列模型，默认使用效果更佳的 plus 版本
        self.model = "qwen-image-plus" 

    def generate_image(self, prompt, size="1024*1024", n=1):
        """
        调用 Qwen-Image-Plus 生成图片
        """
        size = size.replace("x", "*")
        
        with self._lock:
            try:
                print(f"DEBUG: Starting generation with model={self.model}, size={size}")
                
                response = ImageSynthesis.call(
                    model=self.model,
                    prompt=prompt,
                    n=n,
                    size=size
                )
                
                # --- 深度调试日志 ---
                print(f"DEBUG: Full Response: {response}")
                print(f"DEBUG: Status Code: {response.status_code}")
                
                if response.status_code == HTTPStatus.OK:
                    if response.output and response.output.results:
                        url = response.output.results[0].url
                        print(f"DEBUG: Success! URL: {url}")
                        return url
                    else:
                        print("DEBUG: Status OK but no results in output.")
                else:
                    # 详细打印错误信息
                    print(f"DEBUG: Request Failed. Code: {response.code}, Message: {response.message}")
                    print(f"DEBUG: Request ID: {response.request_id}")

                return None
                    
            except Exception as e:
                print(f"CRITICAL ERROR: {e}")
                import traceback
                traceback.print_exc()
                return None
