from ..models.grid import Grid
from ..models.frontier import QueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class BreadthFirstSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Breadth First Search

        Args:
            grid (Grid): Grid of points

        Returns:
            Solution: Solution found
        """
        # Initialize a node with the initial position
        node = Node("", grid.start, cost=0)

        # Initialize the explored dictionary to be empty
        explored = {}

        # Initialize the frontier with the initial node
        frontier = QueueFrontier()
        frontier.add(node)

        while not frontier.is_empty():
            # Remove a node from the frontier
            node = frontier.remove()

            # Mark the node as explored
            explored[node.state] = True

            # Return if the node contains a goal state
            if node.state == grid.end:
                return Solution(node, explored)

            # BFS
            neighbours = grid.get_neighbours(node.state)
            for action, postion in neighbours.items():
                if postion not in explored:
                    new_node = Node(
                        "", postion, node.cost + grid.get_cost(postion), parent=node, action=action)
                    frontier.add(new_node)

        return NoSolution(explored)
