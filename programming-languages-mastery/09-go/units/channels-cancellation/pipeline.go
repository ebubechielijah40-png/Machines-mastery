// Package pipeline implements a finite, owned-input, cancellation-aware work stream.
package pipeline

import (
    "context"
    "errors"
    "sync"
)

type Result struct { Index int; Square int64 }
type Stream struct { Results <-chan Result; Done <-chan struct{} }
type job struct { index int; value int64 }

// Start snapshots input before spawning. The caller must not mutate input concurrently
// with this call. The consumer must drain Results or cancel ctx, then await Done.
func Start(ctx context.Context, input []int64, workers int) (Stream, error) {
    if ctx == nil { return Stream{}, errors.New("nil context") }
    if workers < 1 || workers > 16 || len(input) > 8192 {
        return Stream{}, errors.New("workers must be 1..16; input length at most 8192")
    }
    for _, value := range input {
        if value < -1000000 || value > 1000000 { return Stream{}, errors.New("input outside exact-square bound") }
    }
    values := append([]int64(nil), input...)
    jobs := make(chan job)
    output := make(chan Result)
    done := make(chan struct{})
    var active sync.WaitGroup
    active.Add(workers + 1)
    go func() {
        defer active.Done()
        defer close(jobs)
        for i, value := range values {
            select {
            case <-ctx.Done(): return
            case jobs <- job{i, value}:
            }
        }
    }()
    for i := 0; i < workers; i++ {
        go func() {
            defer active.Done()
            for {
                select {
                case <-ctx.Done(): return
                case item, ok := <-jobs:
                    if !ok { return }
                    result := Result{item.index, item.value * item.value}
                    select {
                    case <-ctx.Done(): return
                    case output <- result:
                    }
                }
            }
        }()
    }
    go func() { active.Wait(); close(output); close(done) }()
    return Stream{output, done}, nil
}

// Squares collects a complete successful stream in input order. On cancellation
// it discards partial output and reports the context error after every worker exits.
func Squares(ctx context.Context, input []int64, workers int) ([]int64, error) {
    stream, err := Start(ctx, input, workers)
    if err != nil { return nil, err }
    answer := make([]int64, len(input))
    count := 0
    for result := range stream.Results { answer[result.Index] = result.Square; count++ }
    <-stream.Done
    if err := ctx.Err(); err != nil { return nil, err }
    if count != len(input) { return nil, errors.New("internal completion count invariant failed") }
    return answer, nil
}
