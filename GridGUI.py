import tkinter as tk
from tkinter import Scrollbar, Canvas, Frame, messagebox, filedialog
from Grid import Grid
from Algorithms import BFS, DFS, GBFS, AStarSearch, BeamSearch, BiDirectionalSearch

CELL_SIZE = 40
AGENT_COLOR = "red"
WALL_COLOR = "grey"
GOAL_COLOR = "green"
EMPTY_COLOR = "white"

class GridGUI:
    def __init__(self, grid=None):
        self.root = tk.Tk()
        self.root.title("Grid Environment")
        self.frame = Frame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.canvas = Canvas(self.frame, bg="white")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.v_scroll = Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)
        self.h_scroll = Scrollbar(self.frame, orient="horizontal", command=self.canvas.xview)

        self.canvas.configure(yscrollcommand=self.v_scroll.set, xscrollcommand=self.h_scroll.set) 
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        self.buttons = {} 
        
        self.open_file_button = tk.Button(self.root, text="Open File", command=self.open_file)
        self.open_file_button.pack()
        
        if grid:
            self.grid = grid
            self.grid_data = grid.grid
            self.setup_grid()
        else:
            self.grid = None
            self.grid_data = []
        
    def create_buttons(self):
        if not self.buttons:
            self.buttons = {
                'bfs': tk.Button(self.root, text="Start BFS Search", command=lambda: self.reset_and_search(BFS(self.grid))),
                'dfs': tk.Button(self.root, text="Start DFS Search", command=lambda: self.reset_and_search(DFS(self.grid))),
                'gbfs': tk.Button(self.root, text="Start GBFS Search", command=lambda: self.reset_and_search(GBFS(self.grid))),
                'astar': tk.Button(self.root, text="Start A* Search", command=lambda: self.reset_and_search(AStarSearch(self.grid))),
                'bidirectional': tk.Button(self.root, text="Start Bi-Directional Search", command=lambda: self.reset_and_search(BiDirectionalSearch(self.grid))),
                'beam': tk.Button(self.root, text="Start Beam Search", command=lambda: self.reset_and_search(BeamSearch(self.grid))),
                'open': tk.Button(self.root, text="Open File", command=self.open_file)
            }
            for button in self.buttons.values():
                button.pack()


        
    def open_file(self):
        filepath = filedialog.askopenfilename(title="Open File", filetypes=[("Text Files", "*.txt")])
        if filepath:
            self.grid = Grid(filepath)
            self.grid_data = self.grid.grid
            self.setup_grid()
    
    def setup_grid(self):
        self.canvas.delete("all")
        self.draw_grid(self.grid_data)
        self.create_buttons()
        self.open_file_button.destroy()
        self.update_scroll_region()
    
    def update_scroll_region(self):
        if self.grid_data:
            self.canvas.config(scrollregion=(0, 0, len(self.grid_data[0]) * CELL_SIZE, len(self.grid_data) * CELL_SIZE))
        

    def draw_grid(self, grid):
        self.grid_squares = {}
        for y, row in enumerate(grid):
            for x, cell in enumerate(row):
                fill_color = EMPTY_COLOR if cell == '' else AGENT_COLOR if cell == 'A' else WALL_COLOR if cell == 'W' else GOAL_COLOR
                self.grid_squares[(x, y)] = self.canvas.create_rectangle(x * CELL_SIZE, y * CELL_SIZE, (x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE, fill=fill_color, outline="black")

    def reset_and_search(self, search_algorithm):
        self.disable_all_buttons()
        self.draw_grid(self.grid.grid)
        goal_node, path, explored_nodes, explored_nodes_num = search_algorithm.search(self.grid.agent_position, self.grid.goals)
        if goal_node:
            self.color_nodes_step_by_step(explored_nodes, 0, lambda: self.show_path(path))
        else:
            messagebox.showinfo("Search Result", "No goal was reached.")
            self.enable_all_buttons()

    def disable_all_buttons(self):
        for button in self.buttons.values():
            button.config(state=tk.DISABLED)

    def enable_all_buttons(self):
        for button in self.buttons.values():
            button.config(state=tk.NORMAL)


    def color_nodes_step_by_step(self, nodes, index, callback):
        if index >= len(nodes):
            callback()
            return
        y, x, status = nodes[index]
        color = "light blue" if status == 'explored' else "brown"
        self.canvas.itemconfig(self.grid_squares[(x, y)], fill=color)
        self.root.after(100, lambda: self.color_nodes_step_by_step(nodes, index + 1, callback))

    def show_path(self, path):
        start = (self.grid.agent_position[1], self.grid.agent_position[0])
        self.canvas.itemconfig(self.grid_squares[start], fill="pink")
        self.root.update_idletasks()
        for move in path:
            if move == 'up':
                start = (start[0], start[1] - 1)
            elif move == 'down':
                start = (start[0], start[1] + 1)
            elif move == 'left':
                start = (start[0] - 1, start[1])
            elif move == 'right':
                start = (start[0] + 1, start[1])
            self.canvas.itemconfig(self.grid_squares[start], fill="pink")
            self.root.update_idletasks()
            self.enable_all_buttons()

    def update_grid(self):
        self.canvas.delete("all")  
        for y, row in enumerate(self.grid.grid):
            for x, cell in enumerate(row):
                color = EMPTY_COLOR
                if cell == 'A':
                    color = AGENT_COLOR
                elif cell == 'W':
                    color = WALL_COLOR
                elif cell == 'G':
                    color = GOAL_COLOR
                self.canvas.create_rectangle(x * CELL_SIZE, y * CELL_SIZE, (x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE, fill=color, outline='black')

    def run(self):
        self.root.mainloop()


