#!/bin/bash

echo "📊 檢查 GCP App Engine 日誌..."

# 檢查最新的日誌
echo "最新日誌:"
gcloud app logs tail -s default

echo ""
echo "如果上面的指令不行，試試這些:"
echo "gcloud logging read 'resource.type=gae_app' --limit=50 --format='table(timestamp,severity,textPayload)'"
echo ""
echo "或者直接在瀏覽器查看:"
echo "https://console.cloud.google.com/logs/query"