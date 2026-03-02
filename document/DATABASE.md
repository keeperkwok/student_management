# 数据库设计文档

## 1. 概述

### 1.1 数据库选型
- **数据库类型**: SQLite 3
- **ORM**: SQLAlchemy 2.0+
- **迁移工具**: Alembic

### 1.2 数据库文件
- 开发环境: `backend/data/develop.db`
- 测试环境: `backend/data/test.db`
- 生产环境: `backend/data/prod.db`

### 1.3 字符编码
- UTF-8

## 2. 数据表设计

### 2.1 学生表 (students)

#### 表说明
存储学生的基本信息和学业信息。

#### 表结构

| 字段名 | 数据类型 | 长度 | 约束 | 默认值 | 说明 |
|--------|---------|------|------|--------|------|
| id | INTEGER | - | PRIMARY KEY | AUTO | 主键ID |
| student_no | VARCHAR | 20 | UNIQUE NOT NULL | - | 学号 |
| name | VARCHAR | 50 | NOT NULL | - | 姓名 |
| gender | VARCHAR | 10 | - | - | 性别 (男/女/其他) |
| birth_date | DATE | - | - | - | 出生日期 |
| phone | VARCHAR | 20 | - | - | 联系电话 |
| email | VARCHAR | 100 | - | - | 电子邮箱 |
| major | VARCHAR | 50 | - | - | 专业 |
| class_name | VARCHAR | 50 | - | - | 班级名称 |
| grade | INTEGER | - | - | - | 年级 (如2024) |
| enrollment_date | DATE | - | - | - | 入学日期 |
| status | VARCHAR | 20 | NOT NULL | 'active' | 状态 (active/graduated/suspended) |
| address | TEXT | - | - | - | 家庭地址 |
| emergency_contact | VARCHAR | 50 | - | - | 紧急联系人 |
| emergency_phone | VARCHAR | 20 | - | - | 紧急联系电话 |
| remark | TEXT | - | - | - | 备注 |
| is_deleted | BOOLEAN | - | NOT NULL | FALSE | 是否删除 (软删除标记) |
| created_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP | 创建时间 |
| updated_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP | 更新时间 |

#### 索引

```sql
-- 唯一索引
CREATE UNIQUE INDEX idx_student_no ON students(student_no) WHERE is_deleted = FALSE;

-- 普通索引
CREATE INDEX idx_student_name ON students(name);
CREATE INDEX idx_student_major ON students(major);
CREATE INDEX idx_student_class ON students(class_name);
CREATE INDEX idx_student_grade ON students(grade);
CREATE INDEX idx_student_status ON students(status);
CREATE INDEX idx_student_created_at ON students(created_at);
```

#### 约束

```sql
-- 状态检查约束
CHECK (status IN ('active', 'graduated', 'suspended'))

-- 性别检查约束
CHECK (gender IN ('男', '女', '其他'))

-- 邮箱格式验证 (应用层实现)
```

#### 示例数据

```sql
INSERT INTO students (
    student_no, name, gender, birth_date, phone, email,
    major, class_name, grade, enrollment_date, status
) VALUES (
    '2024001', '张三', '男', '2005-03-15', '13800138000', 'zhangsan@example.com',
    '计算机科学与技术', '计科2401班', 2024, '2024-09-01', 'active'
);
```

---

### 2.2 成绩表 (grades)

#### 表说明
存储学生的课程成绩信息。

#### 表结构

| 字段名 | 数据类型 | 长度 | 约束 | 默认值 | 说明 |
|--------|---------|------|------|--------|------|
| id | INTEGER | - | PRIMARY KEY | AUTO | 主键ID |
| student_id | INTEGER | - | NOT NULL FOREIGN KEY | - | 学生ID (关联students.id) |
| course_name | VARCHAR | 100 | NOT NULL | - | 课程名称 |
| course_code | VARCHAR | 20 | - | - | 课程代码 |
| score | DECIMAL | 5,2 | - | - | 成绩分数 (0-100) |
| credits | DECIMAL | 3,1 | - | - | 学分 |
| semester | VARCHAR | 20 | - | - | 学期 (如"2024-1") |
| academic_year | VARCHAR | 20 | - | - | 学年 (如"2024-2025") |
| exam_type | VARCHAR | 20 | - | - | 考试类型 (期中/期末/补考) |
| exam_date | DATE | - | - | - | 考试日期 |
| teacher_name | VARCHAR | 50 | - | - | 任课教师 |
| remark | TEXT | - | - | - | 备注 |
| is_deleted | BOOLEAN | - | NOT NULL | FALSE | 是否删除 |
| created_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP | 创建时间 |
| updated_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP | 更新时间 |

#### 索引

```sql
-- 外键索引
CREATE INDEX idx_grade_student_id ON grades(student_id);

-- 复合索引
CREATE INDEX idx_grade_student_course ON grades(student_id, course_code);

-- 普通索引
CREATE INDEX idx_grade_semester ON grades(semester);
CREATE INDEX idx_grade_academic_year ON grades(academic_year);
CREATE INDEX idx_grade_course_name ON grades(course_name);
```

#### 约束

```sql
-- 外键约束
FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE

-- 成绩范围约束
CHECK (score >= 0 AND score <= 100)

-- 学分范围约束
CHECK (credits >= 0 AND credits <= 10)

-- 考试类型约束
CHECK (exam_type IN ('期中', '期末', '补考', '重修'))
```

#### 示例数据

```sql
INSERT INTO grades (
    student_id, course_name, course_code, score, credits,
    semester, academic_year, exam_type
) VALUES (
    1, '高等数学', 'MATH101', 85.5, 4.0,
    '2024-1', '2024-2025', '期末'
);
```

---

### 2.3 用户表 (users)

#### 表说明
存储系统用户信息，用于认证和权限管理。

#### 表结构

| 字段名 | 数据类型 | 长度 | 约束 | 默认值 | 说明 |
|--------|---------|------|------|--------|------|
| id | INTEGER | - | PRIMARY KEY | AUTO | 主键ID |
| username | VARCHAR | 50 | UNIQUE NOT NULL | - | 用户名 |
| email | VARCHAR | 100 | UNIQUE | - | 电子邮箱 |
| hashed_password | VARCHAR | 255 | NOT NULL | - | 加密后的密码 (bcrypt) |
| full_name | VARCHAR | 50 | - | - | 全名 |
| role | VARCHAR | 20 | NOT NULL | 'user' | 角色 (admin/user) |
| is_active | BOOLEAN | - | NOT NULL | TRUE | 是否激活 |
| avatar_url | VARCHAR | 255 | - | - | 头像URL |
| last_login | DATETIME | - | - | - | 最后登录时间 |
| login_count | INTEGER | - | NOT NULL | 0 | 登录次数 |
| is_deleted | BOOLEAN | - | NOT NULL | FALSE | 是否删除 |
| created_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP | 创建时间 |
| updated_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP | 更新时间 |

#### 索引

```sql
-- 唯一索引
CREATE UNIQUE INDEX idx_user_username ON users(username) WHERE is_deleted = FALSE;
CREATE UNIQUE INDEX idx_user_email ON users(email) WHERE is_deleted = FALSE;

-- 普通索引
CREATE INDEX idx_user_role ON users(role);
CREATE INDEX idx_user_is_active ON users(is_active);
```

#### 约束

```sql
-- 角色检查约束
CHECK (role IN ('admin', 'user'))

-- 用户名长度约束
CHECK (length(username) >= 3)
```

#### 示例数据

```sql
-- 注意: hashed_password 是通过 bcrypt 加密的密码
INSERT INTO users (
    username, email, hashed_password, full_name, role
) VALUES (
    'admin', 'admin@example.com', 
    '$2b$12$abcdefghijklmnopqrstuvwxyz1234567890', 
    '系统管理员', 'admin'
);
```

---

## 3. 表关系图 (ER图)

```
┌─────────────────────────┐
│       students          │
│─────────────────────────│
│ id (PK)                 │
│ student_no (UK)         │
│ name                    │
│ gender                  │
│ birth_date              │
│ phone                   │
│ email                   │
│ major                   │
│ class_name              │
│ grade                   │
│ enrollment_date         │
│ status                  │
│ address                 │
│ emergency_contact       │
│ emergency_phone         │
│ remark                  │
│ is_deleted              │
│ created_at              │
│ updated_at              │
└───────────┬─────────────┘
            │
            │ 1:N
            │
            ▼
┌─────────────────────────┐
│        grades           │
│─────────────────────────│
│ id (PK)                 │
│ student_id (FK)         │───┐
│ course_name             │   │
│ course_code             │   │
│ score                   │   │
│ credits                 │   │
│ semester                │   │
│ academic_year           │   │
│ exam_type               │   │
│ exam_date               │   │
│ teacher_name            │   │
│ remark                  │   │
│ is_deleted              │   │
│ created_at              │   │
│ updated_at              │   │
└─────────────────────────┘   │
                              │
                              │ references
                              │
                              └─ students.id


┌─────────────────────────┐
│         users           │
│─────────────────────────│
│ id (PK)                 │
│ username (UK)           │
│ email (UK)              │
│ hashed_password         │
│ full_name               │
│ role                    │
│ is_active               │
│ avatar_url              │
│ last_login              │
│ login_count             │
│ is_deleted              │
│ created_at              │
│ updated_at              │
└─────────────────────────┘

说明:
- PK: Primary Key (主键)
- FK: Foreign Key (外键)
- UK: Unique Key (唯一键)
- 1:N: 一对多关系
```

## 4. 数据字典

### 4.1 学生状态 (students.status)

| 值 | 说明 |
|----|------|
| active | 在读 |
| graduated | 已毕业 |
| suspended | 休学/停学 |

### 4.2 性别 (students.gender)

| 值 | 说明 |
|----|------|
| 男 | 男性 |
| 女 | 女性 |
| 其他 | 其他 |

### 4.3 用户角色 (users.role)

| 值 | 说明 | 权限 |
|----|------|------|
| admin | 管理员 | 所有操作权限 |
| user | 普通用户 | 查看和编辑权限 |

### 4.4 考试类型 (grades.exam_type)

| 值 | 说明 |
|----|------|
| 期中 | 期中考试 |
| 期末 | 期末考试 |
| 补考 | 补考 |
| 重修 | 重修考试 |

## 5. 视图设计

### 5.1 学生成绩汇总视图

```sql
CREATE VIEW v_student_grade_summary AS
SELECT 
    s.id,
    s.student_no,
    s.name,
    s.major,
    s.class_name,
    COUNT(g.id) as total_courses,
    ROUND(AVG(g.score), 2) as avg_score,
    SUM(g.credits) as total_credits,
    ROUND(AVG(
        CASE 
            WHEN g.score >= 90 THEN 4.0
            WHEN g.score >= 80 THEN 3.0
            WHEN g.score >= 70 THEN 2.0
            WHEN g.score >= 60 THEN 1.0
            ELSE 0.0
        END
    ), 2) as gpa
FROM students s
LEFT JOIN grades g ON s.id = g.student_id AND g.is_deleted = FALSE
WHERE s.is_deleted = FALSE
GROUP BY s.id, s.student_no, s.name, s.major, s.class_name;
```

### 5.2 专业统计视图

```sql
CREATE VIEW v_major_statistics AS
SELECT 
    major,
    COUNT(*) as student_count,
    COUNT(CASE WHEN status = 'active' THEN 1 END) as active_count,
    COUNT(CASE WHEN status = 'graduated' THEN 1 END) as graduated_count,
    COUNT(CASE WHEN gender = '男' THEN 1 END) as male_count,
    COUNT(CASE WHEN gender = '女' THEN 1 END) as female_count
FROM students
WHERE is_deleted = FALSE
GROUP BY major;
```

## 6. 触发器设计

### 6.1 更新时间自动更新触发器 (students)

```sql
CREATE TRIGGER update_student_timestamp 
AFTER UPDATE ON students
FOR EACH ROW
BEGIN
    UPDATE students 
    SET updated_at = CURRENT_TIMESTAMP 
    WHERE id = NEW.id;
END;
```

### 6.2 更新时间自动更新触发器 (grades)

```sql
CREATE TRIGGER update_grade_timestamp 
AFTER UPDATE ON grades
FOR EACH ROW
BEGIN
    UPDATE grades 
    SET updated_at = CURRENT_TIMESTAMP 
    WHERE id = NEW.id;
END;
```

### 6.3 更新时间自动更新触发器 (users)

```sql
CREATE TRIGGER update_user_timestamp 
AFTER UPDATE ON users
FOR EACH ROW
BEGIN
    UPDATE users 
    SET updated_at = CURRENT_TIMESTAMP 
    WHERE id = NEW.id;
END;
```

## 7. 查询示例

### 7.1 查询学生及其平均成绩

```sql
SELECT 
    s.student_no,
    s.name,
    s.major,
    s.class_name,
    ROUND(AVG(g.score), 2) as avg_score,
    COUNT(g.id) as course_count
FROM students s
LEFT JOIN grades g ON s.id = g.student_id AND g.is_deleted = FALSE
WHERE s.is_deleted = FALSE
GROUP BY s.id
ORDER BY avg_score DESC;
```

### 7.2 查询某专业的成绩分布

```sql
SELECT 
    CASE 
        WHEN score >= 90 THEN '优秀'
        WHEN score >= 80 THEN '良好'
        WHEN score >= 70 THEN '中等'
        WHEN score >= 60 THEN '及格'
        ELSE '不及格'
    END as grade_level,
    COUNT(*) as count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) as percentage
FROM grades g
JOIN students s ON g.student_id = s.id
WHERE s.major = '计算机科学与技术' 
    AND s.is_deleted = FALSE 
    AND g.is_deleted = FALSE
GROUP BY grade_level
ORDER BY 
    CASE grade_level
        WHEN '优秀' THEN 1
        WHEN '良好' THEN 2
        WHEN '中等' THEN 3
        WHEN '及格' THEN 4
        WHEN '不及格' THEN 5
    END;
```

### 7.3 查询GPA排名前10的学生

```sql
SELECT 
    s.student_no,
    s.name,
    s.major,
    s.class_name,
    ROUND(AVG(
        CASE 
            WHEN g.score >= 90 THEN 4.0
            WHEN g.score >= 80 THEN 3.0
            WHEN g.score >= 70 THEN 2.0
            WHEN g.score >= 60 THEN 1.0
            ELSE 0.0
        END
    ), 2) as gpa,
    SUM(g.credits) as total_credits
FROM students s
JOIN grades g ON s.id = g.student_id AND g.is_deleted = FALSE
WHERE s.is_deleted = FALSE
GROUP BY s.id
ORDER BY gpa DESC, total_credits DESC
LIMIT 10;
```

### 7.4 查询不及格学生名单

```sql
SELECT DISTINCT
    s.student_no,
    s.name,
    s.major,
    s.class_name,
    g.course_name,
    g.score,
    g.semester
FROM students s
JOIN grades g ON s.id = g.student_id
WHERE g.score < 60 
    AND s.is_deleted = FALSE 
    AND g.is_deleted = FALSE
ORDER BY s.student_no, g.semester;
```

## 8. 数据迁移计划

### 8.1 初始化迁移

使用Alembic创建初始迁移文件：

```bash
# 创建迁移
alembic revision --autogenerate -m "initial tables"

# 应用迁移
alembic upgrade head
```

### 8.2 种子数据

创建初始管理员用户和测试数据：

```python
# 位置: backend/app/db/init_db.py

def init_db():
    # 创建管理员用户
    admin_user = User(
        username="admin",
        email="admin@example.com",
        hashed_password=get_password_hash("admin123"),
        full_name="系统管理员",
        role="admin"
    )
    db.add(admin_user)
    
    # 创建测试学生
    test_students = [
        Student(
            student_no="2024001",
            name="张三",
            gender="男",
            major="计算机科学与技术",
            class_name="计科2401班",
            grade=2024,
            enrollment_date=date(2024, 9, 1)
        ),
        # ... 更多测试数据
    ]
    db.add_all(test_students)
    db.commit()
```

## 9. 备份策略

### 9.1 自动备份脚本

```bash
#!/bin/bash
# backup_db.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="./backups"
DB_FILE="./data/prod.db"

mkdir -p $BACKUP_DIR

# 备份数据库
cp $DB_FILE "$BACKUP_DIR/prod_${DATE}.db"

# 保留最近30天的备份
find $BACKUP_DIR -name "prod_*.db" -mtime +30 -delete

echo "Backup completed: prod_${DATE}.db"
```

### 9.2 恢复数据库

```bash
# 停止应用
# 恢复数据库文件
cp ./backups/prod_20240101_120000.db ./data/prod.db
# 重启应用
```

## 10. 性能优化建议

### 10.1 索引优化
- 为常用查询字段添加索引
- 避免过多索引影响写入性能
- 定期分析查询计划

### 10.2 查询优化
- 使用分页查询
- 避免SELECT *，只查询需要的字段
- 使用JOIN代替子查询

### 10.3 连接池配置

```python
# SQLAlchemy连接池配置
engine = create_engine(
    DATABASE_URL,
    pool_size=10,          # 连接池大小
    max_overflow=20,       # 最大溢出连接数
    pool_timeout=30,       # 获取连接超时时间
    pool_recycle=3600      # 连接回收时间
)
```

## 11. 数据库升级路径

### 11.1 迁移到PostgreSQL

如果需要迁移到PostgreSQL：

1. 导出SQLite数据
2. 转换数据格式
3. 导入到PostgreSQL
4. 更新配置文件
5. 测试验证

### 11.2 迁移到MySQL

如果需要迁移到MySQL：

1. 使用工具导出数据
2. 调整数据类型
3. 导入MySQL
4. 更新ORM配置
5. 测试验证

## 12. 注意事项

1. **软删除**: 所有表都使用 `is_deleted` 字段实现软删除，物理删除需谨慎
2. **时间戳**: 创建和更新时间由数据库自动维护
3. **外键约束**: 删除学生时会级联删除相关成绩记录
4. **唯一约束**: 学号和用户名必须唯一
5. **数据验证**: 除数据库约束外，应用层也需要进行验证
6. **事务处理**: 批量操作应使用事务确保数据一致性
7. **备份策略**: 生产环境应定期备份数据库
8. **权限控制**: SQLite文件权限应设置为600或660
