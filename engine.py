import libtcodpy as libtcod
from input_handlers import handle_keys
from entity import Entity, get_blocking_entities_at_location
from render_function import render_all, clear_all, RenderOrder, render_bar
from map_objects.game_map import GameMap
from fov_functions import initialize_fov, recompute_fov
from game_states import GameStates
from components.fighter import Fighter
from components.death_function import kill_player, kill_monster
from game_messages import MessageLog, Message

#fonction main Check if the module is ran as main program (name devient main).
#Si ce fichier est importé d'un autre module, name sera le nom du module
def main():
#Carac de l'écran
    screen_width = 120
    screen_height = 50
    map_width = 80
    map_height = 43

#Carac des barres
    bar_width = 20
    panel_height = 8
    panel_y = 1
    panel_width = screen_width - map_width
    card_panel_height = 7
    card_panel_y = screen_height - card_panel_height
#Message box
    message_x = panel_y
    message_width = panel_width
    message_height = panel_height - 1

#Minimum de la room
    room_max_size = 15
    room_min_size = 6
    max_rooms = 30

    fov_algorithm = 1
    fov_light_walls = True
    fov_radius = 10

    max_monsters_per_room = 3
    cardslots = 6


    colors = {
        'dark_wall': libtcod.Color(51, 0, 25),
        'dark_ground': libtcod.Color(0, 51, 51),
        'light_wall': libtcod.Color(255, 0, 127),
        'light_ground': libtcod.Color(0, 153, 153)
    }

    fighter_component = Fighter(hp=30, defense=2, power=5)
    player = Entity(0, 0, '@', libtcod.white, 'Player', blocks=True, render_order=RenderOrder.ACTOR, fighter=fighter_component)
    entities = [player]


    libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
#What create the screen (Width, Height, Nom, Fullscreen)
    libtcod.console_init_root(screen_width, screen_height, 'Eolandia', False)
#Console principale?
    con = libtcod.console_new(screen_width, screen_height)
#Message box
    panel = libtcod.console_new(panel_width, panel_height)
#Card box
    card_panel = libtcod.console_new(map_width, card_panel_height)
    windows = [con, panel, card_panel]
#Initialise la Game map
    game_map = GameMap(map_width, map_height)
    game_map.make_map(max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities, max_monsters_per_room)

    fov_recompute = True
    fov_map = initialize_fov(game_map)
    message_log = MessageLog(message_x, message_width, message_height)


    key = libtcod.Key()
    mouse = libtcod.Mouse()

    game_state = GameStates.PLAYERS_TURN
#boucle qui se finit pas
    while not libtcod.console_is_window_closed():
#Function that capture new event
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)

        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y, fov_radius, fov_light_walls, fov_algorithm)
#Function that draws entities
        render_all(con, panel, card_panel, entities, player, game_map, fov_map, fov_recompute, message_log, screen_width,
                   screen_height, bar_width, panel_height, panel_y, card_panel_height, card_panel_y, mouse, colors, cardslots)

        fov_recompute = False

        libtcod.console_flush()
#Clear les entities pour que ça ne laisse pas de traces
        clear_all(con, entities)
#Partie pour bouger. Apelle le fichier Handle keys.
#Return des dictionary.Ces valeurs vont dans la variable action
#Action contiendras des clés (move, exit, or fullscre)
        action = handle_keys(key)

        move = action.get('move')
        exiting = action.get('exit')
        fullscreen = action.get('fullscreen')

        player_turn_results = []

        if move and game_state == GameStates.PLAYERS_TURN:
            dx, dy = move
            destination_x = player.x + dx
            destination_y = player.y + dy

            if not game_map.is_blocked(destination_x, destination_y):
                target = get_blocking_entities_at_location(entities, destination_x, destination_y)
                if target:
                    attack_results = player.fighter.attack(target)
                    player_turn_results.extend(attack_results)
                else:
                    player.move(dx, dy)

                    fov_recompute = True

                game_state = GameStates.ENEMY_TURN

        if exiting:
            return True

        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

        for player_turn_result in player_turn_results:
            message = player_turn_result.get('message')
            dead_entity = player_turn_result.get('dead')

            if message:
                message_log.add_message(message)

            if dead_entity:
                if dead_entity == player:
                    message, game_state = kill_player(dead_entity)
                else:
                    message = kill_monster(dead_entity)

                message_log.add_message(message)

        if game_state == GameStates.ENEMY_TURN:
            for entity in entities:
                if entity.ai:
                    enemy_turn_results = entity.ai.take_turn(player, fov_map, game_map, entities)

                    for enemy_turn_result in enemy_turn_results:
                        message = enemy_turn_result.get('message')
                        dead_entity = enemy_turn_result.get('dead')

                        if message:
                            message_log.add_message(message)

                        if dead_entity:
                            if dead_entity == player:
                                message, game_state = kill_player(dead_entity)
                            else:
                                message = kill_monster(dead_entity)

                            message_log.add_message(message)

                            if game_state == GameStates.PLAYER_DEAD:
                                break
                    if game_state == GameStates.PLAYER_DEAD:
                        break

            else:
                game_state = GameStates.PLAYERS_TURN


if __name__ == '__main__':
    main()
