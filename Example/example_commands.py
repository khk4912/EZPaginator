import discord
from discord.ext import commands
from EZPaginator import Paginator


bot = commands.Bot(command_prefix="!")


@bot.command(name="페이징")
async def text_pagination(ctx):
    msg = await ctx.send("페이지1")
    contents = ["페이지1", "페이지2", "페이지3"]

    page = Paginator(bot, msg, contents=contents)
    await page.start()


@bot.command(name="페이징2")
async def embed_pagination(ctx):
    embed1 = discord.Embed(title="Embed1", description="embed1")
    embed2 = discord.Embed(title="Embed2", description="embed2")
    embed3 = discord.Embed(title="Embed3", description="embed3")
    embeds = [embed1, embed2, embed3]
    msg = await ctx.send(embed=embed1)

    page = Paginator(bot, msg, embeds=embeds)
    await page.start()


bot.run("token")
