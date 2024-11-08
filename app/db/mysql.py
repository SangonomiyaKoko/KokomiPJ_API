from typing import Optional

import aiomysql
from aiomysql.pool import Pool
from aiomysql.connection import Connection
from aiomysql.cursors import Cursor

from app.core import EnvConfig
from app.core import api_logger
# from app.db import MySQLConnectionPool


class MysqlConnection:
    '''管理MySQL连接'''
    __pool: Optional[Pool] = None
    
    async def __init_connection(self) -> None:
        "初始化MySQL连接"
        try:
            config = EnvConfig.get_config()
            self.__pool = await aiomysql.create_pool(
                host=config.MYSQL_HOST, 
                port=config.MYSQL_PORT, 
                user=config.MYSQL_USERNAME, 
                password=config.MYSQL_PASSWORD, 
                db='kokomi',
                pool_recycle=3600
            )
            api_logger.info('MySQL connection initialization is complete')
        except Exception as e:
            api_logger.error(f'Failed to initialize the MySQL connection')
            api_logger.error(e)

    @classmethod
    async def test_mysql(self) -> None:
        "测试MySQL连接"
        try:
            if self.__pool:
                pass
            else:
                await self.__init_connection(self)
            mysql_pool = self.__pool
            query = """
                SELECT COUNT(*)
                FROM information_schema.tables
                WHERE table_schema = %s
            """
            async with mysql_pool.acquire() as conn:
                conn: Connection
                async with conn.cursor() as cur:
                    cur: Cursor
                    await cur.execute(query, ('kokomi',))
                    result = await cur.fetchone()
                    if result != None:
                        api_logger.info('The MySQL connection was successfully tested')
                    else:
                        api_logger.warning('Failed to test the MySQL connection')
        except Exception as e:
            api_logger.warning(f'Failed to test the MySQL connection')
            api_logger.error(e)

    @classmethod
    async def get_connection(self):
        "获取一条连接，记得使用完要使用release释放"
        if not self.__pool:
            await self.__init_connection(self)
        return await self.__pool.acquire()

    @classmethod
    async def release_connection(self, conn):
        "释放连接"
        if self.__pool:
            await self.__pool.release(conn)

    @classmethod
    async def close_mysql(self) -> None:
        "关闭MySQL连接"
        try:
            if self.__pool:
                self.__pool.close()
                await self.__pool.wait_closed()
                api_logger.info('The MySQL connection is closed')
            else:
                api_logger.warning('The MySQL connection is empty and cannot be closed')
        except Exception as e:
            api_logger.error(f'Failed to close the MySQL connection')
            api_logger.error(e)
        
        
