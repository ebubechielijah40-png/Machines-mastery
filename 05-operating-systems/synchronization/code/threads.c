/* Defined C11 experiment: each individual split access is atomic, but the
 * load-plus-store algorithm can still lose an increment. No data-racy int demo.
 */
#include <assert.h>
#include <stdatomic.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <threads.h>

enum Mode { SPLIT, FETCH_ADD, WHOLE_LOCK };
struct Shared {
    atomic_uint counter, ready;
    atomic_bool go;
    mtx_t mutex;
    unsigned plain, loaded[2];
    enum Mode mode;
};
struct Argument { struct Shared *shared; unsigned index; };

static int worker(void *argument) {
    struct Argument *a = argument;
    struct Shared *s = a->shared;
    unsigned local = 0;
    if (s->mode == SPLIT) {
        local = atomic_load(&s->counter);
        s->loaded[a->index] = local;
    }
    atomic_fetch_add(&s->ready, 1);
    while (!atomic_load(&s->go)) thrd_yield();
    if (s->mode == SPLIT) {
        atomic_store(&s->counter, local + 1);
    } else if (s->mode == FETCH_ADD) {
        s->loaded[a->index] = atomic_fetch_add(&s->counter, 1);
    } else {
        if (mtx_lock(&s->mutex) != thrd_success) return 1;
        s->loaded[a->index] = s->plain;
        s->plain += 1;
        if (mtx_unlock(&s->mutex) != thrd_success) return 1;
    }
    return 0;
}

static int run_case(enum Mode mode, unsigned *result, unsigned loaded[2]) {
    struct Shared shared;
    atomic_init(&shared.counter, 0);
    atomic_init(&shared.ready, 0);
    atomic_init(&shared.go, false);
    shared.plain = 0;
    shared.mode = mode;
    shared.loaded[0] = shared.loaded[1] = 0;
    if (mtx_init(&shared.mutex, mtx_plain) != thrd_success) return 1;
    thrd_t threads[2];
    struct Argument arguments[2] = {{&shared, 0}, {&shared, 1}};
    unsigned created = 0;
    for (; created < 2; ++created) {
        if (thrd_create(&threads[created], worker, &arguments[created]) != thrd_success)
            break;
    }
    if (created == 2) {
        /* Both split loads precede ready==2, and all stores follow go. */
        while (atomic_load(&shared.ready) != 2) thrd_yield();
    }
    atomic_store(&shared.go, true); /* Also release a partially created pair. */
    int failed = created != 2;
    for (unsigned i = 0; i < created; ++i) {
        int status = 1;
        if (thrd_join(threads[i], &status) != thrd_success) abort();
        if (status != 0) failed = 1;
    }
    *result = mode == WHOLE_LOCK ? shared.plain : atomic_load(&shared.counter);
    loaded[0] = shared.loaded[0]; loaded[1] = shared.loaded[1];
    mtx_destroy(&shared.mutex);
    return failed;
}

int main(void) {
    const char *names[] = {"split_atomic_load_store", "atomic_fetch_add", "whole_mutex"};
    printf("{\"kind\":\"actual C11 thread executions\",\"cases\":[");
    for (unsigned mode = 0; mode < 3; ++mode) {
        unsigned result = 0, loaded[2] = {0, 0};
        for (unsigned iteration = 0; iteration < 20; ++iteration) {
            if (run_case((enum Mode)mode, &result, loaded)) {
                fprintf(stderr, "thread or mutex operation failed\n");
                return 2;
            }
            assert(result == (mode == SPLIT ? 1u : 2u));
            if (mode == SPLIT) assert(loaded[0] == 0 && loaded[1] == 0);
        }
        printf("%s{\"mode\":\"%s\",\"executions\":20,\"last_observed_value\":%u,"
               "\"last_loaded_values\":[%u,%u]}", mode ? "," : "", names[mode],
               result, loaded[0], loaded[1]);
    }
    printf("]}\n");
    return 0;
}
