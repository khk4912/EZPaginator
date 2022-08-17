from discord import Emoji
from discord.ui import button

DEFAULT_EMOJIS = ["⬅️", "➡️"]
DEFAULT_EXTENDED_EMOJIS = ["⬅️", "➡️", "⏩", "⏪"]


DEFAULT_BUTTONS = [button(emoji="⬅️"), button(emoji="➡️")]
DEFAULT_EXTENDED_BUTTONS = [
    button(emoji="⬅️"),
    button(emoji="➡️"),
    button(emoji="⏩"),
    button(emoji="⏪"),
]

T_emoji = list[str] | list[Emoji] | list[Emoji | str]
