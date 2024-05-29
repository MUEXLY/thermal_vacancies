hello:
	echo "Hello world!"

clean:
	rm outputs/*; \
	rm log.lammps; \
	rm ins_cantor.o*; \
	rm trash/*; \
	rm -r venv/

python = python
venv:
	${python} -m venv venv; \
	venv/bin/pip install -r requirements.txt

executable = ./lmp
num_procs = 16
run:
	OMP_NUM_THREADS=1 mpirun -np ${num_procs} ${executable} -in insertions.in

analyze: outputs/occupying_energy.txt outputs/vacant_energy.txt outputs/enthalpy.txt
	venv/bin/python vacancy_concentration.py

plot: outputs/concentration.txt
	venv/bin/python concentration_plot.py