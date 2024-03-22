# Instructions for setting up Eddie for TensorFlow-Probability

https://www.wiki.ed.ac.uk/display/ResearchServices/Quickstart

- You'll need to be logged into the university VPN if not using eduroam.

- You have only 10GB storage in your home directory. You have a scratch space which you can use for most stuff, but be aware that files there get deleted automatically after some time, and back them up somewhere.

- Follow the steps below to create a virtual environment with the main libraries you'll need. You can install other things like matplotlib, etc. yourself afterwards using `conda install <package_name>`.


        module load anaconda
        conda config --add envs_dirs /exports/eddie/scratch/<uun>/anaconda/envs
        conda config --add pkgs_dirs /exports/eddie/scratch/<uun>/anaconda/pkgs

- To be safe you should also check (using a text editor like vim, or through vs code) the .condarc file in your home directory and delete any other directories listed as envs_dir or pkgs_dir.

        qlogin -l h_vmem=4G
        module load anaconda
        conda create -n plankton
        conda activate plankton
        conda install pip
        pip install tensorflow[and-cuda]==2.14
        pip install tensorflow-probability==0.22.1
