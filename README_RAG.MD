# 小智 ESP32 服务器 - RAG 增强版

## 依赖安装
```bash
pip install -r requirements.txt

构建与运行
docker build -t xiaozhi-server .
docker run -p 8000:8000 -p 8003:8003 xiaozhi-server

功能说明

每日首次唤醒 → 自动触发健康问诊

后续唤醒 → 普通对话模式（调用通义千问 + RAG）

敏感词自动过滤

支持本地知识库检索 (FAISS)