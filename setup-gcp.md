# GCP 部署設定指南

## 1. 安裝 Google Cloud CLI 後的設定步驟

### 初始化 gcloud
```bash
# 登入 Google Cloud
gcloud auth login

# 設定專案 ID（替換成你的專案 ID）
gcloud config set project YOUR_PROJECT_ID

# 確認設定
gcloud config list
```

### 啟用必要的 API
```bash
# 啟用 App Engine API
gcloud services enable appengine.googleapis.com

# 啟用 Cloud Build API
gcloud services enable cloudbuild.googleapis.com

# 啟用 Dialogflow API
gcloud services enable dialogflow.googleapis.com
```

### 建立 App Engine 應用（如果還沒有）
```bash
# 建立 App Engine 應用，選擇地區（建議 asia-east1）
gcloud app create --region=asia-east1
```

## 2. 設定 Cloud Build 自動部署

### 連接 GitHub 儲存庫
1. 前往 [Cloud Build 觸發器頁面](https://console.cloud.google.com/cloud-build/triggers)
2. 點擊「建立觸發器」
3. 選擇「GitHub」作為來源
4. 授權並選擇你的儲存庫
5. 設定觸發條件：
   - 事件：推送到分支
   - 分支：`^main$` 或 `^master$`
   - 組態：Cloud Build 組態檔案 (yaml 或 json)
   - 位置：儲存庫中的 `cloudbuild.yaml`

### 手動部署（第一次）
```bash
# 直接部署
gcloud app deploy

# 或使用 Cloud Build
gcloud builds submit --config cloudbuild.yaml
```

## 3. 環境變數和機密設定

### 上傳 Dialogflow 認證檔案
確保 `dialogflow_auth.json` 檔案在專案根目錄中。

### 檢查部署狀態
```bash
# 查看應用狀態
gcloud app describe

# 查看日誌
gcloud app logs tail -s default

# 開啟瀏覽器查看應用
gcloud app browse
```

## 4. 更新 Webhook URL

部署完成後，你的應用 URL 會是：
`https://YOUR_PROJECT_ID.appspot.com`

需要更新：
1. LINE Bot Webhook URL: `https://YOUR_PROJECT_ID.appspot.com/webhook`
2. Dialogflow Fulfillment URL: `https://YOUR_PROJECT_ID.appspot.com/webhook`

## 5. 自動部署流程

設定完成後，每次推送到 main/master 分支時，Cloud Build 會自動：
1. 拉取最新代碼
2. 建置應用
3. 部署到 App Engine

## 故障排除

### 查看建置日誌
```bash
gcloud builds list
gcloud builds log BUILD_ID
```

### 查看應用日誌
```bash
gcloud app logs tail -s default
```

### 重新部署
```bash
gcloud app deploy --force
```