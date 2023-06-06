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
from search import LocalSearch
import pandas as pd
import numpy as np

# Algoritmos involucrados
HILL_CLIMBING = "hill"
HILL_CLIMBING_RANDOM_RESET = "hill_r"
TABU_SEARCH = "tabu"
TABU_RESET = "tabu_r"
ALGO_NAMES = [HILL_CLIMBING,
              HILL_CLIMBING_RANDOM_RESET, TABU_SEARCH, TABU_RESET]

def main() -> None:
    """Funcion principal."""
    # Parsear los argumentos de la linea de comandos
    args = parse.parse()

    # Leer la instancia
    G, coords = load.read_tsp(args.filename)
    print(args.filename)

    metodo = args.metodo  # hill, "mismo", "reverso", "ambos"
    starts = pd.read_csv("inicio.csv", sep=";")
    import json
    init_list = [(n, json.loads(arr)) for n, arr in starts.values]

    # p=problem.TSP(G)
    # r=[p.random_reset() or list(p.init) for _ in enumerate(range(25))]
    # pd.DataFrame.from_dict({"problem_n":list(range(len(r))),"inicio":r}).to_csv("inicio.csv", index=False, sep=";")


    if metodo == "hill":
        df = pd.DataFrame()
        p = problem.TSP(G)
        for problem_n, init in init_list:
            p.init = list(init)
            algo = search.HillClimbing()
            algo.solve(p)
            df = pd.concat([
                df,
                pd.DataFrame.from_dict({
                    "name": [algo.__class__.__name__],
                    "value": [algo.value],
                    "niters": [algo.niters],
                    "time": [algo.time],
                    "problem_n": [problem_n],
                    "tabu_iter":[np.nan],
                    "tabu_max_len":[np.nan],
                    "tabu_prob":[np.nan],
                    "tabu_improv_treshold":[np.nan],
                    "tabu_lista":[np.nan],
                    "tabu_salida":[np.nan],
                    "inicio": [p.init],
                    "solution": [algo.tour],
                })])
        df.reset_index(drop=True, inplace=True)
        df.to_pickle("hill.pkl")

    elif metodo in ["mismo", "reverso", "ambos", "estado"]:
        iterar_sobre=[np.nan]
        if metodo!="estado":
            prob_len=len(init_list[0][1])
            iterar_sobre = set([1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                            prob_len//2, prob_len//3, prob_len//4,
                            prob_len//5, prob_len//6, prob_len//7,
                            prob_len//8, prob_len//9, prob_len//10])

        print(iterar_sobre)
        veces=10
        df = pd.DataFrame()
        p = problem.TSP(G)

        for max_len in iterar_sobre:
            for prob in [0, 1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1]:
                for improv_treshold in [1e-5, 1e-4, 1e-3, 1e-2, 1e-1]:
                    print(max_len, prob, improv_treshold)
                    # print("Valor:", "Tiempo:", "Iters:", "Algoritmo:", sep="\t\t")
                    # Resolver el TSP con cada algoritmo
                    for problem_n, init in init_list:
                        for i in range(veces):
                            algo = search.Tabu(max_len=max_len, prob=prob, improv_treshold=improv_treshold, use=metodo)
                            p.init = list(init)
                            algo.solve(p)
                            df = pd.concat([df,
                                            pd.DataFrame.from_dict({
                                                "name": [algo.__class__.__name__],
                                                "value": [algo.value],
                                                "niters": [algo.niters],
                                                "time": [algo.time],
                                                "problem_n": [problem_n],
                                                "tabu_iter": [i],
                                                "tabu_max_len":  [algo.max_len],
                                                "tabu_prob": [algo.prob],
                                                "tabu_improv_treshold": [algo.improv_treshold],
                                                "tabu_lista": [algo.use],
                                                "tabu_salida": [algo.reason],
                                                "inicio": [p.init],
                                                "solution": [algo.tour],
                                            })])
        df.reset_index(drop=True, inplace=True)
        df.to_pickle(f"{metodo}.pkl")


if __name__ == "__main__":
    main()
    # import winsound
    # winsound.Beep(550, 1000)
    # winsound.Beep(330, 1000)
    # winsound.Beep(440, 2000)
    # winsound.Beep(550, 1000)
    # winsound.Beep(330, 1000)
