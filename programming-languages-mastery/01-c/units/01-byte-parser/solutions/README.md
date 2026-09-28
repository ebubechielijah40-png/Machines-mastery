# Reference reasoning

1: 1. 2: 256. 3: indices 0 and 1. 4: input pointer, claimed available length, output pointer. 5: return 0, preserve 99. 6: 255*256+255=65535. 7: alignment, permitted type access and host ordering (also width). 8: initialize out to a sentinel, test each error independently and assert it survives. 9: maximum is 2^32−1; require a type and arithmetic at least that wide, converting before operations and verifying octet width. 10: behavior on the defined domain must match, emitted instructions need not. Actual observations require your own log.

The final implementation is [parser.c](parser.c). Its proof and alternatives are in the lesson. Reconstruct it later without opening this directory.
