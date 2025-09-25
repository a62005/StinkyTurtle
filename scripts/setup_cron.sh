#!/bin/bash
# 設置 cron job 的腳本

# 獲取當前腳本的絕對路徑
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
PYTHON_SCRIPT="$PROJECT_DIR/scripts/update_image.py"

# 檢查 Python 腳本是否存在
if [ ! -f "$PYTHON_SCRIPT" ]; then
    echo "錯誤: 找不到 Python 腳本 $PYTHON_SCRIPT"
    exit 1
fi

# 設置 cron job (每天 13:50 執行)
CRON_JOB="50 13 * * * cd $PROJECT_DIR && python3 $PYTHON_SCRIPT >> /tmp/linebot_update.log 2>&1"

# 添加到 crontab
(crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -

echo "Cron job 已設置："
echo "$CRON_JOB"
echo ""
echo "日誌文件位置: /tmp/linebot_update.log"
echo "查看當前 cron jobs: crontab -l"
echo "移除 cron job: crontab -e (然後刪除對應行)"