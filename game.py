import random

GOAL = 100

def start_game():
    bank = [0,0] #index matches active player
    active_player = 0 #player1 = 0, player2 = 1 -> changes by adding 1 then modulus 2
    winner = "none"

def roll(turn_total):
    roll = random.randint(1,6)
    if roll == 1:
        return False, 0
    else:
        turn_total += roll
        return True, turn_total

def next_turn():
    active_player += 1
    active_player = active_player % 2

def play_turn(active_player, bank):
    turn = True
    turn_total = 0
    while turn:
        action = input("Type \"R\" to roll or \"H\" to hold.\n").strip().lower()
        if action == "r":
            turn, turn_total = roll(turn_total)
        elif action == "h":
            turn = False
        else:
            pass
        if bank[active_player] + turn_total >= GOAL:
            end_game(active_player)
    bank[active_player] += turn_total

def end_game(active_player):
    print(f"Congrats, {active_player} won the game!")
    restart = input("Type \"P\" to play again.").strip().lower()
    if restart == "p":
        start_game()