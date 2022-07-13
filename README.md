# WCLL modelling

Multiphysics modelling of WCLL breeder blanket geometries.


## To run FESTIM in Docker
The FEniCS project provides a [Docker image](https://hub.docker.com/r/fenicsproject/stable/) with FEniCS and its dependencies (python3, UFL, DOLFIN, numpy, sympy...)  already installed. See their ["FEniCS in Docker" manual](https://fenics.readthedocs.io/projects/containers/en/latest/).

Get Docker [here](https://www.docker.com/community-edition).

Pull the Docker image and run the container, sharing a folder between the host and container:

For Windows users:
```python
docker run -ti -v ${PWD}:/home/fenics/shared --name fenics quay.io/fenicsproject/stable:latest
```

Install a FESTIM v0.10.0
```
pip install git+https://github.com/RemDelaporteMathurin/FESTIM@v0.10.0
```
To run the FESTIM simulations, first configure all simualtion paramters in the file `parameters.py`. Then follow the work flow of heat transfer --> fluid dyanamics --> hydrogen transport, thus first run the file:
```
python3 solve_heat_transfer.py
```
then:
```
python3 solve_NS_submesh.py
```
then
```
python3 solve_H_transport.py
```
This will produce a bunch of .xdmf files and an excel derived_quantities file