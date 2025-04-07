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

        # 创建鱼竿商店表fishing_rod_store   ID:自动编号    ItemName:物品名称    ItemCount:物品数量    ItemType:物品类型    ItemValue:物品价值    ItemDurability:物品耐久
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS fishing_rod_store (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                ItemName TEXT NOT NULL,
                ItemCount INTEGER NOT NULL,
                ItemType TEXT NOT NULL,
                ItemValue REAL NOT NULL,
                ItemDurability INTEGER NOT NULL
            )
        """)

        # 创建鱼饵商店表bait_store   ID:自动编号    ItemName:物品名称    ItemCount:物品数量    ItemType:物品类型    ItemValue:物品价值
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS bait_store (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                ItemName TEXT NOT NULL,
                ItemCount INTEGER NOT NULL,
                ItemType TEXT NOT NULL,
                ItemValue REAL NOT NULL
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
                if self.get_all_fishing_rod_store() == []:
                    self.cursor.execute(sql_script)
                    self.connection.commit()
                    print(f"成功执行 SQL 文件 '{sql_file}'")
                
                with open(os.path.join(FISHSQL_FILE, "1"+sql_file), 'r', encoding='utf-8') as f:  # 使用 utf-8 编码处理文件
                    sql_script = f.read()
                if self.get_all_bait_store() == []:
                    self.cursor.execute(sql_script)
                    self.connection.commit()
                    print(f"成功执行 SQL 文件 '1{sql_file}'")
            
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
    
    # ********** fishing_rod_store表操作 **********

    def get_all_fishing_rod_store(self):
        """
        获取所有 渔具商店 鱼竿 信息。
        Returns:
            list: 包含所有渔具商店鱼竿信息的列表。
        """
        self.cursor.execute("SELECT * FROM fishing_rod_store")
        result = self.cursor.fetchall()
        return result
    
    def get_fishing_rod_store_item(self, ID):
        """
        获取指定名称的 渔具商店 鱼竿 信息。
        Args:
            ID (int): 物品ID。
        Returns:
            list: 包含指定渔具商店鱼竿信息的列表。
        """
        self.cursor.execute("SELECT * FROM fishing_rod_store WHERE ID=?", (ID,))
        result = self.cursor.fetchone()
        return result
    
    # ********** bait_store表操作 **********

    def get_all_bait_store(self):
        """
        获取所有 渔具商店 鱼饵 信息。  
        Returns:
            list: 包含所有鱼饵物品信息的列表。
        """
        self.cursor.execute("SELECT * FROM bait_store")
        result = self.cursor.fetchall()
        return result
    
    def get_bait_store_item(self, ID):
        """
        获取指定名称的 渔具商店 鱼饵 信息。
        Args:
            ID (int): 物品ID。
        Returns:
            list: 包含指定鱼饵物品信息的列表。
        """
        self.cursor.execute("SELECT * FROM bait_store WHERE ID=?", (ID,))
        result = self.cursor.fetchone()
        return result

    def get_bait_store_item_ItemName(self, ItemName):
        """
        获取指定名称的 渔具商店 鱼饵 信息。
        Args:
            ItemName (str): 物品名称。
        Returns:
            list: 包含指定鱼饵物品信息的列表。
        """
        self.cursor.execute("SELECT * FROM bait_store WHERE ItemName=?", (ItemName,))
        result = self.cursor.fetchone()
        return result