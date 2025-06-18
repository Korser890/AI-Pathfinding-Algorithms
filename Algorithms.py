import sys
import heapq
from collections import deque
from SearchAlgo import SearchAlgorithm

class BFS(SearchAlgorithm):
    def search(self, start, goals):
        directions = [((-1, 0), 'up'), ((0, -1), 'left'), ((1, 0), 'down'), ((0, 1), 'right')]
        queue = deque([(start, [])])
        visited = set([start])
        explored_nodes = []
        nodes_explored = 1

        while queue:
            current, path = queue.popleft()
            nodes_explored += 1
            explored_nodes.append((current[0], current[1], 'explored')) 

            if current in goals:
                return current, path, explored_nodes, nodes_explored

            for (dx, dy), move in directions:
                nx, ny = current[0] + dx, current[1] + dy
                if self.grid.is_valid_move(nx, ny) and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    explored_nodes.append((nx, ny, 'visited'))  
                    queue.append(((nx, ny), path + [move]))

        return None, [], explored_nodes, nodes_explored 

class DFS(SearchAlgorithm):
    def search(self, start, goals):
        directions = [((0, 1), 'right'), ((1, 0), 'down'), ((0, -1), 'left'), ((-1, 0), 'up')]
        stack = deque([(start, [])])  
        visited = set([start]) 
        explored_nodes = []
        nodes_explored = 0 

        nodes_explored += 1
        explored_nodes.append((start[0], start[1], 'explored')) 

        while stack:
            current, moves = stack.pop()
            explored_nodes.append((current[0], current[1], 'explored'))

            if current in goals:
                return current, moves, explored_nodes, nodes_explored

            for (dx, dy), move in directions:
                nx, ny = current[0] + dx, current[1] + dy
                next_node = (nx, ny)
                if self.grid.is_valid_move(nx, ny) and next_node not in visited:
                    visited.add(next_node) 
                    nodes_explored += 1 
                    explored_nodes.append((nx, ny, 'visited')) 
                    stack.append((next_node, moves + [move]))

        return None, [], explored_nodes, nodes_explored


class GBFS(SearchAlgorithm):
    def heuristic(self, node):
        return min(abs(node[0] - goal[0]) + abs(node[1] - goal[1]) for goal in self.grid.goals)

    def search(self, start, goals):
        priority_queue = []
        heapq.heappush(priority_queue, (self.heuristic(start), start, [])) 
        visited = set()
        explored_nodes = []
        nodes_explored = 1
        
        
        while priority_queue:
            _, current, moves = heapq.heappop(priority_queue)
            explored_nodes.append((current[0], current[1], 'explored'))
            if current in visited:
                continue
            visited.add(current)

            if current in goals:
                return (current, moves,  explored_nodes, nodes_explored)

            for (dx, dy), move in [((-1, 0), 'up'), ((0, -1), 'left'), ((1, 0), 'down'), ((0, 1), 'right')]:
                nx, ny = current[0] + dx, current[1] + dy
                if self.grid.is_valid_move(nx, ny) and (nx, ny) not in visited:
                    heapq.heappush(priority_queue, (self.heuristic((nx, ny)), (nx, ny), moves + [move]))
                    nodes_explored += 1
                    explored_nodes.append((nx, ny, 'visited'))
       
        return None, [], explored_nodes, nodes_explored
    
class AStarSearch(SearchAlgorithm):
    def heuristic(self, node):
        return min(abs(node[0] - goal[0]) + abs(node[1] - goal[1]) for goal in self.grid.goals)

    def search(self, start, goals):
        priority_queue = []
        initial_heuristic = self.heuristic(start)
        heapq.heappush(priority_queue, (initial_heuristic, 0, start, []))
        visited = set()
        nodes_explored = 1
        explored_nodes = []

        while priority_queue:
            f, g, current, moves = heapq.heappop(priority_queue)
            nodes_explored += 1
            explored_nodes.append((current[0], current[1], 'explored'))
            if current in visited:
                continue
            visited.add(current)

            if current in goals:
                return (current, moves, explored_nodes, nodes_explored)

            for (dx, dy), move in [((-1, 0), 'up'), ((0, -1), 'left'), ((1, 0), 'down'), ((0, 1), 'right')]:
                nx, ny = current[0] + dx, current[1] + dy
                if self.grid.is_valid_move(nx, ny) and (nx, ny) not in visited:
                    new_g = g + 1
                    h = self.heuristic((nx, ny))
                    new_f = new_g + h
                    heapq.heappush(priority_queue, (new_f, new_g, (nx, ny), moves + [move]))
                    explored_nodes.append((nx, ny, 'visited'))

        return None, [], explored_nodes, nodes_explored

class BiDirectionalSearch(SearchAlgorithm):
    def search(self, start, goals):
        if not goals:
            return None, [], [], []

        front_queue = deque([(start, [])])
        front_visited = {start: []}
        explored_nodes = []
        nodes_explored = 0

        back_queue = deque()
        back_visited = {}
        for goal in goals:
            back_queue.append((goal, []))
            back_visited[goal] = []

        while front_queue and back_queue:
            nodes_explored += 1

            if front_queue:
                front_current, front_moves = front_queue.popleft()
                explored_nodes.append((front_current[0], front_current[1], 'explored'))
                if front_current in back_visited:
                    goal_node = front_current if front_current in goals else list(goals)[0]
                    combined_moves = front_moves + back_visited[front_current][::-1]
                    return goal_node, combined_moves, explored_nodes, nodes_explored

                for (dx, dy), move in [((-1, 0), 'up'), ((0, -1), 'left'), ((1, 0), 'down'), ((0, 1), 'right')]:
                    nx, ny = front_current[0] + dx, front_current[1] + dy
                    if self.grid.is_valid_move(nx, ny) and (nx, ny) not in front_visited:
                        front_visited[(nx, ny)] = front_moves + [move]
                        front_queue.append(((nx, ny), front_visited[(nx, ny)]))
                        explored_nodes.append((nx, ny, 'visited'))

            if back_queue:
                back_current, back_moves = back_queue.popleft()
                explored_nodes.append((back_current[0], back_current[1], 'explored'))
                if back_current in front_visited:
                    goal_node = back_current if back_current in goals else start
                    combined_moves = front_visited[back_current] + back_moves[::-1]
                    return goal_node, combined_moves, explored_nodes, nodes_explored

                for (dx, dy), move in [((-1, 0), 'down'), ((0, -1), 'right'), ((1, 0), 'up'), ((0, 1), 'left')]:
                    nx, ny = back_current[0] + dx, back_current[1] + dy
                    if self.grid.is_valid_move(nx, ny) and (nx, ny) not in back_visited:
                        back_visited[(nx, ny)] = back_moves + [move]
                        back_queue.append(((nx, ny), back_visited[(nx, ny)]))
                        explored_nodes.append((nx, ny, 'visited'))

        return None, [], explored_nodes, nodes_explored

class BeamSearch(SearchAlgorithm):
    def __init__(self, grid, beam_width=3):
        super().__init__(grid)
        self.beam_width = beam_width

    def heuristic(self, node):
        return min(abs(node[0] - goal[0]) + abs(node[1] - goal[1]) for goal in self.grid.goals)

    def search(self, start, goals):
        if not goals:
            return None, [], [], 0

        priority_queue = [(self.heuristic(start), start, [])]
        visited = set()
        explored_nodes = []
        nodes_explored = 0

        while priority_queue:
            priority_queue.sort(key=lambda x: x[0])
            current_level = priority_queue[:self.beam_width]
            priority_queue = []

            for _, current, path in current_level:
                nodes_explored += 1
                explored_nodes.append((current[0], current[1], 'explored'))
                visited.add(current)

                if current in goals:
                    return current, path, explored_nodes, nodes_explored

                for (dx, dy), move in [((-1, 0), 'up'), ((0, -1), 'left'), ((1, 0), 'down'), ((0, 1), 'right')]:
                    nx, ny = current[0] + dx, current[1] + dy
                    if self.grid.is_valid_move(nx, ny) and (nx, ny) not in visited:
                        new_path = path + [move]
                        priority_queue.append((self.heuristic((nx, ny)), (nx, ny), new_path))
                        explored_nodes.append((nx, ny, 'visited'))

        return None, [], explored_nodes, nodes_explored