from typing import Optional

from fastapi import APIRouter

from .schemas import RegionList, LanguageList
from app.utils import UtilityFunctions
from app.response import JSONResponse, ResponseDict
from app.apis.robot import wws_me, wws_me_clan
from app.middlewares import record_api_call

router = APIRouter()

@router.get("/user-basic/")
async def getUserBasic(
    region: RegionList,
    account_id: int,
    language: LanguageList
) -> ResponseDict:
    """用户基础数据

    -

    参数:
    - None

    返回:
    - ResponseDict
    """
    region_id = UtilityFunctions.get_region_id(region)
    if not region_id:
        return JSONResponse.API_1010_IllegalRegion
    if UtilityFunctions.check_aid_and_rid(account_id, region_id) == False:
        return JSONResponse.API_1003_IllegalAccoutIDorRegionID
    result = await wws_me.main(account_id,region_id,language,'pr')
    await record_api_call(result['status'])
    return result

@router.get("/clan-basic/")
async def getClanBasic(
    region: RegionList,
    clan_id: int,
    language: LanguageList
) -> ResponseDict:
    """工会基础数据

    -

    参数:
    - None

    返回:
    - ResponseDict
    """
    region_id = UtilityFunctions.get_region_id(region)
    if not region_id:
        return JSONResponse.API_1010_IllegalRegion
    if UtilityFunctions.check_cid_and_rid(clan_id,region_id) == False:
        return JSONResponse.API_1003_IllegalAccoutIDorRegionID
    result = await wws_me_clan.main(clan_id,region_id,language,'pr')
    await record_api_call(result['status'])
    return result