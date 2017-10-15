import libtcodpy as libtcod

def load_customfont():
    a = 256

    for y in range(5,6):
        libtcod.console_map_ascii_codes_to_font(a, 16, 0, y)
        a += 16
