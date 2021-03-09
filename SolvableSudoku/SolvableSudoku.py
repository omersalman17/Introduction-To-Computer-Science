############################################################################
# FILE : SolvableSudoku
# WRITER : Omer Salman
# EXERCISE : intro2cs1 ex8 2018-2019
"""DESCRIPTION: a program that checks if a sudoku is solvable and returns
 True or False accordingly. the program also runs several recursive functions
  in order to find k length subsets of n length set."""
############################################################################

import math


def solve_sudoku(board):
    """function gets matrix presents sudoku, function checks if the sudoku is
     solvable using calling a recursive function "solve_sudoku_helper" """
    line_index, row_index = find_next_zero(board)
    if line_index == -1 and row_index == -1:
        return True
    return sudoku_helper(board, line_index, row_index)


def sudoku_helper(board, line_index, row_index):
    """function checks if soduku is solvable, function returns true if it is
     and false if it isn't"""
    for number in range(len(board)):
        number = number + 1
        if illegal_placement(board, line_index, row_index, number):
            continue
        board[line_index][row_index] = number
        if solve_sudoku(board):
            return True
        continue
    board[line_index][row_index] = 0
    return False


def illegal_placement(board, line_index, row_index, number):
    """function checks if a number's placement is legal, if it is, function
     returns True, is it is not, function returns False"""
    if number_in_square(board, number, row_index, line_index):
        return True
    else:
        for i in range(len(board)):
            if board[line_index][i] == number:
                return True
        for i in range(len(board)):
            if board[i][row_index] == number:
                return True
    return False


def number_in_square(board, number, row_index, line_index):
    """function checks if a number is already in a sudoku square. function
     returns True if it is and False if it isn't."""
    square_length = int(math.sqrt(len(board)))
    line_index = int(line_index / square_length) * square_length
    row_index = int(row_index / square_length) * square_length
    for i in range(square_length):
        for j in range(square_length):
            if board[line_index + i][row_index + j] == number:
                return True
    return False


def find_next_zero(board):
    """function searches the next empty place in sudoku. if there is one,
     function returns its coordinates, is there is no one function
      returns -1 and -1 as the coordinates"""
    if len(board) >= 1:
        for line_index in range(len(board)):
            for row_index in range(len(board)):
                if board[line_index][row_index] == 0:
                    return line_index, row_index
    return -1, -1


def print_k_subsets(n, k):
    """function prints all k length subsets of n length set"""
    if k <= n:
        cur_set = [False] * n
        print_k_subsets_helper(cur_set, k, 0, 0)


def print_k_subsets_helper(cur_set, k, index, picked):
    """helper recursive function to the function "print_k_subsets" """

    if k == picked:
        print_set(cur_set)
        return

    if index == len(cur_set):
        return

    cur_set[index] = True
    print_k_subsets_helper(cur_set, k, index + 1, picked + 1)

    cur_set[index] = False
    print_k_subsets_helper(cur_set, k, index + 1, picked)


def print_set(cur_set):
    """function prints set"""
    lst = []
    for (idx, in_cur_set) in enumerate(cur_set):
        if in_cur_set:
            lst.append(idx)
    print(lst)


def fill_k_subsets(n, k, lst):
    """function returns list with all k length subsets of n length """
    if k <= n:
        cur_set = [False] * n
        fill_k_subset_helper(cur_set, k, 0, 0, lst)


def fill_k_subset_helper(cur_set, k, index, picked, lst):
    """recursive helper function for function "fill_k_subsets" """

    if k == picked:
        fill_set(cur_set, lst)
        return

    if index == len(cur_set):
        return

    cur_set[index] = True
    fill_k_subset_helper(cur_set, k, index + 1, picked + 1, lst)

    cur_set[index] = False
    fill_k_subset_helper(cur_set, k, index + 1, picked, lst)


def fill_set(cur_set, lst):
    """function fills lst with suitable subsets"""
    temp_lst = []
    for (idx, in_cur_set) in enumerate(cur_set):
        if in_cur_set:
            temp_lst.append(idx)
    lst.append(temp_lst)


def return_k_subsets(n, k):
    """function returns a list of all k length subsets of n length set
     as lists"""
    if k == 0:
        return [[]]
    elif k > n:
        return []
    elif k == n:
        return [[1]]
    return return_k_subsets_helper(n, k, 0)


def return_k_subsets_helper(n, k, picked):
    """recursive helper function for function "return_k_subsets" """
    if k == picked:
        return [[]]
    res = []
    for i in range(n):
        lists_with_i = return_k_subsets_helper(n, k, picked + 1)
        for lst in lists_with_i:
            if len(lst) > 0:
                if lst[len(lst) - 1] >= i:
                    lists_with_i.remove(lst)
                    continue
            lst.append(i)
        res += lists_with_i
    new_res = []
    for lst in res:
        if len(lst) < k - picked:
            continue
        new_res.append(lst)
    return new_res
