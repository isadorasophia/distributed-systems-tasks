CC	   = gcc
CFLAGS =
K 	   = 4
N      = 64
export K

all: seq mt mp

seq: seq.c
	$(CC) $(FLAGS) $< -o $@

mt: mt.c
	$(CC) -DK=$(K) $(FLAGS) $< -o $@ -fopenmp

mp: mp.c
	$(CC) -DK=$(K) $(FLAGS) $< -o $@ -lrt

clean:
	rm -rf seq mt mp
