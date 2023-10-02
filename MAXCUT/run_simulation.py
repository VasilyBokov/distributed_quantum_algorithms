from application import AliceProgram, BobProgram
from squidasm.run.stack.config import StackNetworkConfig
from squidasm.run.stack.run import run
import angle_value

import numpy as np
import time

# import network configuration from file
cfg = StackNetworkConfig.from_file("config.yaml")


# Create instances of programs to run
alice_program = AliceProgram()
bob_program = BobProgram()

shots = 512

# Defining the graph topology for MAX-CUT
edges = [(0,1), (1,2), (2,3), (3,0)]

def counts(bitstring):
# Initialize an empty dictionary to store the counts
    bitstring_counts = {}

# Count the occurrences of each bitstring
    for x in bitstring:
        if x in bitstring_counts:
            bitstring_counts[x] += 1
        else:
            bitstring_counts[x] = 1
    return bitstring_counts 

def maxcut_obj(x, edges):
    """
    Given a bitstring as a solution, this function returns
    the number of edges shared between the two partitions
    of the graph.
    """
    obj = 0
    for i, j in edges:
        if x[i] != x[j]:
            obj -= 1
    return obj

def compute_expectation(counts):
    avg = 0
    sum_count = 0
    for bitstring, count in counts.items():
        obj = maxcut_obj(bitstring, edges)
        avg += obj * count
        sum_count += count

    return avg/sum_count


def cost():
    # Capture the start time
    start_time = time.time()

    # Run the simulation. Programs argument is a mapping of network node labels to programs to run on that node
    results_alice, results_bob = run(config=cfg,
    programs={"Alice": alice_program, "Bob": bob_program},
    num_times=shots)

    # results have List[Dict[]] structure. List contains the simulation iterations
    results_alice = [results_alice[i]["measurement"] for i in range(shots)]
    results_bob = [results_bob[i]["measurement"] for i in range(shots)]

    # Capture the end time
    end_time = time.time()

    # Calculate the elapsed time
    elapsed_time = end_time - start_time

    # Print the elapsed time
    print("**********FINISHED**************")
    print("Simulation time:", elapsed_time, "seconds")

    results = []
    for result_alice, result_bob in zip(results_alice, results_bob):
        results.append(str(result_alice[0]) + str(result_alice[1]) + str(result_bob[0])+ str(result_bob[1]))  
    res = compute_expectation(counts(results))
    # error = counts(results)['0000']/shots

    print("Result is ", res, "Counts:" ,counts(results))
    # print(error)
    return res

def cost_function(params):
    _gamma, _beta = params
    angle_value.gamma = _gamma
    angle_value.beta = _beta
    print(params)
    return cost()

from scipy.optimize import minimize


# res = minimize(cost_function, 
#                [1.0, 1.0], method='COBYLA')

# print(res)

cost_function((2,1))



