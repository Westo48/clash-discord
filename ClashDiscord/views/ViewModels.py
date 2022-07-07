from disnake.ui import View, Button


class ButtonListView(View):

    def __init__(
            self, buttons: list[Button]):
        super().__init__(timeout=None)
        self.buttons = buttons

        for button in buttons:
            self.add_item(button)
