import tkinter as tk
from datetime import datetime
from random import choices, randint
from tkinter import messagebox
from tkinter.font import Font, nametofont
from tkinter.ttk import Notebook

import pandas as pd
from PIL import Image, ImageTk

from config import DB_PATH
from db import GameDB
from game import DFDSimulation, EasyGame, RealGame
from scenario import EasyScenario, RealScenario, scenario_dict
from config import logger


class GUI():
    
    def __init__(self, root):
        self.root = root

        self.root.title('The PRM Game')
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.geometry('1600x800')

        self.default_font = nametofont('TkDefaultFont')
        self.default_font.configure(family='Helvetica', size='12')
        self.entry_font = nametofont('TkTextFont')
        self.entry_font.configure(family='Helvetica', size='12')
        self.header_font = Font(family='Helvetica', size='14', weight='bold')
        self.label_font = Font(family='Helvetica', size='12', weight='bold')
        # self.root.option_add('*Dialog.msg.font', 'Helvetica 18')

        self.game_db = GameDB(DB_PATH)

        self.build_home()

    ### HOME PAGE

    def build_home(self):
        # create the main container
        self.home = tk.Frame(self.root, padx=30, pady=30, relief='sunken', borderwidth=5, width=1200, height=600)
        self.home.grid(column=0, row=0, sticky='N S E W')
        self.home.rowconfigure((0,1), weight=1)
        self.home.columnconfigure((0,1), weight=1)

        self.build_logo_frame()
        self.build_player_frame()
        self.build_button_frame()
        self.build_home_option_frame()
        

    def build_logo_frame(self):
        self.logo_frame = tk.Frame(self.home, padx=20, pady=20, relief='groove', borderwidth=5, bg='white')
        self.logo_frame.rowconfigure(0, weight=1)
        self.logo_frame.columnconfigure(0, weight=1)
        self.logo_frame.grid(row=0, column=0, padx=10, sticky='N S E W', rowspan=3)

        self.logo_path = 'images/airplane_title.png'
        self.logo_img = ImageTk.PhotoImage(Image.open(self.logo_path))
        self.logo = tk.Label(self.logo_frame, image=self.logo_img)
        self.logo.grid(row=0, column=0, sticky='N S E W')

        self.change_bg_to_white(self.logo_frame)


    def build_player_frame(self):
        self.player_frame = tk.Frame(self.home, padx=20, pady=10, relief='groove', borderwidth=5, bg='white')
        self.player_frame.grid(row=0, column=1, sticky='N E W')

        self.player_frame.grid_rowconfigure(0, weight=1)
        self.player_frame.grid_rowconfigure(1, weight=1)
        self.player_frame.grid_columnconfigure(0, weight=1)
        self.player_frame.grid_columnconfigure(1, weight=1)

        self.player_name_label = tk.Label(self.player_frame, text='What\'s your name?', bg='white')
        self.player_name_value = tk.StringVar()
        self.player_name_entry = tk.Entry(self.player_frame, textvariable=self.player_name_value)
        self.player_name_label.grid(row=0, column=0, padx=20, pady=10, sticky='N W')
        self.player_name_entry.grid(row=0, column=1, padx=20, pady=10, sticky='N E')

        self.player_loc_label = tk.Label(self.player_frame, text='Where are you from?', bg='white')
        self.player_loc_value = tk.StringVar()
        self.player_loc_entry = tk.Entry(self.player_frame, textvariable=self.player_loc_value)
        self.player_loc_label.grid(row=1, column=0, padx=20, pady=10, sticky='S W')
        self.player_loc_entry.grid(row=1, column=1, padx=20, pady=10, sticky='S E')

        self.player_name_entry.focus_set()
        self.player_name_entry.insert(0, 'Test')
        self.player_loc_entry.insert(0, 'ORD')


    def build_button_frame(self):
        self.button_frame = tk.Frame(self.home, pady=10, relief='groove', borderwidth=5, bg='white')
        self.button_frame.grid(row=1, column=1, sticky='N S E W')
        self.button_frame.rowconfigure(0, weight=1)
        self.button_frame.columnconfigure((0,1), weight=1)

        self.easy_button_path = 'images/100.png'
        self.easy_button_image = ImageTk.PhotoImage(Image.open(self.easy_button_path).resize((80,80), resample=5))
        self.easy_button = tk.Button(self.button_frame, text='Play easy mode', image=self.easy_button_image, compound='top', height=160, width=240, bg='white', 
            command=self.play_easy_mode, pady=10)
        self.easy_button.grid(row=0, column=0, padx=20, pady=10)

        self.real_button_people = ['man','woman','person']
        self.real_button_path = f'images/shrug{randint(1,6)}.png'
        self.real_button_image = ImageTk.PhotoImage(Image.open(self.real_button_path).resize((80,80), resample=5))
        self.real_button = tk.Button(self.button_frame, text='Play real life mode', image=self.real_button_image, compound='top', height=160, width=240, bg='white', 
            command=self.build_real_button_frame, pady=10)
        self.real_button.grid(row=0, column=1, padx=20, pady=10)


    def build_real_button_frame(self):
        self.button_frame.rowconfigure((0,1), weight=1)

        # real_mode_button_frame = tk.Frame(self.button_frame, bg='white', relief='groove', borderwidth=5)
        real_mode_button_frame = tk.Frame(self.button_frame, bg='white')
        real_mode_button_frame.grid(row=1, column=0, columnspan=2, sticky='S E W')
        real_mode_button_frame.grid_rowconfigure((0,1), weight=1)
        real_mode_button_frame.grid_columnconfigure((0,1,2), weight=1)

        game1_image_path = scenario_dict[1]['image']
        game1_image = ImageTk.PhotoImage(Image.open(game1_image_path).resize((80,80), resample=5))
        game1_button = tk.Button(real_mode_button_frame, text=scenario_dict[1]['name'], bg='white', image=game1_image, compound='left',
            command=lambda: self.play_real_mode(1), padx=5)
        game1_button.image = game1_image
        game1_button.grid(row=0, column=0, padx=(20, 10), pady=10)

        game2_image_path = scenario_dict[2]['image']
        game2_image = ImageTk.PhotoImage(Image.open(game2_image_path).resize((80,80), resample=5))
        game2_button = tk.Button(real_mode_button_frame, text=scenario_dict[2]['name'], bg='white', image=game2_image, compound='left',
            command=lambda: self.play_real_mode(2), padx=5)
        game2_button.image = game2_image
        game2_button.grid(row=0, column=1, padx=10, pady=10)

        game3_image_path = scenario_dict[3]['image']
        game3_image = ImageTk.PhotoImage(Image.open(game3_image_path).resize((80,80), resample=5))
        game3_button = tk.Button(real_mode_button_frame, text=scenario_dict[3]['name'], bg='white', image=game3_image, compound='left',
            command=lambda: self.play_real_mode(3), padx=5)
        game3_button.image = game3_image
        game3_button.grid(row=0, column=2, padx=(10, 20), pady=10)

        game4_image_path = scenario_dict[4]['image']
        game4_image = ImageTk.PhotoImage(Image.open(game4_image_path).resize((80,80), resample=5))
        game4_button = tk.Button(real_mode_button_frame, text=scenario_dict[4]['name'], bg='white', image=game4_image, compound='left',
            command=lambda: self.play_real_mode(4), padx=5)
        game4_button.image = game4_image
        game4_button.grid(row=1, column=0, padx=(20, 10), pady=10)

        game5_image_path = scenario_dict[5]['image']
        game5_image = ImageTk.PhotoImage(Image.open(game5_image_path).resize((80,80), resample=5))
        game5_button = tk.Button(real_mode_button_frame, text=scenario_dict[5]['name'], bg='white', image=game5_image, compound='left',
            command=lambda: self.play_real_mode(5), padx=5)
        game5_button.image = game5_image
        game5_button.grid(row=1, column=1, padx=10, pady=10)

        game6_image_path = scenario_dict[6]['image']
        game6_image = ImageTk.PhotoImage(Image.open(game6_image_path).resize((80,80), resample=5))
        game6_button = tk.Button(real_mode_button_frame, text=scenario_dict[6]['name'], bg='white', image=game6_image, compound='left',
            command=lambda: self.play_real_mode(6), padx=5)
        game6_button.image = game6_image
        game6_button.grid(row=1, column=2, padx=(10, 20), pady=10)

        game3_button['state'] = 'disabled'
        game4_button['state'] = 'disabled'
        game5_button['state'] = 'disabled'
        game6_button['state'] = 'disabled'


    def play_easy_mode(self):
        if (self.player_name_value.get() != '') and (self.player_loc_value.get() != ''):
            self.home.destroy()
            self.game = EasyGame(EasyScenario(scenario_dict[0]))

            logger.info('******************************')
            logger.info(f'New game {self.game.game_type}')
            logger.info(f'--------- Game start --------')
            self.log_dfd_header
            self.log_current_stats()

            self.skip_ob = True
            self.game.set_player_info(self.player_name_value.get(), self.player_loc_value.get())
            self.build_game()
        else:
            tk.messagebox.showerror(title='Error', message=f'Please enter a player name and location before continuing.')


    def play_real_mode(self, which_game):
        if (self.player_name_value.get() != '') and (self.player_loc_value.get() != ''):
            self.home.destroy()
            self.game = RealGame(RealScenario(scenario_dict[which_game]))
            
            logger.info('******************************')
            logger.info(f'New game {self.game.game_type}')
            logger.info(f'--------- Game start --------')
            self.log_dfd_header
            self.log_current_stats()
            
            self.skip_ob = False
            self.game.set_player_info(self.player_name_value.get(), self.player_loc_value.get())
            self.build_game()
        else:
            tk.messagebox.showerror(title='Error', message=f'Please enter a player name and location before continuing.')


    def build_home_option_frame(self):
        self.home_option_frame = tk.Frame(self.home, relief='groove', borderwidth=5, bg='white')
        self.home_option_frame.grid(row=2, column=1, pady=(20, 0), sticky='E')

        self.leaderboard_button = tk.Button(self.home_option_frame, text='Leaderboard', fg='#0033A0', command=self.build_home_leaderboard)
        self.leaderboard_button.grid(row=0, column=0, padx=(10, 5), pady=10, sticky='E')

        self.admin_button = tk.Button(self.home_option_frame, text='Admin', fg='#0033A0', command=self.build_admin)
        self.admin_button.grid(row=0, column=1, padx=(5, 10), pady=10, sticky='E')

        self.change_bg_to_white(self.home_option_frame)


    def build_admin(self):
        self.player_frame.destroy()
        self.button_frame.destroy()
        self.home_option_frame.destroy()
        self.build_admin_frame()


    def build_admin_frame(self):
        self.admin_frame = tk.Frame(self.home, relief='groove', borderwidth=5, bg='white', padx=10, pady=10)
        self.admin_frame.grid(row=0, column=1, sticky='N S E W')

        self.admin_label = tk.Label(self.admin_frame, text='Admin options', bg='white', font=self.header_font)
        self.admin_label.grid(row=0, column=0, sticky='N')

        self.reset_leaderboard_button = tk.Button(self.admin_frame, text='Reset leaderboard', fg='#0033A0', command=self.reset_leaderboard)
        self.reset_leaderboard_button.grid(row=1, column=0, padx=10, pady=10)

        self.admin_option_frame = tk.Frame(self.home, relief='groove', borderwidth=5, bg='white')
        self.admin_option_frame.grid(row=2, column=1, pady=(20, 0), sticky='S E')
        self.admin_option_frame.rowconfigure(0, weight=1)
        self.admin_option_frame.columnconfigure(0, weight=1)

        self.main_menu_button = tk.Button(self.admin_option_frame, text='Main menu', fg='#0033A0', command=self.rebuild_home_from_home)
        self.main_menu_button.grid(row=0, column=2, padx=10, pady=10)


    def rebuild_home_from_home(self):
        self.home.destroy()
        self.build_home()

    
    ### GAME


    def build_game(self):
        
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

        self.game_option_frame = tk.Frame(self.main, padx=10, pady=20, relief='groove', borderwidth=5, bg='white')
        self.game_option_frame.grid(row=1, column=2, padx=10, pady=(50, 0), sticky='S E')

        self.build_stats_frame(which='game')
        self.build_forecast_frame()
        if not self.skip_ob:
            self.build_overbook_frame()
        else:
            self.build_reserve_frame()
        self.build_game_option_frame()

        self.dfdsim = DFDSimulation(self.game, self.game.curr_dfd)

        self.change_bg_to_white(self.left_frame)
        self.change_bg_to_white(self.middle_frame)
        self.change_bg_to_white(self.right_frame)

    
    def build_stats_frame(self, which):
        self.stats_frame = tk.Frame(self.left_frame)
        self.stats_frame.grid(row=0, column=0, sticky='N S E W')
        self.stats_frame.rowconfigure((1,2,3), weight=1)
        self.stats_frame.columnconfigure((0,1), weight=1)
        
        ### images
        
        self.stats_header = tk.Label(self.stats_frame, text=f'Flight to {self.game.game_type}', font='Helvetica 14 bold')
        self.stats_header.grid(row=0, column=0, columnspan=2, padx=5, pady=10)

        self.date_image = ImageTk.PhotoImage(Image.open('images/calendar.png').resize((80,80), resample=5))
        self.date_image_label = tk.Label(self.stats_frame, image=self.date_image)
        self.date_image_label.image = self.date_image
        self.date_image_label.grid(row=1, column=0, pady=10)

        self.seat_image = ImageTk.PhotoImage(Image.open('images/seat.png').resize((80,80), resample=5))
        self.seat_image_label = tk.Label(self.stats_frame, image=self.seat_image)
        self.seat_image_label.image = self.seat_image
        self.seat_image_label.grid(row=2, column=0, pady=10)
        
        self.money_image = ImageTk.PhotoImage(Image.open('images/money.png').resize((80,80), resample=5))
        self.money_image_label = tk.Label(self.stats_frame, image=self.money_image)
        self.money_image_label.image = self.money_image
        self.money_image_label.grid(row=3, column=0, pady=10)

        ### date frame and values
        self.date_frame = tk.Frame(self.stats_frame)
        self.date_frame.grid(row=1, column=1, padx=(0,30), sticky='E W')
        self.date_frame.columnconfigure((0,1), weight=1)

        if which == 'game':
            self.today_label = tk.Label(self.date_frame, text=f'Today:', font=self.label_font)
            self.today_value = tk.Label(self.date_frame, text=f'{self.game.curr_dow_long}')
            self.today_label.grid(row=0, column=0, sticky='W')
            self.today_value.grid(row=0, column=1, sticky='E')
            self.dep_label = tk.Label(self.date_frame, text=f'Departure:', font=self.label_font)
            self.dep_value = tk.Label(self.date_frame, text=f'Friday')
            self.dep_label.grid(row=1, column=0, sticky='W')
            self.dep_value.grid(row=1, column=1, sticky='E')
        elif which == 'end':
            self.today_label = tk.Label(self.date_frame, text=f'The flight has departed.', font=self.label_font)
            self.today_label.grid(row=0, column=0, sticky='W')

        ### seat frame and values
        self.seat_frame = tk.Frame(self.stats_frame)
        self.seat_frame.grid(row=2, column=1, padx=(0,30), sticky='E W')
        self.seat_frame.columnconfigure((0,1), weight=1)


        if which == 'game':
            # AC
            self.ac_label = tk.Label(self.seat_frame, text=f'Aircraft capacity:', font=self.label_font)
            self.ac_value = tk.Label(self.seat_frame, text=f'{self.game.ac}')
            self.ac_label.grid(row=0, column=0, sticky='W')
            self.ac_value.grid(row=0, column=1, sticky='E')
            # AU
            if not self.game.easy_mode:
                self.au_label = tk.Label(self.seat_frame, text=f'Authorized with overbooking:', font=self.label_font)
                self.au_value = tk.Label(self.seat_frame, text=f'{self.game.au}')
                self.au_label.grid(row=1, column=0, sticky='W')
                self.au_value.grid(row=1, column=1, sticky='E')
            # LB
            self.lb_label = tk.Label(self.seat_frame, text=f'Seats sold:', font=self.label_font)
            self.lb_value = tk.Label(self.seat_frame, text=f'{self.game.total_lb}')
            self.lb_label.grid(row=2, column=0, sticky='W')
            self.lb_value.grid(row=2, column=1, sticky='E')
            # SA
            self.sa_label = tk.Label(self.seat_frame, text=f'Remaining seats:', font=self.label_font)
            self.sa_value = tk.Label(self.seat_frame, text=f'{self.game.sa}')
            self.sa_label.grid(row=3, column=0, sticky='W')
            self.sa_value.grid(row=3, column=1, sticky='E')
        elif which == 'end':
            self.game.total_onboard = min(self.game.total_lb, self.game.ac)
            # LB
            self.lb_label = tk.Label(self.seat_frame, text=f'Total on board:', font=self.label_font)
            self.lb_value = tk.Label(self.seat_frame, text=f'{self.game.total_onboard}')
            self.lb_label.grid(row=0, column=0, sticky='W')
            self.lb_value.grid(row=0, column=1, sticky='E')
            # LF
            self.lf_label = tk.Label(self.seat_frame, text=f'Final load factor:', font=self.label_font)
            self.lf_value = tk.Label(self.seat_frame, text=f'{int(100 * self.game.total_onboard / self.game.ac)}%')
            self.lf_label.grid(row=1, column=0, sticky='W')
            self.lf_value.grid(row=1, column=1, sticky='E')
            # DB
            if not self.game.easy_mode:
                self.db_label = tk.Label(self.seat_frame, text=f'Denied boardings:', font=self.label_font)
                self.db_value = tk.Label(self.seat_frame, text=f'{self.game.dbs}')
                self.db_label.grid(row=2, column=0, sticky='W')
                self.db_value.grid(row=2, column=1, sticky='E')

        ### revenue frame and values
        self.rev_frame = tk.Frame(self.stats_frame)
        self.rev_frame.grid(row=3, column=1, padx=(0,30), sticky='E W')
        self.rev_frame.columnconfigure((0,1), weight=1)

        # rev
        self.rev_label = tk.Label(self.rev_frame, text=f'Revenue:', font=self.label_font)
        if (which == 'game') or self.game.easy_mode:
            self.rev_value = tk.Label(self.rev_frame, text=f'${self.game.total_rev:,}')
        elif (which == 'end') and not self.game.easy_mode:
            if self.game.dbs > 0:
                self.rev_value = tk.Label(self.rev_frame, text=f'${self.game.total_rev + self.game.total_db_cost:,}')  # need to back into pre-DB rev
            else:
                self.rev_value = tk.Label(self.rev_frame, text=f'${self.game.total_rev:,}')
        self.rev_label.grid(row=0, column=0, sticky='W')
        self.rev_value.grid(row=0, column=1, sticky='E')
        if (which == 'end') and not self.game.easy_mode:
            # DB cost
            self.db_cost_label = tk.Label(self.rev_frame, text=f'DB cost:', font=self.label_font)
            if self.game.dbs > 0:
                self.db_cost_value = tk.Label(self.rev_frame, text=f'${self.game.total_db_cost:,}')
            else:
                self.db_cost_value = tk.Label(self.rev_frame, text=f'$0')
            self.db_cost_label.grid(row=1, column=0, sticky='W')
            self.db_cost_value.grid(row=1, column=1, sticky='E')
            # Final rev
            self.final_rev_label = tk.Label(self.rev_frame, text=f'Final revenue:', font=self.label_font)
            self.final_rev_value = tk.Label(self.rev_frame, text=f'${self.game.total_rev:,}')
            self.final_rev_label.grid(row=2, column=0, sticky='W')
            self.final_rev_value.grid(row=2, column=1, sticky='E')
                
        self.change_bg_to_white(self.left_frame)
        self.change_bg_to_white(self.stats_frame)
        self.change_bg_to_white(self.date_frame)
        self.change_bg_to_white(self.seat_frame)
        self.change_bg_to_white(self.rev_frame)


    def build_forecast_frame(self):
        self.fc_frame = tk.Frame(self.middle_frame)
        self.fc_frame.grid(row=0, column=0, sticky='N S E W')
        self.fc_frame.rowconfigure(1, weight=1)
        self.fc_frame.columnconfigure(0, weight=1)

        self.fc_header = tk.Label(self.fc_frame, text='Forecast', font=self.header_font)
        self.fc_header.grid(row=0, column=0, padx=10, pady=10)

        self.fc_value_frame = tk.Frame(self.fc_frame)
        self.fc_value_frame.grid(row=1, column=0)

        self.fc_label_1 = tk.Label(self.fc_value_frame, text='Booking\nday', font=self.label_font)
        self.fc_label_2 = tk.Label(self.fc_value_frame, text='Fare', font=self.label_font)
        self.fc_label_3 = tk.Label(self.fc_value_frame, text='Average\ndemand', font=self.label_font)
        if not self.game.easy_mode:
            self.fc_label_4 = tk.Label(self.fc_value_frame, text='Likely\nrange', font=self.label_font)
        
        self.fc_label_1.grid(row=0, column=0, padx=10, pady=10)  # DOW
        self.fc_label_2.grid(row=0, column=1, padx=10, pady=10)  # fare
        if self.game.easy_mode:
            self.fc_label_3.grid(row=0, column=2, padx=10, pady=10)  # demand
        else:
            self.fc_label_3.grid(row=0, column=2, padx=10, pady=10)  # demand
            self.fc_label_4.grid(row=0, column=3, padx=10, pady=10)  # stdev

        # create and place forecast value labels
        for i, dfd in enumerate(range(self.game.curr_dfd, -1, -1)):
            tk.Label(self.fc_value_frame, text=self.game.fc.loc[dfd, 'dow_short']).grid(row=i+2, column=0, padx=10)
            tk.Label(self.fc_value_frame, text=f"${self.game.fc.loc[dfd, 'fare']:,}").grid(row=i+2, column=1, padx=10, pady=10)
            if self.game.easy_mode:
                tk.Label(self.fc_value_frame, text=self.game.fc.loc[dfd, 'demand']).grid(row=i+2, column=2, padx=10, pady=10)
            else:
                tk.Label(self.fc_value_frame, text=self.game.fc.loc[dfd, 'demand']).grid(row=i+2, column=2, padx=10, pady=10)
                range_low = max(int(self.game.fc.loc[dfd, 'demand'] - 2 * self.game.fc.loc[dfd, 'stdev']), 0)
                range_high = max(int(self.game.fc.loc[dfd, 'demand'] + 2 * self.game.fc.loc[dfd, 'stdev']), 0)
                tk.Label(self.fc_value_frame, text=f'{range_low}...{range_high}').grid(row=i+2, column=3, padx=10, pady=10)

        # create and place blank row between values and total
        tk.Label(self.fc_value_frame, text='     ').grid(row=i+3, column=0, padx=10)
        tk.Label(self.fc_value_frame, text='     ').grid(row=i+3, column=1, padx=10, pady=10)
        if self.game.easy_mode:
            tk.Label(self.fc_value_frame, text='     ').grid(row=i+3, column=2, padx=10, pady=10)
        else:
            tk.Label(self.fc_value_frame, text='     ').grid(row=i+3, column=2, padx=10, pady=10)
            tk.Label(self.fc_value_frame, text='     ').grid(row=i+3, column=3, padx=10, pady=10)

        # create and place demand total labels
        tk.Label(self.fc_value_frame, text='Remaining demand:', font=self.label_font).grid(row=i+4, column=0, pady=10, columnspan=2)
        tk.Label(self.fc_value_frame, text=self.game.fc['demand'].sum()).grid(row=i+4, column=2, padx=10, pady=10)

        self.change_bg_to_white(self.fc_frame)
        self.change_bg_to_white(self.fc_value_frame)


    def build_overbook_frame(self):
        self.ob_frame = tk.Frame(self.right_frame)
        self.ob_frame.grid(row=0, column=0, sticky='N S E W')
        self.ob_frame.rowconfigure((0,1,2), weight=1)
        self.ob_frame.columnconfigure((0,1,2), weight=1)

        ob_msg = f'We know that, on average, {int(self.game.ns_rate * 100)}% of customers will not show up for the flight, so we might overbook. How many seats would you like to overbook by?'
        
        self.ob_label = tk.Label(self.ob_frame, text=ob_msg, wraplengt=300)
        self.ob_label.grid(row=0, column=0, padx=5, pady=10)

        self.ob_value = tk.StringVar()
        self.ob_entry = tk.Entry(self.ob_frame, width=10, textvariable=self.ob_value)
        self.ob_entry.grid(row=0, column=1, padx=5, pady=10)
        self.ob_entry_funcid = self.ob_entry.bind('<Return>', self.validate_overbooking)
        self.ob_entry.focus_set()

        self.check_image = ImageTk.PhotoImage(Image.open('images/check.png').resize((40,40), resample=5))
        self.check_button = tk.Button(self.ob_frame, image=self.check_image)
        self.check_button.image = self.check_image
        self.check_button.grid(row=0, column=2, padx=5, pady=10)
        self.check_button_funcid =self.check_button.bind('<Button-1>', self.validate_overbooking)

        self.change_bg_to_white(self.ob_frame)


    def validate_overbooking(self, event=None):
        try:
            self.game.over_au = int(self.ob_value.get())
        except ValueError:
            tk.messagebox.showerror(title='Error', message=f'Oberbooking value must be an integer >= 0.')
        
        if self.game.over_au >= 0:
            self.apply_overbooking()
        else:
            tk.messagebox.showerror(title='Error', message=f'Oberbooking value must be an integer >= 0.')


    def apply_overbooking(self, event=None):
        self.game.au = self.game.ac + self.game.over_au
        self.game.sa = self.game.au
        self.skip_ob = True

        # logger.info(f'OB: {self.game.over_au}')
        self.log_ob_entry()
        self.log_current_stats(incl_fc=False)

        self.ob_entry.unbind('<Return>', self.ob_entry_funcid)
        self.ob_entry['state'] = 'disabled'
        self.check_button.unbind('Button-1>', self.check_button_funcid)
        self.check_button['state'] = 'disabled'
        
        self.new_au_label = tk.Label(self.ob_frame, 
            text=f'OK. You\'ll sell up to {self.game.au} seats. At the end, we\'ll see how many people no-show.', padx=5, pady=5, bg='lightblue', wraplengt=300)
        self.new_au_label.grid(row=1, column=0, columnspan=3, padx=5, pady=10, sticky='E W')

        self.next_image = ImageTk.PhotoImage(Image.open('images/next.png').resize((80,80), resample=5))

        next_button_text = 'Start selling'
    
        self.next_image_button = tk.Button(self.ob_frame, text=next_button_text, image=self.next_image, compound='top', height=120, width=120, 
                bg='white', command=self.confirm_overbooking)

        self.next_image_button.image = self.next_image
        self.next_image_button.grid(row=2, column=0, columnspan=3, pady=10)
        self.next_image_button.focus_set()


    def confirm_overbooking(self):
        self.main.destroy()
        self.build_game()


    def build_reserve_frame(self):
        self.rsv_frame = tk.Frame(self.right_frame)
        self.rsv_frame.grid(row=0, column=0, sticky='N S E W')
        self.rsv_frame.rowconfigure((0,1,2,3), weight=1)
        self.rsv_frame.columnconfigure((0,1,2), weight=1)

        if self.game.curr_dfd > 0:
            rsv_msg = f'How many seats would you like to reserve today at ${self.game.fc.loc[self.game.curr_dfd, "fare"]}?'
        else:
            rsv_msg = f'The flight departs today, so you should reserve all remaining seats at ${self.game.fc.loc[self.game.curr_dfd, "fare"]}.'

        self.rsv_label = tk.Label(self.rsv_frame, text=rsv_msg, wraplengt=300)
        self.rsv_label.grid(row=0, column=0, padx=5, pady=10)

        self.rsv_value = tk.StringVar()
        self.rsv_entry = tk.Entry(self.rsv_frame, width=10, textvariable=self.rsv_value)
        self.rsv_entry.grid(row=0, column=1, padx=5, pady=10)
        self.rsv_entry_funcid = self.rsv_entry.bind('<Return>', self.validate_reserve)
        self.rsv_entry.focus_set()
        if self.game.curr_dfd == 0:
            self.rsv_entry.insert(0, max(self.game.sa, 0))

        self.check_image = ImageTk.PhotoImage(Image.open('images/check.png').resize((40,40), resample=5))
        self.check_button = tk.Button(self.rsv_frame, image=self.check_image)
        self.check_button.image = self.check_image
        self.check_button.grid(row=0, column=2, padx=5, pady=10)
        self.check_button_funcid =self.check_button.bind('<Button-1>', self.validate_reserve)

        self.change_bg_to_white(self.rsv_frame)


    def validate_reserve(self, event=None):
        try:
            self.dfdsim.rsv = int(self.rsv_value.get())
        except ValueError:
            if self.game.sa > 0:
                tk.messagebox.showerror(title='Error', message=f'Reserve value must be an integer between 0 and {self.game.sa}.')
            else:
                tk.messagebox.showerror(title='Error', message=f'You have already sold the authorized number of seats, so you must reserve 0 seats.')

        if (self.game.sa > 0):
            if (self.dfdsim.rsv >= 0) and (self.dfdsim.rsv <= self.game.sa):
                self.run_dfd()
            else:
                tk.messagebox.showerror(title='Error', message=f'Reserve value must be an integer between 0 and {self.game.sa}.')    
        else:
            if self.dfdsim.rsv == 0:
                self.run_dfd()
            else:
                tk.messagebox.showerror(title='Error', message=f'You have already sold the authorized number of seats, so you must reserve 0 seats.')


    def run_dfd(self, event=None):
        # self.rsv = int(self.rsv_entry.get())

        self.log_rsv_entry()

        self.rsv_entry.unbind('<Return>', self.rsv_entry_funcid)
        self.rsv_entry['state'] = 'disabled'
        self.check_button.unbind('Button-1>', self.check_button_funcid)
        self.check_button['state'] = 'disabled'
        
        self.dfdsim.observe_bookings(self.dfdsim.rsv)
        
        self.log_dfdsim_outcome()

        rsv_s = (lambda x: '' if x == 1 else 's') (self.dfdsim.rsv)
        lb_s = (lambda x: '' if x == 1 else 's') (self.dfdsim.lb)
        lb_people = (lambda x: 'person' if x == 1 else 'people') (self.dfdsim.lb)
        
        self.outcome_label = tk.Label(self.rsv_frame, 
            text=f'{self.dfdsim.arr} {lb_people} wanted to book today, and you reserved {self.dfdsim.rsv} seat{rsv_s}. \nYou sold {self.dfdsim.lb} seat{lb_s} and earned ${self.dfdsim.rev:,}.', 
            padx=5, pady=5, bg='lightblue', wraplengt=300)
        self.outcome_label.grid(row=1, column=0, columnspan=3, padx=5, pady=10, sticky='E W')

        if (not self.game.easy_mode) and self.game.curr_dfd > 0:
            self.forecast_update_label = tk.Label(self.rsv_frame, text='The forecast will update as we go to the next booking day.', 
                padx=5, pady=5, bg='lightblue', wraplengt=300)
            self.forecast_update_label.grid(row=2, column=0, columnspan=3, padx=5, pady=10, sticky='E W')

        self.next_image = ImageTk.PhotoImage(Image.open('images/next.png').resize((80,80), resample=5))

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
        self.next_image_button.grid(row=3, column=0, columnspan=3, pady=10)
        self.next_image_button.focus_set()
        

    def go_to_next_dfd(self):
        # go_to_next_dfd prepares game for next dfd by:
        # deleting the past dfd row from the forecast
        # selecting a random event and applying it
        # displaying a message about the event
        # redistributing probabilities if an event was selected

        self.dfdsim.dfd_cleanup()
        
        self.log_dfd_header()
        if not self.game.easy_mode:
            self.log_event()
        self.log_current_stats()

        if not self.game.easy_mode:
            if self.dfdsim.dfd_event:
                self.display_event_message()
        self.main.destroy()
        self.build_game()


    def display_event_message(self):
        self.event_box = tk.Toplevel(padx=10, pady=10)
        self.event_box.focus_set()  # focus_set places focus on new top window
        self.event_box.grab_set()  # grab_set disallows activity in the bottom window

        self.event_image_path = self.dfdsim.dfd_event.image_path
        self.event_image = ImageTk.PhotoImage(Image.open(self.event_image_path).resize((80,80), resample=5))
        self.event_image_label = tk.Label(self.event_box, image=self.event_image)
        self.event_image_label.image = self.event_image
        self.event_image_label.grid(row=0, column=0, rowspan=3, padx=20, pady=20)
        
        self.event_box_title = tk.Label(self.event_box, text=self.dfdsim.dfd_event.name, font=self.label_font, padx=10, pady=10)
        self.event_box_message = tk.Label(self.event_box, text=self.dfdsim.dfd_event.message, font=self.default_font, wraplengt=300, padx=10, pady=10)
        self.ok_button = tk.Button(self.event_box, text='OK', command=self.dismiss_event_message, padx=10,  pady=5)

        self.event_box_title.grid(row=0, column=1)
        self.event_box_message.grid(row=1, column=1)
        self.ok_button.grid(row=2, column=1)

        self.ok_button.focus_set()


    def dismiss_event_message(self):
        self.event_box.grab_release()
        self.event_box.destroy()


    def build_departure_frame(self):
        self.dfdsim.dfd_cleanup()

        self.build_stats_frame(which='game')

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

        self.log_ns_db()

        self.dep_image_path = 'images/departure.png'
        self.dep_image = ImageTk.PhotoImage(Image.open(self.dep_image_path).resize((120,120), resample=5))
        self.dep_image_label = tk.Label(self.dep_frame, image=self.dep_image, bg='white')
        self.dep_image_label.image = self.dep_image
        self.dep_image_label.grid(row=0, column=0, pady=10, sticky='N S E W')

        noshow_people = (lambda x: 'person' if x == 1 else 'people') (self.game.noshows)
        db_people = (lambda x: 'person' if x == 1 else 'people') (self.game.dbs)
        dep_msg = f'At departure, {self.game.noshows} {noshow_people} no-showed, so there are {self.game.total_lb} people for {self.game.ac} seats.'
        if self.game.dbs > 0:
            dep_msg += f'\n\nYou\'ll need to offer DB compensation to {self.game.dbs} {db_people}.'
        else:
            dep_msg += '\n\nNo need for volunteers.'
        self.dep_label = tk.Label(self.dep_frame, text=dep_msg, bg='lightblue', wraplengt=300)
        self.dep_label.grid(row=1, column=0, padx=5, pady=10, sticky='N S E W')

        if self.game.dbs > 0:
            next_text = 'Compensate DBs'
            next_command = self.compensate_dbs
        else:
            next_text = 'See results'
            next_command = self.end_game
        self.next_image_button = tk.Button(self.dep_frame, text=next_text, image=self.next_image, compound='top', height=120, width=120, 
                bg='white', command=next_command)
        self.next_image_button.image = self.next_image
        self.next_image_button.grid(row=2, column=0, columnspan=2, pady=10)
        self.next_image_button.focus_set()

        self.change_bg_to_white(self.left_frame)
        self.change_bg_to_white(self.right_frame)
        self.change_bg_to_white(self.stats_frame)


    def compensate_dbs(self):
        self.game.db_cost = self.game.compensate_dbs()
        self.game.total_db_cost = self.game.db_cost * self.game.dbs
        self.game.total_rev -= self.game.total_db_cost

        self.log_db_cost()
        self.log_current_stats()

        if self.game.db_cost <= 250:
            self.db_comp_msg = f'You got lucky. There were plenty of other options, and you only paid ${self.game.db_cost:,} per denied boarding.'
        elif self.game.db_cost <= 1000:
            self.db_comp_msg = f'There were limited alternative flights, and you paid ${self.game.db_cost:,} per denied boarding.'
        else:
            self.db_comp_msg = f'Ouch! No one was flexible with their travel plans, and you had to pay ${self.game.db_cost:,} per denied boarding.'
        
        self.dep_label.destroy()
        
        self.db_outcome_label = tk.Label(self.dep_frame, text=self.db_comp_msg, padx=5, pady=5, bg='lightblue', wraplengt=300)
        self.db_outcome_label.grid(row=1, column=0, padx=5, pady=10, sticky='N S E W')

        self.next_image_button.destroy()

        self.next_image_button = tk.Button(self.dep_frame, text='See results', image=self.next_image, compound='top', height=120, width=120, 
                bg='white', command=self.end_game)
        self.next_image_button.image = self.next_image
        self.next_image_button.grid(row=2, column=0, pady=10)
        self.next_image_button.focus_set()

        self.dep_frame.columnconfigure(0, weight=1)


    def end_game(self):
        logger.info('---------- Game end ----------')
        logger.info('******************************')

        self.add_results_to_db()
        self.build_end()


    def add_results_to_db(self):
        result = (self.player_name_value.get(),
            self.player_loc_value.get(),
            self.game.game_type,
            self.game.total_rev,
            datetime.now().isoformat()
            )
        self.game_db.insert_results(result)


    def build_end(self):
        if self.game.easy_mode:
            self.dfdsim.dfd_cleanup()
            self.middle_frame.destroy()
        self.build_stats_frame('end')

        self.leaderboard_outer_frame = tk.Frame(self.right_frame)
        self.leaderboard_outer_frame.grid(row=0, column=0, sticky='N S E W', pady=10)
        self.leaderboard_outer_frame.columnconfigure((0,1), weight=1)
        self.build_end_leaderboard_frame(which='today')
        self.build_end_leaderboard_frame(which='all')


    def build_game_option_frame(self):    
        self.return_to_home_button = tk.Button(self.game_option_frame, text='Main menu', fg='#0033A0', command=self.return_to_home)
        self.return_to_home_button.grid(row=0, column=0)

        self.change_bg_to_white(self.game_option_frame)


    def return_to_home(self):
        if self.game.curr_dfd >= 0:
            go_home = tk.messagebox.askyesno('Main menu?', 'Return to the main menu? Your progress will be lost.')
            if go_home:
                logger.info('------- Quitting game --------')
                logger.info('')
                logger.info('******************************')
                self.main.destroy()
                self.build_home()
        else:
            self.main.destroy()
            self.build_home()


    ### LEADERBOARD


    def build_home_leaderboard_frame(self, when):
        self.leaderboard_frame = tk.Frame(self.home, relief='groove', borderwidth=5, bg='white', padx=10, pady=10)
        self.leaderboard_frame.grid(row=0, column=1, sticky='N S E W')
        if when == 'today':
            self.results_df = self.game_db.get_todays_results()
        elif when == 'all':
            self.results_df = self.game_db.get_all_results()

        self.leaderboard_frame.rowconfigure((1,2,3), weight=1)
        self.leaderboard_frame.columnconfigure((0,1), weight=1)

        if when =='today':
            self.lb_header = tk.Label(self.leaderboard_frame, text='Today\'s leaderboard', font=self.header_font)
        elif when =='all':
            self.lb_header = tk.Label(self.leaderboard_frame, text='All-time leaderboard', font=self.header_font)
        self.lb_header.grid(row=0, column=0, columnspan=2, padx=5)

        self.lb1_frame = tk.Frame(self.leaderboard_frame)
        self.lb1_frame.grid(row=1, column=0, padx=5, pady=5, sticky='N S E W')
        self.lb2_frame = tk.Frame(self.leaderboard_frame)
        self.lb2_frame.grid(row=1, column=1, padx=5, pady=5, sticky='N S E W')
        self.lb3_frame = tk.Frame(self.leaderboard_frame)
        self.lb3_frame.grid(row=2, column=0, padx=5, pady=5, sticky='N S E W')
        self.lb4_frame = tk.Frame(self.leaderboard_frame)
        self.lb4_frame.grid(row=2, column=1, padx=5, pady=5, sticky='N S E W')
        self.lb5_frame = tk.Frame(self.leaderboard_frame)
        self.lb5_frame.grid(row=3, column=0, padx=5, pady=5, sticky='N S E W')
        self.lb6_frame = tk.Frame(self.leaderboard_frame)
        self.lb6_frame.grid(row=3, column=1, padx=5, pady=5, sticky='N S E W')

        frames = [self.lb1_frame, self.lb2_frame, self.lb3_frame, self.lb4_frame, self.lb5_frame, self.lb6_frame]

        for i, frame in enumerate(frames):
            frame.rowconfigure((1,2,3), weight=1)
            frame.columnconfigure((0,1,2,3), weight=1)
            tk.Label(frame, text='Name', font=self.label_font).grid(row=0, column=0, padx=5, pady=10, sticky='N')
            tk.Label(frame, text='From', font=self.label_font).grid(row=0, column=1, padx=5, pady=10, sticky='N')
            tk.Label(frame, text='Game', font=self.label_font).grid(row=0, column=2, padx=5, pady=10, sticky='N')
            tk.Label(frame, text='Revenue', font=self.label_font).grid(row=0, column=3, padx=5, pady=10, sticky='N')

            these_results = self.results_df[self.results_df['game'] == scenario_dict[i+1]['name']]

            for j in range(min(3, len(these_results))):
                tk.Label(frame, text=these_results.iloc[j, 1]).grid(row=j+1, column=0, padx=5, pady=5)
                tk.Label(frame, text=these_results.iloc[j, 2]).grid(row=j+1, column=1, padx=5, pady=5)
                lb_image_path = scenario_dict[i+1]['image']
                lb_image = ImageTk.PhotoImage(Image.open(lb_image_path).resize((25,25), resample=5))
                lb_image_label = tk.Label(frame, image=lb_image)
                lb_image_label.image = lb_image
                lb_image_label.grid(row=j+1, column=2, padx=5, pady=5)
                tk.Label(frame, text=f"${these_results.iloc[j, 4]:,}").grid(row=j+1, column=3, padx=5, pady=5)

            self.change_bg_to_white(frame)

        self.change_bg_to_white(self.leaderboard_frame)


    def build_end_leaderboard_frame(self, which):
        if which == 'today':
            self.leaderboard_frame = tk.Frame(self.leaderboard_outer_frame, bg='white', padx=10, pady=10)
            self.leaderboard_frame.grid(row=0, column=0, sticky='N E W')
            self.results_df = self.game_db.get_some_of_todays_results(which_game=self.game.game_type)
            self.lb_header = tk.Label(self.leaderboard_frame, text='Today\'s leaderboard', font=self.header_font)
        elif which == 'all':
            self.leaderboard_frame = tk.Frame(self.leaderboard_outer_frame, bg='white', padx=10, pady=10)
            self.leaderboard_frame.grid(row=0, column=1, sticky='N E W')
            self.results_df = self.game_db.get_some_results(which_game=self.game.game_type)
            self.lb_header = tk.Label(self.leaderboard_frame, text='All-time leaderboard', font=self.header_font)

        self.leaderboard_frame.rowconfigure(1, weight=1)
        self.leaderboard_frame.columnconfigure((0,1), weight=1)

        self.lb_header.grid(row=0, column=0, padx=5)

        self.lb_value_frame = tk.Frame(self.leaderboard_frame)
        self.lb_value_frame.grid(row=1, column=0)

        self.lb_label_1 = tk.Label(self.lb_value_frame, text='Name', font=self.label_font)
        self.lb_label_2 = tk.Label(self.lb_value_frame, text='From', font=self.label_font)
        self.lb_label_3 = tk.Label(self.lb_value_frame, text='Game', font=self.label_font)
        self.lb_label_4 = tk.Label(self.lb_value_frame, text='Revenue', font=self.label_font)

        self.lb_label_1.grid(row=0, column=0, padx=5, pady=10)  # name
        self.lb_label_2.grid(row=0, column=1, padx=5, pady=10)  # from
        self.lb_label_3.grid(row=0, column=2, padx=5, pady=10)  # game
        self.lb_label_4.grid(row=0, column=3, padx=5, pady=10)  # revenue

        player_on_leaderboard = False

        def add_this_player():
            tk.Label(self.lb_value_frame, text=self.game.player, fg='#0033A0', font=self.label_font).grid(row=i+1, column=0, padx=5, pady=5)
            tk.Label(self.lb_value_frame, text=self.game.location, fg='#0033A0', font=self.label_font).grid(row=i+1, column=1, padx=5, pady=5)
            lb_image_path = self.game.game_image_path
            lb_image = ImageTk.PhotoImage(Image.open(lb_image_path).resize((25,25), resample=5))
            lb_image_label = tk.Label(self.lb_value_frame, image=lb_image)
            lb_image_label.image = lb_image
            lb_image_label.grid(row=i+1, column=2, padx=5, pady=5)
            tk.Label(self.lb_value_frame, text=f'${self.game.total_rev:,}', fg='#0033A0').grid(row=i+1, column=3, padx=5, pady=5)

        i = 0
        for i in range(min(10, len(self.results_df))):
            if (self.results_df.loc[i, 'revenue'] > self.game.total_rev) or player_on_leaderboard:
                tk.Label(self.lb_value_frame, text=self.results_df.loc[i, 'name']).grid(row=i+1, column=0, padx=5, pady=5)
                
                tk.Label(self.lb_value_frame, text=self.results_df.loc[i, 'location']).grid(row=i+1, column=1, padx=5, pady=5)
                
                lb_image_path = self.game.game_image_path
                lb_image = ImageTk.PhotoImage(Image.open(lb_image_path).resize((25,25), resample=5))
                lb_image_label = tk.Label(self.lb_value_frame, image=lb_image)
                lb_image_label.image = lb_image
                lb_image_label.grid(row=i+1, column=2, padx=5, pady=5)

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

        self.change_bg_to_white(self.right_frame)
        self.change_bg_to_white(self.leaderboard_outer_frame)
        self.change_bg_to_white(self.leaderboard_frame)
        self.change_bg_to_white(self.lb_value_frame)


    def build_home_leaderboard(self):
        self.player_frame.destroy()
        self.button_frame.destroy()
        self.build_home_leaderboard_frame(when='all')
        self.build_leaderboard_option_frame()


    def build_leaderboard_option_frame(self):
        self.home_option_frame.destroy()

        self.leaderboard_option_frame = tk.Frame(self.home, relief='groove', borderwidth=5, bg='white')
        self.leaderboard_option_frame.grid(row=2, column=1, pady=(20, 0), sticky='S E')
        self.leaderboard_option_frame.rowconfigure(0, weight=1)
        self.leaderboard_option_frame.columnconfigure(0, weight=1)

        self.all_leaders_button = tk.Button(self.leaderboard_option_frame, text='All-time leaders', fg='#0033A0', command=self.switch_leaderboard_to_all)
        self.all_leaders_button.grid(row=0, column=0, padx=10, pady=10)

        self.todays_leaders_button = tk.Button(self.leaderboard_option_frame, text='Today\'s leaders', fg='#0033A0', command=self.switch_leaderboard_to_today)
        self.todays_leaders_button.grid(row=0, column=1, padx=10, pady=10)

        self.main_menu_button = tk.Button(self.leaderboard_option_frame, text='Main menu', fg='#0033A0', command=self.rebuild_home_from_home)
        self.main_menu_button.grid(row=0, column=2, padx=10, pady=10)


    def switch_leaderboard_to_all(self):
        self.leaderboard_frame.destroy()
        self.build_home_leaderboard_frame(when='all')


    def switch_leaderboard_to_today(self):
        self.leaderboard_frame.destroy()
        self.build_home_leaderboard_frame(when='today')


    def reset_leaderboard(self):
        self.confirm_reset_leaderboard = tk.messagebox.askyesno('Reset leaderboard?', 'Reset leaderboard? This will delete all results.')
        if self.confirm_reset_leaderboard:
            self.game_db.drop_results()


    ### UTILITIES

    def change_bg_to_white(self, parent):
        for widget in parent.winfo_children():
            widget.configure(bg='white')


    def change_bg_to_lightblue(self, parent):
        for widget in parent.winfo_children():
            widget.configure(bg='lightblue')


    def log_dfd_header(self):
        logger.info(f'---------- DFD {self.game.curr_dfd} ----------')

    def log_current_stats(self, incl_fc=True):
        logger.info(f'AC: {self.game.ac}, AU: {self.game.au}, LB: {self.game.total_lb}, SA: {self.game.sa}, Rev: {self.game.total_rev}')
        if incl_fc:
            logger.info(f'Fare: {self.game.fc["fare"].to_dict()}')
            logger.info(f'Demand: {self.game.fc["demand"].to_dict()}')
            logger.info(f'CV: {self.game.fc["cv"].to_dict()}')
            logger.info(f'Stdev: {self.game.fc["stdev"].to_dict()}')

    def log_ob_entry(self):
        logger.info(f'OB: {self.game.over_au}')

    def log_rsv_entry(self):
        logger.info(f'RSV: {self.dfdsim.rsv}')

    def log_dfdsim_outcome(self):
        logger.info(f'Arr: {self.dfdsim.arr}, LB+: {self.dfdsim.lb}, Rev+: {self.dfdsim.rev}')
    
    def log_event(self):
        if self.dfdsim.dfd_event:
            logger.info(f'Event: {self.dfdsim.dfd_event.name}')
        else:
            logger.info('No event')

    def log_ns_db(self):
        logger.info(f'NS: {self.game.noshows}, DB: {self.game.dbs}')

    def log_db_cost(self):
        logger.info(f'DB cost: {self.game.db_cost}')