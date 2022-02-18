from coc.utils import get


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


def get_th_url(th_level):
    if th_level not in th_url_dict:
        return None
    return th_url_dict[th_level]


th_url_list = [
    TH_Url(1, "https://i.imgur.com/XLDc4If.png"),
    TH_Url(2, "https://i.imgur.com/cAhg1w5.png"),
    TH_Url(3, "https://i.imgur.com/kD9mU1O.png"),
    TH_Url(4, "https://i.imgur.com/FJy3Jz7.png"),
    TH_Url(5, "https://i.imgur.com/EK2GJcS.png"),
    TH_Url(6, "https://i.imgur.com/D0ChOuk.png"),
    TH_Url(7, "https://i.imgur.com/65atIGV.png"),
    TH_Url(8, "https://i.imgur.com/pL81ZQP.png"),
    TH_Url(9, "https://i.imgur.com/lYSheK5.png"),
    TH_Url(10, "https://i.imgur.com/jr6AxZP.png"),
    TH_Url(11, "https://i.imgur.com/7mKqDyo.png"),
    TH_Url(12, "https://i.imgur.com/AAsgIrK.png"),
    TH_Url(13, "https://i.imgur.com/EfOqiD1.png"),
    TH_Url(14, "https://i.imgur.com/cCmQhpw.png")
]

th_url_dict = {
    1: "https://i.imgur.com/XLDc4If.png",
    2: "https://i.imgur.com/cAhg1w5.png",
    3: "https://i.imgur.com/kD9mU1O.png",
    4: "https://i.imgur.com/FJy3Jz7.png",
    5: "https://i.imgur.com/EK2GJcS.png",
    6: "https://i.imgur.com/D0ChOuk.png",
    7: "https://i.imgur.com/65atIGV.png",
    8: "https://i.imgur.com/pL81ZQP.png",
    9: "https://i.imgur.com/lYSheK5.png",
    10: "https://i.imgur.com/jr6AxZP.png",
    11: "https://i.imgur.com/7mKqDyo.png",
    12: "https://i.imgur.com/AAsgIrK.png",
    13: "https://i.imgur.com/EfOqiD1.png",
    14: "https://i.imgur.com/cCmQhpw.png"
}
