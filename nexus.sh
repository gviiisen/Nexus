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


TARGET_DIR="/home/nexus"

# 创建目标目录（如果不存在）
mkdir -p $TARGET_DIR

# 下载 Python 脚本和 SH 文件
echo "正在下载 Python 脚本..."
wget https://github.com/gviiisen/Nexus/raw/main/logging_config.py -P $TARGET_DIR
wget https://github.com/gviiisen/Nexus/raw/main/main.py -P $TARGET_DIR

# 授权执行权限
chmod +x $TARGET_DIR

# 使用 screen 创建新的会话来执行 Python 脚本，这样脚本能和用户交互
echo "正在执行 Python 脚本 main.py (通过 screen 启动新的会话)..."
screen -dmS main_py_session sudo python3 $TARGET_DIR/main.py

# 执行后续操作
echo "Python 脚本已在新的 screen 会话中执行，您可以通过 'screen -r main_py_session' 来查看输出。"