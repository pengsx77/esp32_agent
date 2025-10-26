import asyncio
import logging
import sys
from core.websocket_server import WebSocketServer
from core.http_server import SimpleHttpServer
from main.llm_service.llm_rag_handler import handler
from main.health_dialogue.dialogue_manager import dialogue_manager
from main.utils.wakeup_detector import is_first_wakeup_today
from config.settings import Settings
from config.logger import setup_logger

def setup():
    setup_logger()
    logging.info("服务端启动中...")

def get_query_handler():
    return handler

def get_daily_questions():
    return dialogue_manager.get_daily_questions()

def is_first_wakeup():
    return is_first_wakeup_today()

def create_servers():
    ws_server = WebSocketServer(query_handler=get_query_handler())
    http_server = SimpleHttpServer()
    return ws_server, http_server

def run():
    setup()
    ws_server, http_server = create_servers()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(ws_server.start())
    loop.run_until_complete(http_server.start())
    loop.run_forever()

if __name__ == "__main__":
    run()
