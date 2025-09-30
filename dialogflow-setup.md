# Dialogflow Webhook 手動設定指南

## 🔧 如果自動更新失敗，請手動設定

### 1. 前往 Dialogflow Console
打開瀏覽器，前往：https://dialogflow.cloud.google.com/

### 2. 選擇你的專案
選擇 `stinkyturtle-ntnj` 專案

### 3. 設定 Fulfillment
1. 在左側選單點擊 **Fulfillment**
2. 啟用 **Webhook**
3. 在 **URL** 欄位輸入你的 GCP 應用 webhook URL：
   ```
   https://YOUR_PROJECT_ID.appspot.com/webhook
   ```
   (將 YOUR_PROJECT_ID 替換成你的實際專案 ID)

### 4. 儲存設定
點擊 **SAVE** 按鈕

## 🔍 如何找到你的專案 ID

### 方法 1: 從 GCP Console
1. 前往 https://console.cloud.google.com/
2. 在頂部的專案選擇器中查看專案 ID

### 方法 2: 從應用日誌
在你的應用日誌中會顯示：
```
📦 專案 ID: your-project-id
🌐 應用 URL: https://your-project-id.appspot.com
📱 Webhook URL: https://your-project-id.appspot.com/webhook
```

## 🔐 認證問題解決方案

### 選項 1: 使用 App Engine 預設服務帳戶
1. 前往 [IAM 頁面](https://console.cloud.google.com/iam-admin/iam)
2. 找到 `your-project-id@appspot.gserviceaccount.com`
3. 確保它有 **Dialogflow API Client** 角色

### 選項 2: 建立新的服務帳戶
1. 前往 [服務帳戶頁面](https://console.cloud.google.com/iam-admin/serviceaccounts)
2. 建立新的服務帳戶
3. 給予 **Dialogflow API Client** 角色
4. 下載 JSON 金鑰檔案
5. 將檔案重新命名為 `dialogflow_auth.json`
6. 重新部署應用

## 🧪 測試 Webhook

設定完成後，你可以：
1. 在 Dialogflow Console 中測試對話
2. 檢查 GCP 應用日誌是否收到請求
3. 使用 LINE Bot 測試實際功能

## 📊 檢查日誌
```bash
gcloud app logs tail -s default
```

或前往：https://console.cloud.google.com/logs