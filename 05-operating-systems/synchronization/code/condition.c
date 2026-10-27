/* One-slot buffer: every access to slot/full/stopping is protected by mutex. */
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <threads.h>

struct Buffer {
    mtx_t mutex;
    cnd_t changed;
    bool full, stopping;
    unsigned slot, sum, producer_waits, consumer_waits;
};

static void require_success(int result) {
    if (result != thrd_success) {
        fputs("C11 thread operation failed\n", stderr);
        abort();
    }
}

static int producer(void *argument) {
    struct Buffer *b = argument;
    for (unsigned value = 1; value <= 100; ++value) {
        require_success(mtx_lock(&b->mutex));
        while (b->full && !b->stopping) {
            b->producer_waits++;
            require_success(cnd_wait(&b->changed, &b->mutex));
        }
        if (b->stopping) { require_success(mtx_unlock(&b->mutex)); return 1; }
        b->slot = value; b->full = true;
        require_success(cnd_broadcast(&b->changed));
        require_success(mtx_unlock(&b->mutex));
    }
    return 0;
}

static int consumer(void *argument) {
    struct Buffer *b = argument;
    for (unsigned expected = 1; expected <= 100; ++expected) {
        require_success(mtx_lock(&b->mutex));
        while (!b->full && !b->stopping) {
            b->consumer_waits++;
            require_success(cnd_wait(&b->changed, &b->mutex));
        }
        if (b->stopping) { require_success(mtx_unlock(&b->mutex)); return 1; }
        if (b->slot != expected) abort();
        b->sum += b->slot; b->full = false;
        require_success(cnd_broadcast(&b->changed));
        require_success(mtx_unlock(&b->mutex));
    }
    return 0;
}

int main(void) {
    struct Buffer buffer = { .full = false, .stopping = false, .sum = 0,
                             .producer_waits = 0, .consumer_waits = 0 };
    if (mtx_init(&buffer.mutex, mtx_plain) != thrd_success) return 2;
    if (cnd_init(&buffer.changed) != thrd_success) {
        mtx_destroy(&buffer.mutex); return 2;
    }
    thrd_t first, second;
    if (thrd_create(&first, producer, &buffer) != thrd_success) {
        cnd_destroy(&buffer.changed); mtx_destroy(&buffer.mutex); return 2;
    }
    if (thrd_create(&second, consumer, &buffer) != thrd_success) {
        require_success(mtx_lock(&buffer.mutex));
        buffer.stopping = true;
        require_success(cnd_broadcast(&buffer.changed));
        require_success(mtx_unlock(&buffer.mutex));
        require_success(thrd_join(first, NULL));
        cnd_destroy(&buffer.changed); mtx_destroy(&buffer.mutex); return 2;
    }
    int producer_status = 1, consumer_status = 1;
    require_success(thrd_join(first, &producer_status));
    require_success(thrd_join(second, &consumer_status));
    if (producer_status || consumer_status || buffer.sum != 5050 || buffer.full) abort();
    printf("{\"kind\":\"actual C11 one-slot buffer\",\"items\":100,\"sum\":%u,"
           "\"producer_waits\":%u,\"consumer_waits\":%u,\"empty_after_join\":true}\n",
           buffer.sum, buffer.producer_waits, buffer.consumer_waits);
    cnd_destroy(&buffer.changed); mtx_destroy(&buffer.mutex);
    return 0;
}
