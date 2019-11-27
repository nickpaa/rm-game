import tkinter as tk
from tkinter import font
from PIL import ImageTk, Image
import random
from game import EasyGame, RealGame, DFDSimulation, EASY_AC, EASY_DFD, EASY_FCDATA


# TODO: validate that user fields are filled in before selecting game
# def validate_user():


class GUI():
    
    def __init__(self, root):

        self.root = root

        root.title('The PRM Game')
        root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)

        # default_font = font.nametofont('TkDefaultFont')
        # default_font.configure(size=16, weight='bold')

        # create the main containers
        self.main = tk.Frame(root)
        self.logo_frame = tk.Frame(self.main, relief='sunken')

        # layout for the main containers
        self.main.grid(column=0, row=0)
        self.logo_frame.grid(column=0, row=0, padx=1, pady=1)

        # create widgets

        ### logo
        self.logo_path = 'images/ua_logo.jpg'
        self.logo_img = ImageTk.PhotoImage(Image.open(self.logo_path))
        self.logo = tk.Label(self.logo_frame, image=self.logo_img)

        ### sign-in fields
        self.player_name_label = tk.Label(self.main, text='What\'s your name?')
        # player_name = tk.Entry(main, textvariable=StringVar())
        self.player_name = tk.Entry(self.main)

        self.player_loc_label = tk.Label(self.main, text='Where are you from?')
        # player_loc = tk.Entry(main, textvariable=StringVar())
        self.player_loc = tk.Entry(self.main)

        ### buttons
        self.easy_button_path = 'images/100_emoji.png'
        self.easy_button_image = ImageTk.PhotoImage(Image.open(self.easy_button_path))
        self.easy_button = tk.Button(self.main, text='Play easy mode', image=self.easy_button_image, compound='top', height=120, width=120, bg='white', 
            command=self.play_easy_mode)

        self.real_button_choices = ['man','woman','person']
        self.real_button_path = 'images/' + random.choice(self.real_button_choices) + '_shrugging_emoji.png'
        self.real_button_image = ImageTk.PhotoImage(Image.open(self.real_button_path))
        self.real_button = tk.Button(self.main, text='Play real life mode', image=self.real_button_image, compound='top', height=120, width=120, bg='white', 
            command=self.play_real_mode)

        # place widgets

        ### logo
        self.logo.grid(row=0, column=0)

        ### sign-in fields
        self.player_name_label.grid(row=1, column=1, padx=20, pady=2, sticky=tk.W)
        self.player_name.grid(row=1, column=2)

        self.player_loc_label.grid(row=2, column=1, padx=20, pady=2, sticky=tk.W)
        self.player_loc.grid(row=2, column=2)

        ### buttons
        self.easy_button.grid(row=3, column=1, padx=20, pady=20)
        self.real_button.grid(row=3, column=2, padx=20, pady=20)


    def play_easy_mode(self):

        # SETUP
        
        print(f'{self.player_name.get()} from {self.player_loc.get()} is playing easy mode')
        self.main.destroy()

        game = EasyGame(EASY_DFD, EASY_FCDATA, EASY_AC)

        ### MAIN CONTAINERS
        
        main = tk.Frame(self.root)
        main.grid(column=0, row=0)

        ### CREATE CORE WIDGETS
        
        intro_message = tk.Label(main, text='EASY MODE')

        # tracking labels and icons
        date_label = tk.Label(main, text=f'Today is DFD {game.curr_dfd}')
        sa_label = tk.Label(main, text=f'There are {game.sa} seats remaining.')
        rev_label = tk.Label(main, text=f'So far, your flight\'s revenue is ${game.totalrev:,}.')

        date_image = ImageTk.PhotoImage(Image.open('images/calendar_emoji.png'))
        date_image_label = tk.Label(main, image=date_image)
        date_image_label.image = date_image

        seat_image = ImageTk.PhotoImage(Image.open('images/seat_emoji.png'))
        seat_image_label = tk.Label(main, image=seat_image)
        seat_image_label.image = seat_image
        
        money_image = ImageTk.PhotoImage(Image.open('images/money_emoji.png'))
        money_image_label = tk.Label(main, image=money_image)
        money_image_label.image = money_image
        
        # forecast headers
        fc_frame = tk.Frame(main, relief='sunken', borderwidth=2)
        fc_label = tk.Label(main, text='--- FORECAST ---')
        fc_label_1 = tk.Label(fc_frame, text='DFD')
        fc_label_2 = tk.Label(fc_frame, text='Fare')
        fc_label_3 = tk.Label(fc_frame, text='Demand')

        # quit button
        quit_button = tk.Button(main, text='Quit game', fg='red')
        
        ### PLACE CORE WIDGETS
        
        intro_message.grid(row=0, column=0)
        
        # tracking labels and icons
        date_image_label.grid(row=1, column=0)
        date_label.grid(row=1, column=1)
        
        seat_image_label.grid(row=2, column=0)
        sa_label.grid(row=2, column=1)
        
        money_image_label.grid(row=3, column=0)
        rev_label.grid(row=3, column=1)

        # forecast headers
        fc_frame.grid(row=1, column=2, rowspan=3)
        fc_label.grid(row=0, column=2)
        fc_label_1.grid(row=0, column=2, padx=5, pady=2)  # DFD
        fc_label_2.grid(row=0, column=3, padx=5, pady=2)  # fare
        fc_label_3.grid(row=0, column=4, padx=5, pady=2)  # demand

        # quit button
        quit_button.grid(row=0, column=5)

        ### DYNAMIC FIELDS FOR EACH DFD

        # loop through each dfd, place widgets, and play game
        for i, dfd in enumerate(range(game.ndfd, -1, -1)):
            print(f'dfd {dfd}')

            ### Create DFDSimulation
            self.dfdsim = DFDSimulation(game, dfd)

            # create and place forecast values
            tk.Label(fc_frame, text=dfd).grid(row=i+1, column=2)
            tk.Label(fc_frame, text=game.fc.loc[dfd, 'fare']).grid(row=i+1, column=3)
            tk.Label(fc_frame, text=game.fc.loc[dfd, 'demand']).grid(row=i+1, column=4)

            # create and place player entries
            rsv_label = tk.Label(main, text=f'How many seats would you \nlike to reserve at ${game.fc.loc[game.curr_dfd, "fare"]}?')
            rsv_value = tk.StringVar()
            self.rsv_entry = tk.Entry(main, width=10, textvariable=rsv_value)

            rsv_label.grid(row=4, column=3)
            self.rsv_entry.grid(row=4, column=4)

            check_image = ImageTk.PhotoImage(Image.open('images/check.png'))
            check_image_button = tk.Button(main, image=check_image)
            check_image_button.image = check_image

            check_image_button.grid(row=4, column=5)

            # store entered value as self.rsv upon Enter or mouse click
            self.rsv_entry.bind('<Return>', self.run_dfd)
            check_image_button.bind('<Button-1>', self.run_dfd)

            
            
    def run_dfd(self, event):
        self.rsv = int(self.rsv_entry.get())
        self.dfdsim.observe_bookings(self.rsv)
        



    def play_real_mode(self):
        print(f'{self.player_name.get()} from {self.player_loc.get()} is playing real life mode')
        self.main.destroy()


    
