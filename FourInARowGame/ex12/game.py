NUM_OF_ROWS = 6
NUM_OF_COLS = 7
WIN_REQ = 4
EMPTY_CELL = "*"
BLUE = 1
RED = 2


class Game:
    def __init__(self):
        """Initializes game object"""
        self.__matrix = []
        for i in range(NUM_OF_ROWS):
            self.__matrix.append([EMPTY_CELL] * NUM_OF_COLS)
        self.__turn = 1
        self.is_game_over = False
        self.__last_move = (None, None)

    def make_move(self, column):
        """If possible makes a move, otherwise raise an exception"""
        if self.is_game_over is False:
            try:
                player = self.get_current_player()
                row_of_empty_square = self.find_top(column)
                self.__matrix[row_of_empty_square][column] = str(player)
                self.__turn += 1
                self.__last_move = (row_of_empty_square, column)
            except:
                raise Exception("Illegal move.")
        else:
            raise Exception("Illegal move.")

    def find_top(self, column):
        """
        :param column: column number
        :return: line of bottom empty row, None if column is full
        """
        for i in range(len(self.__matrix))[::-1]:
            if self.__matrix[i][column] == "*":
                return i

    def is_full(self):
        """Checks if the board is full"""
        for column in range(NUM_OF_COLS):
            if self.get_player_at(0, column) is None:
                return False
        return True

    def get_winner(self):
        """Returns winning player (1 for blue, 2 for red),
         0 if tie or None if game not over"""
        if self.__turn == 1:
            return
        if self.find_winning_coor() is not None:
            row, col = self.__last_move
            self.is_game_over = True
            return int(self.__matrix[row][col])
        elif self.is_full() is True:
            self.is_game_over = True
            return 0

    def get_player_at(self, row, col):
        """Returns the player in the coordinate of a given row and column"""
        try:
            if self.__matrix[row][col] == "*":
                return None
            else:
                return int(self.__matrix[row][col])
        except:
            raise Exception("Illegal location.")

    def get_current_player(self):
        """Returns the current player's turn"""
        if self.__turn % 2 == 0:
            player = RED  # red player turn
        else:
            player = BLUE  # blue player turn
        return player

    def find_winning_coor(self):
        """Returns a list of coordinates of all winning chips (4),
         None otherwise"""
        row, col = self.__last_move
        winner = self.__matrix[row][col]
        counter = 0
        if self.check_line(winner, counter) is not None:
            return self.check_line(winner, counter)
        elif self.check_row(winner, counter) is not None:
            return self.check_row(winner, counter)
        elif self.check_diagonal_right_to_left(winner, counter) is not None:
            return self.check_diagonal_right_to_left(winner, counter)
        elif self.check_diagonal_left_to_right(winner, counter) is not None:
            return self.check_diagonal_left_to_right(winner, counter)

    def check_line(self, winner, counter):
        """Checks if the 4 winning chips are in this line,
        if they are, returns a list of  their coordinates"""
        wining_row = self.__last_move[0]
        win_coor_list = []
        for column in range(len(self.__matrix[wining_row])):
            if self.__matrix[wining_row][column] == winner:
                counter += 1
                win_coor_list.append((wining_row, column))
                if counter == WIN_REQ:
                    return win_coor_list
            else:
                counter = 0
                win_coor_list = []

    def check_row(self, winner, counter):
        """Checks if the 4 winning chips are in this row,
        if they are, returns a list of  their coordinates"""
        wining_column = self.__last_move[1]
        win_coor_list = []
        for row in range(len(self.__matrix)):
            if self.__matrix[row][wining_column] == winner:
                counter += 1
                win_coor_list.append((row, wining_column))
                if counter == WIN_REQ:
                    return win_coor_list
            else:
                counter = 0
                win_coor_list = []

    def check_diagonal_right_to_left(self, winner, counter):
        """Checks if the 4 winning chips are in this diagonal (right to
         left), if they are, returns a list of  their coordinates"""
        wining_row = self.__last_move[0]
        wining_column = self.__last_move[1]
        win_coor_list = []
        if wining_row < wining_column:
            diagonal_first_coor = (0, wining_column - wining_row)
        else:
            diagonal_first_coor = (wining_row - wining_column, 0)
        row = diagonal_first_coor[0]
        column = diagonal_first_coor[1]
        while row <= NUM_OF_ROWS - 1 and column <= NUM_OF_COLS - 1:
            if self.__matrix[row][column] == winner:
                counter += 1
                win_coor_list.append((row, column))
                if counter == WIN_REQ:
                    return win_coor_list
            else:
                counter = 0
                win_coor_list = []
            row += 1
            column += 1

    def check_diagonal_left_to_right(self, winner, counter):
        """Checks if the 4 winning chips are in this diagonal (left to
         right), if they are, returns a list of  their coordinates"""
        wining_row = self.__last_move[0]
        wining_column = self.__last_move[1]
        win_coor_list = []
        while wining_row != NUM_OF_ROWS - 1 and wining_column != 0:
            wining_row += 1
            wining_column -= 1
        row = wining_row
        column = wining_column
        while row >= 0 and column <= NUM_OF_COLS - 1:
            if self.__matrix[row][column] == winner:
                counter += 1
                win_coor_list.append((row, column))
                if counter == WIN_REQ:
                    return win_coor_list
            else:
                counter = 0
                win_coor_list = []
            row -= 1
            column += 1
