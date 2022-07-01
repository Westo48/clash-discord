import disnake


class HelpMainView(disnake.ui.View):

    def __init__(
            self, buttons: list):
        super().__init__(timeout=None)
        self.buttons = buttons

        for button in buttons:
            self.add_item(button)
