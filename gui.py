import random
import tkinter as tk
from datetime import datetime
from tkinter import messagebox
from tkinter.font import Font, nametofont

import pandas as pd
from PIL import Image, ImageTk

from data import *
from db import create_connection, db_file, insert_results
from game import DFDSimulation, EasyGame, RealGame


class GUI():
    
    def __init__(self, root):
        self.root = root

        self.root.title('The PRM Game')
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        self.default_font = nametofont('TkDefaultFont')
        self.default_font.configure(family='Helvetica', size='14')

        self.entry_font = nametofont('TkTextFont')
        self.entry_font.configure(family='Helvetica', size='14')

        self.build_home()

    
    ### HOME PAGE ###


    def build_home(self):
        # create the main container
        self.home = tk.Frame(self.root, padx=100, pady=100, relief='sunken', borderwidth=5)
        self.home.grid(column=0, row=0)

        # create widgets

        ### logo
        self.logo_path = 'images/airplane_title.png'
        self.logo_img = ImageTk.PhotoImage(Image.open(self.logo_path))
        self.logo = tk.Label(self.home, image=self.logo_img)

        ### sign-in fields
        self.player_name_label = tk.Label(self.home, text='What\'s your name?')
        self.player_name_value = tk.StringVar()
        self.player_name = tk.Entry(self.home, textvariable=self.player_name_value)

        self.player_loc_label = tk.Label(self.home, text='Where are you from?')
        self.player_loc_value = tk.StringVar()
        self.player_loc = tk.Entry(self.home, textvariable=self.player_loc_value)

        ### buttons
        self.easy_button_path = 'images/100.png'
        self.easy_button_image = ImageTk.PhotoImage(Image.open(self.easy_button_path))
        self.easy_button = tk.Button(self.home, text='Play easy mode', image=self.easy_button_image, compound='top', height=160, width=240, bg='white', 
            command=self.play_easy_mode)

        self.real_button_choices = ['man','woman','person']
        self.real_button_path = 'images/' + random.choice(self.real_button_choices) + '_shrugging.png'
        self.real_button_image = ImageTk.PhotoImage(Image.open(self.real_button_path))
        self.real_button = tk.Button(self.home, text='Play real life mode', image=self.real_button_image, compound='top', height=160, width=240, bg='white', 
            command=self.play_real_mode)

        # place widgets

        ### logo
        self.logo.grid(row=0, column=0, rowspan=4)

        ### sign-in fields
        # TODO: validate that user fields are filled in before selecting game
        self.player_name_label.grid(row=1, column=1, padx=20, pady=0, sticky='W')
        self.player_name.grid(row=1, column=2)

        self.player_loc_label.grid(row=2, column=1, padx=20, pady=(10, 40), sticky='W')
        self.player_loc.grid(row=2, column=2, pady=(10, 40))

        ### buttons
        self.easy_button.grid(row=3, column=1, padx=20, pady=20)
        self.real_button.grid(row=3, column=2, padx=20, pady=20)


    def play_easy_mode(self):
        self.home.destroy()
        self.game = EasyGame(DFLT_DFD, DFLT_FCDATA, DFLT_AC)
        self.game.set_player_info(self.player_name_value.get(), self.player_loc_value.get())
        self.build_game()


    def play_real_mode(self):
        pass


    ### GAME PAGE ###


    def build_game(self):
        ### MAIN CONTAINERS
        
        self.main = tk.Frame(self.root, padx=30, pady=30, relief='sunken', borderwidth=5)
        self.main.grid(column=0, row=0)

        self.stats_frame = tk.Frame(self.main, padx=20, pady=20, relief='groove', borderwidth=5, bg='white')
        self.stats_frame.grid(row=0, column=0, padx=10, sticky='N S W')

        self.fc_frame = tk.Frame(self.main, padx=20, pady=20, relief='groove', borderwidth=5, bg='white')
        self.fc_frame.grid(row=0, column=1, padx=10, sticky='N S')

        self.action_frame = tk.Frame(self.main, padx=20, pady=20, relief='groove', borderwidth=5, bg='white')
        self.action_frame.grid(row=0, column=2, padx=10, sticky='N S E')

        self.option_frame = tk.Frame(self.main, padx=10, pady=20, relief='groove', borderwidth=5, bg='white')
        self.option_frame.grid(row=1, column=2, padx=10, pady=(50, 0), sticky='S E')

        self.display_stats_frame()
        self.display_forecast_frame()
        self.display_action_frame()
        self.display_option_frame()

        self.dfdsim = DFDSimulation(self.game, self.game.curr_dfd)


    def display_stats_frame(self):        
        # create widgets
        self.intro_message = tk.Label(self.stats_frame, text=self.game.game_type)

        if self.game.curr_dfd >= 0:
            self.date_label = tk.Label(self.stats_frame, text=f'Today is {self.game.curr_dow_long}, and\nthe flight departs on Friday.')
            self.sa_label = tk.Label(self.stats_frame, text=f'There are {self.game.sa} seats remaining.')
            self.rev_label = tk.Label(self.stats_frame, text=f'So far, you\'ve earned\n${self.game.totalrev:,}.')
        else:
            self.date_label = tk.Label(self.stats_frame, text=f'The flight has departed!')
            self.sa_label = tk.Label(self.stats_frame, text=f'Your load factor is {int(100 * (1 - self.game.sa / self.game.AC))}%.')
            self.rev_label = tk.Label(self.stats_frame, text=f'You earned a total of ${self.game.totalrev:,}.')

        self.date_image = ImageTk.PhotoImage(Image.open('images/calendar.png'))
        self.date_image_label = tk.Label(self.stats_frame, image=self.date_image)
        self.date_image_label.image = self.date_image

        self.seat_image = ImageTk.PhotoImage(Image.open('images/seat.png'))
        self.seat_image_label = tk.Label(self.stats_frame, image=self.seat_image)
        self.seat_image_label.image = self.seat_image
        
        self.money_image = ImageTk.PhotoImage(Image.open('images/money.png'))
        self.money_image_label = tk.Label(self.stats_frame, image=self.money_image)
        self.money_image_label.image = self.money_image

        # place widgets
        self.intro_message.grid(row=0, column=0, pady=(5, 10), sticky = 'N S W')

        self.date_image_label.grid(row=1, column=0, padx=10, pady=10, sticky = 'N S')
        self.date_label.grid(row=1, column=1, padx=5, pady=10, sticky = 'N S')
        
        self.seat_image_label.grid(row=2, column=0, padx=10, pady=10, sticky = 'N S')
        self.sa_label.grid(row=2, column=1, padx=5, pady=10, sticky = 'N S')
        
        self.money_image_label.grid(row=3, column=0, padx=10, pady=10, sticky = 'N S')
        self.rev_label.grid(row=3, column=1, padx=5, pady=(10, 0), sticky = 'N S')

        self.change_bg_to_white(self.stats_frame)
        self.intro_message.configure(bg='lightblue')


    def display_forecast_frame(self):
        # create widgets for headers
        self.fc_label = tk.Label(self.fc_frame, text='--- FORECAST ---')
        self.fc_label_1 = tk.Label(self.fc_frame, text='Book day')
        self.fc_label_2 = tk.Label(self.fc_frame, text='Fare')
        self.fc_label_3 = tk.Label(self.fc_frame, text='Demand')

        # place widgets for headers
        self.fc_label.grid(row=0, column=0, padx=5, pady=10, columnspan=3)
        self.fc_label_1.grid(row=1, column=0, padx=(0, 5), pady=10)  # DOW
        self.fc_label_2.grid(row=1, column=1, padx=10, pady=10)  # fare
        self.fc_label_3.grid(row=1, column=2, padx=(5, 0), pady=10)  # demand

        # create and place forecast values
        for i, dfd in enumerate(range(self.game.curr_dfd, -1, -1)):
            tk.Label(self.fc_frame, text=self.game.fc.loc[dfd, 'dow_short']).grid(row=i+2, column=0, padx=(0, 5))
            tk.Label(self.fc_frame, text=self.game.fc.loc[dfd, 'fare']).grid(row=i+2, column=1, padx=10, pady=10)
            tk.Label(self.fc_frame, text=self.game.fc.loc[dfd, 'demand']).grid(row=i+2, column=2, padx=(5, 0), pady=10)

        self.change_bg_to_white(self.fc_frame)


    def display_action_frame(self):
        if self.game.curr_dfd > 0:
            rsv_msg = f'How many seats would you \nlike to reserve today at ${self.game.fc.loc[self.game.curr_dfd, "fare"]}?'
        else:
            rsv_msg = f'The flight departs today, so you should \nreserve all remaining seats at ${self.game.fc.loc[self.game.curr_dfd, "fare"]}.'

        self.rsv_label = tk.Label(self.action_frame, text=rsv_msg)
        self.rsv_value = tk.StringVar()
        self.rsv_entry = tk.Entry(self.action_frame, width=10, textvariable=self.rsv_value)

        if self.game.curr_dfd == 0:
            self.rsv_entry.insert(0, self.game.sa)

        self.check_image = ImageTk.PhotoImage(Image.open('images/check.png'))
        self.check_button = tk.Button(self.action_frame, image=self.check_image)
        self.check_button.image = self.check_image

        self.rsv_label.grid(row=1, column=0, padx=5, pady=10)
        self.rsv_entry.grid(row=1, column=1, padx=5, pady=10)
        self.check_button.grid(row=1, column=2, padx=5, pady=10)

        # store entered value as self.rsv upon Enter or mouse click and then simulated the dfd
        self.rsv_entry_funcid = self.rsv_entry.bind('<Return>', self.run_dfd)
        self.check_button_funcid =self.check_button.bind('<Button-1>', self.run_dfd)

        self.change_bg_to_white(self.action_frame)


    def display_option_frame(self):
        if self.game.curr_dfd >= 0:
            self.quit_button = tk.Button(self.option_frame, text='Quit game', fg='red', command=self.quit_game)
            self.quit_button.grid(row=0, column=0)
        else:
            self.return_to_home_button = tk.Button(self.option_frame, text='Main menu', fg='red', command=self.return_to_home)
            self.return_to_home_button.grid(row=0, column=0)

        self.change_bg_to_white(self.option_frame)


    def quit_game(self):
        quit = tk.messagebox.askyesno('Quit?', 'Do you really want to quit the game?')
        if quit:
            self.main.destroy()
            self.build_home()


    def return_to_home(self):
        go_home = tk.messagebox.askyesno('Main menu?', 'Ready to go back to the main menu?')
        if go_home:
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
        
        self.outcome_label = tk.Label(self.action_frame, 
            text=f'{self.dfdsim.arr} people showed up to book today, \nand you reserved {self.rsv} seat{rsv_s}. \
        \n\nYou sold {self.dfdsim.lb} seat{lb_s} and earned ${self.dfdsim.rev:,}.', padx=5, pady=5, bg='lightblue')
        self.outcome_label.grid(row=2, column=0, columnspan=3, padx=5, pady=10)

        # if dfd > 0, go to next dfd
        self.next_image = ImageTk.PhotoImage(Image.open('images/next.png'))

        if self.game.curr_dfd > 0:
            next_button_text = 'Next day'
            next_command = self.go_to_next_dfd
        else:
            next_button_text = 'See results'
            next_command = self.end_game
        
        self.next_image_button = tk.Button(self.action_frame, text=next_button_text, image=self.next_image, compound='top', height=120, width=120, 
                bg='white', command=next_command)

        self.next_image_button.image = self.next_image
        self.next_image_button.grid(row=3, column=0, columnspan=3, sticky='S', pady=(20, 0))
        

    def go_to_next_dfd(self):
        self.dfdsim.dfd_cleanup()
        self.main.destroy()
        self.build_game()


    def end_game(self):
        self.dfdsim.dfd_cleanup()
        self.main.destroy()
        self.add_results_to_db()
        self.build_end()


    def add_results_to_db(self):
        result = (self.player_name_value.get(),
            self.player_loc_value.get(),
            self.game.game_type,
            self.game.totalrev,
            datetime.now().isoformat()
            )
        conn = create_connection(db_file)
        insert_results(conn, result)
        conn.close()


    ### END PAGE ###


    def build_end(self):
        self.main = tk.Frame(self.root, padx=50, pady=50, relief='sunken', borderwidth=5)
        self.main.grid(column=0, row=0)

        self.stats_frame = tk.Frame(self.main, padx=50, pady=20, relief='groove', borderwidth=5, bg='white')
        self.stats_frame.grid(row=0, column=0, padx=10, sticky='N S W')

        self.lb_frame = tk.Frame(self.main, padx=50, pady=20, relief='groove', borderwidth=5, bg='white')
        self.lb_frame.grid(row=0, column=1, padx=10, sticky='N S E')

        self.option_frame = tk.Frame(self.main, padx=10, pady=20, relief='groove', borderwidth=5, bg='white')
        self.option_frame.grid(row=1, column=2, padx=10, pady=(50, 0), sticky='S E')

        self.display_stats_frame()
        self.display_leaderboard_frame()
        self.display_option_frame()


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


    def display_leaderboard_frame(self):
        self.results_df = self.get_results()

        # create widgets for headers
        self.lb_label = tk.Label(self.lb_frame, text='--- LEADERBOARD ---')
        self.lb_label_1 = tk.Label(self.lb_frame, text='Name')
        self.lb_label_2 = tk.Label(self.lb_frame, text='From')
        self.lb_label_3 = tk.Label(self.lb_frame, text='Game')
        self.lb_label_4 = tk.Label(self.lb_frame, text='Revenue')

        # place widgets for headers
        self.lb_label.grid(row=0, column=0, padx=5, pady=10, columnspan=4)
        self.lb_label_1.grid(row=1, column=0, padx=5, pady=10)  # name
        self.lb_label_2.grid(row=1, column=1, padx=5, pady=10)  # from
        self.lb_label_3.grid(row=1, column=2, padx=5, pady=10)  # game
        self.lb_label_4.grid(row=1, column=3, padx=5, pady=10)  # revenue

        # create and place leaderboard values
        player_on_leaderboard = False

        def add_this_player():
            tk.Label(self.lb_frame, text=self.game.player).grid(row=i+2, column=0, padx=5, pady=10)
            tk.Label(self.lb_frame, text=self.game.location).grid(row=i+2, column=1, padx=5, pady=10)
            tk.Label(self.lb_frame, text=self.game.game_type).grid(row=i+2, column=2, padx=5, pady=10)
            tk.Label(self.lb_frame, text=f'${self.game.totalrev:,}').grid(row=i+2, column=3, padx=5, pady=10)

        for i in range(5):
            if (self.results_df.loc[i, 'revenue'] > self.game.totalrev) or player_on_leaderboard:
                tk.Label(self.lb_frame, text=self.results_df.loc[i, 'name']).grid(row=i+2, column=0, padx=5, pady=10)
                tk.Label(self.lb_frame, text=self.results_df.loc[i, 'location']).grid(row=i+2, column=1, padx=5, pady=10)
                tk.Label(self.lb_frame, text=self.results_df.loc[i, 'game']).grid(row=i+2, column=2, padx=5, pady=10)
                tk.Label(self.lb_frame, text=f'${self.results_df.loc[i, "revenue"]:,}').grid(row=i+2, column=3, padx=5, pady=10)
            else:
                player_on_leaderboard = True
                add_this_player()
        
        if not player_on_leaderboard:
            i += 1
            tk.Label(self.lb_frame, text='-----').grid(row=i+2, column=0, padx=5, pady=10)
            tk.Label(self.lb_frame, text='-----').grid(row=i+2, column=1, padx=5, pady=10)
            tk.Label(self.lb_frame, text='-----').grid(row=i+2, column=2, padx=5, pady=10)
            tk.Label(self.lb_frame, text='-----').grid(row=i+2, column=3, padx=5, pady=10)
            i += 1
            add_this_player()

        self.change_bg_to_white(self.lb_frame)


    ### HELPERS ###

    
    def change_bg_to_white(self, parent):
        for widget in parent.winfo_children():
            widget.configure(bg='white')