#!/bin/sh
# Grid Engine options (lines prefixed with #$)

# Name of job
#$ -N m_brolly
# Directory in which to run code (-cwd or -wd <path-to-wd>)
#$ -cwd
# Requested runtime allowance
#$ -l h_rt=00:20:00
# Requested number of cores in gpu parallel environment
#$ -pe gpu 1
# Requested memory per core
#$ -l h_vmem=16G
# Email address for notifications
#$ -M m.brolly@ed.ac.uk
# Option to request resource reservation
#$ -R y

# Initialise the environment modules
. /etc/profile.d/modules.sh

# Load conda
module load anaconda
# Activate conda environment
source activate ml

# Run the program
python test.py

