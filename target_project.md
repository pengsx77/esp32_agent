xiaozhi-esp32-server/
│
├─ app.py                                  # 原文件，保持不变
│
├─ main/
│  ├─ rag/
│  │   ├─ rag_engine.py                    # 向量检索核心逻辑（FAISS + Embedding）
│  │   ├─ rag_data/
│  │   │   ├─ knowledge_texts.json         # 示例健康知识库
│  │   │   └─ index.faiss                  # （运行后自动生成）
│  │   └─ __init__.py
│  │
│  ├─ llm_service/
│  │   ├─ llm_rag_handler.py               # 结合RAG与通义千问调用
│  │   └─ __init__.py
│  │
│  ├─ health_dialogue/
│  │   ├─ dialogue_manager.py              # 每日问诊逻辑控制器
│  │   ├─ questions.json                   # 问诊主题题库配置
│  │   └─ __init__.py
│  │
│  ├─ safety/
│  │   ├─ sensitive_filter.py              # 敏感词识别与干预
│  │   └─ __init__.py
│  │
│  ├─ utils/
│  │   ├─ wakeup_detector.py               # 每日首次唤醒检测逻辑
│  │   └─ __init__.py
│  │
│  ├─ server_rag_entry.py                  # 新增服务端路由入口（供 WebSocket 调用）
│  │
│  └─ __init__.py
│
├─ requirements.txt                        # 新依赖
├─ Dockerfile-server                       # 新增构建命令
└─ README-RAG.md                           # 部署与运行说明
