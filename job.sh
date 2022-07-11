#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --job-name="HT_272"
#SBATCH --output=output.txt
#SBATCH --error=error.txt
#SBATCH --cpus-per-task=1
#SBATCH --nodelist=node004

conda init bash
conda activate fenics-3.6.9 
                                          
mpirun -np 12 python3 solve_3D_H_transport.py
#python3 solve_3D_NS_submesh.py
