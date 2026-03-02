# 后端初始化指南

## 环境设置

### 1. 创建并激活conda虚拟环境

```bash
cd backend
conda create -n student_mgmt python=3.11
conda activate student_mgmt
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

开发环境的配置文件 `.env.develop` 已经创建,包含了默认的开发配置。

如需修改配置,可以编辑 `.env.develop` 文件。

## 初始化数据库

运行初始化脚本创建数据库表和管理员账户:

```bash
python scripts/init_db.py
```

这个脚本会:
1. 创建所有数据库表
2. 创建默认管理员用户

### 默认管理员账户

- **用户名**: `admin`
- **密码**: `admin123`
- **角色**: `admin` (管理员)
- **邮箱**: `admin@example.com`

## 数据库文件位置

- 开发环境: `backend/data/develop.db`
- 测试环境: `backend/data/test.db`
- 生产环境: `backend/data/prod.db`

## 重新初始化数据库

如果需要重新初始化数据库:

```bash
# 删除现有数据库文件
rm data/develop.db

# 重新运行初始化脚本
python scripts/init_db.py
```

## 下一步

初始化完成后,您可以:

1. 启动开发服务器 (需要先实现 FastAPI 主应用)
2. 使用管理员账户登录系统
3. 开始开发其他功能模块

## 注意事项

⚠️ **重要**: 
- 默认的 SECRET_KEY 和 JWT_SECRET_KEY 仅用于开发环境
- 在生产环境中,必须修改这些密钥为强随机字符串
- 数据库文件已添加到 .gitignore,不会提交到版本控制
