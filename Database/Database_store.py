import sqlite3
from math import exp
import json
from datetime import datetime, timedelta

class Database_store:
    def __init__(self, id=None):
        self.userId = id
        self.uuid = f"u{id}"
        self.connection = sqlite3.connect(r'C:\Users\Administrator\Desktop\Launcher_ALL_Requirements\Manyana\data\Database\store.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS store (
                item TEXT               -- 物品标识
                name TEXT,              -- 物品的名称
                单价 INTEGER,           -- 物品的单价，整数值
                类型 TEXT,              -- 物品的类型
                描述 TEXT,              -- 物品的描述
                品质 TEXT,              -- 物品的品质
                PRIMARY KEY (item, name) -- 将 uuid 和 name 作为复合主键
            );
        ''')
        # self.cursor.execute('''
        #     CREATE TABLE IF NOT EXISTS backpack (
        #         uuid TEXT,              -- 用户的唯一标识符
        #         name TEXT,              -- 物品的名称
        #         耐久 INTEGER,           -- 物品的耐久
        #         最大耐久 INTEGER,       -- 物品的最大耐久
        #         单价 INTEGER,           -- 物品的单价，整数值
        #         类型 TEXT,              -- 物品的类型
        #         描述 TEXT,              -- 物品的描述
        #         状态 TEXT,              -- 物品的状态
        #         品质 TEXT,              -- 物品的品质
        #         PRIMARY KEY (uuid, name) -- 将 uuid 和 name 作为复合主键
        #     );
        # ''')

        # self.cursor.execute('''
        #     CREATE TABLE IF NOT EXISTS cooling (
        #         uuid TEXT,
        #         name TEXT,
        #         cooling DATETIME,
        #         PRIMARY KEY (uuid, name)
        #     )
        # ''')

    def close(self):
        self.cursor.close()
        self.connection.close()
    
    def store_rarity(self):
        '''获取商店列表'''
        if self.userId is None: return
        # uuid = f"u{self.userId}"
        result = self.cursor.execute('SELECT * FROM store').fetchall()
        # if len(result) == 0: return "空包"
        return result
    
    # def backpack_rarity_type(self,Type):
    #     '''获取用户背包内某类型物品'''
    #     if self.userId is None: return
    #     # uuid = f"u{self.userId}"
    #     result = self.cursor.execute('SELECT * FROM backpack WHERE uuid = ?,AND 类型 = ?', (self.uuid,Type,)).fetchall()
    #     if Type == "鱼竿" and len(result) == 0:
    #         self.backpack_add("木制简易钓鱼竿",5,5,2,"鱼竿","用2根小木棍制作的简易钓鱼竿，希望能钓上鱼","使用中","灰色")
    #         result = self.cursor.execute('SELECT * FROM backpack WHERE uuid = ?,AND 类型 = ?', (self.uuid,Type,)).fetchall()
    #     return result

    # def backpack_add(self, name, 耐久=0,最大耐久 = 0, 单价=0.0, 类型='物品', 描述=None,状态="不可用", 品质='灰色'):
    #     '''添加物品进背包'''
    #     if self.userId is None: return
    #     # uuid = f"u{self.userId}"
    #     self.cursor.execute('INSERT INTO backpack_fish (uuid, name, 耐久, 最大耐久, 单价, 类型, 描述,状态, 品质) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (self.uuid, name, 耐久, 最大耐久, 单价, 类型, 描述, 状态, 品质,))
    #     # if len(self.cursor.fetchall()) == 0: return "空包"
    #     self.connection.commit()

    

if __name__ == '__main__':
    db = Database_store(3079233608)
