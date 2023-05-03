from ..models.grid import Grid
from ..models.frontier import StackFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class DepthFirstSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Depth First Search

        Args:
            grid (Grid): Grid of points

        Returns:
            Solution: Solution found
        """
        node = Node("", grid.start, cost=0)

        # Initialize the explored dictionary to be empty
        explored = {}

        # Initialize the frontier with the initial node
        frontier = StackFrontier()
        frontier.add(node)

        while not frontier.is_empty():
            # Remove a node from the frontier
            node = frontier.remove()

            # Return if the node contains a goal state
            if node.state == grid.end:
                return Solution(node, explored)

            if node.state not in explored:
                # Mark the node as explored
                explored[node.state] = True

                neighbours = grid.get_neighbours(node.state)
                for action, postion in neighbours.items():
                    if postion not in explored:
                        child_node = Node(
                            value="",
                            state=postion,
                            cost=node.cost + grid.get_cost(postion),
                            parent=node,
                            action=action)
                        frontier.add(child_node)

        return NoSolution(explored)
