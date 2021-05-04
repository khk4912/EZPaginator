# EZPaginator
![](https://img.shields.io/badge/python-%3E%3D%203.6-blue) ![](https://img.shields.io/badge/discord.py-%3E%3D1.0.0-blue)

Simple pagination wrapper for discord.py.

## Install
```
pip install EZPaginator
```

## Usage

### Parameters
| Parameter | Type | Description |
|-|-|-|
| bot | Union[Client, AutoShardedClient, Bot, AutoShardedBot] | Bot or Client class. |
| message | discord.Message | A message which wants to apply pagination. |
| contents | List[str], optional | List of contents. |
| embeds | List[Embed], optional | List of embeds.If both contents and embeds are given, the priority is embed. |
| timeout | int, default 30 | A timeout of receiving Emoji event. Defaults to 30. |
| use_extend | bool, default False | Whether to use extended emoji(which includes first/end buttons.). Defaults to False. |
| only | discord.abc.User, optional | If a parameter is given, the library will respond only to the selected user. |
| basic_emoji | List[Emoji], optional | Custom basic emoji list. There should be 2 emojis. |
| extended_emojis | List[Emoji], optional | Custom extended emoji list, There should be 4 emojis. |
| auto_delete | bool, default False | Whether to delete message after timeout. Defaults to False. |

## Example
<details><summary>Click to expand example</summary>
<p>

[Full example code](/Example/example.py)

### Basic text pagination
```py
@bot.command(name="text")
async def text_pagination(ctx: Context):
    """ Basic text pagination """

    msg = await ctx.send("Test1")
    contents = ["Test1", "Test2", "Test3"]

    page = Paginator(bot=bot, message=msg, contents=contents)
    await page.start()

```
![Basic text](https://i.imgur.com/eHND0WA.gif)

### Text pagination with extended emojis
```py
@bot.command(name="text2")
async def text_pagination_with_extend(ctx: Context):
    """ Text pagination with extended emoji """

    msg = await ctx.send("Test1")
    contents = ["Test1", "Test2", "Test3"]

    page = Paginator(bot=bot, message=msg, contents=contents, use_extend=True)
    await page.start()
```
![Extended text](https://i.imgur.com/20yOaf3.gif)

### Basic embed pagination
```py
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
```
![Basic embed](https://i.imgur.com/LGqm6Jl.gif)

### Embed pagination with extended emojis
```py
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
```
![Extended Embed](https://i.imgur.com/Py74Ybl.gif)


</p>
</details>
<br>

## Contacts
khk4912@uniquecode.team  
Discord -> BGM#0970

## License
[MIT License](https://github.com/khk4912/EZPaginator/blob/master/LICENSE)