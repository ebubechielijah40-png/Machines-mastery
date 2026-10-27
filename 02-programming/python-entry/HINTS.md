# Progressive hints

1. Quote marks make text; equality returns a Boolean. Evaluate the right-hand side
   of assignment before rebinding the left-hand name.
2. List order controls updates. A while condition must eventually become false or
   encounter an explicit exit; count how many increments remain.
3. Decide before appending. Zero sizes fit but still consume one finite list entry.
4. Input validity and selection are separate obligations; validate before choosing.
5. accepted=[] creates a list. accepted=sizes creates another binding to one list.
6. Compare tuple/list values with assertEqual and use assertRaises for the defined
   exception. Check module path before debugging the algorithm on an import error.
7. Keep both used≤capacity and len(accepted)≤3 true before each append.
8. Write the contract and one worked trace first. A memorized for loop alone does
   not distinguish prefix admission from packing or all-or-nothing admission.
