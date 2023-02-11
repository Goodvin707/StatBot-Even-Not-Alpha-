import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from parsing import page_loader


def get_my_current_clan_members(url):
    try:
        my_clan_members_stats_with_tags = (
            page_loader.prepare_data(url).find("div", id="members").find_all("tr")
        )
        my_clan_members_stats_with_tags = my_clan_members_stats_with_tags[
            1 : len(my_clan_members_stats_with_tags)
        ]
        my_clan_members_stats = [
            _extract_data(i) for i in my_clan_members_stats_with_tags
        ]
        return my_clan_members_stats
    except Exception as e:
        return f"Data retrieval error\n{e.with_traceback(None)}"


def _extract_data(my_clan_member):
    """
    Note: 01.02.2023
    3 - league
    5 - thLevel
    7 - nickname & id
    9 - role
    11 - cwParticipation
    13 - trophies
    15 - playerLevel
    17 - capitalLevel
    19 - capitalTotalDonations
    21 - altarTroopsDonated & altarTroopsReceived
    """

    league = my_clan_member.contents[3].find("img")["title"]
    th_level = my_clan_member.contents[5].find("img")["title"]
    nickname = (
        str(my_clan_member.contents[7].find("a").contents[0])
        .replace(" ", "")
        .replace("\n", "")
    )
    id = my_clan_member.contents[7].find("span").string
    role = my_clan_member.contents[9].find("span").string
    cw_participation = _define_cw_participation(
        my_clan_member.contents[11].find("span").find("img")["src"]
    )
    trophies = int(
        my_clan_member.contents[13].find("span", class_="value").string.replace(",", "")
    )
    player_level = int(my_clan_member.contents[15].find("span", class_="value").string)
    capital_level = int(my_clan_member.contents[17].find("span", class_="value").string)
    capital_total_donations = int(
        my_clan_member.contents[19].find("span", class_="value").string.replace(",", "")
    )
    altar_troops_donated = int(
        my_clan_member.contents[21]
        .find("span", title="Troops donated")
        .find("span", class_="value")
        .string.replace(",", "")
    )
    altar_troops_received = int(
        my_clan_member.contents[21]
        .find("span", title="Troops received")
        .find("span", class_="value")
        .string.replace(",", "")
    )
    return {
        "nickname": nickname,
        "thLevel": th_level,
        "cwParticipation": cw_participation,
        "role": role,
        "league": league,
        "trophies": trophies,
        "playerLevel": player_level,
        "capitalLevel": capital_level,
        "capitalTotalDonations": capital_total_donations,
        "altarTroopsDonated": altar_troops_donated,
        "altarTroopsReceived": altar_troops_received,
        "id": id,
    }


def _define_cw_participation(icon_path):
    if "war-opt-in" in icon_path:
        return "yes"
    return "no"
