import asyncio
from main.llm_service.llm_rag_handler import LLMRAGHandler
from main.health_dialogue.dialogue_manager import DialogueManager
from main.utils.wakeup_detector import is_first_wakeup_today

handler = LLMRAGHandler(api_key="你的通义千问API Key")
dialogue = DialogueManager()

async def handle_user_query(query: str):
    if is_first_wakeup_today():
        theme, qs = dialogue.get_daily_questions()
        greeting = f"早上好！今天我们聊聊主题《{theme}》。"
        questions = "；".join(qs)
        return f"{greeting} 我想问问你：{questions}"
    else:
        return await handler.generate(query)
