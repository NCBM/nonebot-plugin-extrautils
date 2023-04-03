import abc
from typing import Any, Dict, Generic, Optional, Type, TypeVar, Union
from nonebot.adapters import Bot, Adapter, Event, Message, MessageSegment

Bot_T = TypeVar("Bot_T", bound=Bot)


class BaseBotCombination(Bot, Generic[Bot_T], abc.ABC):
    def __init__(self, adapter: Type[Adapter], *bots: Bot_T):
        if _badbot := self._validate(adapter, *bots):
            raise ValueError(f"{_badbot} does not belong to {adapter}")
        self.bots = bots
        self.adapter: Adapter = bots[0].adapter
        """协议适配器实例"""

    @property
    def self_id(self) -> str:
        return "botcombination__" + "~".join(_b.self_id for _b in self.bots)

    def _validate(self, adapter: Type[Adapter], *bots: Bot_T) -> Optional[Bot_T]:
        for _bot in bots:
            if not isinstance(_bot.adapter, adapter):
                return _bot

    @abc.abstractmethod
    def find_bot(self, user_id: Optional[int] = None, group_id: Optional[int] = None) -> Bot_T:
        raise NotImplementedError

    @staticmethod
    def _get_finder_args(data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "user_id": data.get("user_id", None),
            "group_id": data.get("group_id", None)
        }

    async def call_api(self, api: str, **data: Any) -> Any:
        bot = self.find_bot(**self._get_finder_args(data))
        # bot._calling_api_hook = self._calling_api_hook
        # bot._called_api_hook = self._called_api_hook
        return await bot.call_api(api, **data)

    async def send(
        self, event: Event, message: Union[str, Message, MessageSegment], **kwargs: Any
    ) -> Any:
        bot = self.find_bot(**self._get_finder_args(event.dict()))
        return await bot.send(event, message, **kwargs)