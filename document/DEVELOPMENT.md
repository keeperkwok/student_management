# 开发指南

## 1. 环境准备

### 1.1 系统要求

- **操作系统**: macOS, Linux, Windows 10+
- **Python**: 3.11 或更高版本
- **Node.js**: 18.0 或更高版本
- **Git**: 2.0 或更高版本

### 1.2 开发工具推荐

#### 代码编辑器
- **VS Code** (推荐)
  - 插件: Python, Pylance, ESLint, Vetur/Volar, Prettier
- **PyCharm Professional**
- **WebStorm**

#### 数据库工具
- **DB Browser for SQLite** (推荐)
- **DBeaver**
- **SQLiteStudio**

#### API测试工具
- **Postman**
- **Insomnia**
- **FastAPI Swagger UI** (内置)

---

## 2. 项目初始化

### 2.1 克隆项目

```bash
git clone git@github.com:keeperkwok/student_management.git
cd student_management
```

### 2.2 后端初始化

```bash
# 进入后端目录
cd backend

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# macOS/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 复制环境配置文件
cp .env.example .env.develop

# 编辑环境配置
vim .env.develop

# 初始化数据库
alembic upgrade head

# 创建初始管理员用户（如果有种子数据脚本）
python -m app.db.init_db

# 启动开发服务器
ENV=develop uvicorn app.main:app --reload --port 8000
```

访问: http://localhost:8000/docs 查看API文档

### 2.3 前端初始化

```bash
# 打开新终端，进入前端目录
cd frontend

# 安装依赖
npm install
# 或使用 yarn/pnpm
# yarn install
# pnpm install

# 复制环境配置文件
cp .env.example .env.development

# 编辑环境配置
vim .env.development

# 启动开发服务器
npm run dev
```

访问: http://localhost:3000

---

## 3. 开发流程

### 3.1 分支管理

```bash
# 从主分支创建功能分支
git checkout main
git pull origin main
git checkout -b feature/student-search

# 开发完成后提交
git add .
git commit -m "feat: add student search functionality"

# 推送到远程
git push origin feature/student-search

# 在GitHub上创建Pull Request
```

### 3.2 提交规范

使用 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

```
<type>(<scope>): <subject>

<body>

<footer>
```

**类型 (type):**
- `feat`: 新功能
- `fix`: Bug修复
- `docs`: 文档更新
- `style`: 代码格式调整（不影响功能）
- `refactor`: 重构
- `test`: 测试相关
- `chore`: 构建/工具相关
- `perf`: 性能优化

**示例:**
```bash
git commit -m "feat(student): add student search by major"
git commit -m "fix(auth): resolve token expiration issue"
git commit -m "docs: update API documentation"
```

---

## 4. 后端开发

### 4.1 项目结构说明

```
backend/
├── app/
│   ├── main.py              # FastAPI 应用入口，路由注册
│   ├── config/              # 配置管理
│   │   ├── settings.py      # 环境配置加载
│   │   └── database.py      # 数据库连接
│   ├── models/              # SQLAlchemy ORM 模型
│   ├── schemas/             # Pydantic 数据验证模型
│   ├── api/                 # API 路由定义
│   │   ├── deps.py          # 依赖注入（如获取数据库会话）
│   │   └── v1/              # API v1 版本
│   ├── services/            # 业务逻辑层
│   ├── utils/               # 工具函数
│   └── middleware/          # 中间件
├── tests/                   # 测试文件
├── alembic/                 # 数据库迁移
└── data/                    # SQLite 数据库文件
```

### 4.2 添加新的数据模型

**步骤:**

1. **创建模型** (`app/models/example.py`):

```python
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from app.models.base import Base

class Example(Base):
    __tablename__ = "examples"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    description = Column(String(200))
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
```

2. **创建Schema** (`app/schemas/example.py`):

```python
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class ExampleBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    description: Optional[str] = None
    is_active: bool = True

class ExampleCreate(ExampleBase):
    pass

class ExampleUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    description: Optional[str] = None
    is_active: Optional[bool] = None

class ExampleResponse(ExampleBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
```

3. **创建数据库迁移**:

```bash
alembic revision --autogenerate -m "add example table"
alembic upgrade head
```

4. **创建Service** (`app/services/example_service.py`):

```python
from sqlalchemy.orm import Session
from app.models.example import Example
from app.schemas.example import ExampleCreate, ExampleUpdate
from typing import List, Optional

class ExampleService:
    @staticmethod
    def create(db: Session, data: ExampleCreate) -> Example:
        db_obj = Example(**data.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    @staticmethod
    def get_by_id(db: Session, id: int) -> Optional[Example]:
        return db.query(Example).filter(
            Example.id == id,
            Example.is_deleted == False
        ).first()
    
    @staticmethod
    def get_list(db: Session, skip: int = 0, limit: int = 10) -> List[Example]:
        return db.query(Example).filter(
            Example.is_deleted == False
        ).offset(skip).limit(limit).all()
    
    @staticmethod
    def update(db: Session, id: int, data: ExampleUpdate) -> Optional[Example]:
        db_obj = ExampleService.get_by_id(db, id)
        if not db_obj:
            return None
        
        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    @staticmethod
    def delete(db: Session, id: int) -> bool:
        db_obj = ExampleService.get_by_id(db, id)
        if not db_obj:
            return False
        
        db_obj.is_deleted = True
        db.commit()
        return True
```

5. **创建API路由** (`app/api/v1/examples.py`):

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.api.deps import get_db, get_current_user
from app.schemas.example import ExampleCreate, ExampleUpdate, ExampleResponse
from app.services.example_service import ExampleService

router = APIRouter()

@router.post("/", response_model=ExampleResponse, status_code=status.HTTP_201_CREATED)
def create_example(
    data: ExampleCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """创建示例"""
    return ExampleService.create(db, data)

@router.get("/{id}", response_model=ExampleResponse)
def get_example(
    id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """获取示例详情"""
    example = ExampleService.get_by_id(db, id)
    if not example:
        raise HTTPException(status_code=404, detail="Example not found")
    return example

@router.get("/", response_model=List[ExampleResponse])
def get_examples(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """获取示例列表"""
    return ExampleService.get_list(db, skip, limit)

@router.put("/{id}", response_model=ExampleResponse)
def update_example(
    id: int,
    data: ExampleUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """更新示例"""
    example = ExampleService.update(db, id, data)
    if not example:
        raise HTTPException(status_code=404, detail="Example not found")
    return example

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_example(
    id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """删除示例"""
    if not ExampleService.delete(db, id):
        raise HTTPException(status_code=404, detail="Example not found")
```

6. **注册路由** (`app/main.py`):

```python
from app.api.v1 import examples

app.include_router(examples.router, prefix="/api/v1/examples", tags=["examples"])
```

### 4.3 运行测试

```bash
# 运行所有测试
pytest

# 运行指定测试文件
pytest tests/test_students.py

# 运行单个测试
pytest tests/test_students.py::test_create_student

# 显示详细输出
pytest -v

# 显示打印信息
pytest -s

# 生成覆盖率报告
pytest --cov=app --cov-report=html

# 查看覆盖率报告
open htmlcov/index.html  # macOS
```

### 4.4 代码检查

```bash
# Ruff 检查
ruff check .

# 自动修复
ruff check --fix .

# 格式化代码
ruff format .

# 类型检查（如果使用 mypy）
mypy app
```

---

## 5. 前端开发

### 5.1 项目结构说明

```
frontend/
├── src/
│   ├── main.ts              # 应用入口
│   ├── App.vue              # 根组件
│   ├── components/          # 可复用组件
│   ├── views/               # 页面组件
│   ├── router/              # 路由配置
│   ├── stores/              # Pinia 状态管理
│   ├── services/            # API 调用
│   ├── types/               # TypeScript 类型定义
│   ├── utils/               # 工具函数
│   └── styles/              # 全局样式
```

### 5.2 添加新页面

**步骤:**

1. **创建页面组件** (`src/views/Example.vue`):

```vue
<template>
  <div class="example-page">
    <a-card title="示例页面">
      <a-button type="primary" @click="handleClick">
        点击我
      </a-button>
      <p>{{ message }}</p>
    </a-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const message = ref('Hello World')

const handleClick = () => {
  message.value = '按钮被点击了！'
}
</script>

<style scoped>
.example-page {
  padding: 20px;
}
</style>
```

2. **添加路由** (`src/router/index.ts`):

```typescript
import { createRouter, createWebHistory } from 'vue-router'
import Example from '@/views/Example.vue'

const routes = [
  // ... 其他路由
  {
    path: '/example',
    name: 'Example',
    component: Example,
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
```

3. **添加导航菜单** (在侧边栏配置中):

```typescript
const menuItems = [
  // ... 其他菜单
  {
    key: 'example',
    icon: 'FileOutlined',
    label: '示例页面',
    path: '/example'
  }
]
```

### 5.3 API调用

**创建API服务** (`src/services/example.ts`):

```typescript
import { apiClient } from './api'
import type { Example, ExampleCreate, ExampleUpdate } from '@/types/example'

export const exampleApi = {
  // 获取列表
  getList: (params?: { page?: number; size?: number }) => {
    return apiClient.get<{ items: Example[]; total: number }>('/examples', { params })
  },
  
  // 获取详情
  getById: (id: number) => {
    return apiClient.get<Example>(`/examples/${id}`)
  },
  
  // 创建
  create: (data: ExampleCreate) => {
    return apiClient.post<Example>('/examples', data)
  },
  
  // 更新
  update: (id: number, data: ExampleUpdate) => {
    return apiClient.put<Example>(`/examples/${id}`, data)
  },
  
  // 删除
  delete: (id: number) => {
    return apiClient.delete(`/examples/${id}`)
  }
}
```

**在组件中使用**:

```vue
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { exampleApi } from '@/services/example'
import type { Example } from '@/types/example'

const examples = ref<Example[]>([])
const loading = ref(false)

const fetchExamples = async () => {
  loading.value = true
  try {
    const response = await exampleApi.getList({ page: 1, size: 10 })
    examples.value = response.data.items
  } catch (error) {
    console.error('获取数据失败:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchExamples()
})
</script>
```

### 5.4 状态管理

**创建Store** (`src/stores/example.ts`):

```typescript
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Example } from '@/types/example'

export const useExampleStore = defineStore('example', () => {
  // State
  const examples = ref<Example[]>([])
  const currentExample = ref<Example | null>(null)
  
  // Getters
  const exampleCount = computed(() => examples.value.length)
  
  // Actions
  const setExamples = (data: Example[]) => {
    examples.value = data
  }
  
  const addExample = (example: Example) => {
    examples.value.push(example)
  }
  
  const removeExample = (id: number) => {
    const index = examples.value.findIndex(e => e.id === id)
    if (index > -1) {
      examples.value.splice(index, 1)
    }
  }
  
  return {
    examples,
    currentExample,
    exampleCount,
    setExamples,
    addExample,
    removeExample
  }
})
```

### 5.5 运行测试

```bash
# 运行单元测试
npm test

# 监听模式
npm test -- --watch

# 生成覆盖率报告
npm run test:coverage
```

### 5.6 代码检查

```bash
# ESLint 检查
npm run lint

# 自动修复
npm run lint:fix

# Prettier 格式化
npm run format

# TypeScript 类型检查
npm run type-check
```

---

## 6. 调试技巧

### 6.1 后端调试

**使用 Python 调试器:**

```python
# 在代码中添加断点
import pdb; pdb.set_trace()

# 或使用 ipdb (更友好)
import ipdb; ipdb.set_trace()
```

**VS Code 调试配置** (`.vscode/launch.json`):

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: FastAPI",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": [
        "app.main:app",
        "--reload",
        "--port",
        "8000"
      ],
      "jinja": true,
      "justMyCode": false,
      "env": {
        "ENV": "develop"
      }
    }
  ]
}
```

### 6.2 前端调试

**使用浏览器开发者工具:**
- 在 Chrome DevTools 中设置断点
- 使用 `console.log()` 输出调试信息
- 使用 Vue DevTools 查看组件状态

**VS Code 调试配置** (`.vscode/launch.json`):

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "chrome",
      "request": "launch",
      "name": "Vue: Chrome",
      "url": "http://localhost:3000",
      "webRoot": "${workspaceFolder}/frontend/src"
    }
  ]
}
```

---

## 7. 常见问题

### 7.1 后端常见问题

**问题1: 数据库连接失败**

```
解决方案:
1. 检查 .env 配置文件中的 DATABASE_URL
2. 确保 data 目录存在
3. 检查文件权限
```

**问题2: Alembic 迁移冲突**

```bash
# 查看当前版本
alembic current

# 回滚到指定版本
alembic downgrade <revision>

# 删除冲突的迁移文件，重新生成
alembic revision --autogenerate -m "new migration"
```

**问题3: 依赖安装失败**

```bash
# 升级 pip
pip install --upgrade pip

# 清除缓存
pip cache purge

# 重新安装
pip install -r requirements.txt
```

### 7.2 前端常见问题

**问题1: npm install 失败**

```bash
# 清除 npm 缓存
npm cache clean --force

# 删除 node_modules 和 lock 文件
rm -rf node_modules package-lock.json

# 重新安装
npm install
```

**问题2: 端口被占用**

```bash
# 查找占用端口的进程
lsof -i :3000  # macOS/Linux
netstat -ano | findstr :3000  # Windows

# 杀死进程
kill -9 <PID>  # macOS/Linux
taskkill /PID <PID> /F  # Windows

# 或者使用其他端口
npm run dev -- --port 3001
```

**问题3: CORS 错误**

```
解决方案:
1. 检查后端 CORS 配置
2. 确保前端配置的 API URL 正确
3. 检查请求头是否正确
```

---

## 8. 性能优化建议

### 8.1 后端优化

1. **使用数据库索引**
2. **实现缓存机制** (Redis)
3. **使用异步操作**
4. **优化数据库查询** (避免 N+1 问题)
5. **实现分页查询**

### 8.2 前端优化

1. **路由懒加载**
2. **组件按需加载**
3. **图片懒加载**
4. **防抖和节流**
5. **使用虚拟滚动**
6. **代码分割**

---

## 9. 最佳实践

### 9.1 代码规范

1. 遵循项目的代码风格指南
2. 编写清晰的注释和文档
3. 使用有意义的变量和函数名
4. 保持函数简短，单一职责
5. 避免代码重复 (DRY原则)

### 9.2 Git使用

1. 频繁提交，保持提交粒度适中
2. 写清晰的提交信息
3. 提交前进行代码审查
4. 使用分支进行功能开发
5. 及时同步远程仓库

### 9.3 安全

1. 不提交敏感信息到代码库
2. 使用环境变量管理配置
3. 定期更新依赖包
4. 进行输入验证和清理
5. 使用 HTTPS

---

## 10. 学习资源

### 10.1 后端

- [FastAPI 官方文档](https://fastapi.tiangolo.com/)
- [SQLAlchemy 文档](https://docs.sqlalchemy.org/)
- [Pydantic 文档](https://docs.pydantic.dev/)
- [Python 最佳实践](https://realpython.com/)

### 10.2 前端

- [Vue 3 官方文档](https://vuejs.org/)
- [Ant Design Vue 文档](https://antdv.com/)
- [TypeScript 文档](https://www.typescriptlang.org/)
- [Vite 文档](https://vitejs.dev/)

---

## 11. 获取帮助

如遇到问题:
1. 查看本文档和项目文档
2. 搜索项目 Issues
3. 查阅相关技术文档
4. 向团队成员寻求帮助
5. 创建新的 Issue
