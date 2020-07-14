import random

class Player:
    def __init__(self, shape):
        self.shape = shape
        self.row = 0
        self.col = 0
        self.num_moves = 0
        self.played = False

    def make_move(self, cells):
        cells[-self.row][self.col-1] = self.shape
        self.num_moves += 1
        self.played = not self.played

class User(Player):
    def take_input(self, cells):
        while True:
            input_val = input("Enter the coordinates: ").split()
            if input_val[0].isdigit():
                col, row = int(input_val[0]), int(input_val[1])
                if any(x < 1 or x > 3 for x in [col, row]):
                    print("Coordinates should be from 1 to 3!")
                elif cells[-row][col-1] != "_":
                    print("This cell is occupied! Choose another one!")
                else:
                    self.row, self.col = row, col
                    break
            else:
                print("You should enter numbers!")


class Computer(Player):
    def take_input(self, cells):
        print("Making move level \"easy\"\n")
        while True:
            row, col = random.randint(1, 3), random.randint(1, 3)
            if cells[-row][col-1] == "_":
                self.row, self.col = row, col
                break

class Game2:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.num_moves = player1.num_moves + player2.num_moves
        self.cells = [list('___') for i in range(3)]

    def play(self):
        self.print_cells()
        while True:
            if self.playerAction(self.player1):
                break
            if self.playerAction(self.player2):
                break


    def playerAction(self, player):
        player.take_input(self.cells)
        player.make_move(self.cells)
        self.num_moves += 1
        self.print_cells()
        if self.check_win(player.shape):
            print(player.shape, "wins\n")
            return True
        if self.num_moves == 9:
            print("Draw\n")
            return True
        return False

    def print_cells(self):
        border = ['-' * 9]
        out_str = border + [" ".join(['|'] + x + ['|']) for x in self.cells] + border
        print("\n".join([x.replace("_", " ") for x in out_str]))

    def check_win(self, shape):
        if any([all([y == shape for y in x]) for x in self.cells]):
            return True
        if any([all([self.cells[j][i] == shape for j in range(3)]) for i in range(3)]):
            return True
        if all([self.cells[i][i] == shape for i in range(3)]):
            return True
        if all([self.cells[i][-i-1] == shape for i in range(3)]):
            return True
        return False



while True:
    input_list = input("Input command: ").split()
    if input_list[0] == 'exit' and len(input_list) == 1:
        break
    elif input_list[0] == 'start' and len(input_list) == 3 \
            and input_list[1] in ['easy', 'user'] \
            and input_list[2] in ['easy', 'user']:
        command_bool = True
        if input_list[1] == 'easy':
            player1 = Computer("X")
        else:
            player1 = User("X")
        if input_list[2] == 'easy':
            player2 = Computer("O")
        else:
            player2 = User("O")
        my_game = Game2(player1, player2)
        my_game.play()
    else:
        print("Bad parameters!")


