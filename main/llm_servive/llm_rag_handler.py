import httpx
from main.rag.rag_engine import RAGEngine
from main.safety.sensitive_filter import SensitiveFilter

class LLMRAGHandler:
    def __init__(self, api_key=None, endpoint="https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"):
        self.api_key = api_key
        self.endpoint = endpoint
        self.rag = RAGEngine()
        self.filter = SensitiveFilter()

    async def generate(self, query):
        # 检查敏感词
        if self.filter.contains_sensitive(query):
            return "我注意到你的内容涉及到情绪困扰，建议你立即联系研究人员或专业的心理医生获得帮助。"

        # 检索知识
        related = self.rag.retrieve(query)
        context = "\n".join(related)

        payload = {
            "model": "qwen-max",
            "input": f"用户问题：{query}\n\n参考资料：{context}\n\n请给出自然友好的回答："
        }

        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}

        async with httpx.AsyncClient(timeout=60) as client:
            resp = await client.post(self.endpoint, headers=headers, json=payload)
            resp.raise_for_status()
            data = resp.json()
            return data.get("output", {}).get("text", "抱歉，我暂时无法回答。")
