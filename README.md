# Stinky Turtle LINE Bot

## 快速啟動

### 方法 1：分別啟動（推薦）

1. **啟動 Cloudflare Tunnel**（在第一個終端）：
```bash
python start_tunnel.py
```
等待看到 tunnel URL，例如：`https://xxx.trycloudflare.com`

2. **啟動 LINE Bot 服務器**（在第二個終端）：
```bash
python linebot.py
```

### 方法 2：使用啟動腳本

```bash
chmod +x start.sh
./start.sh
```

## 測試

發送 `#測試` 到你的 LINE Bot 來測試圖片功能。

## 架構

- `linebot.py` - FastAPI 服務器
- `start_tunnel.py` - Cloudflare Tunnel 啟動器
- `handlers/` - 業務邏輯處理
- `utils/` - 工具函數
- `config/` - 配置管理

## 故障排除

如果遇到問題：

1. 確保已安裝 cloudflared：`brew install cloudflared`
2. 檢查端口 8001 是否被占用
3. 確保網絡連接正常
4. 查看終端輸出的錯誤信息