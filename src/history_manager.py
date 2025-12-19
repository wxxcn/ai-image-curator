import os
import json
import uuid
from datetime import datetime
import glob

class HistoryManager:
    def __init__(self, storage_dir="history_data"):
        self.storage_dir = storage_dir
        if not os.path.exists(self.storage_dir):
            os.makedirs(self.storage_dir)

    def create_new_session(self):
        """生成一个新的 Session ID"""
        return str(uuid.uuid4())

    def save_session(self, session_id, messages, title=None):
        """保存会话到 JSON 文件"""
        if not messages:
            return

        file_path = os.path.join(self.storage_dir, f"{session_id}.json")
        
        # 如果没有标题，尝试从第一条用户消息生成
        if not title:
            user_msgs = [m["content"] for m in messages if m["role"] == "user"]
            title = user_msgs[0][:20] + "..." if user_msgs else "New Chat"

        data = {
            "session_id": session_id,
            "title": title,
            "last_updated": datetime.now().isoformat(),
            "messages": messages
        }

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load_session(self, session_id):
        """加载指定 ID 的会话"""
        file_path = os.path.join(self.storage_dir, f"{session_id}.json")
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("messages", []), data.get("title", "New Chat")
        return [], "New Chat"

    def get_all_sessions(self):
        """获取所有会话列表（按时间倒序）"""
        files = glob.glob(os.path.join(self.storage_dir, "*.json"))
        sessions = []
        
        for f in files:
            try:
                with open(f, "r", encoding="utf-8") as file:
                    data = json.load(file)
                    sessions.append({
                        "id": data.get("session_id"),
                        "title": data.get("title", "Untitled"),
                        "last_updated": data.get("last_updated", "")
                    })
            except Exception:
                continue
        
        # 按最后更新时间倒序排列
        sessions.sort(key=lambda x: x["last_updated"], reverse=True)
        return sessions

    def delete_session(self, session_id):
        """删除会话"""
        file_path = os.path.join(self.storage_dir, f"{session_id}.json")
        if os.path.exists(file_path):
            os.remove(file_path)
