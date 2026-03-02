# 部署文档

## 1. 部署概述

本文档介绍如何在不同环境中部署学生信息管理系统。系统支持三种运行环境：
- **develop**: 开发环境
- **test**: 测试环境
- **prod**: 生产环境

---

## 2. 服务器要求

### 2.1 最低配置

| 项目 | 开发/测试环境 | 生产环境 |
|------|--------------|---------|
| CPU | 2核 | 4核 |
| 内存 | 2GB | 4GB |
| 硬盘 | 20GB | 50GB |
| 操作系统 | Ubuntu 20.04+ | Ubuntu 20.04+ / CentOS 8+ |

### 2.2 软件要求

- Python 3.11+
- Node.js 18+
- Nginx 1.18+
- Supervisor (可选，用于进程管理)
- SQLite 3 (或 PostgreSQL/MySQL)

---

## 3. 后端部署

### 3.1 准备工作

```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装 Python 和相关工具
sudo apt install python3.11 python3.11-venv python3-pip -y

# 安装 Nginx
sudo apt install nginx -y

# 安装 Supervisor (可选)
sudo apt install supervisor -y
```

### 3.2 部署步骤

#### 3.2.1 创建部署用户

```bash
# 创建专用用户
sudo useradd -m -s /bin/bash deploy
sudo passwd deploy

# 切换到部署用户
sudo su - deploy
```

#### 3.2.2 上传代码

```bash
# 在部署用户家目录创建项目目录
cd ~
mkdir -p student_management
cd student_management

# 方式1: 使用 Git 克隆
git clone https://github.com/keeperkwok/student_management.git .

# 方式2: 使用 scp 上传
# 在本地执行:
# scp -r ./backend deploy@server_ip:/home/deploy/student_management/
```

#### 3.2.3 配置后端环境

```bash
cd ~/student_management/backend

# 创建虚拟环境
python3.11 -m venv venv

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
pip install --upgrade pip
pip install -r requirements.txt

# 配置生产环境变量
cp .env.example .env.prod
vim .env.prod
```

**编辑 `.env.prod`:**

```ini
ENV=prod
DEBUG=False
SECRET_KEY=your-super-secret-key-change-this-in-production
DATABASE_URL=sqlite:///./data/prod.db
CORS_ORIGINS=["https://yourdomain.com"]

# 如果使用 PostgreSQL
# DATABASE_URL=postgresql://user:password@localhost/student_management

# JWT 配置
JWT_SECRET_KEY=another-super-secret-key
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=1440
```

#### 3.2.4 初始化数据库

```bash
# 创建数据目录
mkdir -p data

# 运行数据库迁移
alembic upgrade head

# 创建初始管理员用户（如果有初始化脚本）
python -m app.db.init_db
```

#### 3.2.5 测试运行

```bash
# 测试启动
ENV=prod uvicorn app.main:app --host 0.0.0.0 --port 8000

# 访问测试
curl http://localhost:8000/api/v1/health
```

### 3.3 使用 Supervisor 管理进程

#### 3.3.1 创建 Supervisor 配置

```bash
sudo vim /etc/supervisor/conf.d/student_backend.conf
```

**配置内容:**

```ini
[program:student_backend]
command=/home/deploy/student_management/backend/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
directory=/home/deploy/student_management/backend
user=deploy
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/supervisor/student_backend.log
stderr_logfile=/var/log/supervisor/student_backend_error.log
environment=ENV="prod"

[program:student_backend_worker]
command=/home/deploy/student_management/backend/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8001 --workers 2
directory=/home/deploy/student_management/backend
user=deploy
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/supervisor/student_backend_worker.log
environment=ENV="prod"
```

#### 3.3.2 启动服务

```bash
# 重新加载配置
sudo supervisorctl reread
sudo supervisorctl update

# 启动服务
sudo supervisorctl start student_backend

# 查看状态
sudo supervisorctl status

# 查看日志
sudo tail -f /var/log/supervisor/student_backend.log
```

### 3.4 使用 systemd 管理进程（替代方案）

```bash
sudo vim /etc/systemd/system/student_backend.service
```

**配置内容:**

```ini
[Unit]
Description=Student Management Backend
After=network.target

[Service]
Type=simple
User=deploy
WorkingDirectory=/home/deploy/student_management/backend
Environment="ENV=prod"
ExecStart=/home/deploy/student_management/backend/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**启动服务:**

```bash
# 重载 systemd
sudo systemctl daemon-reload

# 启动服务
sudo systemctl start student_backend

# 设置开机自启
sudo systemctl enable student_backend

# 查看状态
sudo systemctl status student_backend

# 查看日志
sudo journalctl -u student_backend -f
```

---

## 4. 前端部署

### 4.1 本地构建

```bash
# 在本地开发机器上
cd frontend

# 安装依赖
npm install

# 配置生产环境变量
cp .env.example .env.production
vim .env.production
```

**编辑 `.env.production`:**

```ini
VITE_API_BASE_URL=https://api.yourdomain.com/api/v1
VITE_APP_TITLE=学生信息管理系统
```

```bash
# 构建生产版本
npm run build

# 构建产物在 dist/ 目录
```

### 4.2 上传到服务器

```bash
# 从本地上传构建产物
scp -r ./dist deploy@server_ip:/home/deploy/student_management/frontend/

# 或者在服务器上直接构建
ssh deploy@server_ip
cd ~/student_management/frontend
npm install
npm run build
```

### 4.3 配置 Nginx

#### 4.3.1 创建 Nginx 配置文件

```bash
sudo vim /etc/nginx/sites-available/student_management
```

**配置内容:**

```nginx
# 前端服务
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    
    # 重定向到 HTTPS (如果配置了SSL)
    # return 301 https://$server_name$request_uri;
    
    # 前端静态文件
    root /home/deploy/student_management/frontend/dist;
    index index.html;
    
    # Gzip 压缩
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;
    gzip_min_length 1000;
    
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    # 静态资源缓存
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    # API 反向代理
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket 支持
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        
        # 超时设置
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
    
    # API 文档
    location /docs {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /openapi.json {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
    }
}
```

#### 4.3.2 启用配置

```bash
# 创建软链接
sudo ln -s /etc/nginx/sites-available/student_management /etc/nginx/sites-enabled/

# 测试配置
sudo nginx -t

# 重启 Nginx
sudo systemctl restart nginx

# 设置开机自启
sudo systemctl enable nginx
```

---

## 5. HTTPS 配置 (使用 Let's Encrypt)

### 5.1 安装 Certbot

```bash
sudo apt install certbot python3-certbot-nginx -y
```

### 5.2 获取证书

```bash
# 自动配置 Nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# 或手动获取证书
sudo certbot certonly --nginx -d yourdomain.com -d www.yourdomain.com
```

### 5.3 自动续期

```bash
# Certbot 会自动添加 cron job
# 手动测试续期
sudo certbot renew --dry-run

# 查看定时任务
sudo systemctl list-timers
```

### 5.4 更新 Nginx 配置支持 HTTPS

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;
    
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    
    # ... 其他配置同上
}
```

---

## 6. 数据库备份

### 6.1 自动备份脚本

创建备份脚本 `/home/deploy/backup_db.sh`:

```bash
#!/bin/bash

# 配置
BACKUP_DIR="/home/deploy/backups"
DB_FILE="/home/deploy/student_management/backend/data/prod.db"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="${BACKUP_DIR}/prod_${DATE}.db"
KEEP_DAYS=30

# 创建备份目录
mkdir -p $BACKUP_DIR

# 备份数据库
cp $DB_FILE $BACKUP_FILE

# 压缩备份文件
gzip $BACKUP_FILE

# 删除旧备份（保留最近30天）
find $BACKUP_DIR -name "prod_*.db.gz" -mtime +$KEEP_DAYS -delete

echo "Backup completed: ${BACKUP_FILE}.gz"
```

### 6.2 设置定时任务

```bash
# 添加执行权限
chmod +x /home/deploy/backup_db.sh

# 编辑 crontab
crontab -e

# 添加每天凌晨2点自动备份
0 2 * * * /home/deploy/backup_db.sh >> /var/log/db_backup.log 2>&1
```

### 6.3 恢复数据库

```bash
# 停止应用
sudo supervisorctl stop student_backend

# 恢复数据库
cp /home/deploy/backups/prod_20240101_020000.db.gz /tmp/
gunzip /tmp/prod_20240101_020000.db.gz
cp /tmp/prod_20240101_020000.db /home/deploy/student_management/backend/data/prod.db

# 启动应用
sudo supervisorctl start student_backend
```

---

## 7. 监控和日志

### 7.1 应用日志

```bash
# Supervisor 日志
sudo tail -f /var/log/supervisor/student_backend.log

# Nginx 访问日志
sudo tail -f /var/log/nginx/access.log

# Nginx 错误日志
sudo tail -f /var/log/nginx/error.log

# systemd 日志（如果使用）
sudo journalctl -u student_backend -f
```

### 7.2 系统监控

```bash
# 查看系统资源
htop

# 查看磁盘使用
df -h

# 查看进程
ps aux | grep uvicorn

# 查看端口
sudo netstat -tulpn | grep 8000
```

### 7.3 日志轮转

创建日志轮转配置 `/etc/logrotate.d/student_management`:

```
/var/log/supervisor/student_backend*.log {
    daily
    rotate 30
    compress
    delaycompress
    notifempty
    create 0644 deploy deploy
    sharedscripts
    postrotate
        supervisorctl restart student_backend > /dev/null 2>&1 || true
    endscript
}
```

---

## 8. 性能优化

### 8.1 Nginx 优化

```nginx
# 在 nginx.conf 中添加
worker_processes auto;
worker_connections 1024;

# 启用缓存
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=api_cache:10m max_size=1g inactive=60m;

# 在 server 块中使用缓存
location /api/v1/statistics {
    proxy_cache api_cache;
    proxy_cache_valid 200 5m;
    proxy_cache_key "$scheme$request_method$host$request_uri";
    add_header X-Cache-Status $upstream_cache_status;
    
    proxy_pass http://127.0.0.1:8000;
}
```

### 8.2 数据库优化

```bash
# SQLite 优化（在配置中）
# 启用 WAL 模式
sqlite3 prod.db "PRAGMA journal_mode=WAL;"

# 如果迁移到 PostgreSQL
# 创建必要的索引
# 定期执行 VACUUM 和 ANALYZE
```

### 8.3 应用优化

- 增加 uvicorn workers 数量
- 实现 Redis 缓存
- 使用 CDN 加速静态资源
- 启用 HTTP/2

---

## 9. 安全加固

### 9.1 防火墙配置

```bash
# 安装 ufw
sudo apt install ufw -y

# 允许 SSH
sudo ufw allow 22/tcp

# 允许 HTTP/HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# 启用防火墙
sudo ufw enable

# 查看状态
sudo ufw status
```

### 9.2 SSH 安全

```bash
# 编辑 SSH 配置
sudo vim /etc/ssh/sshd_config

# 修改以下配置:
# Port 2222                    # 更改默认端口
# PermitRootLogin no           # 禁止root登录
# PasswordAuthentication no    # 禁用密码登录（使用密钥）

# 重启 SSH
sudo systemctl restart sshd
```

### 9.3 限制访问

```nginx
# 在 Nginx 中限制 API 访问速率
limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;

location /api/ {
    limit_req zone=api_limit burst=20 nodelay;
    # ... 其他配置
}
```

---

## 10. 故障排查

### 10.1 常见问题

**问题1: 应用无法启动**

```bash
# 检查日志
sudo supervisorctl tail student_backend stderr

# 检查端口占用
sudo netstat -tulpn | grep 8000

# 检查权限
ls -la /home/deploy/student_management/backend/data/
```

**问题2: 502 Bad Gateway**

```bash
# 检查后端服务状态
sudo supervisorctl status

# 检查 Nginx 配置
sudo nginx -t

# 查看 Nginx 错误日志
sudo tail -f /var/log/nginx/error.log
```

**问题3: 数据库锁定**

```bash
# SQLite 数据库锁定
# 检查是否有其他进程占用
fuser /home/deploy/student_management/backend/data/prod.db

# 重启应用
sudo supervisorctl restart student_backend
```

### 10.2 性能问题

```bash
# 查看系统负载
uptime
top

# 查看磁盘IO
iostat

# 查看数据库大小
ls -lh /home/deploy/student_management/backend/data/

# 分析慢查询（需要配置日志）
```

---

## 11. 更新和回滚

### 11.1 更新应用

```bash
# 切换到部署用户
sudo su - deploy

# 拉取最新代码
cd ~/student_management
git pull origin main

# 后端更新
cd backend
source venv/bin/activate
pip install -r requirements.txt
alembic upgrade head

# 前端更新
cd ../frontend
npm install
npm run build

# 重启服务
sudo supervisorctl restart student_backend
sudo systemctl reload nginx
```

### 11.2 回滚

```bash
# 回滚到指定版本
git checkout <commit_hash>

# 回滚数据库
alembic downgrade <revision>

# 重启服务
sudo supervisorctl restart student_backend
```

---

## 12. Docker 部署（可选）

### 12.1 后端 Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 12.2 前端 Dockerfile

```dockerfile
FROM node:18-alpine as builder

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### 12.3 Docker Compose

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - ENV=prod
    volumes:
      - ./backend/data:/app/data
    restart: always
  
  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend
    restart: always
```

---

## 13. 检查清单

部署前检查:
- [ ] 环境变量配置正确
- [ ] 数据库迁移已执行
- [ ] 防火墙规则已配置
- [ ] SSL证书已配置（生产环境）
- [ ] 备份策略已设置
- [ ] 监控和日志已配置
- [ ] 进程管理已配置
- [ ] Nginx配置已测试
- [ ] 应用可以正常访问
- [ ] API接口测试通过

---

## 14. 联系支持

如遇到部署问题，请联系技术支持团队。
