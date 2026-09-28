# Self-contained study protocol

The repository replaces **required** cover-to-cover reading with a source-grounded, active-learning workflow. It does not pretend that AI reconstruction is identical to an author's book. When exact wording, a disputed claim, or a specification detail matters, consult the original source. For normal learning, stay here.

## One learning session

### 1. Enter through a question
Write what you are trying to explain or build. Examples: “Why does an index make some database queries faster?”, “What physically stores one bit?”, “Why can a TCP write be split across reads?”, “How can two qubits have correlations no pair of classical bits can reproduce?”

### 2. Predict first
Before reading the answer, write a prediction. Wrong predictions are useful because they expose your model.

### 3. Learn the mechanism
Do not accept labels as explanations. “The cache is faster” is not enough. Ask where the bytes are, how they are addressed, how the lookup proceeds, what state is updated, and what happens on a miss.

### 4. Run something
Use code, a simulator, a trace, a measurement, or a controlled physical experiment. If a unit cannot be run, use a worked state trace and a reconstruction exercise.

### 5. Break one assumption
Increase input size, remove an index, corrupt a message, delay a node, change a boundary condition, or use a counterexample. The goal is to discover where the model stops working.

### 6. Explain without notes
Explain the mechanism from first principles. Then reconstruct the architecture or algorithm from memory.

### 7. Transfer
Solve a related problem whose surface details differ. Transfer is stronger evidence than recognition.

## Reading compression

Each “coursebook” in `coursebooks/` is an original, compressed teaching text. It is not a summary of a copyrighted book. It combines the minimum theory, deeper mechanism, examples, labs, assignments, and internal references needed to progress.

## Assistance levels

Project guides use four assistance levels:

- **A0 — independent:** problem and acceptance tests only.
- **A1 — prompts:** design questions, no architecture.
- **A2 — scaffold:** interfaces and checkpoints.
- **A3 — guided:** detailed implementation plan and reference solution after attempt.

Start at A0/A1. Escalate only when blocked. After using A3, rebuild a smaller version without the guide.
