
class Grid:
    def __init__(self, filepath=None):
        if filepath:
            self.load_grid_data(filepath)
        else:
            self.grid = []
            self.agent_position = (0, 0) 
            self.goals = set()

    def load_grid_data(self, filepath):
        with open(filepath, 'r') as file:
            lines = file.readlines()
        grid_dimensions = tuple(map(int, lines[0].strip().strip('[]').split(',')))
        rows, cols = grid_dimensions
        self.grid = [['' for _ in range(cols)] for _ in range(rows)]
        agent_position = tuple(map(int, lines[1].strip().strip('()').split(',')))
        self.grid[agent_position[1]][agent_position[0]] = 'A'
        self.agent_position = (agent_position[1], agent_position[0])
        self.goals = set()
        goal_positions = lines[2].strip().split(' | ')
        for goal in goal_positions:
            r, c = map(int, goal.strip('()').split(','))
            self.grid[c][r] = 'G'
            self.goals.add((c, r))
        for line in lines[3:]:
            x, y, width, height = map(int, line.strip().strip('()').split(','))
            for i in range(x, x + width):
                for j in range(y, y + height):
                    self.grid[j][i] = 'W'

    def is_valid_move(self, x, y):
        if 0 <= x < len(self.grid) and 0 <= y < len(self.grid[0]):
            return self.grid[x][y] not in ('W', 'A')
        return False