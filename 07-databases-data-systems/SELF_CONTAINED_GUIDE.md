# Databases and data systems — self-contained phase guide

This guide supplements the phase README with a learner-facing mechanism/application path. For each module, perform the example, code/lab task, and limitation check.

## 1. Relational Model/Sql

**Problem.** Identify the real system problem that makes relational model/SQL necessary.

**Mechanism.** Describe state, inputs, outputs, transformations, invariants, resource costs, and failure modes. Descend one abstraction layer below the normal API.

**Example.** Construct the smallest concrete example that exhibits the mechanism; trace it by hand before running it.

**Code/application.** Implement a bounded model or inspect an existing executable lab. Add correctness tests and at least one adversarial/edge case.

**Experiment.** Change one variable (input size, latency, memory, noise, concurrency, failure, or assumption), measure, and compare with a prediction.

**Production/real-world question.** What changes at 1×, 100×, and 10,000× load/data/state? What becomes observable only in production?

**Limit.** State one thing this model cannot establish and one condition under which it fails.

## 2. Storage Pages/Indexes

**Problem.** Identify the real system problem that makes storage pages/indexes necessary.

**Mechanism.** Describe state, inputs, outputs, transformations, invariants, resource costs, and failure modes. Descend one abstraction layer below the normal API.

**Example.** Construct the smallest concrete example that exhibits the mechanism; trace it by hand before running it.

**Code/application.** Implement a bounded model or inspect an existing executable lab. Add correctness tests and at least one adversarial/edge case.

**Experiment.** Change one variable (input size, latency, memory, noise, concurrency, failure, or assumption), measure, and compare with a prediction.

**Production/real-world question.** What changes at 1×, 100×, and 10,000× load/data/state? What becomes observable only in production?

**Limit.** State one thing this model cannot establish and one condition under which it fails.

## 3. Transactions/Isolation

**Problem.** Identify the real system problem that makes transactions/isolation necessary.

**Mechanism.** Describe state, inputs, outputs, transformations, invariants, resource costs, and failure modes. Descend one abstraction layer below the normal API.

**Example.** Construct the smallest concrete example that exhibits the mechanism; trace it by hand before running it.

**Code/application.** Implement a bounded model or inspect an existing executable lab. Add correctness tests and at least one adversarial/edge case.

**Experiment.** Change one variable (input size, latency, memory, noise, concurrency, failure, or assumption), measure, and compare with a prediction.

**Production/real-world question.** What changes at 1×, 100×, and 10,000× load/data/state? What becomes observable only in production?

**Limit.** State one thing this model cannot establish and one condition under which it fails.

## 4. Query Planning

**Problem.** Identify the real system problem that makes query planning necessary.

**Mechanism.** Describe state, inputs, outputs, transformations, invariants, resource costs, and failure modes. Descend one abstraction layer below the normal API.

**Example.** Construct the smallest concrete example that exhibits the mechanism; trace it by hand before running it.

**Code/application.** Implement a bounded model or inspect an existing executable lab. Add correctness tests and at least one adversarial/edge case.

**Experiment.** Change one variable (input size, latency, memory, noise, concurrency, failure, or assumption), measure, and compare with a prediction.

**Production/real-world question.** What changes at 1×, 100×, and 10,000× load/data/state? What becomes observable only in production?

**Limit.** State one thing this model cannot establish and one condition under which it fails.

## 5. Batch/Stream Pipelines

**Problem.** Identify the real system problem that makes batch/stream pipelines necessary.

**Mechanism.** Describe state, inputs, outputs, transformations, invariants, resource costs, and failure modes. Descend one abstraction layer below the normal API.

**Example.** Construct the smallest concrete example that exhibits the mechanism; trace it by hand before running it.

**Code/application.** Implement a bounded model or inspect an existing executable lab. Add correctness tests and at least one adversarial/edge case.

**Experiment.** Change one variable (input size, latency, memory, noise, concurrency, failure, or assumption), measure, and compare with a prediction.

**Production/real-world question.** What changes at 1×, 100×, and 10,000× load/data/state? What becomes observable only in production?

**Limit.** State one thing this model cannot establish and one condition under which it fails.

## 6. Lineage/Scaling

**Problem.** Identify the real system problem that makes lineage/scaling necessary.

**Mechanism.** Describe state, inputs, outputs, transformations, invariants, resource costs, and failure modes. Descend one abstraction layer below the normal API.

**Example.** Construct the smallest concrete example that exhibits the mechanism; trace it by hand before running it.

**Code/application.** Implement a bounded model or inspect an existing executable lab. Add correctness tests and at least one adversarial/edge case.

**Experiment.** Change one variable (input size, latency, memory, noise, concurrency, failure, or assumption), measure, and compare with a prediction.

**Production/real-world question.** What changes at 1×, 100×, and 10,000× load/data/state? What becomes observable only in production?

**Limit.** State one thing this model cannot establish and one condition under which it fails.

## Exit assignment

Build one small system combining at least three modules. Provide tests, an experiment log, a failure analysis, and a reconstruction sketch created without looking at the implementation.
