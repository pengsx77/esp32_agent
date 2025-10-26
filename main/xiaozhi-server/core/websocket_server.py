import asyncio
import json
import websockets

TAG = "WebSocketServer"

class WebSocketServer:
    def __init__(self, config, host="0.0.0.0", port=8000, query_handler=None):
        """
        query_handler: 异步函数，接收 query(str) 返回 reply(str)
        """
        self.host = host
        self.port = int(config.get("server", {}).get("port", port))
        self.query_handler = query_handler

    async def _handle_client(self, websocket, path):
        """
        每个客户端连接的处理
        """
        print(f"[{TAG}] 客户端已连接: {websocket.remote_address}")
        try:
            async for message in websocket:
                try:
                    data = json.loads(message)
                    query = data.get("query", "")
                    if not query:
                        await websocket.send(json.dumps({"reply": "没有收到问题"}))
                        continue

                    # 调用集成的功能
                    if self.query_handler:
                        reply = await self.query_handler(query)
                    else:
                        reply = "服务端未配置 query_handler"

                    await websocket.send(json.dumps({"reply": reply}))

                except json.JSONDecodeError:
                    await websocket.send(json.dumps({"reply": "无法解析请求"}))
        except websockets.exceptions.ConnectionClosed:
            print(f"[{TAG}] 客户端断开连接: {websocket.remote_address}")

    async def start(self):
        print(f"[{TAG}] WebSocket服务启动: ws://{self.host}:{self.port}/xiaozhi/v1/")
        async with websockets.serve(self._handle_client, self.host, self.port):
            await asyncio.Future()  # 永远等待
