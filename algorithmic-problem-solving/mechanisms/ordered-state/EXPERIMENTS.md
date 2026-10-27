# Count collisions, heap repair and tree shape

Question: which cost claims survive a changed input distribution? Hypotheses:
constant hashes defeat bucket growth; bottom-up heap construction uses less work
than descending repeated insertion for this input; sorted BST insertion produces
a chain. Fix n at16,64,256,1024, byte keys as four-byte little-endian integers,
integer heap priorities in descending order and tree shuffle seed718. Count key
or heap comparisons and rehashed entries, not a proxy fabricated from big-O.

Run the six independent tests, then
`python3 algorithmic-problem-solving/mechanisms/ordered-state/experiment.py`.
[observed.json](evidence/observed.json) is the actual2026-10-23 run with source
hashes and runtime/platform. Each result checks its observable output separately.

| n | Constant-hash comparisons | Rehashed entries | Heap build / repeated-push comparisons | Ascending / shuffled BST height |
| --- | --- | --- | --- | --- |
|16|120|21|24 /38|16 /6|
|64|2016|93|116 /264|64 /11|
|256|32640|381|496 /1546|256 /15|
|1024|523776|1533|2028 /8204|1024 /20|

Constant-hash chain length equaled n and comparisons equaled n(n−1)/2 despite
capacity growth. The default rolling hash had max chain2 at1024, but this selected
key family cannot establish robustness against adversarial keys. Rehashed-entry
counts stayed below2n; this supports the geometric relocation calculation, not
constant worst-case insertion. Ascending tree insertion also made n(n−1)/2
comparisons; its iterative implementation avoided recursive-stack failure without
improving that cost. One shuffled tree per size is not a worst-case balance proof.

Heap counts include the reference's pair comparisons, not Python bytecode or
allocation. Descending insertion forces long upward paths; another order can
change the comparison gap. No wall-time ranking is claimed. Follow-up: repeat
many shuffle seeds, use deliberately colliding rolling-hash keys, vary key length,
and add a balanced tree with verified metadata repairs. Record memory, cost units
and any newly imposed service bounds separately.
