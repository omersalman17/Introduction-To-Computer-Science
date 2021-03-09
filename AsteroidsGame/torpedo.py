############################################################################
# FILE : torpedo.py
# WRITERS : Omer Salman, Ido Karniel
# EXERCISE :  2018-2019 intro2cs1 ex10 "Asteroid" game
# DESCRIPTION: A file that contain the class Torpedo for the game "Asteroid"
############################################################################

import math


class Torpedo:
    """
    class to defining set up torpedo.
    """

    def __init__(self, axis_x, x_speed, axis_y, y_speed, direction, life_time=200):
        """
        the init func that build new torpedo objects.
        :param axis_x: the x axis point.
        :param x_speed: the speed on axis x.
        :param axis_y: the y axis point.
        :param y_speed: the speed on axis y.
        :param direction: the torpedo heading.
        :param life_time: the torpedo life time. default 200
        """
        self.__axis_x = axis_x
        self.__axis_y = axis_y
        self.__direction = direction
        self.__x_speed = 2 * math.cos((self.__direction * math.pi) / 180) + x_speed
        self.__y_speed = 2 * math.sin((self.__direction * math.pi) / 180) + y_speed
        if life_time >= 0:
            self.__life_time = life_time
        else:
            self.__life_time = 0

    def get_axis_x(self):
        """
        get method for getting the torpedo location on axis X.
        :return: the torpedo location on axis X.
        """
        return self.__axis_x

    def get_axis_y(self):
        """
        get method for getting the torpedo location on axis Y.
        :return: the torpedo location on axis Y.
        """
        return self.__axis_y

    def get_direction(self):
        """
        get method for getting the torpedo heading.
        :return: the torpedo hading on degrees.
        """
        return self.__direction

    def get_speed_x(self):
        """
        get method for getting the torpedo speed on axis X.
        :return: the torpedo speed on axis X.
        """
        return self.__x_speed

    def get_speed_y(self):
        """
        get method for getting the torpedo speed on axis Y.
        :return: the torpedo speed on axis Y.
        """
        return self.__y_speed

    def get_radius(self):
        """
        get method for getting the torpedo radius.
        :return: the ship radius.
        :type: int
        """
        return 4

    def check_life_time(self):
        """
        get method for check if the torpedo reach the and of his life.
        if return True the torpedo end his life else hie lose 1 from his life.
        :return: True if the torpedo reached the end of his life else False.
        """
        if self.__life_time == 0:
            return True
        else:
            self.__life_time = self.__life_time - 1
            return False

    def set_axis_x(self, new_axis_point):
        """
        set method for getting the torpedo location on axis X.
        :param new_axis_point: the new axis point
        """
        self.__axis_x = new_axis_point

    def set_axis_y(self, new_axis_point):
        """
        set method for getting the torpedo location on axis Y.
        :param new_axis_point: the new axis point
        """
        self.__axis_y = new_axis_point
