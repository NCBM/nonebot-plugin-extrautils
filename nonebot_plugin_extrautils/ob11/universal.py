from typing import Any, Optional, Union
import httpx
from nonebot.adapters.onebot.v11 import (
    Bot as _OneBotV11Bot,
    Message as _OneBotV11Message,
    MessageEvent as _OneBotV11MessageEvent,
    MessageSegment as _OneBotV11MessageSegment
)

from nonebot.adapters.onebot.v11 import (
    GroupMessageEvent, GroupUploadNoticeEvent,
    GroupAdminNoticeEvent, GroupDecreaseNoticeEvent,
    GroupIncreaseNoticeEvent, GroupBanNoticeEvent,
    GroupRecallNoticeEvent, GroupRequestEvent, NotifyEvent
)

_GroupEvent = Union[
    GroupMessageEvent, GroupUploadNoticeEvent,
    GroupAdminNoticeEvent, GroupDecreaseNoticeEvent,
    GroupIncreaseNoticeEvent, GroupBanNoticeEvent,
    GroupRecallNoticeEvent, GroupRequestEvent, NotifyEvent
]

AVATAR_SIZE_SMALL = 40
AVATAR_SIZE_MEDIUM = 100
AVATAR_SIZE_BIG = 640


def get_avatar_url(uid: Union[int, str], size: int = AVATAR_SIZE_BIG) -> str:
    if size not in (AVATAR_SIZE_SMALL, AVATAR_SIZE_MEDIUM, AVATAR_SIZE_BIG):
        raise ValueError(
            f"unsupported avatar size: {size}\n\n"
            "You should use pre-defined constants starts with 'AVATAR_SIZE_'."
        )
    if (isinstance(uid, str) and not uid.isdigit()) or \
            (isinstance(uid, int) and uid < 10000):
        raise ValueError(f"invalid uid: {uid}")
    return f"https://q1.qlogo.cn/g?b=qq&nk={uid}&s={size}"


async def get_avatar_bytes(
    uid: Union[int, str], size: int = AVATAR_SIZE_BIG
) -> bytes:
    async with httpx.AsyncClient(follow_redirects=True) as cli:
        res = await cli.get(get_avatar_url(uid, size))
        res.raise_for_status()
        return res.content
    

async def _get_user_name_bare(
    *, bot: _OneBotV11Bot, uid: int, no_cache: bool = False
) -> str:
    return str(
        (await bot.get_stranger_info(user_id=uid, no_cache=no_cache))
        ["nickname"]
    )


async def _get_user_name_group(
    *, bot: _OneBotV11Bot, gid: int, uid: int, no_cache: bool = False
) -> str:
    info = await bot.get_group_member_info(
        group_id=gid, user_id=uid, no_cache=no_cache
    )
    return str(info["card"] or info["nickname"])


async def get_user_name_bare(
    *, bot: _OneBotV11Bot, event: _OneBotV11MessageEvent,
    no_cache: bool = False
):
    return await _get_user_name_bare(
        bot=bot, uid=event.user_id, no_cache=no_cache
    )


async def get_user_name_group(
    *, bot: _OneBotV11Bot, event: _GroupEvent,
    no_cache: bool = False
):
    return await _get_user_name_group(
        bot=bot, gid=event.group_id, uid=event.user_id, no_cache=no_cache
    )