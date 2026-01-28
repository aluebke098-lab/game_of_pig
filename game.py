import random

GOAL = 100

def start_game():
    bank = [0,0] #index matches active player
    active_player = -1 #player1 = 0, player2 = 1 -> changes by adding 1 then modulus 2
    end = False
    while not end:
        print("")
        active_player = next_turn(active_player)
        active_player, bank, score, end = play_turn(active_player, bank)
    end_game(active_player, score)

def roll(turn_total): #rolls a d6, and adjusts the turn total
    roll = random.randint(1,6)
    print(f"You rolled a {roll}!")
    if roll == 1:
        return False, 0
    else:
        turn_total += roll
        print(f"Your turn total is {turn_total}.")
        return True, turn_total

def next_turn(active_player): # changes the active player, to change turns
    active_player += 1
    active_player = active_player % 2
    return active_player

def play_turn(active_player, bank): # roll/hold, check to see if there's a winner
    turn = True
    turn_total = 0
    print(f"It is Player {active_player+1}'s turn.")
    print(f"Current Totals:\n  Player 1: {bank[0]}\n  Player 2: {bank[1]}")

    while turn:
        valid_input = False
        while not valid_input:
            action = input("Type \"R\" to roll or \"H\" to hold.\n").strip().lower() 
            if action == "r":
                valid_input = True
                turn, turn_total = roll(turn_total)
                score = bank[active_player] + turn_total
                print(f"Player {active_player+1} currently has a total of {score}.")
            elif action == "h":
                valid_input = True
                turn = False
                bank[active_player] = score
            else:
                pass 

        if score >= GOAL:
            turn = False
            end = True
        else:
            end = False
    print("")
    return active_player, bank, score, end

def end_game(active_player, score): # announce winner, restart
    print(f"Congrats, Player {active_player} won the game with a total of {score}!")
    restart = input("Type \"P\" to play again.\n").strip().lower()
    if restart == "p":
        start_game()
    
start_game()