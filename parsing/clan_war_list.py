import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from parsing import page_loader


def get_wars(url):
    try:
        return [
            _extract_war_data(i)
            for i in page_loader.prepare_data(url)
            .find("tbody", id="clan-warlog-container")
            .find_all("tr")
        ]
    except Exception as e:
        return f"Data retrieval error\n{e}\n{e.with_traceback(None)}"


def _extract_war_data(war):
    """
    1 - clan1Name & clan1Id
    3 - clan2Name & clan2Id
    5 - warSize
    7 - Summary
        └──1 - clan1Percent
        └──3 - clan1Stars
        └──5 - clan2Percent
        └──7 - clan2Stars
    9 - warWinLose
    11 - warDate & warHour
    13 - href
    """

    clan1_name = (
        str(war.contents[1].find("a").contents[0]).replace("\n", "").replace(" ", "")
    )
    clan1_id = war.contents[1].find("span").string
    clan2_name = (
        str(war.contents[3].find("a").contents[0]).replace("\n", "").replace(" ", "")
    )
    clan2_id = war.contents[3].find("span").string
    war_size = int(war.contents[5].find("span").string)

    summary = war.contents[7].contents
    clan1_percent = ""
    clan1_stars = 0
    clan2_percent = ""
    clan2_stars = 0
    if len(summary) != 1:
        clan1_percent = summary[1].string
        clan1_stars = int(summary[3].string)
        clan2_stars = int(summary[5].string)
        clan2_percent = summary[7].string

    war_win_lose = war.contents[9].contents[1].string

    war_date = war.contents[11].contents[1].string
    war_hour = war.contents[11].contents[3].string

    war_href_tag = war.contents[13].find("a")
    href = _get_war_href(war_href_tag)
    return {
        "clan1Name": clan1_name,
        "clan1Id": clan1_id,
        "clan2Name": clan2_name,
        "clan2Id": clan2_id,
        "warSize": war_size,
        "clan1Percent": clan1_percent,
        "clan1Stars": clan1_stars,
        "clan2Percent": clan2_percent,
        "clan2Stars": clan2_stars,
        "warWinLose": war_win_lose,
        "warDate": war_date,
        "warHour": war_hour,
        "href": href,
    }


def _get_war_href(war_href_tag):
    if str(war_href_tag) == "None":
        return "Log for this war doesn't exist"
    return str("https://clashspot.net" + str(war_href_tag["href"]))
