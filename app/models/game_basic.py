from aiomysql.connection import Connection
from aiomysql.cursors import Cursor

from app.db import MysqlConnection
from app.log import ExceptionLogger
from app.response import JSONResponse, ResponseDict

class GameModel:
    @ExceptionLogger.handle_database_exception_async
    async def get_game_version(region_id: int) -> ResponseDict:
        '''获取数据库中存储的游戏版本

        方法描述

        参数:
            params
        
        返回:
            ResponseDict
        '''
        try:
            conn: Connection = await MysqlConnection.get_connection()
            await conn.begin()
            cur: Cursor = await conn.cursor()

            data = {
                'version': None
            }
            await cur.execute(
                "SELECT game_version FROM kokomi.region_version WHERE region_id = %s;",
                [region_id]
            )
            game = await cur.fetchone()
            if game == None:
                raise ValueError('Table Not Found')
            else:
                data['version'] = game[0]

            await conn.commit()
            return JSONResponse.get_success_response(data)
        except Exception as e:
            await conn.rollback()
            raise e
        finally:
            await cur.close()
            await MysqlConnection.release_connection(conn)