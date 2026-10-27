# Checkable solutions

1. Types are int,float,str,bool,NoneType. Assignment creates/changes a binding;
   comparison evaluates equality. Starting x=3, print(x), x=x+1, print(x) displays3,4.
2. used evolves0→4→4→11. Empty input leaves0. For a while loop incrementing i from0
   toward3,3−i decreases on each valid iteration and never goes below0 before exit.
3. Results:([4,0],4),([0,0],0),([],0). Skipping6 to accept1 violates ordered-prefix
   semantics. Zero-size packets do not create an infinite loop over a finite list.
4. This API promises that every listed byte count is valid. Returning success
   without inspecting the negative later count would violate that declared boundary.
5. A new outer list holds selected immutable integers. A second name for sizes
   shares the same mutable list and exposes caller state to append/remove changes.
6. Valid expected examples include([2,3],5)→([2,3],5),([6],5)→([],0); invalid[-1]
   requires ValueError. Import errors prevent the function/test from being reached.
7. Before accepting, reject/stop if len(accepted)==3 or used+size>capacity. Both
   constraints must hold after every append. [0,0,0,0] with capacity0 then accepts
   exactly three packets. This extension is specified for learner implementation.
8. The maximum-sum subset could select11+9 from[12,11,9], but ordered-prefix
   admission stops after12. Validation, effect-free return and independent tests
   are separate parts of a complete small program.
