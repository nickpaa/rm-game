import tkinter as tk
#from tkinter import tk
from PIL import ImageTk, Image
import random


def play_easy_mode():
    print(f'{player_name.get()} from {player_loc.get()} is playing easy mode')
    main.destroy()

    # main containers    
    main = tk.Frame(root)
    main.grid(column=0, row=0)

    # create easy game widgets
    intro_message = tk.Label(main, text='This is easy mode. Let\'s play.')
    intro_message.grid()


def play_real_mode():
    print(f'{player_name.get()} from {player_loc.get()} is playing real life mode')
    main.destroy()

# TODO: validate that user fields are filled in before selecting game
# def validate_user():


root = tk.Tk()
root.title('The PRM Game')

root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

# create the main containers
# main = tk.Frame(root, padding=("3 3 12 12"))
main = tk.Frame(root)
# logo_frame = tk.Frame(main, relief='sunken', padding=1)
logo_frame = tk.Frame(main, relief='sunken')

# layout for the main containers

main.grid(column=0, row=0)
logo_frame.grid(column=0, row=0, padx=1, pady=1)

# create widgets

### logo
logo_path = 'images/ua_logo.jpg'
logo_img = ImageTk.PhotoImage(Image.open(logo_path))
logo = tk.Label(logo_frame, image=logo_img)

### sign-in fields
player_name_label = tk.Label(main, text='What\'s your name?')
# player_name = tk.Entry(main, textvariable=StringVar())
player_name = tk.Entry(main)

player_loc_label = tk.Label(main, text='Where are you from?')
# player_loc = tk.Entry(main, textvariable=StringVar())
player_loc = tk.Entry(main)

### buttons
easy_button_path = 'images/100_emoji.png'
easy_button_image = ImageTk.PhotoImage(Image.open(easy_button_path))
easy_button = tk.Button(main, text='Play easy mode', image=easy_button_image, compound='top', height=120, width=120, bg='white', 
    command=play_easy_mode)

real_button_choices = ['man','woman','person']
real_button_path = 'images/' + random.choice(real_button_choices) + '_shrugging_emoji.png'
real_button_image = ImageTk.PhotoImage(Image.open(real_button_path))
real_button = tk.Button(main, text='Play real life mode', image=real_button_image, compound='top', height=120, width=120, bg='white', 
    command=play_real_mode)

# place widgets

### logo
logo.grid(row=0, column=0)

### sign-in fields
player_name_label.grid(row=1, column=1, padx=20, pady=2)
player_name.grid(row=1, column=2)

player_loc_label.grid(row=2, column=1, padx=20, pady=2)
player_loc.grid(row=2, column=2)

### buttons
easy_button.grid(row=3, column=1, padx=20, pady=20)
real_button.grid(row=3, column=2, padx=20, pady=20)

# subframe0 = tk.Label(frame, text='(0,0) sub')
# subframe0.grid(row=0, column=0)
# subframe1 = tk.Label(frame, text='(1,0) sub')
# subframe1.grid(row=1, column=0)

# tk.Label(main, text='(1,1)').grid(column=1, row=1)
# tk.Button(main, text='(2,1)', command=(lambda: print('Easy'))).grid(column=1, row=2)
# tk.Label(main, text='(3,2)').grid(column=2, row=3)
# tk.Button(main, text='(0,3)', command=(lambda: print('Real life'))).grid(column=3, row=0)

root.mainloop()