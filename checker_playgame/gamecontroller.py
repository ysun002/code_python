from checker import Checker
from board import Board
from redchecker import RedChecker
from score import Score
import math


class GameController():
    def __init__(self, square_size, board_width):
        """
        Construct a class for game controller
        """
        self.width = board_width
        self.lenth = self.width
        self.checker_num = 12
        self.square_size = square_size
        self.orginal_x = 0
        self.orginal_y = 0
        self.origi_i = 0
        self.origi_j = 0
        self.current_checker = None
        self.highlight_x = 0
        self.highlight_y = 0
        self.board = Board(self.square_size, self.width)
        self.matrix = self.board.matrix
        self.legal_posi = []
        self.drag = False
        self.valid_jump = []
        self.black_can_jump = False
        self.black_valid_jump = []
        self.remove_red = []
        self.red_king_valid = []
        self.num_black_checker = 0
        self.num_red_checker = 0
        self.step_count = 0
        self.player_turn = True
        self.end_game = False
        self.black_win = "blank"
        self.red_win = "blank"
        self.both_draw = "blank"
        # player name and score
        self.player_score = 0
        self.name = 0
        self.start_write = True
        self.countdown = 50

    def update(self):
        """
        update the matrix and display checkers
        update game status
        """
        self.num_black_checker = 0
        self.num_red_checker = 0
        for j in range(self.lenth):
            for i in range(self.width):
                if self.matrix[j][i] is not None:
                    self.matrix[j][i].display()

        self.check_jump()
        self.game_over()
        if self.end_game is False:
            if self.player_turn is False:
                self.countdown_time()
                if (self.countdown == 0):
                    self.red_player_move()
                    self.step_count += 1
                    self.initialize_delay()
        if self.end_game is True:
            self.display_end_text()
            # update score to txt
            if self.start_write is True:
                s = Score()
                s.build_dict()
                s.add_player(self.name, self.player_score)
                s.sort_the_data()
                s.write_data()
                # close writing in draw
                self.start_write = False

    def game_over(self):
        """
        Check if the game is over
        or game continue
        """
        largest_no_jump = 50
        for j in range(self.lenth):
            for i in range(self.width):
                if self.matrix[j][i] is not None:
                    if self.matrix[j][i].color == 0:  # black
                        self.num_black_checker += 1
                    if self.matrix[j][i].color == 1:
                        self.num_red_checker += 1
        if self.num_red_checker == 0:
            # black"wins"
            self.drag = False
            self.black_win = True
            self.player_score = 1
            self.end_game = True

        if self.num_black_checker == 0:
            # red wins #
            self.drag = False
            self.red_win = True
            self.player_score = 0
            self.end_game = True

        if (self.step_count > largest_no_jump
           and self.num_red_checker == self.checker_num
           and self.num_black_checker == self.checker_num):
            self.drag = False
            self.player_score = 0
            self.both_draw = True
            self.end_game = True

    def initialize_delay(self):
        """
        innitialize delay time for red checker moving
        """
        self.countdown = 100

    def countdown_time(self):
        """
        countdown time for a few seconds
        """
        if (self.countdown != 0):
            self.countdown = self.countdown - 1

    def display_end_text(self):
        """
        display end text to the player
        """
        if self.black_win is True:
            message = "Black Wins !"
        elif self.red_win is True:
            message = "Red Wins !"
        elif self.both_draw is True:
            message = "Draw!"
        center = self.width * self.square_size / 2
        offset = 3
        textAlign(CENTER)
        WHITE = 255
        fill(WHITE)
        TEXT_SIZE = 110
        textSize(TEXT_SIZE)
        text(message, center, center)

    def red_player_move(self):
        """
        game control red player move
        """
        TWO = 2
        # add new line
        self.red_king_valid = []
        # add new line
        # jump
        for j in range(self.lenth):
            for i in range(self.width):
                if (self.matrix[j][i] is not None
                   and self.matrix[j][i].color == 1):
                    if [i, j] in self.valid_jump:
                        self.red_jump(i, j)
                        return

        # single move
        if not self.player_turn:
            for j in range(self.lenth):
                for i in range(self.width):
                    if (self.matrix[j][i] is not None
                       and self.matrix[j][i].color == 1
                       and self.matrix[j][i].king is False):
                        if ((j+1 < self.lenth) and (i-1 >= 0)
                                and self.matrix[j+1][i-1] is None):
                            self.matrix[j][i] = None
                            circle_x = ((i-1) * self.square_size +
                                        self.square_size/TWO)
                            circle_y = ((j+1) * self.square_size +
                                        self.square_size/TWO)
                            self.matrix[j+1][i-1] = RedChecker(circle_x,
                                                               circle_y)
                            self.player_turn = True
                            return
                        if ((j+1 < self.lenth) and (i+1 < self.lenth)
                                and self.matrix[j+1][i+1] is None):
                            self.matrix[j][i] = None
                            circle_x = ((i+1) * self.square_size +
                                        self.square_size/TWO)
                            circle_y = ((j+1) * self.square_size +
                                        self.square_size/TWO)
                            self.matrix[j+1][i+1] = RedChecker(circle_x,
                                                               circle_y)
                            self.player_turn = True
                            return
                    # red king new modify

                    if (self.matrix[j][i] is not None
                       and self.matrix[j][i].color == 1
                       and self.matrix[j][i].king is True):
                        if ((0 <= j-1 < self.lenth) and (0 <= i-1 < self.lenth)
                                and self.matrix[j-1][i-1] is None):
                            self.matrix[j][i] = None
                            circle_x = ((i-1) * self.square_size
                                        + self.square_size/TWO)
                            circle_y = ((j-1) * self.square_size
                                        + self.square_size/TWO)
                            self.matrix[j-1][i-1] = RedChecker(circle_x,
                                                               circle_y)
                            self.matrix[j-1][i-1].king = True
                            self.player_turn = True
                            return
                        if ((0 <= j-1 < self.lenth) and (0 <= i+1 < self.lenth)
                                and self.matrix[j-1][i+1] is None):
                            self.matrix[j][i] = None
                            circle_x = ((i+1) * self.square_size
                                        + self.square_size/TWO)
                            circle_y = ((j-1) * self.square_size
                                        + self.square_size/TWO)
                            self.matrix[j-1][i+1] = RedChecker(circle_x,
                                                               circle_y)
                            self.matrix[j-1][i+1].king = True
                            self.player_turn = True
                            return
                        # modify here
                        if ((0 <= j+1 < self.lenth) and (0 <= i-1 < self.lenth)
                                and self.matrix[j+1][i-1] is None):
                            self.matrix[j][i] = None
                            circle_x = ((i-1) * self.square_size
                                        + self.square_size/TWO)
                            circle_y = ((j+1) * self.square_size
                                        + self.square_size/TWO)
                            self.matrix[j+1][i-1] = RedChecker(circle_x,
                                                               circle_y)
                            self.matrix[j+1][i-1].king = True
                            self.player_turn = True
                            return
                        if ((0 <= j+1 < self.lenth) and (0 <= i+1 < self.lenth)
                                and self.matrix[j+1][i+1] is None):
                            self.matrix[j][i] = None
                            circle_x = ((i+1) * self.square_size
                                        + self.square_size/TWO)
                            circle_y = ((j+1) * self.square_size
                                        + self.square_size/TWO)
                            self.matrix[j+1][i+1] = RedChecker(circle_x,
                                                               circle_y)
                            self.matrix[j+1][i+1].king = True
                            self.player_turn = True
                            return

    def red_jump(self, i, j):
        """
        red checker jump and eat black checker
        """
        TWO = 2
        if (j+1 < self.lenth) and (i-1 >= 0):
            if (self.matrix[j+1][i-1] is not None
               and self.matrix[j+1][i-1].color == 0):
                if (j+2 <= self.lenth) and (i-2 >= 0):
                    if self.matrix[j+2][i-2] is None:
                        if self.matrix[j][i].king is False:
                            # not king
                            self.matrix[j][i] = None
                            self.matrix[j+1][i-1] = None
                            circle_x = ((i-2) * self.square_size
                                        + self.square_size/TWO)
                            circle_y = ((j+2) * self.square_size
                                        + self.square_size/TWO)
                            self.matrix[j+2][i-2] = RedChecker(circle_x,
                                                               circle_y)
                            # handle double jump__need to add more line
                            self.again_red_jump(i-2, j+2)
                        else:
                            self.matrix[j][i] = None
                            self.matrix[j+1][i-1] = None
                            circle_x = ((i-2) * self.square_size
                                        + self.square_size/TWO)
                            circle_y = ((j+2) * self.square_size
                                        + self.square_size/TWO)
                            self.matrix[j+2][i-2] = RedChecker(circle_x,
                                                               circle_y)
                            self.matrix[j+2][i-2].king = True
                        self.player_turn = True
                        return
        if (j+1 < self.lenth) and (i+1 < self.lenth):
            if (self.matrix[j+1][i+1] is not None
               and self.matrix[j+1][i+1].color == 0):
                if (j+2 < self.lenth) and (0 <= i+2 < self.lenth):
                    if self.matrix[j+2][i+2] is None:
                        if self.matrix[j][i].king is False:
                            self.matrix[j][i] = None
                            self.matrix[j+1][i+1] = None
                            circle_x = ((i+2) * self.square_size
                                        + self.square_size/TWO)
                            circle_y = ((j+2) * self.square_size
                                        + self.square_size/TWO)
                            self.matrix[j+2][i+2] = RedChecker(circle_x,
                                                               circle_y)
                            # add new line for double jump
                            self.again_red_jump(i+2, j+2)
                        else:
                            self.matrix[j][i] = None
                            self.matrix[j+1][i+1] = None
                            circle_x = ((i+2) * self.square_size
                                        + self.square_size/TWO)
                            circle_y = ((j+2) * self.square_size
                                        + self.square_size/TWO)
                            self.matrix[j+2][i+2] = RedChecker(circle_x,
                                                               circle_y)
                            self.matrix[j+2][i+2].king = True
                        # handle double jump
                        self.player_turn = True
                        return

    def again_red_jump(self, i, j):
        """
        do red checker jump again
        """
        # check down-left direction
        TWO = 2
        if (0 <= j+1 < self.lenth) and (i-1 >= 0):
            if (self.matrix[j+1][i-1] is not None
               and self.matrix[j+1][i-1].color == 0):
                if (0 <= j+2 < self.lenth) and (i-2 >= 0):
                    if self.matrix[j+2][i-2] is None:
                        circle_x = ((i-2) * self.square_size
                                    + self.square_size/TWO)
                        circle_y = ((j+2) * self.square_size
                                    + self.square_size/TWO)
                        self.matrix[j+2][i-2] = RedChecker(circle_x,
                                                           circle_y)
                        self.matrix[j+1][i-1] = None
                        self.matrix[j][i] = None
                        self.player_turn = True
                        return
        # check down-right direction
        if (0 <= j+1 < self.lenth) and (0 <= i+1 < self.lenth):
            if (self.matrix[j+1][i+1] is not None
               and self.matrix[j+1][i+1].color == 0):
                if (0 <= j+2 < self.lenth) and (0 <= i+2 < self.lenth):
                    if self.matrix[j+2][i+2] is None:
                        circle_x = ((i+2) * self.square_size
                                    + self.square_size/TWO)
                        circle_y = ((j+2) * self.square_size
                                    + self.square_size/TWO)
                        self.matrix[j+2][i+2] = RedChecker(circle_x,
                                                           circle_y)
                        self.matrix[j][i] = None
                        self.matrix[j+1][i+1] = None
                        self.player_turn = True
                        return

    def check_jump(self):
        """
        for loop all checkers both black and red in the board
        check valid jumps
        """
        for j in range(self.lenth):
            for i in range(self.width):
                if (self.matrix[j][i] is not None
                   and self.matrix[j][i].color == 1):  # red
                    if (j+1 < self.lenth) and (i-1 >= 0):
                        if (self.matrix[j+1][i-1] is not None
                           and self.matrix[j+1][i-1].color == 0):
                            if (j+2 < self.lenth) and (i-2 >= 0):
                                if self.matrix[j+2][i-2] is None:
                                    self.valid_jump.append([i, j])
                    if (j+1 < self.lenth) and (i+1 < self.lenth):
                        if (self.matrix[j+1][i+1] is not None
                           and self.matrix[j+1][i+1].color == 0):
                            if (j+2 < self.lenth) and (0 <= i+2 < self.lenth):
                                if self.matrix[j+2][i+2] is None:
                                    self.valid_jump.append([i, j])

                if (self.matrix[j][i] is not None
                   and self.matrix[j][i].color == 0):  # black
                    if (j-1 >= 0) and (i+1 < self.lenth):
                        if (self.matrix[j-1][i+1] is not None
                           and self.matrix[j-1][i+1].color == 1):
                            if (j-2 >= 0) and (i+2 < self.lenth):
                                if self.matrix[j-2][i+2] is None:
                                    self.valid_jump.append([i, j])
                                    # self.black_valid_jump.append([i, j])
                    if (j-1 >= 0) and (i-1 >= 0):
                        if (self.matrix[j-1][i-1] is not None
                           and self.matrix[j-1][i-1].color == 1):
                            if (j-2 >= 0) and (i-2 >= 0):
                                if self.matrix[j-2][i-2] is None:
                                    self.valid_jump.append([i, j])
                                    # self.black_valid_jump.append([i, j])

    def black_jump(self):
        """
        check for only for oridinary black checkers jump
        """
        for j in range(self.lenth):
            for i in range(self.width):
                if (self.matrix[j][i] is not None
                   and self.matrix[j][i].color == 0):  # black
                    if (j-1 >= 0) and (i+1 < self.lenth):
                        if (self.matrix[j-1][i+1] is not None
                           and self.matrix[j-1][i+1].color == 1):
                            if (j-2 >= 0) and (i+2 < self.lenth):
                                if self.matrix[j-2][i+2] is None:
                                    self.black_valid_jump.append([i, j])
                    if (j-1 >= 0) and (i-1 >= 0):
                        if (self.matrix[j-1][i-1] is not None
                           and self.matrix[j-1][i-1].color == 1):
                            if (j-2 >= 0) and (i-2 >= 0):
                                if self.matrix[j-2][i-2] is None:
                                    self.black_valid_jump.append([i, j])

    def mouse_click(self, mouseX, mouseY):
        """
        when click the mouse
        select a checker to be current checker
        """
        self.black_jump()
        TWO = 2
        i, j = self.convert_index(mouseX, mouseY)
        if self.matrix[j][i] is not None:
            # i and j are index
            self.origi_i = i
            self.origi_j = j
            self.orginal_x = i * self.square_size + self.square_size/TWO
            self.orginal_y = j * self.square_size + self.square_size/TWO
        #  change code here
        if self.matrix[j][i] is not None:
            if self.matrix[j][i].color == 0:  # black
                if self.matrix[j][i].king is False:
                    if len(self.black_valid_jump) != 0:
                        if [i, j] in self.black_valid_jump:
                            self.black_can_jump = True
                            self.current_checker = self.matrix[j][i]
                            self.drag = True
                            self.black_jump_legal_position(i, j)
                            self.get_delete_red(i, j)
                        else:
                            self.black_can_jump = False
                            self.drag = False
                    else:
                        # single move, not king
                        self.matrix[j][i].can_jump = False
                        self.current_checker = self.matrix[j][i]
                        self.drag = True
                else:
                    # is black king
                    # check black king can jump
                    # need to modify
                    self.origi_i = i
                    self.origi_j = j
                    self.current_checker = self.matrix[j][i]
                    self.drag = True
        else:
            self.drag = False

    def mouse_release(self, mouseX, mouseY):
        """
        work only for black checkers
        when release mouse
        move the black checker to valid position
        or snap back
        """
        TWO = 2
        index_x = int(math.floor(mouseX / self.square_size))
        index_y = int(math.floor(mouseY / self.square_size))
        release_posi = [index_x, index_y]
        if (self.current_checker is not None
           and self.current_checker.color == 0):  # black checker
            if mouseY <= self.square_size:
                print("You achieves a King Rank")
                self.current_checker.king = True
            if self.black_can_jump is False:
                if self.current_checker.king is True:
                    self.king_legal()
                    self.black_king_jump(self.origi_i, self.origi_j)
                else:
                    self.posi_black_legal()
            # add line _modify

        if ((release_posi in self.legal_posi)
           and (self.matrix[index_y][index_x] is None)):
            # if the move is valid
            self.current_checker.circle_x = (index_x * self.square_size
                                             + self.square_size/TWO)
            self.current_checker.circle_y = (index_y * self.square_size
                                             + self.square_size/TWO)
            self.matrix[index_y][index_x] = self.current_checker
            self.matrix[self.origi_j][self.origi_i] = None
            if (self.black_can_jump is True
               and self.current_checker.king is False):
                # call a function to delete red checker
                self.remove_red_after_black_jump(index_x, index_y)
            if self.current_checker.king is True:
                # call a function to delete red checker
                self.remove_red_after_black_jump(index_x, index_y)

            self.black_can_jump = False

            # after valid release, change turn to computer
            self.player_turn = False
            self.step_count += 1
        else:
            self.current_checker.circle_x = self.orginal_x
            self.current_checker.circle_y = self.orginal_y
        # clear the list of legal positions
        self.legal_posi = []
        # clear black_valid_jump
        self.black_can_jump = False
        self.black_valid_jump = []
        self.remove_red = []
        self.valid_jump = []

    def black_jump_legal_position(self, i, j):
        """
        find the legal positions for black jumps
        """
        if (self.matrix[j][i] is not None
           and self.matrix[j][i].color == 0):  # black
            if (j-1 >= 0) and (i+1 < self.lenth):
                if (self.matrix[j-1][i+1] is not None
                   and self.matrix[j-1][i+1].color == 1):
                    if (j-2 >= 0) and (i+2 < self.lenth):
                        if self.matrix[j-2][i+2] is None:
                            self.legal_posi.append([i+2, j-2])
            if (j-1 >= 0) and (i-1 >= 0):
                if (self.matrix[j-1][i-1] is not None
                   and self.matrix[j-1][i-1].color == 1):
                    if (j-2 >= 0) and (i-2 >= 0):
                        if self.matrix[j-2][i-2] is None:
                            self.legal_posi.append([i-2, j-2])

    def get_delete_red(self, i, j):
        """
        delete red checker in the matrix
        """
        if (self.matrix[j][i] is not None
           and self.matrix[j][i].color == 0):  # black
            if (j-1 >= 0) and (i+1 < self.lenth):
                if (self.matrix[j-1][i+1] is not None
                   and self.matrix[j-1][i+1].color == 1):
                    self.remove_red.append([i+1, j-1])
            if (j-1 >= 0) and (i-1 >= 0):
                if (self.matrix[j-1][i-1] is not None
                   and self.matrix[j-1][i-1].color == 1):
                    self.remove_red.append([i-1, j-1])

    def black_king_jump(self, i, j):
        """
        find the legal positions for black King jumps
        BLACK King can go to four directions look for jump
        """
        if (self.matrix[j][i] is not None
           and self.matrix[j][i].color == 0):  # black
            # check up-right direction
            if (j-1 >= 0) and (i+1 < self.lenth):
                if (self.matrix[j-1][i+1] is not None
                   and self.matrix[j-1][i+1].color == 1):
                    if (j-2 >= 0) and (i+2 < self.lenth):
                        if self.matrix[j-2][i+2] is None:
                            self.legal_posi.append([i+2, j-2])
            # check up-left direction
            if (j-1 >= 0) and (i-1 >= 0):
                if (self.matrix[j-1][i-1] is not None
                   and self.matrix[j-1][i-1].color == 1):
                    if (j-2 >= 0) and (i-2 >= 0):
                        if self.matrix[j-2][i-2] is None:
                            self.legal_posi.append([i-2, j-2])
            # check down-left direction
            if (0 <= j+1 < self.lenth) and (i-1 >= 0):
                if (self.matrix[j+1][i-1] is not None
                   and self.matrix[j+1][i-1].color == 1):
                    if (0 <= j+2 < self.lenth) and (i-2 >= 0):
                        if self.matrix[j+2][i-2] is None:
                            self.legal_posi.append([i-2, j+2])
            # check down-right direction
            if (0 <= j+1 < self.lenth) and (0 <= i+1 < self.lenth):
                if (self.matrix[j+1][i+1] is not None
                   and self.matrix[j+1][i+1].color == 1):
                    if (0 <= j+2 < self.lenth) and (0 <= i+2 < self.lenth):
                        if self.matrix[j+2][i+2] is None:
                            self.legal_posi.append([i+2, j+2])

    def remove_red_after_black_jump(self, index_x, index_y):
        """
        After black jump
        find the direction and delete red checker
        """
        # check right first
        if index_y - self.origi_j > 1:
            # go down
            if index_x - self.origi_i > 1:
                # go right
                red_i = index_x - 1
                red_j = index_y - 1
                # down-right
                self.matrix[red_j][red_i] = None
                return
            elif index_x - self.origi_i < 0:
                # go left
                red_i = index_x + 1
                red_j = index_y - 1
                # down-left
                self.matrix[red_j][red_i] = None
                return
        elif index_y - self.origi_j < 0:
            # go up
            if index_x - self.origi_i > 1:
                # go right
                # up-right
                red_i = index_x - 1
                red_j = index_y + 1
                self.matrix[red_j][red_i] = None
                return
            elif index_x - self.origi_i < 0:
                # go left
                # up-left
                red_i = index_x + 1
                red_j = index_y + 1
                self.matrix[red_j][red_i] = None
                return

    def red_king_jump(self, i, j):
        """
        find the legal positions for red King jumps
        RED King can go to four directions look for jump
        """
        TWO = 2
        if (self.matrix[j][i] is not None
           and self.matrix[j][i].color == 1):  # red
            # check up-right direction
            if (j-1 >= 0) and (i+1 < self.lenth):
                if (self.matrix[j-1][i+1] is not None
                   and self.matrix[j-1][i+1].color == 0):
                    if (j-2 >= 0) and (i+2 < self.lenth):
                        if self.matrix[j-2][i+2] is None:
                            circle_x = ((i+2) * self.square_size
                                        + self.square_size/TWO)
                            circle_y = ((j-2) * self.square_size
                                        + self.square_size/TWO)
                            self.matrix[j-2][i+2] = RedChecker(circle_x,
                                                               circle_y)
                            self.matrix[j-2][i+2].king = True
                            self.matrix[j-1][i+1] = None
                            self.player_turn = True
                            return
            # check up-left direction
            if (j-1 >= 0) and (i-1 >= 0):
                if (self.matrix[j-1][i-1] is not None
                   and self.matrix[j-1][i-1].color == 0):
                    if (j-2 >= 0) and (i-2 >= 0):
                        if self.matrix[j-2][i-2] is None:
                            circle_x = ((i-2) * self.square_size
                                        + self.square_size/TWO)
                            circle_y = ((j-2) * self.square_size
                                        + self.square_size/TWO)
                            self.matrix[j-2][i-2] = RedChecker(circle_x,
                                                               circle_y)
                            self.matrix[j-2][i-2].king = True
                            self.matrix[j-1][i-1] = None
                            self.player_turn = True
                            return
            # check down-left direction
            if (0 <= j+1 < self.lenth) and (i-1 >= 0):
                if (self.matrix[j+1][i-1] is not None
                   and self.matrix[j+1][i-1].color == 0):
                    if (0 <= j+2 < self.lenth) and (i-2 >= 0):
                        if self.matrix[j+2][i-2] is None:
                            circle_x = ((i-2) * self.square_size
                                        + self.square_size/TWO)
                            circle_y = ((j+2) * self.square_size
                                        + self.square_size/TWO)
                            self.matrix[j+2][i-2] = RedChecker(circle_x,
                                                               circle_y)
                            self.matrix[j+2][i-2].king = True
                            self.matrix[j+1][i-1] = None
                            self.player_turn = True
                            return
            # check down-right direction
            if (0 <= j+1 < self.lenth) and (0 <= i+1 < self.lenth):
                if (self.matrix[j+1][i+1] is not None
                   and self.matrix[j+1][i+1].color == 0):
                    if (0 <= j+2 < self.lenth) and (0 <= i+2 < self.lenth):
                        if self.matrix[j+2][i+2] is None:
                            circle_x = ((i+2) * self.square_size
                                        + self.square_size/TWO)
                            circle_y = ((j+2) * self.square_size
                                        + self.square_size/TWO)
                            self.matrix[j+2][i+2] = RedChecker(circle_x,
                                                               circle_y)
                            self.matrix[j+2][i+2].king = True
                            self.matrix[j+1][i+1] = None
                            self.player_turn = True
                            return

    def mouse_highlight_valid(self, mouseX, mouseY):
        """
        When the mouse pass a checker
        If the checker has valid movable steps
        we highlight the white frame of checker
        To tell the player that this checker is movable
        """
        rightup = 0
        leftup = 0
        index_x, index_y = self.convert_index(mouseX, mouseY)
        if self.matrix[index_y][index_x] is not None:
            if self.matrix[index_y][index_x].color == 0:
                self.highlight_x = index_x
                self.highlight_y = index_y
                if self.highlight_jump() is False:
                    if index_y-1 >= 0 and index_x+1 < self.lenth:
                        if self.matrix[index_y-1][index_x+1] is None:
                            rightup = True
                    if index_y-1 >= 0 and index_x-1 >= 0:
                        if self.matrix[index_y-1][index_x-1] is None:
                            leftup = True
                    if rightup is True or leftup is True:
                        self.matrix[index_y][index_x].highlight_checker = True
                else:
                    self.matrix[index_y][index_x].highlight_checker = False
        else:
            if self.matrix[self.highlight_y][self.highlight_x] is not None:
                h_x = self.highlight_x
                h_y = self.highlight_y
                self.matrix[h_y][h_x].highlight_checker = False

    def highlight_jump(self):
        """
        before highlighting
        check whether there are possible jumps for black checkers
        return True or False
        """
        for j in range(self.lenth):
            for i in range(self.width):
                if (self.matrix[j][i] is not None
                   and self.matrix[j][i].color == 0):  # black
                    if (j-1 >= 0) and (i+1 < self.lenth):
                        if (self.matrix[j-1][i+1] is not None
                           and self.matrix[j-1][i+1].color == 1):
                            if (j-2 >= 0) and (i+2 < self.lenth):
                                if self.matrix[j-2][i+2] is None:
                                    return True
                    elif (j-1 >= 0) and (i-1 >= 0):
                        if (self.matrix[j-1][i-1] is not None
                           and self.matrix[j-1][i-1].color == 1):
                            if (j-2 >= 0) and (i-2 >= 0):
                                if self.matrix[j-2][i-2] is None:
                                    return True
        return False

    def posi_black_legal(self):
        """
        input the position of a black checker
        transfer position to index of matrix
        then check the legal position
        the left-up and right-up diagonal position
        is vacant or not
        if the position is not occupied --- means vacant,
        then this position is a valid position
        """
        if self.origi_j-1 >= 0 and self.origi_i+1 < self.lenth:
            rightup = [self.origi_i+1, self.origi_j-1]
            self.legal_posi.append(rightup)
        if self.origi_j-1 >= 0 and self.origi_i-1 >= 0:
            leftup = [self.origi_i-1, self.origi_j-1]
            self.legal_posi.append(leftup)

    def king_legal(self):
        """
        check king's legal single move
        """
        if self.origi_j-1 >= 0 and self.origi_i+1 < self.lenth:
            rightup = [self.origi_i+1, self.origi_j-1]
            self.legal_posi.append(rightup)
        if self.origi_j-1 >= 0 and self.origi_i-1 >= 0:
            leftup = [self.origi_i-1, self.origi_j-1]
            self.legal_posi.append(leftup)
        if (self.origi_j+1 < self.lenth) and (self.origi_i-1 >= 0):
            leftdown = [self.origi_i-1, self.origi_j+1]
            self.legal_posi.append(leftdown)
        if (self.origi_j+1 < self.lenth) and (self.origi_i+1 < self.lenth):
            rightdown = [self.origi_i+1, self.origi_j+1]
            self.legal_posi.append(rightdown)

    def delete_checker(self, checker):
        """
        find the index of a specific checker
        delete the checker from the matrix
        """
        for j in range(self.lenth):
            for i in range(self.width):
                if self.matrix[j][i] == checker:
                    self.matrix[j][i] = None

    def convert_index(self, x, y):
        """
        convert circle x and circle y to index of matrix
        """
        TWO = 2
        index_x = int(math.floor(x / self.square_size))
        index_y = int(math.floor(y / self.square_size))
        return index_x, index_y
