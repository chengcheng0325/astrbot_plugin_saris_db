import sqlite3
from math import exp
import json
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from datetime import datetime, timedelta
from astrbot.api import AstrBotConfig
import os

class Database_user(Star):
    def __init__(self,config, DatabaseFile, Id=None):
        database_config = config.get("database", {})
        database_name = database_config.get("user", "")
        if database_name == "": database_name = "astrbot_plugin_database_user"
        db_file = os.path.join(DatabaseFile, database_name + ".db")
        self.UID = Id
        self.UserId = f"U{Id}"
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()
        
        # 创建用户表Users   ID:自动编号   UserId:U+用户QQ    UID:用户QQ    UserName:用户名
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Users (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                UserId TEXT NOT NULL,
                UID INTEGER NOT NULL,
                UserName TEXT NOT NULL
            )
        """)

        # 创建用户签到表SignIns     ID:自动编号   UserId:U+用户QQ    SignInDate:签到日期    SignInCount:签到次数    SignInCoins:签到获得的金币
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS SignIns (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                UserId TEXT NOT NULL,
                SignInDate TEXT NOT NULL,  -- 可以存储 YYYY-MM-DD 格式的日期
                SignInCount INTEGER NOT NULL DEFAULT 1,
                SignInCoins REAL NOT NULL DEFAULT 0.0
            )
        """)

        # 创建用户表Users   ID:自动编号   UserId:U+用户QQ    UID:用户QQ    UserName:用户名
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS fish_cooling (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                UserId TEXT NOT NULL,
                cooling TEXT NOT NULL
            )
        """)


    def close(self):
        self.cursor.close()
        self.connection.close()
    
    # ********** users表操作 **********

    def insert_user(self,user_name):
        """
        向 users 表中插入一条新记录。
        Args:
            user_name: 用户名 (字符串, 支持 Emoji)。
        """
        if self.UserId is None: return
        try:
            self.cursor.execute("""
                INSERT INTO users (UserId, UID, UserName)
                VALUES (?, ?, ?)
            """, (self.UserId, self.UID, user_name))
            self.connection.commit()
        except sqlite3.Error as e:
            return f"插入用户时发生错误：{e}"
    
    def query_user(self):
        """
        根据 UserId 查询用户信息。
        Returns:
            一个元组，包含查询到的用户信息 (ID, UserId, UID, UserName)，如果没有找到则返回 None。
        """
        try:
            self.cursor.execute("""
                SELECT ID, UserId, UID, UserName
                FROM users
                WHERE UserId = ?
            """, (self.UserId,))
            result = self.cursor.fetchone()  # 获取一条记录
            return result
        except sqlite3.Error as e:
            print(f"查询用户时发生错误：{e}")
            return None

    # ********** signIns表操作 **********

    def insert_sign_in(self):
        """
        向 signIns 表中插入一条新记录。
        """
        if self.UserId is None: return
        try:
            # sign_in_date = datetime.now().strftime("%Y-%m-%d")
            sign_in_date = "2025-01-01"
            self.cursor.execute("""
                INSERT INTO signIns (UserId, SignInDate, SignInCount, SignInCoins)
                VALUES (?, ?, ?, ?)
            """, (self.UserId, sign_in_date, 0, 0.0))
            self.connection.commit()
        except sqlite3.Error as e:
            return f"插入签到记录时发生错误：{e}"
    
    def query_sign_in(self):
        """
        根据 UserId 查询用户签到信息。
        Returns:
            一个元组，包含查询到的签到信息 (ID, UserId, SignInDate, SignInCount, SignInCoins)，如果没有找到则返回 None。
        """
        try:
            self.cursor.execute("""
                SELECT ID, UserId, SignInDate, SignInCount, SignInCoins
                FROM signIns
                WHERE UserId = ?
            """, (self.UserId,))
            result = self.cursor.fetchone()  # 获取一条记录
            return result
        except sqlite3.Error as e:
            print(f"查询签到记录时发生错误：{e}")
            return None
    
    def update_sign_in(self,economy):
        """
        更新用户签到信息。
        Args:
            economy: 签到获得的金币数。
        """
        if self.UserId is None: return
        try:
            sign_in_date = datetime.now().strftime("%Y-%m-%d")
            self.cursor.execute("""
                UPDATE signIns
                SET SignInDate = ?,
                    SignInCount = SignInCount + 1,
                    SignInCoins = ?
                WHERE UserId = ?
            """, (sign_in_date, economy, self.UserId))
            self.connection.commit()
        except sqlite3.Error as e:
            return f"更新签到记录时发生错误：{e}"
    
    def query_sign_in_count(self):
        """
        查询用户签到次数。
        Returns:
            一个整数，表示用户签到次数。
        """
        if self.UserId is None: return 0
        try:
            self.cursor.execute("""
                SELECT SignInCount
                FROM signIns
                WHERE UserId = ?
            """, (self.UserId,))
            result = self.cursor.fetchone()  # 获取一条记录
            if result is None: return 0
            return result
        except sqlite3.Error as e:
            print(f"查询签到次数时发生错误：{e}")
            return 0
    
    def query_sign_in_coins(self):
        """
        查询用户签到获得的金币。
        Returns:
            一个浮点数，表示用户签到获得的金币。
        """
        if self.UserId is None: return 0.0
        try:
            self.cursor.execute("""
                SELECT SignInCoins
                FROM signIns
                WHERE UserId = ?
            """, (self.UserId,))
            result = self.cursor.fetchone()  # 获取一条记录
            if result is None: return 0.0
            return result[0]
        except sqlite3.Error as e:
            print(f"查询签到获得的金币时发生错误：{e}")
            return 0.0
    
    def query_last_sign_in_date(self):
        """
        查询用户上次签到日期。
        Returns:
            一个字符串，表示用户上次签到日期 (YYYY-MM-DD 格式)。
        """
        if self.UserId is None: return ""
        try:
            self.cursor.execute("""
                SELECT SignInDate
                FROM signIns
                WHERE UserId = ?
                ORDER BY ID DESC
                LIMIT 1
            """, (self.UserId,))
            result = self.cursor.fetchone()  # 获取一条记录
            if result is None: return ""
            return result[0]
        except sqlite3.Error as e:
            print(f"查询上次签到日期时发生错误：{e}")
            return ""
    
    # ********** fish_cooling表操作 **********

    def insert_fish_cooling(self):
        """
        向 fish_cooling 表中插入一条新记录。
        """
        if self.UserId is None: return
        try:
            self.cursor.execute("""
                INSERT INTO fish_cooling (UserId, cooling)
                VALUES (?, ?)
            """, (self.UserId, "2024-12-30 10:00:00"))
            self.connection.commit()
        except sqlite3.Error as e:
            return f"插入用户时发生错误：{e}"
    
    def query_fish_cooling(self):
        """
        根据 UserId 查询用户钓鱼冷却信息。
        Returns:
            一个元组，包含查询到的用户信息 (cooling,)，如果没有找到则返回 None。
        """
        try:
            self.cursor.execute("""
                SELECT cooling
                FROM fish_cooling
                WHERE UserId = ?
            """, (self.UserId,))
            result = self.cursor.fetchone()  # 获取一条记录
            return result
        except sqlite3.Error as e:
            print(f"查询用户时发生错误：{e}")
            return None
        
    def update_fish_cooling(self, minutes):
        """
        更新用户钓鱼冷却信息。
        Args:
            minutes: 冷却时间，单位为分钟。
        """
        if self.UserId is None: return
        try:
            cooling_time_date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cooling_time_date = datetime.strptime(cooling_time_date_str, "%Y-%m-%d %H:%M:%S")
            cooling_time_date = cooling_time_date + timedelta(minutes=minutes)
            cooling_time_date = cooling_time_date.strftime("%Y-%m-%d %H:%M:%S")
            self.cursor.execute("""
                UPDATE fish_cooling
                SET cooling = ?
                WHERE UserId = ?
            """, (cooling_time_date, self.UserId))
            self.connection.commit()
        except sqlite3.Error as e:
            return f"更新签到记录时发生错误：{e}"