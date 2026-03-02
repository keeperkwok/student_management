# 学生信息管理系统

一个现代化的前后端分离学生信息管理系统，支持学生信息管理、成绩管理、数据统计和Excel导入导出等功能。

## 📋 项目简介

本系统采用前后端分离架构，提供完整的学生信息管理解决方案：

- **后端**: Python + FastAPI + SQLAlchemy + SQLite
- **前端**: Vue 3 + TypeScript + Ant Design Vue
- **代码质量**: Ruff (后端) + ESLint (前端)
- **数据库**: SQLite (支持迁移到 PostgreSQL/MySQL)

## ✨ 功能特性

- ✅ **用户认证**: JWT Token 认证，角色权限管理
- ✅ **学生管理**: 完整的学生信息 CRUD 操作
- ✅ **高级搜索**: 多条件组合搜索和筛选
- ✅ **成绩管理**: 成绩录入、GPA 计算、学分统计
- ✅ **数据导入导出**: Excel 批量导入导出
- ✅ **统计报表**: 数据可视化图表和统计分析
- ✅ **多环境支持**: develop、test、prod 三环境配置
- ✅ **响应式界面**: 支持桌面和移动端访问
- ✅ **自动化文档**: FastAPI 自动生成 API 文档

## 🚀 快速开始

### 环境要求

- Python 3.11+
- Node.js 18+
- Git

### 后端运行

```bash
# 进入后端目录
cd backend

# 创建并激活虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env.develop
# 编辑 .env.develop 配置数据库等信息

# 初始化数据库
alembic upgrade head

# 启动开发服务器
ENV=develop uvicorn app.main:app --reload --port 8000
```

访问 API 文档: http://localhost:8000/docs

### 前端运行

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 配置环境变量
cp .env.example .env.development
# 编辑 .env.development 配置 API 地址

# 启动开发服务器
npm run dev
```

访问应用: http://localhost:3000

## 📚 文档

详细文档请查看 `document/` 目录：

- [系统设计文档](document/DESIGN.md) - 系统架构和核心设计
- [数据库设计文档](document/DATABASE.md) - 数据表结构和关系
- [API接口文档](document/API.md) - 完整的 API 接口说明
- [开发指南](document/DEVELOPMENT.md) - 开发流程和最佳实践
- [部署文档](document/DEPLOYMENT.md) - 生产环境部署指南
- [AI代理指南](AGENTS.md) - AI 编码代理使用规范

## 🗂️ 项目结构

```
student_management/
├── backend/                 # Python 后端
│   ├── app/
│   │   ├── main.py         # FastAPI 应用入口
│   │   ├── config/         # 配置管理
│   │   ├── models/         # 数据库模型
│   │   ├── schemas/        # Pydantic 数据验证
│   │   ├── api/            # API 路由
│   │   ├── services/       # 业务逻辑
│   │   ├── utils/          # 工具函数
│   │   └── middleware/     # 中间件
│   ├── tests/              # 测试文件
│   ├── alembic/            # 数据库迁移
│   ├── data/               # SQLite 数据库文件
│   └── requirements.txt    # Python 依赖
│
├── frontend/               # Vue 前端
│   ├── src/
│   │   ├── main.ts        # 应用入口
│   │   ├── App.vue        # 根组件
│   │   ├── components/    # 可复用组件
│   │   ├── views/         # 页面组件
│   │   ├── router/        # 路由配置
│   │   ├── stores/        # 状态管理
│   │   ├── services/      # API 调用
│   │   ├── types/         # TypeScript 类型
│   │   └── utils/         # 工具函数
│   └── package.json       # npm 依赖
│
├── document/              # 项目文档
│   ├── DESIGN.md         # 系统设计
│   ├── DATABASE.md       # 数据库设计
│   ├── API.md            # API 文档
│   ├── DEVELOPMENT.md    # 开发指南
│   └── DEPLOYMENT.md     # 部署文档
│
├── README.md             # 项目说明（本文件）
└── AGENTS.md             # AI 代理指南
```

## 🛠️ 开发环境

### 后端开发

```bash
# 进入后端目录并激活虚拟环境
cd backend
source venv/bin/activate

# 开发环境运行
ENV=develop uvicorn app.main:app --reload --port 8000

# 运行测试
pytest                              # 运行所有测试
pytest tests/test_students.py       # 运行单个测试文件
pytest tests/test_students.py::test_create_student  # 运行单个测试
pytest -v                           # 详细输出
pytest --cov                        # 生成覆盖率报告

# 代码检查
ruff check .                        # Ruff 检查
ruff check --fix .                  # 自动修复
ruff format .                       # 格式化代码

# 数据库迁移
alembic revision --autogenerate -m "description"  # 创建迁移
alembic upgrade head                              # 应用迁移
alembic downgrade -1                              # 回滚迁移
```

### 前端开发

```bash
# 进入前端目录
cd frontend

# 开发环境运行
npm run dev                         # 启动开发服务器
npm run build                       # 生产构建
npm run preview                     # 预览构建结果

# 测试
npm test                            # 运行测试
npm test -- --watch                 # 监听模式
npm run test:coverage               # 生成覆盖率

# 代码检查
npm run lint                        # ESLint 检查
npm run lint:fix                    # 自动修复
npm run format                      # Prettier 格式化
npm run type-check                  # TypeScript 类型检查
```

## 🚢 生产部署

### 测试环境

```bash
# 后端
ENV=test uvicorn app.main:app --port 8001

# 前端
npm run build:test
npm run preview
```

### 生产环境

```bash
# 后端（使用 Supervisor 或 systemd 管理）
ENV=prod uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4

# 前端（构建后使用 Nginx 提供服务）
npm run build
# 将 dist/ 目录部署到 Nginx
```

详细部署步骤请参考 [部署文档](document/DEPLOYMENT.md)。

## 📊 数据库管理

### SQLite 数据库文件

- 开发环境: `backend/data/develop.db`
- 测试环境: `backend/data/test.db`
- 生产环境: `backend/data/prod.db`

### 数据库迁移

```bash
# 创建新迁移
cd backend
alembic revision --autogenerate -m "add new table"

# 应用迁移
alembic upgrade head

# 回滚迁移
alembic downgrade -1

# 查看迁移历史
alembic history

# 查看当前版本
alembic current
```

### 数据备份

```bash
# 备份数据库
cp backend/data/prod.db backups/prod_$(date +%Y%m%d).db

# 恢复数据库
cp backups/prod_20240101.db backend/data/prod.db
```

## 🔐 环境配置

### 后端环境变量 (.env.develop)

```ini
ENV=develop
DEBUG=True
SECRET_KEY=your-secret-key-for-development
DATABASE_URL=sqlite:///./data/develop.db
CORS_ORIGINS=["http://localhost:3000"]
JWT_SECRET_KEY=jwt-secret-key
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=1440
```

### 前端环境变量 (.env.development)

```ini
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_APP_TITLE=学生信息管理系统-开发环境
```

## 📝 API 文档

后端启动后，可以通过以下地址访问自动生成的 API 文档：

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 🧪 测试

### 后端测试

```bash
cd backend
source venv/bin/activate

# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/test_students.py

# 运行特定测试函数
pytest tests/test_students.py::test_create_student

# 详细输出
pytest -v -s

# 生成覆盖率报告
pytest --cov=app --cov-report=html
# 查看报告: open htmlcov/index.html
```

### 前端测试

```bash
cd frontend

# 运行测试
npm test

# 监听模式
npm test -- --watch

# 生成覆盖率
npm run test:coverage
```

## 🤝 贡献指南

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'feat: add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

### 提交规范

使用 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `style`: 代码格式（不影响功能）
- `refactor`: 重构
- `test`: 测试相关
- `chore`: 构建/工具相关

示例:
```bash
git commit -m "feat(student): add advanced search functionality"
git commit -m "fix(auth): resolve token expiration issue"
```

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 👥 作者

- 开发者: [Your Name]
- 邮箱: [your.email@example.com]
- GitHub: [https://github.com/keeperkwok/student_management](https://github.com/keeperkwok/student_management)

## 🙏 致谢

- [FastAPI](https://fastapi.tiangolo.com/) - 现代化的 Python Web 框架
- [Vue.js](https://vuejs.org/) - 渐进式 JavaScript 框架
- [Ant Design Vue](https://antdv.com/) - 企业级 UI 组件库
- [SQLAlchemy](https://www.sqlalchemy.org/) - Python SQL 工具包和 ORM

## 📞 支持

如有问题或建议，请通过以下方式联系：

- 提交 [Issue](https://github.com/keeperkwok/student_management/issues)
- 发送邮件至 [your.email@example.com]
- 查看 [常见问题](document/DEVELOPMENT.md#7-常见问题)

## 🗺️ 路线图

### v1.0 (当前版本)
- ✅ 基础学生信息管理
- ✅ 成绩管理
- ✅ 用户认证和权限
- ✅ 数据导入导出
- ✅ 统计报表

### v1.1 (计划中)
- 📅 头像上传功能
- 📅 操作日志记录
- 📅 邮件通知
- 📅 数据备份功能

### v2.0 (未来规划)
- 📅 课程管理模块
- 📅 教师管理模块
- 📅 考勤管理
- 📅 移动端适配

---

**如果这个项目对您有帮助，请给个 ⭐️ Star 支持一下！**
