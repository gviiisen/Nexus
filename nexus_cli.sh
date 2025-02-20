#!/bin/bash

# 更新系统并安装必要的开发工具
echo "更新系统并安装依赖..."
sudo apt update
sudo apt install -y build-essential pkg-config libssl-dev git-all

# 安装协议编译器 (Protobuf)
echo "安装协议编译器..."
sudo apt install -y protobuf-compiler

# 安装 Rust 语言环境
echo "一键安装最新 Rust 工具链..."
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# 激活环境变量
echo "激活 Rust 环境变量..."
source $HOME/.cargo/env

# 添加特殊编译目标
echo "添加特殊编译目标..."
rustup target add riscv32i-unknown-none-elf

# 安装解压工具
echo "安装解压工具..."
sudo apt install -y unzip

# 下载并配置 Protoc 21.3 专用版本
echo "下载并配置 Protoc 21.3..."
wget https://github.com/protocolbuffers/protobuf/releases/download/v21.3/protoc-21.3-linux-x86_64.zip
unzip protoc-21.3-linux-x86_64.zip -d /usr/local

echo "设置内存优化方案..."
sudo swapoff -a
# 设置 swap 大小为 2GB 或 4GB
sudo fallocate -l 2G /swapfile    # 缩小为 2GB，避免占用过多磁盘空间
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# 系统内存策略调整
echo "调整系统内存策略..."
# 设置系统更倾向于使用内存而不是交换
sudo sysctl -w vm.swappiness=10  # 将 swap 使用优先级降低
echo 'vm.swappiness=10' | sudo tee -a /etc/sysctl.conf

# 调整过度分配内存策略
sudo sysctl -w vm.overcommit_memory=1
echo 'vm.overcommit_memory=1' | sudo tee -a /etc/sysctl.conf


# 启动守护会话
echo "启动守护会话..."
screen -S nexus
