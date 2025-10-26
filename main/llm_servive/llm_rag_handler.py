import os
import httpx
from main.rag.rag_engine import rag_engine
from main.safety.sensitive_filter import sensitive_filter

API_KEY = os.getenv("QWEN_API_KEY")
API_URL = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"

class LLMRAGHandler:
    def __init__(self):
        self.rag = rag_engine
        self.filter = sensitive_filter

    async def generate(self, query: str):
        if self.filter.contains_sensitive(query):
            return "检测到内容涉及情绪困扰，请立即联系研究人员或专业心理医生。"

        context = "\n".join(self.rag.retrieve(query))
        payload = {
            "model": "qwen-max",
            "input": f"用户问题：{query}\n参考资料：{context}\n请给出友好的回答："
        }
        headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

        async with httpx.AsyncClient(timeout=60) as client:
            resp = await client.post(API_URL, headers=headers, json=payload)
            resp.raise_for_status()
            data = resp.json()
            return data.get("output", {}).get("text", "抱歉，我暂时无法回答。")

handler = LLMRAGHandler()
