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

    def solve(self, problem: TSP):
        start = time()

        actual = Node(problem.init, problem.obj_val(problem.init))
        best = actual
        # Creamos una lista tabu que solo pueda guardar una cantidad limite de acciones, de modo tal,
        # de no privar al metodo de explorar acciones pasadas que puedan ser convinientes en
        # estados mas recientes.
        # este valor es arbitrario y empirico de correrlo sobre varios recorridos.
        tabu = deque(maxlen=len(problem.init)//5)
        # contador para terminar el algoritmo en caso de que no se haya encontrado mejoras, 
        # un numero determinado de veces
        no_improvements_counter = 0

        while True:
            # criterio de parada arbitrario modulado por el numero de puntos
            if no_improvements_counter > len(problem.init)//3:
                break

            # No puede quedarse iterando indefinidamente, por lo que se le agrega
            # otra parada.
            if self.niters > len(problem.init)*5:
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
                             if abs(max_val - val) <= 0.05*abs(max_val)]

            # de no haber acciones disponibles, sale.
            # generalmente ocacionado por la cantidad de restricciones en la lista tabu.
            if not bests_act_val:
                break

            # elegimos una acción al azar
            act, val = choice(bests_act_val)
            neightbour = Node(problem.result(actual.state, act), actual.value + val)

            # si, nuestro estado vecino, no mejora en 0.01% nuestro score, 
            # se considera que no aportó mejora significativa.
            if (best.value - neightbour.value)/best.value < 1e-4:
                no_improvements_counter += 1

            # si el score del estado es mejor, reemplazamos el mejor por el vecino.
            if best.value < neightbour.value:
                best = neightbour

            # insertamos la acción en la lista tabú para evitar caminos ciclicos/redundantes
            tabu.append(act)
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