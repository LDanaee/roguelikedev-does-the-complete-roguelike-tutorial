import libtcodpy as libtcod
from enum import Enum
from custom_fontthing import load_customfont

class RenderOrder(Enum):
    CORPSE = 1
    ITEM = 2
    ACTOR = 3

def get_names_under_mouse(mouse, entities, fov_map):
    (x, y) = (mouse.cx, mouse.cy)

    names = [entity.name for entity in entities
             if entity.x == x and entity.y == y and libtcod.map_is_in_fov(fov_map, entity.x, entity.y)]
    names = ', '.join(names)

    return names.capitalize()

def render_bar(panel, x, y, total_width, name, value, maximum, bar_color, back_color):
    bar_width = int(float(value) / maximum * total_width)

    libtcod.console_set_default_background(panel, back_color)
    libtcod.console_rect(panel, x, y, total_width, 1, False, libtcod.BKGND_SCREEN)

    libtcod.console_set_default_background(panel, bar_color)
    if bar_width > 0:
        libtcod.console_rect(panel, x, y, bar_width, 1, False, libtcod.BKGND_SCREEN)

    libtcod.console_set_default_foreground(panel, libtcod.white)
    libtcod.console_print_ex(panel, int(x + total_width / 2), y, libtcod.BKGND_NONE, libtcod.CENTER,
                             '{0}: {1}/{2}'.format(name, value, maximum))

def render_all(con, panel, card_panel, entities, player, game_map, fov_map, fov_recompute, message_log, screen_width, screen_height, bar_width, panel_height, panel_y, card_panel_height, card_panel_y, mouse, colors, cardslots):
    load_customfont()
    wall_tile = 256
    floor_tile = 257
    player_tile = 258
    orc_tile = 259
    troll_tile = 260
    scroll_tile = 261
    healingpotion_tile = 262
    sword_tile = 263
    shield_tile = 264
    stairsdown_tile = 265
    dagger_tile = 266
    if fov_recompute:
        # Draw all the tiles in the game map
        for y in range(game_map.height):
            for x in range(game_map.width):
                visible = libtcod.map_is_in_fov(fov_map, x, y)
                wall = game_map.tiles[x][y].block_sight
                if visible:
                    if wall:
                        libtcod.console_put_char_ex(con, x, y, wall_tile, libtcod.purple, libtcod.black)
                    else:
                        libtcod.console_put_char_ex(con, x, y, floor_tile, libtcod.white, libtcod.black)
                    game_map.tiles[x][y].explored = True
                elif game_map.tiles[x][y].explored:
                    if wall:
                        libtcod.console_put_char_ex(con, x, y, wall_tile, libtcod.violet, libtcod.black)
                    else:#if not draw floor
                        libtcod.console_put_char_ex(con, x, y, floor_tile, libtcod.grey, libtcod.black)

    # Draw all entities in the list
    entities_in_render_order = sorted(entities, key=lambda x: x.render_order.value)
    for entity in entities_in_render_order:
        draw_entity(con, entity, fov_map)
#blits???
    libtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)

    libtcod.console_set_default_background(panel, libtcod.black)
    libtcod.console_clear(panel)
    libtcod.console_set_default_background(card_panel, libtcod.black)
    libtcod.console_clear(card_panel)


    libtcod.console_print_frame(con, 0, 0, 80, 43, False, libtcod.BKGND_SET, None)
    libtcod.console_print_frame(panel, 0, 0, 39, 15, False, libtcod.BKGND_SET, None)
    render_bar(panel, 1, 1, bar_width, 'HP', player.fighter.hp,
    player.fighter.max_hp, libtcod.light_red, libtcod.darker_red)
    libtcod.console_set_default_foreground(panel, libtcod.light_gray)
    libtcod.console_print_ex(panel, 1, 0, libtcod.BKGND_NONE, libtcod.LEFT, get_names_under_mouse(mouse, entities, fov_map))
    libtcod.console_print_frame(card_panel, 0, 0, 80, 7, False, libtcod.BKGND_SET, 'Cards')
    for i in range(cardslots) :
        j = (80//cardslots) - 1
        libtcod.console_print_frame(card_panel, (i*j) + 1, 1, j, 5, False, libtcod.BKGND_SET, None)
        # Print the game messages, one line at a time
    y = 3
    for message in message_log.messages:
        libtcod.console_set_default_foreground(panel, message.color)
        libtcod.console_print_ex(panel, message_log.x, y, libtcod.BKGND_NONE, libtcod.LEFT, message.text)
        y += 1
    libtcod.console_blit(panel, 0, 0, screen_width, panel_height, 0, 80, panel_y)
    libtcod.console_blit(card_panel, 0, 0, screen_width, card_panel_height, 0, 0, card_panel_y)






def clear_all(con, entities):
    for entity in entities:
        clear_entity(con, entity)

#function qui draw duh
def draw_entity(con, entity, fov_map):
    if libtcod.map_is_in_fov(fov_map, entity.x, entity.y):
        libtcod.console_set_default_foreground(con, entity.color)
        libtcod.console_put_char(con, entity.x, entity.y, entity.char, libtcod.BKGND_NONE)


def clear_entity(con, entity):
    # erase the character that represents this object
    libtcod.console_put_char(con, entity.x, entity.y, ' ', libtcod.BKGND_NONE)
