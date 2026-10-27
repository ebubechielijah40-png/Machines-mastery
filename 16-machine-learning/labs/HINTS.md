# Hints

1–5: dot product is one scalar. Rows count positions; columns count features.
For a constant value, factor the vector out of the weighted sum.

6: adding the same constant to both values shifts o but leaves the difference
between `r_j` and their weighted mean unchanged.

7: zero keys imply zero scores. Average projected payloads, not raw tokens
unless W_V is identity.

8: the reference operation allows d_k and d_v to differ.

9: replace random coordinates with identical deterministic ones.

10: sum `a_j(r_j-mean)` and use `sum a_j=1`.

11: `q_j=sum_i x_i W_ij`; first work out `dq_j/dW_ij`.

12: keep matrices, width, sequence length, interpreter and procedure fixed.

13: trace features before the mask. Causality is a property of the entire
computational graph relative to the prediction cutoff.
