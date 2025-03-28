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
    SQL_FILE = os.path.join(RUNNING_SCRIPT_DIRECTORY, os.path.join('data', 'plugins', 'astrbot_plugin_saris_fish', 'sql'))
else:
    SQL_FILE = False

class Database_fish():
    def __init__(self,config, DatabaseFile, Id=None):
        database_config = config.get("database", {})
        database_name = database_config.get("fish", "")
        if database_name == "": database_name = "astrbot_plugin_database_fish"
        db_file = os.path.join(DatabaseFile, database_name + ".db")
        self.UID = Id
        self.UserId = f"U{Id}"
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

        # 创建鱼表fish   自动编号，种类，价格(浮点)，稀有度，高度(列表)，生物群系(列表)，渔获品质
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS fish (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                种类 TEXT UNIQUE NOT NULL,
                价格 REAL,
                稀有度 TEXT,
                高度 TEXT,
                生物群系 TEXT,
                渔获品质 TEXT,
                是否任务 INTEGER
            )
        """)

        # 创建鱼竿表fishing_pole   自动编号，种类，渔力(整数)，价格(浮点)，稀有度，最大耐久，最小耐久
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS fishing_pole (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                种类 TEXT UNIQUE NOT NULL,
                渔力 INTEGER,
                价格 REAL,
                稀有度 TEXT,
                最大耐久 INTEGER,
                最小耐久 INTEGER
            )
        """)

        # 创建鱼饵表bait   自动编号，种类，渔力(整数)，价格(浮点)，稀有度
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS bait (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                种类 TEXT UNIQUE NOT NULL,
                渔力 INTEGER,
                价格 REAL,
                稀有度 TEXT
            )
        """)

        self._execute_sql_file("fish.sql")

    def _execute_sql_file(self, sql_file):
        """
        读取 SQL 文件并执行其中的 SQL 语句。
        Args:
            sql_file (str): SQL 文件的路径。
        """
        try:
            if not SQL_FILE: return
            with open(os.path.join(SQL_FILE, sql_file), 'r', encoding='utf-8') as f:  # 使用 utf-8 编码处理文件
                sql_script = f.read()
            if self.get_all_fish() == []:
                self.cursor.execute(sql_script)
                self.connection.commit()
                print(f"成功执行 SQL 文件 '{sql_file}'")
            
            with open(os.path.join(SQL_FILE, f"1{sql_file}"), 'r', encoding='utf-8') as f:  # 使用 utf-8 编码处理文件
                sql_script = f.read()
            if self.get_all_fishing_pole() == []:
                self.cursor.execute(sql_script)
                self.connection.commit()
                print(f"成功执行 SQL 文件 '{sql_file}'")
            
            with open(os.path.join(SQL_FILE, f"2{sql_file}"), 'r', encoding='utf-8') as f:  # 使用 utf-8 编码处理文件
                sql_script = f.read()
            if self.get_all_bait() == []:
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



    def close(self):
        self.cursor.close()
        self.connection.close()
    
    # ********** fish表操作 **********
    
    def get_all_fish(self):
        """
        获取所有鱼的信息。
        Returns:
            一个元组，包含查询到的鱼的信息 (ID, 种类, 价格, 稀有度, 高度, 生物群系, 渔获品质, 是否任务)，如果没有找到则返回 None。
        """
        try:
            self.cursor.execute("SELECT * FROM fish")
            result = self.cursor.fetchall()  # 获取一条记录
            return result
        except sqlite3.Error as e:
            print(f"获取鱼信息时发生错误：{e}")
            return None
    


    # ********** fishing_pole表操作 **********

    def get_all_fishing_pole(self):
        """
        获取所有鱼竿的信息。
        Returns:
            一个元组，包含查询到的鱼竿的信息 (ID, 种类, 渔力, 价格, 稀有度, 最大耐久, 最小耐久)，如果没有找到则返回 None。
        """
        try:
            self.cursor.execute("SELECT * FROM fishing_pole")
            result = self.cursor.fetchall()  # 获取一条记录
            return result
        except sqlite3.Error as e:
            print(f"获取鱼竿信息时发生错误：{e}")
            return None
    
    def get_fishing_pole_by_kind(self, 种类):
        """
        根据 鱼竿种类 查询鱼竿信息。
        Args:
            种类 (str): 鱼竿名称。
        Returns:
            一个元组，包含查询到的鱼竿信息 (ID, 种类, 渔力, 价格, 稀有度, 最大耐久, 最小耐久)，如果没有找到则返回 None。
        """
        try:
            self.cursor.execute("""
                SELECT *
                FROM fishing_pole
                WHERE 种类 = ?
            """, (种类,))
            result = self.cursor.fetchone()  # 获取一条记录
            return result
        except sqlite3.Error as e:
            print(f"查询鱼竿信息时发生错误：{e}")
            return None

    # # ********** bait表操作 **********

    def get_all_bait(self):
        """
        获取所有鱼饵的信息。
        Returns:
            一个元组，包含查询到的鱼饵的信息 (ID, 种类, 渔力, 价格, 稀有度)，如果没有找到则返回 None。
        """
        try:
            self.cursor.execute("SELECT * FROM bait")
            result = self.cursor.fetchall()  # 获取一条记录
            return result
        except sqlite3.Error as e:
            print(f"获取鱼饵信息时发生错误：{e}")
            return None
        
    def get_bait_by_kind(self, 种类):
        """
        根据 鱼饵种类 查询鱼饵信息。
        Args:
            种类 (str): 鱼饵名称。
        Returns:
            一个元组，包含查询到的鱼饵信息 (ID, 种类, 渔力, 价格, 稀有度)，如果没有找到则返回 None。
        """
        try:
            self.cursor.execute("""
                SELECT *
                FROM bait
                WHERE 种类 = ?
            """, (种类,))
            result = self.cursor.fetchone()  # 获取一条记录
            return result
        except sqlite3.Error as e:
            print(f"查询鱼饵信息时发生错误：{e}")
            return None
