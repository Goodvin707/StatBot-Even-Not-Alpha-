import telebot
from telebot import types

from tolkien import TOKEN
from parsing import members, clan_war, clan_war_list, lcw, lcw_list, clan_games

bot = telebot.TeleBot(TOKEN)
"""
Атрибуты бота
name - 'StatBot (Beta)'
username (типо id) - '@ClashOfClansClanStatBot'
"""


clan_url = ""
command_list = "\n/reg - зарегать клан\n/clanmems - вывести информацио о игроках в клане\n/wars - список клановых войн\n/lwars - список войн лиги клановвых войн (beta)\n/badplayerslastcw - список игроков, которые не атаковали на последнием КВ\n/badplayerslastlcw - список игроков, которые не атаковали на последнием ЛКВ\n/badplayerscg - список игроков, которые не участвовали на ИК\nОстальные команды есть внутри подпунктов этих команд."
cw_command_list = "\nВыберите опцию\n/opencw - открыть КВ по номеру\n/badplayerscwbynum - найти неэффективных игроков на выбранном КВ"
lcw_command_list = "\nВыберите опцию\n/openlcw - открыть ЛКВ по номеру\n/back - назад"
lcw_rounds_command_list = "\nВыберите опцию\n/openround - открыть раунд ЛКВ по номеру\n/badplayersroundbynum - найти неэффективных игроков на выбранном раунде ЛКВ\n/back - назад"

site_tabs = {
    "home": "/view/home-village",
    "clanWars": "/wars/home-village",
    "lClanWars": "/clan-war-leagues/home-village",
}

war_list = []
l_war_list = []
l_war_rounds = []


@bot.message_handler(content_types=["text"])
def start(message):
    match message.text:
        case "/reg":
            bot.send_message(
                message.from_user.id,
                "Скинь id своего клана. Его можно посмотреть в игре на странице клана",
            )
            bot.register_next_step_handler(message, get_clan_id)

        case "/clanmems":
            cur_mems = members.get_my_current_clan_members(clan_url + site_tabs["home"])
            if not isinstance(cur_mems, str):
                s = ""
                for i in cur_mems:
                    s += i["nickname"] + " | Звание: " + i["role"] + "\n"
                bot.send_message(message.from_user.id, s)
            else:
                print(cur_mems)

        case "/wars":
            bot.send_message(message.from_user.id, "Ща оформим")
            global war_list
            war_list = clan_war_list.get_wars(clan_url + site_tabs["clanWars"])
            if not isinstance(war_list, str):
                s = ""
                index = 1
                for i in war_list:
                    s += f'#{index}| {i["clan1Name"]} VS {i["clan2Name"]}\n├──Размер: {i["warSize"]} Результат: {i["warWinLose"]}\n└──Итоги: {i["clan1Percent"]} {i["clan1Stars"]} |:| {i["clan2Percent"]} {i["clan2Stars"]}\nДата: {i["clan2Stars"]} {i["warHour"]}'
                    index += 1
                bot.send_message(message.from_user.id, s)
                bot.send_message(message.from_user.id, cw_command_list)
                bot.register_next_step_handler(message, work_with_cw)
            else:
                print(war_list)
                war_list = []

        case "/lwars":
            bot.send_message(message.from_user.id, "Ща оформим")
            global l_war_list
            l_war_list = lcw_list.get_lcw_wars(clan_url + site_tabs["lClanWars"])
            if not isinstance(l_war_list, str):
                s = ""
                index = 1

                for i in l_war_list:
                    s += f"#{index}| {i['month']}\n├──Результат: {i['result']}, {i['league']}, {i['rank']}-е место\n├──Размер: {i['size']}\n├──★: {i['stars']} Разрушение: {i['destruction']}\n├──Побед: {i['victories']} Поражений: {i['defeats']} Draws: {i['draws']}\n└──Состояние: {i['state']}\n"
                    index += 1
                bot.send_message(message.from_user.id, s)
                bot.send_message(message.from_user.id, lcw_command_list)
                bot.register_next_step_handler(message, work_with_lcw)
            else:
                print(l_war_list)
                l_war_list = []

        case "/badplayerslastcw":
            last_cw = clan_war.get_cw_units(
                clan_war_list.get_wars(clan_url + site_tabs["clanWars"])[0]["href"]
            )
            if not isinstance(last_cw, str):
                s = ""
                for i in last_cw:
                    if i["attackList"][0] == "no attacks":
                        s += f"{i['position']}. {i['nickname']}\n"
                bot.send_message(message.from_user.id, s)
            else:
                print(last_cw)

        case "/badplayerslastlcw":
            last_lcw = lcw.get_lcw_rounds(
                lcw_list.get_lcw_wars(clan_url + site_tabs["lClanWars"])[0]["href"]
            )
            if not isinstance(last_lcw, str):
                for i in last_lcw:
                    round_cw_units = clan_war.get_cw_units(i["href"])
                    s = "------" + i["round"] + "------\n"
                    for j in round_cw_units:
                        if j["attackList"][0] == "no attacks":
                            s += f"{j['position']}. {j['nickname']}\n"
                    bot.send_message(message.from_user.id, s)

                bot.send_message(message.from_user.id, "Подсчет окончен")
            else:
                print(last_lcw)

        case "/badplayerscg":
            bot.send_message(message.from_user.id, "Пака не работает, падажжи")

        case _:
            bot.send_message(
                message.from_user.id,
                "Вот список команд короче, а то чето ты не то вводишь" + command_list,
            )


def get_clan_id(message):
    global clan_url
    clan_url = "https://clashspot.net/en/clan/" + message.text
    bot.send_message(message.from_user.id, "Оке, вот кто есть в клане")

    cur_mems = members.get_my_current_clan_members(clan_url + site_tabs["home"])
    if not isinstance(cur_mems, str):
        s = ""
        for i in cur_mems:
            s += i["nickname"] + " | Звание:" + i["role"] + "\n"
        print(s)
        bot.send_message(message.from_user.id, s)
    else:
        print(cur_mems)


def work_with_cw(message):
    global war_list
    match message.text:
        case "/opencw":
            bot.send_message(message.from_user.id, "Введи номер КВ")
            bot.register_next_step_handler(message, work_with_cw_opencw)
        case "/badplayerscwbynum":
            bot.send_message(message.from_user.id, "Введи номер КВ")
            bot.register_next_step_handler(message, work_with_cw_badplayerscwbynum)
        case _:
            bot.send_message(
                message.from_user.id, "Что-то ты не то вводишь\n" + cw_command_list
            )
            bot.register_next_step_handler(message, work_with_cw)
            return


def work_with_cw_opencw(message):
    global war_list
    if not message.text.isdigit():
        bot.send_message(
            message.from_user.id,
            "Что-то ты не то вводишь. Я не воспринимаю это сообщение как число",
        )
        bot.register_next_step_handler(message, work_with_cw_opencw)
        return
    elif int(message.text) < 1 or int(message.text) > len(war_list):
        bot.send_message(
            message.from_user.id,
            "Такого КВ нет",
        )
        bot.register_next_step_handler(message, work_with_cw_opencw)
        return

    ind = int(message.text)
    ind -= 1
    cw_units = clan_war.get_cw_units(war_list[ind]["href"])
    if not isinstance(cw_units, str):
        s = ""
        for i in cw_units:
            s += f"{i['position']}| {i['nickname']} Атак: {i['attackCount']}\n"

            attack_list = i["attackList"]
            if attack_list[0] != "no attacks":
                for i in range(len(attack_list)):
                    s += f"└──{attack_list[i]['enemyPosition']}| {attack_list[i]['enemyNickname']} {beautify_stars(attack_list[i]['stars'])} {attack_list[i]['attackPercent']}\n"
        bot.send_message(message.from_user.id, s)
    else:
        print(cw_units)


def work_with_cw_badplayerscwbynum(message):
    global war_list
    if not message.text.isdigit():
        bot.send_message(
            message.from_user.id,
            "Что-то ты не то вводишь. Я не воспринимаю это сообщение как число",
        )
        bot.register_next_step_handler(message, work_with_cw_opencw)
        return
    elif int(message.text) < 1 or int(message.text) > len(war_list):
        bot.send_message(
            message.from_user.id,
            "Такого КВ нет",
        )
        bot.register_next_step_handler(message, work_with_cw_opencw)
        return

    ind = int(message.text)
    ind -= 1
    cw_units = clan_war.get_cw_units(war_list[ind]["href"])
    if not isinstance(cw_units, str):
        s = ""
        for i in cw_units:
            if i["attackList"][0] == "no attacks":
                s += f"{i['position']}. {i['nickname']}\n"
        bot.send_message(message.from_user.id, s)
    else:
        print(cw_units)


def work_with_lcw(message):
    match message.text:
        case "/openlcw":
            bot.send_message(message.from_user.id, "Введи номер ЛКВ")
            bot.register_next_step_handler(message, work_with_lcw_openlcw)
        case "/back":
            bot.send_message(message.from_user.id, command_list)
            bot.register_next_step_handler(message, start)
        case _:
            bot.send_message(
                message.from_user.id, "Что-то ты не то вводишь\n" + lcw_command_list
            )
            bot.register_next_step_handler(message, work_with_lcw)
            return


def work_with_lcw_openlcw(message):
    global l_war_list
    global l_war_rounds
    if not message.text.isdigit():
        bot.send_message(
            message.from_user.id,
            "Что-то ты не то вводишь. Я не воспринимаю это сообщение как число",
        )
        bot.register_next_step_handler(message, work_with_lcw_openlcw)
        return
    elif int(message.text) < 1 or int(message.text) > len(l_war_list):
        bot.send_message(
            message.from_user.id,
            "Такого ЛКВ нет",
        )
        bot.register_next_step_handler(message, work_with_lcw_openlcw)
        return

    ind = int(message.text)
    ind -= 1
    l_war_rounds = lcw.get_lcw_rounds(l_war_list[ind]["href"])
    if not isinstance(l_war_rounds, str):
        s = ""
        index = 1
        for i in l_war_rounds:
            s += f"#{index}| {i['round']}\n├──{i['clan1']} Атак: {i['clan1Attacks']} Звезд: {i['clan1Stars']}\n└──{i['clan2']} Атак: {i['clan2Attacks']} Звезд: {i['clan2Stars']}\n"
            index += 1
        bot.send_message(message.from_user.id, s)
        bot.send_message(message.from_user.id, lcw_rounds_command_list)
        bot.register_next_step_handler(message, work_withlcw_rounds)
    else:
        print(l_war_rounds)
        l_war_rounds = []


def work_withlcw_rounds(message):
    match message.text:
        case "/openround":
            bot.send_message(message.from_user.id, "Введи номер раунда ЛКВ")
            bot.register_next_step_handler(message, work_with_lcw_openround)
        case "/badplayersroundbynum":
            bot.send_message(message.from_user.id, "Введи номер раунда ЛКВ")
            bot.register_next_step_handler(
                message, work_withlcw_rounds_badplayersroundbynum
            )
        case "/back":
            bot.register_next_step_handler(message, work_with_lcw_openlcw)
        case _:
            bot.send_message(
                message.from_user.id,
                "Что-то ты не то вводишь\n" + lcw_rounds_command_list,
            )
            bot.register_next_step_handler(message, work_withlcw_rounds)
            return


def work_with_lcw_openround(message):
    global l_war_rounds
    if not message.text.isdigit():
        bot.send_message(
            message.from_user.id,
            "Что-то ты не то вводишь. Я не воспринимаю это сообщение как число",
        )
        bot.register_next_step_handler(message, work_with_lcw_openround)
        return
    elif int(message.text) < 1 or int(message.text) > len(l_war_rounds):
        bot.send_message(
            message.from_user.id,
            "Такого раунда нет",
        )
        bot.register_next_step_handler(message, work_with_lcw_openround)
        return

    ind = int(message.text)
    ind -= 1
    cw_units = clan_war.get_cw_units(l_war_rounds[ind]["href"])
    if not isinstance(cw_units, str):
        s = ""
        for i in cw_units:
            s += f"{i['position']}| {i['nickname']} Атак: {i['attackCount']}\n"

            attack_list = i["attackList"]
            if attack_list[0] != "no attacks":
                for i in range(len(attack_list)):
                    s += f"└──{attack_list[i]['enemyPosition']}| {attack_list[i]['enemyNickname']} {beautify_stars(attack_list[i]['stars'])} {attack_list[i]['attackPercent']}\n"
        bot.send_message(message.from_user.id, s)
    else:
        print(cw_units)


def work_withlcw_rounds_badplayersroundbynum(message):
    global l_war_rounds
    if not message.text.isdigit():
        bot.send_message(
            message.from_user.id,
            "Что-то ты не то вводишь. Я не воспринимаю это сообщение как число",
        )
        bot.register_next_step_handler(
            message, work_withlcw_rounds_badplayersroundbynum
        )
        return
    elif int(message.text) < 1 or int(message.text) > len(l_war_rounds):
        bot.send_message(
            message.from_user.id,
            "Такого раунда нет",
        )
        bot.register_next_step_handler(
            message, work_withlcw_rounds_badplayersroundbynum
        )
        return

    ind = int(message.text)
    ind -= 1
    cw_units = clan_war.get_cw_units(l_war_rounds[ind]["href"])
    if not isinstance(cw_units, str):
        s = ""
        for i in cw_units:
            if i["attackList"][0] == "no attacks":
                s += f"{i['position']}. {i['nickname']}\n"
        bot.send_message(message.from_user.id, s)
    else:
        print(cw_units)


def beautify_stars(stars):
    """
    ★★★
    ✰✰✰
    """

    match stars:
        case 0:
            return "✰✰✰"
        case 1:
            return "★✰✰"
        case 2:
            return "★★✰"
        case 3:
            return "★★★"


bot.polling(none_stop=True)
