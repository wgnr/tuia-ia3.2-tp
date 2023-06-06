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
from problem import TSP
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

    def solve(self, problem: TSP, attempts = 10):
        start = time()
        self.value = float("-inf")

        for _ in range(attempts):
            solution = HillClimbing()
            solution.solve(problem)
            problem.random_reset()
            self.niters += solution.niters
            if self.value < solution.value:
                self.tour = solution.tour
                self.value = solution.value
        
        self.time = time()-start


class Tabu(LocalSearch):
    """Algoritmo de busqueda tabu."""

    def __init__(self, use, max_len=2, prob=0.05, improv_treshold=1e-4) -> None:
        super().__init__()
        self.max_len = max_len
        self.prob = prob
        self.improv_treshold=improv_treshold
        self.reason= None
        self.use = use
    
    def solve(self, problem: TSP):
        if self.use=="estado":
            self.solve_state_(problem)
        else:
            self.solve_act_(problem)

    def solve_state_(self, problem: TSP):
        start = time()

        actual = Node(problem.init, problem.obj_val(problem.init))
        best = actual
        tabu = [actual.state]
        no_improvements_counter = 0

        while True:
            if no_improvements_counter > len(problem.init)*10:
                self.reason="FALTA DE MEJORAS"
                break

            if self.niters > len(problem.init)*30:
                self.reason="EXCESO DE ITERACIONES"
                break

            self.niters += 1

            diff={act: val for act, val in 
                                problem.val_diff(actual.state).items()
                    if problem.result(actual.state, act) not in tabu}
            
            max_val = max(diff.values())
            bests_act_val = [(act, val) for act, val in diff.items()
                             if abs(max_val - val) <= self.prob*abs(max_val)]
            
            if not bests_act_val:
                self.reason="AGOTAMIENTO DE ACCIONES"
                break

            act, val = choice(bests_act_val)
            neightbour = Node(problem.result(actual.state, act), actual.value + val)
            tabu.append(neightbour.state)
            if best.value < neightbour.value:
                best = neightbour

            actual = neightbour

        self.tour = best.state
        self.value = best.value
        end = time()
        self.time = end-start


    def solve_act_(self, problem: TSP):
        start = time()

        actual = Node(problem.init, problem.obj_val(problem.init))
        best = actual
        tabu = deque(maxlen=self.max_len)
        no_improvements_counter = 0

        while True:
            if no_improvements_counter > len(problem.init)*10:
                self.reason="FALTA DE MEJORAS"
                break

            # No puede quedarse iterando indefinidamente, por lo que se le agrega
            # otra parada.
            if self.niters > len(problem.init)*30:
                self.reason="EXCESO DE ITERACIONES"
                break

            self.niters += 1
            diff = problem.val_diff(actual.state)

            # filtramos aquellas que no estén en la lista tabú
            diff = {act: val for act, val in diff.items() if act not in tabu}

            # buscamos el mejor score disponible
            max_val = max(diff.values())
            
            # tomamos todas las acciones posibles que estén como máximo a una 
            # distancia del 5% del score máximo. así, permitimos aumentar el 
            # espacio de estados potencial a explorar, permitiendo recorrer más
            # caminos subóptimos (simil, Gradiente Estocástico)
            bests_act_val = [(act, val) for act, val in diff.items()
                             if abs(max_val - val) <= self.prob*abs(max_val)]

            # de no haber acciones disponibles, sale.
            # generalmente ocacionado por la cantidad de restricciones en la lista tabu.
            if not bests_act_val:
                self.reason="AGOTAMIENTO DE ACCIONES"
                break

            # elegimos una acción al azar
            act, val = choice(bests_act_val)
            neightbour = Node(problem.result(actual.state, act), actual.value + val)

            if (best.value - neightbour.value)/best.value < self.improv_treshold:
                no_improvements_counter += 1

            # si el score del estado es mejor, reemplazamos el mejor por el vecino.
            if best.value < neightbour.value:
                best = neightbour

            # insertamos la accion contraria
            if self.use == "mismo":
                tabu.append(act)
            elif self.use == "reverso":
                tabu.append(act[::-1])
            elif self.use == "ambos":
                tabu.append(act)
                tabu.append(act[::-1])
            else:
                raise ValueError("use debe ser 'mismo', 'reverso' o 'ambos'")

            actual = neightbour

        self.tour = best.state
        self.value = best.value
        end = time()
        self.time = end-start

class TabuReset(LocalSearch):
    """Algoritmo Tabú con reinicio aleatorio.
    exactamente igual al HillClimbingReset pero instanciando con la clase Tabu
    """

    def solve(self, problem: TSP, attempts = 10):
        start = time()
        self.value = float("-inf")

        for _ in range(attempts):
            solution = Tabu()
            solution.solve(problem)
            problem.random_reset()
            self.niters += solution.niters
            if self.value < solution.value:
                self.tour = solution.tour
                self.value = solution.value
        
        self.time = time()-start