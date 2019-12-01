from random import choice, choices
import tkinter as tk
from datetime import datetime
from tkinter import messagebox
from tkinter.font import Font, nametofont

import pandas as pd
from PIL import Image, ImageTk

from scenario import *
from db import create_connection, db_file, insert_results
from game import DFDSimulation, EasyGame, RealGame


class GUI():
    
    def __init__(self, root):
        self.root = root

        self.root.title('The PRM Game')
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        self.default_font = nametofont('TkDefaultFont')
        self.default_font.configure(family='Helvetica', size='12')

        self.entry_font = nametofont('TkTextFont')
        self.entry_font.configure(family='Helvetica', size='12')

        self.build_home()

    
    ### HOME PAGE ###


    def build_home(self):
        # create the main container
        self.home = tk.Frame(self.root, padx=30, pady=30, relief='sunken', borderwidth=5)
        self.home.grid(column=0, row=0)

        self.display_logo_frame()
        self.display_player_frame()
        self.display_button_frame()
        
        # TODO: display leaderboard and admin options
        # self.display_option_frame()


    def display_logo_frame(self):
        self.logo_frame = tk.Frame(self.home, padx=20, pady=20, relief='groove', borderwidth=5, bg='white')
        self.logo_frame.grid(row=0, column=0, padx=10, sticky='N S W', rowspan=3)

        self.logo_path = 'images/airplane_title.png'
        self.logo_img = ImageTk.PhotoImage(Image.open(self.logo_path))
        self.logo = tk.Label(self.home, image=self.logo_img)
        self.logo.grid(row=0, column=0, rowspan=4)


    def display_player_frame(self):
        self.player_frame = tk.Frame(self.home, padx=20, pady=10, relief='groove', borderwidth=5, bg='white')
        self.player_frame.grid(row=0, column=1, sticky='N E W')

        self.player_frame.grid_rowconfigure(0, weight=1)
        self.player_frame.grid_rowconfigure(1, weight=1)
        self.player_frame.grid_columnconfigure(0, weight=1)
        self.player_frame.grid_columnconfigure(1, weight=1)

        self.player_name_label = tk.Label(self.player_frame, text='What\'s your name?', bg='white')
        self.player_name_value = tk.StringVar()
        self.player_name = tk.Entry(self.player_frame, textvariable=self.player_name_value)
        self.player_name_label.grid(row=0, column=0, padx=20, pady=10, sticky='N W')
        self.player_name.grid(row=0, column=1, padx=20, pady=10, sticky='N E')

        self.player_loc_label = tk.Label(self.player_frame, text='Where are you from?', bg='white')
        self.player_loc_value = tk.StringVar()
        self.player_loc = tk.Entry(self.player_frame, textvariable=self.player_loc_value)
        self.player_loc_label.grid(row=1, column=0, padx=20, pady=10, sticky='S W')
        self.player_loc.grid(row=1, column=1, padx=20, pady=10, sticky='S E')

        self.player_name.focus_set()

        # TODO: validate that user fields are filled in before selecting game


    def display_button_frame(self):
        self.button_frame = tk.Frame(self.home, padx=20, pady=10, relief='groove', borderwidth=5, bg='white')
        self.button_frame.grid(row=1, column=1, sticky='W S E')

        self.top_row_button_frame = tk.Frame(self.button_frame, bg='white', relief='groove', borderwidth=5)
        self.top_row_button_frame.grid(row=0, column=0, sticky='W N E')

        self.easy_button_path = 'images/100.png'
        self.easy_button_image = ImageTk.PhotoImage(Image.open(self.easy_button_path))
        self.easy_button = tk.Button(self.top_row_button_frame, text='Play easy mode', image=self.easy_button_image, compound='top', height=160, width=240, bg='white', 
            command=self.play_easy_mode)
        self.easy_button.grid(row=0, column=0, padx=20, pady=20)

        self.real_button_people = ['man','woman','person']
        self.real_button_path = 'images/' + choice(self.real_button_people) + '_shrugging.png'
        self.real_button_image = ImageTk.PhotoImage(Image.open(self.real_button_path))
        self.real_button = tk.Button(self.top_row_button_frame, text='Play real life mode', image=self.real_button_image, compound='top', height=160, width=240, bg='white', 
            command=self.display_real_button_frame)
        self.real_button.grid(row=0, column=1, padx=20, pady=20)


    def display_real_button_frame(self):
        self.easy_button['state'] = 'disabled'

        self.real_mode_button_frame = tk.Frame(self.button_frame, bg='white', relief='groove', borderwidth=5)
        self.real_mode_button_frame.grid(row=1, column=0, sticky='S E W')
        self.real_mode_button_frame.grid_rowconfigure(0, weight=1)
        self.real_mode_button_frame.grid_rowconfigure(1, weight=1)
        self.real_mode_button_frame.grid_columnconfigure(0, weight=1)
        self.real_mode_button_frame.grid_columnconfigure(1, weight=1)
        self.real_mode_button_frame.grid_columnconfigure(2, weight=1)

        self.game1_button = tk.Button(self.real_mode_button_frame, text='Play game 1', bg='white', 
            command=lambda: self.play_real_mode(1))
        self.game1_button.grid(row=0, column=0, padx=(20, 10), pady=10)

        self.game2_button = tk.Button(self.real_mode_button_frame, text='Play game 2', bg='white', 
            command=lambda: self.play_real_mode(2))
        self.game2_button.grid(row=0, column=1, padx=10, pady=10)

        self.game3_button = tk.Button(self.real_mode_button_frame, text='Play game 3', bg='white', 
            command=lambda: self.play_real_mode(3))
        self.game3_button.grid(row=0, column=2, padx=(10, 20), pady=10)

        self.game4_button = tk.Button(self.real_mode_button_frame, text='Play game 4', bg='white',
            command=lambda: self.play_real_mode(4))
        self.game4_button.grid(row=1, column=0, padx=(20, 10), pady=10)

        self.game5_button = tk.Button(self.real_mode_button_frame, text='Play game 5', bg='white',
            command=lambda: self.play_real_mode(5))
        self.game5_button.grid(row=1, column=1, padx=10, pady=10)

        self.game6_button = tk.Button(self.real_mode_button_frame, text='Play game 6', bg='white',
            command=lambda: self.play_real_mode(6))
        self.game6_button.grid(row=1, column=2, padx=(10, 20), pady=10)


    def play_easy_mode(self):
        self.home.destroy()
        self.game = EasyGame(EasyScenario(scenario_dict[0]))
        self.skip_ob = True
        self.game.set_player_info(self.player_name_value.get(), self.player_loc_value.get())
        self.build_game()


    def play_real_mode(self, which_game):
        self.home.destroy()
        self.game = RealGame(RealScenario(scenario_dict[which_game]))
        self.skip_ob = False
        self.game.set_player_info(self.player_name_value.get(), self.player_loc_value.get())
        self.build_game()
    
    
    ### GAME PAGE ###


    def build_game(self):
        ### MAIN CONTAINERS
        
        self.main = tk.Frame(self.root, padx=30, pady=30, relief='sunken', borderwidth=5)
        self.main.grid(column=0, row=0, sticky='N S E W')
        self.main.rowconfigure(0, weight=1)
        self.main.columnconfigure((0,1,2), weight=1)

        self.left_frame = tk.Frame(self.main, relief='groove', borderwidth=5, bg='white')
        self.left_frame.grid(row=0, column=0, padx=10, sticky='N S E W')
        self.left_frame.rowconfigure(0, weight=1)
        self.left_frame.columnconfigure(0, weight=1)

        self.middle_frame = tk.Frame(self.main, relief='groove', borderwidth=5, bg='white')
        self.middle_frame.grid(row=0, column=1, padx=10, sticky='N S E W')
        self.middle_frame.rowconfigure(0, weight=1)
        self.middle_frame.columnconfigure(0, weight=1)

        self.right_frame = tk.Frame(self.main, relief='groove', borderwidth=5, bg='white')
        self.right_frame.grid(row=0, column=2, padx=10, sticky='N S E W')
        self.right_frame.rowconfigure(0, weight=1)
        self.right_frame.columnconfigure(0, weight=1)

        self.option_frame = tk.Frame(self.main, padx=10, pady=20, relief='groove', borderwidth=5, bg='white')
        self.option_frame.grid(row=1, column=2, padx=10, pady=(50, 0), sticky='S E')

        self.build_stats_frame()
        self.build_forecast_frame()
        if not self.skip_ob:
            self.build_overbook_frame()
        else:
            self.build_reserve_frame()
        self.display_option_frame()

        self.dfdsim = DFDSimulation(self.game, self.game.curr_dfd)


    def build_stats_frame(self):
        self.stats_frame = tk.Frame(self.left_frame)
        self.stats_frame.grid(row=0, column=0, sticky='N S E W')
        self.stats_frame.rowconfigure((1,2,3), weight=1)
        self.stats_frame.columnconfigure((0,1), weight=1)
        
        ### IMAGES
        
        self.stats_header = tk.Label(self.stats_frame, text=self.game.game_type)
        self.stats_header.grid(row=0, column=0, padx=5, pady=10)

        self.date_image = ImageTk.PhotoImage(Image.open('images/calendar.png'))
        self.date_image_label = tk.Label(self.stats_frame, image=self.date_image)
        self.date_image_label.image = self.date_image
        self.date_image_label.grid(row=1, column=0, pady=10)

        self.seat_image = ImageTk.PhotoImage(Image.open('images/seat.png'))
        self.seat_image_label = tk.Label(self.stats_frame, image=self.seat_image)
        self.seat_image_label.image = self.seat_image
        self.seat_image_label.grid(row=2, column=0, pady=10)
        
        self.money_image = ImageTk.PhotoImage(Image.open('images/money.png'))
        self.money_image_label = tk.Label(self.stats_frame, image=self.money_image)
        self.money_image_label.image = self.money_image
        self.money_image_label.grid(row=3, column=0, pady=10)

        ### date frame and values

        self.date_frame = tk.Frame(self.stats_frame)
        self.date_frame.grid(row=1, column=1, padx=5)

        self.today_label = tk.Label(self.date_frame, text=f'Today:')
        self.today_value = tk.Label(self.date_frame, text=f'{self.game.curr_dow_long}')
        self.dep_label = tk.Label(self.date_frame, text=f'Departure:')
        self.dep_value = tk.Label(self.date_frame, text=f'Friday')

        self.today_label.grid(row=0, column=0, sticky='W')
        self.today_value.grid(row=0, column=1)
        self.dep_label.grid(row=1, column=0, sticky='W')
        self.dep_value.grid(row=1, column=1)

        ### seat frame and values

        self.seat_frame = tk.Frame(self.stats_frame)
        self.seat_frame.grid(row=2, column=1, padx=5)

        self.ac_label = tk.Label(self.seat_frame, text=f'Aircraft capacity:')
        self.ac_value = tk.Label(self.seat_frame, text=f'{self.game.ac}')
        if not self.game.easy_mode:
            self.au_label = tk.Label(self.seat_frame, text=f'With overbooking:')
            self.au_value = tk.Label(self.seat_frame, text=f'{self.game.au}')
        self.lb_label = tk.Label(self.seat_frame, text=f'Seats sold:')
        self.lb_value = tk.Label(self.seat_frame, text=f'{self.game.total_lb}')
        self.sa_label = tk.Label(self.seat_frame, text=f'Remaining seats:')
        self.sa_value = tk.Label(self.seat_frame, text=f'{self.game.sa}')

        self.ac_label.grid(row=0, column=0, sticky='W')
        self.ac_value.grid(row=0, column=1)
        if not self.game.easy_mode:
            self.au_label.grid(row=1, column=0, sticky='W')
            self.au_value.grid(row=1, column=1)
        self.lb_label.grid(row=2, column=0, sticky='W')
        self.lb_value.grid(row=2, column=1)
        self.sa_label.grid(row=3, column=0, sticky='W')
        self.sa_value.grid(row=3, column=1)

        ### revenue frame and values

        self.rev_frame = tk.Frame(self.stats_frame)
        self.rev_frame.grid(row=3, column=1, padx=5)

        self.rev_label = tk.Label(self.rev_frame, text=f'Revenue:')
        self.rev_value = tk.Label(self.rev_frame, text=f'${self.game.total_rev:,}')

        self.rev_label.grid(row=0, column=0)
        self.rev_value.grid(row=0, column=1)

        self.change_bg_to_white(self.stats_frame)
        self.change_bg_to_white(self.date_frame)
        self.change_bg_to_white(self.seat_frame)
        self.change_bg_to_white(self.rev_frame)


    def build_forecast_frame(self):
        self.fc_frame = tk.Frame(self.middle_frame)
        self.fc_frame.grid(row=0, column=0, sticky='N S E W')
        self.fc_frame.rowconfigure(1, weight=1)
        self.fc_frame.columnconfigure(0, weight=1)

        self.fc_header = tk.Label(self.fc_frame, text='--- FORECAST ---', font='Helvetica 14 bold')
        self.fc_header.grid(row=0, column=0, padx=5)

        self.fc_value_frame = tk.Frame(self.fc_frame)
        self.fc_value_frame.grid(row=1, column=0)

        self.fc_label_1 = tk.Label(self.fc_value_frame, text='Book day', font='Helvetica 14 bold')
        self.fc_label_2 = tk.Label(self.fc_value_frame, text='Fare', font='Helvetica 14 bold')
        self.fc_label_3 = tk.Label(self.fc_value_frame, text='Demand', font='Helvetica 14 bold')
        if not self.game.easy_mode:
            self.fc_label_4 = tk.Label(self.fc_value_frame, text='Confidence', font='Helvetica 14 bold')
        
        self.fc_label_1.grid(row=0, column=0, padx=5, pady=10)  # DOW
        self.fc_label_2.grid(row=0, column=1, padx=5, pady=10)  # fare
        if self.game.easy_mode:
            self.fc_label_3.grid(row=0, column=2, padx=(5, 10), pady=10)  # demand
        else:
            self.fc_label_3.grid(row=0, column=2, padx=5, pady=10)  # demand
            self.fc_label_4.grid(row=0, column=3, padx=(5, 10), pady=10)  # stdev

        # create and place forecast value labels
        for i, dfd in enumerate(range(self.game.curr_dfd, -1, -1)):
            tk.Label(self.fc_value_frame, text=self.game.fc.loc[dfd, 'dow_short']).grid(row=i+2, column=0, padx=(10, 5))
            tk.Label(self.fc_value_frame, text=f"${self.game.fc.loc[dfd, 'fare']:,}").grid(row=i+2, column=1, padx=5, pady=10)
            if self.game.easy_mode:
                tk.Label(self.fc_value_frame, text=self.game.fc.loc[dfd, 'demand']).grid(row=i+2, column=2, padx=(5, 10), pady=10)
            else:
                tk.Label(self.fc_value_frame, text=self.game.fc.loc[dfd, 'demand']).grid(row=i+2, column=2, padx=5, pady=10)
                confidence = self.convert_stdev_to_confidence(self.game.fc.loc[dfd, 'demand'], self.game.fc.loc[dfd, 'stdev'])
                tk.Label(self.fc_value_frame, text=confidence).grid(row=i+2, column=3, padx=(5, 10), pady=10)

        # create and place blank row between values and total
        tk.Label(self.fc_value_frame, text='     ').grid(row=i+3, column=0, padx=(10, 5))
        tk.Label(self.fc_value_frame, text='     ').grid(row=i+3, column=1, padx=5, pady=10)
        if self.game.easy_mode:
            tk.Label(self.fc_value_frame, text='     ').grid(row=i+3, column=2, padx=(5, 10), pady=10)
        else:
            tk.Label(self.fc_value_frame, text='     ').grid(row=i+3, column=2, padx=5, pady=10)
            tk.Label(self.fc_value_frame, text='     ').grid(row=i+3, column=3, padx=(5, 10), pady=10)

        # create and place demand total labels
        tk.Label(self.fc_value_frame, text='Remaining demand').grid(row=i+4, column=0, pady=10, columnspan=2)
        tk.Label(self.fc_value_frame, text=self.game.fc['demand'].sum()).grid(row=i+4, column=2, pady=10)

        self.change_bg_to_white(self.fc_value_frame)


    def convert_stdev_to_confidence(self, mu, sigma):
        if sigma / mu > 0.25:
            return 'low'
        elif sigma / mu > 0.1:
            return 'medium'
        else:
            return 'high'


    def build_overbook_frame(self):
        self.ob_frame = tk.Frame(self.right_frame)
        self.ob_frame.grid(row=0, column=0, sticky='N S E W')
        self.ob_frame.rowconfigure((0,1,2), weight=1)
        self.ob_frame.columnconfigure((0,1,2), weight=1)

        ob_msg = f'We know that, on average, {int(self.game.ns_rate * 100)}%\nof customers will not show up\nfor the flight, so we might overbook.\nHow many seats would you\nlike to overbook by?'
        
        self.ob_label = tk.Label(self.ob_frame, text=ob_msg)
        self.ob_label.grid(row=0, column=0, padx=5, pady=10)

        self.ob_value = tk.StringVar()
        self.ob_entry = tk.Entry(self.ob_frame, width=10, textvariable=self.ob_value)
        self.ob_entry.grid(row=0, column=1, padx=5, pady=10)
        self.ob_entry_funcid = self.ob_entry.bind('<Return>', self.apply_overbooking)
        self.ob_entry.focus_set()

        self.check_image = ImageTk.PhotoImage(Image.open('images/check.png'))
        self.check_button = tk.Button(self.ob_frame, image=self.check_image)
        self.check_button.image = self.check_image
        self.check_button.grid(row=0, column=2, padx=5, pady=10)
        self.check_button_funcid =self.check_button.bind('<Button-1>', self.apply_overbooking)

        self.change_bg_to_white(self.ob_frame)


    def apply_overbooking(self, event=None):
        self.game.au = self.game.ac + int(self.ob_entry.get())
        self.game.sa = self.game.au
        self.skip_ob = True

        self.ob_entry.unbind('<Return>', self.ob_entry_funcid)
        self.ob_entry['state'] = 'disabled'
        self.check_button.unbind('Button-1>', self.check_button_funcid)
        self.check_button['state'] = 'disabled'
        
        self.new_au_label = tk.Label(self.ob_frame, 
            text=f'OK. You\'ll sell up to {self.game.au} seats. \nAt the end, we\'ll see how many people no-show.', padx=5, pady=5, bg='lightblue')
        self.new_au_label.grid(row=1, column=0, columnspan=3, padx=5, pady=10)

        self.next_image = ImageTk.PhotoImage(Image.open('images/next.png'))

        next_button_text = 'Start selling'
        next_command = self.build_game
    
        self.next_image_button = tk.Button(self.ob_frame, text=next_button_text, image=self.next_image, compound='top', height=120, width=120, 
                bg='white', command=self.confirm_overbooking)

        self.next_image_button.image = self.next_image
        self.next_image_button.grid(row=2, column=0, columnspan=3, pady=10)


    def confirm_overbooking(self):
        self.main.destroy()
        self.build_game()


    def build_reserve_frame(self):
        self.rsv_frame = tk.Frame(self.right_frame)
        self.rsv_frame.grid(row=0, column=0, sticky='N S E W')
        self.rsv_frame.rowconfigure((0,1,2), weight=1)
        self.rsv_frame.columnconfigure((0,1,2), weight=1)

        if self.game.curr_dfd > 0:
            rsv_msg = f'How many seats would\nyou like to reserve\ntoday at ${self.game.fc.loc[self.game.curr_dfd, "fare"]}?'
        else:
            rsv_msg = f'The flight departs today,\nso you should reserve\nall remaining seats at ${self.game.fc.loc[self.game.curr_dfd, "fare"]}.'

        self.rsv_label = tk.Label(self.rsv_frame, text=rsv_msg)
        self.rsv_label.grid(row=0, column=0, padx=5, pady=10)

        self.rsv_value = tk.StringVar()
        self.rsv_entry = tk.Entry(self.rsv_frame, width=10, textvariable=self.rsv_value)
        self.rsv_entry.grid(row=0, column=1, padx=5, pady=10)
        self.rsv_entry_funcid = self.rsv_entry.bind('<Return>', self.run_dfd)
        self.rsv_entry.focus_set()
        if self.game.curr_dfd == 0:
            self.rsv_entry.insert(0, self.game.sa)

        self.check_image = ImageTk.PhotoImage(Image.open('images/check.png'))
        self.check_button = tk.Button(self.rsv_frame, image=self.check_image)
        self.check_button.image = self.check_image
        self.check_button.grid(row=0, column=2, padx=5, pady=10)
        self.check_button_funcid =self.check_button.bind('<Button-1>', self.run_dfd)

        self.change_bg_to_white(self.rsv_frame)


    def build_departure_frame(self):
        self.dfdsim.dfd_cleanup()

        self.stats_frame.destroy()
        self.build_stats_frame()

        # done with middle frame; leaderboard will go in right
        self.middle_frame.destroy()

        self.rsv_frame.destroy()

        self.dep_frame = tk.Frame(self.right_frame)
        self.dep_frame.grid(row=0, column=0, sticky='N S E W')
        self.dep_frame.rowconfigure((0,1,2), weight=1)
        self.dep_frame.columnconfigure(0, weight=1)

        self.game.noshows = self.game.simulate_noshows()
        self.game.total_lb -= self.game.noshows
        self.game.dbs = max(0, self.game.total_lb - self.game.ac)

        noshow_people = (lambda x: 'person' if x == 1 else 'people') (self.game.noshows)
        db_people = (lambda x: 'person' if x == 1 else 'people') (self.game.dbs)
        dep_msg = f'At departure, {self.game.noshows} {noshow_people} no-showed,\nso there are {self.game.total_lb} people\nfor {self.game.ac} seats.\n'
        if self.game.dbs > 0:
            dep_msg += f'\n\nYou\'ll need to offer\nDB compensation to {self.game.dbs} {db_people}.'
        else:
            dep_msg += 'No need for volunteers.'
        self.dep_label = tk.Label(self.dep_frame, text=dep_msg, bg='lightblue')
        self.dep_label.grid(row=0, column=0, padx=5, pady=10)

        if self.game.dbs > 0:
            next_text = 'Compensate DBs'
            next_command = self.compensate_dbs
        else:
            next_text = 'See results'
            next_command = self.end_game
        self.next_image_button = tk.Button(self.dep_frame, text=next_text, image=self.next_image, compound='top', height=120, width=120, 
                bg='white', command=next_command)
        self.next_image_button.image = self.next_image
        self.next_image_button.grid(row=2, column=0, pady=10)

        self.change_bg_to_white(self.dep_frame)


    def compensate_dbs(self):
        self.game.db_cost = self.game.compensate_dbs()
        self.game.total_db_cost = self.game.db_cost * self.game.dbs
        self.game.total_rev -= self.game.total_db_cost

        if self.game.db_cost <= 250:
            self.db_comp_msg = f'You got lucky. There were\nplenty of other options,\nand you only paid ${self.game.db_cost:,}\nper denied boarding.'
        elif self.game.db_cost <= 1000:
            self.db_comp_msg = f'Could be worse. There were\nlimited alternative flights,\nand you paid ${self.game.db_cost:,}\nper denied boarding.'
        else:
            self.db_comp_msg = f'Ouch! No one was flexible\nwith their travel plans,\nand you had to pay ${self.game.db_cost:,}\nper denied boarding.'
        self.db_outcome_label = tk.Label(self.dep_frame, text=self.db_comp_msg, padx=5, pady=5, bg='lightblue')
        self.db_outcome_label.grid(row=1, column=0, padx=5, pady=10)

        self.next_image_button = tk.Button(self.dep_frame, text='See results', image=self.next_image, compound='top', height=120, width=120, 
                bg='white', command=self.end_game)
        self.next_image_button.image = self.next_image
        self.next_image_button.grid(row=2, column=0, pady=10)


    def display_option_frame(self):
        # check if parent is home or game
        # if home, offer leaderboard and admin buttons
        # if game, offer quit or main menu button
        
        self.return_to_home_button = tk.Button(self.option_frame, text='Main menu', fg='red', command=self.return_to_home)
        self.return_to_home_button.grid(row=0, column=0)

        self.change_bg_to_white(self.option_frame)


    def return_to_home(self):
        # if game still in progress, confirm they want to leave
        if self.game.curr_dfd >= 0:
            go_home = tk.messagebox.askyesno('Main menu?', 'Return to the main menu? Your progress will be lost.')
            # if they confirm, go home
            if go_home:
                self.main.destroy()
                self.build_home()
        # if the game is over, just go home
        else:
            self.main.destroy()
            self.build_home()


    ### SIMULATE DFD ###


    def run_dfd(self, event=None):
        self.rsv = int(self.rsv_entry.get())  # TODO: validate this somehow
        if (self.rsv < 0) or (self.rsv > self.game.sa):
            print('error')

        self.rsv_entry.unbind('<Return>', self.rsv_entry_funcid)
        self.rsv_entry['state'] = 'disabled'
        self.check_button.unbind('Button-1>', self.check_button_funcid)
        self.check_button['state'] = 'disabled'
        
        self.dfdsim.observe_bookings(self.rsv)

        rsv_s = (lambda x: '' if x == 1 else 's') (self.rsv)
        lb_s = (lambda x: '' if x == 1 else 's') (self.dfdsim.lb)
        lb_people = (lambda x: 'person' if x == 1 else 'people') (self.dfdsim.lb)
        
        self.outcome_label = tk.Label(self.rsv_frame, 
            text=f'{self.dfdsim.arr} {lb_people} showed up to book today, \nand you reserved {self.rsv} seat{rsv_s}. \
        \n\nYou sold {self.dfdsim.lb} seat{lb_s} and earned ${self.dfdsim.rev:,}.', padx=5, pady=5, bg='lightblue')
        self.outcome_label.grid(row=1, column=0, columnspan=3, padx=5, pady=10)

        # if dfd > 0, go to next dfd
        self.next_image = ImageTk.PhotoImage(Image.open('images/next.png'))

        if self.game.curr_dfd > 0:
            next_button_text = 'Next day'
            next_command = self.go_to_next_dfd
        else:
            if self.game.easy_mode:
                next_button_text = 'See results'
                next_command = self.end_game
            else:
                next_button_text = 'Flight departure'
                next_command = self.build_departure_frame
        
        self.next_image_button = tk.Button(self.rsv_frame, text=next_button_text, image=self.next_image, compound='top', height=120, width=120, 
                bg='white', command=next_command)

        self.next_image_button.image = self.next_image
        self.next_image_button.grid(row=2, column=0, columnspan=3, pady=10)
        

    def go_to_next_dfd(self):
        self.dfdsim.dfd_cleanup()
        self.main.destroy()
        self.build_game()


    def run_departure(self):
        self.dfdsim.dfd_cleanup()
        self.reserve_frame.destroy()
        self.display_departure_frame()


    def end_game(self):
        # self.dfdsim.dfd_cleanup() -- moved to build_end
        self.add_results_to_db()
        self.build_end()


    def add_results_to_db(self):
        result = (self.player_name_value.get(),
            self.player_loc_value.get(),
            self.game.game_type,
            self.game.total_rev,
            datetime.now().isoformat()
            )
        conn = create_connection(db_file)
        insert_results(conn, result)
        conn.close()


    ### END PAGE ###


    def build_end(self):
        # self.right_frame.destroy() -- not needed, destroying middle in build_departure_frame
        if self.game.easy_mode:
            self.dfdsim.dfd_cleanup()
            self.middle_frame.destroy()
        # self.fc_frame.destroy()
        self.build_end_stats_frame()
        self.build_leaderboard_frame()


    def build_end_stats_frame(self):
        self.date_frame.destroy()
        self.date_frame = tk.Frame(self.stats_frame)
        self.date_frame.grid(row=1, column=1, padx=5)

        self.today_label = tk.Label(self.date_frame, text=f'The flight has departed.')
        self.today_label.grid(row=0, column=0)

        self.seat_frame.destroy()
        self.seat_frame = tk.Frame(self.stats_frame)
        self.seat_frame.grid(row=2, column=1, padx=5)

        self.game.total_onboard = min(self.game.total_lb, self.game.ac)

        self.ac_label = tk.Label(self.seat_frame, text=f'Total on board:')
        self.ac_value = tk.Label(self.seat_frame, text=f'{self.game.total_onboard}')
        self.ac_label.grid(row=0, column=0, sticky='W')
        self.ac_value.grid(row=0, column=1)
        self.lf_label = tk.Label(self.seat_frame, text=f'Final load factor:')
        self.lf_value = tk.Label(self.seat_frame, text=f'{int(100 * self.game.total_onboard / self.game.ac)}%')
        self.lf_label.grid(row=1, column=0, sticky='W')
        self.lf_value.grid(row=1, column=1)
        if not self.game.easy_mode:
            self.db_label = tk.Label(self.seat_frame, text=f'Denied boardings:')
            self.db_value = tk.Label(self.seat_frame, text=f'{self.game.dbs}')
            self.db_label.grid(row=2, column=0, sticky='W')
            self.db_value.grid(row=2, column=1)

        self.rev_frame.destroy()
        self.rev_frame = tk.Frame(self.stats_frame)
        self.rev_frame.grid(row=3, column=1, padx=5)
        self.rev_label = tk.Label(self.rev_frame, text='Final revenue:')
        self.rev_value = tk.Label(self.rev_frame, text=f'${self.game.total_rev:,}')
        self.rev_label.grid(row=0, column=0, sticky='W')
        self.rev_value.grid(row=0, column=1)


    def build_leaderboard_frame(self):
        self.lb_frame = tk.Frame(self.right_frame)
        self.lb_frame.grid(row=0, column=0, sticky='N S E W', pady=10)
        self.lb_frame.rowconfigure(1, weight=1)
        self.lb_frame.columnconfigure(0, weight=1)

        self.lb_header = tk.Label(self.lb_frame, text='--- LEADERBOARD ---', font='Helvetica 14 bold')
        self.lb_header.grid(row=0, column=0, padx=5)

        self.lb_value_frame = tk.Frame(self.lb_frame)
        self.lb_value_frame.grid(row=1, column=0)

        self.results_df = self.get_results()

        self.lb_label_1 = tk.Label(self.lb_value_frame, text='Name')
        self.lb_label_2 = tk.Label(self.lb_value_frame, text='From')
        self.lb_label_3 = tk.Label(self.lb_value_frame, text='Game')
        self.lb_label_4 = tk.Label(self.lb_value_frame, text='Revenue')

        self.lb_label_1.grid(row=0, column=0, padx=5, pady=10)  # name
        self.lb_label_2.grid(row=0, column=1, padx=5, pady=10)  # from
        self.lb_label_3.grid(row=0, column=2, padx=5, pady=10)  # game
        self.lb_label_4.grid(row=0, column=3, padx=5, pady=10)  # revenue

        # create and place leaderboard values
        player_on_leaderboard = False

        def add_this_player():
            tk.Label(self.lb_value_frame, text=self.game.player).grid(row=i+1, column=0, padx=5, pady=5)
            tk.Label(self.lb_value_frame, text=self.game.location).grid(row=i+1, column=1, padx=5, pady=5)
            tk.Label(self.lb_value_frame, text=self.game.game_type).grid(row=i+1, column=2, padx=5, pady=5)
            tk.Label(self.lb_value_frame, text=f'${self.game.total_rev:,}').grid(row=i+1, column=3, padx=5, pady=5)

        for i in range(min(8, len(self.results_df))):
            if (self.results_df.loc[i, 'revenue'] > self.game.total_rev) or player_on_leaderboard:
                tk.Label(self.lb_value_frame, text=self.results_df.loc[i, 'name']).grid(row=i+1, column=0, padx=5, pady=5)
                tk.Label(self.lb_value_frame, text=self.results_df.loc[i, 'location']).grid(row=i+1, column=1, padx=5, pady=5)
                tk.Label(self.lb_value_frame, text=self.results_df.loc[i, 'game']).grid(row=i+1, column=2, padx=5, pady=5)
                tk.Label(self.lb_value_frame, text=f'${self.results_df.loc[i, "revenue"]:,}').grid(row=i+1, column=3, padx=5, pady=5)
            else:
                player_on_leaderboard = True
                add_this_player()
        
        if not player_on_leaderboard:
            i += 1
            tk.Label(self.lb_value_frame, text='-----').grid(row=i+1, column=0, padx=5, pady=5)
            tk.Label(self.lb_value_frame, text='-----').grid(row=i+1, column=1, padx=5, pady=5)
            tk.Label(self.lb_value_frame, text='-----').grid(row=i+1, column=2, padx=5, pady=5)
            tk.Label(self.lb_value_frame, text='-----').grid(row=i+1, column=3, padx=5, pady=5)
            i += 1
            add_this_player()

        self.change_bg_to_white(self.lb_frame)


    def get_results(self):
        easy_query = """
        select * 
        from results 
        where game = 'Easy mode' 
        order by revenue desc, gametime desc;
        """

        real_query = """
        select * 
        from results 
        where game <> 'Easy mode' 
        order by revenue desc, gametime desc;
        """

        conn = create_connection(db_file)
        if self.game.easy_mode:
            df = pd.read_sql_query(easy_query, conn)
        else:
            df = pd.read_sql_query(real_query, conn)
        conn.close()

        return df


    ### HELPERS ###

    
    def change_bg_to_white(self, parent):
        for widget in parent.winfo_children():
            widget.configure(bg='white')
