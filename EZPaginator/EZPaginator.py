import asyncio
from typing import List, Optional, Union

import discord
from discord.ext import commands


from .exceptions import MissingAttributeException, InvaildArgumentException


Emoji = List[Union[discord.Emoji, discord.Reaction, discord.PartialEmoji, str]]


class Paginator:
    """
    Class for Pagination.

    Attributes
    ----------
    bot : Union[Client, AutoShardedClient, Bot, AutoShardedBot]
        Bot or Client class.
    message : discord.Message
        A message which wants to apply pagination.
    contents : List[str], optional
        List of contents.
    embeds : List[Embed], optional
        List of embeds. If both contents and embeds are given, the priority is embed.
    timeout : int, default 30
        A timeout of receiving Emoji event.
    use_extend : bool, default False
        Whether to use extended emoji(which includes first/end buttons.).
    only : discord.abc.User, optional
        If a parameter is given, the library responds only to the selected user.
    basic_emoji : List[Emoji], optional
        Custom basic emoji list. There should be 2 emojis.
    extended_emojis : List[Emoji], optional
        Extended emoji list, There should be 4 emojis.
    auto_delete : bool,
        The number of seconds to wait in the background before deleting the target message.
    """

    def __init__(
        self,
        bot: Union[
            discord.Client,
            discord.AutoShardedClient,
            commands.Bot,
            commands.AutoShardedBot,
        ],
        message: discord.Message,
        contents: Optional[List[str]] = None,
        embeds: Optional[List[discord.Embed]] = None,
        timeout: int = 30,
        use_extend: bool = False,
        only: Optional[discord.abc.User] = None,
        clear_react: bool = False,
        basic_emojis: Optional[Emoji] = None,
        extended_emojis: Optional[Emoji] = None,
        auto_delete: bool = False,
    ) -> None:
        self.bot = bot
        self.message = message
        self.contents = contents
        self.embeds = embeds
        self.timeout = timeout
        self.use_extend = use_extend
        self.only = only
        self.clear_react = clear_react
        self.basic_emojis = ["⬅️", "➡️"]
        self.extended_emojis = ["⏪", "⬅️", "➡️", "⏩"]
        self.auto_delete = auto_delete
        self.index = 0

        if (
            isinstance(bot, discord.Client)
            or isinstance(bot, discord.AutoShardedClient)
            or isinstance(bot, commands.Bot)
            or isinstance(bot, commands.AutoShardedBot)
        ):
            pass
        elif (
            issubclass(bot, discord.Client)
            or issubclass(bot, discord.AutoShardedClient)
            or issubclass(bot, commands.Bot)
            or issubclass(bot, commands.AutoShardedBot)
        ):
            pass
        else:
            raise TypeError

        if contents is None and embeds is None:
            raise MissingAttributeException(
                "Both contents and embeds are None."
            )

        if not isinstance(timeout, int):
            raise TypeError("timeout must be int.")

        if basic_emojis is not None:
            if self.use_extend:
                raise InvaildArgumentException("use_extend should be False.")

            if len(set(self.basic_emojis)) != 2:
                raise InvaildArgumentException(
                    "There should be 2 elements in basic_emojis."
                )
            self.basic_emojis = basic_emojis

        if extended_emojis is not None:
            if not self.use_extend:
                raise InvaildArgumentException("use_extend should be True.")

            if len(set(self.extended_emojis)) != 4:
                raise InvaildArgumentException(
                    "Ther should be 4 elements in extended_emojis"
                )
            self.extended_emojis = extended_emojis

    def emoji_check(self, payload: discord.RawReactionActionEvent) -> bool:
        if payload.user_id == self.bot.user.id:
            return False

        if payload.message_id != self.message.id:
            return False

        if self.only is not None:
            if payload.user_id != self.only.id:
                return False

        if self.use_extend:
            if str(payload.emoji) not in self.extended_emojis:
                return False
        else:
            if str(payload.emoji) not in self.basic_emojis:
                return False

        return True

    async def start(self) -> None:
        await self.add_reaction()

        while True:
            try:
                add_reaction = asyncio.ensure_future(
                    self.bot.wait_for(
                        "raw_reaction_add", check=self.emoji_check
                    )
                )

                remove_reaction = asyncio.ensure_future(
                    self.bot.wait_for(
                        "raw_reaction_remove", check=self.emoji_check
                    )
                )

                done, pending = await asyncio.wait(
                    (add_reaction, remove_reaction),
                    return_when=asyncio.FIRST_COMPLETED,
                    timeout=self.timeout,
                )

                for i in pending:
                    i.cancel()

                if len(done) == 0:
                    raise asyncio.TimeoutError

                payload = done.pop().result()
                await self.handle_pagination(payload.emoji)

            except asyncio.TimeoutError:
                break

        if self.auto_delete:
            try:
                await self.message.delete()
            except:
                pass
 
    async def add_reaction(self) -> None:
        if self.use_extend:
            for i in self.extended_emojis:
                await self.message.add_reaction(i)
        else:
            for i in self.basic_emojis:
                await self.message.add_reaction(i)

    async def handle_pagination(self, emoji: discord.PartialEmoji) -> None:
        if self.use_extend:
            if str(emoji) == self.extended_emojis[1]:
                await self.go_previous()
            elif str(emoji) == self.extended_emojis[2]:
                await self.go_next()

            elif str(emoji) == self.extended_emojis[0]:
                await self.go_first()
            elif str(emoji) == self.extended_emojis[3]:
                await self.go_last()
        else:
            if str(emoji) == self.basic_emojis[0]:
                await self.go_previous()
            elif str(emoji) == self.basic_emojis[1]:
                await self.go_next()

    async def go_previous(self) -> None:
        if self.index == 0:
            return

        self.index -= 1
        if self.contents is None:
            await self.message.edit(embed=self.embeds[self.index])
        else:
            await self.message.edit(content=self.contents[self.index])

    async def go_next(self) -> None:
        if self.embeds is not None:
            if self.index != len(self.embeds) - 1:
                self.index += 1
                await self.message.edit(embed=self.embeds[self.index])

        elif self.contents is not None:
            if self.index != len(self.contents) - 1:
                self.index += 1
                await self.message.edit(content=self.contents[self.index])

    async def go_first(self) -> None:
        if self.index == 0:
            return

        self.index = 0

        if self.contents is None:
            await self.message.edit(embed=self.embeds[self.index])
        else:
            await self.message.edit(content=self.contents[self.index])

    async def go_last(self) -> None:
        if self.embeds is not None:
            if self.index != len(self.embeds) - 1:
                self.index = len(self.embeds) - 1
                await self.message.edit(embed=self.embeds[self.index])

        elif self.contents is not None:
            if self.index != len(self.contents) - 1:
                self.index = len(self.contents) - 1
                await self.message.edit(content=self.contents[self.index])