import os
import readchar
import random

# Positions Constants.
POS_X = 0
POS_Y = 1
# Size Map Constants.
MAP_WIDTH = 20
MAP_HEIGHT = 15
NUM_OF_OBJECTS = 10

# Variables
my_position = [1, 1]
tail_length = 0
tail = []
map_objects = []
created_objects = 0
dead = False
end_game = False

obstacle_definition = '''\
####################
#   ##     ###     #
# ##   ###     ##  #
#    ##    ##      #
###      ####   ####
#   ####       ##  #
# ##    ## ###     #
#    ##        ### #
#  ####   ##       #
#    ##     ## ### #
###     ####     ###
#   ##       ##    #
# ##    ####    ## #
#     ##    ##     #
####################\
'''

# Create obstacle map
obstacle_definition = [list(row) for row in obstacle_definition.split("\n")]

# Main Loop
while not end_game:
    os.system('cls')
    # Generate random objects coordinates
    while len(map_objects) < 1:
        new_position = [random.randint(0, MAP_WIDTH - 1), random.randint(0, MAP_HEIGHT - 1)]
        if (new_position not in map_objects and new_position != my_position and
                obstacle_definition[new_position[POS_Y]][new_position[POS_X]] != "#"):
            map_objects.append(new_position)
            created_objects += 1
    # Draw Map
    print("+" + "-" * MAP_WIDTH * 3 + "+")
    for coordinate_y in range(MAP_HEIGHT):
        print("|", end="")
        # Draw Player on map.
        for coordinate_x in range(MAP_WIDTH):
            char_to_draw = " "
            object_in_cell = None
            tail_in_cell = None
            # Draw position object
            for map_object in map_objects:
                if map_object[POS_X] == coordinate_x and map_object[POS_Y] == coordinate_y:
                    char_to_draw = "*"
                    object_in_cell = map_object
            # Draw Tail last position head.
            for tail_piece in tail:
                if tail_piece[POS_X] == coordinate_x and tail_piece[POS_Y]== coordinate_y:
                    char_to_draw = "@"
                    tail_in_cell = tail_piece
            # Draw position player
            if my_position[POS_X] == coordinate_x and my_position[POS_Y] == coordinate_y:
                char_to_draw = "@"
                if object_in_cell:
                    map_objects.remove(object_in_cell)
                    tail_length += 1
                    if created_objects < NUM_OF_OBJECTS:
                        while True:
                            new_object = [random.randint(0, MAP_WIDTH - 1), random.randint(0, MAP_HEIGHT - 1)]
                            if (new_object != my_position and new_object not in tail and
                                    obstacle_definition[new_object[POS_Y]][new_object[POS_X]] != "#"):
                                map_objects.append(new_object)
                                created_objects += 1
                                break
                if tail_in_cell:
                    char_to_draw = "x"
                    end_game = True
                    dead = True
                if created_objects == NUM_OF_OBJECTS and len(map_objects) == 0:
                    end_game =True

            if obstacle_definition[coordinate_y][coordinate_x] == "#":
                char_to_draw = "#"

            print(" {} ".format(char_to_draw), end="")
        print("|")
    print("+" + "-" * MAP_WIDTH * 3 + "+")

    # Instructions of Game.
    print("\nUsa [W]🡡[A]🡣[S]🡠[D]🡢 para moverte, [Q] para salir.\n")

    # End Game Message.
    if end_game:
        if dead:
            print("\n💥 Has muerto al tocar tu propia cola.")
            print("Game Over.Tu Puntuación es: {}\n".format(tail_length))
        else:
            print("\nEnhorabuena! Has recogido toda la comida!")
            print("Tu Puntuación final es: {}\n".format(tail_length))
        input("Pulsa Enter para salir...")
        break

    # Assign W, A, S, D to move the player.
    direction = readchar.readchar()
    new_position = None
    if direction == "w":
        new_position = [my_position[POS_X], (my_position[POS_Y] - 1) % MAP_HEIGHT]

    elif direction == "s":
        new_position = [my_position[POS_X], (my_position[POS_Y] + 1) % MAP_HEIGHT]

    elif direction == "a":
        new_position = [(my_position[POS_X] - 1) % MAP_WIDTH, my_position[POS_Y]]

    elif direction == "d":
        new_position = [(my_position[POS_X] + 1) % MAP_WIDTH, my_position[POS_Y]]

    elif direction == "q":
        end_game = True

    if new_position:
        if obstacle_definition[new_position[POS_Y]][new_position[POS_X]] != "#":
            tail.insert(0, my_position.copy())
            tail = tail[:tail_length]
            my_position = new_position
    os.system('cls')