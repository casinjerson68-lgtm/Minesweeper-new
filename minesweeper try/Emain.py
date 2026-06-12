import tkinter as tk
import Elogic
import settings

WINDOW_SIZE = settings.WINDOW_SIZE
HEADER_HEIGHT = settings.HEADER_HEIGHT
GRID_SIZE = settings.EASY_GRID_SIZE

root = tk.Tk()
root.title("Minesweeper")
root.geometry(f"{WINDOW_SIZE}x{WINDOW_SIZE}")
root.resizable(False, False)
root.configure(bg='#9c9c9c')

# Connect root window to Cell class
Elogic.Cell.root_window = root

# Create main container with border
main_container = tk.Frame(root, bg="#b9b9b9", relief=tk.RAISED, bd=3)
main_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

# Create header frame with border
header_frame = tk.Frame(main_container, bg='#9c9c9c', height=HEADER_HEIGHT, relief=tk.RAISED, bd=4)
header_frame.pack(fill=tk.X, padx=5, pady=5)
header_frame.pack_propagate(False)

# Cell counter (left)
cell_counter_frame = tk.Frame(header_frame, bg='#9c9c9c', width=70, height=50, relief=tk.RAISED, bd=2)
cell_counter_frame.pack(side=tk.LEFT, padx=10, pady=5)
cell_counter_frame.pack_propagate(False)

cell_counter_inner = tk.Frame(cell_counter_frame, bg='#000080', relief=tk.SUNKEN, bd=2)
cell_counter_inner.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

cell_counter_label = tk.Label(cell_counter_inner, text=f"{Elogic.Cell.cell_count}", font=('System', 28, 'bold'), 
                       bg='#000080', fg='#ff0000')
cell_counter_label.pack()

# Connect label to Cell class
Elogic.Cell.cell_count_label_object = cell_counter_label

# Reset button (center)
Title = tk.Label(header_frame, text='Minesweeper', font=('System', 28, 'bold'),
                         bg="#b9b9b9", relief=tk.SUNKEN, bd=3)
Title.pack(side=tk.LEFT, expand=True)

# Timer (right)
timer_frame = tk.Frame(header_frame, bg='#9c9c9c', width=70, height=50, relief=tk.RAISED, bd=2)
timer_frame.pack(side=tk.LEFT, padx=10, pady=5)
timer_frame.pack_propagate(False)

timer_inner = tk.Frame(timer_frame, bg='#000080', relief=tk.SUNKEN, bd=2)
timer_inner.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

timer_label = tk.Label(timer_inner, text='00', font=('System', 32, 'bold'),
                       bg='#000080', fg='#ff0000')
timer_label.pack()

# Connect timer label to Cell class
Elogic.Cell.timer_label_object = timer_label

# Create game board frame with border
board_outer = tk.Frame(main_container, bg="#9c9c9c", relief=tk.RAISED, bd=2)
board_outer.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

board_frame = tk.Frame(board_outer, bg="#9c9c9c", relief=tk.SUNKEN, bd=2)
board_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

# Configure grid weights for equal cell distribution
for i in range(GRID_SIZE):
    board_frame.grid_rowconfigure(i, weight=1)
    board_frame.grid_columnconfigure(i, weight=1)

# Create grid of cells
for row in range(settings.EASY_GRID_SIZE):
    for col in range(settings.EASY_GRID_SIZE):
        c = Elogic.Cell(row, col)
        c.Create_btn_object(board_frame)
        c.cell_btn_object.grid(row=row, column=col, sticky='nsew')

Elogic.Cell.randomize_mines()

# debug (optional)
for c in Elogic.Cell.all:
    print(c.is_mine)
root.mainloop()