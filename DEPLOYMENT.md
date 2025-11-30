# 部署指南

## 部署成功 ✅

你的 Web SSH 客户端已经成功部署！

## 访问信息

### 🌐 Web 界面
```
http://31.22.111.107:80
```

### 📡 API 后端
```
http://31.22.111.107:8000
```

### 📚 API 文档 (Swagger UI)
```
http://31.22.111.107:8000/docs
```

### 🔍 健康检查
```
http://31.22.111.107:8000/health
```

---

## 容器状态

### 运行中的容器

| 容器名 | 镜像 | 端口映射 | 状态 |
|--------|------|----------|------|
| ssh-client-frontend | ssh-terminal-frontend | 80:80 | ✅ Running |
| ssh-client-backend | ssh-terminal-backend | 8000:8000 | ✅ Running (healthy) |

---

## 常用命令

### 查看容器状态
```bash
docker compose ps
```

### 查看日志
```bash
# 所有容器日志
docker compose logs -f

# 仅后端日志
docker compose logs -f backend

# 仅前端日志
docker compose logs -f frontend
```

### 重启服务
```bash
docker compose restart
```

### 停止服务
```bash
docker compose stop
```

### 完全关闭并删除容器
```bash
docker compose down
```

### 重新构建并启动
```bash
docker compose down
docker compose build
docker compose up -d
```

---

## 已实现功能

### ✅ 后端 (FastAPI)
- [x] FastAPI 应用框架
- [x] 健康检查端点 (`/health`)
- [x] 自动 API 文档 (`/docs`)
- [x] CORS 配置
- [x] 数据库模型 (SQLAlchemy)
  - SSHServer
  - Credential
  - SSHSession
- [x] Pydantic Schemas
- [x] 配置管理 (环境变量)
- [x] Docker 容器化

### ✅ 前端
- [x] MVP 测试页面
- [x] 后端状态检测
- [x] 响应式设计
- [x] 功能展示面板

### ⏳ 待开发
- [ ] SSH 连接核心功能 (Paramiko)
- [ ] WebSocket 双向通信
- [ ] 完整 Vue 3 前端界面
- [ ] xterm.js 终端集成
- [ ] 会话管理界面
- [ ] 凭据管理功能
- [ ] 日志记录系统

---

## Git 提交历史

所有代码更改已经妥善提交到 Git，提交信息详细说明了每个功能模块：

1. **docs**: 设计文档和任务规划
2. **chore**: 项目结构初始化
3. **feat(backend)**: FastAPI 框架搭建
4. **feat(backend)**: 数据库模型实现
5. **feat(backend)**: Pydantic schemas
6. **build**: Docker 配置
7. **fix(backend)**: 依赖修复
8. **fix(backend)**: CORS 配置解析
9. **fix(frontend)**: 文件权限修复

---

## 技术栈

### 后端
- **Python 3.11**
- **FastAPI 0.104.1** - 现代异步 Web 框架
- **SQLAlchemy 2.0.23** - ORM
- **Paramiko 3.4.0** - SSH 库
- **Cryptography 41.0.7** - 加密
- **Uvicorn 0.24.0** - ASGI 服务器

### 前端
- **Nginx Alpine** - 轻量级 Web 服务器
- **原生 HTML/CSS/JavaScript** (MVP)
- **Future**: Vue 3 + Vite + xterm.js

### 基础设施
- **Docker** - 容器化
- **Docker Compose** - 编排
- **SQLite** - 数据库

---

## 数据持久化

### 卷挂载
- `./logs` → `/app/logs` - SSH 会话日志
- `./data` → `/app/data` - SQLite 数据库

### 备份
重要数据存储在宿主机目录：
```
ssh-terminal/
├── data/          # 数据库文件
│   └── ssh_client.db
└── logs/          # 会话日志
    └── {服务器名}/
        └── {服务器名}_{时间戳}.log
```

---

## 下一步开发

### 优先级 1: SSH 核心功能
1. 实现 `SSHConnectionManager`
2. 实现 `SSHConnection` 封装
3. 添加 Paramiko 集成
4. 实现 PTY 管理

### 优先级 2: WebSocket 通信
1. 实现 WebSocket 端点
2. 双向数据转发
3. 终端大小调整
4. 心跳机制

### 优先级 3: 完整前端
1. Vue 3 + Vite 项目搭建
2. xterm.js 终端组件
3. 侧边栏会话管理
4. 凭据管理界面
5. 日志查看器

---

## 故障排查

### 容器无法启动
```bash
# 查看详细日志
docker compose logs

# 检查配置
docker compose config
```

### 端口冲突
如果端口 80 或 8000 被占用：
```yaml
# 修改 docker-compose.yml
services:
  backend:
    ports:
      - "8001:8000"  # 改为 8001
  frontend:
    ports:
      - "8080:80"    # 改为 8080
```

### 权限问题
```bash
# 确保日志和数据目录可写
chmod 755 logs data
```

---

## 安全建议

### 生产环境
1. **更换加密密钥**
   ```bash
   python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
   ```
   更新 `.env` 中的 `ENCRYPTION_KEY`

2. **启用 HTTPS**
   - 配置 SSL 证书
   - 更新 nginx.conf

3. **限制访问**
   - 配置防火墙
   - 添加用户认证

4. **关闭 DEBUG 模式**
   ```bash
   # .env
   DEBUG=false
   ```

---

## 支持与反馈

如有问题，请查看：
- [设计文档](./DESIGN.md)
- [任务规划](./TASKS.md)
- [README](./README.md)

---

**🎉 恭喜！你的 Web SSH 客户端 MVP 版本已成功部署！**
