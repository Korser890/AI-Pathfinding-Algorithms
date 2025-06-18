A Python-based pathfinding visualizer that implements BFS, DFS, A, GBFS, Bidirectional, and Beam Search algorithms for solving grid-based robot navigation problems.

## Features
- CLI & Tkinter-based GUI
- Supports:
  - Breadth-First Search (BFS)
  - Depth-First Search (DFS)
  - Greedy Best-First Search (GBFS)
  - A* Search
  - Bidirectional Search
  - Beam Search
- Visual grid exploration in GUI
- Loadable test cases from `.txt` files

## How to Run
- GUI Mode
  - Open your terminal or command prompt.
  - Navigate to the folder containing `search.py`.
  - Run the GUI mode with the following command: python **search.py gui**
  - A window will open with a blank grid.
  - Click the **“Open File”** button to select a `.txt` file (e.g., `RobotNav-test.txt`).
  - Once the file is loaded, click any of the algorithm buttons (e.g., **BFS**, **A\***, etc.) to start the search.
  - The grid will visually display explored nodes and the final path.
  - Click “Open File” again to load a different test case.

- CLI Mode
  - Open your terminal or command prompt.
  - Navigate to the folder containing `search.py`.
  - Run the script using the following command format:
    - python search.py <filename.txt> <algorithm>
    - Replace <filename.txt> with the name of the test file (e.g., RobotNav-test.txt).
  - Replace <algorithm> with one of the following options:
    - bfs for Breadth-First Search
    - dfs for Depth-First Search
    - gbfs for Greedy Best-First Search
    - astar for A* Search
    - bidirectional for Bidirectional Search
    - beam for Beam Search
  - Example Command: python search.py RobotNav-test.txt bfs
