"""Modulo principal.

Autor: Mauro Lucci.
Fecha: 2023.
Materia: Prog3 - TUIA
"""

import parse
import load
import search
import plot
import problem

# Algoritmos involucrados
HILL_CLIMBING = "hill"
HILL_CLIMBING_RANDOM_RESET = "hill_r"
TABU_SEARCH = "tabu"
TABU_RESET = "tabu_r"
ALGO_NAMES = [HILL_CLIMBING, HILL_CLIMBING_RANDOM_RESET, TABU_SEARCH, TABU_RESET]


def main() -> None:
    """Funcion principal."""
    # Parsear los argumentos de la linea de comandos
    args = parse.parse()

    # Leer la instancia
    G, coords = load.read_tsp(args.filename)
    print(args.filename)

    # Construir la instancia de TSP
    p = problem.TSP(G)
    p.random_reset()
    # queremos repetir el mismo estado inicial para todos los algoritmos.
    intial_state = list(p.init)

    # Construir las instancias de los algoritmos
    algos = {
        HILL_CLIMBING: search.HillClimbing(),
        HILL_CLIMBING_RANDOM_RESET: search.HillClimbingReset(),
        TABU_SEARCH: search.Tabu(),
        TABU_RESET: search.TabuReset(),
    }

    # Resolver el TSP con cada algoritmo
    for algo in algos.values():
        print("Starting", algo.__class__.__name__)
        # asignamos una copia del estado inicial para evitar que el 
        # `.random_reset()` de los algoritmos con reset, muten mi estado inicial.
        p.init = list(intial_state)
        algo.solve(p)

    # Mostrar resultados por linea de comandos
    print("Valor:", "Tiempo:", "Iters:", "Algoritmo:", sep="\t\t")
    for name, algo in algos.items():
        print(algo.value, "%.2f" % algo.time, algo.niters, name, sep="\t\t")

    # Graficar los tours
    tours = {}
    tours['init'] = (intial_state, p.obj_val(intial_state))  # estado inicial

    for name, algo in algos.items():
        tours[name] = (algo.tour, algo.value)
    plot.show(G, coords, args.filename, tours)


if __name__ == "__main__":
    main()
