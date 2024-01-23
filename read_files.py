import json


def read_settings():
    # Читает данные из файла settings
    with open('files_txt_json_db/settings') as file:
        data = file.read().split(';')
        in_tamer_on_off, hide_HUD_on_off = [True if i == 'True' else False for i in data[2:4]]
        sound_effct, music = list(map(float, data[0:2]))
    return sound_effct, music, in_tamer_on_off, hide_HUD_on_off


def read_lvl():
    # Читает последний выбранный лвл
    with open('files_txt_json_db/lvl.txt') as file:
        data = int(file.read())
    return data


def dump_lvl(lvl):
    # После перехода на новый уровень записывает в файл этот уровень
    with open('files_txt_json_db/lvl.txt', 'w') as file:
        file.write(str(lvl))


def restart_lvl():
    # Сбрасывает лвл
    with open('files_txt_json_db/lvl.txt', 'w') as file:
        file.write('0')


def read_json_file():
    # Читает данные из файла json
    with open('files_txt_json_db/prices_and_player.json', encoding='utf-8') as file:
        data = json.load(file)
    profile_player = data['Player']
    prices = data['Prices']

    player_speed, player_wall_punch = profile_player.values()
    speed_price, hp_price, wall_punch_price = prices.values()
    return [player_speed, player_wall_punch], [speed_price, hp_price, wall_punch_price]


def dump_json_file(dct=None):
    # Сброс настроек json файла
    if dct is None:
        dct = {"Player": {"speed": 0.75, "wall punch": 30},
               "Prices": {"speed": 10, "hp": 10, "wall punch": 10}}
    with open('files_txt_json_db/prices_and_player.json', 'w') as file:
        json.dump(dct, file, ensure_ascii=False, indent=4)


def read_money_and_health():
    # Возвращает количество здоровья и денег в данный момент
    with open('files_txt_json_db/money_health') as file:
        money, health = map(int, file.read().split(';'))
    return money, health


def dump_money_and_health(money, health):
    # Сброс здоровья и денег
    with open('files_txt_json_db/money_health', 'w') as file:
        file.write(str(money) + ';' + str(health))
