# Enhanced Gaussian Process based on Particle Swarm Optimization

Informative path planning for monitoring systems based on meta-heuristic algorithm, Particle Swarm Optimization, and a surrogate model, Gaussian Process.

The main objective is to guide a swarm of autonomous surface vehicles to obtain a model of the water quality of the water resources.

## Installation

Please install the ```requirements.txt``` file before use.

```
pip install -r requirements.txt
```

Note: the last versions of scipy library produce errors. The version used in this code was 1.5.4

## Use

The [main](main.py) file contains the proposed algorithm. The hyperpameter optimization is in [Hyperparameter](Hyperparameter/hyper_opt.py).
