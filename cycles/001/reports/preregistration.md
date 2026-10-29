# Preregistration: AdamW weight decay on sklearn digits (exploratory engineering replication)

Author: Libor "Burny" Burian (specification); executed by Claude Code. Machine-readable twin: `research/protocol.json` (it governs if the two differ).

**Status: exploratory.** Prior Haiku and Luna runs (https://github.com/BurnyCoder/eureka-digits-haiku, https://github.com/BurnyCoder/eureka-digits-luna) already reported results on this same evaluation set (`digits-stratified-42-test-v1`). This run cannot give untouched-data confirmation. Every conclusion is exploratory. No result exists at the time of writing, and nothing was trained in this phase.

## Objective and question
Engineering objective: produce verified, reproducible artifacts (pilot, comparison arms, report) whether the effect is positive, negative or inconclusive.
Question: does AdamW weight decay 0.01 (vs 0) improve held-out accuracy of a 64-128-10 ReLU MLP on the bundled digits data?

## Hypothesis h1
Mean paired test-accuracy difference (decay 0.01 − decay 0) over seeds 0,1,2 is positive.

Prior expectation (from the research phase): a null or tiny effect. With lr 1e-3, decoupled decay θ ← θ(1 − lr·λ) shrinks weights by only 1e-5 per step. Over 50 epochs of about 17 steps each (~850 steps) that gives a cumulative shrink of about 0.85%, so near-identical models are expected. Sources: PyTorch AdamW docs https://docs.pytorch.org/docs/stable/generated/torch.optim.AdamW.html; Loshchilov & Hutter, https://arxiv.org/abs/1711.05101.

## Alternative explanations
1. No effect (decay too weak at this lr and step count). This is the leading expectation.
2. Regularization reduces accuracy.
3. An apparent gain or loss comes from seed randomness or an implementation bug, such as decay not applied, leakage, or an arithmetic error in the metric.
4. Stronger simple baselines (logistic regression) match or beat the MLP, so the decay question is of little practical importance.

## Distinguishing predictions
- Paired seeds with identical data and batch order (order generator seeded by the seed) isolate decay. Predicted: per-seed differences are small, with magnitude of order a few test examples out of 360 (one example = 0.278 pp).
- Bug check: regularized and unregularized weights for the same seed differ (not bit-identical), with regularized weight norm slightly smaller. If they are identical, decay was not applied (alternative 3).
- Shuffled-label control (decay 0.01) should reach near-chance accuracy (~10%, well below real-label arms). If it does not, there is leakage or a metric bug.
- Class-prior baseline should be roughly 10%. Logistic regression and the MLPs should be above 95%.
- Sensitivity arm (decay 0.001) should lie between or near the two main arms. This is descriptive only.
- Accuracy recomputed from the saved `y_true`/`y_pred` must equal the stored `accuracy`.

## Primary metric
Mean over seeds {0,1,2} of test accuracy(decay=0.01) − test accuracy(decay=0). The test split has 360 examples.

## Falsification
A paired conditional 95% bootstrap interval wholly below zero contradicts the directional hypothesis. An interval that spans zero is inconclusive, not proof of equivalence. An interval wholly above zero is only exploratory support (see data boundaries). Failure of the shuffled-label control to fall to chance, or of the weights to differ between arms, would indicate a pipeline defect and invalidate the comparison.

## Methods and arms
`regularized` (wd 0.01), `unregularized` (wd 0), `sensitivity` (wd 0.001), `shuffled_labels` (wd 0.01, training labels permuted), `logistic` (sklearn LogisticRegression, C=1.0, max_iter=1000), `class_prior` (majority class). The network is 64-128-10 ReLU, AdamW, lr 1e-3, batch 64, 50 epochs, seeds 0,1,2 for neural arms (logistic and class_prior use seed 0). Hyperparameters are fixed in advance and none are selected on the test set. The decay values are a descriptive local sensitivity check, not a sweep. The pilot is the regularized seed-0 run, scored on validation only, and is published before the comparison arms are fit. The final regularized seed 0 reuses the pilot checkpoint. Fixture: `study.py` (scientific definitions unchanged); data https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_digits.html; checkpoints are safetensors.

## Seeds
0, 1, 2 (training/init/batch order). Split seed 42. Bootstrap seed 2026.

## Data boundaries
Frozen stratified 60/20/20 train/validation/test split (split seed 42). Pixels are divided by the constant 16 (no learned preprocessing). Split disjointness and coverage are asserted in code. Pilot reports validation only. No test result selects a model, epoch or hyperparameter. Generalization is limited to this random example split (no writer IDs, no other dataset). Prior results on this evaluation set are known, so there is no untouched data.

## Budget
180 active minutes and 60 CLI invocations in total (166.99 s and 2 calls used at the start of this phase). No silent extension. Training is a few small CPU/GPU runs.

## Analysis plan
Primary: 10000 paired bootstrap resamples of test example indices, RNG seed 2026, preserving pairing across methods and across all trained seeds. The interval conditions on the three trained models and does not estimate training-population uncertainty. Also report each seed's effect and the sample standard deviation across seeds. Report every other comparison (sensitivity, shuffled labels, logistic, class prior) descriptively with no post-hoc selection of a primary. Run the bug and consistency checks listed above (weight comparison, loss histories, metric recomputation) and label them post-hoc exploratory audits. Report negative and inconclusive results in full. Any change to this protocol will be an amendment made before the affected data is generated.

## Limitations
Three seeds; one random split; 360 test examples (coarse 0.28 pp resolution); conditional intervals; known prior outcomes. This trial shows one execution, not model superiority or general scientific reliability.
