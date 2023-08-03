import sqlite3
import os

# 创建或连接到SQLite数据库
db_path = "translation.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 创建翻译任务集合表
def create_translation_task_table():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS translation_tasks (
            id INTEGER PRIMARY KEY,
            input_text TEXT NOT NULL,
            target_language TEXT NOT NULL,
            translation TEXT,
            translation_source TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()

# 创建关键字表集合表
def create_keyword_table():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS keywords (
            id INTEGER PRIMARY KEY,
            keyword TEXT NOT NULL,
            translation TEXT NOT NULL
        )
    """)
    conn.commit()

# 插入翻译任务
def insert_translation_task(input_text, target_language, translation, translation_source):
    cursor.execute("""
        INSERT INTO translation_tasks (input_text, target_language, translation, translation_source)
        VALUES (?, ?, ?, ?)
    """, (input_text, target_language, translation, translation_source))
    conn.commit()

# 插入关键字表
def insert_keyword(keyword, translation):
    cursor.execute("""
        INSERT INTO keywords (keyword, translation)
        VALUES (?, ?)
    """, (keyword, translation))
    conn.commit()

# 查询关键字翻译
def query_keyword_translation(keyword):
    cursor.execute("""
        SELECT translation FROM keywords WHERE keyword = ?
    """, (keyword,))
    result = cursor.fetchone()
    return result[0] if result else None

# 查询翻译任务
def query_translation_task(input_text, target_language):
    cursor.execute("""
        SELECT translation, translation_source FROM translation_tasks 
        WHERE input_text = ? AND target_language = ? 
        ORDER BY created_at DESC LIMIT 1
    """, (input_text, target_language))
    result = cursor.fetchone()
    return result if result else (None, None)

# 关闭数据库连接
def close_connection():
    cursor.close()
    conn.close()

# 如果数据库文件已存在，则直接连接，否则创建新的数据库
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
else:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    create_translation_task_table()
    create_keyword_table()
