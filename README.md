# EZPaginator

![Python version](https://img.shields.io/pypi/pyversions/EZPaginator?style=for-the-badge&logo=python) ![discord.py version](https://img.shields.io/badge/discord.py-%3E%3D%202.0-blue?style=for-the-badge) ![Monthly donwload count](https://img.shields.io/pypi/dm/EZPaginator?color=blue&style=for-the-badge)

Easy-to-use pagination library for discord.py

## Install

```
pip3 install EZPaginator
```

## Usage

### Parameters

| Parameter           | Type                     | Description                                                                                                                                                  |
|---------------------|--------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------|
| context             | Context \| Interaction   | Context or Interaction object.                                                                                                                               |
| embeds              | list[Embed]              | List of embed contents, by default [].                                                                                                                       |
| contents            | list[str]                | List of message contents, by default []. <br /> If both embeds and contents are given, Paginator will paginate only embeds.                                  |
| timeout             | int                      | Timeout of the paginator, by default 30                                                                                                                      |
| start_index         | int                      | Start index of embeds/contents, by default 0.                                                                                                                |
| auto_clear_emoji    | bool                     | Whether to clear the emoji when the pagination is stopped by function stop() or timeout. by default True.<br /> This might need 'manage message' permission. |
| auto_delete_message | bool                     | Whether to delete the message when the pagination is stopped by function stop() or by timeout. by default False.                                             |
| use_extend          | bool                     | Whether to use the extended emoji set(First, Previous, Next, Last). by default False.                                                                        |
| emojis              | list[str \| Emoji]       | List of emojis to use for pagination. by default ["⬅️", "➡️"]                                                                                                  |
| extended_emojis     | list[str \| Emoji]       | List of extended emojis to use for pagination. by default ["⏪", "⬅️", "➡️", "⏩"]         only : User \| None, optional                                         |
| only                | discord.abc.User \| None | Restrict only the user to use the pagination. by default None.                                                                                               |
| auto_fill_index     | bool                     | Enable auto-fill index mode, by default False.                                                                                                               |
## Example

<details>
    <summary>Click to expand example</summary>

[Full example code](/Example)

### Basic Emebd Pagination

```py
## Commands
@bot.command()
async def test(ctx: commands.Context) -> None:
    embeds = [
        discord.Embed(title="TEST 1", description="Page 1", color=discord.Color.red()),
        discord.Embed(title="TEST 2", description="Page 2", color=discord.Color.blue()),
        discord.Embed(title="TEST 3", description="Page 3", color=discord.Color.gold()),
    ]

    page = Paginator(ctx, embeds=embeds)
    await page.start()


## Slash Commands
@bot.tree.command()
async def slash_embed(interaction: discord.Interaction):
    embeds = [
        discord.Embed(title="TEST 1", description="Page 1", color=discord.Color.red()),
        discord.Embed(title="TEST 2", description="Page 2", color=discord.Color.blue()),
        discord.Embed(title="TEST 3", description="Page 3", color=discord.Color.gold()),
    ]

    page = Paginator(interaction, embeds=embeds)
    await page.start()


```

Commands                   |  Slash Command
:-------------------------:|:-------------------------:
![](https://user-images.githubusercontent.com/30457148/181737625-e8d19098-7c3c-4990-8339-7955ab86f279.mov)  |  ![](https://user-images.githubusercontent.com/30457148/181737907-aa3ba67c-261a-4b86-a235-997eb2514e7b.mov)

### Text Pagination W/ Extended Emojis

```py
## Commands
@bot.command()
async def test(ctx: commands.Context) -> None:
    contents = ["This is Page 1", "This is Page 2", "This is Page 3"]

    page = Paginator(ctx, contents=contents, use_extend=True)
    await page.start()


## Slash Commands
@bot.tree.command()
async def slash_content(interaction: discord.Interaction) -> None:
    contents = ["This is Page 1", "This is Page 2", "This is Page 3"]

    page = Paginator(interaction, contents=contents, use_extend=True)
    await page.start()

```

Commands                   |  Slash Command
:-------------------------:|:-------------------------:
![](https://user-images.githubusercontent.com/30457148/181743036-18182010-6ffe-494b-9c00-6d2e4b994cf3.mov
)  |  ![](https://user-images.githubusercontent.com/30457148/181743122-c34424ba-16ba-4269-bed0-ef5a752ff5c7.mov)


### Use Custom Emoji

```py
## Commands
@bot.command()
async def test(ctx: commands.Context) -> None:
    embeds = [
        discord.Embed(title="TEST 1", description="Page 1", color=discord.Color.red()),
        discord.Embed(title="TEST 2", description="Page 2", color=discord.Color.blue()),
        discord.Embed(title="TEST 3", description="Page 3", color=discord.Color.gold()),
    ]

    page = Paginator(ctx, embeds=embeds, emojis=["⬇️", "⬆️"])
    await page.start()


## Slash Commands
@bot.tree.command()
async def slash_content(interaction: discord.Interaction) -> None:
    contents = ["This is Page 1", "This is Page 2", "This is Page 3"]

    page = Paginator(
        interaction,
        contents=contents,
        use_extend=True,
        extended_emojis=["⏬", "⬇️", "⬆️", "⏫"],
    )
    await page.start()
```

Commands w/ custom emojis  |  Slash Command w/ extended custom emojis
:-------------------------:|:-------------------------:
![](https://user-images.githubusercontent.com/30457148/181746283-cb8c2593-1b42-4cdd-9e56-6d45afa12c06.mov
)  |  ![](https://user-images.githubusercontent.com/30457148/181746387-c1248f17-7205-4264-b0c0-0142e9c42149.mov)

### Auto-fill Index mode

If `auto_fill_index` is True, `{current_page}` and `{total_pages}` will be automatically filled with the current page and total pages.  
Auto-fill Index also works with contents.

```py
@bot.command()
async def test(ctx: commands.Context) -> None:
    embeds = [
        discord.Embed(
            title="Hello ({current_page} / {total_pages})",
            description="World",
        ),
        discord.Embed(
            title="Wow ({current_page} / {total_pages})",
            description="Current page is {current_page}",
        ),
    ]

    for i in embeds:
        i.set_footer(text="Page {current_page} of {total_pages}")

    page = Paginator(
        ctx,
        embeds=embeds,
        auto_fill_index=True,
    )
    await page.start()
```
![](https://user-images.githubusercontent.com/30457148/181747803-562df165-8d79-493d-bb8b-cd788c480c2c.mov)

</p>
</details>
  

## Contacts

BGM#0970

## License

[MIT License](https://github.com/khk4912/EZPaginator/blob/master/LICENSE)
