from checker import Checker
from redchecker import RedChecker


class Board():
    def __init__(self, square_size, board_width):
        """
        construct a class for board
        """
        self.width = board_width
        self.lenth = self.width
        self.square_size = square_size
        self.x_posi = 0
        self.y_posi = 0
        self.matrix = []
        self.add_checker()

    def add_checker(self):
        """
        add checkers to the matrix
        """
        FIVE = 5
        TWO = 2
        THREE = 3
        for i in range(self.width):
            self.matrix.append([])

        # Add red checker
        for y in range(THREE):
            if y % TWO == 0:
                for x in range(self.width):
                    if x % TWO != 0:
                        circle_x = x*self.square_size + self.square_size / TWO
                        circle_y = y*self.square_size + self.square_size / TWO
                        self.matrix[y].append(RedChecker(circle_x, circle_y))
                    else:
                        self.matrix[y].append(None)
            else:
                for x in range(self.width):
                    if x % TWO != 0:
                        self.matrix[y].append(None)
                    else:
                        circle_x = x*self.square_size + self.square_size / TWO
                        circle_y = y*self.square_size + self.square_size / TWO
                        self.matrix[y].append(RedChecker(circle_x, circle_y))

        # Add blank part with "None"
        for j in range(THREE, FIVE):
            for i in range(self.width):
                self.matrix[j].append(None)

        # add black checker
        for j in range(FIVE, self.lenth):
            if j % TWO != 0:
                for i in range(self.width):
                    if i % TWO == 0:
                        circle_x = i*self.square_size + self.square_size / TWO
                        circle_y = j*self.square_size + self.square_size / TWO
                        self.matrix[j].append(Checker(circle_x, circle_y))
                    else:
                        self.matrix[j].append(None)
            else:
                for i in range(self.width):
                    if i % TWO == 0:
                        self.matrix[j].append(None)
                    else:
                        circle_x = i*self.square_size + self.square_size / TWO
                        circle_y = j*self.square_size + self.square_size / TWO
                        self.matrix[j].append(Checker(circle_x, circle_y))

    def display(self):
        """
        display the board with BROWN and BEIGE colors
        Use the relation between odd numbers and even numbers
        to fill different color for each square
        """
        noStroke()
        BROWN = (115, 69, 13)
        BEIGE = (224, 191, 153)
        TWO = 2
        for y in range(0, self.lenth):
            self.x_posi = 0
            for x in range(0, self.width):
                if y % TWO == 0 and x % TWO == 0:
                    square_color = BEIGE
                elif y % TWO == 0 and x % TWO != 0:
                    square_color = BROWN
                elif y % TWO != 0 and x % TWO == 0:
                    square_color = BROWN
                elif y % TWO != 0 and x % TWO != 0:
                    square_color = BEIGE
                fill(*square_color)
                square(self.x_posi,  self.y_posi, self.square_size)
                self.x_posi = self.x_posi + self.square_size
            self.y_posi = self.y_posi + self.square_size
