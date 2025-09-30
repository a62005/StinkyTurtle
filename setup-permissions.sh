#!/bin/bash

echo "🔧 設定 GCP 自動部署權限..."

# 獲取專案 ID
PROJECT_ID=$(gcloud config get-value project)

if [ -z "$PROJECT_ID" ]; then
    echo "❌ 無法獲取專案 ID，請先設定："
    echo "gcloud config set project YOUR_PROJECT_ID"
    exit 1
fi

echo "📦 專案 ID: $PROJECT_ID"

# 設定 App Engine 服務帳戶的 Dialogflow 權限
echo "🔐 設定 App Engine 服務帳戶權限..."
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$PROJECT_ID@appspot.gserviceaccount.com" \
    --role="roles/dialogflow.client"

# 確保 Dialogflow API 已啟用
echo "🔧 啟用 Dialogflow API..."
gcloud services enable dialogflow.googleapis.com

# 確保 App Engine API 已啟用
echo "🔧 啟用 App Engine API..."
gcloud services enable appengine.googleapis.com

echo ""
echo "✅ 權限設定完成！"
echo ""
echo "現在可以部署應用："
echo "gcloud app deploy"
echo ""
echo "部署後，應用會自動："
echo "1. 檢測 GCP 環境"
echo "2. 獲取應用 URL"
echo "3. 自動更新 Dialogflow Webhook"
echo ""
echo "🎉 完全自動化部署完成！"