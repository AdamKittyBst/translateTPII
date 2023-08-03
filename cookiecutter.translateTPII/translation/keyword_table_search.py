import os
import sqlite3

def export_keywords_to_file(output_file_path):
    # 连接到数据库
    conn = sqlite3.connect('translation.db')
    c = conn.cursor()

    # 执行SELECT语句查询keywords表的数据
    c.execute("SELECT keyword, translation FROM keywords")

    # 获取查询结果
    results = c.fetchall()

    # 关闭数据库连接
    conn.close()

    # 将查询结果保存到文本文件
    with open(output_file_path, "w", encoding="utf-8") as f:
        for keyword, translation in results:
            f.write(f"{keyword}\t{translation}\n")

if __name__ == "__main__":
    # 输出文件路径
    output_file_path = os.path.join("C:\\TranslateTPII-dev", "keywords_output.txt")

    # 导出数据库记录到文件
    export_keywords_to_file(output_file_path)

    print("数据导出完成，结果保存在 " + output_file_path)
