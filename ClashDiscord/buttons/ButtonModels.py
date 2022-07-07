from disnake import ButtonStyle
from disnake.ui import Button


class LinkButton(Button):
    def __init__(
        self,
        btn_name: str,
        url: str,
        btn_style: ButtonStyle = ButtonStyle.primary
    ):
        super().__init__(
            label=btn_name,
            style=btn_style,
            url=url)
