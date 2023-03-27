from typing import Any, Dict, Sequence, TypeAlias, Union
from .universal import *
from .protocols import *
from nonebot.adapters.onebot.v11 import Bot, Message, MessageSegment

ComplexMessage = Union[Message, Sequence[Dict[str, Any]]]
CQCode: TypeAlias = str
SimpleMessage = Union[ComplexMessage, CQCode]


def Node(uid: int, name: str, content: SimpleMessage) -> MessageSegment:
    """
    构造适用于 go-cqhttp 的简单自定义消息节点

    参数：
    - uid: 发送者用户 ID （QQ 号）
    - name: 发送者昵称
    - content: 消息内容

    返回值: 构造好的消息段

    更多信息参阅 https://docs.go-cqhttp.org/cqcode/#%E5%90%88%E5%B9%B6%E8%BD%AC%E5%8F%91%E6%B6%88%E6%81%AF%E8%8A%82%E7%82%B9
    """
    return MessageSegment(
        "node", {"uin": uid, "name": name, "content": content}
    )


async def msg2node_self(
    *msgs: SimpleMessage, bot: Bot, event: _BaseEvent
) -> Message:
    """
    转化多条消息到发送者为自身的消息节点

    参数：
    - *msgs: OneBot v11 消息对象
    - bot: OneBot v11 Bot 实例
    - event: OneBot v11 事件

    返回值: 构造好的消息节点序列
    """
    name = await get_self_name(bot=bot, event=event)
    uid = event.self_id
    return Message(Node(uid, name, m) for m in msgs)


def msg2node_custom(*msgs: SimpleMessage, uid: int, name: str) -> Message:
    """
    转化多条消息到发送者为指定用户的消息节点

    参数：
    - *msgs: OneBot v11 消息对象
    - uid: 发送者用户 ID （QQ 号）
    - name: 发送者昵称

    返回值: 构造好的消息节点序列
    """
    return Message(Node(uid, name, m) for m in msgs)


async def _send_forward_msg_custom(
    *, bot: Bot, type: str, dest_id: int, nodes: ComplexMessage
) -> Dict[str, Any]:
    """
    发送合并转发消息

    参数：
    - bot: OneBot v11 Bot 实例
    - type: 消息类型，可为 `"private"` 或 `"group"`
    - dest_id: 目标 ID
    - nodes: 消息节点序列

    返回值: 消息 ID 和转发 ID
    """
    if type == MSG_TYPE_PRIVATE:
        return await bot.send_private_forward_msg(
            user_id=dest_id, messages=nodes
        )
    elif type == MSG_TYPE_GROUP:
        return await bot.send_group_forward_msg(
            group_id=dest_id, messages=nodes
        )
    else:
        raise ValueError(
            f"type {type!r} is unknown\n\n"
            f"Only {MSG_TYPE_PRIVATE=} and {MSG_TYPE_GROUP=} are supported."
        )
    

async def send_forward_msg_custom(
    *, bot: Bot, event: _UserEvent, nodes: ComplexMessage
) -> Dict[str, Any]:
    """
    发送合并转发消息

    参数：
    - bot: OneBot v11 Bot 实例
    - event: 可提取用户 ID 的 OneBot v11 事件
    - nodes: 消息节点序列

    返回值: 消息 ID 和转发 ID
    """
    if not hasattr(event, "user_id"):
        raise AttributeError(
            f"event {event!r} does not include attrinute 'user_id'"
        )
    if (gid := getattr(event, "group_id", None)) is not None:
        return await _send_forward_msg_custom(
            bot=bot, type=MSG_TYPE_GROUP, dest_id=gid, nodes=nodes
        )
    return await _send_forward_msg_custom(
        bot=bot, type=MSG_TYPE_GROUP, dest_id=event.user_id, nodes=nodes
    )


async def send_forward_msg(
    *, bot: Bot, event: _UserEvent, msgs: Sequence[SimpleMessage]
) -> Dict[str, Any]:
    """
    发送合并转发消息

    参数：
    - bot: OneBot v11 Bot 实例
    - event: 可提取用户 ID 的 OneBot v11 事件
    - nodes: 消息序列

    返回值: 消息 ID 和转发 ID
    """
    return await send_forward_msg_custom(
        bot=bot, event=event,
        nodes=await msg2node_self(*msgs, bot=bot, event=event)
    )