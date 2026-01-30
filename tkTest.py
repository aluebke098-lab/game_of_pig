import tkinter as tk
button_clicks = 0

def say_hi():
    global button_clicks
    button_clicks += 1
    if button_clicks % 2 == 1:
        label.config(text="( OwO)/ Hewo!", font=("Arial", 28))
    else:
        label.config(text="Bye Bye! \(OwO )", font=("Arial", 14))

# create main window
root = tk.Tk()
root.title("My First Tkinter Project!") # label at the top of the window
root.geometry("400x300") # width x height

label = tk.Label(root, text="\(O w O)/", font=("Arial", 14)) # first parameter is destination
label.pack() # REQUIRED for Label to work

button = tk.Button(root, text="Click to Wave", font=("Arial", 28), command=say_hi) # first parameter is destination
button.pack()

# runs the program above
root.mainloop()