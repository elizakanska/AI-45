from tkinter import *
import random
from tkinter import ttk
import time
import copy


class GameState:
    def __init__(self, numbers: list, scores: list, is_maximizing_player: bool):
        """Initializes the game state

        Args:
            numbers (list): row of numbers
            scores (list): scores of the players
            is_maximizing_player (bool): True if it is the turn of computer, False if it is the turn of human
        """
        self.numbers = numbers
        self.scores = scores
        self.is_maximizing_player = is_maximizing_player
        self.checked_nodes = 0

    def get_possible_moves(self) -> list:
        """Generates all possible moves

        Returns:
            list: list of all possible moves
        """
        moves = []
        if len(self.numbers) > 1:
            for i in range(len(self.numbers) - 1):
                for j in range(i + 1, len(self.numbers)):
                    if [i + 1, j + 1] in [
                        [1, 2],
                        [3, 4],
                        [5, 6],
                        [7, 8],
                        [9, 10],
                        [11, 12],
                        [13, 14],
                        [15, 16],
                        [17, 18],
                        [19, 20],
                        [21, 22],
                        [23, 24],
                    ]:
                        new_numbers = (
                            self.numbers[:i]
                            + [self.numbers[i] + self.numbers[j]]
                            + self.numbers[i + 1 : j]
                            + self.numbers[j + 1 :]
                        )
                        new_numbers = [
                            (x - 1) % 6 + 1 if x > 6 else x for x in new_numbers
                        ]
                        moves.append(
                            GameState(
                                new_numbers,
                                self.scores.copy(),
                                not self.is_maximizing_player,
                            )
                        )
            if len(self.numbers) % 2 != 0:
                moves.append(
                    GameState(
                        self.numbers[:-1],
                        self.scores.copy(),
                        not self.is_maximizing_player,
                    )
                )
        return moves

    def is_terminal(self) -> bool:
        """Checks if the state is terminal

        Returns:
            bool: True if the state is terminal, False otherwise
        """
        return len(self.numbers) == 1

    def evaluate(self) -> int:
        """Evaluates the state

        Returns:
            int: score of the state
        """
        return sum(self.scores)

    def min_max(self, state: "GameState", depth: int) -> list:
        """Min-Max algorithm

        Args:
            state (GameState): current state
            depth (int): current depth

        Returns:
            list: (score, best_move)
        """
        if state.is_terminal() or depth == 0:
            return [state.evaluate(), None]
        if state.is_maximizing_player:
            max_eval = float("-inf")
            best_move = None
            for move in state.get_possible_moves():
                self.checked_nodes += 1  # Increment checked nodes count
                eval, _ = self.min_max(move, depth - 1)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
            return [max_eval, best_move]
        else:
            min_eval = float("inf")
            best_move = None
            for move in state.get_possible_moves():
                self.checked_nodes += 1  # Increment checked nodes count
                eval, _ = self.min_max(move, depth - 1)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
            return [min_eval, best_move]

    def alpha_beta(
        self, state: "GameState", alpha: int, beta: int, depth: int
    ) -> tuple:
        """Alpha-Beta algorithm

        Args:
            state (GameState): current state
            alpha (int):  minimum score that the maximizing player is assured of
            beta (int): maximum score that the minimizing player is assured of
            depth (int): current depth

        Returns:
            tuple: (score, best_move)
                    score - score of the state
                    best_move - best move
        """
        if state.is_terminal() or depth == 0:
            return state.evaluate(), None
        if state.is_maximizing_player:
            max_eval = float("-inf")
            best_move = None
            for move in state.get_possible_moves():
                self.checked_nodes += 1  # Increment checked nodes count
                eval, _ = self.alpha_beta(move, alpha, beta, depth - 1)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = float("inf")
            best_move = None
            for move in state.get_possible_moves():
                self.checked_nodes += 1  # Increment checked nodes count
                eval, _ = self.alpha_beta(move, alpha, beta, depth - 1)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, best_move

    def generate_min_max(self, numbers: list, scores: list, max_depth: int) -> list:
        """Generates the best move using Min-Max

        Args:
            numbers (list): row of numbers
            scores (list): scores of the players
            max_depth (int): maximum depth

        Returns:
            list: best move
        """
        initial_state = GameState(numbers, scores, True)
        self.checked_nodes = 0  # Reset checked nodes count
        result = self.min_max(initial_state, max_depth)
        if result[1] is not None:
            for i in range(len(numbers)):
                if numbers[i] != result[1].numbers[i]:
                    return [True, i]
        else:
            return [False, None]

    def generate_alpha_beta(self, numbers: list, scores: list, max_depth: int) -> list:
        """Generates the best move using Alpha-Beta

        Args:
            numbers (list): row of numbers
            scores (list): scores of the players
            max_depth (int): maximum depth

        Returns:
            list: best move
        """
        initial_state = GameState(numbers, scores, True)
        self.checked_nodes = 0  # Reset checked nodes count
        result = self.alpha_beta(initial_state, float("-inf"), float("inf"), max_depth)
        if result[1] is not None:
            for i in range(len(numbers)):
                try:
                    if numbers[i] != result[1].numbers[i]:
                        return [True, i]
                except:
                    return [True, i]
        else:
            return [False, None]


class Game:
    def __init__(self):
        self.pairs = {
            1: 1,
            2: 2,
            3: 3,
            4: 1,
            5: 2,
            6: 3,
            7: 1,
            8: 2,
            9: 3,
            10: 4,
            11: 5,
            12: 6,
        }
        self.alpha_beta = False
        self.checked = 0
        self.root = Tk()
        self.root.title("Game")
        self.root.geometry("1000x600")
        self.root.resizable(width=False, height=False)

        self.humanScore = 0
        self.computerScore = 0
        self.numberRow = []

        self.btn_NewGame = Button(
            self.root, text="New game", font="Arial 15", command=self.new_game
        )
        self.btn_NewGame.place(relx=0.5, rely=0.07, anchor=CENTER)

        self.cbox_length = ttk.Combobox(
            self.root, state="readonly", font="Arial 14", width=5
        )
        lengths = [i for i in range(15, 26)]
        self.cbox_length["values"] = lengths

        self.cbox_alpha_beta = ttk.Combobox(
            self.root, state="readonly", font="Arial 14", width=10
        )
        algorithm = ["Alpha-Beta", "Minimax"]
        self.cbox_alpha_beta["values"] = algorithm

        self.lbl_alpha_beta = Label(
            self.root, text="Please choose algorithm:", font="Arial 14"
        )

        self.lbl_length = Label(
            self.root,
            text="Please choose the length of number row (between 15 and 25):",
            font="Arial 14",
        )

        self.btn_enter = Button(
            self.root, text="Enter", font="Arial 14", padx=5, command=self.create_row
        )

        self.lbl_row = Label(self.root, text="", font="Arial 18")

        self.lbl_whoStarts = Label(self.root, text="Who starts?", font="Arial 15")
        self.btn_computer = Button(
            self.root,
            text="Computer",
            font="Arial 14",
            width=8,
            command=lambda: self.start_game("computer"),
        )
        self.btn_you = Button(
            self.root,
            text="You",
            font="Arial 14",
            width=7,
            command=lambda: self.start_game("human"),
        )

        self.cbox_desired_pair = ttk.Combobox(
            self.root, font="Arial 14", width=5, state="readonly"
        )
        self.btn_sum = Button(
            self.root, text="Summarize", font="Arial 14", command=self.human_turn_sum
        )
        self.btn_erase = Button(
            self.root, text="Erase", font="Arial 14", command=self.human_turn_erase
        )

        self.lbl_human_score = Label(self.root, text="Your score:", font="Arial 15")
        self.lbl_computer_score = Label(
            self.root, text="Computer score:", font="Arial 15"
        )
        self.lbl_human_counter = Label(self.root, text="0", font="Arial 15")
        self.lbl_computer_counter = Label(self.root, text="0", font="Arial 15")

        self.lbl_game_result = Label(self.root, text="", font="Arial 40")

        self.root.mainloop()

    def new_game(self):
        for element in self.root.winfo_children():
            if element != self.btn_NewGame:
                element.place_forget()
        self.lbl_length.place(x=30, y=90)
        self.cbox_length.place(x=30, y=135)
        self.cbox_length.set("")
        self.lbl_alpha_beta.place(x=30, y=180)
        self.cbox_alpha_beta.place(x=30, y=225)
        self.cbox_alpha_beta.set("")
        self.cbox_desired_pair.set("")
        self.btn_enter.place(x=30, y=270)
        self.lbl_computer_counter.config(text="0")
        self.lbl_human_counter.config(text="0")
        self.numberRow = []
        self.humanScore = 0
        self.computerScore = 0
        self.btn_erase["state"] = "normal"

    def create_row(self):
        row_length = self.cbox_length.get()
        if self.cbox_alpha_beta.get() == "Alpha-Beta":
            self.alpha_beta = True
        else:
            self.alpha_beta = False

        if not row_length.isdigit():
            pass
        else:
            new_array = [random.randint(1, 6) for _ in range(int(row_length))]
            self.numberRow = new_array
            self.lbl_row.config(text=" ".join(map(str, self.numberRow)))
            self.lbl_row.place(relx=0.5, rely=0.4, anchor=CENTER)
            self.lbl_length.place_forget()
            self.btn_enter.place_forget()
            self.cbox_length.place_forget()
            self.lbl_alpha_beta.place_forget()
            self.cbox_alpha_beta.place_forget()
            self.who_starts()

    def who_starts(self):
        self.lbl_whoStarts.place(x=40, y=90)
        self.btn_you.place(x=40, y=130)
        self.btn_computer.place(x=140, y=130)

    def start_game(self, who_starts):
        self.lbl_whoStarts.place_forget()
        self.btn_you.place_forget()
        self.btn_computer.place_forget()
        self.cbox_desired_pair.place(x=400, y=350)
        self.btn_sum.place(x=500, y=347)
        self.btn_erase.place(x=500, y=400)
        self.lbl_human_score.place(x=40, y=400)
        self.lbl_human_counter.place(x=40, y=430)
        self.lbl_computer_score.place(x=800, y=400)
        self.lbl_computer_counter.place(x=800, y=430)
        length = len(self.numberRow)
        if who_starts == "human":
            if length % 2 == 0:
                self.btn_erase["state"] = "disabled"
                cbox_pairs = [i for i in range(1, int(length / 2 + 1))]
                self.cbox_desired_pair["values"] = cbox_pairs
            else:
                cbox_pairs = [i for i in range(1, int((length - 1) / 2 + 1))]
                self.cbox_desired_pair["values"] = cbox_pairs
        else:
            if length % 2 == 1:
                self.btn_erase["state"] = "disabled"
            self.computer_turn()

    def human_turn_sum(self):
        index = self.cbox_desired_pair.get()
        if not index.isdigit():
            pass
        else:
            index = int(self.cbox_desired_pair.get()) * 2 - 2
            new_number = self.sum_pair(index)
            if new_number == 1 or new_number == 2 or new_number == 3:
                self.humanScore += 1
                self.lbl_human_counter.config(text=self.humanScore)
            else:
                self.humanScore += 2
                self.lbl_human_counter.config(text=self.humanScore)
            if len(self.numberRow) > 1:
                self.computer_turn()
            else:
                self.game_end()

    def sum_pair(self, index):
        number1 = self.numberRow.pop(index + 1)
        number2 = self.numberRow.pop(index)
        sum = number1 + number2
        new_number = self.pairs[sum]
        self.numberRow.insert(index, new_number)
        self.lbl_row.config(text=" ".join(map(str, self.numberRow)))
        return new_number

    def human_turn_erase(self):
        self.numberRow.pop()
        self.lbl_row.config(text=" ".join(map(str, self.numberRow)))
        self.computerScore -= 1
        self.lbl_computer_counter.config(text=self.computerScore)
        if len(self.numberRow) > 1:
            self.computer_turn()
        else:
            self.game_end()

    def computer_turn(self):
        
        self.root.update()
        time.sleep(1)
        game_state = GameState(
            self.numberRow, [self.humanScore, self.computerScore], True
        )
        scores = [self.humanScore, self.computerScore]
        if not self.alpha_beta:
            result = game_state.generate_min_max(self.numberRow, scores, 2)
            if hasattr(game_state, "checked_nodes"):
                print("Number of checked nodes:", game_state.checked_nodes)
            if result[0]:
                self.computer_turn_sum(result[1])
            else:
                self.computer_turn_erase()
        else:
            result = game_state.generate_alpha_beta(self.numberRow, scores, 2)
            if hasattr(game_state, "checked_nodes"):
                print("Number of checked nodes:", game_state.checked_nodes)
            if result[0]:
                self.computer_turn_sum(result[1])
            else:
                self.computer_turn_erase()

    def computer_turn_sum(self, index=None):
        length = len(self.numberRow)
        if index is None:
            index = random.randint(0, int((length - 2) / 2)) * 2
        new_number = self.sum_pair(index)
        if new_number == 1 or new_number == 2 or new_number == 3:
            self.computerScore += 1
            self.lbl_computer_counter.config(text=self.computerScore)
        else:
            self.computerScore += 2
            self.lbl_computer_counter.config(text=self.computerScore)
        length = len(self.numberRow)
        if length < 2:
            self.game_end()
        else:
            length = len(self.numberRow)
            if length % 2 == 0:
                cbox_pairs = [i for i in range(1, int(length / 2 + 1))]
                self.cbox_desired_pair["values"] = cbox_pairs
            else:
                cbox_pairs = [i for i in range(1, int((length - 1) / 2 + 1))]
                self.cbox_desired_pair["values"] = cbox_pairs
            self.cbox_desired_pair.set("")

    def computer_turn_erase(self):
        self.numberRow.pop()
        self.lbl_row.config(text=" ".join(map(str, self.numberRow)))
        self.humanScore -= 1
        self.lbl_human_counter.config(text=self.humanScore)
        length = len(self.numberRow)
        if length < 2:
            self.game_end()
        else:
            if length % 2 == 0:
                cbox_pairs = [i for i in range(1, int(length / 2 + 1))]
                self.cbox_desired_pair["values"] = cbox_pairs
            else:
                cbox_pairs = [i for i in range(1, int((length - 1) / 2 + 1))]
                self.cbox_desired_pair["values"] = cbox_pairs
            self.cbox_desired_pair.set("")

    def game_end(self):
        self.lbl_row.place_forget()
        self.cbox_desired_pair.place_forget()
        self.btn_sum.place_forget()
        self.btn_erase.place_forget()
        if self.humanScore > self.computerScore:
            self.lbl_game_result.config(text="You win!", fg="blue")
            self.lbl_game_result.place(relx=0.5, rely=0.4, anchor=CENTER)
        elif self.humanScore < self.computerScore:
            self.lbl_game_result.config(text="You lose!", fg="red")
            self.lbl_game_result.place(relx=0.5, rely=0.4, anchor=CENTER)
        else:
            self.lbl_game_result.config(text="Tie!", fg="green")
            self.lbl_game_result.place(relx=0.5, rely=0.4, anchor=CENTER)


def main():
    Game()


if __name__ == "__main__":
    main()

