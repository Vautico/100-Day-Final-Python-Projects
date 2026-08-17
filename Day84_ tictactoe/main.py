# how to make tic tac toe
# print title
# print the board
# Ask for p1 and p2
# tells who goes first, random
# way for person to select space to put their thing in
# Switches to other player
# Game loop that goes until win
#           Something to check if somebody has won
import random


print("Yo wsp gng gng wlcm to ma ticy tacky toey gme pls inpt plyr 1 n 2")
player1 = input("Name of P1:")

player2 = input("Name of P2:")

players = [player1, player2]

who_goes_first = random.choice(players)
who_goes_second = players[1] if who_goes_first == players[0] else players[0]
print(f"{who_goes_first} will go first. You are X.")
print(f"{who_goes_second} will go second. You are O.")

positions = {
    "a": "_",
    "b": "_",
    "c": "_",
    "d": "_",
    "e": "_",
    "f": "_",
    "g": "_",
    "h": "_",
    "i": "_",
}

# problem:how to check if there is a win???

def print_board():
    print(f"\n  {positions['a']}  |  {positions['b']}  |  {positions['c']}\n"
          " ---------------\n"
          f"  {positions['d']}  |  {positions['e']}  |  {positions['f']}\n"
          " ---------------\n"
          f"  {positions['g']}  |  {positions['h']}  |  {positions['i']}")


first_all_moves = ""
second_all_moves = ""
win_cons = ["abc", "def", "ghi", "adg", "beh", "cfi", "gec", "aei"]
def check_win():
    for win_con in win_cons:
        if all(position in first_all_moves for position in win_con):
            print(f"{who_goes_first} wins!!!")
            return False

        if all(position in second_all_moves for position in win_con):
            print(f"{who_goes_second} wins!!!")
            return False
    if all("_" not in val for val in positions.values()):
        print("Draw")
        return False

    return True



print_board()

while True:
    while True:
        first_players_move = input(f"\n\n{who_goes_first}: your move's position (a-i):").lower()

        if first_players_move in positions and positions[first_players_move] == "_":
            positions[first_players_move] = "X"
            first_all_moves += first_players_move
            print_board()
            break

        print("Position not possible. Try again.")

    game_on = check_win()
    if not game_on:
        break

    while True:
        second_players_move = input(f"\n\n{who_goes_second}: your move's position (a-i):").lower()

        if second_players_move in positions.keys() and positions[second_players_move] == "_":
            positions[second_players_move] = "O"
            second_all_moves += second_players_move
            print_board()
            break

        print("Position not possible. Try again.")
    game_on = check_win()
    if not game_on:
        break




