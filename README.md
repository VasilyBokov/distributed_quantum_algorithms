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



