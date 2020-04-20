import asyncio
import discord
from discord.ext import commands


class YouLLamaed(Exception):
    pass


class Submarine(Exception):
    pass


class Paginator:
    def __init__(
        self,
        ctx,
        message: discord.Message,
        contents: list = None,
        embeds: list = None,
        timeout: int = 30,
    ):
        self.ctx = ctx
        self.message = message  # Pagination Target
        self.timeout = timeout
        self.reactions = ["⬅️", "➡️"]
        self.contents = contents
        self.index = 0
        self.embeds = embeds

        if contents is None and embeds is None:
            raise YouLLamaed("LLama ate all of your contents and embeds.")

        if not isinstance(self.timeout, int):
            raise Submarine("Your submarine tried to jump in a string.")

    def emoji_checker(self, payload):
        if payload.user_id == self.ctx.user.id:
            return False

        if payload.message_id != self.message.id:
            return False

        if str(payload.emoji) in self.reactions:
            return True
        return False

    async def add_reactions(self):
        for i in self.reactions:
            await self.message.add_reaction(i)
        return True

    async def start(self):
        await self.add_reactions()

        while True:
            try:
                add_reaction = asyncio.ensure_future(
                    self.ctx.wait_for(
                        "raw_reaction_add", check=self.emoji_checker
                    )
                )
                remove_reaction = asyncio.ensure_future(
                    self.ctx.wait_for(
                        "raw_reaction_remove", check=self.emoji_checker
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
                    raise asyncio.TimeoutError()

                payload = done.pop().result()  ## done : set
                await self.pagination(payload.emoji)

            except asyncio.TimeoutError:
                try:
                    await self.message.clear_reactions()
                    break
                except:
                    break

    async def pagination(self, emoji):
        if str(emoji) == "⬅️":
            await self.go_previous()
        elif str(emoji) == "➡️":
            await self.go_next()

    async def go_previous(self):
        if self.index != 0:
            self.index -= 1
            if self.contents is None:
                await self.message.edit(embed=self.embeds[self.index])
            else:
                await self.message.edit(content=self.contents[self.index])

    async def go_next(self):
        if self.contents is None:
            if self.index != len(self.embeds) - 1:
                self.index += 1
                await self.message.edit(embed=self.embeds[self.index])

        else:
            if self.index != len(self.contents) - 1:
                self.index += 1
                await self.message.edit(content=self.contents[self.index])
