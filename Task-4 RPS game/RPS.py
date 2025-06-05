import tkinter as tk
from tkinter import messagebox
import random

class RPSGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🎮 Rock Paper Scissors Game")
        self.root.geometry("600x500")
        self.root.config(bg="yellow")
        self.root.resizable(False, False)

        self.choices = ['Rock', 'Paper', 'Scissors']
        self.icons = {'Rock': '🪨', 'Paper': '📄', 'Scissors': '✂️'}

        self.user_score = 0
        self.computer_score = 0
        self.round = 1
        self.total_rounds = 5
        self.game_active = True

        self.build_ui()

    def build_ui(self):
        tk.Label(self.root, text="Rock Paper Scissors", font=('Times New Roman', 22, 'bold'),
                 bg="yellow", fg="black").pack(pady=15)

        self.round_label = tk.Label(self.root, text=f"Round {self.round}/{self.total_rounds}",
                                    font=('Times New Roman', 16, 'bold'), bg="yellow", fg="black")
        self.round_label.pack()

        btn_frame = tk.Frame(self.root, bg="yellow")
        btn_frame.pack(pady=20)

        self.buttons = {}
        colors = {'Rock': '#e74c3c', 'Paper': '#e67e22', 'Scissors': '#2ecc71'}

        for idx, choice in enumerate(self.choices):
            btn = tk.Button(
                btn_frame,
                text=f"{self.icons[choice]} {choice}",
                font=('Times New Roman', 14, 'bold'),
                width=12,
                command=lambda c=choice: self.play_round(c),
                bg=colors[choice],
                fg="white",
                activebackground="black"
            )
            btn.grid(row=0, column=idx, padx=15)
            self.buttons[choice] = btn

        self.result_text = tk.Label(self.root, text="", font=('Times New Roman', 18, 'bold'), bg="yellow", fg="black")
        self.result_text.pack(pady=15)

        self.user_choice_label = tk.Label(self.root, text="You: ", font=('Times New Roman', 14, 'bold'),
                                          bg="yellow", fg="black")
        self.user_choice_label.pack()

        self.computer_choice_label = tk.Label(self.root, text="Computer: ", font=('Times New Roman', 14, 'bold'),
                                              bg="yellow", fg="black")
        self.computer_choice_label.pack()

        self.score_label = tk.Label(self.root, text="Score - You: 0 | Computer: 0",
                                    font=('Times New Roman', 14, 'bold'), bg="yellow", fg="black")
        self.score_label.pack(pady=10)

        self.reset_btn = tk.Button(self.root, text="🔁 Reset Game", font=('Times New Roman', 12, 'bold'),
                                   bg="black", fg="white", command=self.reset_game)
        self.reset_btn.pack(pady=10)

    def play_round(self, user_choice):
        if not self.game_active:
            return

        self.disable_buttons()
        comp_choice = random.choice(self.choices)
        result = self.get_result(user_choice, comp_choice)

        self.user_choice_label.config(text=f"You: {self.icons[user_choice]} {user_choice}")
        self.computer_choice_label.config(text=f"Computer: {self.icons[comp_choice]} {comp_choice}")
        self.result_text.config(text=result)

        if result == "You Win!":
            self.user_score += 1
        elif result == "You Lose!":
            self.computer_score += 1

        self.score_label.config(text=f"Score - You: {self.user_score} | Computer: {self.computer_score}")

        self.round += 1
        self.update_round()
        self.root.after(1500, self.check_game_over)

    def get_result(self, user, comp):
        if user == comp:
            return "It's a Tie!"
        elif (user == 'Rock' and comp == 'Scissors') or \
             (user == 'Scissors' and comp == 'Paper') or \
             (user == 'Paper' and comp == 'Rock'):
            return "You Win!"
        else:
            return "You Lose!"

    def update_round(self):
        if self.round <= self.total_rounds:
            self.round_label.config(text=f"Round {self.round}/{self.total_rounds}")
        else:
            self.round_label.config(text="Final Round!")

    def check_game_over(self):
        if self.round > self.total_rounds:
            self.game_active = False
            if self.user_score > self.computer_score:
                final = "🎉 You Won the Match!"
            elif self.user_score < self.computer_score:
                final = "😞 You Lost the Match!"
            else:
                final = "🤝 It's a Draw!"

            messagebox.showinfo("Game Over", f"{final}\nFinal Score:\nYou: {self.user_score} | Computer: {self.computer_score}")
        else:
            self.enable_buttons()

    def reset_game(self):
        self.user_score = 0
        self.computer_score = 0
        self.round = 1
        self.game_active = True

        self.user_choice_label.config(text="You: ")
        self.computer_choice_label.config(text="Computer: ")
        self.result_text.config(text="")
        self.score_label.config(text="Score - You: 0 | Computer: 0")
        self.round_label.config(text=f"Round {self.round}/{self.total_rounds}")
        self.enable_buttons()

    def disable_buttons(self):
        for btn in self.buttons.values():
            btn.config(state='disabled')

    def enable_buttons(self):
        for btn in self.buttons.values():
            btn.config(state='normal')


# Launch the game
root = tk.Tk()
game = RPSGame(root)
root.mainloop()
