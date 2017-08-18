#include "common.h"

int main(int argc, char* argv[]) {

    /* Validate input */
    if (argc != 2) {
        usage();
        error("Incorrect arguments!");
    }

    uint64_t *arr, avg = 0;
	int64_t elapsed_time;

    struct timespec start, end;
    clock_gettime(CLOCK_REALTIME, &start);

    /* random seed */
    srand(time(NULL));

    /* Assume we get a valid integer 
     *  (no overflow or conversion errors):
     *  - creates array of size N * 2^{20} of 64 bits */
    int32_t N = atoi(argv[1]),
            size = N * (1 << 20);

    arr = malloc(size * sizeof(uint64_t));

    /* allocate random numbers */
    for (int32_t i = 0; i < size; ++i) {
        arr[i] = rand() % LIMIT;
        avg += arr[i];
    }

    clock_gettime(CLOCK_REALTIME, &end);
    elapsed_time = MILLISEC(end) - MILLISEC(start);

    double res = (double)avg/size;
    fprintf(stdout, "Average output: %lf\n\
Elapsed time for SEQUENTIAL application: %ldms\n", res, elapsed_time);

    free(arr);

    return 0;
}
