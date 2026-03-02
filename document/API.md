# API接口文档

## 1. 概述

### 1.1 基本信息
- **Base URL**: `http://localhost:8000/api/v1`
- **协议**: HTTP/HTTPS
- **数据格式**: JSON
- **字符编码**: UTF-8

### 1.2 认证方式
使用 JWT (JSON Web Token) 进行认证。

**请求头:**
```
Authorization: Bearer <access_token>
```

### 1.3 通用响应格式

**成功响应:**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    // 响应数据
  }
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

### 1.4 HTTP状态码

| 状态码 | 说明 |
|--------|------|
| 200 | 请求成功 |
| 201 | 创建成功 |
| 204 | 删除成功 |
| 400 | 请求参数错误 |
| 401 | 未认证 |
| 403 | 无权限 |
| 404 | 资源不存在 |
| 422 | 数据验证失败 |
| 500 | 服务器错误 |

---

## 2. 认证接口

### 2.1 用户注册

**接口**: `POST /api/v1/auth/register`

**描述**: 注册新用户

**是否需要认证**: 否

**请求体:**
```json
{
  "username": "zhangsan",
  "email": "zhangsan@example.com",
  "password": "password123",
  "full_name": "张三"
}
```

**请求参数说明:**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| username | string | 是 | 用户名，3-50字符 |
| email | string | 是 | 邮箱地址 |
| password | string | 是 | 密码，至少6位 |
| full_name | string | 否 | 全名 |

**成功响应 (201):**
```json
{
  "code": 201,
  "message": "注册成功",
  "data": {
    "id": 1,
    "username": "zhangsan",
    "email": "zhangsan@example.com",
    "full_name": "张三",
    "role": "user",
    "is_active": true,
    "created_at": "2024-01-01T10:00:00"
  }
}
```

**错误响应:**
- 400: 用户名或邮箱已存在
- 422: 数据验证失败

---

### 2.2 用户登录

**接口**: `POST /api/v1/auth/login`

**描述**: 用户登录获取JWT Token

**是否需要认证**: 否

**请求体:**
```json
{
  "username": "zhangsan",
  "password": "password123"
}
```

**请求参数说明:**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| username | string | 是 | 用户名或邮箱 |
| password | string | 是 | 密码 |

**成功响应 (200):**
```json
{
  "code": 200,
  "message": "登录成功",
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "expires_in": 86400,
    "user": {
      "id": 1,
      "username": "zhangsan",
      "full_name": "张三",
      "role": "user"
    }
  }
}
```

**错误响应:**
- 401: 用户名或密码错误
- 403: 账户未激活

---

### 2.3 获取当前用户信息

**接口**: `GET /api/v1/auth/me`

**描述**: 获取当前登录用户的信息

**是否需要认证**: 是

**成功响应 (200):**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "id": 1,
    "username": "zhangsan",
    "email": "zhangsan@example.com",
    "full_name": "张三",
    "role": "user",
    "is_active": true,
    "last_login": "2024-01-01T10:00:00",
    "created_at": "2024-01-01T09:00:00"
  }
}
```

---

### 2.4 刷新Token

**接口**: `POST /api/v1/auth/refresh`

**描述**: 刷新访问令牌

**是否需要认证**: 是

**成功响应 (200):**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "expires_in": 86400
  }
}
```

---

## 3. 学生管理接口

### 3.1 创建学生

**接口**: `POST /api/v1/students`

**描述**: 创建新学生记录

**是否需要认证**: 是

**权限要求**: user 或 admin

**请求体:**
```json
{
  "student_no": "2024001",
  "name": "张三",
  "gender": "男",
  "birth_date": "2005-03-15",
  "phone": "13800138000",
  "email": "zhangsan@example.com",
  "major": "计算机科学与技术",
  "class_name": "计科2401班",
  "grade": 2024,
  "enrollment_date": "2024-09-01",
  "status": "active",
  "address": "北京市海淀区",
  "emergency_contact": "李四",
  "emergency_phone": "13900139000",
  "remark": "备注信息"
}
```

**请求参数说明:**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| student_no | string | 是 | 学号，唯一 |
| name | string | 是 | 姓名 |
| gender | string | 否 | 性别 (男/女/其他) |
| birth_date | string | 否 | 出生日期 (YYYY-MM-DD) |
| phone | string | 否 | 联系电话 |
| email | string | 否 | 邮箱 |
| major | string | 否 | 专业 |
| class_name | string | 否 | 班级 |
| grade | integer | 否 | 年级 |
| enrollment_date | string | 否 | 入学日期 |
| status | string | 否 | 状态 (active/graduated/suspended) |
| address | string | 否 | 地址 |
| emergency_contact | string | 否 | 紧急联系人 |
| emergency_phone | string | 否 | 紧急联系电话 |
| remark | string | 否 | 备注 |

**成功响应 (201):**
```json
{
  "code": 201,
  "message": "创建成功",
  "data": {
    "id": 1,
    "student_no": "2024001",
    "name": "张三",
    "gender": "男",
    "birth_date": "2005-03-15",
    "phone": "13800138000",
    "email": "zhangsan@example.com",
    "major": "计算机科学与技术",
    "class_name": "计科2401班",
    "grade": 2024,
    "enrollment_date": "2024-09-01",
    "status": "active",
    "created_at": "2024-01-01T10:00:00",
    "updated_at": "2024-01-01T10:00:00"
  }
}
```

**错误响应:**
- 400: 学号已存在
- 422: 数据验证失败

---

### 3.2 获取学生列表

**接口**: `GET /api/v1/students`

**描述**: 分页查询学生列表，支持多条件筛选

**是否需要认证**: 是

**查询参数:**

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| page | integer | 否 | 1 | 页码 |
| size | integer | 否 | 10 | 每页数量 (最大100) |
| student_no | string | 否 | - | 学号搜索 |
| name | string | 否 | - | 姓名搜索 (模糊匹配) |
| major | string | 否 | - | 专业筛选 |
| class_name | string | 否 | - | 班级筛选 |
| grade | integer | 否 | - | 年级筛选 |
| status | string | 否 | - | 状态筛选 |
| sort_by | string | 否 | created_at | 排序字段 |
| order | string | 否 | desc | 排序方向 (asc/desc) |

**请求示例:**
```
GET /api/v1/students?page=1&size=10&major=计算机科学与技术&grade=2024
```

**成功响应 (200):**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "items": [
      {
        "id": 1,
        "student_no": "2024001",
        "name": "张三",
        "gender": "男",
        "major": "计算机科学与技术",
        "class_name": "计科2401班",
        "grade": 2024,
        "status": "active",
        "created_at": "2024-01-01T10:00:00"
      }
    ],
    "total": 100,
    "page": 1,
    "size": 10,
    "pages": 10
  }
}
```

---

### 3.3 获取学生详情

**接口**: `GET /api/v1/students/{student_id}`

**描述**: 获取指定学生的详细信息

**是否需要认证**: 是

**路径参数:**

| 参数 | 类型 | 说明 |
|------|------|------|
| student_id | integer | 学生ID |

**成功响应 (200):**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "id": 1,
    "student_no": "2024001",
    "name": "张三",
    "gender": "男",
    "birth_date": "2005-03-15",
    "phone": "13800138000",
    "email": "zhangsan@example.com",
    "major": "计算机科学与技术",
    "class_name": "计科2401班",
    "grade": 2024,
    "enrollment_date": "2024-09-01",
    "status": "active",
    "address": "北京市海淀区",
    "emergency_contact": "李四",
    "emergency_phone": "13900139000",
    "remark": "备注信息",
    "created_at": "2024-01-01T10:00:00",
    "updated_at": "2024-01-01T10:00:00"
  }
}
```

**错误响应:**
- 404: 学生不存在

---

### 3.4 更新学生信息

**接口**: `PUT /api/v1/students/{student_id}`

**描述**: 更新学生信息

**是否需要认证**: 是

**权限要求**: user 或 admin

**路径参数:**

| 参数 | 类型 | 说明 |
|------|------|------|
| student_id | integer | 学生ID |

**请求体:**
```json
{
  "name": "张三",
  "phone": "13800138001",
  "email": "zhangsan_new@example.com",
  "status": "graduated"
}
```

**说明**: 只需要提供需要更新的字段

**成功响应 (200):**
```json
{
  "code": 200,
  "message": "更新成功",
  "data": {
    "id": 1,
    "student_no": "2024001",
    "name": "张三",
    "phone": "13800138001",
    "email": "zhangsan_new@example.com",
    "status": "graduated",
    "updated_at": "2024-01-01T11:00:00"
  }
}
```

**错误响应:**
- 404: 学生不存在
- 422: 数据验证失败

---

### 3.5 删除学生

**接口**: `DELETE /api/v1/students/{student_id}`

**描述**: 删除学生 (软删除)

**是否需要认证**: 是

**权限要求**: admin

**路径参数:**

| 参数 | 类型 | 说明 |
|------|------|------|
| student_id | integer | 学生ID |

**成功响应 (200):**
```json
{
  "code": 200,
  "message": "删除成功"
}
```

**错误响应:**
- 403: 权限不足
- 404: 学生不存在

---

### 3.6 批量导入学生

**接口**: `POST /api/v1/students/import`

**描述**: 从Excel文件批量导入学生

**是否需要认证**: 是

**权限要求**: admin

**请求类型**: `multipart/form-data`

**请求参数:**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| file | file | 是 | Excel文件 (.xlsx, .xls) |

**成功响应 (200):**
```json
{
  "code": 200,
  "message": "导入成功",
  "data": {
    "success_count": 50,
    "fail_count": 2,
    "errors": [
      {
        "row": 10,
        "student_no": "2024010",
        "error": "学号已存在"
      },
      {
        "row": 25,
        "student_no": "2024025",
        "error": "邮箱格式错误"
      }
    ]
  }
}
```

---

### 3.7 导出学生列表

**接口**: `GET /api/v1/students/export`

**描述**: 导出学生列表为Excel文件

**是否需要认证**: 是

**查询参数**: 同"获取学生列表"接口的筛选参数

**成功响应**: 
- Content-Type: `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`
- 返回Excel文件流

---

## 4. 成绩管理接口

### 4.1 创建成绩记录

**接口**: `POST /api/v1/grades`

**描述**: 创建新成绩记录

**是否需要认证**: 是

**请求体:**
```json
{
  "student_id": 1,
  "course_name": "高等数学",
  "course_code": "MATH101",
  "score": 85.5,
  "credits": 4.0,
  "semester": "2024-1",
  "academic_year": "2024-2025",
  "exam_type": "期末",
  "exam_date": "2024-06-15",
  "teacher_name": "王老师"
}
```

**请求参数说明:**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| student_id | integer | 是 | 学生ID |
| course_name | string | 是 | 课程名称 |
| course_code | string | 否 | 课程代码 |
| score | number | 否 | 成绩 (0-100) |
| credits | number | 否 | 学分 |
| semester | string | 否 | 学期 |
| academic_year | string | 否 | 学年 |
| exam_type | string | 否 | 考试类型 |
| exam_date | string | 否 | 考试日期 |
| teacher_name | string | 否 | 教师姓名 |

**成功响应 (201):**
```json
{
  "code": 201,
  "message": "创建成功",
  "data": {
    "id": 1,
    "student_id": 1,
    "course_name": "高等数学",
    "course_code": "MATH101",
    "score": 85.5,
    "credits": 4.0,
    "semester": "2024-1",
    "created_at": "2024-01-01T10:00:00"
  }
}
```

---

### 4.2 获取成绩列表

**接口**: `GET /api/v1/grades`

**描述**: 查询成绩列表

**是否需要认证**: 是

**查询参数:**

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| page | integer | 否 | 1 | 页码 |
| size | integer | 否 | 10 | 每页数量 |
| student_id | integer | 否 | - | 学生ID |
| student_no | string | 否 | - | 学号 |
| course_name | string | 否 | - | 课程名称 |
| semester | string | 否 | - | 学期 |
| academic_year | string | 否 | - | 学年 |

**成功响应 (200):**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "items": [
      {
        "id": 1,
        "student": {
          "id": 1,
          "student_no": "2024001",
          "name": "张三"
        },
        "course_name": "高等数学",
        "score": 85.5,
        "credits": 4.0,
        "semester": "2024-1",
        "created_at": "2024-01-01T10:00:00"
      }
    ],
    "total": 50,
    "page": 1,
    "size": 10,
    "pages": 5
  }
}
```

---

### 4.3 获取学生成绩汇总

**接口**: `GET /api/v1/grades/summary/{student_id}`

**描述**: 获取学生的成绩汇总信息

**是否需要认证**: 是

**路径参数:**

| 参数 | 类型 | 说明 |
|------|------|------|
| student_id | integer | 学生ID |

**成功响应 (200):**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "student": {
      "id": 1,
      "student_no": "2024001",
      "name": "张三",
      "major": "计算机科学与技术"
    },
    "total_courses": 10,
    "total_credits": 40.0,
    "avg_score": 85.5,
    "gpa": 3.5,
    "pass_rate": 100.0,
    "grade_distribution": {
      "优秀": 3,
      "良好": 5,
      "中等": 2,
      "及格": 0,
      "不及格": 0
    }
  }
}
```

---

### 4.4 更新成绩

**接口**: `PUT /api/v1/grades/{grade_id}`

**描述**: 更新成绩记录

**是否需要认证**: 是

**路径参数:**

| 参数 | 类型 | 说明 |
|------|------|------|
| grade_id | integer | 成绩ID |

**请求体:**
```json
{
  "score": 90.0,
  "remark": "补考成绩"
}
```

**成功响应 (200):**
```json
{
  "code": 200,
  "message": "更新成功",
  "data": {
    "id": 1,
    "score": 90.0,
    "remark": "补考成绩",
    "updated_at": "2024-01-01T11:00:00"
  }
}
```

---

### 4.5 删除成绩

**接口**: `DELETE /api/v1/grades/{grade_id}`

**描述**: 删除成绩记录

**是否需要认证**: 是

**权限要求**: admin

**路径参数:**

| 参数 | 类型 | 说明 |
|------|------|------|
| grade_id | integer | 成绩ID |

**成功响应 (200):**
```json
{
  "code": 200,
  "message": "删除成功"
}
```

---

## 5. 统计报表接口

### 5.1 获取总体统计

**接口**: `GET /api/v1/statistics/overview`

**描述**: 获取系统总体统计数据

**是否需要认证**: 是

**成功响应 (200):**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "total_students": 1000,
    "active_students": 850,
    "graduated_students": 140,
    "suspended_students": 10,
    "total_courses": 500,
    "avg_gpa": 3.2,
    "pass_rate": 95.5
  }
}
```

---

### 5.2 获取专业分布统计

**接口**: `GET /api/v1/statistics/major`

**描述**: 获取各专业学生分布

**是否需要认证**: 是

**成功响应 (200):**
```json
{
  "code": 200,
  "message": "success",
  "data": [
    {
      "major": "计算机科学与技术",
      "student_count": 300,
      "male_count": 200,
      "female_count": 100,
      "avg_gpa": 3.3
    },
    {
      "major": "软件工程",
      "student_count": 250,
      "male_count": 180,
      "female_count": 70,
      "avg_gpa": 3.2
    }
  ]
}
```

---

### 5.3 获取成绩分布统计

**接口**: `GET /api/v1/statistics/grade-distribution`

**描述**: 获取成绩分布统计

**是否需要认证**: 是

**查询参数:**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| major | string | 否 | 专业筛选 |
| semester | string | 否 | 学期筛选 |

**成功响应 (200):**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "distribution": [
      { "level": "优秀", "count": 150, "percentage": 30.0 },
      { "level": "良好", "count": 200, "percentage": 40.0 },
      { "level": "中等", "count": 100, "percentage": 20.0 },
      { "level": "及格", "count": 40, "percentage": 8.0 },
      { "level": "不及格", "count": 10, "percentage": 2.0 }
    ],
    "total_records": 500
  }
}
```

---

## 6. 用户管理接口

### 6.1 获取用户列表

**接口**: `GET /api/v1/users`

**描述**: 获取用户列表 (仅管理员)

**是否需要认证**: 是

**权限要求**: admin

**查询参数:**

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| page | integer | 否 | 1 | 页码 |
| size | integer | 否 | 10 | 每页数量 |
| role | string | 否 | - | 角色筛选 |
| is_active | boolean | 否 | - | 状态筛选 |

**成功响应 (200):**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "items": [
      {
        "id": 1,
        "username": "admin",
        "email": "admin@example.com",
        "full_name": "管理员",
        "role": "admin",
        "is_active": true,
        "last_login": "2024-01-01T10:00:00",
        "created_at": "2024-01-01T09:00:00"
      }
    ],
    "total": 10,
    "page": 1,
    "size": 10,
    "pages": 1
  }
}
```

---

### 6.2 更新用户信息

**接口**: `PUT /api/v1/users/{user_id}`

**描述**: 更新用户信息

**是否需要认证**: 是

**权限要求**: admin 或 自己

**路径参数:**

| 参数 | 类型 | 说明 |
|------|------|------|
| user_id | integer | 用户ID |

**请求体:**
```json
{
  "full_name": "新名字",
  "email": "newemail@example.com"
}
```

**成功响应 (200):**
```json
{
  "code": 200,
  "message": "更新成功",
  "data": {
    "id": 1,
    "username": "zhangsan",
    "email": "newemail@example.com",
    "full_name": "新名字",
    "updated_at": "2024-01-01T11:00:00"
  }
}
```

---

### 6.3 修改密码

**接口**: `POST /api/v1/users/change-password`

**描述**: 修改当前用户密码

**是否需要认证**: 是

**请求体:**
```json
{
  "old_password": "oldpass123",
  "new_password": "newpass123"
}
```

**成功响应 (200):**
```json
{
  "code": 200,
  "message": "密码修改成功"
}
```

**错误响应:**
- 400: 旧密码错误

---

## 7. 错误码说明

| 错误码 | 说明 |
|--------|------|
| 1001 | 用户名或密码错误 |
| 1002 | Token无效或已过期 |
| 1003 | 权限不足 |
| 2001 | 学号已存在 |
| 2002 | 学生不存在 |
| 3001 | 课程不存在 |
| 3002 | 成绩已存在 |
| 4001 | 文件格式错误 |
| 4002 | 文件过大 |
| 5000 | 服务器内部错误 |

---

## 8. API调用示例

### 8.1 Python 示例

```python
import requests

# 基础URL
BASE_URL = "http://localhost:8000/api/v1"

# 登录获取Token
login_data = {
    "username": "admin",
    "password": "admin123"
}
response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
token = response.json()["data"]["access_token"]

# 设置认证头
headers = {
    "Authorization": f"Bearer {token}"
}

# 获取学生列表
params = {
    "page": 1,
    "size": 10,
    "major": "计算机科学与技术"
}
response = requests.get(f"{BASE_URL}/students", headers=headers, params=params)
students = response.json()["data"]["items"]

print(students)
```

### 8.2 JavaScript 示例

```javascript
// 使用 axios
import axios from 'axios';

const BASE_URL = 'http://localhost:8000/api/v1';

// 登录
const login = async () => {
  const response = await axios.post(`${BASE_URL}/auth/login`, {
    username: 'admin',
    password: 'admin123'
  });
  
  const token = response.data.data.access_token;
  
  // 设置默认请求头
  axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  
  return token;
};

// 获取学生列表
const getStudents = async () => {
  const response = await axios.get(`${BASE_URL}/students`, {
    params: {
      page: 1,
      size: 10,
      major: '计算机科学与技术'
    }
  });
  
  return response.data.data.items;
};

// 使用
await login();
const students = await getStudents();
console.log(students);
```

### 8.3 cURL 示例

```bash
# 登录
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# 获取学生列表 (需要替换TOKEN)
curl -X GET "http://localhost:8000/api/v1/students?page=1&size=10" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"

# 创建学生
curl -X POST http://localhost:8000/api/v1/students \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "student_no": "2024001",
    "name": "张三",
    "major": "计算机科学与技术"
  }'
```

---

## 9. 自动生成的API文档

FastAPI提供了自动生成的交互式API文档：

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

推荐使用Swagger UI进行接口测试和调试。

---

## 10. 版本历史

| 版本 | 日期 | 变更说明 |
|------|------|---------|
| v1.0 | 2024-01-01 | 初始版本 |

---

## 11. 联系方式

如有问题或建议，请联系开发团队或提交Issue。
