import sys
import uuid
import signal
import asyncio
from aioconsole import ainput
from config.settings import load_config
from config.logger import setup_logging
from core.utils.util import get_local_ip, validate_mcp_endpoint, check_ffmpeg_installed
from core.http_server import SimpleHttpServer
from core.websocket_server import WebSocketServer

# 新增模块
from main.llm_service.llm_rag_handler import handler
from main.health_dialogue.dialogue_manager import dialogue_manager
from main.utils.wakeup_detector import is_first_wakeup_today

TAG = __name__
logger = setup_logging()

async def handle_user_message(query: str):
    if is_first_wakeup_today():
        theme, qs = dialogue_manager.get_daily_questions()
        greeting = f"早上好！今天主题：{theme}"
        questions = "；".join(qs)
        return f"{greeting} 我想问：{questions}"
    else:
        return await handler.generate(query)

async def wait_for_exit() -> None:
    loop = asyncio.get_running_loop()
    stop_event = asyncio.Event()
    if sys.platform != "win32":
        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(sig, stop_event.set)
        await stop_event.wait()
    else:
        try:
            await asyncio.Future()
        except KeyboardInterrupt:
            pass

async def monitor_stdin():
    while True:
        await ainput()

async def main():
    check_ffmpeg_installed()
    config = load_config()
    auth_key = config["server"].get("auth_key", "")
    if not auth_key or len(auth_key) == 0:
        auth_key = config.get("manager-api", {}).get("secret", "")
        if not auth_key:
            auth_key = str(uuid.uuid4().hex)
    config["server"]["auth_key"] = auth_key

    stdin_task = asyncio.create_task(monitor_stdin())

    ws_server = WebSocketServer(config, query_handler=handle_user_message)
    ws_task = asyncio.create_task(ws_server.start())
    ota_server = SimpleHttpServer(config)
    ota_task = asyncio.create_task(ota_server.start())

    try:
        await wait_for_exit()
    finally:
        stdin_task.cancel()
        ws_task.cancel()
        if ota_task:
            ota_task.cancel()
        await asyncio.wait(
            [stdin_task, ws_task, ota_task] if ota_task else [stdin_task, ws_task],
            timeout=3.0,
            return_when=asyncio.ALL_COMPLETED,
        )
        print("服务器已关闭，程序退出。")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("手动中断，程序终止。")
