import tkinter as tk
from tkinter import PhotoImage
import subprocess
import os
import sys

tree = tk.Tk()
tree.configure(bg='white')
tree.geometry("1280x720")
tree.title("Minesweeper")
tree.resizable(False, False)
image_path = PhotoImage(file=r"C:\Users\Diane\Downloads\minesweeper-screen-saver-v0-x8pud88xawsa1.gif")

bg_image = tk.Label(tree, image=image_path)
bg_image.place(relwidth=1, relheight=1)

title_frame = tk.Frame(tree)
title_frame.pack(fill='x', pady=(20, 10))
title_frame.place(x=640, y=210, anchor='center')
title_label = tk.Label(title_frame, 
    text='Minesweeper Game',
    bg='gray20',
    fg='white',
    font=('System', 50, 'bold')
    )
title_label.pack()

def create_rounded_rect(canvas, x1, y1, x2, y2, radius=10, **kwargs):
    points = [
        x1 + radius, y1,
        x2 - radius, y1,
        x2, y1,
        x2, y1 + radius,
        x2, y2 - radius,
        x2, y2,
        x2 - radius, y2,
        x1 + radius, y2,
        x1, y2,
        x1, y2 - radius,
        x1, y1 + radius,
        x1, y1,
    ]
    return canvas.create_polygon(points, smooth=True, splinesteps=36, **kwargs)

class RoundedButton(tk.Canvas):
    def __init__(self, parent, text, width, height, radius=20, bg='#4CAF50', fg='white', hover_bg=None, command=None, font=('System', 14, 'bold')):
        super().__init__(parent, width=width, height=height, bg=parent['bg'], highlightthickness=0, bd=0, relief='sunken')
        self.command = command
        self.bg = bg
        self.hover_bg = hover_bg or bg
        self.rect = create_rounded_rect(self, 2, 2, width - 2, height - 2, radius, fill=bg, outline=bg)
        self.text_item = self.create_text(width / 2, height / 2, text=text, fill=fg, font=font)

        self.tag_bind(self.rect, '<Button-1>', self._on_click)
        self.tag_bind(self.text_item, '<Button-1>', self._on_click)
        self.tag_bind(self.rect, '<Enter>', self._on_enter)
        self.tag_bind(self.text_item, '<Enter>', self._on_enter)
        self.tag_bind(self.rect, '<Leave>', self._on_leave)
        self.tag_bind(self.text_item, '<Leave>', self._on_leave)


    def _on_click(self, event):
        if self.command:
            self.command()

    def _on_enter(self, event):
        self.itemconfig(self.rect, fill=self.hover_bg, outline=self.hover_bg)

    def _on_leave(self, event):
        self.itemconfig(self.rect, fill=self.bg, outline=self.bg)


def show_difficulties():
    difficulty_window = tk.Toplevel(tree)
    difficulty_window.configure(bg='gray20')
    difficulty_window.title("Select Difficulty")
    difficulty_window.resizable(False, False)
    difficulty_window.transient(tree)
    
    # Center the window
    window_width = 400
    window_height = 400
    x = (tree.winfo_width() // 2) - (window_width // 2) + tree.winfo_x()
    y = (tree.winfo_height() // 2) - (window_height // 2) + tree.winfo_y()
    difficulty_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Title
    title_frame = tk.Frame(difficulty_window, bg="gray20")
    title_frame.pack(fill='x', pady=(20, 30))
    title_label = tk.Label(title_frame, 
        text='Select Difficulty', 
        bg='gray20', 
        fg='white', 
        font=('Times New Roman', 24, 'bold')
    )
    title_label.pack()
    
    # Easy Button
    easy_button = RoundedButton(
        difficulty_window,
        text='Easy',
        width=260,
        height=55,
        radius=15,
        bg='#4CAF50',
        hover_bg="#99C59B",
        fg='white',
        font=('Arial', 16, 'bold')
    )
    easy_button.pack(pady=10)

    # Medium Button
    medium_button = RoundedButton(
        difficulty_window,
        text='Medium',
        width=260,
        height=55,
        radius=15,
        bg='#FF9800',
        hover_bg="#FFB74D",
        fg='white',
        font=('Arial', 16, 'bold')
    )
    medium_button.pack(pady=10)

    # Hard Button
    hard_button = RoundedButton(
        difficulty_window,
        text='Hard',
        width=260,
        height=55,
        radius=15,
        bg='#F44336',
        hover_bg="#EF5350",
        fg='white',
        font=('Arial', 16, 'bold')
    )
    hard_button.pack(pady=10)

def play_game():
    show_difficulties()

def show_instructions():
    instruction_window = tk.Toplevel(tree)
    instruction_window.configure(bg='gray20')
    instruction_window.title("How to Play Minesweeper")
    instruction_window.resizable(False, False)
    instruction_window.transient(tree)
    
    # Center the window
    window_width = 600
    window_height = 500
    x = (tree.winfo_width() // 2) - (window_width // 2) + tree.winfo_x()
    y = (tree.winfo_height() // 2) - (window_height // 2) + tree.winfo_y()
    instruction_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Title
    title_frame = tk.Frame(instruction_window, bg="gray20")
    title_frame.pack(fill='x', pady=(15, 10))
    title_label = tk.Label(title_frame, 
        text='How to Play Minesweeper', 
        bg='gray20', 
        fg='white', 
        font=('Times New Roman', 24, 'bold')
    )
    title_label.pack()
    
    # Instructions text
    text_frame = tk.Frame(instruction_window, bg='gray20')
    text_frame.pack(fill='both', expand=True, padx=20, pady=(10, 20))
    
    instructions_text = """
Objective:
Clear all cells without hitting a mine.

How to Play:
• Left-click on a cell to reveal it
• Right-click on a cell to flag/unflag it
• Numbers show how many mines are adjacent to that cell
• If you reveal a mine, the game is over
• Flag all mines and reveal all safe cells to win!

Tips:
• Start by clicking in the center or corners
• Use logic to deduce where mines are
• If a cell shows 0, all adjacent cells are safe
• Flag mines to keep track of them
• Take your time and think strategically!
    """
    
    instructions_label = tk.Label(text_frame,
        text=instructions_text,
        bg='gray20',
        fg='white',
        font=('Arial', 11),
        justify='left',
        wraplength=550
    )
    instructions_label.pack(fill='both', expand=True)
    
    # Close button
    close_button = RoundedButton(
        instruction_window,
        text='Close',
        width=150,
        height=45,
        radius=15,
        bg='#4CAF50',
        hover_bg="#99C59B",
        fg='white',
        font=('Arial', 12, 'bold'),
        command=instruction_window.destroy
    )
    close_button.pack(pady=(0, 20))
    

play_button = RoundedButton(
    tree,
    text='Play',
    width=260,
    height=70,
    radius=25,
    bg='#4CAF50',
    hover_bg="#99C59B",
    fg='white',
    font=('Arial', 20, 'bold'),
    command=play_game
)
play_button.pack()
play_button.place(x=640, y=360, anchor='center')

how_to_play_button = RoundedButton(
    tree,
    text='How to Play',
    width=260,
    height=55,
    radius=25,
    bg="#33353D",
    hover_bg="#616368",
    fg='white',
    font=('Arial', 14),
    command=show_instructions
)
how_to_play_button.pack()
how_to_play_button.place(x=640, y=440, anchor='center')


tree.mainloop()
