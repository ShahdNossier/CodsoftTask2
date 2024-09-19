import tkinter as tk
import random

# Global Variables
game_over = False
current_player = 'X'  # Player 'X' starts
color_blue = "#4584b6"
color_yellow = "#ffde57"
color_gray = "#343434"
color_light_gray = "#646464"

def start_game():
    global game_over, current_player
    game_over = False
    current_player = 'X'
    for row in range(3):
        for col in range(3):
            board[row][col]['text'] = ''
            board[row][col].config(foreground=color_blue, background=color_gray)
    label.config(text=f"{current_player}'s turn")

def set_tile(row, col):
    global game_over, current_player
    if board[row][col]['text'] == '' and not game_over:
        board[row][col]['text'] = current_player
        if check_winner(current_player):
            label.config(text=f"{current_player} wins!", foreground=color_yellow)
            game_over = True
        elif all(board[r][c]['text'] != '' for r in range(3) for c in range(3)):
            label.config(text="It's a draw!", foreground=color_yellow)
            game_over = True
        else:
            current_player = 'O' if current_player == 'X' else 'X'
            label.config(text=f"{current_player}'s turn")
            if current_player == 'O':
                window.after(500, ai_move)

def ai_move():
    empty_tiles = [(row, col) for row in range(3) for col in range(3) if board[row][col]['text'] == '']
    if empty_tiles:
        row, col = random.choice(empty_tiles)
        set_tile(row, col)

def check_winner(symbol):
    # Check rows, columns, and diagonals for a winner
    win_positions = [
        [(r, c) for c in range(3)] for r in range(3)
    ] + [
        [(r, c) for r in range(3)] for c in range(3)
    ] + [
        [(i, i) for i in range(3)],
        [(i, 2-i) for i in range(3)]
    ]
    for positions in win_positions:
        if all(board[r][c]['text'] == symbol for r, c in positions):
            for r, c in positions:
                board[r][c].config(foreground=color_yellow, background=color_light_gray)
            return True
    return False

def new_game():
    start_game()

# Initialize game window and components
window = tk.Tk()
window.title('Tic Tac Toe')
window.resizable(False, False)

frame = tk.Frame(window)
label = tk.Label(frame, text=f"{current_player}'s turn", font=('Consolas', 20), background=color_gray, foreground='white')

label.grid(row=0, column=0, columnspan=3, sticky='we')

board = [[None for _ in range(3)] for _ in range(3)]

for row in range(3):
    for col in range(3):
        board[row][col] = tk.Button(frame, text='', font=('Consolas', 50, 'bold'),
                                    background=color_gray, foreground=color_blue, width=4, height=1,
                                    command=lambda row=row, col=col: set_tile(row, col))
        board[row][col].grid(row=row + 1, column=col)

button = tk.Button(frame, text='Restart', font=('Consolas', 20), background=color_gray,
                   foreground='white', command=new_game)
button.grid(row=4, column=0, columnspan=3, sticky='we')

frame.pack()

# Center the window
window.update()
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window_x = int((screen_width / 2) - (window_width / 2))
window_y = int((screen_height / 2) - (window_height / 2))
window.geometry(f'{window_width}x{window_height}+{window_x}+{window_y}')

window.mainloop()

