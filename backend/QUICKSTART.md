# 快速开始 - 初始化管理员用户

## 三步完成初始化

### 1️⃣ 创建环境并安装依赖
```bash
cd backend
conda create -n student_mgmt python=3.11
conda activate student_mgmt
pip install -r requirements.txt
```

### 2️⃣ 初始化数据库
```bash
python scripts/init_db.py
```

### 3️⃣ 使用管理员登录
- **用户名**: `admin`
- **密码**: `admin123`

---

## 文件结构

```
backend/
├── app/
│   ├── config/          # 配置模块
│   │   ├── settings.py  # 应用配置
│   │   └── database.py  # 数据库连接
│   ├── models/          # 数据模型
│   │   ├── base.py      # 基础模型
│   │   └── user.py      # 用户模型
│   └── utils/           # 工具函数
│       └── security.py  # 密码加密和JWT
├── scripts/
│   └── init_db.py       # 初始化脚本 ⭐
├── data/                # 数据库文件目录
├── requirements.txt     # Python依赖
├── .env.develop         # 开发环境配置
└── README.md           # 详细说明
```

---

## 重置数据库

```bash
rm data/develop.db
python scripts/init_db.py
```

---

详细说明请查看 `INIT_COMPLETED.md`
