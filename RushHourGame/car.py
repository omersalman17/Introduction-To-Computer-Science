############################################################################
# FILE : car.py
# WRITER : Omer Salman
# EXERCISE : intro2cs1 ex9 2018-2019
"""DESCRIPTION: a program that defines the object Car for the game
"rush hour\""""
############################################################################

VERTICAL = 0
HORIZONTAL = 1


class Car:
    """
    the purpose of the class Car is to create a Car type object with
     suitable methods for the game "rush hour"
    """

    def __init__(self, name, length, location, orientation):
        """
        A constructor for a Car object
        :param name: A string representing the car's name
        :param length: A positive int representing the car's length.
        :param location: A tuple representing the car's head (row, col) location
        :param orientation: One of either 0 (VERTICAL) or 1 (HORIZONTAL)
        """
        # Note that this function is required in your Car implementation.
        # However, is not part of the API for general car types.

        self.name = name
        self.length = length
        self.location = location
        self.orientation = orientation

    def car_coordinates(self):
        """
        :return: A list of coordinates the car is in
        """
        coordinates = []
        if self.orientation == VERTICAL:
            for i in range(self.length):
                coordinates.append((self.location[0] + i, self.location[1]))
        elif self.orientation == HORIZONTAL:
            for i in range(self.length):
                coordinates.append((self.location[0], self.location[1] + i))
        return coordinates

    def possible_moves(self):
        """
        :return: A dictionary of strings describing possible movements permitted by this car.
        """
        # For this car type, keys are from 'udrl'
        # The keys for vertical cars are 'u' and 'd'.
        # The keys for horizontal cars are 'l' and 'r'.
        # You may choose appropriate strings.

        # The dictionary returned should look something like this:
        # result = {'f': "cause the car to fly and reach the Moon",
        #          'd': "cause the car to dig and reach the core of Earth",
        #          'a': "another unknown action"}
        # A car returning this dictionary supports the commands 'f','d','a'.

        possible_moves_dic = {}
        VERTICAL = 0
        HORIZONTAL = 1
        if self.orientation == VERTICAL:
            possible_moves_dic['d'] = "car can move one square down"
            possible_moves_dic['u'] = "car can move one square up"
        elif self.orientation == HORIZONTAL:
            possible_moves_dic['r'] = "car can move one square right"
            possible_moves_dic['l'] = "car can move one square left"
        return possible_moves_dic

    def movement_requirements(self, movekey):
        """ 
        :param movekey: A string representing the key of the required move.
        :return: A list of cell locations which must be empty in order for this move to be legal.
        """
        # For example, a car in locations [(1,2),(2,2)] requires [(3,2)] to
        # be empty in order to move down (with a key 'd').

        movement_requirements_list = []
        first_row_coordinate = self.location[0]
        first_col_coordinate = self.location[1]
        car_last_coordinates = self.car_coordinates()[-1]
        last_row_coordinate = car_last_coordinates[0]
        last_col_coordinate = car_last_coordinates[1]
        if movekey == 'd':
            movement_requirements_list = [(last_row_coordinate + 1, self.location[1])]
        elif movekey == 'u':
            movement_requirements_list = [(first_row_coordinate - 1, self.location[1])]
        elif movekey == 'r':
            movement_requirements_list = [(self.location[0], last_col_coordinate + 1)]
        elif movekey == 'l':
            movement_requirements_list = [(self.location[0], first_col_coordinate - 1)]
        return movement_requirements_list

    def move(self, movekey):
        """ 
        :param movekey: A string representing the key of the required move.
        :return: True upon success, False otherwise
        """
        if self.orientation == 0:
            if movekey == 'u':
                self.location = (self.location[0] - 1, self.location[1])
                return True
            elif movekey == 'd':
                self.location = (self.location[0] + 1, self.location[1])
                return True
        elif self.orientation == 1:
            if movekey == 'r':
                self.location = (self.location[0], self.location[1] + 1)
                return True
            elif movekey == 'l':
                self.location = (self.location[0], self.location[1] - 1)
                return True
        return False

    def get_name(self):
        """
        :return: The name of this car.
        """
        return self.name
