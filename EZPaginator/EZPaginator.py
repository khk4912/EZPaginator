import asyncio
from abc import ABC, abstractmethod
from enum import Enum, auto

from discord import (
    Embed,
    Emoji,
    Interaction,
    InteractionMessage,
    Message,
    RawReactionActionEvent,
)
from discord.abc import User
from discord.ext.commands import Context

from .exceptions import InvaildArgumentException


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
        embeds: list[Embed] = [],
        contents: list[str] = [],
        timeout: int = 30,
        start_index: int = 0,
        auto_clear_emoji: bool = True,
        auto_delete_message: bool = False,
        use_extend: bool = False,
        emojis: list[str | Emoji] = ["⬅️", "➡️"],
        extended_emojis: list[str | Emoji] = ["⏪", "⬅️", "➡️", "⏩"],
        only: User | None = None,
        auto_fill_index: bool = False,
    ) -> None:
        """_summary_

        Parameters
        ----------
        context : Context | Interaction
            _description_
        timeout : int, optional
            Timeout of the paginator, by default 30
        embeds : list[Embed], optional
            _description_, by default []
        contents : list[str], optional
            _description_, by default []
        start_index : int, optional
            _description_, by default 0
        auto_clear_emoji : bool, optional
            Whether to clear the emoji when the pagination is stopped by function stop() or by timeout. by default True.
        auto_delete_message : bool, optional
            Whether to delete the message when the pagination is stopped by function stop() or by timeout. by default False.
        use_extend : bool, optional
            Whether to use the extended emoji set(First, Previous, Next, Last). by default False.
        emojis : list[str  |  Emoji], optional
            List of emojis to use for pagination. by default ["⬅️", "➡️"]
        extended_emojis : list[str  |  Emoji], optional
            List of extended emojis to use for pagination, by default ["⏪", "⬅️", "➡️", "⏩"]
        only : User | None, optional
            Restrain the pagination to only the specified user, by default None.
        auto_fill_index : bool, optional
            Enable auto-fill index mode, by default False.

        Raises
        ------
        InvaildArgumentException
            _description_
        InvaildArgumentException
            _description_
        """

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
        self.auto_fill_index = auto_fill_index

        if isinstance(context, Context):
            self.context_mode = ContextType.CTX
        elif isinstance(context, Interaction):
            self.context_mode = ContextType.INTERACTION
        else:
            raise InvaildArgumentException(
                "Parameter 'context' must be Context or Interaction!"
            )

        if embeds:
            self.paginator_mode = PaginatorMode.EMBED
        elif contents:
            self.paginator_mode = PaginatorMode.CONTENT
        else:
            raise InvaildArgumentException(
                "Parameter 'embeds' or 'contents' must not be empty!"
            )

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
            if payload.user_id != self.only.id:
                return False

        if self.use_extend:
            if str(payload.emoji) not in self.extended_emojis:
                return False
        else:
            if str(payload.emoji) not in self.emojis:
                return False

        return True

    def _embed_fill_index(self, content: str) -> str:
        return content.format(
            current_page=self.index + 1,
            total_pages=len(self.embeds),
        )

    def _embed_auto_index(self, embed: Embed) -> Embed:
        embed_dict = embed.to_dict()

        if "title" in embed_dict:
            embed_dict["title"] = self._embed_fill_index(embed_dict["title"])
        if "description" in embed_dict:
            embed_dict["description"] = self._embed_fill_index(
                embed_dict["description"]
            )

        if "fields" in embed_dict:
            for field in embed_dict["fields"]:
                field["name"] = self._embed_fill_index(field["name"])
                field["value"] = self._embed_fill_index(field["value"])

        if "footer" in embed_dict:
            if embed_dict["footer"]:
                if footer_text := embed_dict["footer"]["text"]:
                    embed_dict["footer"]["text"] = self._embed_fill_index(footer_text)

        return Embed.from_dict(embed_dict)

    def _content_auto_index(self, content: str) -> str:
        return content.format(
            current_page=self.index + 1,
            total_pages=len(self.contents),
        )

    async def _ctx_start(self) -> Message:
        ctx = self.context
        assert isinstance(ctx, Context)

        if self.paginator_mode == PaginatorMode.EMBED:
            embed = self.embeds[self.index]

            if self.auto_fill_index:
                embed = self._embed_auto_index(embed)

            msg = await ctx.send(embed=embed)
        else:
            content = self.contents[self.index]

            if self.auto_fill_index:
                content = self._content_auto_index(content)

            msg = await ctx.send(content)

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
            embed = self.embeds[self.index]

            if self.auto_fill_index:
                embed = self._embed_auto_index(embed)

            await self.__message.edit(embed=embed)
        else:
            content = self.contents[self.index]

            if self.auto_fill_index:
                content = self._content_auto_index(content)

            await self.__message.edit(content=content)

    async def start(self) -> None:
        """
        A function to start the paginator.
        """
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
        """
        A function to stop the paginator.
        """

        assert self.__message

        if self.auto_delete_message:
            try:
                await self.__message.delete()
            except:
                pass
            return

        if self.auto_clear_emoji:
            try:
                await self.__message.clear_reactions()
            except:
                pass
            return
