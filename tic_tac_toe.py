import tkinter as tk
from tkinter import messagebox

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe")
        self.root.resizable(False, False)

        # Zones de saisie pour les noms des joueurs
        player1_label = tk.Label(root, text="Nom du joueur 1:")
        player1_label.grid(row=0, column=0, padx=10, pady=5)
        self.player1_entry = tk.Entry(root)
        self.player1_entry.grid(row=0, column=1, padx=10, pady=5)

        player2_label = tk.Label(root, text="Nom du joueur 2:")
        player2_label.grid(row=1, column=0, padx=10, pady=5)
        self.player2_entry = tk.Entry(root)
        self.player2_entry.grid(row=1, column=1, padx=10, pady=5)

        # Bouton de démarrage du jeu
        start_button = tk.Button(root, text="Commencer le jeu", command=self.start_game)
        start_button.grid(row=2, columnspan=2, padx=10, pady=5)

        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.current_player = None
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.player1_name = ""
        self.player2_name = ""

    def start_game(self):
        # Vérifier que les noms des joueurs ont été entrés
        self.player1_name = self.player1_entry.get()
        self.player2_name = self.player2_entry.get()
        if not self.player1_name or not self.player2_name:
            messagebox.showerror("Erreur", "Veuillez entrer les noms des deux joueurs.")
            return

        # Mettre à jour l'interface pour afficher les noms des joueurs
        self.player1_entry.config(state="disabled")
        self.player2_entry.config(state="disabled")
        self.player1_entry.grid_forget()
        self.player2_entry.grid_forget()
        player1_label = tk.Label(self.root, text=f"Joueur 1: {self.player1_name}")
        player1_label.grid(row=0, column=0, padx=10, pady=5)
        player2_label = tk.Label(self.root, text=f"Joueur 2: {self.player2_name}")
        player2_label.grid(row=1, column=0, padx=10, pady=5)

        # Créer le plateau de jeu
        for row in range(3):
            for col in range(3):
                button = tk.Button(self.root, text="", font='normal 20 bold', width=5, height=2,
                                   command=lambda row=row, col=col: self.click(row, col))
                button.grid(row=row+3, column=col, padx=5, pady=5)
                self.buttons[row][col] = button

        # Initialiser le joueur actuel
        self.current_player = "X"

    def click(self, row, col):
        if self.buttons[row][col]["text"] == "":
            self.buttons[row][col]["text"] = self.current_player
            self.board[row][col] = self.current_player

            # Vérifier s'il y a un gagnant ou un match nul
            winner = self.check_winner()
            if winner:
                winner_name = self.player1_name if winner == "X" else self.player2_name
                messagebox.showinfo("Fin de partie", f"Le joueur {winner_name} a gagné !")
                self.reset_board()
            elif self.is_draw():
                messagebox.showinfo("Fin de partie", "Match nul !")
                self.reset_board()
            else:
                self.current_player = "O" if self.current_player == "X" else "X"

    def check_winner(self):
        for row in range(3):
            if self.board[row][0] == self.board[row][1] == self.board[row][2] != "":
                return self.board[row][0]
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != "":
                return self.board[0][col]
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != "":
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != "":
            return self.board[0][2]
        return None

    def is_draw(self):
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == "":
                    return False
        return True

    def reset_board(self):
        for row in range(3):
            for col in range(3):
                self.buttons[row][col]["text"] = ""
                self.board[row][col] = ""
        self.current_player = "X"

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
