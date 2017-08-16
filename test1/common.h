#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>
#include <stdint.h>

#define LIMIT 1000
#define MILLISEC(d) (int64_t)(d.tv_sec*1000 + d.tv_nsec / 1.0e6)

void error(const char* msg) {
    char* tag = "ERROR";

    fprintf(stderr, "[%s] %s\n", tag, msg);
    exit(1);
}

void usage() {
    const char* msg = "Usage:\n\tmy_program n_size\n";

    fprintf(stdout, "%s", msg);
}
