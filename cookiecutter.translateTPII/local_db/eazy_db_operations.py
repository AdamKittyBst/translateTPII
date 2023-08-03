import sqlite3

def create_keywords_table():
    connection = sqlite3.connect('translation.db')  # Replace 'your_database_name.db' with the actual name of your SQLite database
    c = connection.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS keywords 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                 keyword TEXT,
                 translation TEXT)''')
    connection.commit()
    connection.close()

def insert_translation(keyword, translation):
    connection = sqlite3.connect('translation.db')  # Replace 'your_database_name.db' with the actual name of your SQLite database
    c = connection.cursor()
    c.execute("INSERT INTO keywords (keyword, translation) VALUES (?, ?)", (keyword, translation))
    connection.commit()
    connection.close()

if __name__ == "__main__":
    create_keywords_table()

    # Now you can use insert_translation() function to insert translated data into the 'keywords' table.
    # For example:
    keyword = "你好，世界！"
    translation = "Hello, world!"
    insert_translation(keyword, translation)
