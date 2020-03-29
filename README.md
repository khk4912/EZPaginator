## EZPaginator
사용하기 쉬운 discord.py의 페이징 구현, EZPaginator입니다.


## Example
```py
import discord
from EZpaginator import Paginator


class Example(discord.Client):
    async def on_message(self, message):
        ## 일반 메시지 
        if message.content == '!페이징':
            msg = await message.channel.send("페이지1")
            contents = ['페이지1', '페이지2', '페이지3']

            page = Paginator(self, msg, contents=contents)
            await page.start()

        ## Embed 
        elif message.content == '!페이징2':
            embed1=discord.Embed(title="Embed1", description="embed1")
            embed2=discord.Embed(title="Embed2", description="embed2")
            embed3=discord.Embed(title="Embed3", description="embed3")
            embeds = [embed1, embed2, embed3]

            msg = await message.channel.send(embed=embed)
            page = Paginator(self, msg, embeds=embeds)
            await page.start()

client = Example()
client.run('token')
```