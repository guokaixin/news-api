# 新闻 API 服务

基于 FastAPI 开发的新闻资讯 API 服务，支持新闻列表查询、详情获取等功能，包含完整的 Docker 部署配置。

## 实现思路

1. **技术选型**：采用 FastAPI 框架，相比 Flask 具有自动生成 API 文档、类型提示、异步支持等优势
2. **数据库设计**：
   - 使用 SQLAlchemy ORM 操作 MySQL 数据库
   - News 表结构包含 id、title、description、content、created_at 字段
   - 为 title 字段创建索引优化查询性能
3. **功能实现**：
   - 支持关键词过滤（标题/描述）
   - 支持分页（page+limit）和偏移量（offset）查询
   - 完整的错误处理机制
4. **部署方案**：通过 Docker Compose 实现应用和数据库的一键部署

## 项目地址和拉取代码方式
```bash
1. url: https://github.com/guokaixin/news-api.git
2. git clone https://github.com/guokaixin/news-api.git
3. cd news_api
```


## 项目结构
```
news-api/                  # 项目根目录
├── src/                   # 源代码目录
│   ├── api/               # 接口路由层
│   │   ├── __init__.py
│   │   └── routes.py      # 新闻接口路由定义
│   ├── config/            # 配置层
│   │   ├── __init__.py
│   │   └── database.py    # 数据库连接配置
│   ├── crud/              # 数据操作层
│   │   ├── __init__.py
│   │   └── news.py        # 新闻数据CRUD操作
│   ├── models/            # 数据模型层
│   │   ├── __init__.py
│   │   └── news.py        # News表模型定义
│   ├── schemas/           # 数据验证/响应模型层
│   │   ├── __init__.py
│   │   └── news.py        # Pydantic模型定义
│   ├── scripts/           # 数据库脚本
│   │   ├── __init__.py
│   │   └── init_db.py     # 数据库初始化脚本
│   └── main.py            # 应用入口文件
├── .env                   # 环境变量配置（不要提交到Git）
├── .gitignore             # Git忽略文件
├── docker-compose.yml     # Docker编排配置
├── Dockerfile             # 应用打包配置
├── requirements.txt       # 项目依赖列表
└── README.md              # 项目说明文档
```


## 运行
### 本地开发环境（conda）
1. 创建虚拟环境：
    ```bash
    conda create -n api_env python=3.10 -y
    conda activate api_env
    ```
2. 安装依赖：
    ```bash
    pip install -r requirements.txt
    ```
3. 初始化数据库：
    ```bash
        python src/scripts/init_db.py
    ```
4. 启动开发服务器：
    ```bash
        python src/main.py
    ```

## 部署

### 前提条件

- 安装 Docker 和 Docker Compose
- 克隆本仓库到本地

### 启动服务

1. 进入项目根目录
2. 执行以下命令启动服务：
   ```bash
   docker-compose up -d
   ```
3. 服务启动后，会自动完成：
   - MySQL 数据库初始化
   - 新闻表结构创建
   - 测试数据插入（15 条示例新闻）

### 访问地址
- API 根路径：http://localhost:8000
- Swagger 文档：http://localhost:8000/docs
- ReDoc 文档：http://localhost:8000/redoc


