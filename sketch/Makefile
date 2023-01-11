CC=gcc
CFLAGS=-I.

all: sketch sketch_diffval sketch_unroll 

sketch: sketch.o
	$(CC) -O3 -o sketch sketch.o

sketch_diffval: sketch_diffval.o
	$(CC) -O3 -o sketch_diffval sketch_diffval.o

sketch_unroll: sketch_unroll.o
	$(CC) -O3 -o sketch_unroll sketch_unroll.o

clean:
	rm -f *.o sketch sketch_diffval sketch_unroll