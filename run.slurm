#!/bin/bash --login
#
# Parallel script produced by bolt
#        Resource: ARCHER2 (HPE Cray EX (128-core per node))
#    Batch system: Slurm
#
# bolt is written by EPCC (http://www.epcc.ed.ac.uk)
#

## Number of 128 core nodes
#SBATCH --nodes=2

## Number of tasks per node
#SBATCH --tasks-per-node=128

#SBATCH --job-name=spherical_dns
#SBATCH --account=n03-lds1
#SBATCH --partition=standard
#SBATCH --qos=long
#SBATCH --time=48:00:00

## Ensure correct modules are loaded
#module load epcc-job-env

module -s restore /etc/cray-pe.d/ProgEnv-cray
module load cray-fftw
module load cray-hdf5-parallel
module load cray-netcdf-hdf5parallel

## Ensure there is no threading
export OMP_NUM_THREADS=1

# Run the parallel program
srun --distribution=block:block --hint=nomultithread --unbuffered ./main.out > OUT
