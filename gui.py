import tkinter as tk
from tkinter import font, messagebox
from PIL import ImageTk, Image
import random
from game import EasyGame, RealGame, DFDSimulation
from data import EASY_AC, EASY_DFD, EASY_FCDATA

class GUI():
    
    def __init__(self, root):
        self.root = root

        self.root.title('The PRM Game')
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        self.build_home_page()


    def build_home_page(self):
        # create the main container
        self.home = tk.Frame(self.root)

        # layout for the main container
        self.home.grid(column=0, row=0)

        # create widgets

        ### logo
        self.logo_path = 'images/airplane_title.png'
        self.logo_img = ImageTk.PhotoImage(Image.open(self.logo_path))
        self.logo = tk.Label(self.home, image=self.logo_img)

        ### sign-in fields
        self.player_name_label = tk.Label(self.home, text='What\'s your name?')
        self.player_name = tk.Entry(self.home)

        self.player_loc_label = tk.Label(self.home, text='Where are you from?')
        self.player_loc = tk.Entry(self.home)

        ### buttons
        self.easy_button_path = 'images/100.png'
        self.easy_button_image = ImageTk.PhotoImage(Image.open(self.easy_button_path))
        self.easy_button = tk.Button(self.home, text='Play easy mode', image=self.easy_button_image, compound='top', height=120, width=120, bg='white', 
            command=self.play_easy_mode)

        self.real_button_choices = ['man','woman','person']
        self.real_button_path = 'images/' + random.choice(self.real_button_choices) + '_shrugging.png'
        self.real_button_image = ImageTk.PhotoImage(Image.open(self.real_button_path))
        self.real_button = tk.Button(self.home, text='Play real life mode', image=self.real_button_image, compound='top', height=120, width=120, bg='white', 
            command=self.play_real_mode)

        # place widgets

        ### logo
        self.logo.grid(row=0, column=0, rowspan=3)

        ### sign-in fields
        # TODO: validate that user fields are filled in before selecting game
        self.player_name_label.grid(row=0, column=1, padx=20, pady=2, sticky=tk.W)
        self.player_name.grid(row=0, column=2)

        self.player_loc_label.grid(row=1, column=1, padx=20, pady=2, sticky=tk.W)
        self.player_loc.grid(row=1, column=2)

        ### buttons
        self.easy_button.grid(row=2, column=1, padx=20, pady=20)
        self.real_button.grid(row=2, column=2, padx=20, pady=20)


    def play_easy_mode(self):
        self.home.destroy()
        self.game = EasyGame(EASY_DFD, EASY_FCDATA, EASY_AC)
        self.build_dfd_in_gui()


    def build_dfd_in_gui(self):
        ### MAIN CONTAINERS
        
        self.main = tk.Frame(self.root)
        self.main.grid(column=0, row=0)

        ### CREATE CORE WIDGETS
        
        self.intro_message = tk.Label(self.main, text='EASY MODE')

        # tracking labels and icons
        self.date_label = tk.Label(self.main, text=f'Today is DFD {self.game.curr_dfd}')
        self.sa_label = tk.Label(self.main, text=f'There are {self.game.sa} seats remaining.')
        self.rev_label = tk.Label(self.main, text=f'So far, your flight\'s revenue is ${self.game.totalrev:,}.')

        self.date_image = ImageTk.PhotoImage(Image.open('images/calendar.png'))
        self.date_image_label = tk.Label(self.main, image=self.date_image)
        self.date_image_label.image = self.date_image

        self.seat_image = ImageTk.PhotoImage(Image.open('images/seat.png'))
        self.seat_image_label = tk.Label(self.main, image=self.seat_image)
        self.seat_image_label.image = self.seat_image
        
        self.money_image = ImageTk.PhotoImage(Image.open('images/money.png'))
        self.money_image_label = tk.Label(self.main, image=self.money_image)
        self.money_image_label.image = self.money_image
        
        # forecast headers
        self.lb_frame = tk.Frame(self.main, relief='sunken', borderwidth=2)
        self.lb_label = tk.Label(self.main, text='--- FORECAST ---')
        self.lb_label_1 = tk.Label(self.lb_frame, text='DFD')
        self.lb_label_2 = tk.Label(self.lb_frame, text='Fare')
        self.lb_label_3 = tk.Label(self.lb_frame, text='Demand')

        # quit button
        self.quit_button = tk.Button(self.main, text='Quit game', fg='red', command=self.quit_game)
        
        ### PLACE CORE WIDGETS
        
        self.intro_message.grid(row=0, column=0)
        
        # tracking labels and icons
        self.date_image_label.grid(row=1, column=0)
        self.date_label.grid(row=1, column=1)
        
        self.seat_image_label.grid(row=2, column=0)
        self.sa_label.grid(row=2, column=1)
        
        self.money_image_label.grid(row=3, column=0)
        self.rev_label.grid(row=3, column=1)

        # forecast headers
        self.lb_frame.grid(row=1, column=2, rowspan=3)
        self.lb_label.grid(row=0, column=2)
        self.lb_label_1.grid(row=0, column=2, padx=5, pady=2)  # DFD
        self.lb_label_2.grid(row=0, column=3, padx=5, pady=2)  # fare
        self.lb_label_3.grid(row=0, column=4, padx=5, pady=2)  # demand

        # quit button
        self.quit_button.grid(row=0, column=5)

        ### kick off dfd simulations

        # loop through each dfd, place widgets, and play self.game
        # for i, dfd in enumerate(range(self.game.ndfd, -1, -1)):

        ### Create DFDSimulation
        self.dfdsim = DFDSimulation(self.game, self.game.curr_dfd)

        # create and place forecast values
        for i, dfd in enumerate(range(self.game.curr_dfd, -1, -1)):
            tk.Label(self.lb_frame, text=dfd).grid(row=i+1, column=2)
            tk.Label(self.lb_frame, text=self.game.fc.loc[dfd, 'fare']).grid(row=i+1, column=3)
            tk.Label(self.lb_frame, text=self.game.fc.loc[dfd, 'demand']).grid(row=i+1, column=4)

        # create and place player entries
        if self.game.curr_dfd > 0:
            self.rsv_label = tk.Label(self.main, text=f'How many seats would you \nlike to reserve at ${self.game.fc.loc[self.game.curr_dfd, "fare"]}?')
        else:
            self.rsv_label = tk.Label(self.main, text=f'Today is the last day, so you should \nreserve all remaining seats at ${self.game.fc.loc[self.game.curr_dfd, "fare"]}.')
        self.rsv_value = tk.StringVar()
        self.rsv_entry = tk.Entry(self.main, width=10, textvariable=self.rsv_value)

        if self.game.curr_dfd == 0:
            self.rsv_entry.insert(0, self.game.sa)

        self.rsv_label.grid(row=1, column=3)
        self.rsv_entry.grid(row=1, column=4)

        self.check_image = ImageTk.PhotoImage(Image.open('images/check.png'))
        self.check_image_button = tk.Button(self.main, image=self.check_image)
        self.check_image_button.image = self.check_image

        self.check_image_button.grid(row=1, column=5)

        # store entered value as self.rsv upon Enter or mouse click and then simulated the dfd
        self.rsv_entry.bind('<Return>', self.run_dfd)
        self.check_image_button.bind('<Button-1>', self.run_dfd)

            
    
    def run_dfd(self, event):
        self.rsv = int(self.rsv_entry.get())  # TODO: validate this somehow
        if (self.rsv < 0) or (self.rsv > self.game.sa):
            print('error')
        
        self.dfdsim.observe_bookings(self.rsv)

        self.outcome_label = tk.Label(self.main, 
            text=f'{self.dfdsim.arr} people showed up to book today, \nand you reserved {self.rsv} seats. \
\n\nYou sold {self.dfdsim.lb} seats and earned ${self.dfdsim.rev:,}.')
        self.outcome_label.grid(row=2, column=3)

        # if dfd > 0, go to next dfd
        self.next_image = ImageTk.PhotoImage(Image.open('images/next.png'))

        if self.game.curr_dfd > 0:
            self.next_image_button = tk.Button(self.main, text='Next day', image=self.next_image, compound='top', height=120, width=120, 
                bg='white', command=self.go_to_next_dfd)
        else:
            self.next_image_button = tk.Button(self.main, text='See results', image=self.next_image, compound='top', height=120, width=120, 
                bg='white', command=self.end_game)

        self.next_image_button.image = self.next_image

        self.next_image_button.grid(row=4, column=3)
        

    def go_to_next_dfd(self):
        self.dfdsim.dfd_cleanup()
        self.main.destroy()
        self.build_dfd_in_gui()


    def end_game(self):
        self.dfdsim.dfd_cleanup()
        self.main.destroy()
        self.build_end_in_gui()


    def quit_game(self):
        quit = tk.messagebox.askyesno('Quit?', 'Do you really want to quit the game?')
        if quit:
            self.main.destroy()
            self.build_home_page()


    def build_end_in_gui(self):
        ### MAIN CONTAINERS
        
        self.main = tk.Frame(self.root)
        self.main.grid(column=0, row=0)

        ### CREATE CORE WIDGETS
        
        self.intro_message = tk.Label(self.main, text='EASY MODE')

        # tracking labels and icons
        self.date_label = tk.Label(self.main, text=f'The flight has departed!')
        self.sa_label = tk.Label(self.main, text=f'Your load factor is {int(100 * (1 - self.game.sa / self.game.AC))}%.')
        self.rev_label = tk.Label(self.main, text=f'You earned a total of ${self.game.totalrev:,}.')

        self.date_image = ImageTk.PhotoImage(Image.open('images/calendar.png'))
        self.date_image_label = tk.Label(self.main, image=self.date_image)
        self.date_image_label.image = self.date_image

        self.seat_image = ImageTk.PhotoImage(Image.open('images/seat.png'))
        self.seat_image_label = tk.Label(self.main, image=self.seat_image)
        self.seat_image_label.image = self.seat_image
        
        self.money_image = ImageTk.PhotoImage(Image.open('images/money.png'))
        self.money_image_label = tk.Label(self.main, image=self.money_image)
        self.money_image_label.image = self.money_image
        
        # leaderboard headers
        self.lb_frame = tk.Frame(self.main, relief='sunken', borderwidth=2)
        self.lb_label = tk.Label(self.main, text='--- LEADERBOARD ---')
        self.lb_label_1 = tk.Label(self.lb_frame, text='Name')
        self.lb_label_2 = tk.Label(self.lb_frame, text='From')
        self.lb_label_3 = tk.Label(self.lb_frame, text='Game')
        self.lb_label_4 = tk.Label(self.lb_frame, text='Revenue')

        # quit button
        self.quit_button = tk.Button(self.main, text='Quit game', fg='red', command=self.quit_game)
        
        ### PLACE CORE WIDGETS
        
        self.intro_message.grid(row=0, column=0)
        
        # tracking labels and icons
        self.date_image_label.grid(row=1, column=0)
        self.date_label.grid(row=1, column=1)
        
        self.seat_image_label.grid(row=2, column=0)
        self.sa_label.grid(row=2, column=1)
        
        self.money_image_label.grid(row=3, column=0)
        self.rev_label.grid(row=3, column=1)

        # leaderboard headers
        self.lb_frame.grid(row=1, column=2, rowspan=3)
        self.lb_label.grid(row=0, column=2)
        self.lb_label_1.grid(row=0, column=2, padx=5, pady=2)  # name
        self.lb_label_2.grid(row=0, column=3, padx=5, pady=2)  # from
        self.lb_label_3.grid(row=0, column=4, padx=5, pady=2)  # game
        self.lb_label_4.grid(row=0, column=5, padx=5, pady=2)  # revenue

        # quit button
        self.quit_button.grid(row=0, column=5)


    def play_real_mode(self):
        self.home.destroy()
    
