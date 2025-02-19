#!/bin/bash

# 更新系统并安装依赖
sudo apt update
sudo apt install python3
sudo apt install python3-pip
sudo pip3 install DrissionPage
sudo pip3 install Pyjwt
sudo pip3 install colorlog

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
chmod +x $TARGET_DIR

# 使用 screen 创建新的会话来执行 Python 脚本
echo "正在执行 Python 脚本 main.py (通过 screen 启动新的会话)..."
screen -dmS nexus_screen sudo python3 $TARGET_DIR/main.py

# 检查 screen 会话是否成功创建
if screen -list | grep -q "nexus_screen"; then
    echo "screen 会话创建成功，准备进入会话..."
else
    echo "创建 screen 会话失败，正在检查..."
    screen -ls  # 列出所有屏幕会话
    exit 1
fi

# 进入 screen 会话
echo "10秒后进入会话..."
echo "screen -r nexus_screen 进入会话， 进入会话后按住CTRL+A然后一起松开，单按K键结束会话"
echo "先按CTRL+A后一起松开，随后单按D键退出screen"
sleep 10  # 等待 3 秒

# 主动进入 screen 会话
screen -r nexus_screen || { echo "无法进入 screen 会话"; exit 1; }
