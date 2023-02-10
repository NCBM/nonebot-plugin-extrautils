from typing import Any, Optional, Union
import httpx
from nonebot.adapters.onebot.v11 import (
    Bot, Message, MessageEvent, MessageSegment
)

from nonebot.adapters.onebot.v11 import (
    GroupMessageEvent, GroupUploadNoticeEvent,
    GroupAdminNoticeEvent, GroupDecreaseNoticeEvent,
    GroupIncreaseNoticeEvent, GroupBanNoticeEvent,
    GroupRecallNoticeEvent, GroupRequestEvent, NotifyEvent,
    FriendAddNoticeEvent, FriendRecallNoticeEvent,
    FriendRequestEvent
)

_GroupEvent = Union[
    GroupMessageEvent, GroupUploadNoticeEvent,
    GroupAdminNoticeEvent, GroupDecreaseNoticeEvent,
    GroupIncreaseNoticeEvent, GroupBanNoticeEvent,
    GroupRecallNoticeEvent, GroupRequestEvent, NotifyEvent
]

_UserEvent = Union[
    MessageEvent, _GroupEvent, FriendAddNoticeEvent,
    FriendRecallNoticeEvent, FriendRequestEvent
]

AVATAR_SIZE_SMALL = 40
AVATAR_SIZE_MEDIUM = 100
AVATAR_SIZE_BIG = 640


def get_avatar_url(uid: Union[int, str], size: int = AVATAR_SIZE_BIG) -> str:
    """
    获取指定 QQ 用户头像 URL

    参数：
    - uid: 用户 QQ 号
    - size: 头像尺寸
      - 建议值: `AVATAR_SIZE_SMALL`, `AVATAR_SIZE_MEDIUM`, `AVATAR_SIZE_BIG`
    
    返回值: 图像 URL
    """
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
    """
    下载指定 QQ 用户头像

    参数：
    - uid: 用户 QQ 号
    - size: 头像尺寸
      - 建议值: `AVATAR_SIZE_SMALL`, `AVATAR_SIZE_MEDIUM`, `AVATAR_SIZE_BIG`

    返回值: 图像字节数据
    """
    async with httpx.AsyncClient(follow_redirects=True) as cli:
        res = await cli.get(get_avatar_url(uid, size))
        res.raise_for_status()
        return res.content
    

async def _get_user_name_bare(
    *, bot: Bot, uid: int, no_cache: bool = False
) -> str:
    """
    获取指定 QQ 用户昵称

    参数：
    - bot: OneBot v11 Bot 实例
    - uid: 用户 ID （QQ 号）
    - no_cache: 是否不使用缓存

    返回值: 昵称字符串
    """
    return str(
        (await bot.get_stranger_info(user_id=uid, no_cache=no_cache))
        ["nickname"]
    )


async def _get_user_name_group(
    *, bot: Bot, gid: int, uid: int, no_cache: bool = False
) -> str:
    """
    获取指定 QQ 用户群昵称

    参数：
    - bot: OneBot v11 Bot 实例
    - gid: 群 ID （群号）
    - uid: 用户 ID （QQ 号）
    - no_cache: 是否不使用缓存

    返回值: 群名片/昵称字符串
    """
    info = await bot.get_group_member_info(
        group_id=gid, user_id=uid, no_cache=no_cache
    )
    return str(info["card"] or info["nickname"])


async def get_user_name_bare(
    *, bot: Bot, event: _UserEvent, no_cache: bool = False
) -> str:
    """
    获取指定 QQ 用户昵称

    参数：
    - bot: OneBot v11 Bot 实例
    - event: 可提取用户 ID 的 OneBot v11 事件
    - no_cache: 是否不使用缓存

    返回值: 昵称字符串
    """
    return await _get_user_name_bare(
        bot=bot, uid=event.user_id, no_cache=no_cache
    )


async def get_user_name_group(
    *, bot: Bot, event: _GroupEvent, no_cache: bool = False
) -> str:
    """
    获取指定 QQ 用户群昵称

    参数：
    - bot: OneBot v11 Bot 实例
    - event: 可提取用户 ID 和群 ID 的 OneBot v11 事件
    - no_cache: 是否不使用缓存

    返回值: 群名片/昵称字符串
    """
    return await _get_user_name_group(
        bot=bot, gid=event.group_id, uid=event.user_id, no_cache=no_cache
    )


async def get_user_name(
    *, bot: Bot, event: _UserEvent, no_cache: bool = False
):
    """
    获取指定 QQ 用户所在会话的昵称

    参数：
    - bot: OneBot v11 Bot 实例
    - event: 可提取用户 ID 的 OneBot v11 事件
    - no_cache: 是否不使用缓存

    返回值: 群名片/昵称字符串
    """
    if not hasattr(event, "user_id"):
        raise AttributeError(
            f"event {event!r} does not include attrinute 'user_id'"
        )
    if (gid := getattr(event, "group_id", None)) is not None:
        return await _get_user_name_group(
            bot=bot, gid=gid, uid=event.user_id, no_cache=no_cache
        )
    return await get_user_name_bare(
        bot=bot, event=event, no_cache=no_cache
    )


__all__ = (
    "AVATAR_SIZE_SMALL", "AVATAR_SIZE_MEDIUM", "AVATAR_SIZE_BIG",
    "get_avatar_url", "get_avatar_bytes",
    "_get_user_name_bare", "_get_user_name_group",
    "get_user_name_bare", "get_user_name_group", "get_user_name"
)