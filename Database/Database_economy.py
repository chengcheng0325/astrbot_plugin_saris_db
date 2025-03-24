import sqlite3
from math import exp
import os
from astrbot.api.star import Context, Star, register

class Database_economy(Star):
    def __init__(self, config, DatabaseFile, Id=None):
        database_config = config.get("database", {})
        database_name = database_config.get("economy", "")
        if database_name == "":
            database_name = "astrbot_plugin_database_economy"
        db_file = os.path.join(DatabaseFile, database_name + ".db")
        self.UID = Id
        self.UserId = f"U{Id}"
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

        # 创建用户表wallet   ID:自动编号   UserId:U+用户QQ    Economy:用户金币
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS wallet (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                UserId TEXT NOT NULL,
                Economy REAL NOT NULL
            )
        """)
        self.connection.commit()  # 确保创建表后提交更改

    def close(self):
        self.cursor.close()
        self.connection.close()

    def insert_user(self):
        """
        插入新用户，并设置初始金币。

        Args:
            initial_economy: 初始金币数量，默认为0。
        """
        if self.UserId is None: return
        try:
            self.cursor.execute("INSERT INTO wallet (UserId, Economy) VALUES (?, ?)", (self.UserId, 0.0))
            self.connection.commit()
        except sqlite3.Error as e:
            return f"插入用户时发生错误：{e}"

    def add_economy(self, amount):
        """
        增加用户金币。

        Args:
            amount: 要增加的金币数量。
        """
        if self.UserId is None: return
        self.cursor.execute("UPDATE wallet SET Economy = Economy + ? WHERE UserId = ?", (amount, self.UserId))
        self.connection.commit()

    def subtract_economy(self, amount):
        """
        减少用户金币。

        Args:
            amount: 要减少的金币数量。如果余额不足，则设置为0。
        """
        if self.UserId is None: return
        self.cursor.execute("UPDATE wallet SET Economy = MAX(0, Economy - ?) WHERE UserId = ?", (amount, self.UserId))
        self.connection.commit()

    def get_economy(self):
        """
        获取用户金币。

        Returns:
            用户的金币数量。如果用户不存在，则返回 None。
        """
        try:
            self.cursor.execute("SELECT Economy FROM wallet WHERE UserId = ?", (self.UserId,))
            result = self.cursor.fetchone()  # 获取一条记录
            return result
        except sqlite3.Error as e:
            print(f"查询用户时发生错误：{e}")
            return None
        

