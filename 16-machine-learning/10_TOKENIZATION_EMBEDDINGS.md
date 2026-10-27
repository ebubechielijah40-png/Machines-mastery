# 10 — Tokenization and embeddings

Language models operate on discrete token IDs, not raw human concepts. A tokenizer defines the interface between text and model vocabulary.

Character tokenization is simple but produces long sequences. Word tokenization creates huge vocabularies and poor handling of rare/new words. Subword tokenizers trade vocabulary size against sequence length by learning reusable fragments.

## BPE intuition

Start with small symbols, count adjacent pairs, merge the most useful pair, repeat. The learned merge table is part of the model interface: changing tokenization changes sequence lengths, vocabulary IDs, training statistics, and model compatibility.

## Embeddings

An embedding table maps integer IDs to learned vectors. It is mathematically a matrix lookup. The meaning of the vector is relational and task-dependent; dimensions do not arrive with labels such as “plurality” or “emotion.”

## Experiment

Tokenize the same multilingual/code-heavy corpus using character, whitespace, and a tiny BPE implementation. Compare vocabulary size, average sequence length, unknown handling, and compression ratio. Explain why “fewer tokens” is not automatically “better model.”

## Complete worked interfaces

[The training unit](training/README.md) derives lookup as one-hot multiplication,
shared embedding gradients, training-only vocabulary fitting and position rows.
Its character tokenizer rejects unknown characters; the runnable [byte-pair
variant](training/bpe.py) begins with256 UTF-8 byte tokens and deterministically
merges adjacent symbols. It is an original bounded variant, not a production
format. For `aaaa`, merging adjacent pair(a,a) nonoverlappingly gives two merged
tokens, not three overlapping replacements. Replaying learned merges at encoding
time preserves a frozen interface. [Tokenizer tests](training/test_bpe.py) verify
roundtrip on unseen Unicode, empty text, deterministic ties and invalid IDs.

Vocabulary compression is not semantic learning. A byte-pair token can contain
several characters, or only part of a multibyte character; decode the concatenated
bytes before interpreting Unicode. The character model's output vocabulary is
still the character mapping it was trained on. Swapping in BPE without changing
its embeddings/output layer and retraining makes those parameter rows meaningless.
