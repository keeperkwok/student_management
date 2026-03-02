# 学生信息管理系统 - 系统设计文档

## 1. 项目概述

### 1.1 项目简介
学生信息管理系统是一个前后端分离的Web应用，用于管理学生的基本信息、学业信息和成绩数据。系统提供完整的CRUD操作、数据搜索筛选、Excel导入导出、统计报表等功能。

### 1.2 技术栈

#### 后端技术栈
- **语言**: Python 3.11+
- **Web框架**: FastAPI 0.104+
- **ORM**: SQLAlchemy 2.0+
- **数据库**: SQLite 3
- **数据验证**: Pydantic 2.0+
- **数据库迁移**: Alembic
- **认证**: JWT (python-jose)
- **密码加密**: bcrypt (passlib)
- **代码检查**: Ruff
- **测试**: pytest, pytest-cov
- **Excel处理**: openpyxl, pandas

#### 前端技术栈
- **框架**: Vue 3.3+
- **语言**: TypeScript 5.0+
- **UI库**: Ant Design Vue 4.0+
- **状态管理**: Pinia 2.1+
- **路由**: Vue Router 4.2+
- **HTTP客户端**: Axios 1.6+
- **构建工具**: Vite 5.0+
- **代码检查**: ESLint 8.0+
- **代码格式化**: Prettier 3.0+
- **图表库**: ECharts (vue-echarts)

### 1.3 运行环境
系统支持三种运行环境：
- **develop**: 开发环境，用于本地开发调试
- **test**: 测试环境，用于功能测试和集成测试
- **prod**: 生产环境，用于正式部署

## 2. 系统架构

### 2.1 整体架构

```
┌─────────────────────────────────────────────────────────────┐
│                         浏览器客户端                           │
│                     (Vue 3 + Ant Design)                     │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTP/HTTPS
                           │ JSON
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                      前端静态服务器                            │
│                      (Nginx / Vite)                          │
└──────────────────────────┬──────────────────────────────────┘
                           │ RESTful API
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                       后端API服务                             │
│                      (FastAPI + Uvicorn)                     │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  API Layer (Routes)                                  │   │
│  │  ├─ /api/v1/auth      (认证)                        │   │
│  │  ├─ /api/v1/students  (学生管理)                    │   │
│  │  ├─ /api/v1/grades    (成绩管理)                    │   │
│  │  ├─ /api/v1/users     (用户管理)                    │   │
│  │  └─ /api/v1/statistics (统计报表)                   │   │
│  └──────────────────────┬───────────────────────────────┘   │
│                         │                                    │
│  ┌──────────────────────┴───────────────────────────────┐   │
│  │  Business Logic Layer (Services)                     │   │
│  │  ├─ StudentService   (学生业务逻辑)                  │   │
│  │  ├─ GradeService     (成绩业务逻辑)                  │   │
│  │  ├─ AuthService      (认证业务逻辑)                  │   │
│  │  └─ ExportService    (导入导出逻辑)                  │   │
│  └──────────────────────┬───────────────────────────────┘   │
│                         │                                    │
│  ┌──────────────────────┴───────────────────────────────┐   │
│  │  Data Access Layer (Models + ORM)                    │   │
│  │  ├─ Student Model                                    │   │
│  │  ├─ Grade Model                                      │   │
│  │  └─ User Model                                       │   │
│  └──────────────────────┬───────────────────────────────┘   │
└─────────────────────────┼───────────────────────────────────┘
                          │
                          ▼
                ┌──────────────────┐
                │   SQLite数据库    │
                │  (develop.db)    │
                │  (test.db)       │
                │  (prod.db)       │
                └──────────────────┘
```

### 2.2 目录结构

```
student_management/
├── backend/                          # Python后端
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                   # FastAPI应用入口
│   │   ├── config/                   # 配置文件
│   │   │   ├── __init__.py
│   │   │   ├── settings.py           # 环境配置
│   │   │   └── database.py           # 数据库配置
│   │   ├── models/                   # SQLAlchemy模型
│   │   │   ├── __init__.py
│   │   │   ├── base.py               # 基础模型类
│   │   │   ├── student.py            # 学生模型
│   │   │   ├── grade.py              # 成绩模型
│   │   │   └── user.py               # 用户模型
│   │   ├── schemas/                  # Pydantic schemas
│   │   │   ├── __init__.py
│   │   │   ├── student.py            # 学生Schema
│   │   │   ├── grade.py              # 成绩Schema
│   │   │   ├── user.py               # 用户Schema
│   │   │   └── common.py             # 通用Schema
│   │   ├── api/                      # API路由
│   │   │   ├── __init__.py
│   │   │   ├── deps.py               # 依赖注入
│   │   │   └── v1/
│   │   │       ├── __init__.py
│   │   │       ├── students.py       # 学生API
│   │   │       ├── grades.py         # 成绩API
│   │   │       ├── users.py          # 用户API
│   │   │       ├── auth.py           # 认证API
│   │   │       └── statistics.py     # 统计API
│   │   ├── services/                 # 业务逻辑
│   │   │   ├── __init__.py
│   │   │   ├── student_service.py    # 学生服务
│   │   │   ├── grade_service.py      # 成绩服务
│   │   │   ├── user_service.py       # 用户服务
│   │   │   ├── auth_service.py       # 认证服务
│   │   │   └── export_service.py     # 导入导出服务
│   │   ├── utils/                    # 工具函数
│   │   │   ├── __init__.py
│   │   │   ├── security.py           # JWT, 密码加密
│   │   │   ├── validators.py         # 自定义验证器
│   │   │   └── excel.py              # Excel处理
│   │   └── middleware/               # 中间件
│   │       ├── __init__.py
│   │       └── cors.py               # CORS配置
│   ├── tests/                        # 测试文件
│   │   ├── __init__.py
│   │   ├── conftest.py               # pytest配置
│   │   ├── test_students.py          # 学生API测试
│   │   ├── test_grades.py            # 成绩API测试
│   │   ├── test_users.py             # 用户API测试
│   │   └── test_auth.py              # 认证测试
│   ├── alembic/                      # 数据库迁移
│   │   ├── versions/                 # 迁移版本
│   │   ├── env.py                    # Alembic环境配置
│   │   └── script.py.mako            # 迁移脚本模板
│   ├── data/                         # SQLite数据库文件
│   │   ├── .gitkeep
│   │   └── (*.db files - git ignored)
│   ├── .env.develop                  # 开发环境配置
│   ├── .env.test                     # 测试环境配置
│   ├── .env.prod                     # 生产环境配置
│   ├── .env.example                  # 环境配置示例
│   ├── requirements.txt              # 依赖列表
│   ├── pyproject.toml                # Python项目配置 (Ruff)
│   ├── alembic.ini                   # Alembic配置
│   └── pytest.ini                    # Pytest配置
│
├── frontend/                         # Vue前端
│   ├── src/
│   │   ├── main.ts                   # 应用入口
│   │   ├── App.vue                   # 根组件
│   │   ├── assets/                   # 静态资源
│   │   │   ├── images/
│   │   │   └── logo.png
│   │   ├── components/               # 组件
│   │   │   ├── layout/
│   │   │   │   ├── AppHeader.vue     # 顶部导航
│   │   │   │   ├── AppSidebar.vue    # 侧边栏
│   │   │   │   ├── AppFooter.vue     # 页脚
│   │   │   │   └── AppLayout.vue     # 主布局
│   │   │   ├── student/
│   │   │   │   ├── StudentTable.vue  # 学生表格
│   │   │   │   ├── StudentForm.vue   # 学生表单
│   │   │   │   └── StudentSearch.vue # 搜索组件
│   │   │   ├── grade/
│   │   │   │   ├── GradeTable.vue    # 成绩表格
│   │   │   │   └── GradeForm.vue     # 成绩表单
│   │   │   └── common/
│   │   │       ├── LoadingSpinner.vue
│   │   │       └── ErrorMessage.vue
│   │   ├── views/                    # 页面
│   │   │   ├── Login.vue             # 登录页
│   │   │   ├── Dashboard.vue         # 仪表盘
│   │   │   ├── student/
│   │   │   │   ├── StudentList.vue   # 学生列表
│   │   │   │   ├── StudentDetail.vue # 学生详情
│   │   │   │   └── StudentEdit.vue   # 学生编辑
│   │   │   ├── grade/
│   │   │   │   └── GradeManage.vue   # 成绩管理
│   │   │   ├── statistics/
│   │   │   │   └── StatisticsView.vue # 统计报表
│   │   │   └── NotFound.vue          # 404页面
│   │   ├── router/                   # 路由配置
│   │   │   └── index.ts
│   │   ├── stores/                   # Pinia状态管理
│   │   │   ├── user.ts               # 用户状态
│   │   │   ├── student.ts            # 学生状态
│   │   │   └── app.ts                # 应用状态
│   │   ├── services/                 # API服务
│   │   │   ├── api.ts                # Axios配置
│   │   │   ├── student.ts            # 学生API
│   │   │   ├── grade.ts              # 成绩API
│   │   │   ├── user.ts               # 用户API
│   │   │   └── auth.ts               # 认证API
│   │   ├── types/                    # TypeScript类型
│   │   │   ├── student.ts            # 学生类型
│   │   │   ├── grade.ts              # 成绩类型
│   │   │   ├── user.ts               # 用户类型
│   │   │   └── api.ts                # API类型
│   │   ├── utils/                    # 工具函数
│   │   │   ├── request.ts            # 请求封装
│   │   │   ├── validator.ts          # 表单验证
│   │   │   ├── format.ts             # 格式化工具
│   │   │   └── storage.ts            # 本地存储
│   │   ├── styles/                   # 样式文件
│   │   │   ├── main.css              # 全局样式
│   │   │   └── variables.css         # CSS变量
│   │   └── constants/                # 常量定义
│   │       └── index.ts
│   ├── public/                       # 公共资源
│   │   └── favicon.ico
│   ├── .env.development              # 开发环境
│   ├── .env.test                     # 测试环境
│   ├── .env.production               # 生产环境
│   ├── .env.example                  # 环境配置示例
│   ├── package.json                  # 依赖配置
│   ├── vite.config.ts                # Vite配置
│   ├── tsconfig.json                 # TypeScript配置
│   ├── tsconfig.node.json            # Node TypeScript配置
│   ├── .eslintrc.cjs                 # ESLint配置
│   ├── .prettierrc.json              # Prettier配置
│   └── index.html                    # HTML入口
│
├── document/                         # 文档
│   ├── DESIGN.md                     # 系统设计文档 (本文件)
│   ├── DATABASE.md                   # 数据库设计文档
│   ├── API.md                        # API接口文档
│   ├── DEVELOPMENT.md                # 开发指南
│   └── DEPLOYMENT.md                 # 部署文档
│
├── README.md                         # 项目说明
├── AGENTS.md                         # AI代理指南
└── .gitignore                        # Git忽略规则
```

## 3. 核心功能设计

### 3.1 用户认证系统

#### 功能描述
- 用户注册和登录
- JWT Token认证
- 角色权限管理 (admin/user)
- Token自动刷新

#### 技术实现
- 使用 `python-jose` 生成和验证JWT
- 使用 `passlib[bcrypt]` 加密密码
- Token有效期: 24小时
- 刷新Token有效期: 7天

### 3.2 学生信息管理

#### 功能列表
- 创建学生信息
- 查询学生列表 (分页)
- 查询单个学生详情
- 更新学生信息
- 删除学生信息 (软删除)
- 批量导入学生
- 批量导出学生

#### 搜索和筛选
- 按学号搜索
- 按姓名搜索 (模糊匹配)
- 按专业筛选
- 按班级筛选
- 按年级筛选
- 按状态筛选 (在读/毕业/休学)
- 多条件组合搜索

### 3.3 成绩管理

#### 功能列表
- 录入成绩
- 查询成绩
- 修改成绩
- 删除成绩
- 计算GPA
- 统计学分

#### 业务规则
- 成绩范围: 0-100
- GPA计算规则: 标准4.0制
  - 90-100: 4.0
  - 80-89: 3.0
  - 70-79: 2.0
  - 60-69: 1.0
  - <60: 0.0

### 3.4 统计报表

#### 统计维度
- 学生总数统计
- 按专业分布统计
- 按班级分布统计
- 按性别分布统计
- 成绩分布统计
- 平均GPA统计
- 及格率统计

#### 图表展示
- 柱状图: 专业/班级人数分布
- 饼图: 性别分布
- 折线图: 成绩趋势
- 表格: 详细数据列表

### 3.5 Excel导入导出

#### 导入功能
- 支持 `.xlsx` 和 `.xls` 格式
- 数据验证和错误提示
- 批量导入学生信息
- 导入进度显示

#### 导出功能
- 导出学生列表
- 导出成绩单
- 导出统计报表
- 自定义导出字段

## 4. 数据流设计

### 4.1 认证流程

```
用户 -> 登录请求 -> FastAPI -> 验证用户名密码
                              -> 生成JWT Token
                              -> 返回Token + 用户信息
     <- 登录响应 <-

用户 -> API请求 (携带Token) -> FastAPI -> 验证Token
                                       -> 解析用户信息
                                       -> 执行业务逻辑
     <- API响应 <-
```

### 4.2 CRUD流程 (以学生为例)

```
创建学生:
前端 -> POST /api/v1/students -> StudentSchema验证
                              -> StudentService.create()
                              -> SQLAlchemy insert
                              -> 返回创建的学生信息

查询列表:
前端 -> GET /api/v1/students?page=1&size=10&major=CS
                              -> StudentService.get_list()
                              -> SQLAlchemy query + filter + paginate
                              -> 返回分页数据

更新学生:
前端 -> PUT /api/v1/students/{id} -> 验证权限
                                   -> StudentSchema验证
                                   -> StudentService.update()
                                   -> SQLAlchemy update
                                   -> 返回更新后的数据

删除学生:
前端 -> DELETE /api/v1/students/{id} -> 验证权限
                                      -> StudentService.delete()
                                      -> 软删除 (标记is_deleted=True)
                                      -> 返回成功信息
```

## 5. 安全设计

### 5.1 认证和授权
- 所有API (除登录/注册) 都需要JWT认证
- 管理员权限: 可以管理用户、删除数据
- 普通用户权限: 只能查看和编辑数据

### 5.2 数据验证
- 前端: 表单验证 (Vue + Ant Design Form)
- 后端: Pydantic Schema强验证
- 数据库: 约束和索引

### 5.3 SQL注入防护
- 使用SQLAlchemy ORM参数化查询
- 禁止拼接SQL字符串

### 5.4 XSS防护
- Vue自动转义输出
- 后端对输入数据进行清理

### 5.5 CORS配置
- 开发环境: 允许 localhost:3000
- 生产环境: 只允许指定域名

## 6. 性能优化

### 6.1 数据库优化
- 为常用查询字段添加索引 (student_no, email等)
- 使用数据库连接池
- 分页查询避免全表扫描
- 软删除代替物理删除

### 6.2 API优化
- 使用 FastAPI 的异步特性
- 响应数据只返回必要字段
- 大数据量分页返回

### 6.3 前端优化
- 路由懒加载
- 组件按需加载
- 图片懒加载
- 使用虚拟滚动处理大列表
- 防抖和节流

## 7. 错误处理

### 7.1 HTTP状态码规范
- `200 OK`: 请求成功
- `201 Created`: 创建成功
- `400 Bad Request`: 参数错误
- `401 Unauthorized`: 未认证
- `403 Forbidden`: 无权限
- `404 Not Found`: 资源不存在
- `422 Unprocessable Entity`: 数据验证失败
- `500 Internal Server Error`: 服务器错误

### 7.2 统一响应格式

**成功响应:**
```json
{
  "code": 200,
  "message": "success",
  "data": { ... }
}
```

**错误响应:**
```json
{
  "code": 400,
  "message": "错误描述",
  "detail": "详细错误信息"
}
```

**分页响应:**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "items": [...],
    "total": 100,
    "page": 1,
    "size": 10,
    "pages": 10
  }
}
```

## 8. 测试策略

### 8.1 后端测试
- 单元测试: 测试Services和Utils
- 集成测试: 测试API endpoints
- 测试覆盖率目标: >80%
- 使用pytest fixtures模拟数据

### 8.2 前端测试
- 组件测试: 使用Vitest
- E2E测试: 使用Cypress (可选)
- 手动测试: 浏览器兼容性测试

## 9. 部署方案

### 9.1 开发环境
- 后端: `uvicorn app.main:app --reload --port 8000`
- 前端: `npm run dev` (Vite dev server)
- 数据库: SQLite (develop.db)

### 9.2 测试环境
- 后端: `uvicorn app.main:app --port 8001`
- 前端: 构建后通过Nginx提供静态文件
- 数据库: SQLite (test.db)

### 9.3 生产环境
- 后端: `uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4`
- 前端: Nginx静态文件服务 + 反向代理API
- 数据库: SQLite (prod.db) 或迁移到PostgreSQL/MySQL
- 进程管理: Supervisor 或 systemd
- 反向代理: Nginx

## 10. 开发规范

### 10.1 代码规范
- Python: 遵循PEP 8，使用Ruff检查
- TypeScript: 遵循ESLint规则
- 提交前必须通过代码检查

### 10.2 Git提交规范
- `feat`: 新功能
- `fix`: 修复bug
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 重构
- `test`: 测试相关
- `chore`: 构建/工具相关

### 10.3 分支管理
- `main`: 主分支，保护分支
- `develop`: 开发分支
- `feature/*`: 功能分支
- `bugfix/*`: 修复分支

## 11. 后续扩展

### 11.1 短期扩展 (1-3个月)
- 头像上传功能
- 操作日志记录
- 数据备份功能
- 邮件通知功能

### 11.2 中期扩展 (3-6个月)
- 课程管理模块
- 教师管理模块
- 考勤管理模块
- 移动端适配

### 11.3 长期扩展 (6-12个月)
- 微服务架构改造
- 分布式部署
- 数据分析和AI预测
- 移动App开发
