# EZPaginator
![](https://img.shields.io/badge/python-%3E%3D%203.6-blue) ![](https://img.shields.io/badge/discord.py-%3E%3D1.0.0-blue)

Simple pagination wrapper for discord.py.

## Install
```
pip install EZPaginator
```

## Usage

### Parameters
|          Name         |                     Type                    |               Description               |
|:---------------------:|:-------------------------------------------:|:---------------------------------------:|
|          ctx          | `discord.Client` `discord.ext.commands.Bot` |                                         |
|        message        |              `discord.Message`              | Message that wants to apply pagination. |
|        contents       |                    `list`                   |             Contents' list              |
|         embeds        |                    `list`                   |               Embeds' list              |
|  timeout `<optional>` |                    `int`                    |       Reaction add/remove timeout       |
| use_more `<optional>` |                    `bool`                   |    Add emoji for going to first/last    |
|   only `<optional>`   |              `discord.abc.User`             |  Paginator works only for selected user |


### Example Bot
```py
import discord
from EZPaginator import Paginator


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

            msg = await message.channel.send(embed=embed1)
            page = Paginator(self, msg, embeds=embeds)
            await page.start()

client = Example()
client.run('token')
```


![exammple](https://user-images.githubusercontent.com/30457148/78644598-14d24f00-78f1-11ea-8671-d8e5f4c2d1cc.gif)


## Contacts
khk49121@gmail.com
Discord -> BGM#0970

## License
[MIT License](https://github.com/khk4912/EZPaginator/blob/master/LICENSE)