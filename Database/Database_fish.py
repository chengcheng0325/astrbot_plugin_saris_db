# import sqlite3
# import json
# from datetime import datetime, timedelta

# class Database_fish:
#     def __init__(self, id=None):
#         self.userId = id
#         self.connection = sqlite3.connect(r'C:\Users\Administrator\Desktop\Launcher_ALL_Requirements\Manyana\data\Database\fish.db')
#         self.cursor = self.connection.cursor()
        
#         # 创建表格
#         self.cursor.execute('''
#             CREATE TABLE IF NOT EXISTS fish_pond (
#                            name TEXT NOT NULL,                   -- 名称
#                            max_size INTEGER NOT NULL,            -- 最大大小
#                            min_size INTEGER NOT NULL,            -- 最小大小
#                            price REAL NOT NULL,                  -- 单价
#                            description TEXT NOT NULL,            -- 描述
#                            type TEXT NOT NULL,                   -- 种类
#                            rarity TEXT NOT NULL                  -- 稀有度
# );
#         ''')
#         self.cursor.execute('''
#             CREATE TABLE IF NOT EXISTS fish_pole (
#                         item TEXT,               -- 物品标识
#                         name TEXT ,             -- 名称
#                         耐久 INTEGER,           -- 物品的大小
#                         最大耐久 INTEGER,       -- 物品的最大耐久
#                         强度 REAL,            -- 鱼竿的上钩率
#                         经验加成 REAL,        -- 经验加成
#                         金币加成 REAL,        -- 金币加成
#                         特殊效果 TEXT,           -- 特殊效果
#                         PRIMARY KEY (item, name)
                        
# );
#         ''')
#                 # self.cursor.execute('''
#         #     CREATE TABLE IF NOT EXISTS rod_levels (
#         #         userId TEXT PRIMARY KEY,
#         #         level INTEGER
#         #     )
#         # ''')
#         # self.cursor.execute('''
#         #     CREATE TABLE IF NOT EXISTS backpack_levels (
#         #         userId TEXT PRIMARY KEY,
#         #         level INTEGER
#         #     )
#         # ''')
#         # self.cursor.execute('''
#         #     CREATE TABLE IF NOT EXISTS backpack (
#         #         userId TEXT,
#         #         backPackData TEXT
#         #     )
#         # ''')
#         # self.cursor.execute('''
#         #     CREATE TABLE IF NOT EXISTS pool (
#         #         fishName TEXT,
#         #         value INTEGER,
#         #         count INTEGER,
#         #         owner TEXT,
#         #         PRIMARY KEY (fishName, owner)
#         #     )
#         # ''')
#         # self.cursor.execute('''
#         #     CREATE TABLE IF NOT EXISTS cooling (
#         #         userId TEXT PRIMARY KEY,
#         #         fishing_time DATETIME,
#         #         release_time DATETIME
#         #     )
#         # ''')
#         self.connection.commit()

#     def close(self):
#         self.cursor.close()
#         self.connection.close()

#     def fish_rarity(self, rarity):
#         '''
#         根据鱼稀有度获取鱼列表
        
#         返回:
#         0: name
#         1: 最大
#         2: 最小
#         3: 单价
#         4: 描述
#         5: 类型
#         6: 稀有度
#         '''
#         if rarity is None: return
#         self.cursor.execute('SELECT * FROM fish_pond WHERE rarity = ?', (rarity,))
#         return self.cursor.fetchall()
    
    


#     def fish_pole_rarity(self, item):
#         '''获取鱼竿属性'''
#         if self.userId is None: return
#         self.cursor.execute('SELECT * FROM fish_pole WHERE item = ?', (item,))
#         return self.cursor.fetchall()[0]


#     # # 冷却相关
#     # def fishing_cooling(self):
#     #     if self.userId is None: return
#     #     result = self.cursor.execute('SELECT fishing_time FROM cooling WHERE userId = ?', (self.userId,))
#     #     if len(result.fetchall()) == 0:
#     #         self.initialization_cooling()
#     #     result = self.cursor.execute('SELECT fishing_time FROM cooling WHERE userId = ?', (self.userId,))
#     #     return self.cursor.fetchone()[0]

#     # def set_fishing_cooling(self, cooling):
#     #     if self.userId is None: return
#     #     self.cursor.execute("UPDATE cooling SET fishing_time = ? WHERE userId = ?", (cooling, self.userId))
#     #     self.connection.commit()

#     # def release_cooling(self):
#     #     if self.userId is None: return
#     #     result = self.cursor.execute('SELECT release_time FROM cooling WHERE userId = ?', (self.userId,))
#     #     if len(result.fetchall()) == 0:
#     #         self.initialization_cooling()
#     #     result = self.cursor.execute('SELECT release_time FROM cooling WHERE userId = ?', (self.userId,))
#     #     return self.cursor.fetchone()[0]

#     # def set_release_cooling(self, cooling):
#     #     if self.userId is None: return
#     #     self.cursor.execute("UPDATE cooling SET release_time = ? WHERE userId = ?", (cooling, self.userId))
#     #     self.connection.commit()

#     # def initialization_cooling(self):
#     #     if self.userId is None: return
#     #     t = datetime.now()
#     #     self.cursor.execute('INSERT INTO cooling (userId, fishing_time, release_time) VALUES (?, ?, ?)', (self.userId, t, t))
#     #     self.connection.commit()

#     # # 鱼塘相关
#     # def updatePool(self, fishData):
#     #     self.cursor.execute('DELETE FROM pool')
#     #     for data in fishData:
#     #         if data[1] == 0: continue
#     #         self.cursor.execute('INSERT INTO pool (fishName, value, count, owner) VALUES (?, ?, ?, ?)', data)
#     #     self.connection.commit()

#     # def insertFish(self, fishName, value, number):
#     #     if self.userId is None: return
#     #     self.cursor.execute('INSERT INTO pool (fishName, value, count, owner) VALUES (?, ?, ?, ?)', (fishName, value, number, self.userId))
#     #     self.connection.commit()

#     # def reduceFish(self, fishName):
#     #     self.cursor.execute('UPDATE pool SET count = count - 1 WHERE fishName = ? AND owner = ?', (fishName, self.userId))
#     #     self.connection.commit()
#     #     if self.cursor.execute('SELECT count FROM pool WHERE fishName = ? AND owner = ?', (fishName, self.userId)).fetchone()[0] == 0:
#     #         self.cursor.execute('DELETE FROM pool WHERE fishName = ? AND owner = ?', (fishName, self.userId))
#     #         self.connection.commit()

#     # def removeFish(self, fishName):
#     #     self.cursor.execute('DELETE FROM pool WHERE fishName = ? AND owner = ?', (fishName, self.userId))
#     #     self.connection.commit()

#     # def selectFishOwner(self, fishName):
#     #     self.cursor.execute('SELECT owner FROM pool WHERE fishName = ?', (fishName,))
#     #     result = self.cursor.fetchall()
#     #     if not result: return None, None
#     #     userId = result[0][0]
#     #     self.cursor.execute('SELECT name FROM users WHERE userId = ?', (userId,))
#     #     return userId, self.cursor.fetchall()[0][0]

#     # def selectFish(self, fishName):
#     #     self.cursor.execute('SELECT * FROM pool WHERE fishName = ? AND owner = ?', (fishName, self.userId))
#     #     return self.cursor.fetchall()

#     # def selectPool(self):
#     #     self.cursor.execute('SELECT * FROM pool WHERE owner = ?', (self.userId,))
#     #     return self.cursor.fetchall()
    
#     # # 用户信用点变更
#     # def selectUser(self):
#     #     if self.userId is None: return
#     #     self.cursor.execute('SELECT * FROM users WHERE userId = ?', (self.userId,))
#     #     return self.cursor.fetchall()

#     # def selectAllUser(self):
#     #     self.cursor.execute('SELECT * FROM users')
#     #     return self.cursor.fetchall()

#     # # 鱼竿相关
#     # def selectRodLevel(self):
#     #     if self.userId is None: return
#     #     result = self.cursor.execute('SELECT level FROM rod_levels WHERE userId = ?', (self.userId,))
#     #     if len(result.fetchall()) == 0:
#     #         self.insertRodLevel(1)
#     #     result = self.cursor.execute('SELECT level FROM rod_levels WHERE userId = ?', (self.userId,))
#     #     return self.cursor.fetchone()[0]

#     # def selectAllRodLevel(self):
#     #     self.cursor.execute('SELECT * FROM rod_levels')
#     #     return self.cursor.fetchall()

#     # def insertRodLevel(self, level):
#     #     if self.userId is None: return
#     #     self.cursor.execute('INSERT INTO rod_levels (userId, level) VALUES (?, ?)', (self.userId, level))
#     #     self.connection.commit()

#     # def updateRodLevel(self, level):
#     #     if self.userId is None: return
#     #     self.selectRodLevel()
#     #     if self.userId is None: return
#     #     self.cursor.execute('UPDATE rod_levels SET level = ? WHERE userId = ?', (level, self.userId))
#     #     self.connection.commit()

#     # def increaseRodLevel(self):
#     #     if self.userId is None: return
#     #     level = self.selectRodLevel()
#     #     pointNeeded = int(20 * (2 ** (level - 1)))
#     #     self.cursor.execute('UPDATE rod_levels SET level = level + 1 WHERE userId = ?', (self.userId,))
#     #     self.connection.commit()

#     # # 背包相关
#     # def updateBackpack(self, backPackData):
#     #     if self.userId is None: return
#     #     dataString = json.dumps(backPackData)
#     #     self.cursor.execute('UPDATE backpack SET backPackData = ? WHERE userId = ?', (dataString, self.userId))
#     #     self.connection.commit()

#     # def selectBackpackLevel(self):
#     #     if self.userId is None: return
#     #     result = self.cursor.execute('SELECT level FROM backpack_levels WHERE userId = ?', (self.userId,))
#     #     if len(result.fetchall()) == 0:
#     #         self.insertBackpackLevel(1)
#     #     result = self.cursor.execute('SELECT level FROM backpack_levels WHERE userId = ?', (self.userId,))
#     #     return self.cursor.fetchone()[0]

#     # def selectAllBackpackLevel(self):
#     #     self.cursor.execute('SELECT * FROM backpack_levels')
#     #     return self.cursor.fetchall()

#     # def insertBackpackLevel(self, level):
#     #     if self.userId is None: return
#     #     self.cursor.execute('INSERT INTO backpack_levels (userId, level) VALUES (?, ?)', (self.userId, level))
#     #     self.connection.commit()

#     # def increaseBackpackLevel(self):
#     #     if self.userId is None: return
#     #     level = self.selectBackpackLevel()
#     #     pointNeeded = int((2.5 ** level) * 15)
#     #     self.cursor.execute('UPDATE backpack_levels SET level = level + 1 WHERE userId = ?', (self.userId,))
#     #     self.connection.commit()

#     # def selectBackpack(self):
#     #     if self.userId is None: return []
#     #     self.cursor.execute('SELECT * FROM backpack WHERE userId = ?', (self.userId,))
#     #     result = self.cursor.fetchall()
#     #     if not result:
#     #         self.cursor.execute('INSERT INTO backpack (userId, backPackData) VALUES (?, "[]")', (self.userId,))
#     #         self.connection.commit()
#     #     return json.loads(result[0][1]) if result else []



# if __name__ == '__main__':
#     db = Database_fish(3079233608)
#     yg = db.fish_pole_rarity("fish_pole_0")
#     print(yg)
#     # data = [(item[2]) for item in yg if item[9] == '使用中']
#     # item = data[0]
#     # print(item)
#     # print(状态)
#     # fish_cooling_str = db.cooling_rarity("钓鱼")
#     # fish_cooling = datetime.strptime(fish_cooling_str, "%Y-%m-%d %H:%M:%S.%f")
#     # time_without_milliseconds = fish_cooling.strftime("%Y-%m-%d %H:%M:%S")
#     # print(time_without_milliseconds)
#     # # print(f"{fish_cooling.strftime(r"%Y-%m-%d %H:%M:%S")}")