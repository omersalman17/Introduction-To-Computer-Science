############################################################################
# FILE : board.py
# WRITER : Omer Salman
# EXERCISE : intro2cs1 ex9 2018-2019
"""DESCRIPTION: a program that defines the object Board for the game
"rush hour\""""
############################################################################


class Board:
    """
    the purpose of the class Board is to create a Board type object with
     suitable methods for the game "rush hour"
    """

    def __init__(self):
        # Note that this function is required in your Board implementation.
        # However, is not part of the API for general board types.

        self.matrix = [['*', '*', '*', '*', '*', '*', '*'],
                       ['*', '*', '*', '*', '*', '*', '*'],
                       ['*', '*', '*', '*', '*', '*', '*'],
                       ['*', '*', '*', '*', '*', '*', '*', '*'],
                       ['*', '*', '*', '*', '*', '*', '*'],
                       ['*', '*', '*', '*', '*', '*', '*'],
                       ['*', '*', '*', '*', '*', '*', '*']]
        self.car_lst = []

    def __str__(self):
        """
        This function is called when a board object is to be printed.
        :return: A string of the current status of the board
        """
        # The game may assume this function returns a reasonable representation
        # of the board for printing, but may not assume details about it.
        returned = ''
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                returned += self.matrix[i][j] + ' '
                if j == len(self.matrix[i]) - 1:
                    returned += "\n"
                    break
        return returned

    def cell_list(self):
        """ This function returns the coordinates of cells in this board
        :return: list of coordinates
        """
        # In this board, returns a list containing the cells in the square
        # from (0,0) to (6,6) and the target cell (3,7)
        returned_cell_list = []
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                returned_cell_list.append((i, j))
        return returned_cell_list

    def possible_moves(self):
        """ This function returns the legal moves of all cars in this board
        :return: list of tuples of the form (name,movekey,description)
                 representing legal moves
        """
        # From the provided example car_config.json file, the return value could be
        # [('O','d',"some description"),('R','r',"some description"),('O','u',"some description")]

        possible_moves_lst = []
        VERTICAL = 0
        HORIZONTAL = 1
        for car in self.car_lst:
            # print(car.get_name())
            car_first_coo = car.car_coordinates()[0]
            car_second_coo = car.car_coordinates()[1]
            car_name = car.get_name()
            if car_first_coo[0] == car_second_coo[0]:
                car_orientation = HORIZONTAL
            else:
                car_orientation = VERTICAL
            req_move_left = car.movement_requirements('l')[0]
            req_move_right = car.movement_requirements('r')[0]
            req_move_up = car.movement_requirements('u')[0]
            req_move_down = car.movement_requirements('d')[0]
            if car_orientation == HORIZONTAL:
                if req_move_right[1] < len(self.matrix[req_move_right[0]]):
                    if self.cell_content(req_move_right) is None:
                        possible_moves_lst.append((car_name, 'r', "one step right"))
                if req_move_left[1] >= 0:
                    if self.cell_content(req_move_left) is None:
                        possible_moves_lst.append((car_name, 'l', "one step left"))
            else:
                if req_move_down[0] < len(self.matrix):
                    if self.cell_content(req_move_down) is None:
                        possible_moves_lst.append((car_name, 'd', "one step down"))
                if req_move_up[0] >= 0:
                    if self.cell_content(req_move_up) is None:
                        possible_moves_lst.append((car_name, 'u', "one step up"))
        return possible_moves_lst

    def target_location(self):
        """
        This function returns the coordinates of the location which is to be filled for victory.
        :return: (row,col) of goal location
        """
        # In this board, returns (3,7)
        return 3, 7

    def cell_content(self, coordinate):
        """
        Checks if the given coordinates are empty.
        :param coordinate: tuple of (row,col) of the coordinate to check
        :return: The name if the car in coordinate, None if empty
        """
        row = coordinate[0]
        col = coordinate[1]
        if self.matrix[row][col] != "*":
            return self.matrix[row][col]
        else:
            return None

    def add_car(self, car):
        """
        Adds a car to the game.
        :param car: car object of car to add
        :return: True upon success. False if failed
        """
        # Remember to consider all the reasons adding a car can fail.
        # You may assume the car is a legal car object following the API.

        car2_name = car.get_name()
        for car1 in self.car_lst:
            if car1.get_name() == car2_name:
                return False
        for i in range(len(car.car_coordinates())):
            if self.cell_content(car.car_coordinates()[i]) is not None:
                return False
        for i in range(len(car.car_coordinates())):
            vertical_coo = car.car_coordinates()[i][0]
            horizontal_coo = car.car_coordinates()[i][1]
            car_name = car.get_name()
            self.matrix[vertical_coo][horizontal_coo] = car_name
        if car not in self.car_lst:
            self.car_lst.append(car)
        return True

    def move_car(self, name, movekey):
        """
        moves car one step in given direction.
        :param name: name of the car to move
        :param movekey: Key of move in car to activate
        :return: True upon success, False otherwise
        """
        possible_cars_moves = []
        for i in range(len(self.possible_moves())):
            possible_cars_moves.append(self.possible_moves()[i][:2])
        move = (name, movekey)
        if move not in possible_cars_moves:
            return False
        else:
            for car in self.car_lst:
                if car.get_name() != name:
                    continue
                if movekey == "d":
                    car_change_row_coo = car.car_coordinates()[0][0]
                    car_change_col_coo = car.car_coordinates()[0][1]
                elif movekey == "u":
                    car_change_row_coo = car.car_coordinates()[-1][0]
                    car_change_col_coo = car.car_coordinates()[-1][1]
                elif movekey == "r":
                    car_change_row_coo = car.car_coordinates()[0][0]
                    car_change_col_coo = car.car_coordinates()[0][1]
                elif movekey == "l":
                    car_change_row_coo = car.car_coordinates()[-1][0]
                    car_change_col_coo = car.car_coordinates()[-1][1]
                self.matrix[car_change_row_coo][car_change_col_coo] = "*"
                movement = car.movement_requirements(movekey)[0]
                row_coo = movement[0]
                col_coo = movement[1]
                self.matrix[row_coo][col_coo] = name
                car.move(movekey)
                return True
