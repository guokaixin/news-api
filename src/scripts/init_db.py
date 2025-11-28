import pymysql
import os
from dotenv import load_dotenv
from src.config.database import engine, Base
from src.models.news import News
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

load_dotenv()

def create_database():
    connection = pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=int(os.getenv("DB_PORT")),
        charset="utf8mb4"
    )
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {os.getenv('DB_NAME')} DEFAULT CHARACTER SET utf8mb4")
            print(f"数据库 {os.getenv('DB_NAME')} 创建/检查完成")
    finally:
        connection.close()

def create_tables():
    Base.metadata.create_all(bind=engine)
    print("数据库表结构创建/检查完成")

def insert_dummy_data():
    db = Session(bind=engine)
    try:
        db.query(News).delete()
        db.commit()

        dummy_news = [
            {
                "title": f"这是第 {i} 条fastapi新闻",
                "description": f"这是fastapi的第 {i} 条的描述，这是一个异步框架，用于测试fastapi的描述",
                "content": f"这是fastapi的第 {i} 条的功能的详细内容，这是一个异步框架，用于测试fastapi的功能的详细内容",
                "created_at": datetime.utcnow() - timedelta(days=i)
            }
            for i in range(1, 16)
        ]

        for news in dummy_news:
            db_news = News(
                title=news["title"],
                description=news["description"],
                content=news["content"],
                created_at=news["created_at"]
            )
            db.add(db_news)
        
        db.commit()
        print("15 条测试新闻数据插入完成")
    except Exception as e:
        db.rollback()
        print(f"插入测试数据失败：{e}")
    finally:
        db.close()

if __name__ == "__main__":
    try:
        create_database()
        create_tables()
        insert_dummy_data()
        print("数据库初始化全部完成！")
    except Exception as e:
        print(f"数据库初始化失败：{e}")