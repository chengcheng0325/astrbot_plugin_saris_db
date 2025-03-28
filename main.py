from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api.all import *
from astrbot.api import logger
from .Database.Database_user import Database_user
from .Database.Database_economy import Database_economy
from .Database.Database_fish import Database_fish

from contextlib import contextmanager

import os

# 路径配置
PLUGIN_DIR = os.path.join('data', 'plugins', 'astrbot_plugin_saris_db')
RUNNING_SCRIPT_DIRECTORY = os.getcwd()
DATABASE_FILE = os.path.join(RUNNING_SCRIPT_DIRECTORY, os.path.join('data', 'Database'))

@contextmanager
def open_databases(config,database_file,uid):
    db_user = Database_user(config=config,DatabaseFile=database_file,Id=uid)
    db_economy = Database_economy(config=config,DatabaseFile=database_file,Id=uid)
    db_fish = Database_fish(config=config,DatabaseFile=database_file,Id=uid)
    try:
        yield db_user, db_economy, db_fish
    finally:
        db_user.close()
        db_economy.close()
        db_fish.close()


@register("Database", "城城", "-----", "0.2.1")
class DatabasePlugin(Star):
    def __init__(self, context: Context, config: dict):
        super().__init__(context)
        self.config = config

    @filter.on_astrbot_loaded()
    async def on_astrbot_loaded(self):
        os.makedirs(DATABASE_FILE, exist_ok=True)
        os.makedirs(PLUGIN_DIR, exist_ok=True)
        


    @event_message_type(EventMessageType.GROUP_MESSAGE, priority=999)
    async def on_group_message(self, event: AstrMessageEvent):
        """初始化用户信息"""
        UserId = event.message_obj.sender.user_id       #  获取消息的纯文本内容
        UserName = event.message_obj.sender.nickname    # 获取消息的发送者昵称
        with open_databases(self.config,DATABASE_FILE,UserId) as (db_user, db_economy, db_fish):
            """初始化"""
            # 用户表
            if db_user.query_user() == None:
                db_user.insert_user(UserName)
            # 签到表
            if db_user.query_sign_in() == None:
                db_user.insert_sign_in()
            # 钓鱼冷却表
            if db_user.query_fish_cooling() == None:
                db_user.insert_fish_cooling()

            # 经济表
            if db_economy.get_economy() == None:
                db_economy.insert_user()
            





















