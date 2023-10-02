from application import AliceProgram, BobProgram
from squidasm.run.stack.config import StackNetworkConfig
from squidasm.run.stack.run import run
# from optimisation import angle
import optimisation

import numpy as np
import time

# default value
# angle = 1 

# import network configuration from file
cfg = StackNetworkConfig.from_file("config.yaml")


# Create instances of programs to run
alice_program = AliceProgram()
bob_program = BobProgram()

simulation_iterations = 200

def cost():
    # Run the simulation. Programs argument is a mapping of network node labels to programs to run on that node
    results_alice, results_bob = run(config=cfg,
    programs={"Alice": alice_program, "Bob": bob_program},
    num_times=simulation_iterations)
    # print(results_alice)

    # results have List[Dict[]] structure. List contains the simulation iterations
    results_alice = [results_alice[i]["measurement"] for i in range(simulation_iterations)]
    results_bob = [results_bob[i]["measurement"] for i in range(simulation_iterations)]

    # Print the elapsed time
    # print("**********FINISHED**************")
    # print("Simulation time:", elapsed_time, "seconds")

    errors = [result_alice != 0 and result_bob !=0 for result_alice, result_bob in zip(results_alice, results_bob)]

    # print(f"average error rate: {sum(errors) / len(errors) * 100: .1f}% using {len(errors)} requests")
    res = sum(errors) / len(errors)
    # print("Result = ", res)

    return res

def cost_function(_angle):
    # global angle 
    optimisation.angle = _angle
    # from run_simulation import cost 
    return cost()

from scipy.optimize import minimize 

progress = []
def callback(xk):
    print("ANGLE ", xk)  
    res = cost_function(xk)
    progress.append(res)
    print("Iteration ", len(progress),": C =  ", res)

def optimisation(coef):
    out = minimize(cost_function, 
               x0=coef, 
               method="COBYLA", 
               callback=callback,
               options={'maxiter':200})
    return out

coef = 1


# Capture the start time
start_time = time.time()

opt_angle = optimisation(coef)

# Capture the end time
end_time = time.time()

# Calculate the elapsed time
elapsed_time = end_time - start_time

print("FINAL ANGLE IS ", opt_angle, "TIME: ", elapsed_time)