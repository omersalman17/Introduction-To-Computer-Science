#############################################################################
# FILE : asteroid.py
# WRITERS : Omer Salman, Ido Karniel
# EXERCISE :  2018-2019 intro2cs1 ex10 "Asteroid" game
# DESCRIPTION: A file that contain the class Asteroid for the game "Asteroid"
#############################################################################

import math


class Asteroid:
    """
    class to defining set up an asteroid.
    """

    def __init__(self, x_axis, x_speed, y_axis, y_speed, size):
        """
        method for initializing an asteroid object.
        :param x_axis: the asteroid location on axis X.
        :param x_speed: the asteroid speed on axis X.
        :param y_axis: the asteroid location on axis Y.
        :param y_speed: the asteroid speed on axis Y.
        :param size: the asteroid size.
        :type: int
        """
        self.__x_axis = x_axis
        self.__x_speed = x_speed
        self.__y_axis = y_axis
        self.__y_speed = y_speed
        self.__size = size

    def get_axis_x(self):
        """
        get method for getting the asteroid location on axis X.
        :return: the asteroid location on axis X.
        """
        return self.__x_axis

    def get_speed_x(self):
        """
        get method for getting the asteroid speed on axis X.
        :return: the asteroid speed on axis X.
        """
        return self.__x_speed

    def get_axis_y(self):
        """
        get method for getting the asteroid location on axis Y.
        :return: the asteroid location on axis Y.
        """
        return self.__y_axis

    def get_speed_y(self):
        """
        get method for getting the asteroid speed on axis Y.
        :return: the asteroid speed on axis Y.
        """
        return self.__y_speed

    def get_radius(self):
        """
        get method for getting the asteroid radius.
        :return: the asteroid radius.
        """
        return self.__size * 10 - 5

    def get_size(self):
        """
        get method for getting the asteroid size.
        :return: the asteroid size.
        :type: int
        """
        return self.__size

    def set_axis_x(self, new_axis_point):
        """
        set method for getting the asteroid location on axis X.
        :param new_axis_point: the new axis point
        """
        self.__x_axis = new_axis_point

    def set_axis_y(self, new_axis_point):
        """
        set method for getting the asteroid location on axis Y.
        :param new_axis_point: the new axis point
        """
        self.__y_axis = new_axis_point

    def has_intersection(self, obj):
        """
        get method for check if object crashed into an asteroid.
        :param obj: any object how have the methods "get_axis_x", "get_axis_y"
                    and "get_radius". e.g of objects (Ship, Torpedo).
        :return: True if the object hit the asteroid or False if not.
        """
        first_cal = obj.get_axis_x() - self.get_axis_x()
        second_cal = obj.get_axis_y() - self.get_axis_y()
        first = math.pow(first_cal, 2)
        second = math.pow(second_cal, 2)
        distance = math.sqrt(first + second)
        if distance <= self.get_radius() + obj.get_radius():
            return True
        else:
            return False
