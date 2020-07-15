import random


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Board:
    def __init__(self):
        self.cells = dict()

    def print(self):
        border = ['-' * 9]
        frame = border + [" ".join(['|'] + [self.get_value(Position(i, j)) for i in range(1, 4)] + ['|']) for j in reversed(range(1, 4))] + border
        print("\n".join(frame))

    def add_value(self, position, value):
        self.cells[(position.x, position.y)] = value

    def get_value(self, position):
        return self.cells.get((position.x, position.y), " ")

    def delete_value(self, position):
        del self.cells[(position.x, position.y)]


class Player:
    def __init__(self, value, board):
        self.value = value
        self.board = board
        self.position = None
        self.played = False

    def take_input(self):
        pass

    def make_move(self):
        self.board.add_value(self.position, self.value)
        self.played = not self.played

    def check_win(self, value):
        if any([all([self.board.get_value(Position(i, j)) == value for i in range(1, 4)]) for j in range(1, 4)]):
            return True
        if any([all([self.board.get_value(Position(i, j)) == value for j in range(1, 4)]) for i in range(1, 4)]):
            return True
        if all([self.board.get_value(Position(i, i)) == value for i in range(1, 4)]):
            return True
        if all([self.board.get_value(Position(i, 4 - i)) == value for i in range(1, 4)]):
            return True
        return False

    def play(self):
        self.take_input()
        self.make_move()
        self.board.print()
        if self.check_win(self.value):
            print(self.value, "wins\n")
            return True
        if len(self.board.cells) == 9:
            print("Draw\n")
            return True
        return False

    def set_random_input(self):
        while True:
            loc_position = Position(random.randint(1, 3), random.randint(1, 3))
            if self.board.get_value(loc_position) == ' ':
                self.position = loc_position
                break


class User(Player):
    def take_input(self):
        while True:
            input_val = input("Enter the coordinates: ").split()
            if input_val[0].isdigit():
                x, y = int(input_val[0]), int(input_val[1])
                if any(x < 1 or x > 3 for x in [x, y]):
                    print("Coordinates should be from 1 to 3!")
                elif self.board.get_value(Position(x, y)) != ' ':
                    print("This cell is occupied! Choose another one!")
                else:
                    self.position = Position(x, y)
                    break
            else:
                print("You should enter numbers!")


class Easy(Player):
    def take_input(self):
        print("Making move level \"easy\"\n")
        self.set_random_input()


class Medium(Player):
    def take_input(self):
        print("Making move level \"medium\"\n")

        if not self.check_move_ahead():
            self.set_random_input()

    def check_move_ahead(self):
        return self.one_move_win() or self.opponent_win()

    def one_move_win(self):
        for i in range(1, 4):
            for j in range(1, 4):
                t_pos = Position(i, j)
                if self.board.get_value(t_pos) == ' ' and \
                        self.test_win(t_pos, self.value):
                    self.board.add_value(t_pos, self.value)
                    return True
        return False

    def opponent_win(self):
        for i in range(1, 4):
            for j in range(1, 4):
                t_pos = Position(i, j)
                if self.board.get_value(t_pos) == ' ':
                    o_value = 'O' if self.value == 'X' else 'X'
                    if self.test_win(t_pos, o_value):
                        self.board.add_value(t_pos, self.value)
                        return True
        return False

    def test_win(self, position, value):
        self.board.add_value(position, value)
        is_win = self.check_win(value)
        self.board.delete_value(position)
        return is_win


class Game:
    def __init__(self):
        self.player1 = None
        self.player2 = None
        self.board = Board()
        self.player_modes = {'easy': Easy, 'user': User, 'medium': Medium}

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
