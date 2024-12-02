from app.log import ExceptionLogger
from app.network import DetailsAPI
from app.response import JSONResponse
from app.models import UserAccessToken, UserAccessToken2

from ..user_basic import get_user_name_and_clan
from ..processors.basic import (
    process_signature_data,
    process_lifetime_data
)

@ExceptionLogger.handle_program_exception_async
async def wws_user_basic(
    account_id: int, 
    region_id: int, 
    game_type: str,
    language: str,
    algo_type: str
):
    '''用于`wws me`功能的接口

    返回用户基本数据
    
    参数:
        account_id 用户id
        region_id 服务器id
        game_type 数据类型
        algo_type 算法类型

    返回:
        ResponseDict
    '''
    try:
        # 返回数据的格式
        data = {
            'user': {},
            'clan': {},
            'statistics': {}
        }
        # 获取用户相关的access token
        ac_value = UserAccessToken.get_ac_value_by_id(account_id, region_id)
        ac2_value = UserAccessToken2.get_ac_value_by_id(account_id, region_id)
        # 获取用户user和clan数据
        user_and_clan_result = await get_user_name_and_clan(
            account_id=account_id,
            region_id=region_id,
            ac_value=ac_value
        )
        if user_and_clan_result['code'] != 1000:
            return user_and_clan_result
        else:
            data['user'] = user_and_clan_result['data']['user']
            data['clan'] = user_and_clan_result['data']['clan']
        # 获取需要请求的数据和处理数据函数的引用
        game_type_dict = {
            'signature': {
                'type_list': ['pvp'],
                'func_reference': process_signature_data
            },
            'lifetime': {
                'type_list': ['pvp','lifetime'],
                'func_reference': process_lifetime_data
            },
            'overall': {
                'type_list': ['pvp_solo','pvp_div2','pvp_div3','rank_solo'],
                'func_reference': None
            },
            'random': {
                'type_list': ['pvp_solo','pvp_div2','pvp_div3'],
                'func_reference': None
            },
            'pvp_solo': {
                'type_list': ['pvp_solo'],
                'func_reference': None
            },
            'pvp_div2': {
                'type_list': ['pvp_div2'],
                'func_reference': None
            },
            'pvp_div3': {
                'type_list': ['pvp_div3'],
                'func_reference': None
            },
            'ranked': {
                'type_list': ['rank_solo'],
                'func_reference': None
            },
            'operation': {
                'type_list': ['oper'],
                'func_reference': None
            },
            'clan_battle': {
                'type_list': ['clan','achievement'],
                'func_reference': None
            }
        }
        game_type_data = game_type_dict.get(game_type)
        # 请求数据
        details_data = await DetailsAPI.get_user_detail(
            account_id=account_id,
            region_id=region_id,
            type_list=game_type_data.get('type_list'),
            ac_value=ac_value,
            ac2_value=ac2_value
        )
        for response in details_data:
            if response['code'] != 1000:
                return response
        # 处理数据
        handle_api_data_func: function = game_type_data.get('func_reference')
        if not handle_api_data_func:
            raise NotImplementedError
        processed_data = handle_api_data_func(
            account_id = account_id, 
            region_id = region_id, 
            responses = details_data,
            language = language,
            algo_type = algo_type
        )
        if processed_data.get('code', None) != 1000:
            return processed_data
        data['statistics'] = processed_data['data']
        # 返回结果
        return JSONResponse.get_success_response(data)
    except Exception as e:
        raise e