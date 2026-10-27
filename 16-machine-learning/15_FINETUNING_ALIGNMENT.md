# 15 — Fine-tuning and alignment

Pretraining teaches broad statistical structure. Fine-tuning changes behavior for a narrower distribution/objective.

## Supervised fine-tuning

Train on prompt-response or task examples using the same next-token objective but curated sequences. The model learns the formatting and behavioral distribution represented in those examples.

## Preference optimization

Preference methods use comparative judgments or reward signals to shift outputs toward desired behavior. The system now includes the data-collection process, annotator instructions, preference model/objective, and policy optimization—not only the base model.

## Parameter-efficient tuning

Methods such as low-rank adapters train small additional parameter sets instead of all weights. This reduces memory/storage and enables many task variants, but does not eliminate the need for evaluation and safety testing.

## Alignment is not truth

Preference alignment can make outputs more useful or policy-compliant, but cannot guarantee factual correctness. Reward models and preference data encode imperfect proxies and can be gamed.

## Experiment

Fine-tune a tiny language model on a small style/task dataset. Compare base and tuned models on held-out prompts, including adversarial prompts outside the fine-tuning distribution. Track both intended gains and regressions.
