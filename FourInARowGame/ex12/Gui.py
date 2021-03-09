from tkinter import *
from .ai import *
from .game import *
from tkinter import messagebox

BALL_SIZE = 90
CANVAS_WIDTH = 640
COLUMN_WIDTH = CANVAS_WIDTH // 7
CANVAS_HEIGHT = 550
COLUMN_SPACING = 10
AI_DELAY = 1000
OPTION_MENU_WIDTH = 5
CHOICES = {'Human', 'PC'}


class Gui:
    def __init__(self):
        """Initializes gui"""
        self.__root = Tk()
        self.__root.resizable(width=False, height=False)
        self.__root.title("Four in a row")
        self.__label_frame = self.init_label_frame()
        self.__input_frame = self.init_input_frame()
        self.__canvas = self.init_canvas()

    def start_game(self):
        """
        Initializes a new game if ai is first triggers first move
        """
        self.__input_frame.pack_forget()
        self.__game = Game()
        red_player = self.__red_tkvar.get()
        blue_player = self.__blue_tkvar.get()
        if blue_player == "PC":
            blue_player = AI(self.__game, 1)
        if red_player == "PC":
            red_player = AI(self.__game, 2)
        self.__players = [None, blue_player, red_player]
        self.__canvas.bind("<Button-1>", self.add_chip)
        self.color_labels()
        self.make_ai_move()

    def current_player(self):
        """
        :return: returns current player Human string or ai object
        """
        return self.__players[self.__game.get_current_player()]

    def is_game_over(self):
        """
        Checks if game is over by strike or tie and resets game
        :return: True if Game is over false otherwise
        """
        winner = self.__game.get_winner()
        if winner is not None and winner != 0:
            self.color_winning_chips()
            self.play_again("player " + str(winner) + " won!")
            return True
        elif winner == 0:
            self.play_again("It's a tie!")
            return True
        return False

    def play_again(self, text):
        """
        Display win/tie message and ask user if he wants to play again
        :param text: string win or tie message
        """
        result = messagebox.askyesno(text, "Would you like to play again?")
        if result is True:
            self.__canvas.destroy()
            self.__input_frame.pack()
            self.__canvas = self.init_canvas()
            self.__redLabel.config(bg="SystemButtonFace")
            self.__blueLabel.config(bg="SystemButtonFace")
        else:
            self.__root.destroy()

    def color_winning_chips(self):
        """
        colors winning chips
        :return:
        """
        win_chips = self.__game.find_winning_coor()
        for row, col in win_chips:
            self.fill_chip(row, col, None)

    def make_ai_move(self):
        """
        Checks current player is ai
        :return:
        """
        ai = self.current_player()
        if ai == "Human" or self.__game is None:
            return
        col = ai.find_legal_move()
        player = self.__game.get_current_player()
        row = self.__game.find_top(col)
        self.__game.make_move(col)
        self.fill_chip(row, col, player)
        if self.is_game_over() is True:
            return
        self.color_labels()
        if self.current_player() != "Human":
            self.__root.after(AI_DELAY, self.make_ai_move)

    def color_labels(self):
        """
        Colors labels according to current player turn
        :return:
        """
        if self.current_player() != "Human":
            self.__instructions.config(fg="SystemButtonFace")
        else:
            self.__instructions.config(fg="black")
        if self.__game.get_current_player() == 1:
            self.__redLabel.config(bg="SystemButtonFace")
            self.__blueLabel.config(bg="green")
        else:
            self.__redLabel.config(bg="green")
            self.__blueLabel.config(bg="SystemButtonFace")

    def init_label_frame(self):
        """
        Initializes label frame
        """
        labelFrame = Frame(self.__root)
        self.__instructions = Label(labelFrame,
                                    text="Please click on wanted column",
                                    font=("Helvetica", 12),
                                    fg="SystemButtonFace")
        self.__instructions.pack(side=LEFT)
        self.__blueLabel = Label(labelFrame, text="Player 1",
                                 fg="blue", padx=30)
        self.__blueLabel.pack(side=LEFT)
        self.__redLabel = Label(labelFrame, text="Player 2", fg="red", padx=30)
        self.__redLabel.pack(side=LEFT)
        labelFrame.pack(fill=X)
        return labelFrame

    def init_input_frame(self):
        """
        Initializes input frame
        """
        input_frame = Frame(self.__root)
        self.__blue_tkvar = StringVar(self.__root)
        self.__blue_tkvar.set('Human')
        blue_popup_menu = OptionMenu(input_frame, self.__blue_tkvar, *CHOICES)
        blue_popup_menu.config(width=OPTION_MENU_WIDTH)
        blue_popup_menu.pack(side=LEFT)
        self.__red_tkvar = StringVar(self.__root)
        self.__red_tkvar.set('PC')
        red_popup_menu = OptionMenu(input_frame, self.__red_tkvar, *CHOICES)
        red_popup_menu.config(width=OPTION_MENU_WIDTH)
        start_button = Button(input_frame, text="Start",
                              command=self.start_game)
        start_button.pack(side=LEFT)
        red_popup_menu.pack(side=LEFT)
        input_frame.pack()
        return input_frame

    def fill_chip(self, row, column, player):
        """
        colors chip in correct color for player 1 or 2, else chip is winning
        colors it yellow
        :param row:
        :param column:
        :return:
        """
        column += 1
        chip_num = NUM_OF_COLS * row + column
        if player == 1:
            self.__canvas.itemconfig(chip_num, fill="blue")
        elif player == 2:
            self.__canvas.itemconfig(chip_num, fill="red")
        else:
            self.__canvas.itemconfig(chip_num, fill="yellow")

    def add_chip(self, event):
        """
        Parses mouse click, calculates column and fills the top chip with
        current player color
        :param event:
        :return:
        """
        if self.current_player() != "Human":
            return
        column = event.x // COLUMN_WIDTH
        player = self.__game.get_current_player()
        row = self.__game.find_top(column)
        self.__game.make_move(column)
        self.fill_chip(row, column, player)
        if self.is_game_over() is True:
            return
        self.color_labels()
        if self.current_player() != "Human":
            self.__root.after(AI_DELAY, self.make_ai_move)

    def init_canvas(self):
        """
        Initializes graphical game board
        :return: Canvas object containing numbered oval objects
        """
        canvas = Canvas(self.__root, width=CANVAS_WIDTH, bg="green",
                        height=CANVAS_HEIGHT)
        for col in range(NUM_OF_ROWS):
            for row in range(NUM_OF_COLS):
                canvas.create_oval(row * BALL_SIZE + COLUMN_SPACING,
                                   col * BALL_SIZE + COLUMN_SPACING,
                                   row * BALL_SIZE + BALL_SIZE,
                                   col * BALL_SIZE + BALL_SIZE, fill="white")
        canvas.pack(side=BOTTOM)
        return canvas

    def main_loop(self):
        """runs mainloop"""
        self.__root.mainloop()
