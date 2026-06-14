from logging import root
from tkinter import Button, Label, Toplevel
import random
import settings
import ctypes
import sys
from PIL import Image, ImageTk
import os
import subprocess

class Cell:
    all = []
    cell_count= settings.HARD_CELL_COUNT
    cell_count_label_object = None
    timer_label_object = None
    timer_started = False
    start_time = None
    root_window = None
    def __init__(self, x, y, is_mine=False):
        self.is_mine = is_mine
        self.is_opened = False
        self.is_mine_candidate = False
        self.cell_btn_object = None
        self.x = x
        self.y = y

        # Append the object to the Cell.all list
        Cell.all.append(self)

    def Create_btn_object(self, location):
        btn = Button(
            location,
            relief='raised',
            width=12,
            height=4,
            bd=5,
            bg='#9c9c9c'
        )
        btn.bind('<Button-1>', self.left_click_actions) # Left Click
        btn.bind('<Button-3>', self.right_click_actions) # Right Click
        self.cell_btn_object = btn

    @staticmethod    
    def create_cell_count_label(location):
        lbl = Label(
            location,
            bg='black',
            fg='white',
            text=f"{Cell.cell_count}",
            width=12,
            height=4,
            font=("System", 30)
        )
        Cell.cell_count_label_object = lbl

    def left_click_actions(self, event):
        # Check if cell is flagged - if so, prevent left click
        if self.is_mine_candidate:
            return
        
        # Start timer on first click
        if not Cell.timer_started:
            Cell.start_timer()
        
        if self.is_mine:
            self.show_mine()
        else:
            
            if self.surrounded_cell_mines_length == 0:
                for cell_obj in self.surrounded_cell:
                    cell_obj.show_cell()
            self.show_cell()
            # If Mines count is equal to the cells left count player won
            if Cell.cell_count == settings.HMINES_COUNT:
                Cell.stop_timer()
                Cell.show_win_window(Cell.root_window, self.restart_game)
        # Cancel left and right click events if the cell is already opened
        self.cell_btn_object.unbind('<Button-1>')
        self.cell_btn_object.unbind('<Button-3>')


    def get_cell_by_axis(self, x, y):
        # Return a cell object based on the value of x and y
        for cell in Cell.all:
            if cell.x == x and cell.y == y:
                return cell
        return None

    @property
    def surrounded_cell(self):
        cells = [
            self.get_cell_by_axis(self.x - 1, self.y - 1),
            self.get_cell_by_axis(self.x - 1, self.y),
            self.get_cell_by_axis(self.x - 1, self.y + 1),
            self.get_cell_by_axis(self.x, self.y - 1),
            self.get_cell_by_axis(self.x, self.y + 1),
            self.get_cell_by_axis(self.x + 1, self.y - 1),
            self.get_cell_by_axis(self.x + 1, self.y),
            self.get_cell_by_axis(self.x + 1, self.y + 1),
        ]

        return [cell for cell in cells if cell is not None]

    @property
    def surrounded_cell_mines_length(self):
        counter = 0
        for cell in self.surrounded_cell:
            if cell.is_mine:
                counter += 1
        
        return counter

    def show_cell(self):
        if not self.is_opened:
            Cell.cell_count -= 1
            self.cell_btn_object.configure(text=self.surrounded_cell_mines_length, relief="raised")
            # Replace the text of cell count label with the newer count
            if Cell.cell_count_label_object:
                Cell.cell_count_label_object.configure(
                    text=f"{Cell.cell_count}"
            )
        # Change to lighter color and sunken relief when revealed
        self.cell_btn_object.configure(
            bg="#b9b9b9",
            relief='raised'
            )
               
            # Mark the cell as opened
        self.is_opened = True
            

    def show_mine(self):

            # mark clicked mine instantly
            self.cell_btn_object.configure(bg="red", text="💣", relief='sunken')
            
            # Stop timer
            Cell.stop_timer()

            # reveal all mines first (like Windows Minesweeper)
            self.reveal_all_mines()

            # delay before popup (gives "animation feel")
            self.cell_btn_object.after(1500, self.game_over_popup)
        
    def reveal_all_mines(self):

        delay = 0

        for cell in Cell.all:

            if cell.is_mine:
                
                delay += 35

                cell.cell_btn_object.after(
                    delay,
                    lambda c=cell: c.cell_btn_object.configure(
                        bg="red",
                        relief= 'sunken',
                        text="💣"
                    )
                )

           
            
    def game_over_popup(self):
        Cell.show_game_over_window(Cell.root_window, self.restart_game)
         
    def restart_game(self):
        
         # reset state first
        for cell in Cell.all:
            cell.is_mine = False
            cell.is_opened = False
            cell.is_mine_candidate = False

            cell.cell_btn_object.configure(
            text="",
            relief='raised',
            bg="#9c9c9c"
        )

            # re-randomize mines AFTER reset
            Cell.randomize_mines()

            Cell.cell_count = settings.HARD_CELL_COUNT
            Cell.randomize_mines()

        for cell in Cell.all:

            cell.is_opened = False
            cell.is_mine_candidate = False

            cell.cell_btn_object.configure(
                text="",
                relief='raised',
                bg="#9c9c9c"
            )

            cell.cell_btn_object.bind(
                "<Button-1>",
                cell.left_click_actions
            )

            cell.cell_btn_object.bind(
                "<Button-3>",
                cell.right_click_actions
            )

        if  Cell.cell_count_label_object:
            Cell.cell_count_label_object.configure(
                text=f"{Cell.cell_count}"
            )
        
        # Reset timer
        Cell.stop_timer()
        Cell.timer_started = False
        if Cell.timer_label_object:
            Cell.timer_label_object.configure(text="00")
            
            self.game_active = True
            
    def shake_effect(self):

        colors = ["red", "dark red", "red"]

        def shake(i=0):

            if i < len(colors):
               self.cell_btn_object.configure(bg=colors[i])
               self.cell_btn_object.after(80, lambda: shake(i + 1))

        shake()
              
    def right_click_actions(self, event):
       
        if not self.is_opened:

            if not self.is_mine_candidate:
                # Flag the cell - disable left click
                self.cell_btn_object.configure(
                    text="🚩",
                    fg="red",
                )
                self.is_mine_candidate = True

            else:
                # Unflag the cell - enable left click
                self.cell_btn_object.configure(
                    text="",
                    fg="black",
                )
                self.is_mine_candidate = False
    
    @staticmethod
    def start_timer():
        import time
        Cell.timer_started = True
        Cell.start_time = time.time()
        Cell.update_timer()
    
    @staticmethod
    def update_timer():
        import time
        if Cell.timer_started and Cell.timer_label_object:
            elapsed = int(time.time() - Cell.start_time)
            Cell.timer_label_object.configure(text=f"{elapsed:02d}")
            # Schedule next update after 1000ms
            Cell.timer_label_object.after(1000, Cell.update_timer)
    
    @staticmethod
    def stop_timer():
        Cell.timer_started = False
    
    @staticmethod
    def show_game_over_window(parent_root, restart_callback):
        """Display a custom game over window with GIF, message, and buttons"""
        game_over_window = Toplevel(parent_root)
        game_over_window.title("Game Over")
        game_over_window.geometry("400x500")
        game_over_window.resizable(False, False)
        game_over_window.configure(bg="#9c9c9c")
        
        # Center the window on the parent window
        game_over_window.update_idletasks()
        parent_x = parent_root.winfo_x()
        parent_y = parent_root.winfo_y()
        parent_width = parent_root.winfo_width()
        parent_height = parent_root.winfo_height()
        win_width = 400
        win_height = 500
        x = parent_x + (parent_width - win_width) // 2
        y = parent_y + (parent_height - win_height) // 2
        game_over_window.geometry(f"400x500+{x}+{y}")
        
        # Game Over message
        message_label = Label(
            game_over_window,
            text="💣 Game Over! 💣\nYou Hit a Mine!",
            font=("System", 18, "bold"),
            bg="#9c9c9c",
            fg="#D62828"
        )
        message_label.pack(pady=15)
        
        # GIF container
        gif_frame = Label(game_over_window, bg="#9c9c9c")
        gif_frame.pack(pady=10)
        
        # Try to load and animate GIF
        gif_path = os.path.join(os.path.dirname(__file__), r"C:\Users\Diane\OneDrive\Desktop\minesweeper try\game-over-cat.gif")
        if os.path.exists(gif_path):
            try:
                gif = Image.open(gif_path)
                frames = []
                durations = []
                
                # Extract all frames from the GIF
                try:
                    while True:
                        duration = gif.info.get('duration', 100)
                        durations.append(duration)
                        frames.append(ImageTk.PhotoImage(gif.convert('RGB').resize((250, 250), Image.Resampling.LANCZOS)))
                        gif.seek(len(frames))
                except EOFError:
                    pass
                
                if frames:
                    # Animate GIF
                    current_frame = [0]
                    
                    def animate_gif():
                        if gif_frame.winfo_exists():
                            gif_frame.configure(image=frames[current_frame[0]])
                            current_frame[0] = (current_frame[0] + 1) % len(frames)
                            delay = durations[current_frame[0] - 1] if current_frame[0] > 0 else durations[-1]
                            gif_frame.after(delay, animate_gif)
                    
                    animate_gif()
            except Exception as e:
                print(f"Error loading GIF: {e}")
        
        # Buttons frame
        button_frame = Label(game_over_window, bg="#9c9c9c")
        button_frame.pack(pady=20)
        
        # Try Again button
        try_again_btn = Button(
            button_frame,
            text="Try Again",
            font=("System", 12, "bold"),
            bg="#c0c0c0",
            fg="#000000",
            relief="raised",
            bd=2,
            width=12,
            command=lambda: [game_over_window.destroy(), restart_callback()]
        )
        try_again_btn.pack(side="left", padx=10)
        
        # Main Menu button
        main_menu_btn = Button(
            button_frame,
            text="Main Menu",
            font=("System", 12, "bold"),
            bg="#c0c0c0",
            fg="#000000",
            relief="raised",
            bd=2,
            width=12,
            command=lambda: [
                game_over_window.destroy(), 
                Cell.root_window.destroy(), 
                subprocess.Popen([sys.executable, os.path.join(os.path.dirname(__file__), 'start.py')])]
        )
        main_menu_btn.pack(side="left", padx=10)
        
        game_over_window.transient(parent_root)
        game_over_window.grab_set()
    
    @staticmethod
    def show_win_window(parent_root, restart_callback):
        """Display a custom win window with GIF, message, and buttons"""
        win_window = Toplevel(parent_root)
        win_window.title("Victory!")
        win_window.geometry("400x500")
        win_window.resizable(False, False)
        win_window.configure(bg="#9c9c9c")
        
        # Center the window on the parent window
        win_window.update_idletasks()
        parent_x = parent_root.winfo_x()
        parent_y = parent_root.winfo_y()
        parent_width = parent_root.winfo_width()
        parent_height = parent_root.winfo_height()
        win_width = 400
        win_height = 500
        x = parent_x + (parent_width - win_width) // 2
        y = parent_y + (parent_height - win_height) // 2
        win_window.geometry(f"400x500+{x}+{y}")
        
        # Congratulations message
        message_label = Label(
            win_window,
            text="🎉 Congratulations! 🎉\nYou Won the Game!",
            font=("System", 18, "bold"),
            bg="#9c9c9c",
            fg="#000080"
        )
        message_label.pack(pady=15)
        
        # GIF container
        gif_frame = Label(win_window, bg="#9c9c9c")
        gif_frame.pack(pady=10)
        
        # Try to load and animate GIF
        gif_path = os.path.join(os.path.dirname(__file__), r"C:\Users\Diane\Downloads\cat-kitty.gif")
        if os.path.exists(gif_path):
            try:
                gif = Image.open(gif_path)
                frames = []
                durations = []
                
                # Extract all frames from the GIF
                try:
                    while True:
                        duration = gif.info.get('duration', 100)
                        durations.append(duration)
                        frames.append(ImageTk.PhotoImage(gif.convert('RGB').resize((250, 250), Image.Resampling.LANCZOS)))
                        gif.seek(len(frames))
                except EOFError:
                    pass
                
                if frames:
                    # Animate GIF
                    current_frame = [0]
                    
                    def animate_gif():
                        if gif_frame.winfo_exists():
                            gif_frame.configure(image=frames[current_frame[0]])
                            current_frame[0] = (current_frame[0] + 1) % len(frames)
                            delay = durations[current_frame[0] - 1] if current_frame[0] > 0 else durations[-1]
                            gif_frame.after(delay, animate_gif)
                    
                    animate_gif()
            except Exception as e:
                print(f"Error loading GIF: {e}")
        
        # Buttons frame
        button_frame = Label(win_window, bg="#9c9c9c")
        button_frame.pack(pady=20)
        
        # Play Again button
        play_again_btn = Button(
            button_frame,
            text="Play Again",
            font=("System", 12, "bold"),
            bg="#c0c0c0",
            fg="#000000",
            relief="raised",
            bd=2,
            width=12,
            command=lambda: [win_window.destroy(), restart_callback()]
        )
        play_again_btn.pack(side="left", padx=10)
        
        # Main Menu button
        main_menu_btn = Button(
            button_frame,
            text="Main Menu",
            font=("System", 12, "bold"),
            bg="#c0c0c0",
            fg="#000000",
            relief="raised",
            bd=2,
            width=12,
            command=lambda: [
                win_window.destroy(), 
                Cell.root_window.destroy(), 
                subprocess.Popen([sys.executable, os.path.join(os.path.dirname(__file__), 'start.py')])]
        )
        main_menu_btn.pack(side="left", padx=10)
        
        win_window.transient(parent_root)
        win_window.grab_set()

    @staticmethod
    def randomize_mines():
        # Reset mines
        for cell in Cell.all:
            cell.is_mine = False

        picked_cells = random.sample(Cell.all, settings.HMINES_COUNT)
        for cell in picked_cells:
            cell.is_mine = True

    def __repr__(self):
        return f"cell({self.x},{self.y})"