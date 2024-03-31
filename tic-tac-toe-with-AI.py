import tkinter as tk
from tkinter import messagebox

# Define the Tic-Tac-Toe board size
BOARD_SIZE = 3

# Global variables
root = None
buttons = None
current_player = 'O'
status_label = None
reset_button = None  # Define reset_button as a global variable
win_color = "#00FF00"  # Color for winning line
tie_color = "#FF0000"  # Color for tie game

# Function to create the GUI for Tic-Tac-Toe
def create_gui():
    global root, buttons, status_label, reset_button

    root = tk.Tk()
    root.title("Tic-Tac-Toe")

    # Define colors
    bg_color = "#FFFFFF"  # Background color
    button_color = "#CCCCCC"  # Button color
    text_color = "#000000"  # Text color
    

    # Create buttons grid
    buttons = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            buttons[i][j] = tk.Button(root, text=" ", font=('Arial', 20), width=6, height=3,
                                       command=lambda row=i, col=j: on_button_click(row, col))
            buttons[i][j].grid(row=i, column=j, padx=5, pady=5)
            buttons[i][j].config(bg=button_color, fg=text_color)

    # Add labels for game status and buttons for resetting the game
    status_label = tk.Label(root, text="Player O's Turn", font=('Arial', 16))
    status_label.grid(row=BOARD_SIZE, columnspan=BOARD_SIZE, padx=5, pady=10)
    status_label.config(bg=bg_color, fg=text_color)

    reset_button = tk.Button(root, text="Reset Game", command=reset_game)
    reset_button.grid(row=BOARD_SIZE + 1, columnspan=BOARD_SIZE, padx=5, pady=10)
    reset_button.config(bg=button_color, fg=text_color)

    # Configure root background color
    root.config(bg=bg_color)

def update_status_label():
    global current_player, status_label
    
    # Highlight current player's label
    status_label.config(text=f"Player {current_player}'s Turn", bg=highlight_color(current_player))

def on_button_click(row, col):
    global current_player
    
    # Disable button after click
    buttons[row][col].config(state="disabled")
    
    if buttons[row][col]['text'] == " ":
        buttons[row][col]['text'] = current_player

        if check_winner(current_player):
            # Highlight winning line
            highlight_winning_line(current_player)
            messagebox.showinfo("Game Over", f"Player {current_player} wins!")
            disable_buttons()
            reset_button.config(state="normal")  # Enable reset button
        elif is_board_full():
            messagebox.showinfo("Game Over", "It's a tie!")
            disable_buttons()
            reset_button.config(state="normal")  # Enable reset button
        else:
            current_player = 'O' if current_player == 'X' else 'X'

            if current_player == 'X':
                ai_row, ai_col = get_ai_move()
                on_button_click(ai_row, ai_col)

    # Update the game status label
    update_status_label()

def disable_buttons():
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            buttons[i][j].config(state="disabled")

def highlight_color(player):
    return "#FFD700" if player == 'X' else "#00BFFF"

def highlight_winning_line(player):
    # Check rows
    for i in range(BOARD_SIZE):
        if all(buttons[i][j]['text'] == player for j in range(BOARD_SIZE)):
            for j in range(BOARD_SIZE):
                buttons[i][j].config(bg=win_color)
            return

    # Check columns
    for j in range(BOARD_SIZE):
        if all(buttons[i][j]['text'] == player for i in range(BOARD_SIZE)):
            for i in range(BOARD_SIZE):
                buttons[i][j].config(bg=win_color)
            return

    # Check diagonals
    if all(buttons[i][i]['text'] == player for i in range(BOARD_SIZE)):
        for i in range(BOARD_SIZE):
            buttons[i][i].config(bg=win_color)
        return

    if all(buttons[i][BOARD_SIZE - i - 1]['text'] == player for i in range(BOARD_SIZE)):
        for i in range(BOARD_SIZE):
            buttons[i][BOARD_SIZE - i - 1].config(bg=win_color)
        return


# Function to handle button clicks
def on_button_click(row, col):
    global current_player

    if buttons[row][col]['text'] == " ":
        buttons[row][col]['text'] = current_player

        if check_winner(current_player):
            messagebox.showinfo("Game Over", f"Player {current_player} wins!")
            reset_game()
        elif is_board_full():
            messagebox.showinfo("Game Over", "It's a tie!")
            reset_game()
        else:
            current_player = 'O' if current_player == 'X' else 'X'

            if current_player == 'X':
                ai_row, ai_col = get_ai_move()
                on_button_click(ai_row, ai_col)

    # Update the game status label
    update_status_label()

# Function to reset the game
def reset_game():
    global current_player

    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            buttons[i][j]['text'] = " "

    current_player = 'O'

    # Update the game status label after resetting the game
    update_status_label()

# Function to update the game status label
def update_status_label():
    global current_player

    status_label.config(text=f"Player {current_player}'s Turn")

# Function to check if a player has won
def check_winner(player):
    for i in range(BOARD_SIZE):
        if all(buttons[i][j]['text'] == player for j in range(BOARD_SIZE)):
            return True

    for j in range(BOARD_SIZE):
        if all(buttons[i][j]['text'] == player for i in range(BOARD_SIZE)):
            return True

    if all(buttons[i][i]['text'] == player for i in range(BOARD_SIZE)) or \
            all(buttons[i][BOARD_SIZE - i - 1]['text'] == player for i in range(BOARD_SIZE)):
        return True

    return False

# Function to check if the board is full
def is_board_full():
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if buttons[i][j]['text'] == " ":
                return False
    return True

# Function to get the AI's move
def get_ai_move():
    best_eval = -float('inf')
    best_move = None

    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if buttons[i][j]['text'] == " ":
                buttons[i][j]['text'] = 'X'
                eval = minimax(0, False, -float('inf'), float('inf'), {})
                buttons[i][j]['text'] = ' '
                if eval > best_eval:
                    best_eval = eval
                    best_move = (i, j)
    return best_move

# Minimax function with alpha-beta pruning and memoization
def minimax(depth, is_maximizing, alpha, beta, memo):
    if check_winner('X'):
        return 1
    elif check_winner('O'):
        return -1
    elif is_board_full():
        return 0

    board_state = tuple(tuple(button['text'] for button in row) for row in buttons)

    if board_state in memo:
        return memo[board_state]

    if is_maximizing:
        max_eval = -float('inf')
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if buttons[i][j]['text'] == " ":
                    buttons[i][j]['text'] = 'X'
                    eval = minimax(depth + 1, False, alpha, beta, memo)
                    buttons[i][j]['text'] = ' '
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
        memo[board_state] = max_eval
        return max_eval
    else:
        min_eval = float('inf')
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if buttons[i][j]['text'] == " ":
                    buttons[i][j]['text'] = 'O'
                    eval = minimax(depth + 1, True, alpha, beta, memo)
                    buttons[i][j]['text'] = ' '
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
        memo[board_state] = min_eval
        return min_eval

# Main function to start the game
def main():
    create_gui()
    root.mainloop()

if __name__ == "__main__":
    main()
