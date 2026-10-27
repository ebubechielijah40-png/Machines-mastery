# Independently checkable solutions

1. A name is text; a declaration introduces a place; a frame is one runtime
activation holding places; a binding chooses the place for a use; its value can
change through assignment while the binding remains fixed.
2. G has registry, B captures the function, and each call adds F with parent B.
Resolved output is registry,registry. Mutable-chain output is registry,block,
because B gains the matching name before the second search.
3. Assignment changes a chosen slot's contents. Shadowing creates a different
slot in a different lexical position. A correct closure can observe changed
contents in its chosen slot without switching to a later slot.
4. Distances0,1,2 respectively, provided the function body has exactly one call
scope/frame and no extra body Block. The linked tests make this convention explicit.
5.4. The new call frame's parent is the function's captured declaration frame,
not the caller's frame containing100.
6. False marks a newly shadowing but not initialized local. Delaying insertion
would silently bind its initializer's same-name read to an outer slot, contrary
to our stated error rule. Define True only after resolving the initializer.
7. a captures factory frame A; b captures B. A.n progresses0→1→2→3 while B.n
progresses0→1. The call frames for next are short-lived; the captured factory
frames remain reachable through the returned closures.
8.1,2,3,4. Now both names refer to one closure/frame; making an alias did not call
the factory again or create an independent cell.
9. The permanent test starts global x=0, declares a local setter before a later
block x=99, then calls it. Resolved output inner99,outer8; mutable-chain output
inner8,outer0. Checking only the setter's return would miss the corrupted target.
10. The resolver rejects before interpretation; no preceding Print executes.
This differs from an execution-budget error after interpretation starts, which
has no rollback guarantee.
11. Before initialization, reading the global slot raises ExecutionError. After
initialization it yields x's value. Later global redeclaration updates that same
global named slot, so subsequent calls see the new value.
12. The own name is defined before resolving its body, permitting recursion.
A later sibling local name is not yet present in the resolver scope; that use
therefore becomes global in this language. Hoisted/mutually recursive local
functions require another explicit rule/pass, not arbitrary runtime searching.
13. Two objects represent two occurrences; one can target d=0 and another d=2.
Keying only by text overwrites the first result. Reusing one object across AST
positions creates the same collision, so the validator rejects shared nodes.
14. If x lies one lexical scope out, the resolver records1. An extra runtime
body frame makes the real x two edges away, so following1 reaches the wrong
frame. Add/remove scopes symmetrically, rather than changing all distances blindly.
15. A stack-of-maps resolver can search up to h maps per name: O(nh) worst case,
with expected constant map access under its usual assumptions. A resolved read
follows d edges: O(d), then expected map access. A separate display/slot design
can improve different terms; merely visiting each syntax node once is insufficient.
16. A correct extension rejects Boolean/noninteger operands and oversized results,
visits/resolves both subtrees, evaluates in defined order and preserves budgets.
Tests should include zero, negative operands, captured reads and a multiplication
that exceeds the declared bit limit. No multiplication implementation is claimed here.
17. Each scope needs a stable slot allocation and parameters/local declarations
must use exactly that layout at runtime. Resolve both distance and slot; create
frames of that size; compare all existing output and error traces. Removing
string lookup alone does not remove parent-edge traversal.
18. Predeclare hoisted bindings before resolving the block; separately model their
uninitialized state and runtime errors/initialization order. An earlier closure's
x use can then bind to a later local x. That is intentionally different semantics.
19. Node/step counts are not full memory/CPU quotas; nested calls can reach the
host stack earlier; host-language objects remain accessible to trusted Python;
there is no OS isolation, capability boundary, recovery transaction or policy for
arbitrary native callbacks. The language deliberately exposes none of those calls.
20. Compare the independently knowable marker output in each frame, both sides of
assignment, separate factory instances and unreachable static errors. Explain a
failed mutable-chain or frame-mismatch implementation, then repair the invariant.
A valid changed rule must modify its matching compile/runtime contracts and
examples; source agreement is not required for a deliberately different language,
but the difference must be named.
