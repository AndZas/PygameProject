def read_settings():
    with open('settings') as file:
        data = file.read().split(';')
        in_tamer_on_off, hide_HUD_on_off = [True if i == 'True' else False for i in data[2:4]]
        sound_effct, music, = list(map(float, data[0:2]))
        lvl = int(data[-1])
    return sound_effct, music, in_tamer_on_off, hide_HUD_on_off, lvl
