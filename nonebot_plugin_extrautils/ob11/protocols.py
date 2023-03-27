from typing import Protocol, runtime_checkable
from nonebot.adapters import Message, MessageSegment


@runtime_checkable
class HasSelfID(Protocol):
    self_id: int


@runtime_checkable
class HasUserID(HasSelfID, Protocol):
    user_id: int


@runtime_checkable
class HasGroupID(HasUserID, Protocol):
    group_id: int


@runtime_checkable
class HasMessage(HasUserID, Protocol):
    message: Message[MessageSegment]


# Keep these below for compatibility
_BaseEvent, _UserEvent, _GroupEvent = HasSelfID, HasUserID, HasGroupID

__all__ = (
    "HasSelfID", "HasUserID", "HasGroupID", "HasMessage",
    "_BaseEvent", "_UserEvent", "_GroupEvent"
)