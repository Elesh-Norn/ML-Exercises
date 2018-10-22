import urllib.request
import json
import pandas as pd

STANDARD_SET_LIST = ['m19', "dom", "rix", "xln", "grn"]


def get_all_card_from_search(url):
    """
    During a search, will pull other cards and add them to the
    "data" list from scryfall. Returns it if there is no other card
    """

    temp_dic = urllib.request.urlopen(url).read()
    temp_dic = json.loads(temp_dic)
    if temp_dic["has_more"]:
        temp_dic["data"].extend(
            get_all_card_from_search(temp_dic["next_page"]))
        return temp_dic["data"]
    else:
        return temp_dic["data"]


def get_set(set):
    """
    Search for card in a set (3 letter string)
    Return a panda dataframe with card name, price in usd, rarity and set
    """

    temp_list = get_all_card_from_search('https://api.scryfall.com/cards/search?q=e:'+set)
    df = pd.DataFrame.from_dict(temp_list)

    return df


def get_all_standard():
    """
    Search for all card in Standard and return a Dataframe
    """
    df = pd.DataFrame()
    for magics_set in STANDARD_SET_LIST:
        df = pd.concat([df, get_set(magics_set)], sort=False)

    return df
