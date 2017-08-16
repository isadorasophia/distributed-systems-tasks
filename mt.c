#include "common.h"

/* multithread libraries */
#include <omp.h>

#define K 4

int main(int argc, char* argv[]) {

    /* Validate input */
    if (argc != 2) {
        usage();
        error("Incorrect arguments!");
    }

    int64_t *arr, elapsed_time,
            avg = 0;

    struct timespec start, end;
    clock_gettime(CLOCK_REALTIME, &start);

    /* Assume we get a valid integer 
     *  (no overflow or conversion errors):
     *  - creates array of size N * 2^{20} of 64 bits */
    int32_t N = atoi(argv[1]),
            size = N * (1 << 20);

    arr = malloc(size * sizeof(int64_t));

    /* allocate random numbers */
    #pragma omp parallel num_threads(K)
    {
        /* random seed */
        int32_t seed = time(NULL) ^ omp_get_thread_num();

        #pragma omp for schedule(static) reduction(+:avg)
        for (int32_t i = 0; i < size; ++i) {
            arr[i] = rand_r(&seed) % LIMIT;
            avg += arr[i];
        }
    }

    clock_gettime(CLOCK_REALTIME, &end);
    elapsed_time = MILLISEC(end) - MILLISEC(start);

    double res = (double)avg/size;
    fprintf(stdout, "Average: %lf\nElapsed time: %ldms\n", res, elapsed_time);

    free(arr);

    return 0;
}