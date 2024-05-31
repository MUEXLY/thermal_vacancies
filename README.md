# thermal_vacancies

This repository computes the concentration of vacancies in an arbitrary crystalline system under thermal conditions using LAMMPS using our paper on impurity concentration [here](https://arxiv.org/abs/2402.07324).

The main piece of code is the LAMMPS input file, which performs various atom swaps at each lattice site. To run the example in this repository (concentration in Fe-9%Cr):

```bash
git clone https://github.com/MUEXLY/thermal_vacancies
make venv # make a python venv with necessary libraries
make run # run LAMMPS input file
make analyze # parse data spit out by LAMMPS
make plot # plot the data
```
