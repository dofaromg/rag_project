from llama_index.core import SQLDatabase
from llama_index.core import ObjectIndex
import mysql.connector
# 连接到 MySQL 数据库
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="200220lhy",
    database="chikawaka"
)

# 创建 SQLDatabase 对象
sql_database = SQLDatabase(mydb)

# 创建索引
index = GPTSQLStructStoreIndex.from_documents(
    [],
    sql_database=sql_database,
    table_name="shujubiao"
)