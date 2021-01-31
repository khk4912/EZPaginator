import discord
from discord.ext import commands
from discord.ext.commands.context import Context

from EZPaginator import Paginator

bot = commands.Bot(command_prefix="!")


@bot.command(name="text")
async def text_pagination(ctx: Context):
    """ Basic text pagination """

    msg = await ctx.send("Test1")
    contents = ["Test1", "Test2", "Test3"]

    page = Paginator(bot=bot, message=msg, contents=contents)
    await page.start()


@bot.command(name="text2")
async def text_pagination_with_extend(ctx: Context):
    """ Text pagination with extended emoji """

    msg = await ctx.send("Test1")
    contents = ["Test1", "Test2", "Test3"]

    page = Paginator(bot=bot, message=msg, contents=contents, use_extend=True)
    await page.start()


@bot.command(name="embed")
async def embed_pagination(ctx: Context):
    """ Basic Embed pagination """

    embed1 = discord.Embed(title="Test1", description="Page1")
    embed2 = discord.Embed(title="Test2", description="Page2")
    embed3 = discord.Embed(title="Test3", description="Page3")
    embeds = [embed1, embed2, embed3]

    msg = await ctx.send(embed=embed1)

    page = Paginator(bot=bot, message=msg, embeds=embeds)
    await page.start()


@bot.command(name="embed2")
async def embed_pagination_with_extend(ctx: Context):
    """ Embed pagination with extended emoji """

    embed1 = discord.Embed(title="Test1", description="Page1")
    embed2 = discord.Embed(title="Test2", description="Page2")
    embed3 = discord.Embed(title="Test3", description="Page3")
    embeds = [embed1, embed2, embed3]

    msg = await ctx.send(embed=embed1)

    page = Paginator(bot=bot, message=msg, embeds=embeds, use_extend=True)
    await page.start()


bot.run("token")
