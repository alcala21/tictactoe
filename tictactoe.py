import random

class Game:
    def __init__(self):
        self.cells = list()
        self.active_player = "X"
        self.num_o = 0
        self.num_x = 0
        self.row = 0
        self.col = 0

    def play(self):
        input_string = "_" * 9
        self.format_cells(input_string)
        self.print_cells()

        while True:
            self.check_active_player()
            if self.active_player == "X":
                self.user_input()
            else:
                self.computer_input()
            self.make_move()

            if self.check_win():
                print(self.active_player, "wins")
                break
            if self.num_o + self.num_x == 9:
                print("Draw")
                break

    def format_cells(self, input_string):
        cell_list = list(input_string)
        self.cells = [cell_list[i:i+3] for i in range(0, len(cell_list), 3)]
        self.num_o = len([x for x in cell_list if x == "O"])
        self.num_x = len([x for x in cell_list if x == "X"])

    def print_cells(self):
        border = ['-' * 9]
        out_str = border + [" ".join(['|'] + x + ['|']) for x in self.cells] + border
        print("\n".join([x.replace("_", " ") for x in out_str]))

    def user_input(self):
        while True:
            input_val = input("Enter the coordinates: ").split()
            if input_val[0].isdigit():
                col, row = int(input_val[0]), int(input_val[1])
                if any(x < 1 or x > 3 for x in [col, row]):
                    print("Coordinates should be from 1 to 3!")
                elif self.cells[-row][col-1] != "_":
                    print("This cell is occupied! Choose another one!")
                else:
                    self.row = row
                    self.col = col
                    break
            else:
                print("You should enter numbers!")

    def make_move(self):
        self.check_active_player()
        self.cells[-self.row][self.col-1] = self.active_player
        if self.active_player == "X":
            self.num_x += 1
        else:
            self.num_o += 1
        self.print_cells()

    def check_active_player(self):
        if self.num_o == self.num_x:
            self.active_player = "X"
        else:
            self.active_player = "O"

    def check_win(self):
        if any([all([y == self.active_player for y in x]) for x in self.cells]):
            return True
        if any([all([self.cells[j][i] == self.active_player for j in range(3)]) for i in range(3)]):
            return True
        if all([self.cells[i][i] == self.active_player for i in range(3)]):
            return True
        if all([self.cells[i][-i-1] == self.active_player for i in range(3)]):
            return True
        return False

    def computer_input(self):
        print("Making move level \"easy\"\n")
        while True:
            row = random.randint(1, 3)
            col = random.randint(1, 3)
            if self.cells[-row][col-1] == "_":
                self.row = row
                self.col = col
                break


my_game = Game()
my_game.play()
