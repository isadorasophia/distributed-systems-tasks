#include "common.h"

/* multiprocess library */
#include <sys/mman.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <sys/file.h>

#include <unistd.h>
#include <fcntl.h>

#ifndef K
    #define K 4
#endif

#define ARR_MEM "arr_mem"
#define ACC_MEM "acc_mem"

void* create_shmem(const char* name, int size, int* fd) {
    *fd = shm_open(name, O_RDWR | O_CREAT, S_IRUSR | S_IWUSR);
    if (ftruncate(*fd, size * sizeof(int64_t)) != 0) {
        error("Unable to allocate memory.");
    }

    return mmap(NULL, size * sizeof(int64_t), 
        PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANONYMOUS, *fd, 0);
}

int main(int argc, char* argv[]) {

    /* Validate input */
    if (argc != 2) {
        usage();
        error("Incorrect arguments!");
    }

    /* clock settings */
    struct timespec start, end;
    int64_t elapsed_time;

    /* Assume we get a valid integer 
     *  (no overflow or conversion errors):
     *  - creates array of size N * 2^{20} of 64 bits */
    int32_t N = atoi(argv[1]),
            size = N * (1 << 20);

    /* access to shared memory */
    int32_t arr_fd, avg_fd;
    int64_t* arr = create_shmem(ARR_MEM, size, &arr_fd);
    int64_t* avg = create_shmem(ACC_MEM, 1, &avg_fd);

    int32_t chunk = size/K, remaining = size % K;
    pid_t pids[K];

    clock_gettime(CLOCK_REALTIME, &start);

    for (int32_t k = 0; k < K; k++) {
        pids[k] = fork();

        switch (pids[k]) {
            case -1: /* error */
                error("Unable to fork!");

            case 0:  /* child process */
                srand(time(NULL) ^ pids[k]);

                /* get our private chunk settings */
                int32_t mem_start = chunk * k;
                int32_t mem_end = mem_start+chunk;

                int32_t local_avg = 0;

                /* if we are the last chunk, get any remaining memory */
                if (k == K-1) mem_end += size % K;

                /* do our work! */
                for (int32_t i = mem_start; i < mem_end; ++i) {
                    arr[i] = rand() % LIMIT;
                    local_avg += arr[i];
                }

                /* add to our current average */
                flock(avg_fd, LOCK_EX);
                *avg += local_avg;
                flock(avg_fd, LOCK_UN);

                return 0;

            default: /* parent process */
                break;
        }
    }

    /* wait for all our children */
    for (int32_t k = 0; k < K; k++) {
        int32_t status = 0;
        while (-1 == waitpid(pids[k], &status, 0));

        if (status != 0) {
            error("One of our children failed!");
        }
    }

    /* get finish time */
    clock_gettime(CLOCK_REALTIME, &end);
    elapsed_time = MILLISEC(end) - MILLISEC(start);

    /* output answer */
    double res = (double)(*avg)/size;
    fprintf(stdout, "Average output: %lf\n\
Elapsed time for MULTIPROCESS application with K=%d: %ldms\n", res, K, elapsed_time);

    /* clean up our mess */
    shm_unlink(ARR_MEM);
    shm_unlink(ACC_MEM);

    return 0;
}
