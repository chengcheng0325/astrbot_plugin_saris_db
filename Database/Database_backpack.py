import sqlite3
from math import exp
import json
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from datetime import datetime, timedelta
from astrbot.api import AstrBotConfig
import os

class Database_backpack(Star):
    def __init__(self,config, DatabaseFile, Id=None):
        database_config = config.get("database", {})
        database_name = database_config.get("backpack", "")
        if database_name == "": database_name = "astrbot_plugin_database_backpack"
        db_file = os.path.join(DatabaseFile, database_name + ".db")
        self.UID = Id
        self.UserId = f"U{Id}"
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()
        
        # 创建背包表Backpacks   0ID:自动编号   1UserId:U+用户QQ    2ItemName:物品名称    3ItemCount:物品数量    4ItemType:物品类型    5ItemValue:物品价值    6ItemMaxDurability:物品最大耐久    7ItemCurrentDurability:物品当前耐久    8ItemUseStatus:物品使用状态(0:未使用|不能使用, 1:已使用)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Backpacks (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                UserId TEXT NOT NULL,
                ItemName TEXT NOT NULL,
                ItemCount INTEGER NOT NULL,
                ItemType TEXT NOT NULL,
                ItemValue REAL NOT NULL,
                ItemMaxDurability INTEGER NOT NULL,
                ItemCurrentDurability INTEGER NOT NULL,
                ItemUseStatus INTEGER NOT NULL
            )
        """)

    def close(self):
        self.cursor.close()
        self.connection.close()
    
    # ********** Backpacks表操作 **********

    def insert_backpack(self, item_name, item_count, item_type, item_value, item_max_durability, item_current_durability,ItemUseStatus=0):
        """
        向 Backpacks 表中插入一条新记录。
        Args:
            item_name: 物品名称 (字符串, 支持 Emoji)。
            item_count: 物品数量 (整数)。
            item_type: 物品类型 (字符串)。
            item_value: 物品价值 (浮点数)。
            item_max_durability: 物品最大耐久 (整数)。
            item_current_durability: 物品当前耐久 (整数)。
            ItemUseStatus:物品使用状态(0:未使用|不能使用, 1:已使用)
        """
        if self.UserId is None: return
        try:
            self.cursor.execute("""
                INSERT INTO Backpacks (UserId, ItemName, ItemCount, ItemType, ItemValue, ItemMaxDurability, ItemCurrentDurability, ItemUseStatus)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (self.UserId, item_name, item_count, item_type, item_value, item_max_durability, item_current_durability,ItemUseStatus))
            self.connection.commit()
        except sqlite3.Error as e:
            return f"插入背包物品时发生错误：{e}"
    
    def query_backpack(self):
        """
        根据 UserId 查询用户背包信息。
        Returns:
            一个元组，包含查询到的用户信息 (ID, UserId, ItemName, ItemCount, ItemType, ItemValue, ItemMaxDurability, ItemCurrentDurability,ItemUseStatus)，如果没有找到则返回 None。
        """
        try:
            self.cursor.execute("""
                SELECT ID, UserId, ItemName, ItemCount, ItemType, ItemValue, ItemMaxDurability, ItemCurrentDurability,ItemUseStatus
                FROM Backpacks
                WHERE UserId = ?
            """, (self.UserId,))
            result = self.cursor.fetchall()  # 获取所有记录
            return result
        except sqlite3.Error as e:
            print(f"查询用户时发生错误：{e}")
            return None
        
    def query_backpack_ID(self,ID):
        """
        根据 UserId 和 ID 查询用户背包信息。
        Returns:
            一个元组，包含查询到的用户信息 (ID, UserId, ItemName, ItemCount, ItemType, ItemValue, ItemMaxDurability, ItemCurrentDurability, ItemUseStatus)，如果没有找到则返回 None。
        """
        try:
            self.cursor.execute("""
                SELECT ID, UserId, ItemName, ItemCount, ItemType, ItemValue, ItemMaxDurability, ItemCurrentDurability,ItemUseStatus
                FROM Backpacks
                WHERE UserId = ? AND ID = ?
            """, (self.UserId, ID))
            result = self.cursor.fetchone()  # 获取一条记录
            return result
        except sqlite3.Error as e:
            print(f"查询用户时发生错误：{e}")
            return None
        
    def query_backpack_ItemName(self,item_name):
        """
        根据 UserId 和 ItemName 查询用户背包信息。
        Returns:
            一个元组，包含查询到的用户信息 (ID, UserId, ItemName, ItemCount, ItemType, ItemValue, ItemMaxDurability, ItemCurrentDurability, ItemUseStatus)，如果没有找到则返回 None。
        """
        try:
            self.cursor.execute("""
                SELECT ID, UserId, ItemName, ItemCount, ItemType, ItemValue, ItemMaxDurability, ItemCurrentDurability,ItemUseStatus
                FROM Backpacks
                WHERE UserId = ? AND ItemName = ?
            """, (self.UserId, item_name))
            result = self.cursor.fetchone()  # 获取一条记录
            return result
        except sqlite3.Error as e:
            print(f"查询用户时发生错误：{e}")
            return None
    
    def query_backpack_item_type(self,item_type):
        """
        根据 UserId 和 item_type 查询用户背包信息。
        Returns:
            一个元组，包含查询到的用户信息 (ID, UserId, ItemName, ItemCount, ItemType, ItemValue, ItemMaxDurability, ItemCurrentDurability, ItemUseStatus)，如果没有找到则返回 None。
        """
        try:
            self.cursor.execute("""
                SELECT ID, UserId, ItemName, ItemCount, ItemType, ItemValue, ItemMaxDurability, ItemCurrentDurability,ItemUseStatus
                FROM Backpacks
                WHERE UserId = ? AND ItemType = ?
            """, (self.UserId, item_type))
            result = self.cursor.fetchall()  # 获取所有记录
            return result
        except sqlite3.Error as e:
            print(f"查询用户时发生错误：{e}")
            return None
        
    
    def update_backpack_item_current_durability(self, item_current_durability, ID):
        """
        更新用户背包内指定物品的当前耐久。
        Args:
            item_current_durability: 物品当前耐久 (整数)。
            ID: 物品ID (整数)。
        """
        if self.UserId is None: return
        try:
            self.cursor.execute("""
                UPDATE Backpacks
                SET ItemCurrentDurability = ItemCurrentDurability - ?
                WHERE UserId = ? AND ID = ?
            """, (item_current_durability, self.UserId, ID))
            self.connection.commit()
        except sqlite3.Error as e:
            return f"更新背包物品时发生错误：{e}"
        
    def update_backpack_item_count(self, item_count, ID):
        """
        更新用户背包内指定物品的数量。
        Args:
            item_count: 物品数量 (整数)。
            ID: 物品ID (整数)。
        """
        if self.UserId is None: return
        try:
            self.cursor.execute("""
                UPDATE Backpacks
                SET ItemCount = ItemCount + ?
                WHERE UserId = ? AND ID = ?
            """, (item_count, self.UserId, ID))
            self.connection.commit()
        except sqlite3.Error as e:
            return f"更新背包物品数量时发生错误：{e}"
        
    def equip(self, ID):
        """
        物品装备。unequip
        Args:
            ID: 物品ID (整数)。
        """
        if self.UserId is None: return
        try:
            self.cursor.execute("""
                UPDATE Backpacks
                SET ItemUseStatus = 1
                WHERE UserId = ? AND ID = ?
            """, (self.UserId, ID))
            self.connection.commit()
        except sqlite3.Error as e:
            return f"装备物品时发生错误：{e}"
    
    def unequip(self, ID):
        """
        物品卸下。
        Args:
            ID: 物品ID (整数)。
        """
        if self.UserId is None: return
        try:
            self.cursor.execute("""
                UPDATE Backpacks
                SET ItemUseStatus = 0
                WHERE UserId = ? AND ID = ?
            """, (self.UserId, ID))
            self.connection.commit()
        except sqlite3.Error as e:
            return f"装备物品时发生错误：{e}"
    
    def delete_backpack(self, ID):
        """
        根据 ID 删除用户背包中的指定物品。
        Args:
            ID: 物品ID (整数)。
        """
        if self.UserId is None: return
        try:
            self.cursor.execute("""
                DELETE FROM Backpacks
                WHERE UserId = ? AND ID = ?
            """, (self.UserId, ID))
            self.connection.commit()
        except sqlite3.Error as e:
            return f"删除背包物品时发生错误：{e}"
    

    