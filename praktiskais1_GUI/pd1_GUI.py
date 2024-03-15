from tkinter import *
import random
from tkinter import ttk
import time


class Game:
    def __init__(self):
        self.root = Tk()
        self.root.title('Game')
        self.root.geometry('1000x600')
        self.root.resizable(width=False, height=False)

        self.humanScore = 0
        self.computerScore = 0
        self.numberRow = []

        self.btn_NewGame = Button(self.root, text='New game', font='Arial 15', command=self.new_game)
        self.btn_NewGame.place(relx=0.5, rely=0.07, anchor=CENTER)

        self.cbox_length = ttk.Combobox(self.root, state='readonly', font='Arial 14', width=5)
        lengths = [i for i in range(15, 26)]
        self.cbox_length['values'] = lengths

        self.lbl_length = Label(self.root,
                                text='Please choose the length of number row (between 15 and 25):', font='Arial 14')

        self.btn_enter = Button(self.root, text='Enter', font='Arial 14', padx=5, command=self.create_row)

        self.lbl_row = Label(self.root, text='', font='Arial 18')

        self.lbl_whoStarts = Label(self.root, text='Who starts?', font='Arial 15')
        self.btn_computer = Button(self.root, text='Computer', font='Arial 14', width=8,
                                   command=lambda: self.start_game("computer"))
        self.btn_you = Button(self.root, text='You', font='Arial 14', width=7, command=lambda: self.start_game("human"))

        self.cbox_desired_pair = ttk.Combobox(self.root, font='Arial 14', width=5, state='readonly')
        self.btn_sum = Button(self.root, text='Summarize', font='Arial 14', command=self.human_turn_sum)
        self.btn_erase = Button(self.root, text='Erase', font='Arial 14', command=self.human_turn_erase)

        self.lbl_human_score = Label(self.root, text='Your score:', font='Arial 15')
        self.lbl_computer_score = Label(self.root, text='Computer score:', font='Arial 15')
        self.lbl_human_counter = Label(self.root, text='0', font='Arial 15')
        self.lbl_computer_counter = Label(self.root, text='0', font='Arial 15')

        self.lbl_game_result = Label(self.root, text='', font='Arial 40')

        self.root.mainloop()

    def new_game(self):
        for element in self.root.winfo_children():
            if element != self.btn_NewGame:
                element.place_forget()
        self.lbl_length.place(x=30, y=90)
        self.cbox_length.place(x=30, y=135)
        self.cbox_length.set("")
        self.cbox_desired_pair.set("")
        self.btn_enter.place(x=130, y=130)
        self.lbl_computer_counter.config(text='0')
        self.lbl_human_counter.config(text='0')
        self.numberRow = []
        self.humanScore = 0
        self.computerScore = 0
        self.btn_erase['state'] = 'normal'

    def create_row(self):
        row_length = self.cbox_length.get()
        if not row_length.isdigit():
            pass
        else:
            new_array = [random.randint(1, 6) for _ in range(int(row_length))]
            self.numberRow = new_array
            self.lbl_row.config(text=' '.join(map(str, self.numberRow)))
            self.lbl_row.place(relx=0.5, rely=0.4, anchor=CENTER)
            self.lbl_length.place_forget()
            self.btn_enter.place_forget()
            self.cbox_length.place_forget()
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
        if who_starts == 'human':
            if length % 2 == 0:
                self.btn_erase['state'] = 'disabled'
                cbox_pairs = [i for i in range(1, int(length/2+1))]
                self.cbox_desired_pair['values'] = cbox_pairs
            else:
                cbox_pairs = [i for i in range(1, int((length-1) / 2 + 1))]
                self.cbox_desired_pair['values'] = cbox_pairs
        else:
            if length % 2 == 1:
                self.btn_erase['state'] = 'disabled'
            self.computer_turn()

    def human_turn_sum(self):
        index = self.cbox_desired_pair.get()
        if not index.isdigit():
            pass
        else:
            index = int(self.cbox_desired_pair.get())*2-2
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
        new_number = sum
        if sum > 6:
            if sum == 7:
                new_number = 1
            elif sum == 8:
                new_number = 2
            elif sum == 9:
                new_number = 3
            elif sum == 10:
                new_number = 4
            elif sum == 11:
                new_number = 5
            elif sum == 12:
                new_number = 6
        self.numberRow.insert(index, new_number)
        self.lbl_row.config(text=' '.join(map(str, self.numberRow)))
        return new_number

    def human_turn_erase(self):
        self.numberRow.pop()
        self.lbl_row.config(text=' '.join(map(str, self.numberRow)))
        self.computerScore -= 1
        self.lbl_computer_counter.config(text=self.computerScore)
        if len(self.numberRow) > 1:
            self.computer_turn()
        else:
            self.game_end()

    def computer_turn(self):
        self.root.update()
        time.sleep(1)
        length = len(self.numberRow)
        if length % 2 == 0:
            self.computer_turn_sum()

        else:
            choice = random.randint(0, 1)
            if choice == 0:
                self.computer_turn_sum()
            else:
                self.computer_turn_erase()

    def computer_turn_sum(self):
        length = len(self.numberRow)
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
                self.cbox_desired_pair['values'] = cbox_pairs
            else:
                cbox_pairs = [i for i in range(1, int((length - 1) / 2 + 1))]
                self.cbox_desired_pair['values'] = cbox_pairs
            self.cbox_desired_pair.set("")

    def computer_turn_erase(self):
        self.numberRow.pop()
        self.lbl_row.config(text=' '.join(map(str, self.numberRow)))
        self.humanScore -= 1
        self.lbl_human_counter.config(text=self.humanScore)
        length = len(self.numberRow)
        if length < 2:
            self.game_end()
        else:
            if length % 2 == 0:
                cbox_pairs = [i for i in range(1, int(length / 2 + 1))]
                self.cbox_desired_pair['values'] = cbox_pairs
            else:
                cbox_pairs = [i for i in range(1, int((length - 1) / 2 + 1))]
                self.cbox_desired_pair['values'] = cbox_pairs
            self.cbox_desired_pair.set("")

    def game_end(self):
        self.lbl_row.place_forget()
        self.cbox_desired_pair.place_forget()
        self.btn_sum.place_forget()
        self.btn_erase.place_forget()
        if self.humanScore > self.computerScore:
            self.lbl_game_result.config(text='You win!', fg='blue')
            self.lbl_game_result.place(relx=0.5, rely=0.4, anchor=CENTER)
        elif self.humanScore < self.computerScore:
            self.lbl_game_result.config(text='You lose!', fg='red')
            self.lbl_game_result.place(relx=0.5, rely=0.4, anchor=CENTER)
        else:
            self.lbl_game_result.config(text='Tie!', fg='green')
            self.lbl_game_result.place(relx=0.5, rely=0.4, anchor=CENTER)


def main():
    Game()


if __name__ == "__main__":
    main()
