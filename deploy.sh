#!/bin/bash

# GCP 部署腳本
echo "🚀 開始部署到 Google Cloud Platform..."

# 檢查是否已安裝 gcloud CLI
if ! command -v gcloud &> /dev/null; then
    echo "❌ gcloud CLI 未安裝"
    echo "請先安裝 Google Cloud CLI: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# 檢查是否已登入
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
    echo "🔐 請先登入 Google Cloud..."
    gcloud auth login
fi

# 設定專案 ID（如果尚未設定）
if [ -z "$GOOGLE_CLOUD_PROJECT" ]; then
    echo "📝 請輸入你的 GCP 專案 ID:"
    read -r PROJECT_ID
    gcloud config set project "$PROJECT_ID"
    export GOOGLE_CLOUD_PROJECT="$PROJECT_ID"
else
    PROJECT_ID="$GOOGLE_CLOUD_PROJECT"
fi

echo "📦 使用專案: $PROJECT_ID"

# 啟用必要的 API
echo "🔧 啟用必要的 Google Cloud APIs..."
gcloud services enable appengine.googleapis.com
gcloud services enable dialogflow.googleapis.com

# 檢查 App Engine 應用是否存在
if ! gcloud app describe &> /dev/null; then
    echo "🏗️  建立 App Engine 應用..."
    echo "請選擇地區 (建議: asia-east1 for 台灣):"
    gcloud app create
fi

# 部署應用
echo "🚀 部署應用到 App Engine..."
gcloud app deploy app.yaml --quiet

# 獲取應用 URL
APP_URL=$(gcloud app describe --format="value(defaultHostname)")
WEBHOOK_URL="https://$APP_URL/webhook"

echo ""
echo "✅ 部署完成！"
echo "🌐 應用 URL: https://$APP_URL"
echo "📱 Webhook URL: $WEBHOOK_URL"
echo ""
echo "📋 接下來的步驟:"
echo "1. 更新 LINE Bot 的 Webhook URL 為: $WEBHOOK_URL"
echo "2. 更新 Dialogflow 的 Fulfillment URL 為: $WEBHOOK_URL"
echo "3. 確認所有環境變數和認證檔案都已正確設定"
echo ""
echo "📊 查看日誌: gcloud app logs tail -s default"
echo "🔧 管理應用: https://console.cloud.google.com/appengine"