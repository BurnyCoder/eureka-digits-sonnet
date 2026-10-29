# Experiments (exploratory engineering replication; prior Haiku/Luna results known)

Runs: `study.py experiments` (log: `research/experiments-run.log`), 15 records in `results/*.json` (regularized/unregularized/sensitivity/shuffled_labels × seeds 0–2, logistic, class_prior; plus the pilot `pilot_regularized_s0`, validation only). Predictions written beforehand: `research/experiment-predictions.md`. Post-hoc audit (exploratory): `research/experiment-analysis.json`, id `audit-experiments`, produced by `experiments_analysis.py` using `analysis.py`. Test split was used only in this planned evaluation; no model/epoch/hyperparameter was selected on it. Everything is exploratory.

## Test accuracy (360 examples, split seed 42)
| Arm | wd | s0 | s1 | s2 | mean ± sd (n=3) | record IDs |
|---|---|---|---|---|---|---|
| regularized | 0.01 | 0.9639 | 0.9694 | 0.9694 | 0.9676 ± 0.0032 | regularized_s0..s2 |
| unregularized | 0 | 0.9639 | 0.9694 | 0.9694 | 0.9676 ± 0.0032 | unregularized_s0..s2 |
| sensitivity | 0.001 | 0.9639 | 0.9694 | 0.9694 | 0.9676 ± 0.0032 | sensitivity_s0..s2 |
| shuffled-label control | 0.01 | 0.0611 | 0.1167 | 0.1083 | 0.0954 ± 0.0300 | shuffled_labels_s0..s2 |
| logistic regression (C=1) | – | 0.9556 | | | | logistic_s0 |
| class prior | – | 0.1028 | | | | class_prior_s0 |

## Primary result (h1)
Paired conditional bootstrap (10,000 resamples, RNG seed 2026) of acc(wd=0.01) − acc(wd=0): mean 0.0000, 95% CI [0, 0]; per-seed effects 0, 0, 0. The CI is not wholly below zero, so h1 is not falsified; the directional prediction (positive effect) is **not supported**. Outcome: null/inconclusive at this resolution (one test example = 0.28 pp). The CI is conditional on the trained models and excludes training-seed uncertainty; the degenerate [0,0] reflects identical predictions, not a precise estimate of equivalence.

## Controls, audits and what they show
- Shuffled labels: 9.5% mean (chance ≈10%), vs 96.8% real labels (paired difference 0.872, CI [0.847, 0.895]). No leakage signal. Train loss stayed ≈2.0 (see history), i.e. the net did not simply memorize in 50 epochs — the control is weaker evidence against leakage than a memorization test would be.
- Baselines: logistic regression 95.6% (MLP +1.2 pp, single seed, not tested); class prior 10.3%.
- Bug check (prediction P2, motivated by the identical results in Haiku/Luna): decay is applied. Max parameter gap between wd=0.01 and wd=0 runs is 0.068/0.019/0.008 (seeds 0/1/2), and final train/validation losses differ in the 4th digit (e.g. seed 0 val loss 0.1202 vs 0.1199), yet all 360 predictions are identical in every seed (0 disagreements). So the null is a real property of this setup (lr·wd = 1e-5 per step, src-adamw-doc), not an unapplied-decay bug. Caveat: gap sizes also reflect GPU/optimizer trajectory divergence; we did not run a same-wd repeat to separate the two, so the weight gap alone does not isolate the decay effect.
- Metric arithmetic: accuracies recomputed from saved `y_pred`/`y_true` match every record (`recomputed_accuracy_matches: true`).
- Seed sensitivity: sd 0.0032 across seeds (identical across arms because predictions coincide); seeds 1 and 2 give the same accuracy, so the seed sd rests on one differing seed.
- Hyperparameter sensitivity: wd ∈ {0, 0.001, 0.01} (descriptive, not selected on test) yields identical test accuracy and predictions pairwise (all paired effects 0, CI [0,0]). Other hyperparameters (lr, epochs, architecture) were not varied; larger decay was not tested, so this says nothing about regime where decay matters.

## Prediction vs observation
P1 (|diff| ≤ 0.6 pp): confirmed (0). P2 (sensitivity within 0.6 pp; check weights): confirmed, weights differ, predictions identical. P3 (shuffled ≈ chance): confirmed (9.5%). P4 (logistic ~95–97%, prior ~10%): confirmed (95.6%, 10.3%); MLP comparable to logistic.

## Limitations and failures
No failed runs. Random example split (no writer IDs) likely mixes writers; 3 seeds; single-split; prior results known so nothing here is confirmatory. The pilot checkpoint (regularized s0) was reused as regularized_s0 by design (identical validation/test source model).

## Learning
The decay effect is exactly zero in predictions at this lr/epochs, matching earlier runs, and the audit rules out the ordinary bug explanation. Next: interpretation/review phases should report an inconclusive-to-null result and not claim equivalence.
