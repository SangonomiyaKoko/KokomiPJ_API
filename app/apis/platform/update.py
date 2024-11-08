import gc
import uuid
import traceback

from app.log import write_error_info
from app.network import OtherAPI
from app.response import JSONResponse
from app.json import JsonData

class Update:
    async def update_ship_name(region_id: int):
        "更新ship_name.json文件的数据"
        try:
            if region_id == 4:
                server = 'lesta'
            else:
                server = 'wg'
            # 加载旧数据
            ship_name_data = JsonData.read_json_data(f'ship_name_{server}')
            # 获取当前最新的数据
            ship_name_result = await OtherAPI.get_ship_name_data(region_id)
            if ship_name_result['code'] != 1000:
                return ship_name_result
            # 记录本次更新的变化
            result = {'add':{},'del':{}}
            # 去除已经删除的船只
            for ship_id, ship_data in ship_name_data.items():
                if ship_id not in ship_name_result['data']:
                    result['del'][ship_id] = ship_data
                else:
                    pass
            for ship_id, _ in result['del'].items():
                del ship_name_data[ship_id]
            # 加入新增的船只
            for ship_id, ship_data in ship_name_result['data'].items():
                if ship_id not in ship_name_data:
                    if server == 'wg':
                        tier = ship_data['level']
                        type = ship_data['tags'][0]
                        nation = ship_data['nation']
                        name = ship_data['name'].split('_')[0]

                        name_cn = ship_data['localization']['shortmark']['zh_sg']
                        name_en = ship_data['localization']['shortmark']['en']
                        name_jp = ship_data['localization']['shortmark']['ja']
                        name_ru = ship_data['localization']['shortmark']['ru']
                        name_en_l = ship_data['localization']['mark']['en']
                        if '[' in name_en and ']' in name_en:
                            continue
                        premium = False
                        special = False
                        if 'uiPremium' in ship_data['tags']:
                            premium = True
                        if 'uiSpecial' in ship_data['tags']:
                            special = True
                        data = {
                            'tier': tier,
                            'type': type,
                            'nation': nation,
                            'premium': premium,
                            'special': special,
                            'index': name,
                            'ship_name': {
                                'cn': name_cn,
                                'en': name_en,
                                'en_l': name_en_l,
                                'ja': name_jp,
                                'ru': name_ru
                            }
                        }
                        ship_name_data[ship_id] = data
                        result['add'][ship_id] = data
                    else:
                        tier = ship_data['level']
                        type = ship_data['tags'][0]
                        nation = ship_data['nation']
                        name = ship_data['name'].split('_')[0]
                        name_ru = ship_data['localization']['shortmark']['ru']
                        if '[' in name_ru and ']' in name_ru:
                            continue
                        premium = False
                        special = False
                        if 'uiPremium' in ship_data['tags']:
                            premium = True
                        if 'uiSpecial' in ship_data['tags']:
                            special = True
                        data = {
                            'tier': tier,
                            'type': type,
                            'nation': nation,
                            'premium': premium,
                            'special': special,
                            'index': name,
                            'ship_name': {
                                'cn': name_ru,
                                'en': name_ru,
                                'en_l': name_ru,
                                'ja': name_ru,
                                'ru': name_ru
                            }
                        }
                        ship_name_data[ship_id] = data
                        result['add'][ship_id] = data
            # 更新json文件
            JsonData.write_json_data(f'ship_name_{server}', ship_name_data)
            # 返回数据
            return JSONResponse.get_success_response(result)
        except Exception as e:
            error_id = str(uuid.uuid4())
            write_error_info(
                error_id = error_id,
                error_type = 'Program',
                error_name = str(type(e).__name__),
                error_file = __file__,
                error_info = f'\n{traceback.format_exc()}'
            )
            return JSONResponse.get_error_response(5000,'ProgramError',error_id)
        finally:
            gc.collect()