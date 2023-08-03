import os
import sqlite3
from datetime import datetime

# 创建翻译任务集合数据库和表
def create_translation_tasks_table():
    conn = sqlite3.connect('translation.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS translation_tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    input_text TEXT,
                    target_language TEXT,
                    translation TEXT,
                    translation_source TEXT,
                    created_at TEXT)''')
    conn.commit()
    conn.close()

# 初始化刷新   
def delete_all_records_from_translation_tasks():
    conn = sqlite3.connect('translation.db')
    c = conn.cursor()

    # 执行删除表中所有记录的SQL语句
    c.execute("DELETE FROM translation_tasks")

    # 提交更改并关闭连接
    conn.commit()
    conn.close()

# 插入翻译任务文档
def insert_translation_task(input_text, target_language, translation=None, translation_source=None):
    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = sqlite3.connect('translation.db')
    c = conn.cursor()
    c.execute("INSERT INTO translation_tasks (input_text, target_language, translation, translation_source, created_at) VALUES (?, ?, ?, ?, ?)",
              (input_text, target_language, translation, translation_source, created_at))
    conn.commit()
    conn.close()

# 查询翻译任务集合中的所有任务文档
def get_all_translation_tasks():
    conn = sqlite3.connect('translation.db')
    c = conn.cursor()
    c.execute("SELECT * FROM translation_tasks")
    tasks = c.fetchall()
    conn.close()
    return tasks

# 初始化数据
def initialize_data():
    # 连接数据库
    conn = sqlite3.connect('translation.db')
    c = conn.cursor()
    # 查询表中的记录数
    c.execute("SELECT COUNT(*) FROM translation_tasks")
    count = c.fetchone()[0]
    # 关闭数据库连接
    conn.close()
    # 如果表中没有记录，则执行初始化操作
    if count == 0:
        create_translation_tasks_table()
        delete_all_records_from_translation_tasks()

        # 插入一些示例翻译任务文档
        insert_translation_task("你好，世界！", "en", "Hello, world!", "Google Translate API")
        insert_translation_task("谢谢！", "en", "Thank you!", "Local Database")
        insert_translation_task("我爱编程。", "id", "Saya suka pemrograman.", "Google Translate API")


if __name__ == "__main__":
    # 初始化数据
    initialize_data()

    # 查询所有翻译任务文档
    tasks = get_all_translation_tasks()

    # 将查询结果输出到本地文件
    output_file_path = os.path.join("C:\\TranslateTPII-dev", "translation_tasks_output.txt")
    with open(output_file_path, "w", encoding="utf-8") as f:
        for task in tasks:
            task_id, input_text, target_language, translation, translation_source, created_at = task
            f.write(f"Task ID: {task_id}\n")
            f.write(f"Input Text: {input_text}\n")
            f.write(f"Target Language: {target_language}\n")
            f.write(f"Translation: {translation}\n")
            f.write(f"Translation Source: {translation_source}\n")
            f.write(f"Created At: {created_at}\n\n")

    print("数据初始化完成，查询结果已保存在 " + output_file_path)
