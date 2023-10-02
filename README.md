# distributed_quantum_algorithms
Algorithms for optimization problems implemented on a distributed manner with packages by QuTech. 

## Installation of required software

Linux/macOS is required. I used Linux. During the installation it might be possible to change the current version of Python, so I strongly recommend to do the installation in a new environment like `conda` for example.

In order to install `netqasm` package simply perform: 
```
pip install netqasm
```
The detailed instructions are here: https://netqasm.readthedocs.io/en/latest/installation.html#installation


But the implementation of distributed quantum algorithms ine also needs to install a simulator. 
To this end, you need to install `netsquid` package first 

```
pip install netsquid
``` 
and then register on the NetSquid forum https://netsquid.org/#registration. Once you have your credentials, it becomes possible to install `squidasm` package:

```
pip install squidasm --extra-index-url=https://{netsquid-user-name}:{netsquid-password}@pypi.netsquid.org
```

Note that there is also `simulaqron` simulator, which can not be used for optimization tasks since it is very slow.

Sometimes, some packages need to be reinstalled with older versions, in my case there were problems with `matplotlib` and `numpy`. For the issues I made the following: 
```
pip install --force-reinstall matplotlib==3.4
pip install --force-reinstall numpy==1.18.0
```

## Repository content 

The repository contains building blocks for creating distributed quantum optimization algorithms: `CNOT`, `RZZ`, `RXX`,`RYY` gates. In all cases two quantum devices were used. Moke optimization algorithm is shown in `RYY_OPT`.
The solving of MAXCUT optimization problem can be found in `MAX_CUT`. 

## Max-Cut problem 

The Maximum Cut Problem is a well-known combinatorial optimization problem in graph theory, where the goal is to partition the vertices of a given graph into two sets such that the number of edges crossing the partition (belonging to different sets) is maximized. It is an NP-hard problem with applications in various fields, including network design and image segmentation.

In this repository, one can find the Max-Cut solution for the following graph: 

![graph](https://github.com/VasilyBokov/distributed_quantum_algorithms/assets/62181457/98cf22f6-9595-40a2-9088-e0799eaaf2f4)


The Quantum Approximate Optimization Algorithm (QAOA) is a quantum computing algorithm designed to tackle combinatorial optimization problems like the Max-Cut problem. The description of how to implement the QAOA algorithm for the Max-Cut problem can be found here: 
 https://qiskit.org/ecosystem/optimization/tutorials/06_examples_max_cut_and_tsp.html

The algorithm involves the construction of a parameterized quantum circuit. Here's a simplified description of the circuit used for QAOA in the Max-Cut problem:

1. **Initialization**: Start with an equal superposition of all possible states of the qubits in the circuit.

2. **Cost Hamiltonian Operator**: Apply a sequence of operators that correspond to the cost (objective) function of the Max-Cut problem. These operators are usually designed to promote the desired partitioning of the graph's vertices into two sets. This involves applying multi-qubit gates that depend on the graph's structure and the parameters of the algorithm.

3. **Mixing Hamiltonian Operator**: Apply a sequence of operators that correspond to a mixing Hamiltonian. This mixing operator helps explore different partitions of the graph's vertices. Typically, it's a simple operator like the sum of Pauli-X operators on all qubits.

4. **Repeat Steps 2 and 3**: Repeatedly apply the cost and mixing Hamiltonians for a fixed number of iterations, each time adjusting the parameters that control the Hamiltonians. These parameters are optimized to find the best partitioning solution.

5. **Measurement**: After running the circuit for a sufficient number of iterations, perform measurements on the qubits. The measurement results are used to estimate the quality of the partition found by the algorithm.

6. **Classical Optimization**: Finally, use classical optimization techniques to adjust the parameter values in a way that maximizes the objective function (Max-Cut value). This optimization process can be performed using methods like gradient descent or more specialized algorithms.

For the shown graph the circuit's construction is as follows: 

![circuit](https://github.com/VasilyBokov/distributed_quantum_algorithms/assets/62181457/fc3dc2f9-abff-4f14-b118-6a7aedeb251e)

In the distributed implementation the qubits 0 and 1 are located on the device "Alice", while 2
 and 3 qubits on the device "Bob". Therefore, the rotations for pairs: (0,2), (1,3) should be performed in a distributed manner. 

The `MAXCUT` program contains one additional file `angle_value.py` with the rotational angles which are optimized in the algorithm. The circuit structure is described in the `application.py'` file. In order to change the number of qubits being used one should open `config.yaml` and set the needed number.

To run the program one should open the required environment with `conda activate your_env` and then run the program file by `python 'run_simulation.py'`. After the optimization, the final distribution of measurements will be obtained. The histogram for such a distribution is shown below: 

![distr](https://github.com/VasilyBokov/distributed_quantum_algorithms/assets/62181457/5c0e86dd-eca8-41e9-b5e5-11295ddc9823)


