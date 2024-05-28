hello:
	echo "Hello world!"

clean:
	rm outputs/*; \
	rm log.lammps; \
	rm ins_cantor.o*; \
  rm trash/*