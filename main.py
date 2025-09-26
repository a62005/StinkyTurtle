#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GCP App Engine 入口點
"""
import os
from linebot import app

# 設置環境變數
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'dialogflow_auth.json'

# 導出 FastAPI 應用供 App Engine 使用
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)