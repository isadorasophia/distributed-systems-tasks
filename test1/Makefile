CC	   = gcc
CFLAGS =

all: seq mt mp

seq: seq.c
	$(CC) $(FLAGS) $< -o $@

mt: mt.c
	$(CC) $(FLAGS) $< -o $@ -fopenmp

mp: mp.c
	$(CC) $(FLAGS) $< -o $@ -lrt

clean:
	rm -rf seq mt mp
