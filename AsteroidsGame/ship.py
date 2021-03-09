#########################################################################
# FILE : ship.py
# WRITERS : Omer Salman, Ido Karniel
# EXERCISE :  2018-2019 intro2cs1 ex10 "Asteroid" game
# DESCRIPTION: A file that contain the class Ship for the game "Asteroid"
#########################################################################

import math


class Ship:
    """
    class Ship is the class that build ship objects for the game "Asteroid".
    """
    def __init__(self, x_axis_p, y_axis_p, x_speed=0, y_speed=0, direction=0):
        """
        init method for build Ship object.
        :param x_axis_p: the ship location in axis x.
        :param y_axis_p: the ship location in axis y.
        :param x_speed: the ship starts speed on x axis.
        :param y_speed: the ship starts speed on y axis.
        :param direction: the ship starts heading.
        """
        self.__x_axis = x_axis_p
        self.__y_axis = y_axis_p
        self.__X_speed = x_speed
        self.__y_speed = y_speed
        self.__direction = direction
        self.__lives = 3

    def get_axis_x(self):
        """
        get method for getting the X axis point.
        :return: the x axis.
        """
        return self.__x_axis

    def get_axis_y(self):
        """
        get method for getting the Y axis point.
        :return: the Y axis.
        """
        return self.__y_axis

    def get_direction(self):
        """
        get method for getting the ship heading.
        :return: the ship hading on degrees.
        """
        return self.__direction

    def get_speed_x(self):
        """
        get method for getting the X speed on axis.
        :return: the X speed on axis.
        """
        return self.__X_speed

    def get_speed_y(self):
        """
        get method for getting the Y speed on axis.
        :return: the Y speed on axis.
        """
        return self.__y_speed

    def get_life(self):
        """
        get method for getting the ship life.
        :return: the ship lives
        :type: int
        """
        return self.__lives

    def get_radius(self):
        """
        get method for getting the ship radius.
        :return: the ship radius.
        :type: int
        """
        return 1

    def set_axis_x(self, new_axis_point):
        """
        set method for updating the X axis point.
        :param new_axis_point: the new X axis point.
        """
        self.__x_axis = new_axis_point

    def set_axis_y(self, new_axis_point):
        """
        set method for updating the Y axis point.
        :param new_axis_point: the new Y axis point.
        """
        self.__y_axis = new_axis_point

    def set_direction(self, right_or_left):
        """
        set method for updating the ship heading.
        :param right_or_left: the direction can be only 'r' or 'l'
        :type: str
        """
        if right_or_left == "r":
            self.__direction = self.__direction - 7
        elif right_or_left == "l":
            self.__direction = self.__direction + 7

    def speedup_x(self):
        """
        set method for updating the speed on axis X.
        """
        new_speed = math.cos((self.__direction*math.pi)/180) + self.__X_speed
        self.__X_speed = new_speed

    def speedup_y(self):
        """
        set method for updating the speed on axis Y.
        """
        new_speed = math.sin((self.__direction*math.pi)/180) + self.__y_speed
        self.__y_speed = new_speed

    def remove_life(self):
        """
        set method to remove 1ife from the ship
        """
        if self.__lives < 0:
            self.__lives -= 1
