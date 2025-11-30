# Web SSH Client

一个基于 Web 的 SSH 客户端，类似 MobaXterm/Xshell/PuTTY，支持 Docker 部署。

## 功能特性

### 核心功能
- ✅ **Web 终端界面** - 基于 xterm.js 的现代终端模拟器
- ✅ **多会话管理** - 侧边栏管理多个 SSH 连接
- ✅ **凭据加密存储** - 使用 Fernet 加密保存密码和私钥
- ✅ **批量密码管理** - 支持批量更新多个服务器密码
- ✅ **自动日志记录** - 所有会话自动记录并按时间戳保存
- ✅ **语法高亮** - 终端支持 ANSI 颜色语法高亮
- ✅ **选中复制** - 鼠标选中自动复制到剪贴板

### 技术特性
- 🐳 **Docker 部署** - 一键启动，跨平台兼容
- 🔒 **安全加密** - 凭据加密存储，HTTPS/WSS 通信
- 🚀 **高性能** - 异步 WebSocket，低延迟交互
- 📊 **实时同步** - 前后端 WebSocket 实时双向通信

## 技术栈

### 后端
- **FastAPI** - 现代异步 Web 框架
- **Paramiko** - SSH 协议实现
- **SQLAlchemy** - ORM 和数据库管理
- **Cryptography** - 加密库

### 前端
- **Vue 3** - 渐进式前端框架
- **Vite** - 下一代前端构建工具
- **xterm.js** - 终端模拟器
- **Element Plus** - UI 组件库

## 快速开始

### 前置要求
- Docker 20.10+
- Docker Compose 2.0+

### 部署步骤

1. **克隆仓库**
```bash
git clone <repository-url>
cd ssh-terminal
```

2. **配置环境变量**
```bash
cp .env.example .env
# 编辑 .env 文件，设置加密密钥
```

3. **生成加密密钥**
```bash
python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
# 将输出的密钥复制到 .env 的 ENCRYPTION_KEY
```

4. **启动服务**
```bash
docker-compose up -d
```

5. **访问应用**
```
http://<your-vps-ip>:80
```

### 本地开发

#### 后端开发
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### 前端开发
```bash
cd frontend
npm install
npm run dev
```

## 项目结构

```
ssh-terminal/
├── backend/              # FastAPI 后端
│   ├── app/
│   │   ├── api/         # API 路由
│   │   ├── core/        # 核心业务逻辑
│   │   ├── models/      # 数据库模型
│   │   ├── schemas/     # Pydantic schemas
│   │   └── utils/       # 工具函数
│   └── requirements.txt
├── frontend/            # Vue 3 前端
│   ├── src/
│   │   ├── components/  # Vue 组件
│   │   ├── views/       # 页面视图
│   │   ├── api/         # API 封装
│   │   └── stores/      # Pinia 状态管理
│   └── package.json
├── docker/              # Docker 配置
│   ├── Dockerfile.backend
│   └── Dockerfile.frontend
├── docker-compose.yml
├── logs/               # 日志存储目录
└── data/               # 数据库存储目录
```

## 使用指南

### 添加 SSH 服务器
1. 点击侧边栏「新建连接」按钮
2. 填写服务器信息（名称、主机、端口、用户名）
3. 选择认证方式（密码或私钥）
4. 保存并连接

### 管理凭据
1. 进入「凭据管理」页面
2. 添加新的凭据（密码或私钥）
3. 在服务器配置中关联凭据
4. 支持批量更新密码

### 查看日志
1. 所有会话自动记录日志
2. 日志保存在 `logs/{服务器名}/{服务器名}_{时间戳}.log`
3. 可以在「日志查看」页面浏览历史日志

## 开发文档

- [设计文档](./DESIGN.md) - 完整的技术架构和设计规范
- [任务规划](./TASKS.md) - 开发任务拆分和提交规范

## License

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！