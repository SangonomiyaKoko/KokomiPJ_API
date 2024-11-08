from typing import Any, Optional

class JSONResponse:
    '''接口返回值
    
    对于code是1000 2000~2003 3000 4000 5000的返回值，请使用内置函数获取response

    对于返回值的描述，请查看设计文档
    '''
    API_1000_Success = {'status': 'ok','code': 1000,'message': 'Success','data': None}
    API_2000_NetworkError = {'status': 'ok','code': 2000,'message': 'NetworkError','data': None}
    API_3000_DatabaseError = {'status': 'ok','code': 3000,'message': 'DatabaseError','data': None}
    API_4000_RedisError = {'status': 'ok','code': 4000,'message': 'RedisError','data': None}
    API_5000_ProgramError = {'status': 'ok','code': 5000,'message': 'ProgramError','data': None}
    API_6000_VersionError = {'status': 'ok','code': 6000,'message': 'VersionError','data': None}

    API_1001_UserNotExist = {'status': 'ok','code': 1001,'message': 'UserNotExist','data' : None}
    API_1002_ClanNotExist = {'status': 'ok','code': 1002,'message': 'ClanNotExist','data' : None}
    API_1003_IllegalAccoutIDorRegionID = {'status': 'ok','code': 1003,'message': 'IllegalAccoutIDorRegionID','data' : None}
    API_1004_IllegalClanIDorRegionID = {'status': 'ok','code': 1004,'message': 'IllegalClanIDorRegionID','data' : None}
    API_1005_UserHiddenProfite = {'status': 'ok','code': 1005,'message': 'UserHiddenProfite','data' : None}
    API_1006_UserDataisNone = {'status': 'ok','code': 1006,'message': 'UserDataisNone','data' : None}
    API_1007_CLanDataisNone = {'status': 'ok','code': 1007,'message': 'CLanDataisNone','data' : None}
    API_1008_UserNotExistinDatabase = {'status': 'ok','code': 1008,'message': 'UserNotExistinDatabase','data' : None}
    API_1009_ClanNotExistinDatabase = {'status': 'ok','code': 1009,'message': 'ClanNotExistinDatabase','data' : None}
    API_1010_IllegalRegion = {'status': 'ok','code': 1010,'message': 'IllegalRegion','data' : None}
    API_1011_IllegalUserName = {'status': 'ok','code': 1011,'message': 'IllegalUserName','data' : None}
    API_1012_IllegalClanTag = {'status': 'ok','code': 1012,'message': 'IllegalClanTag','data' : None}
    API_1013_ACisInvalid = {'status': 'ok','code': 1013,'message': 'ACisInvalid','data' : None}

    @staticmethod
    def get_success_response(
        data: Optional[Any] = None
    ) -> dict:
        "成功的返回值"
        return {
            'status': 'ok',
            'code': 1000,
            'message': 'Success',
            'data': data
        }
    
    @staticmethod
    def get_error_response(
        code: str,
        message: str,
        error_id: str
    ) -> dict:
        "失败的返回值"
        return {
            'status': 'error',
            'code': code,
            'message': message,
            'data': {
                'error_id': error_id
            }
        }