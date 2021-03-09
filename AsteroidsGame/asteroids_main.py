######################################################
# FILE : asteroids_main.py
# WRITERS : Omer Salman, Ido Karniel
# EXERCISE :  2018-2019 intro2cs1 ex10 "Asteroid" game
# DESCRIPTION: A program that run the game "Asteroid"
######################################################

from screen import Screen
from ship import Ship
from asteroid import Asteroid
from torpedo import Torpedo
import random as rnd
import math
import sys

DEFAULT_ASTEROIDS_NUM = 5


class GameRunner:
    """
    class that include the connect all the game parts and running them.
    """

    def __init__(self, asteroids_amount):
        """
        init method to creat object game whit all the things that game need for
        initialize.
        :param asteroids_amount: the asteroid amount.
        :type: int.
        """
        self.__screen = Screen()

        self.__screen_max_x = Screen.SCREEN_MAX_X
        self.__screen_max_y = Screen.SCREEN_MAX_Y
        self.__screen_min_x = Screen.SCREEN_MIN_X
        self.__screen_min_y = Screen.SCREEN_MIN_Y

        # create a ship object in a random location.
        random_x_location = rnd.randint(self.__screen_min_x,
                                          self.__screen_max_x)
        random_y_location = rnd.randint(self.__screen_min_y,
                                          self.__screen_max_y)
        self.__ship = Ship(random_x_location, random_y_location)

        self.__asteroids_list = []  # list of Asteroid objects
        self.__adding_asteroids(asteroids_amount)

        self.__torpedo_list = []  # list of Torpedo objects
        self.__user_score = 0  # the score the user starts with.

    def __adding_asteroids(self, asteroids_amount):
        """
        a self method that create's the asteroids for start the game.
        and add's them to the asteroid list.
        :param asteroids_amount: the amount of the asteroids that
        the user input in the game starting or from the default amount.
        :type: int.
        """
        for i in range(asteroids_amount):
            ast_x_place = rnd.randint(self.__screen_min_x,
                                        self.__screen_max_x)
            ast_y_place = rnd.randint(self.__screen_min_y,
                                        self.__screen_max_y)
            if ast_x_place == self.__ship.get_axis_x():
                ast_x_place = rnd.randint(self.__screen_min_x,
                                            self.__screen_max_x)
            if ast_y_place == self.__ship.get_axis_y():
                ast_y_place = rnd.randint(self.__screen_min_x,
                                            self.__screen_max_x)
            ast_size = 3
            ast_x_speed = rnd.randint(1, 4)
            ast_y_speed = rnd.randint(1, 4)
            asteroid = Asteroid(ast_x_place, ast_x_speed, ast_y_place,
                                ast_y_speed, ast_size)
            self.__asteroids_list.append(asteroid)
            self.__screen.register_asteroid(asteroid, ast_size)

    def __new_coord_x(self, obj):
        """
        self method for calculate the objects movement in axis x.
        **important**
        The object need method get_speed_x(), get_axis_y() ans set_axis()
        :param obj: some object how can move in this game. e.g (ship, asteroid)
        :return: the new coord in axis x.
        """
        delta = self.__screen_max_x - self.__screen_min_x
        parentheses = obj.get_speed_x() + obj.get_axis_x()-self.__screen_min_x
        new_cord = parentheses % delta + self.__screen_min_x
        obj.set_axis_x(new_cord)

    def __new_coord_y(self, obj):
        """
        self method for calculate the objects movement in axis y.
        **important**
        The object need method get_speed_y(), get_axis_y() ans set_axis()
        :param obj: some object how can move in this game. e.g (ship, asteroid)
        :return: the new coord in axis y.
        """
        delta = self.__screen_max_y - self.__screen_min_y
        parentheses = obj.get_speed_y() + obj.get_axis_y() - self.__screen_min_y
        new_cord = parentheses % delta + self.__screen_min_y
        obj.set_axis_y(new_cord)

    def run(self):
        self._do_loop()
        self.__screen.start_screen()

    def _do_loop(self):
        # You don't need to change this method!
        self._game_loop()

        # Set the timer to go off again
        self.__screen.update()
        self.__screen.ontimer(self._do_loop, 5)

    def _game_loop(self):
        """
        The main method that calls all the methods for run the game properly.
        this method run on loop until the game is ending.
        """
        self.__user_input()
        self.__move_and_draw()
        self.__asteroids_crash()
        self.__game_ending()

    def __user_input(self):
        """
        self method for checking if the user chose to do an accession.
        """
        if self.__screen.is_up_pressed():
            self.__ship.speedup_x()
            self.__ship.speedup_y()
        if self.__screen.is_right_pressed():
            self.__ship.set_direction("r")
        if self.__screen.is_left_pressed():
            self.__ship.set_direction("l")
        if self.__screen.is_space_pressed():
            self.__add_torpedo()
        self.__check_teleport_pressed()

    def __move_and_draw(self):
        """
        this self method move all the objects in the game.
        """
        self.__new_coord_x(self.__ship)
        self.__new_coord_y(self.__ship)
        self.__draw_ship()
        self.__update_torpedo()
        for asteroid in self.__asteroids_list:
            self.__new_coord_x(asteroid)
            self.__new_coord_y(asteroid)
            self.__screen.draw_asteroid(asteroid, asteroid.get_axis_x(),
                                        asteroid.get_axis_y())

    def __bulls_eye(self):
        """
        self method for check if torpedo hit an asteroid.
        this method update the user score,
        the asteroid list and the torpedo list.
        """
        for asteroid in self.__asteroids_list:
            for torpedo in self.__torpedo_list:
                if asteroid.has_intersection(torpedo):
                    self.__torpedo_list.remove(torpedo)
                    self.__screen.unregister_torpedo(torpedo)
                    if asteroid.get_size() == 3:
                        self.__divide_asteroid(torpedo, asteroid, 2)
                        self.__user_score += 20
                    elif asteroid.get_size() == 2:
                        self.__divide_asteroid(torpedo, asteroid, 1)
                        self.__user_score += 50
                    elif asteroid.get_size() == 1:
                        self.__asteroids_list.remove(asteroid)
                        self.__user_score += 100
                    self.__screen.unregister_asteroid(asteroid)
                    self.__screen.set_score(self.__user_score)
                    break

    def __check_teleport_pressed(self):
        """
        this self method check if the user chose to teleport the ship and
        teleport it.
        """
        if self.__screen.is_teleport_pressed():
            random_x_location = rnd.randint(self.__screen_min_x,
                                            self.__screen_max_x)
            random_y_location = rnd.randint(self.__screen_min_y,
                                            self.__screen_max_y)
            self.__ship.set_axis_x(random_x_location)
            self.__ship.set_axis_y(random_y_location)
            for asteroid in self.__asteroids_list:
                if asteroid.has_intersection(self.__ship):
                    self.__check_teleport_pressed()

    def __asteroids_crash(self):
        """
        this self method check if the ship crashed into an asteroid,
        remove life, remove the asteroid and send a massage to the user.
        """
        for asteroid in self.__asteroids_list:
            if asteroid.has_intersection(self.__ship):
                self.__ship.remove_life()
                self.__screen.remove_life()
                self.__screen.show_message("watch out!",
                                           "asteroids intersection!")
                self.__asteroids_list.remove(asteroid)
                self.__screen.unregister_asteroid(asteroid)
                break

    def __divide_asteroid(self, torp, ast, size):
        """
        self method for divide asteroids and make them smaller
        when torpedo hits them.
        the method update the __asteroid_list and register them.
        :param torp: a Torpedo object.
        :param ast: an Asteroid object.
        :param size: the new size that the new asteroid gat.
        :type: int
        """
        for i in range(2):
            if i == 1:
                opposite = -1
            else:
                opposite = 1
            speed_x = (ast.get_speed_x() * opposite + torp.get_speed_x()) /\
                      math.sqrt(math.pow(ast.get_speed_y(), 2) +
                                math.pow(ast.get_speed_x(), 2))

            speed_y = (ast.get_speed_y() * opposite + torp.get_speed_y()) /\
                      math.sqrt(math.pow(ast.get_speed_y(), 2) +
                                math.pow(ast.get_speed_x(), 2))
            self.__asteroids_list.append(
                Asteroid(ast.get_axis_x(), speed_x, ast.get_axis_y(),
                         speed_y, size))
            self.__screen.register_asteroid(self.__asteroids_list[-1], size)
        if ast in self.__asteroids_list:
            self.__asteroids_list.remove(ast)

    def __update_torpedo(self):
        """
        self method for updating the torpedo locations,
        and setting torpedo life amd removed the old torpedo.
        """
        if len(self.__torpedo_list) >= 10:
            first_torpedo = self.__torpedo_list.pop(0)
            self.__screen.unregister_torpedo(first_torpedo)
        self.__bulls_eye()  # checking if torpedo hit an asteroid
        for torpedo in self.__torpedo_list:
            self.__new_coord_x(torpedo)
            self.__new_coord_y(torpedo)
            self.__screen.draw_torpedo(torpedo, torpedo.get_axis_x(),
                                       torpedo.get_axis_y(),
                                       torpedo.get_direction())
            if torpedo.check_life_time():
                self.__screen.unregister_torpedo(torpedo)
                self.__torpedo_list.remove(torpedo)

    def __add_torpedo(self):
        """
        self method for create and register a new torpedo.
        this method update the __torpedo_list.
        """
        self.__torpedo_list.append(Torpedo(self.__ship.get_axis_x(),
                                           self.__ship.get_speed_x(),
                                           self.__ship.get_axis_y(),
                                           self.__ship.get_speed_y(),
                                           self.__ship.get_direction()))
        self.__screen.register_torpedo(self.__torpedo_list[-1])

    def __draw_ship(self):
        """
        self method for better cod dishing
        """
        self.__screen.draw_ship(self.__ship.get_axis_x(),
                                self.__ship.get_axis_y(),
                                self.__ship.get_direction())

    def __game_ending(self):
        """
        self method for check if the game is ended and exit the game
        """
        if not self.__asteroids_list:
            self.__screen.show_message("you won!", "no more asteroids!")
            self.__screen.end_game()
            sys.exit()
        elif self.__ship.get_life() == 0:
            self.__screen.show_message("you lost!", "out of lives!")
            self.__screen.end_game()
            sys.exit()
        elif self.__screen.should_end():
            self.__screen.show_message("quit game", "q button pressed")
            self.__screen.end_game()
            sys.exit()
# -----------------------------end of class---------------------------------


def main(amount):
    runner = GameRunner(amount)
    runner.run()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(int(sys.argv[1]))
    else:
        main(DEFAULT_ASTEROIDS_NUM)
