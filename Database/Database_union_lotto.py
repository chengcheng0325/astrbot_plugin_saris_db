import sqlite3
from math import exp
import json
from datetime import datetime, timedelta
# pip install mysql-connector-python

class Database_union_lotto:
    '''双色球'''
    def __init__(self, id=None):
        self.userId = id
        self.connection = sqlite3.connect(r'C:\Users\Administrator\Desktop\Launcher_ALL_Requirements\Manyana\data\Database\test.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS Winning (期 INT PRIMARY KEY, red_balls TEXT, blue_ball TEXT)')
        self.cursor.execute('CREATE TABLE IF NOT EXISTS user_union_lotto (userId VARCHAR(255) PRIMARY KEY, red_balls TEXT, blue_ball TEXT, state bit)')
        self.cursor.execute('CREATE TABLE IF NOT EXISTS temporary_user_union_lotto (userId VARCHAR(255) PRIMARY KEY, red_balls TEXT, blue_ball TEXT, grade INT, prize TEXT, amount INT)')
        self.cursor.execute('CREATE TABLE IF NOT EXISTS union_lotto_switch (groupId VARCHAR(255) PRIMARY KEY, state bit)')
        self.cursor.execute('CREATE TABLE IF NOT EXISTS Jackpot (name VARCHAR(255) PRIMARY KEY, bonus INT)')

    def close(self):
        self.cursor.close()
        self.connection.close()

    def initialization_union_lotto_Winning_results(self, 期, red_balls, blue_ball):
        '''写入开奖双色球'''
        self.cursor.execute('INSERT INTO Winning (期, red_balls, blue_ball) VALUES (?, ?, ?)', (期, red_balls, blue_ball))
        self.connection.commit()

    def union_lotto_Winning_results(self):
        '''双色球开奖结果'''
        result = self.cursor.execute('SELECT * FROM Winning WHERE 期 = (SELECT MAX(期) FROM Winning)').fetchall()
        if not result:
            self.initialization_union_lotto_Winning_results(0, '[]', 0)
            result = self.cursor.execute('SELECT * FROM Winning WHERE 期 = (SELECT MAX(期) FROM Winning)').fetchall()
        return result[0]

    def get_user_union_lotto(self):
        '''获取用户双色球'''
        if self.userId is None: return
        result = self.cursor.execute('SELECT * FROM user_union_lotto WHERE userId = ?', (self.userId,)).fetchall()
        if not result:
            self.initialization_user_union_lotto()
            result = self.cursor.execute('SELECT * FROM user_union_lotto WHERE userId = ?', (self.userId,)).fetchall()
        return result[0]

    def get_all_user_union_lotto(self, state=True):
        '''获取所有用户双色球\n默认获取所有已购买用户'''
        result = self.cursor.execute('SELECT * FROM user_union_lotto WHERE state = ?', (state,)).fetchall()
        return result

    def initialization_user_union_lotto(self):
        '''初始化用户双色球'''
        if self.userId is None: return
        t = datetime.now()
        self.cursor.execute('INSERT INTO user_union_lotto (userId, red_balls, blue_ball, state) VALUES (?, ?, ?, ?)', (self.userId, '[]', 0, False))
        self.connection.commit()

    def update_user_union_lotto(self, red_balls, blue_ball, state):
        '''更新用户彩票'''
        if self.userId is None: return
        self.cursor.execute('UPDATE user_union_lotto SET red_balls = ?, blue_ball = ?, state = ? WHERE userId = ?', (str(red_balls), blue_ball, state, self.userId))
        self.connection.commit()

    def delete_user_union_lotto(self, uid):
        '''删除用户彩票'''
        self.cursor.execute('DELETE FROM user_union_lotto WHERE userId = ?', (uid,))
        self.connection.commit()

    def get_groupId_union_lotto(self, state=True):
        '''获取群聊双色球开关'''
        result = self.cursor.execute('SELECT * FROM union_lotto_switch WHERE state = ?', (state,)).fetchall()
        if not result:
            self.initialization_groupId_union_lotto()
            result = self.cursor.execute('SELECT * FROM union_lotto_switch WHERE state = ?', (state,)).fetchall()
        return result

    def initialization_groupId_union_lotto(self):
        '''初始化用户双色球'''
        if self.userId is None: return
        t = datetime.now()
        self.cursor.execute('INSERT INTO union_lotto_switch (groupId, state) VALUES (?, ?)', (0, False))
        self.connection.commit()

    def temporary_user_union_lotto(self, userId, red_balls, blue_ball, grade, prize, amount):
        '''写入用户临时双色球开奖结果'''
        self.cursor.execute('INSERT INTO temporary_user_union_lotto (userId, red_balls, blue_ball, grade, prize, amount) VALUES (?, ?, ?, ?, ?, ?)', (userId, red_balls, blue_ball, grade, prize, amount))
        self.connection.commit()

    def get_temporary_user_union_lotto(self):
        '''获取临时双色球开奖结果'''
        result = self.cursor.execute('SELECT * FROM temporary_user_union_lotto').fetchall()
        if not result: return None
        return result

    def delete_temporary_user_union_lotto(self):
        '''删除临时彩票'''
        self.cursor.execute('DELETE FROM temporary_user_union_lotto')
        self.connection.commit()

    def update_Jackpot(self, bonus):
        '''更新奖池'''
        self.cursor.execute('UPDATE Jackpot SET bonus = ? WHERE name = "奖池"', (bonus,))
        self.connection.commit()

    def get_Jackpot(self):
        '''获取奖池'''
        result = self.cursor.execute('SELECT * FROM Jackpot WHERE name = "奖池"').fetchall()
        if not result:
            self.cursor.execute('INSERT INTO Jackpot (bonus, name) VALUES (0, "奖池")')
            return None
        return result[0][1]