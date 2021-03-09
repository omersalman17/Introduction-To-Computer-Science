############################################################################
# FILE : game.py
# WRITER : Omer Salman
# EXERCISE : intro2cs1 ex9 2018-2019
"""DESCRIPTION: a program that runs the game "rush hour" using command line
 and data given from a json file"""
############################################################################

import sys
import helper
import car
import board


class Game:
    """
    he purpose of the class Game is to create a Game type object with
     suitable methods for the game "rush hour".
    """

    def __init__(self, board):
        """
        Initialize a new Game object.
        :param board: An object of type board
        """
        # You may assume board follows the API

        self.game_board = board

    def __single_turn(self):
        """
        Note - this function is here to guide you and it is *not mandatory*
        to implement it. 

        The function runs one round of the game :
            1. Get user's input of: what color car to move, and what 
                direction to move it.
            2. Check if the input is valid.
            3. Try moving car according to user's input.

        Before and after every stage of a turn, you may print additional 
        information for the user, e.g., printing the board. In particular,
        you may support additional features, (e.g., hints) as long as they
        don't interfere with the API.
        """
        print("please input: (car to move),(direction)")
        user_input = input()
        car_name, direction, car_object = valid_turn_input(user_input)
        if self.game_board.move_car(car_name, direction):
            pass
        else:
            print("not legal move, try again.")
            self.__single_turn()

    def play(self):
        """
        The main driver of the Game. Manages the game until completion.
        :return: None
        """
        target_coordinate = self.game_board.target_location()
        target_content = self.game_board.cell_content(target_coordinate)
        while target_content is None:
            print(self.game_board)
            self.__single_turn()
            target_coordinate = self.game_board.target_location()
            target_content = self.game_board.cell_content(target_coordinate)
        print(self.game_board)
        print("you won!")


def valid_turn_input(user_input):
    """function checks if the user's input for this turn is valid, if it is,
     returns it. if it is not, asks for new input until a valid one is given"""
    while True:
        if len(user_input) == 3:
            if user_input[0] in filtered_cars_dictionary:
                car_name = user_input[0]
                if user_input[1] == ",":
                    for car in cars_lst:
                        if car.get_name() == car_name:
                            car_object = car
                            possible_moves_lst = car.possible_moves()
                            break
                    if user_input[2] in possible_moves_lst:
                        direction = user_input[2]
                        return car_name, direction, car_object
        print("invalid input, please enter again")
        user_input = input()


def check_cars_list(cars_dictionary, game_board):
    """
    function filters the cars dictionary loaded from the json file
    and returns a dictionary contains only valid cars according to the game
     rules.
    :param cars_dictionary: dictionary of Car objectss' values, each key in
     this dictionary presents a car name and the key value is the car's data
      (values).
    :param game_board: Board object presents the game_board
    """
    filtered_cars_dictionary = {}
    for key in cars_dictionary:
        car = cars_dictionary[key]
        if invalid_car_info(key, car, game_board):
            continue
        filtered_cars_dictionary[key] = car
    return filtered_cars_dictionary


def invalid_car_info(key, car, game_board):
    """
    function checks Car object values, returns True is it is valid according
     to the game rules, returns False if it is not.
    """
    car_properties = len(car)
    if car_properties != 3:
        return True
    else:
        car_name = key
        legal_car_names = ['Y', 'B', 'O', 'W', 'G', 'R']
        car_length = car[0]
        car_location = car[1]
        car_orientation = car[2]
        car_first_row_coo = car_location[0]
        car_first_col_coo = car_location[1]
        VERTICAL = 0
        HORIZONTAL = 1
        BOARD_LEN_INDEX = game_board.target_location()[1] - 1
        LAST_VERTICAL_CAR_INDEX = car_location[0] + car_length - 1
        LAST_HORIZONTAL_CAR_INDEX = car_location[1] + car_length - 1
        if car_name not in legal_car_names:
            return True
        elif car_first_col_coo < 0 or car_first_row_coo < 0:
            return True
        elif car_length > 4 or car_length < 2 or car_length < 0:
            return True
        elif len(car_location) != 2:
            return True
        elif car_orientation != VERTICAL and car_orientation != HORIZONTAL:
            return True
        elif car_orientation == VERTICAL:
            if LAST_VERTICAL_CAR_INDEX > BOARD_LEN_INDEX or \
                    LAST_VERTICAL_CAR_INDEX < 0:
                return True
        elif car_orientation == HORIZONTAL:
            if LAST_HORIZONTAL_CAR_INDEX > BOARD_LEN_INDEX or \
                    LAST_HORIZONTAL_CAR_INDEX < 0:
                return True
    return False


if __name__ == "__main__":

    # Your code here
    # All access to files, non API constructors, and such must be in this
    # section, or in functions called from this section.

    game_board = board.Board()
    cars_dictionary = helper.load_json(sys.argv[1])
    filtered_cars_dictionary = check_cars_list(cars_dictionary, game_board)
    cars_lst = []
    for key in filtered_cars_dictionary:
        car_length = filtered_cars_dictionary[key][0]
        car_coordinates = filtered_cars_dictionary[key][1]
        car_orientation = filtered_cars_dictionary[key][2]
        tmp_car = car.Car(key, car_length, car_coordinates, car_orientation)
        cars_lst.append(tmp_car)
        game_board.add_car(tmp_car)
    G = Game(game_board)
    G.play()
