import sqlite3
from math import exp
import json
# from astrbot.api.star import Context, Star, register
# from astrbot.api import logger
from datetime import datetime, timedelta
# from astrbot.api import AstrBotConfig
import os

RUNNING_SCRIPT_DIRECTORY = os.getcwd()
SQL_FILE = os.path.join(RUNNING_SCRIPT_DIRECTORY, os.path.join('data', 'plugins', 'astrbot_plugin_saris_fish', 'sql'))

class Database_fish():
    def __init__(self,config, DatabaseFile, Id=None):
        database_config = config.get("database", {})
        database_name = database_config.get("user", "")
        if database_name == "": database_name = "astrbot_plugin_database_fish"
        db_file = os.path.join(DatabaseFile, database_name + ".db")
        self.UID = Id
        self.UserId = f"U{Id}"
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

        # 创建用户表Users   自动编号，种类，价格(浮点)，稀有度，高度(列表)，生物群系(列表)，渔获品质
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

        # 创建用户表Users   自动编号，种类，价格(浮点)，稀有度，高度(列表)，生物群系(列表)，渔获品质
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

        # 创建用户表Users   自动编号，种类，价格(浮点)，稀有度，高度(列表)，生物群系(列表)，渔获品质
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS bait (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                种类 TEXT UNIQUE NOT NULL,
                渔力 INTEGER,
                价格 REAL,
                稀有度 TEXT
            )
        """)

        self._execute_sql_file("a.db", "fish.sql")

    def _execute_sql_file(self, db_file, sql_file):
        """
        读取 SQL 文件并执行其中的 SQL 语句。
        Args:
            db_file (str): 数据库文件的路径。
            sql_file (str): SQL 文件的路径。
        """
        try:
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
        根据 UserId 查询用户信息。
        Returns:
            一个元组，包含查询到的用户信息 (ID, UserId, UID, UserName)，如果没有找到则返回 None。
        """
        try:
            self.cursor.execute("SELECT * FROM fish")
            result = self.cursor.fetchall()  # 获取一条记录
            return result
        except sqlite3.Error as e:
            print(f"查询用户时发生错误：{e}")
            return None
    


    # ********** fishing_pole表操作 **********

    def get_all_fishing_pole(self):
        """
        根据 UserId 查询用户信息。
        Returns:
            一个元组，包含查询到的用户信息 (ID, UserId, UID, UserName)，如果没有找到则返回 None。
        """
        try:
            self.cursor.execute("SELECT * FROM fishing_pole")
            result = self.cursor.fetchall()  # 获取一条记录
            return result
        except sqlite3.Error as e:
            print(f"查询用户时发生错误：{e}")
            return None
    
    def get_fishing_pole_by_kind(self, 种类):
        """
        根据 UserId 查询用户签到信息。
        Returns:
            一个元组，包含查询到的签到信息 (ID, UserId, SignInDate, SignInCount, SignInCoins)，如果没有找到则返回 None。
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
            print(f"查询签到记录时发生错误：{e}")
            return None

    # # ********** bait表操作 **********

    def get_all_bait(self):
        """
        根据 UserId 查询用户信息。
        Returns:
            一个元组，包含查询到的用户信息 (ID, UserId, UID, UserName)，如果没有找到则返回 None。
        """
        try:
            self.cursor.execute("SELECT * FROM bait")
            result = self.cursor.fetchall()  # 获取一条记录
            return result
        except sqlite3.Error as e:
            print(f"查询用户时发生错误：{e}")
            return None
        
    def get_bait_by_kind(self, 种类):
        """
        根据 UserId 查询用户签到信息。
        Returns:
            一个元组，包含查询到的签到信息 (ID, UserId, SignInDate, SignInCount, SignInCoins)，如果没有找到则返回 None。
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
            print(f"查询签到记录时发生错误：{e}")
            return None

    # def insert_sign_in(self):
    #     """
    #     向 signIns 表中插入一条新记录。
    #     """
    #     if self.UserId is None: return
    #     try:
    #         # sign_in_date = datetime.now().strftime("%Y-%m-%d")
    #         sign_in_date = "2025-01-01"
    #         self.cursor.execute("""
    #             INSERT INTO signIns (UserId, SignInDate, SignInCount, SignInCoins)
    #             VALUES (?, ?, ?, ?)
    #         """, (self.UserId, sign_in_date, 0, 0.0))
    #         self.connection.commit()
    #     except sqlite3.Error as e:
    #         return f"插入签到记录时发生错误：{e}"
    
    # def query_sign_in(self):
    #     """
    #     根据 UserId 查询用户签到信息。
    #     Returns:
    #         一个元组，包含查询到的签到信息 (ID, UserId, SignInDate, SignInCount, SignInCoins)，如果没有找到则返回 None。
    #     """
    #     try:
    #         self.cursor.execute("""
    #             SELECT ID, UserId, SignInDate, SignInCount, SignInCoins
    #             FROM signIns
    #             WHERE UserId = ?
    #         """, (self.UserId,))
    #         result = self.cursor.fetchone()  # 获取一条记录
    #         return result
    #     except sqlite3.Error as e:
    #         print(f"查询签到记录时发生错误：{e}")
    #         return None
    
    # def update_sign_in(self,economy):
    #     """
    #     更新用户签到信息。
    #     """
    #     if self.UserId is None: return
    #     try:
    #         sign_in_date = datetime.now().strftime("%Y-%m-%d")
    #         self.cursor.execute("""
    #             UPDATE signIns
    #             SET SignInDate = ?,
    #                 SignInCount = SignInCount + 1,
    #                 SignInCoins = ?
    #             WHERE UserId = ?
    #         """, (sign_in_date, economy, self.UserId))
    #         self.connection.commit()
    #     except sqlite3.Error as e:
    #         return f"更新签到记录时发生错误：{e}"
    
    # def query_sign_in_count(self):
    #     """
    #     查询用户签到次数。
    #     Returns:
    #         一个整数，表示用户签到次数。
    #     """
    #     if self.UserId is None: return 0
    #     try:
    #         self.cursor.execute("""
    #             SELECT SignInCount
    #             FROM signIns
    #             WHERE UserId = ?
    #         """, (self.UserId,))
    #         result = self.cursor.fetchone()  # 获取一条记录
    #         if result is None: return 0
    #         return result
    #     except sqlite3.Error as e:
    #         print(f"查询签到次数时发生错误：{e}")
    #         return 0
    
    # def query_sign_in_coins(self):
    #     """
    #     查询用户签到获得的金币。
    #     Returns:
    #         一个浮点数，表示用户签到获得的金币。
    #     """
    #     if self.UserId is None: return 0.0
    #     try:
    #         self.cursor.execute("""
    #             SELECT SignInCoins
    #             FROM signIns
    #             WHERE UserId = ?
    #         """, (self.UserId,))
    #         result = self.cursor.fetchone()  # 获取一条记录
    #         if result is None: return 0.0
    #         return result[0]
    #     except sqlite3.Error as e:
    #         print(f"查询签到获得的金币时发生错误：{e}")
    #         return 0.0
    
    # def query_last_sign_in_date(self):
    #     """
    #     查询用户上次签到日期。
    #     Returns:
    #         一个字符串，表示用户上次签到日期 (YYYY-MM-DD 格式)。
    #     """
    #     if self.UserId is None: return ""
    #     try:
    #         self.cursor.execute("""
    #             SELECT SignInDate
    #             FROM signIns
    #             WHERE UserId = ?
    #             ORDER BY ID DESC
    #             LIMIT 1
    #         """, (self.UserId,))
    #         result = self.cursor.fetchone()  # 获取一条记录
    #         if result is None: return ""
    #         return result[0]
    #     except sqlite3.Error as e:
    #         print(f"查询上次签到日期时发生错误：{e}")
    #         return ""



# if __name__ == '__main__':
#     Database_user()