from ..models.grid import Grid
from ..models.frontier import PriorityQueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class UniformCostSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Uniform Cost Search

        Args:
            grid (Grid): Grid of points

        Returns:
            Solution: Solution found
        """
        # Initialize a node with the initial position
        node = Node(value="root", state=grid.start, cost=0)

        # Initialize the explored dictionary
        explored = {node.state: node}

        frontier = PriorityQueueFrontier()
        frontier.add(node, node.cost)

        while not frontier.is_empty():
            node = frontier.pop()

            if node.state == grid.end:
                return Solution(node, explored)

            neighbours = grid.get_neighbours(node.state)

            for action, postion in neighbours.items():
                child_cost = node.cost + grid.get_cost(postion)

                if postion not in explored or child_cost < explored[postion].cost:
                    child_node = Node(
                        value="",
                        state=postion,
                        cost=child_cost,
                        parent=node,
                        action=action)
                    frontier.add(child_node, child_node.cost)
                    explored[child_node.state] = child_node

        return NoSolution(explored)
