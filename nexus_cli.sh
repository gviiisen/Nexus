#!/bin/bash

# 更新系统并安装必要的开发工具
echo "更新系统并安装依赖..."
export DEBIAN_FRONTEND=noninteractive
sudo apt update
sudo apt install -y cmake build-essential pkg-config libssl-dev git-all

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

# 启动守护会话
echo "启动守护会话..."
screen -S nexus
