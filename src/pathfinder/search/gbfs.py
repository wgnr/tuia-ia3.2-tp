from ..models.grid import Grid
from ..models.frontier import PriorityQueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node
from typing import Callable


def manhattan_distance(node: Node, goal: tuple[int, int]) -> int:
    return sum(abs(a-b) for a, b in zip(node.state, goal))


class GreedyBestFirstSearch:
    @staticmethod
    def search(grid: Grid, h: Callable[[Node, tuple[int, int]], int] = manhattan_distance) -> Solution:
        """Find path between two points in a grid using Greedy Best First Search

        Args:
            grid (Grid): Grid of points

        Returns:
            Solution: Solution found
        """
        # Initialize a node with the initial position
        node = Node("root", grid.start, 0)

        # Initialize the explored dictionary
        explored = {node.state: node}

        frontier = PriorityQueueFrontier()
        frontier.add(node, h(node, grid.end))

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
                    explored[child_node.state] = child_node
                    frontier.add(child_node, h(child_node, grid.end))

        return NoSolution(explored)
