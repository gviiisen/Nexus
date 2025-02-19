#!/bin/bash

# 更新系统并安装依赖
sudo apt update
sudo apt install -y python3 python3-pip screen
sudo pip3 install DrissionPage Pyjwt colorlog

# 创建并设置文件夹权限
sudo mkdir -p /home/dp_data
sudo chmod 777 /home/dp_data

# 下载并安装 Google Chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install -y ./google-chrome-stable_current_amd64.deb

# 设置目标目录
TARGET_DIR="/home/nexus"

# 创建目标目录（如果不存在）
mkdir -p $TARGET_DIR

# 下载 Python 脚本和 SH 文件
echo "正在下载 Python 脚本..."
wget https://github.com/gviiisen/Nexus/raw/main/logging_config.py -P $TARGET_DIR
wget https://github.com/gviiisen/Nexus/raw/main/main.py -P $TARGET_DIR

# 授权执行权限
chmod +x $TARGET_DIR/main.py

# 检查是否已存在 nexus_screen 会话
if screen -list | grep -q "nexus_screen"; then
    echo "检测到已存在的 nexus_screen 会话，请先关闭旧会话："
    echo "运行 'screen -r nexus_screen' 进入会话，按 Ctrl+A, K 结束会话"
    exit 1
fi

# 使用 screen 创建新的会话来执行 Python 脚本
echo "正在执行 Python 脚本 main.py (通过 screen 启动新的会话)..10秒后将自动进入会话"
screen -dmS nexus_screen python3 $TARGET_DIR/main.py

# 等待 2 秒，确保会话有时间启动
sleep 2

# 检查 screen 会话是否成功创建
if screen -list | grep -q "nexus_screen"; then
    echo "screen 会话创建成功"
    echo "请使用以下命令进入会话，与 main.py 交互："
    echo "  screen -r nexus_screen"
    echo "交互提示："
    echo "  - 在会话中，按 Ctrl+A, D 分离会话（关闭 shell 后脚本继续运行）"
    echo "  - 再次运行 'screen -r nexus_screen' 可重新进入会话"
    echo "  - 在会话中，按 Ctrl+A, K 结束会话（停止脚本运行）"
    echo "现在将自动进入会话..."
    sleep 10
    screen -r nexus_screen || { echo "无法进入 screen 会话"; exit 1; }
else
    echo "创建 screen 会话失败，正在检查..."
    screen -ls  # 列出所有屏幕会话
    echo "可能的原因："
    echo "1. Python 脚本启动失败，请手动运行 python3 $TARGET_DIR/main.py 检查错误。"
    echo "2. screen 会话立即退出，请检查脚本是否有权限或依赖问题。"
    exit 1
fi

