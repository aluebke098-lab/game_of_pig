# Avoid the Blocks Extensions Included:
    # Restart button after you game over (press space to (re)start)
    # Prevent player from leaving the screen (sets player to the edge on screen if movement would go off screen)
    # Scoreboard (points for every block that falls off screen)
    # Collectible objects (multiplier boosters)
    # Changing player size (because of multipliers)
    # Making game harder as it goes on (chance to add a block increases over time until it's 100% chance every frame,
        # also bigger player size make it harder and the booster spawn chance increases over time as well.)

import tkinter as tk
import random

# Declare some CONSTANTS
WIDTH = 400
HEIGHT = WIDTH*.75
ENEMY_SIZE = 20
MOVE_SPEED = 20

# Movement functions
def move_left(event):
    global player_size
    canvas.move(player, -MOVE_SPEED, 0) # what to move, change x, change y
    x0, y0, x1, y1 = canvas.coords(player)
    if x0 < 0:
        canvas.coords(player, 0, y0, player_size, y1)

def move_right(event):
    global player_size
    canvas.move(player, +MOVE_SPEED, 0)
    x0, y0, x1, y1 = canvas.coords(player)
    if x1 > WIDTH:
        canvas.coords(player, WIDTH-player_size, y0, WIDTH, y1)

# Make Enemies
def spawn_enemy():
    x_pos = random.randint(0, WIDTH-ENEMY_SIZE)
    enemy = canvas.create_rectangle(x_pos, 0, x_pos+ENEMY_SIZE, ENEMY_SIZE, fill="#CA1259") #starting them at the random x_pos, start at the top of screen
    enemies.append(enemy)

# make multipliers
def add_booster():
    x_pos = random.randint(0, WIDTH-ENEMY_SIZE)
    food = canvas.create_oval(x_pos, 0, x_pos+ENEMY_SIZE, ENEMY_SIZE, fill="#157ACC")
    boosters.append(food)

# run game
def run_game():
    global alive, spawn_chance, score, multiplier, player_size
    if spawn_chance > 100:
        spawn_chance -= 1
    
    if not alive:
        canvas.delete("all") # removes all of the objects on the canvas
        canvas.create_text(WIDTH//2, HEIGHT//2, text="GAME OVER", fill="#AD0000", font=("Arial", 24))
        canvas.create_text(WIDTH//2, HEIGHT//2 + 30, text="Press Space to Restart", fill="#8D8D8D", font=("Arial", 12))
        canvas.create_text(WIDTH//2, HEIGHT//2 - 60, text=("Final Score: " + str(score)), fill="#6100E0", font=("Arial", 20))
        return
    else:
        if random.randint(1, spawn_chance//100) == 1:
            spawn_enemy()
        if random.randint(1, spawn_chance//50) == 1:
            add_booster()
        
        for food in boosters:
            canvas.move(food, 0, MOVE_SPEED//2)
        
            if canvas.bbox(food) and canvas.bbox(player): #bounding box - if they exist is a boolean I think?
                fx1, fy1, fx2, fy2 = canvas.bbox(food) #defining bbox of booster and player
                px1, py1, px2, py2 = canvas.bbox(player)

                # stops moving boosters once they fall off of the screen
                if fy1 > HEIGHT:
                    boosters.remove(food)
                    canvas.delete(food)
                
                if fx1 < px2 and fx2 > px1 and fy1 < py2 and fy2 > py1: #actual collision check, adds to multiplier when you collect it
                    multiplier += 1
                    boosters.remove(food)
                    canvas.delete(food)
                    canvas.itemconfigure("mult", text="x" + str(multiplier) + " Multiplier")
                    
                    # adjusting player size
                    player_size += multiplier
                    x0, y0, x1, y1 = canvas.coords(player)
                    x0 -= multiplier
                    y0 -= multiplier
                    x1 = x0 + player_size
                    y1 = y0 + player_size
                    canvas.coords(player, x0, y0, x1, y1)

        for enemy in enemies:
            canvas.move(enemy, 0, MOVE_SPEED//2)
        
            if canvas.bbox(enemy) and canvas.bbox(player): #bounding box - if they exist is a boolean I think?
                ex1, ey1, ex2, ey2 = canvas.bbox(enemy) #defining bbox of enemy and player
                px1, py1, px2, py2 = canvas.bbox(player)

                # stops moving enemies once they fall off of the screen, and adds to the score
                if ey1 > HEIGHT:
                    enemies.remove(enemy)
                    canvas.delete(enemy)
                    score += 1*multiplier
                    canvas.itemconfigure("scoreboard", text="Score: " + str(score))

                if ex1 < px2 and ex2 > px1 and ey1 < py2 and ey2 > py1: #actual collision check
                    alive = False

        root.after(50, run_game) #after 50 milliseconds, runs function - putting it inside itself means it runs every 50 milliseconds  

# (re)start game
def restart(event):
    global alive, player, enemies, spawn_chance, score, multiplier, boosters, player_size
    
    if not alive:
        # reset all variables to restart game
        canvas.delete("all")
        alive = True

        # Make the Player
        player_size = 30
        player = canvas.create_rectangle(180, 250, 180+player_size, 250+player_size, fill="#238064") # x,y, for top left coord; x1,y1 for bottom right coord
        # Make a list to hold Enemies
        enemies = []
        # enemy spawn change variable so it happens more the longer it goes on
        spawn_chance = 2000

        # variable to hold score
        score = 0
        canvas.create_text(WIDTH//2 - 100, 20, text="Score: " + str(score), fill="#6100E0", tags="scoreboard", font=("Arial", 20))

        # variable to multiply score and player size, collect boosters to add to multiplier (list to hold boosters like with enemies)
        multiplier = 1
        boosters = []
        canvas.create_text(WIDTH//2 + 100, 20, text="x" + str(multiplier) + " Multiplier", fill="#F0C03F", tags="mult", font=("Arial", 20))

        run_game()   

# Build our Window
root = tk.Tk()
root.title("Avoid the Blocks")

#background - width + height here works instead of root.geometry()
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="#000000")
canvas.pack()

# Make bool for player alive - starts false so that the (re)start function will work properly
alive = False

# initial message when the game first boots up
canvas.create_text(WIDTH//2, HEIGHT//2, text="Press Space to Start", fill="#FFFFFF", font=("Arial", 24))

# binding Buttons - .bind(button, function) 
root.bind("a", move_left)
root.bind("d", move_right)
root.bind("<Left>", move_left) #arrow keys
root.bind("<Right>", move_right)
root.bind("<space>", restart) #start func

root.mainloop()