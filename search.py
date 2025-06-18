import sys
from collections import deque
from Grid import Grid
from Algorithms import BFS , DFS, GBFS, AStarSearch, BeamSearch, BiDirectionalSearch
from GridGUI import GridGUI

def main():
    if len(sys.argv) == 3:
        filename = sys.argv[1]
        search_method = sys.argv[2].lower()
        grid = Grid(filename)
        search_algorithms = {
            "bfs": BFS(grid),
            "dfs": DFS(grid),
            "gbfs": GBFS(grid),
            "astar": AStarSearch(grid),
            "bidirectional": BiDirectionalSearch(grid),
            "beam": BeamSearch(grid)
        }
        
        if search_method in search_algorithms:
            search_algorithm = search_algorithms[search_method]
            goal_node, path, explored_nodes, explored_nodes_num = search_algorithm.search(grid.agent_position, grid.goals)
            if goal_node:
                print(f"{filename} {search_method.title()}")
                print(f"<Node ({goal_node[1]}, {goal_node[0]})> {explored_nodes_num}")
                print(f"{path}")
            else:
                print(f"No goal is reachable; {explored_nodes_num}")

    
            
        else:
            print(f"Search method {search_method} not supported.")
    elif len(sys.argv) == 2 and sys.argv[1].lower() == 'gui':

        gui = GridGUI(None) 
        gui.run()
    else:
        print("Usage:")
        print("CLI mode: python gui4.py <filename> <search_method>")
        print("GUI mode: python gui4.py gui")

if __name__ == "__main__":
    main()