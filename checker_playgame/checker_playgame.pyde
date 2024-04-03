from board import Board
from checker import Checker
from gamecontroller import GameController

square_size = 100
board_width = 8
TWO = 2
board = Board(square_size, board_width)
gc = GameController(square_size, board_width)
background_size = board.width * square_size

circle_x = square_size/TWO
circly_y = square_size + square_size/TWO


def setup():
    user_name = input('enter your name')
    if user_name:
        gc.name = user_name
        print("hi" + user_name)
    size(background_size, background_size)
    board.display()


def draw():
    board.x_posi = 0
    board.y_posi = 0
    board.display()
    gc.update()


def mousePressed():
    if gc.player_turn is True:
        gc.mouse_click(mouseX, mouseY)


def mouseMoved():
    gc.mouse_highlight_valid(mouseX, mouseY)


def mouseDragged():
    if gc.drag is True:
        if gc.current_checker is not None:
            gc.current_checker.circle_x = mouseX
            gc.current_checker.circle_y = mouseY


def mouseReleased():
    if gc.drag is True:
        gc.mouse_release(mouseX, mouseY)
        gc.drag = False


def input(self, message=''):
    from javax.swing import JOptionPane
    return JOptionPane.showInputDialog(frame, message)
