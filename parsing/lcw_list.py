import requests
from bs4 import BeautifulSoup
from selenium import webdriver


def get_lcw_wars(url):
    try:
        return _remove_ocurrences_by_value(
            [_extract_war_data(i) for i in _prepare_wars_data(url).find_all("tr")], ""
        )
    except Exception as e:
        return f"Data retrieval error\n{e.with_traceback(None)}"


def _prepare_wars_data(url):
    driver = webdriver.Edge()
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    # page = requests.get(url)
    # soup = BeautifulSoup(page.text, "html.parser")
    # print(soup.find("tbody", id="leagues-container"))
    return soup.find("tbody", id="leagues-container")


def _extract_war_data(war):
    """
    1 - league
    3 - result
    5 - month
    7 - size
    9 - rank
    11 - stars
    13 - destruction
    15 - victories
    17 - defeats
    19 - draws
    21 - state
    23 - href
    """

    # league = ""
    # result = ""
    # month = ""
    # size = ""
    # rank = ""
    # stars = ""
    # destruction = ""
    # victories = ""
    # defeats = ""
    # draws = ""
    # state = ""
    # href = ""
    if not _check_for_year_tag(war.contents):
        league = war.contents[1].find("img")["title"]
        result = _define_lcw_result(war.contents[3])
        month = war.contents[5].find("a").string
        size = int(war.contents[7].string)
        rank = int(war.contents[9].string)
        stars = int(
            str(war.contents[11].contents[0]).replace("\n", "").replace(" ", "")
        )
        destruction = int(
            str(war.contents[13].contents[0]).replace("\n", "").replace(" ", "")
        )
        victories = int(
            str(war.contents[15].find("span").string).replace("\n", "").replace(" ", "")
        )
        defeats = int(
            str(war.contents[17].find("span").string).replace("\n", "").replace(" ", "")
        )
        draws = str(war.contents[19].string).replace("\n", "").replace(" ", "")
        state = war.contents[21].find("span").string
        href = _get_war_href(war.contents[23].find("a"))
        return {
            "month": month,
            "result": result,
            "league": league,
            "rank": rank,
            "size": size,
            "stars": stars,
            "destruction": destruction,
            "victories": victories,
            "defeats": defeats,
            "draws": draws,
            "state": state,
            "href": href,
        }
    return ""


def _check_for_year_tag(warTag):
    return len(warTag) == 3


def _get_war_href(war_href_tag):
    if str(war_href_tag) == "None":
        return "Log for this war doesn't exist"
    return str("https://clashspot.net" + str(war_href_tag["href"]))


def _define_lcw_result(result_tag):
    """
    fas fa-minus
    fas fa-caret-down
    fas fa-caret-up
    """

    result_tag = result_tag.find_all("span")[1]
    match result_tag["class"][1]:
        case "fa-minus":
            return "Stay"
        case "fa-caret-down":
            return "Lose"
        case "fa-caret-up":
            return "Win"


def _remove_ocurrences_by_value(list, val):
    return [value for value in list if value != val]
