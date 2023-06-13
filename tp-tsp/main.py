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
import json

# Algoritmos involucrados
HILL_CLIMBING = "hill"
HILL_CLIMBING_RANDOM_RESET = "hill_r"
TABU_SEARCH = "tabu"
TABU_RESET = "tabu_r"
ALGO_NAMES = [HILL_CLIMBING,
              HILL_CLIMBING_RANDOM_RESET, TABU_SEARCH, TABU_RESET]


def main() -> None:
    """Funcion principal."""

    args = parse.parse()

    with open(args.config, "r") as f:
        conf_file = json.load(f)
        instance_file = conf_file["instance"]
        init_list = conf_file["problem_list"]
        problem_len = len(init_list[0][1])

    # Leer la instancia
    # create path to file tp-tsp\instances\burma14.tsp using pathlib

    
    G, coords = load.read_tsp(f'instances/{instance_file}')
    # print(args.filename)

    p = problem.TSP(G)
    metodo = args.metodo  # hill, "mismo", "reverso", "ambos"
    
    # cantidad_problemas=10
    # r=[p.random_reset() or list(p.init) for _ in enumerate(range(cantidad_problemas))]
    # pd.DataFrame.from_dict({"problem_n":list(range(len(r))),"inicio":r}).to_csv(f"{instance_file}-inicio.csv", index=False, sep=";")
    # exit()
    # Parsear los argumentos de la linea de comandos


    # starts = pd.read_csv("inicio.csv", sep=";")
    # init_list = [(n, json.loads(arr)) for n, arr in starts.values]

    df = pd.DataFrame()
    if metodo == "hill":
        for problem_n, init in init_list:
            p.init = list(init)
            algo = search.HillClimbing()
            algo.solve(p)
            df = pd.concat([
                df,
                pd.DataFrame.from_dict({
                    "algorithm": [algo.__class__.__name__],
                    "instance": [instance_file],
                    "instance_points": [problem_len],
                    "instance_problem": [problem_n],
                    "value": [algo.value],
                    "iters": [algo.niters],
                    "time": [algo.time],
                    "solution": [algo.tour],
                    "tabu_list_method": [np.nan],
                    "tabu_list_len": [np.nan],
                    "tabu_run": [np.nan],
                    "tabu_chance_prob": [np.nan],
                    "tabu_improv_treshold": [np.nan],
                    "tabu_improv_stop_mult": [np.nan],
                    "tabu_iter_stop_mult": [np.nan],
                    "tabu_exit": [np.nan],
                })])

    elif metodo in ["mismo", "reverso", "ambos", "estado"]:
        max_len_list = [np.nan]
        if metodo != "estado":
            max_len_list = set(conf_file["tabu"]["len_list"]["fixed"] +
                               [int(problem_len*n) for n in conf_file["tabu"]["len_list"]["proporcional"]])
            print(max_len_list)

        chance_prob_list = conf_file["tabu"]["chance_prob_list"]
        improv_treshold_list = conf_file["tabu"]["improv_treshold_list"]
        improv_treshold_proportional = conf_file["tabu"]["improv_treshold_proportional"]
        max_iter = conf_file["tabu"]["max_iter"]
        runs = conf_file["tabu"]["runs"]

        total = len(max_len_list)*len(chance_prob_list) * \
            len(improv_treshold_list)*len(init_list)*runs
        print("Cantidad total de iteraciones", total)
        contador = 0

        for max_len in max_len_list:
            for chance_prob in chance_prob_list:
                for improv_treshold in improv_treshold_list:
                    print(
                        f"Progreso: {contador}/{total} ({contador/total*100:.2f}%)")
                    for problem_n, init in init_list:
                        for i in range(runs):
                            algo = search.Tabu(
                                max_len=max_len,
                                prob=chance_prob,
                                improv_treshold=improv_treshold,
                                list_method=metodo,
                                improv_treshold_limit=improv_treshold_proportional,
                                max_iter=max_iter
                            )
                            p.init = list(init)
                            algo.solve(p)
                            df = pd.concat([df,
                                            pd.DataFrame.from_dict({
                                                "algorithm": [algo.__class__.__name__],
                                                "instance": [instance_file],
                                                "instance_points": [problem_len],
                                                "instance_problem": [problem_n],
                                                "value": [algo.value],
                                                "iters": [algo.niters],
                                                "time": [algo.time],
                                                "solution": [algo.tour],
                                                "tabu_list_method": [algo.tabu_list_method],
                                                "tabu_list_len":  [algo.tabu_list_len],
                                                "tabu_run": [i],
                                                "tabu_chance_prob": [algo.tabu_chance_prob],
                                                "tabu_improv_treshold": [algo.tabu_improv_treshold],
                                                "tabu_improv_stop_mult": [algo.improv_treshold_stop_mult],
                                                "tabu_iter_stop_mult": [algo.tabu_iter_stop_mult],
                                                "tabu_exit": [algo.reason],
                                            })])
                        contador += runs

    df.reset_index(drop=True, inplace=True)
    df.to_pickle(f"{args.config}-{metodo}.pkl")


if __name__ == "__main__":
    main()
    # import winsound
    # winsound.Beep(550, 1000)
    # winsound.Beep(330, 1000)
    # winsound.Beep(440, 2000)
    # winsound.Beep(550, 1000)
    # winsound.Beep(330, 1000)
