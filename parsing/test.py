from members import get_my_current_clan_members
from clan_war_list import get_wars
from clan_war import get_cw_units
from clan_war import get_my_clan_attacks
from lcw_list import get_lcw_wars
from lcw import get_lcw_rounds


# https://clashspot.net/en/clan/V8GJ9C0U/view/home-village -- участники клана
# https://clashspot.net/en/clan/V8GJ9C0U/wars/home-village -- список войн клана
# https://clashspot.net/en/clan/V8GJ9C0U/clan-war-leagues/home-village -- список ЛВК
# ★★★ ✰✰✰-- смайлы звезд за атаку
# ├──
# └──


# ----------------------Main Section (Call Methods Section)----------------------

allMethods = [1, 2, 3, 4, 5, 6]
callMethods = []
inp = -1

print(f"1 - {len(allMethods)} -- номера функций")
print("0 -- прекращения ввода")
while inp != 0:
    inp = int(input("Enter: "))
    callMethods.append(inp)

for i in callMethods:
    match i:
        case 1:
            clanMembers_DictionaryList = get_my_current_clan_members(
                "https://clashspot.net/en/clan/V8GJ9C0U/view/home-village"
            )
            print(clanMembers_DictionaryList)
            print()
        case 2:
            clanAttacks_DictionaryList = get_my_clan_attacks(
                "https://clashspot.net/en/clan/V8GJ9C0U/war/133048752"
            )
            print(clanAttacks_DictionaryList)
            print()
        case 3:
            clanWarsList_DictionaryList = get_wars(
                "https://clashspot.net/en/clan/V8GJ9C0U/wars/home-village"
            )
            print(clanWarsList_DictionaryList)
            print()
        case 4:
            clanCWUnits_DictionaryList = get_cw_units(
                "https://clashspot.net/en/clan/V8GJ9C0U/war/133048752"
            )
            print(clanCWUnits_DictionaryList)
            print()
        case 5:
            clanLeagueWarsList_DictionaryList = get_lcw_wars(
                "https://clashspot.net/en/clan/V8GJ9C0U/clan-war-leagues/home-village"
            )
            print(clanLeagueWarsList_DictionaryList)
            print()
        case 6:
            clanLeagueWarsRounds_DictionaryList = get_lcw_rounds(
                "https://clashspot.net/en/clan/V8GJ9C0U/clan-war-leagues/2023-02/details"
            )
            print(get_cw_units(clanLeagueWarsRounds_DictionaryList[0]["href"]))
            print()
