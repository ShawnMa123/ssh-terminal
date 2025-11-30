# Web SSH 客户端 - 子任务规划

## 阶段 1: MVP（最小可行产品）

### 子任务 1.1: 初始化项目目录结构
**目标**: 创建完整的项目目录框架

**交付物**:
- backend/ 目录结构
- frontend/ 目录结构
- docker/ 目录
- 配置文件模板

**Git Commit**: `chore: initialize project directory structure`

---

### 子任务 1.2: 后端基础框架搭建
**目标**: FastAPI 应用基础框架

**文件**:
- `backend/app/main.py` - FastAPI 应用入口
- `backend/app/config.py` - 配置管理
- `backend/requirements.txt` - Python 依赖
- `backend/app/__init__.py`

**功能**:
- FastAPI 应用初始化
- CORS 配置
- 基础路由
- 健康检查接口

**Git Commit**: `feat(backend): setup FastAPI application foundation`

---

### 子任务 1.3: 数据库模型和初始化
**目标**: SQLAlchemy 模型定义和数据库初始化

**文件**:
- `backend/app/database.py` - 数据库连接
- `backend/app/models/server.py` - 服务器模型
- `backend/app/models/session.py` - 会话模型
- `backend/app/models/credential.py` - 凭据模型
- `backend/app/schemas/` - Pydantic schemas

**功能**:
- 数据库连接池
- 模型定义
- 初始化脚本

**Git Commits**:
1. `feat(backend): add database connection and base model`
2. `feat(backend): implement server and session models`
3. `feat(backend): add credential model with encryption support`

---

### 子任务 1.4: SSH 连接核心模块
**目标**: Paramiko SSH 连接封装

**文件**:
- `backend/app/core/ssh_manager.py` - SSH 管理器
- `backend/app/core/ssh_connection.py` - SSH 连接封装

**功能**:
- SSH 连接建立
- PTY 创建
- 认证（密码/私钥）
- 连接管理

**Git Commits**:
1. `feat(backend): implement SSH connection wrapper`
2. `feat(backend): add SSH manager for connection pool`

---

### 子任务 1.5: WebSocket 通信实现
**目标**: WebSocket 端点和双向数据转发

**文件**:
- `backend/app/api/websocket.py` - WebSocket 路由
- `backend/app/core/session_manager.py` - 会话管理器

**功能**:
- WebSocket 连接处理
- 双向数据转发（前端 ↔ SSH）
- 心跳机制
- 终端大小调整

**Git Commit**: `feat(backend): implement WebSocket bidirectional data forwarding`

---

### 子任务 1.6: 前端基础框架
**目标**: Vue 3 + Vite 项目搭建

**文件**:
- `frontend/package.json`
- `frontend/vite.config.js`
- `frontend/src/main.js`
- `frontend/src/App.vue`
- `frontend/index.html`

**功能**:
- Vite 配置
- Vue Router
- Axios 配置
- Element Plus 集成

**Git Commit**: `feat(frontend): setup Vue 3 + Vite project foundation`

---

### 子任务 1.7: xterm.js 终端组件
**目标**: 实现可用的终端界面

**文件**:
- `frontend/src/components/Terminal.vue`
- `frontend/src/api/websocket.js`
- `frontend/src/views/Home.vue`

**功能**:
- xterm.js 初始化
- WebSocket 连接
- 终端数据收发
- 终端自适应

**Git Commits**:
1. `feat(frontend): add xterm.js terminal component`
2. `feat(frontend): implement WebSocket client integration`

---

### 子任务 1.8: Docker 配置文件
**目标**: Docker 容器化配置

**文件**:
- `docker/Dockerfile.backend`
- `docker/Dockerfile.frontend`
- `docker-compose.yml`
- `.dockerignore`
- `.env.example`

**功能**:
- 后端容器配置
- 前端 Nginx 容器
- Docker Compose 编排
- 卷挂载配置

**Git Commit**: `build: add Docker configuration for deployment`

---

### 子任务 1.9: 本地 Docker 部署和测试
**目标**: 完整部署并验证功能

**任务**:
- 构建镜像
- 启动容器
- 测试 SSH 连接
- 验证终端交互
- 文档更新

**文件**:
- `README.md` - 使用说明
- `DEPLOYMENT.md` - 部署指南

**Git Commit**: `docs: add deployment guide and usage instructions`

---

## 提交规范

### Commit Message 格式
```
<type>(<scope>): <subject>

<body>

<footer>
```

### Type 类型
- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 重构
- `test`: 测试相关
- `chore`: 构建/工具配置
- `build`: 构建系统

### Scope 范围
- `backend`: 后端代码
- `frontend`: 前端代码
- `docker`: Docker 相关
- `docs`: 文档

### 示例
```
feat(backend): implement SSH connection wrapper

- Add SSHConnection class to encapsulate Paramiko SSH client
- Support password and private key authentication
- Implement PTY creation with configurable terminal size
- Add connection lifecycle management methods
- Include error handling and logging

Closes #1
```

---

## 验收标准

### 阶段 1 完成标准
- ✅ 可以通过 Web 界面连接 SSH 服务器
- ✅ 终端可以正常交互（输入输出）
- ✅ Docker 容器正常运行
- ✅ 可以通过 VPS IP:端口访问
- ✅ 代码有清晰的 Git 提交历史
