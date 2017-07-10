import libtcodpy as libtcod
from input_handlers import handle_keys
from entity import Entity
from entity import Adventurer
from render_function import render_all, clear_all
from map_objects.game_map import GameMap
from map_objects.mapstartingconfig import mapconfig

#fonction main Check if the module is ran as main program (name devient main).
#Si ce fichier est importé d'un autre module, name sera le nom du module
def main():


    colors = {
        'dark_wall': libtcod.Color(128, 128, 128),
        'dark_ground': libtcod.Color(0, 0, 0)
    }


    player = Adventurer(int(mapconfig['screen_width']/ 2), int(mapconfig['screen_height'] / 2), '@', libtcod.purple)
    npc = Entity(int(mapconfig['screen_width'] / 2 - 5), int(mapconfig['screen_height'] / 2), '@', libtcod.yellow)
    entities = [npc, player]


    libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
#What create the screen (Width, Height, Nom, Fullscreen)
    libtcod.console_init_root(mapconfig['screen_width'], mapconfig['screen_height'], 'Eolandia', False)
#Console principale?
    con = libtcod.console_new(mapconfig['screen_width'], mapconfig['screen_height'])
#Initialise la Game map
    game_map = GameMap(mapconfig['map_width'], mapconfig['map_height'])
    game_map.make_map(mapconfig['max_rooms'], mapconfig['room_min_size'], mapconfig['room_max_size'], mapconfig['map_width'], mapconfig['map_height'], player)

    key = libtcod.Key()
    mouse = libtcod.Mouse()
#boucle qui se finit pas
    while not libtcod.console_is_window_closed():
#Function that capture new event
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)
#Pour afficher les PV
        hpList = list(map(lambda i: Entity(29 + i, 48, '/', libtcod.red), range(player.HP)))
        entitiestorender = entities + hpList

#Function that draws entities
        render_all(con, entitiestorender, game_map, colors)
        libtcod.console_flush()
#Clear les entities pour que ça ne laisse pas de traces
        clear_all(con, entitiestorender)
#Partie pour bouger. Apelle le fichier Handle keys.
#Return des dictionary.Ces valeurs vont dans la variable action
#Action contiendras des clés (move, exit, or fullscre)
        action = handle_keys(key)

        move = action.get('move')
        exiting = action.get('exit')
        fullscreen = action.get('fullscreen')
        hurt = action.get('hurt')

        if move:
            dx, dy = move
            if not game_map.is_blocked(player.x + dx, player.y + dy):
                player.move(dx, dy)

        if hurt:
            player.HP += -1


        elif exiting:
            return True

        elif fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())


if __name__ == '__main__':
    main()
