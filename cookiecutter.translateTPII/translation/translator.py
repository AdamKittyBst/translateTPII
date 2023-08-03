import os
import sqlite3
from googletrans import Translator
from datetime import datetime
import keyword_table_search as kts
import history_search as hs
# 设置谷歌翻译 API 客户端
translator = Translator(service_urls=['translate.google.com'])

# SQLite数据库连接
conn = sqlite3.connect('translation.db')
c = conn.cursor()

# 创建关键字表
c.execute('''CREATE TABLE IF NOT EXISTS keywords (id INTEGER PRIMARY KEY AUTOINCREMENT, keyword text, translation text)''')

# 关闭连接
conn.close()

def get_output_file_path(input_file_path):
    # 拆分文件名和路径
    basepath, filename = os.path.split(input_file_path)
    # 拆分文件名和扩展名
    name, ext = os.path.splitext(filename)
    # 组合新的文件名和路径
    return os.path.join(basepath, name + "_translated" + ext)

def lookup(keyword):
    conn = sqlite3.connect('translation.db')
    c = conn.cursor()
    c.execute("SELECT translation FROM keywords WHERE keyword=:keyword", {'keyword':keyword})
    result = c.fetchone()
    conn.close()
    if result is None:
        return None
    else:
        return result[0]
    
# 插入翻译任务文档
def insert_translation_task(input_text, target_language, translation=None, translation_source=None):
    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = sqlite3.connect('translation.db')
    c = conn.cursor()
    c.execute("INSERT INTO translation_tasks (input_text, target_language, translation, translation_source, created_at) VALUES (?, ?, ?, ?, ?)",
              (input_text, target_language, translation, translation_source, created_at))
    conn.commit()
    conn.close()

# 插入翻译关键字
def insert_translation(keyword, translation):
    conn = sqlite3.connect('translation.db')
    c = conn.cursor()

    c.execute("INSERT INTO keywords (keyword, translation) VALUES (:keyword, :translation)", {'keyword':keyword, 'translation':translation})
    conn.commit()

    conn.close()

def translate_text(text,target_language):
    translation = translator.translate(text, target_language)
    return translation.text

def translate_file(input_file_path):
    # 获取输出文件路径
    output_file_path = get_output_file_path(input_file_path)
    # 读取文本文件
    with open(input_file_path, "r", encoding="utf-8") as f:
        text = f.read() #后面要变成文本拆分关键字和语义识别

    # 查询关键字表
    translation = lookup(text)
    is_local_translation = True

    # 如果找不到匹配项，则使用Google翻译API进行翻译
    if translation is None:
        translation = translate_text(text,target_language)
        insert_translation(text, translation)
        insert_translation_task(text, target_language, translation, "Google Translate API")
        is_local_translation = False

    # 将翻译结果写入输出文件
    with open(output_file_path, "w", encoding="utf-8") as f:
        f.write(translation)  # Only write the translation text

    return output_file_path, is_local_translation

if __name__ == "__main__":
    # 处理命令行参数：输入文件路径
    input_file_path = input("请输入需要翻译的文件路径: ")

    # 处理命令行参数：目标语言
    target_language = input("请输入目标语言（en 或 id）: ")

    # 执行翻译并输出结果文件路径和翻译来源
    output_file_path, is_local_translation = translate_file(input_file_path)
    if is_local_translation:
        print("本次翻译结果来自本地数据库。")
    else:
        print("本次翻译结果来自谷歌翻译 API。")
    print("翻译完成，结果文件保存在 " + output_file_path)

    #以下为执行导出keyword结果的程序
    # 输出文件路径
    output_file_path = os.path.join("C:\\TranslateTPII-dev", "keywords_output.txt")
    # 导出数据库记录到文件
    kts.export_keywords_to_file(output_file_path)
    print("数据导出完成，keyword结果保存在 " + output_file_path)

    #以下为执行到处history_serach结果的程序   
    # 导出数据库记录到文件
    tasks = hs.get_all_translation_tasks()
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
    print("数据导出完成，history_serach查询结果已保存在 " + output_file_path)

