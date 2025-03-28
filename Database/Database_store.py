import sqlite3
from math import exp
import json
# from astrbot.api.star import Context, Star, register
# from astrbot.api import logger
from datetime import datetime, timedelta
# from astrbot.api import AstrBotConfig
import os

RUNNING_SCRIPT_DIRECTORY = os.getcwd()
if os.path.exists(os.path.join('data', 'plugins', 'astrbot_plugin_saris_fish', 'sql')):
    FISHSQL_FILE = os.path.join(RUNNING_SCRIPT_DIRECTORY, os.path.join('data', 'plugins', 'astrbot_plugin_saris_fish', 'sql'))
else:
    FISHSQL_FILE = False
SQL_FILE = os.path.join(RUNNING_SCRIPT_DIRECTORY, os.path.join('data', 'plugins', 'astrbot_plugin_saris_db', 'sql'))

class Database_store():
    def __init__(self,config, DatabaseFile, Id=None):
        database_config = config.get("database", {})
        database_name = database_config.get("store", "")
        if database_name == "": database_name = "astrbot_plugin_database_store"
        db_file = os.path.join(DatabaseFile, database_name + ".db")
        self.UID = Id
        self.UserId = f"U{Id}"
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

        # 创建商店表store   ID:自动编号    ItemName:物品名称    ItemCount:物品数量    ItemType:物品类型    ItemValue:物品价值    ItemDurability:物品耐久
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS store (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                ItemName TEXT NOT NULL,
                ItemCount INTEGER NOT NULL,
                ItemType TEXT NOT NULL,
                ItemValue REAL NOT NULL,
                ItemDurability INTEGER NOT NULL
            )
        """)

        # 创建钓鱼商店表fishstore   ID:自动编号    ItemName:物品名称    ItemCount:物品数量    ItemType:物品类型    ItemValue:物品价值    ItemDurability:物品耐久
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS fishstore (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                ItemName TEXT NOT NULL,
                ItemCount INTEGER NOT NULL,
                ItemType TEXT NOT NULL,
                ItemValue REAL NOT NULL,
                ItemDurability INTEGER NOT NULL
            )
        """)
    
        self._execute_sql_file("store.sql")
    
    def close(self):
        self.cursor.close()
        self.connection.close()

    def _execute_sql_file(self, sql_file):
        """
        读取 SQL 文件并执行其中的 SQL 语句。
        Args:
            sql_file (str): SQL 文件的路径。
        """
        try:
            if FISHSQL_FILE: 
                with open(os.path.join(FISHSQL_FILE, sql_file), 'r', encoding='utf-8') as f:  # 使用 utf-8 编码处理文件
                    sql_script = f.read()
                if self.get_all_fish_store() == []:
                    self.cursor.execute(sql_script)
                    self.connection.commit()
                    print(f"成功执行 SQL 文件 '{sql_file}'")
            
            with open(os.path.join(SQL_FILE, f"{sql_file}"), 'r', encoding='utf-8') as f:  # 使用 utf-8 编码处理文件
                sql_script = f.read()
            if self.get_all_store() == []:
                self.cursor.execute(sql_script)
                self.connection.commit()
                print(f"成功执行 SQL 文件 '{sql_file}'")
        
        except sqlite3.Error as e:
            print(f"执行 SQL 文件时发生错误: {e}")
        except FileNotFoundError:
            print(f"找不到 SQL 文件: {sql_file}")
        except Exception as e:  # 捕获其他异常
            print(f"发生未知错误: {e}")
        finally:
            pass
    
    # ********** store表操作 **********

    def get_all_store(self):
        """
        获取所有商店中的物品信息。
        Returns:
            list: 包含所有商店物品信息的列表。
        """
        self.cursor.execute("SELECT * FROM store")
        result = self.cursor.fetchall()
        return result
    
    def get_store_item(self, ID):
        """
        获取指定名称的物品信息。
        Args:
            ID (int): 物品ID。
        Returns:
            list: 包含指定物品信息的列表。
        """
        self.cursor.execute("SELECT * FROM store WHERE ItemName=?", (ID,))
        result = self.cursor.fetchone()
        return result
    
    # ********** fishstore表操作 **********

    def get_all_fish_store(self):
        """
        获取所有钓鱼商店中的物品信息。
        Returns:
            list: 包含所有钓鱼杆物品信息的列表。
        """
        self.cursor.execute("SELECT * FROM fishstore")
        result = self.cursor.fetchall()
        return result
    
    def get_fish_store_item(self, ID):
        """
        获取指定名称的钓鱼商店物品信息。
        Args:
            ID (int): 物品ID。
        Returns:
            list: 包含指定钓鱼杆物品信息的列表。
        """
        self.cursor.execute("SELECT * FROM fishstore WHERE ID=?", (ID,))
        result = self.cursor.fetchone()
        return result
