class TH_Url(object):
    """
        TH_Url: object for TH urls

            Instance Attributes
                display_name (str): 
                    emoji name to display if emoji is not found or usable
                discord_id (int): id for emoji in discord
                discord_name (str): formatted discord name emoji name
                coc_name (str): formatted coc.py name
                # description (str): description for emoji
    """

    def __init__(self, level, url):
        self.level = level
        self.url = url


th_url_list = [
    TH_Url(1, "https://imgur.com/XLDc4If"),
    TH_Url(2, "https://imgur.com/cAhg1w5"),
    TH_Url(3, "https://imgur.com/kD9mU1O"),
    TH_Url(4, "https://imgur.com/FJy3Jz7"),
    TH_Url(5, "https://imgur.com/EK2GJcS"),
    TH_Url(6, "https://imgur.com/D0ChOuk"),
    TH_Url(7, "https://imgur.com/65atIGV"),
    TH_Url(8, "https://imgur.com/pL81ZQP"),
    TH_Url(9, "https://imgur.com/lYSheK5"),
    TH_Url(10, "https://imgur.com/jr6AxZP"),
    TH_Url(11, "https://imgur.com/7mKqDyo"),
    TH_Url(12, "https://imgur.com/AAsgIrK"),
    TH_Url(13, "https://imgur.com/EfOqiD1"),
    TH_Url(14, "https://imgur.com/cCmQhpw")
]

th_url_dict = {
    1: "https://imgur.com/XLDc4If",
    2: "https://imgur.com/cAhg1w5",
    3: "https://imgur.com/kD9mU1O",
    4: "https://imgur.com/FJy3Jz7",
    5: "https://imgur.com/EK2GJcS",
    6: "https://imgur.com/D0ChOuk",
    7: "https://imgur.com/65atIGV",
    8: "https://imgur.com/pL81ZQP",
    9: "https://imgur.com/lYSheK5",
    10: "https://imgur.com/jr6AxZP",
    11: "https://imgur.com/7mKqDyo",
    12: "https://imgur.com/AAsgIrK",
    13: "https://imgur.com/EfOqiD1",
    14: "https://imgur.com/cCmQhpw"
}
