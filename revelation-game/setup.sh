#!/bin/bash

# 《啓示路：樂土之門》安裝腳本

echo "🌊 開始安裝《啓示路：樂土之門》Discord Bot..."

# 檢查 Python 版本
echo "🐍 檢查 Python 版本..."
python3 --version || {
    echo "❌ 錯誤：未找到 Python 3"
    exit 1
}

# 創建虛擬環境 (可選)
read -p "是否創建 Python 虛擬環境？(y/n) " create_venv
if [ "$create_venv" = "y" ]; then
    echo "📦 創建虛擬環境..."
    python3 -m venv venv
    source venv/bin/activate
fi

# 安裝依賴
echo "📦 安裝依賴..."
pip install -r requirements.txt

# 檢查 .env 文件
if [ ! -f .env ]; then
    echo "⚠️  未找到 .env 文件"
    echo "📝 請複製 .env.example 並填入你的 Discord Bot Token:"
    echo "   cp .env.example .env"
    echo "   然後編輯 .env 文件，填入 DISCORD_TOKEN"
    echo ""
    read -p "是否現在創建 .env 文件？(y/n) " create_env
    if [ "$create_env" = "y" ]; then
        cp .env.example .env
        echo "✅ .env 文件已創建，請編輯並填入 Token"
        echo "   nano .env 或 vim .env"
    fi
fi

echo ""
echo "✅ 安裝完成！"
echo ""
echo "🚀 啟動 Bot:"
echo "   python bot.py"
echo ""
echo "📖 查看幫助:"
echo "   cat README.md"
echo ""
