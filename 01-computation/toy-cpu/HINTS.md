# Hints

1–2. Count ones; separate the low bit from twice the high bit. In the induction,
carry leaving column k is input to column k+1.

3. Compare255+1 and127+1 under both interpretations.

4–5. Divide the encoded byte by16. The low nibble is an address for ADD/LDA/STA.

6–7. The loop's final iteration skips its JMP. Restarting address0 resets product
but does not restore the counter. Track memory13 and15 separately.

8. Start A=0;0x00 is NOP.

9–12. Define the mathematical output independently before implementing a flag.
Reserve space for entry logic before deciding where data begins. For SUB, state
whether the flag means borrow or no borrow; neither name alone specifies it.
