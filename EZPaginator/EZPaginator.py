import asyncio
from enum import Enum, auto
from abc import ABC, abstractmethod

from discord import (
    Embed,
    Emoji,
    Interaction,
    InteractionMessage,
    Message,
    RawReactionActionEvent,
)
from discord.ext.commands import Context

from EZPaginator.exceptions import InvaildArgumentException


class ContextType(Enum):
    CTX = auto()
    INTERACTION = auto()


class PaginatorMode(Enum):
    EMBED = auto()
    CONTENT = auto()


class PaginatorABC(ABC):
    @abstractmethod
    async def start(self) -> None:
        pass

    @abstractmethod
    async def stop(self) -> None:
        pass


class Paginator(PaginatorABC):
    def __init__(
        self,
        context: Context | Interaction,
        timeout: int = 30,
        embeds: list[Embed] = [],
        contents: list[str] = [],
        start_index: int = 0,
        auto_clear_emoji: bool = True,
        auto_delete_message: bool = False,
        use_extend: bool = False,
        emojis: list[str | Emoji] = ["⬅️", "➡️"],
        extended_emojis: list[str | Emoji] = ["⏪", "⬅️", "➡️", "⏩"],
        only: list[int] = [],
    ) -> None:
        self.context = context
        self.timeout = timeout
        self.index = start_index
        self.auto_clear_emoji = auto_clear_emoji
        self.auto_delete_message = auto_delete_message

        self.embeds = embeds
        self.contents = contents

        self.use_extend = use_extend
        self.emojis = emojis
        self.extended_emojis = extended_emojis

        self.only = only

        if isinstance(context, Context):
            self.context_mode = ContextType.CTX
        elif isinstance(context, Interaction):
            self.context_mode = ContextType.INTERACTION
        else:
            raise TypeError("context must be Context or Interaction!")

        if embeds:
            self.paginator_mode = PaginatorMode.EMBED
        elif contents:
            self.paginator_mode = PaginatorMode.CONTENT
        else:
            raise InvaildArgumentException("embeds or contents must be not empty!")

        self.__message: Message | InteractionMessage | None = None

    def _emoji_check(self, payload: RawReactionActionEvent) -> bool:
        context = self.context
        bot = (
            context.bot
            if isinstance(context, Context)
            else context._state._get_client()
        )
        if not bot.user:
            return False

        if not self.__message:
            return False

        if payload.user_id == bot.user.id:
            return False

        if payload.message_id != self.__message.id:
            return False

        if self.only:
            if payload.user_id not in self.only:
                return False

        if self.use_extend:
            if str(payload.emoji) not in self.extended_emojis:
                return False
        else:
            if str(payload.emoji) not in self.emojis:
                return False

        return True

    async def _ctx_start(self) -> Message:
        ctx = self.context
        assert isinstance(ctx, Context)

        if self.paginator_mode == PaginatorMode.EMBED:
            msg = await ctx.send(embed=self.embeds[self.index])
        else:
            msg = await ctx.send(self.contents[self.index])

        return msg

    async def _interaction_start(self) -> InteractionMessage:
        interaction = self.context
        assert isinstance(interaction, Interaction)

        if self.paginator_mode == PaginatorMode.EMBED:
            await interaction.response.send_message(embed=self.embeds[self.index])

        else:
            await interaction.response.send_message(self.contents[self.index])

        original_message = await interaction.original_message()

        return original_message

    async def _go_first(self) -> None:
        self.index = 0

    async def _go_previous(self) -> None:
        if self.index == 0:
            return

        self.index -= 1

    async def _go_next(self) -> None:
        if self.paginator_mode == PaginatorMode.EMBED:
            if self.index == len(self.embeds) - 1:
                return
        else:
            if self.index == len(self.contents) - 1:
                return

        self.index += 1

    async def _go_last(self) -> None:
        self.index = len(self.embeds) - 1

    async def _handle_pagination(self, emoji: str) -> None:
        assert self.__message

        if self.use_extend:
            if emoji == self.extended_emojis[0]:
                await self._go_first()
            elif emoji == self.extended_emojis[1]:
                await self._go_previous()
            elif emoji == self.extended_emojis[2]:
                await self._go_next()
            elif emoji == self.extended_emojis[3]:
                await self._go_last()

        else:
            if emoji == self.emojis[0]:
                await self._go_previous()
            elif emoji == self.emojis[1]:
                await self._go_next()

        if self.paginator_mode == PaginatorMode.EMBED:
            await self.__message.edit(embed=self.embeds[self.index])
        else:
            await self.__message.edit(content=self.contents[self.index])

    async def start(self) -> None:
        context = self.context
        if self.context_mode == ContextType.CTX:
            msg = await self._ctx_start()
        else:
            msg = await self._interaction_start()

        self.__message = msg

        if self.use_extend:
            for i in self.extended_emojis:
                await msg.add_reaction(i)
        else:
            for i in self.emojis:
                await msg.add_reaction(i)

        bot = (
            context.bot
            if isinstance(context, Context)
            else context._state._get_client()
        )

        while True:

            add_reaction_event = asyncio.create_task(
                bot.wait_for(
                    "raw_reaction_add", timeout=self.timeout, check=self._emoji_check
                )
            )
            remove_reaction_event = asyncio.create_task(
                bot.wait_for(
                    "raw_reaction_remove", timeout=self.timeout, check=self._emoji_check
                )
            )
            try:
                done, pending = await asyncio.wait(
                    (add_reaction_event, remove_reaction_event),
                    return_when=asyncio.FIRST_COMPLETED,
                    timeout=self.timeout,
                )

                for i in pending:
                    i.cancel()

                if len(done) == 0:
                    raise asyncio.TimeoutError

                payload = done.pop().result()
                await self._handle_pagination(str(payload.emoji))
            except asyncio.TimeoutError:
                await self.stop()
                break

    async def stop(self) -> None:
        assert self.__message

        if self.auto_delete_message:
            await self.__message.delete()
            return

        if self.auto_clear_emoji:
            await self.__message.clear_reactions()
            return
