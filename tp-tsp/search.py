"""Este modulo define la clase LocalSearch.

LocalSearch representa un algoritmo de busqueda local general.

Las subclases que se encuentran en este modulo son:

* HillClimbing: algoritmo de ascension de colinas. Se mueve al sucesor con
mejor valor objetivo, y los empates se resuelvan de forma aleatoria.
Ya viene implementado.

* HillClimbingReset: algoritmo de ascension de colinas de reinicio aleatorio.
No viene implementado, se debe completar.

* Tabu: algoritmo de busqueda tabu.
No viene implementado, se debe completar.
"""


from __future__ import annotations
from problem import OptProblem, TSP
from node import Node, Action
from random import choice
from time import time
from collections import deque


class LocalSearch:
    """Clase que representa un algoritmo de busqueda local general."""

    def __init__(self) -> None:
        """Construye una instancia de la clase."""
        self.niters = 0  # Numero de iteraciones totales
        self.time = 0  # Tiempo de ejecucion
        self.tour = []  # Solucion, inicialmente vacia
        self.value = None  # Valor objetivo de la solucion

    def solve(self, problem: TSP):
        """Resuelve un problema de optimizacion."""
        self.tour = problem.init
        self.value = problem.obj_val(problem.init)


class HillClimbing(LocalSearch):
    """Clase que representa un algoritmo de ascension de colinas.

    En cada iteracion se mueve al estado sucesor con mejor valor objetivo.
    El criterio de parada es alcanzar un optimo local.
    """

    def solve(self, problem: TSP):
        """Resuelve un problema de optimizacion con ascension de colinas.

        Argumentos:
        ==========
        problem: OptProblem
            un problema de optimizacion
        """
        # Inicio del reloj
        start = time()

        # Crear el nodo inicial
        actual = Node(problem.init, problem.obj_val(problem.init))

        while True:

            # Determinar las acciones que se pueden aplicar
            # y las diferencias en valor objetivo que resultan
            diff = problem.val_diff(actual.state)

            # Buscar las acciones que generan el  mayor incremento de valor obj
            max_acts = [act for act, val in diff.items() if val ==
                        max(diff.values())]

            # Elegir una accion aleatoria
            act = choice(max_acts)

            # Retornar si estamos en un optimo local
            if diff[act] <= 0:

                self.tour = actual.state
                self.value = actual.value
                end = time()
                self.time = end-start
                return

            # Sino, moverse a un nodo con el estado sucesor
            else:

                actual = Node(problem.result(actual.state, act),
                              actual.value + diff[act])
                self.niters += 1


class HillClimbingReset(LocalSearch):
    """Algoritmo de ascension de colinas con reinicio aleatorio."""

    def solve(self, problem: TSP):
        start = time()
        attempts = 10
        best_value = float("-inf")

        for _ in range(attempts):
            solution = HillClimbing()
            solution.solve(problem)
            problem.random_reset()
            self.niters += solution.niters
            if best_value < solution.value:
                best_value = solution.value
                self.tour = solution.tour
                self.value = solution.value
                self.time = time()-start


class Tabu(LocalSearch):
    """Algoritmo de busqueda tabu."""

    def solve(self, problem: TSP):
        start = time()

        # Crear el nodo inicial
        actual = Node(problem.init, problem.obj_val(problem.init))
        best = actual
        tabu = deque(maxlen=len(problem.init)//5)
        no_improvements_counter = 0

        while True:
            if no_improvements_counter > len(problem.init)//3:
                # print("SALE POR FALTA DE MEJORAS")
                break

            if self.niters > len(problem.init)*5:
                # print("SALE POR EXCESO DE ITERACIONES")
                break

            self.niters += 1
            diff = problem.val_diff(actual.state)

            max_val = max(diff.values())
            bests_act_val = [(act, val) for act, val in diff.items()
                             if abs(max_val - val)/abs(max_val) < 0.05
                             and act not in tabu]

            if not bests_act_val:
                # print("SALE POR NO HABER MAS ACCIONES")
                break

            act, val = choice(bests_act_val)
            neightbour = Node(problem.result(
                actual.state, act), actual.value + val)

            if (best.value - neightbour.value)/best.value < 1e-4:
                no_improvements_counter += 1

            if best.value < neightbour.value:
                best = neightbour

            # insertamos la accion contraria
            tabu.append(act[::-1])
            actual = neightbour

        self.tour = best.state
        self.value = best.value
        end = time()
        self.time = end-start

class TabuReset(LocalSearch):
    """Algoritmo Tabu con reinicio aleatorio."""

    def solve(self, problem: TSP):
        start = time()
        attempts = 10
        best_value = float("-inf")

        for _ in range(attempts):
            solution = Tabu()
            solution.solve(problem)
            problem.random_reset()
            self.niters += solution.niters
            if best_value < solution.value:
                best_value = solution.value
                self.tour = solution.tour
                self.value = solution.value
                self.time = time()-start