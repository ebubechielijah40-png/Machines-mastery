# Ownership exercises

1. Draw allocation owners after `Buffer a(2); Buffer b=a; Buffer c=std::move(b);`.
   Count live allocations before and after each destructor. Distinguish resource
   ID, object name and pointer address.
2. Explain why copying only data_ breaks exactly-once release. Show the failure
   as an ownership diagram; do not execute undefined behavior in the reference.
3. Trace `a=c` and `a=std::move(alias)` when alias references a. Identify the
   moment a's old resource is released and whether copying can fail before entry.
4. Borrow `int& r=a.at(0)` then replace a. What has happened to r? Why can't the
   range check on a later unrelated call prove r is safe?
5. Implement a nonallocating failpoint for the copy allocation in a learner copy.
   Verify failed assignment retains target contents, source contents and live count.
6. Replace the raw array with vector<int>. Explain which explicitly written
   operations can disappear, and preserve the public value/bounds contract.
7. From a blank file rebuild the owner, deep copy, move and release tests. Transfer
   the design to a local file-handle wrapper, stating what counts as an empty handle
   and whether copying is prohibited or duplicates a handle.
