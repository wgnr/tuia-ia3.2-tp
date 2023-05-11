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

        # Initialize the explored dictionary
        explored = {node.state: True}

        if node.state == grid.end:
            return Solution(node, explored)

        # Initialize the frontier with the initial node
        frontier = QueueFrontier()
        frontier.add(node)

        while not frontier.is_empty():
            # Remove a node from the frontier
            node = frontier.remove()

            neighbours = grid.get_neighbours(node.state)
            for action, postion in neighbours.items():
                child_node = Node(
                    value="",
                    state=postion,
                    cost=node.cost + grid.get_cost(postion),
                    parent=node,
                    action=action)

                if child_node.state == grid.end:
                    return Solution(child_node, explored)

                if child_node.state not in explored:
                    explored[child_node.state] = True
                    frontier.add(child_node)

        return NoSolution(explored)
