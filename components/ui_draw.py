import libtcodpy as libtcod

def draw_window_borders(window, width, height, color=libtcod.white):
    for x in width:
        libtcod.console_put_char(window, x, height, libtcod.CHAR_HLINE=196, libtcod.BKGND_NONE)
        libtcod.console_put_char(window, x, 0, libtcod.CHAR_HLINE=196, libtcod.BKGND_NONE)
