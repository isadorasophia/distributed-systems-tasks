CC	= gcc
CFLAGS	=
K	= 4
N	= 64
export K

all: seq mt mp

seq: seq.c
	$(CC) $(FLAGS) $< -o $@

mt: mt.c
	$(CC) -DK=$(K) $(FLAGS) $< -o $@ -fopenmp

mp: mp.c
	$(CC) -DK=$(K) $(FLAGS) $< -o $@ -lrt

# run our three applications and report its time (as their output)
run: clean seq mt mp
	@echo "\033[1;34mExecuting sequential application for N=$(N):\033[0m"
	@echo "./seq $(N)" | bash
	@echo "\033[1;34mExecuting multithread application for N=$(N):\033[0m"
	@echo "./mt $(N)" | bash
	@echo "\033[1;34mExecuting multiprocess application for N=$(N):\033[0m"
	@echo "./mp $(N)" | bash

clean:
	rm -rf seq mt mp
