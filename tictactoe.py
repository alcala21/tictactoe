import random

class Board:
    def __init__(self):
        self.cells = dict()

    def print(self):
        border = ['-' * 9]
        frame = border + [" ".join(['|'] + [self.cells.get((i, j), ' ') for j in range(3)] + ['|']) for i in range(3)] + border
        print("\n".join(frame))

    def fill_position(self, row, col, value):
        self.cells[(3-row, col - 1)] = value


class Player:
    def __init__(self, value, board):
        self.value = value
        self.board = board
        self.row = 0
        self.col = 0
        self.played = False

    def take_input(self):
        pass

    def make_move(self):
        self.board.fill_position(self.row, self.col, self.value)
        self.played = not self.played

    def check_win(self):
        if any([all([self.board.cells.get((i, j), "") == self.value for j in range(3)]) for i in range(3)]):
            return True
        if any([all([self.board.cells.get((j, i), "") == self.value for j in range(3)]) for i in range(3)]):
            return True
        if all([self.board.cells.get((i, i), "") == self.value for i in range(3)]):
            return True
        if all([self.board.cells.get((i, 3-i-1)) == self.value for i in range(3)]):
            return True
        return False

    def play(self):
        self.take_input()
        self.make_move()
        self.board.print()
        if self.check_win():
            print(self.value, "wins\n")
            return True
        if len(self.board.cells) == 9:
            print("Draw\n")
            return True
        return False


class User(Player):
    def take_input(self):
        while True:
            input_val = input("Enter the coordinates: ").split()
            if input_val[0].isdigit():
                col, row = int(input_val[0]), int(input_val[1])
                if any(x < 1 or x > 3 for x in [col, row]):
                    print("Coordinates should be from 1 to 3!")
                elif self.board.cells.get((3-row, col-1), '') != '':
                    print("This cell is occupied! Choose another one!")
                else:
                    self.row, self.col = row, col
                    break
            else:
                print("You should enter numbers!")

class Computer(Player):
    def take_input(self):
        print("Making move level \"easy\"\n")
        while True:
            col, row = random.randint(1, 3), random.randint(1, 3)
            if self.board.cells.get((3-row, col-1), '') == '':
                self.row, self.col = row, col
                break

class Game:
    def __init__(self):
        self.player1 = None
        self.player2 = None
        self.board = Board()
        self.player_modes = {'easy': Computer, 'user': User}

    def play(self):
        while self.select_players():
            self.board.print()
            while True:
                if self.player1.play():
                    break
                if self.player2.play():
                    break

    def select_players(self):
        select_bool = False
        while True:
            input_list = input("Input command: ").split()
            if input_list[0] == 'exit' and len(input_list) == 1:
                break
            elif input_list[0] == 'start' and len(input_list) == 3 \
                    and input_list[1] in self.player_modes \
                    and input_list[2] in self.player_modes:
                select_bool = True
                self.board = Board()
                self.player1 = self.player_modes[input_list[1]]("X", self.board)
                self.player2 = self.player_modes[input_list[2]]("O", self.board)
                break
            else:
                print("Bad parameters!")
        return select_bool

Game().play()