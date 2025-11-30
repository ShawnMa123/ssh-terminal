# Web SSH Client

<div align="center">

**🚀 基于 Web 的现代化 SSH 客户端**

一个功能强大的 Web SSH 终端，类似 MobaXterm、Xshell 和 PuTTY，采用 Docker 容器化部署，提供企业级的远程服务器管理能力。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-ready-2496ED.svg)](https://www.docker.com/)

[功能特性](#功能特性) • [快速开始](#快速开始) • [架构设计](#系统架构) • [开发指南](#开发指南) • [文档](#文档)

</div>

---

## 📖 项目介绍

### 概述

Web SSH Client 是一个完全基于 Web 的 SSH 终端管理系统，旨在提供与传统桌面 SSH 客户端（如 MobaXterm、Xshell、PuTTY）相媲美的功能，同时具备 Web 应用的便捷性和跨平台特性。

### 设计理念

- **🌐 Web 优先**: 无需安装任何客户端，浏览器即可访问
- **🔒 安全第一**: 凭据加密存储，支持 HTTPS/WSS 通信
- **🎯 用户友好**: 直观的操作界面，类似传统桌面客户端的体验
- **🐳 云原生**: 完全容器化，易于部署和扩展
- **📝 可追溯**: 自动记录所有操作日志，便于审计和回溯

### 应用场景

- **运维管理**: 集中管理多台服务器，批量执行命令
- **开发调试**: 快速连接开发/测试环境进行调试
- **远程办公**: 无需 VPN，通过 Web 安全访问内部服务器
- **教育培训**: 为学员提供统一的 SSH 学习环境
- **应急响应**: 任何设备的浏览器都能快速接入处理问题

---

## ✨ 功能特性

### 核心功能

#### 🖥️ Web 终端
- 基于 **xterm.js** 的现代终端模拟器
- 完整的 ANSI 颜色支持和语法高亮
- 支持鼠标选中复制、右键菜单
- 终端窗口自适应调整
- 全键盘快捷键支持（Ctrl+C、Ctrl+V 等）

#### 📊 多会话管理
- 侧边栏展示所有活跃会话
- 支持会话标签页切换
- 会话状态实时显示（活跃/断开/错误）
- 会话分组和标签管理
- 快速会话搜索和过滤

#### 🔐 凭据加密存储
- 使用 **Fernet** 对称加密算法
- 支持密码和 SSH 私钥两种认证方式
- 私钥密码短语加密保护
- 批量密码管理和更新
- 凭据分组和权限控制

#### 📝 自动日志记录
- 所有终端输出实时记录
- 日志按服务器和时间戳分类存储
- 命名规则：`logs/{服务器名}/{服务器名}_{时间戳}.log`
- 支持日志查看、搜索和导出
- 日志文件完整性保护

### 技术特性

#### 🐳 Docker 容器化
- 一键部署，零依赖冲突
- 前后端分离的容器架构
- 数据持久化卷挂载
- 容器健康检查和自动重启
- 支持 Docker Compose 编排

#### 🔒 企业级安全
- 所有敏感数据加密存储
- 支持 HTTPS/WSS 加密传输
- CORS 跨域保护
- SQL 注入防护
- 命令注入防护

#### 🚀 高性能设计
- FastAPI 异步框架，高并发处理
- WebSocket 双向通信，低延迟
- 连接池管理，资源复用
- 异步日志写入，不阻塞主流程
- 数据库查询优化

#### 📊 可观测性
- 健康检查端点（`/health`）
- 自动生成 API 文档（Swagger UI）
- 详细的应用日志
- 容器运行状态监控

---

## 🏗️ 系统架构

### 整体架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                          浏览器客户端                              │
│                                                                   │
│  ┌──────────────┐        ┌────────────────────────────────┐    │
│  │  侧边栏组件   │        │       主终端区域                 │    │
│  │              │        │                                │    │
│  │ • Session列表 │        │  ┌──────────────────────────┐ │    │
│  │ • 新建连接   │        │  │ xterm.js 终端实例 (Tab1) │ │    │
│  │ • 凭据管理   │        │  └──────────────────────────┘ │    │
│  │ • 日志查看   │        │  ┌──────────────────────────┐ │    │
│  │ • 系统设置   │        │  │ xterm.js 终端实例 (Tab2) │ │    │
│  │              │        │  └──────────────────────────┘ │    │
│  └──────────────┘        └────────────────────────────────┘    │
│         │                              │                        │
│         └──────────── HTTP/WebSocket ──┴────────────────────────┤
└─────────────────────────────────────────────────────────────────┘
                                 │
                    ┌────────────┴────────────┐
                    │   Nginx 反向代理         │
                    │  • 静态资源服务          │
                    │  • API 路由转发          │
                    │  • WebSocket 代理        │
                    └────────────┬────────────┘
                                 │
┌─────────────────────────────────────────────────────────────────┐
│                      FastAPI 后端服务                             │
│                                                                   │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                      API 路由层                            │  │
│  │  • REST API: /api/sessions, /api/servers, /api/credentials│  │
│  │  • WebSocket: /ws/{session_id}                            │  │
│  │  • Health Check: /health                                  │  │
│  │  • API Docs: /docs                                        │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                 │                                │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                      核心业务层                            │  │
│  │                                                            │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │  │
│  │  │ SSH Manager  │  │Session Manager│  │Credential Mgr│   │  │
│  │  │ • 连接池     │  │ • 会话状态    │  │ • 加密存储   │   │  │
│  │  │ • PTY 管理   │  │ • 生命周期    │  │ • 批量操作   │   │  │
│  │  └──────────────┘  └──────────────┘  └──────────────┘   │  │
│  │                                                            │  │
│  │  ┌──────────────┐  ┌──────────────┐                      │  │
│  │  │ Logger       │  │ Config Mgr   │                      │  │
│  │  │ • 实时记录   │  │ • 环境变量   │                      │  │
│  │  │ • 文件存储   │  │ • 设置管理   │                      │  │
│  │  └──────────────┘  └──────────────┘                      │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                 │                                │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                      数据访问层                            │  │
│  │  • SQLAlchemy ORM                                         │  │
│  │  • 异步数据库操作                                          │  │
│  │  • 连接池管理                                             │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                 │                                │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                     数据持久化层                           │  │
│  │  • SQLite 数据库 (sessions, credentials, servers)         │  │
│  │  • 文件系统 (日志文件)                                     │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                                 │
                                 │ SSH Protocol (Port 22)
                                 ▼
              ┌─────────────────────────────────────┐
              │        远程 SSH 服务器集群           │
              │  • Production Server (192.168.1.10) │
              │  • Dev Server       (192.168.1.20) │
              │  • Test Server      (192.168.1.30) │
              └─────────────────────────────────────┘
```

### 数据流向

#### 1. SSH 连接建立流程

```
用户操作 → 前端 Vue 组件
    ↓
HTTP POST /api/sessions/create {server_id, cols, rows}
    ↓
FastAPI SessionManager.create_session()
    ↓
SSHManager.create_connection(host, port, username, auth)
    ↓
Paramiko: SSH 连接 + PTY 创建
    ↓
SessionLogger: 创建日志文件
    ↓
返回 session_id
    ↓
前端: 建立 WebSocket 连接 /ws/{session_id}
    ↓
双向数据流开始
```

#### 2. 实时终端交互流程

```
用户键盘输入 → xterm.js onData 事件
    ↓
WebSocket.send(data)
    ↓
后端 WebSocket Handler 接收
    ↓
SSH Channel.send(data)
    ↓
远程服务器执行命令
    ↓
SSH Channel.recv() 接收输出
    ↓
Logger.write() 异步记录日志
    ↓
WebSocket.send(output)
    ↓
xterm.js terminal.write() 渲染输出
```

#### 3. 凭据加密存储流程

```
用户输入密码 → CredentialCreate Schema 验证
    ↓
CredentialManager.encrypt_password(plaintext)
    ↓
Fernet.encrypt() 使用主密钥加密
    ↓
保存加密密文到数据库
    ↓
使用时: CredentialManager.decrypt_password(ciphertext)
    ↓
Fernet.decrypt() 解密
    ↓
返回明文密码用于 SSH 认证
```

### 核心技术组件

#### 后端技术栈

| 组件 | 版本 | 用途 |
|------|------|------|
| **Python** | 3.11 | 编程语言 |
| **FastAPI** | 0.104.1 | Web 框架，提供 REST API 和 WebSocket |
| **Uvicorn** | 0.24.0 | ASGI 服务器，高性能异步处理 |
| **Paramiko** | 3.4.0 | SSH 协议实现，建立 SSH 连接 |
| **SQLAlchemy** | 2.0.23 | ORM 框架，数据库操作 |
| **aiosqlite** | 0.19.0 | 异步 SQLite 驱动 |
| **Cryptography** | 41.0.7 | 加密库（Fernet 算法） |
| **Pydantic** | 2.x | 数据验证和序列化 |
| **aiofiles** | 23.2.1 | 异步文件操作（日志写入） |

#### 前端技术栈

| 组件 | 版本 | 用途 |
|------|------|------|
| **Vue 3** | 3.x | 前端框架（计划中） |
| **Vite** | 4.x | 前端构建工具（计划中） |
| **xterm.js** | 5.x | 终端模拟器（计划中） |
| **Element Plus** | 2.x | UI 组件库（计划中） |
| **Pinia** | 2.x | 状态管理（计划中） |
| **Nginx** | Alpine | Web 服务器和反向代理 |

#### 基础设施

| 组件 | 版本 | 用途 |
|------|------|------|
| **Docker** | 20.10+ | 容器化运行环境 |
| **Docker Compose** | 2.0+ | 多容器编排 |
| **SQLite** | 3.x | 轻量级数据库 |

---

## 📁 项目结构

```
ssh-terminal/
├── backend/                      # 后端 Python 代码
│   ├── app/
│   │   ├── __init__.py          # 应用初始化
│   │   ├── main.py              # FastAPI 应用入口
│   │   ├── config.py            # 配置管理（环境变量）
│   │   ├── database.py          # 数据库连接和会话管理
│   │   │
│   │   ├── api/                 # API 路由层
│   │   │   ├── __init__.py
│   │   │   ├── sessions.py      # 会话管理 API（计划中）
│   │   │   ├── servers.py       # 服务器管理 API（计划中）
│   │   │   ├── credentials.py   # 凭据管理 API（计划中）
│   │   │   ├── logs.py          # 日志查询 API（计划中）
│   │   │   └── websocket.py     # WebSocket 端点（计划中）
│   │   │
│   │   ├── core/                # 核心业务逻辑层
│   │   │   ├── __init__.py
│   │   │   ├── ssh_manager.py   # SSH 连接管理器（计划中）
│   │   │   ├── ssh_connection.py# SSH 连接封装（计划中）
│   │   │   ├── session_manager.py# 会话管理器（计划中）
│   │   │   ├── credential_manager.py# 凭据管理器（计划中）
│   │   │   └── logger.py        # 日志记录器（计划中）
│   │   │
│   │   ├── models/              # SQLAlchemy 数据模型
│   │   │   ├── __init__.py
│   │   │   ├── server.py        # SSH 服务器模型
│   │   │   ├── credential.py    # 凭据模型
│   │   │   └── session.py       # 会话模型
│   │   │
│   │   ├── schemas/             # Pydantic 数据模式
│   │   │   ├── __init__.py
│   │   │   ├── server.py        # 服务器 Schema
│   │   │   ├── credential.py    # 凭据 Schema
│   │   │   └── session.py       # 会话 Schema
│   │   │
│   │   └── utils/               # 工具函数
│   │       ├── __init__.py
│   │       ├── crypto.py        # 加密工具（计划中）
│   │       └── validators.py    # 验证器（计划中）
│   │
│   ├── tests/                   # 测试代码
│   │   └── .gitkeep
│   │
│   └── requirements.txt         # Python 依赖列表
│
├── frontend/                    # 前端代码
│   ├── dist/                    # 构建输出（当前为 MVP 版本）
│   │   └── index.html           # MVP 测试页面
│   │
│   ├── src/                     # Vue 源代码（计划中）
│   │   ├── main.js
│   │   ├── App.vue
│   │   ├── router/              # 路由配置
│   │   ├── stores/              # Pinia 状态管理
│   │   ├── components/          # Vue 组件
│   │   │   ├── layout/          # 布局组件
│   │   │   ├── terminal/        # 终端组件
│   │   │   ├── session/         # 会话管理组件
│   │   │   ├── credential/      # 凭据管理组件
│   │   │   └── logs/            # 日志查看组件
│   │   ├── views/               # 页面视图
│   │   ├── api/                 # API 客户端封装
│   │   └── utils/               # 工具函数
│   │
│   ├── public/                  # 静态资源
│   │   └── .gitkeep
│   │
│   ├── package.json             # Node.js 依赖（计划中）
│   └── vite.config.js           # Vite 配置（计划中）
│
├── docker/                      # Docker 配置文件
│   ├── Dockerfile.backend       # 后端镜像构建
│   ├── Dockerfile.frontend      # 前端镜像构建
│   └── nginx.conf               # Nginx 配置
│
├── logs/                        # SSH 会话日志存储
│   └── .gitkeep
│
├── data/                        # 数据库文件存储
│   └── .gitkeep
│
├── docker-compose.yml           # Docker Compose 编排
├── .env.example                 # 环境变量模板
├── .env                         # 环境变量（不提交到 Git）
├── .gitignore                   # Git 忽略规则
│
├── README.md                    # 项目说明（本文件）
├── DESIGN.md                    # 详细设计文档
├── TASKS.md                     # 开发任务规划
├── DEPLOYMENT.md                # 部署指南
└── LICENSE                      # MIT 许可证
```

---

## 🚀 快速开始

### 前置要求

- **Docker**: 20.10 或更高版本
- **Docker Compose**: 2.0 或更高版本
- **Git**: 用于克隆仓库

检查版本：
```bash
docker --version
docker compose version
```

### 一键部署

#### 1. 克隆仓库

```bash
git clone https://github.com/ShawnMa123/ssh-terminal.git
cd ssh-terminal
```

#### 2. 配置环境变量

```bash
# 复制环境变量模板
cp .env.example .env

# 生成加密密钥
python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"

# 编辑 .env 文件，将生成的密钥填入 ENCRYPTION_KEY
vi .env
```

`.env` 配置示例：
```bash
DATABASE_URL=sqlite+aiosqlite:///./data/ssh_client.db
ENCRYPTION_KEY=u6UEoDuI6AcOSvakMRw4hZh83tj37UNUReS7Ml6iGDc=
LOG_DIR=./logs
DEBUG=true
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:80
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
```

#### 3. 启动服务

```bash
# 构建并启动容器
docker compose up -d

# 查看容器状态
docker compose ps

# 查看日志
docker compose logs -f
```

#### 4. 访问应用

- **Web 界面**: http://localhost
- **API 文档**: http://localhost:8000/docs
- **健康检查**: http://localhost:8000/health

如果部署在远程服务器，将 `localhost` 替换为服务器 IP 地址。

---

## 🐳 Docker 使用指南

### Docker Compose 命令

#### 启动服务
```bash
# 后台启动
docker compose up -d

# 前台启动（可查看实时日志）
docker compose up

# 仅启动指定服务
docker compose up -d backend
docker compose up -d frontend
```

#### 停止服务
```bash
# 停止所有容器（保留容器）
docker compose stop

# 停止并删除容器
docker compose down

# 停止并删除容器、网络、卷
docker compose down -v
```

#### 查看状态
```bash
# 查看容器状态
docker compose ps

# 查看详细信息
docker compose ps -a

# 查看资源使用情况
docker stats
```

#### 查看日志
```bash
# 查看所有容器日志
docker compose logs

# 实时跟踪日志
docker compose logs -f

# 查看特定服务日志
docker compose logs backend
docker compose logs frontend

# 查看最近 100 行日志
docker compose logs --tail=100

# 查看带时间戳的日志
docker compose logs -t
```

#### 重启服务
```bash
# 重启所有服务
docker compose restart

# 重启特定服务
docker compose restart backend
docker compose restart frontend
```

#### 重新构建
```bash
# 重新构建所有镜像
docker compose build

# 重新构建特定服务
docker compose build backend

# 无缓存重新构建
docker compose build --no-cache

# 重新构建并启动
docker compose up -d --build
```

#### 进入容器
```bash
# 进入后端容器
docker compose exec backend sh

# 进入前端容器
docker compose exec frontend sh

# 以 root 用户进入
docker compose exec -u root backend sh
```

#### 执行命令
```bash
# 在后端容器执行 Python 命令
docker compose exec backend python -c "print('Hello')"

# 查看后端容器文件
docker compose exec backend ls -la /app

# 查看前端 Nginx 配置
docker compose exec frontend cat /etc/nginx/nginx.conf
```

### 容器配置说明

#### 后端容器 (ssh-client-backend)

**基础镜像**: `python:3.11-slim`

**端口映射**: `8000:8000`

**卷挂载**:
- `./logs:/app/logs` - 日志存储
- `./data:/app/data` - 数据库存储

**环境变量**:
- `DATABASE_URL` - 数据库连接字符串
- `ENCRYPTION_KEY` - 加密主密钥
- `LOG_DIR` - 日志目录
- `DEBUG` - 调试模式
- `ALLOWED_ORIGINS` - CORS 允许的源
- `BACKEND_HOST` - 监听地址
- `BACKEND_PORT` - 监听端口

**健康检查**:
```yaml
test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
interval: 30s
timeout: 10s
retries: 3
start_period: 40s
```

#### 前端容器 (ssh-client-frontend)

**基础镜像**: `nginx:alpine`

**端口映射**: `80:80`

**配置文件**: `docker/nginx.conf`

**功能**:
- 静态文件服务
- API 反向代理 (`/api/*` → `backend:8000`)
- WebSocket 代理 (`/ws/*` → `backend:8000`)
- 健康检查代理 (`/health` → `backend:8000/health`)

### 数据持久化

#### 重要数据目录

| 宿主机路径 | 容器内路径 | 说明 |
|-----------|-----------|------|
| `./logs/` | `/app/logs` | SSH 会话日志文件 |
| `./data/` | `/app/data` | SQLite 数据库文件 |

#### 备份数据

```bash
# 备份数据库
cp data/ssh_client.db data/ssh_client.db.backup

# 备份日志
tar -czf logs_backup_$(date +%Y%m%d).tar.gz logs/

# 备份所有数据
tar -czf ssh_client_backup_$(date +%Y%m%d).tar.gz data/ logs/
```

#### 恢复数据

```bash
# 停止服务
docker compose down

# 恢复数据库
cp data/ssh_client.db.backup data/ssh_client.db

# 恢复日志
tar -xzf logs_backup_20231201.tar.gz

# 重启服务
docker compose up -d
```

### 故障排查

#### 容器无法启动

**检查日志**:
```bash
docker compose logs backend
docker compose logs frontend
```

**常见问题**:
1. 端口被占用 → 修改 `docker-compose.yml` 中的端口映射
2. 权限问题 → 检查 `logs/` 和 `data/` 目录权限
3. 环境变量错误 → 检查 `.env` 文件配置

#### 后端 API 无法访问

**检查容器状态**:
```bash
docker compose ps
```

**测试后端连接**:
```bash
curl http://localhost:8000/health
```

**检查 Nginx 配置**:
```bash
docker compose exec frontend nginx -t
```

#### WebSocket 连接失败

**检查 Nginx 配置**:
```bash
docker compose exec frontend cat /etc/nginx/nginx.conf | grep -A 10 "location /ws"
```

**查看 WebSocket 代理日志**:
```bash
docker compose logs frontend | grep ws
```

#### 数据库问题

**进入容器检查**:
```bash
docker compose exec backend sh
cd /app/data
ls -la
sqlite3 ssh_client.db ".tables"
```

**重新初始化数据库**:
```bash
docker compose down
rm data/ssh_client.db
docker compose up -d
```

---

## 💻 本地开发

### 后端开发

#### 环境准备

```bash
cd backend

# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt
```

#### 运行开发服务器

```bash
# 确保已配置 .env 文件
cd ..
cp .env.example .env
vi .env

# 启动 FastAPI 开发服务器（支持热重载）
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

访问：
- API 服务: http://localhost:8000
- 交互式文档: http://localhost:8000/docs
- ReDoc 文档: http://localhost:8000/redoc

#### 数据库迁移

```bash
# 创建迁移脚本（使用 Alembic）
alembic revision --autogenerate -m "描述"

# 应用迁移
alembic upgrade head

# 回滚迁移
alembic downgrade -1
```

#### 运行测试

```bash
# 安装测试依赖
pip install pytest pytest-asyncio pytest-cov

# 运行所有测试
pytest

# 运行测试并生成覆盖率报告
pytest --cov=app --cov-report=html
```

### 前端开发（计划中）

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 构建生产版本
npm run build

# 预览生产构建
npm run preview
```

---

## 📚 代码流程详解

### 1. 应用启动流程

```python
# backend/app/main.py

# 1. 导入依赖
from fastapi import FastAPI
from app.config import settings

# 2. 创建 FastAPI 应用实例
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时执行
    print("🚀 Starting application...")
    # 初始化数据库连接
    # 加载配置
    # 启动后台任务

    yield

    # 关闭时执行
    print("👋 Shutting down...")
    # 关闭数据库连接
    # 清理资源

app = FastAPI(lifespan=lifespan)

# 3. 配置 CORS
app.add_middleware(CORSMiddleware, ...)

# 4. 注册路由
app.include_router(sessions.router)
app.include_router(servers.router)
...

# 5. Uvicorn 启动服务器
# uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 2. SSH 连接建立流程（计划实现）

```python
# 用户请求创建 SSH 会话

# 1. API 端点接收请求
@router.post("/api/sessions/create")
async def create_session(request: SessionCreate, db: AsyncSession):
    # 2. 验证请求参数
    # 3. 从数据库获取服务器配置
    server = await get_server(db, request.server_id)

    # 4. 获取并解密凭据
    credential = await credential_manager.get_credential(server.credential_id)

    # 5. 创建 SSH 连接
    session_id = str(uuid.uuid4())
    ssh_conn = await ssh_manager.create_connection(
        session_id=session_id,
        host=server.host,
        port=server.port,
        username=server.username,
        password=credential['password'],  # 已解密
        private_key=credential['private_key']
    )

    # 6. 打开 PTY (伪终端)
    await ssh_conn.open_shell(cols=80, rows=24)

    # 7. 创建日志记录器
    logger = SessionLogger(
        session_id=session_id,
        server_name=server.name,
        log_dir=settings.log_dir
    )

    # 8. 保存会话到数据库
    session = SSHSession(
        session_id=session_id,
        server_id=server.id,
        status="active",
        log_file_path=logger.log_file_path
    )
    await db.add(session)
    await db.commit()

    # 9. 返回 session_id
    return {"session_id": session_id}
```

### 3. WebSocket 双向通信流程（计划实现）

```python
# WebSocket 端点

@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    # 1. 接受 WebSocket 连接
    await websocket.accept()

    # 2. 获取 SSH 连接实例
    ssh_conn = ssh_manager.get_connection(session_id)
    if not ssh_conn:
        await websocket.close(code=1008)
        return

    # 3. 启动双向数据转发任务
    try:
        await asyncio.gather(
            # 前端 → SSH
            forward_client_to_ssh(websocket, ssh_conn),
            # SSH → 前端
            forward_ssh_to_client(ssh_conn, websocket),
            # 心跳保持
            heartbeat_task(websocket)
        )
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        await ssh_conn.close()


async def forward_client_to_ssh(websocket: WebSocket, ssh_conn: SSHConnection):
    """前端输入 → SSH 服务器"""
    while True:
        # 1. 接收前端数据
        data = await websocket.receive_bytes()

        # 2. 特殊命令处理（如终端大小调整）
        if is_resize_command(data):
            cols, rows = parse_resize(data)
            await ssh_conn.resize_pty(cols, rows)
            continue

        # 3. 发送到 SSH 服务器
        await ssh_conn.send_data(data)


async def forward_ssh_to_client(ssh_conn: SSHConnection, websocket: WebSocket):
    """SSH 服务器输出 → 前端显示"""
    while True:
        # 1. 从 SSH 通道读取数据
        data = await ssh_conn.recv_data()

        if not data:
            break

        # 2. 记录日志（异步）
        asyncio.create_task(ssh_conn.logger.write(data))

        # 3. 发送到前端
        await websocket.send_bytes(data)
```

### 4. 凭据加密解密流程

```python
# backend/app/core/credential_manager.py

class CredentialManager:
    def __init__(self, encryption_key: str):
        # 初始化 Fernet 加密器
        self.cipher = Fernet(encryption_key.encode())

    def encrypt_password(self, password: str) -> str:
        """加密密码"""
        # 1. 转换为字节
        password_bytes = password.encode('utf-8')

        # 2. Fernet 加密
        encrypted = self.cipher.encrypt(password_bytes)

        # 3. 转换为字符串存储
        return encrypted.decode('utf-8')

    def decrypt_password(self, encrypted: str) -> str:
        """解密密码"""
        # 1. 转换为字节
        encrypted_bytes = encrypted.encode('utf-8')

        # 2. Fernet 解密
        decrypted = self.cipher.decrypt(encrypted_bytes)

        # 3. 转换为字符串返回
        return decrypted.decode('utf-8')

    async def save_credential(self, name: str, password: str):
        """保存加密的凭据"""
        # 1. 加密密码
        encrypted_password = self.encrypt_password(password)

        # 2. 保存到数据库
        credential = Credential(
            name=name,
            credential_type="password",
            encrypted_password=encrypted_password
        )
        db.add(credential)
        await db.commit()
```

### 5. 日志记录流程

```python
# backend/app/core/logger.py

class SessionLogger:
    def __init__(self, session_id: str, server_name: str, log_dir: str):
        self.session_id = session_id
        self.server_name = server_name

        # 生成日志文件路径
        # logs/{server_name}/{server_name}_{timestamp}.log
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        server_dir = os.path.join(log_dir, server_name)
        os.makedirs(server_dir, exist_ok=True)

        self.log_file_path = os.path.join(
            server_dir,
            f"{server_name}_{timestamp}.log"
        )

        # 缓冲区（提高性能）
        self.buffer = []
        self.buffer_size = 1024

    async def write(self, data: bytes):
        """异步写入日志"""
        # 1. 添加到缓冲区
        self.buffer.append(data)

        # 2. 缓冲区满时刷新
        if len(self.buffer) >= self.buffer_size:
            await self._flush()

    async def _flush(self):
        """刷新缓冲区到文件"""
        if not self.buffer:
            return

        # 异步写入文件
        async with aiofiles.open(self.log_file_path, 'ab') as f:
            await f.write(b''.join(self.buffer))

        # 清空缓冲区
        self.buffer.clear()

    async def close(self):
        """关闭日志，刷新剩余数据"""
        await self._flush()
```

---

## 📖 文档

- **[DESIGN.md](./DESIGN.md)** - 详细的技术架构和设计规范
  - 技术栈选型
  - 系统架构设计
  - 数据库设计
  - 核心功能模块设计
  - 前端组件结构
  - 安全考虑

- **[TASKS.md](./TASKS.md)** - 开发任务拆分和提交规范
  - 子任务规划
  - Git 提交规范
  - 验收标准

- **[DEPLOYMENT.md](./DEPLOYMENT.md)** - 部署指南
  - 访问信息
  - 容器状态
  - 常用命令
  - 故障排查

---

## 🔐 安全建议

### 生产环境部署

#### 1. 更换加密密钥

```bash
# 生成新的强加密密钥
python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"

# 更新 .env 文件
ENCRYPTION_KEY=新生成的密钥
```

⚠️ **警告**: 更换密钥后，已加密的旧凭据将无法解密！

#### 2. 启用 HTTPS

配置 SSL 证书（推荐使用 Let's Encrypt）：

```nginx
# docker/nginx.conf
server {
    listen 443 ssl http2;
    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;

    # 其他配置...
}
```

#### 3. 关闭调试模式

```bash
# .env
DEBUG=false
```

#### 4. 限制 CORS 来源

```bash
# .env
ALLOWED_ORIGINS=https://yourdomain.com
```

#### 5. 配置防火墙

```bash
# 仅允许特定 IP 访问
ufw allow from 192.168.1.0/24 to any port 80
ufw allow from 192.168.1.0/24 to any port 8000
```

#### 6. 添加认证授权（计划中）

- JWT Token 认证
- 用户角色权限控制
- API 密钥管理

---

## 🤝 贡献指南

欢迎贡献代码！请遵循以下步骤：

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'feat: add some amazing feature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

### Commit 规范

遵循 [Conventional Commits](https://www.conventionalcommits.org/)：

- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `style`: 代码格式（不影响功能）
- `refactor`: 重构
- `test`: 测试相关
- `chore`: 构建/工具配置

---

## 📄 开源协议

本项目采用 [MIT License](./LICENSE) 开源协议。

---

## 🙏 致谢

本项目使用了以下优秀的开源项目：

- [FastAPI](https://fastapi.tiangolo.com/) - 现代 Python Web 框架
- [Paramiko](https://www.paramiko.org/) - Python SSH 实现
- [xterm.js](https://xtermjs.org/) - Web 终端模拟器
- [Vue.js](https://vuejs.org/) - 渐进式 JavaScript 框架
- [SQLAlchemy](https://www.sqlalchemy.org/) - Python SQL 工具包
- [Docker](https://www.docker.com/) - 容器化平台

---

## 📮 联系方式

- **GitHub**: [ShawnMa123/ssh-terminal](https://github.com/ShawnMa123/ssh-terminal)
- **Issues**: [提交问题](https://github.com/ShawnMa123/ssh-terminal/issues)

---

<div align="center">

**如果这个项目对你有帮助，请给一个 ⭐️ Star！**

Made with ❤️ by ShawnMa123

</div>
