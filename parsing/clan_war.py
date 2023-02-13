import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from parsing import page_loader

# ------------------War Course------------------


def get_cw_units(url):
    try:
        return [
            _extract_cw_unit_data(i)
            for i in page_loader.prepare_data(url)
            .find("section", class_="members separator separator-bottom separator-top")
            .find_all("div", class_="members-position")
        ]
    except Exception as e:
        return f"Data retrieval error\n{e.with_traceback(None)}"


def _extract_cw_unit_data(cw_couple):
    """
    1 - myClanMember
    3 - enemyClanMember
    """

    my_clan_member_position_and_nickname = (
        str(
            cw_couple.contents[1]
            .find("span", class_="members-position-header")
            .find("a", class_="members-position-name")
            .string
        )
        .replace("\n", "")
        .replace(" ", "")
    )
    position = my_clan_member_position_and_nickname.split(".")[0]
    nickname = my_clan_member_position_and_nickname.split(".")[1]
    id = (
        cw_couple.contents[1]
        .find("span", class_="members-position-header")
        .find("a", class_="members-position-name")["href"]
        .split("/")[3]
    )

    my_clan_member_attaks = cw_couple.contents[1].find(
        "span", class_="members-position-attacks"
    )
    attack_count = _check_attack_count(my_clan_member_attaks)
    attack_list = _extract_unit_attack_list(my_clan_member_attaks)
    return {
        "position": position,
        "nickname": nickname,
        "attackList": attack_list,
        "attackCount": attack_count,
        "id": id,
    }


def _extract_unit_attack_list(clan_member_attacks):
    """
    1 - attackPercent
    3 - stars
    5 - enemyNickname
    7 - enemyPosition
    """

    if str(clan_member_attacks.find("span", "members-position-attack")) != "None":
        attack_list = []
        clan_member_attacks = clan_member_attacks.find_all(
            "span", "members-position-attack"
        )
        for i in range(len(clan_member_attacks)):
            attack_percent = clan_member_attacks[i].contents[1].string
            stars = len(
                clan_member_attacks[i]
                .contents[3]
                .find_all("i", class_="fas fa-star stars-win")
            )
            enemy_nickname = clan_member_attacks[i].contents[5].string
            enemy_position = int(clan_member_attacks[i].contents[7].string)
            attack_list.append(
                {
                    "enemyPosition": enemy_position,
                    "enemyNickname": enemy_nickname,
                    "stars": stars,
                    "attackPercent": attack_percent,
                }
            )
        return attack_list
    return ["no attacks"]


def _check_attack_count(clan_member_attacks):
    if str(clan_member_attacks.find("span", "members-position-attack")) != "None":
        return len(clan_member_attacks.find_all("span", "members-position-attack"))
    return 0


# ------------------Attacks------------------


def get_my_clan_attacks(url):
    try:
        return [
            _extract_attack_data(i)
            for i in page_loader.prepare_data(url)
            .find("section", class_="attacks separator separator-bottom")
            .find_all("tr", class_="clan1")
        ]
    except Exception as e:
        return f"Data retrieval error\n{e}\n{e.with_traceback(None)}"


def _extract_attack_data(my_clan_member):
    """
    1 - position
    3 - nickname & id
    9 - stars
    """

    tag_position = my_clan_member.contents[1]
    tag_nickname = my_clan_member.contents[3]
    tag_stars = my_clan_member.contents[9]
    tag_id = my_clan_member.contents[3]

    position = int(tag_position.contents[1].string)
    nickname = tag_nickname.find(class_="player-name").string
    id = tag_id.find(class_="player-tag").string
    stars = len(tag_stars.find_all(class_="fas fa-star stars-win"))
    return {"position": position, "nickname": nickname, "stars": stars, "id": id}
