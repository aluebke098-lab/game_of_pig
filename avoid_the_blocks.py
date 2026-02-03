import tkinter as tk
import random

# Declare some CONSTANTS
WIDTH = 400
HEIGHT = WIDTH*.75
PLAYER_SIZE = 30
ENEMY_SIZE = 20
MOVE_SPEED = 20

# Build our Window
root = tk.Tk()
root.title("Avoid the Blocks")

#background - width + height here works instead of root.geometry()
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="#000000")
canvas.pack()

# Make the Player
player = canvas.create_rectangle(180, 250, 180+PLAYER_SIZE, 250+PLAYER_SIZE, fill="#238064") # x,y, for top left coord; x1,y1 for bottom right coord

# Make a list to hold Enemies
enemies = []

# enemy spawn change variable so it happens more the longer it goes on
spawn_chance = 400

# Make bool for player alive
alive = True

# Movement functions
def move_left(event):
    canvas.move(player, -MOVE_SPEED, 0) # what to move, change x, change y

def move_right(event):
    canvas.move(player, +MOVE_SPEED, 0)

# binding Buttons - .bind(button, function) 
root.bind("a", move_left)
root.bind("d", move_right)

root.bind("<Left>", move_left) #arrow keys
root.bind("<Right>", move_right)

# Make Enemies
def spawn_enemy():
    x_pos = random.randint(0, WIDTH-ENEMY_SIZE)
    enemy = canvas.create_rectangle(x_pos, 0, x_pos+ENEMY_SIZE, ENEMY_SIZE, fill="#CA1259") #starting them at the random x_pos, start at the top of screen
    enemies.append(enemy)

# run game
def run_game():
    global alive, spawn_chance
    if spawn_chance > 20:
        spawn_chance -= 1
    
    if not alive:
        canvas.delete(all) # removes all of the objects on the canvas
        canvas.create_text(WIDTH//2, HEIGHT//2, text="GAME OVER", fill="#FFFFFF", font=("Arial", 24))
        return
    else:
        if random.randint(1,spawn_chance//20) == 1:
            spawn_enemy()
        
        for enemy in enemies:
            canvas.move(enemy, 0, MOVE_SPEED//2)
        
            if canvas.bbox(enemy) and canvas.bbox(player): #bounding box - if they exist is a boolean I think?
                ex1, ey1, ex2, ey2 = canvas.bbox(enemy) #defining bbox of enemy and player
                px1, py1, px2, py2 = canvas.bbox(player)

                if ex1 < px2 and ex2 > px1 and ey1 < py2 and ey2 > py1: #actual collision check
                    alive = False

        root.after(50, run_game) #after 50 milliseconds, runs function - putting it inside itself means it runs every 50 milliseconds

run_game() #initiate everything
root.mainloop()