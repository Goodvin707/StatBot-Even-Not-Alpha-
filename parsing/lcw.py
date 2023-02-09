import requests
from bs4 import BeautifulSoup
from selenium import webdriver


def get_lcw_rounds(url):
    try:
        clan_id = url.split("/")[5]
        return [
            _extract_round_data(i, clan_id)
            for i in _prepare_wars_data(url).find_all("section", class_="league-round")
        ]
    except Exception as e:
        return f"Data retrieval error\n{e.with_traceback(None)}"


def _prepare_wars_data(url):
    driver = webdriver.Edge()
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    # page = requests.get(url)
    # soup = BeautifulSoup(page.text, "html.parser")
    return soup.find("div", id="matches")


def _extract_round_data(round_tag, clan_id):
    """
    1 - round
    3 - matches
        └──1
            └──1 clan1
            └──3 attacks
            └──5 stars
        └──3 href
        └──5
            └──1 stars
            └──3 attacks
            └──5 clan2
    """

    round = str(round_tag.contents[1].string).replace(" ", "").replace("\n", "")
    clan1 = ""
    clan1_attacks = 0
    clan1_stars = 0
    clan2 = ""
    clan2_attacks = 0
    clan2_stars = 0
    href = ""

    matches_tag = round_tag.contents[3].find_all("li")
    for match in matches_tag:
        if _is_my_clan(match.find("div")["data-clan"], clan_id):
            clan1 = (
                str(match.contents[1].contents[1].string)
                .replace(" ", "")
                .replace("\n", "")
            )
            clan1_attacks = int(
                (
                    str(match.contents[1].contents[3].contents[0])
                    .replace(" ", "")
                    .replace("\n", "")
                )
            )

            clan1_stars = int(
                (
                    str(match.contents[1].contents[5].contents[0])
                    .replace(" ", "")
                    .replace("\n", "")
                )
            )

            clan2 = (
                str(match.contents[5].contents[5].string)
                .replace(" ", "")
                .replace("\n", "")
            )
            clan2_attacks = int(
                (
                    str(match.contents[5].contents[3].contents[2])
                    .replace(" ", "")
                    .replace("\n", "")
                )
            )

            clan2_stars = int(
                (
                    str(match.contents[5].contents[1].contents[2])
                    .replace(" ", "")
                    .replace("\n", "")
                )
            )
            href = "https://clashspot.net" + match.contents[3].find("a")["href"]
    return {
        "round": round,
        "clan1": clan1,
        "clan1Attacks": clan1_attacks,
        "clan1Stars": clan1_stars,
        "clan2": clan2,
        "clan2Attacks": clan2_attacks,
        "clan2Stars": clan2_stars,
        "href": href,
    }


def _is_my_clan(matchTag, clanID):
    return str(matchTag) == clanID
