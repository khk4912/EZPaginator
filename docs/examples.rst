Examples
========

- Embed pagination w/o use_extend option

  .. code-block:: python
    

      bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())


      @bot.command()
      async def test(ctx: commands.Context) -> None:
          embeds = [
              discord.Embed(title="TEST 1", description="Page1"),
              discord.Embed(title="TEST 2", description="Page2"),
              discord.Embed(title="TEST 3", description="Page3"),
          ]

          page = Paginator(ctx, embeds=embeds)
          await page.start()

  .. image:: https://user-images.githubusercontent.com/30457148/181721637-d2a5b96c-2769-406b-a9a0-008844ebc141.gif
