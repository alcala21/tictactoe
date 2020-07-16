import random

class Board:
    def __init__(self):
        self.used_cells = dict()
        self.empty_cells = [(i, j) for i in range(1, 4) for j in range(1, 4)]

    def print(self):
        border = ['-' * 9]
        frame = border + [" ".join(['|'] + [self.get_value((i, j)) for i in range(1, 4)] + ['|']) for j in reversed(range(1, 4))] + border
        print("\n".join(frame))

    def add_value(self, position, value):
        self.used_cells[position] = value
        self.empty_cells.remove(position)

    def get_value(self, position):
        return self.used_cells.get(position, " ")

    def delete_value(self, position):
        del self.used_cells[position]
        self.empty_cells.append(position)

    def is_occupied(self, position):
        if position in self.used_cells:
            return True


class Player:
    def __init__(self, value, board):
        self.value = value
        self.board = board
        self.position = None
        self.o_value = 'O' if self.value == 'X' else 'X'

    def take_input(self):
        pass

    def make_move(self):
        self.board.add_value(self.position, self.value)

    def check_win(self, value):
        if any([all([self.board.get_value((i, j)) == value for i in range(1, 4)]) for j in range(1, 4)]):
            return True
        if any([all([self.board.get_value((i, j)) == value for j in range(1, 4)]) for i in range(1, 4)]):
            return True
        if all([self.board.get_value((i, i)) == value for i in range(1, 4)]):
            return True
        if all([self.board.get_value((i, 4 - i)) == value for i in range(1, 4)]):
            return True
        return False

    def play(self):
        if self.__str__():
            print(self.__str__())
        self.take_input()
        self.make_move()
        self.board.print()
        if self.check_win(self.value):
            print(self.value, "wins\n")
            return True
        if len(self.board.used_cells) == 9:
            print("Draw\n")
            return True
        return False

    def set_random_input(self):
        while True:
            loc_position = (random.randint(1, 3), random.randint(1, 3))
            if self.board.get_value(loc_position) == ' ':
                self.position = loc_position
                break

    def __str__(self):
        pass


class User(Player):
    def take_input(self):
        while True:
            input_val = input("Enter the coordinates: ").split()
            if input_val[0].isdigit():
                x, y = int(input_val[0]), int(input_val[1])
                if any(x < 1 or x > 3 for x in [x, y]):
                    print("Coordinates should be from 1 to 3!")
                elif self.board.is_occupied((x, y)):
                    print("This cell is occupied! Choose another one!")
                else:
                    self.position = (x, y)
                    break
            else:
                print("You should enter numbers!")


class Easy(Player):
    def __str__(self):
        return "Making move level \"easy\"\n"

    def take_input(self):
        self.set_random_input()


class Medium(Player):
    def __str__(self):
        return "Making move level \"medium\"\n"

    def take_input(self):
        if not self.check_move_ahead():
            self.set_random_input()

    def check_move_ahead(self):
        return self.one_move_win(self.value) or self.one_move_win(self.o_value)

    def one_move_win(self, value):
        for (i, j) in self.board.empty_cells[:]:
            t_pos = (i, j)
            if self.test_win(t_pos, value):
                self.position = t_pos
                return True
        return False

    def test_win(self, position, value):
        self.board.add_value(position, value)
        is_win = self.check_win(value)
        self.board.delete_value(position)
        return is_win

class Hard(Player):
    def __str__(self):
        return "Making move level \"hard\"\n"

    def take_input(self):
        self.set_random_input()


class Game:
    def __init__(self):
        self.player1 = None
        self.player2 = None
        self.board = Board()
        self.player_modes = {'user': User, 'easy': Easy,
                             'medium': Medium, 'hard': Hard}

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
