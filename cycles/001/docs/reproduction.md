# Reproduction guide (cycle 001, exploratory engineering replication)

Question (research/protocol.json): does AdamW weight decay 0.01 vs 0 change held-out accuracy of a 64-128-10 ReLU MLP on scikit-learn `load_digits`? Prior Haiku/Luna results are known, so **everything here is exploratory**; no untouched-data confirmation is claimed. The expected outcome is null/inconclusive; any result is reported.

## Environment
Python venv: `<harness>/.venv` (torch, numpy, scikit-learn, safetensors, pytest). All commands run with cwd `cycles/001`. No LLM/API is used by the code.

## Commands
| Step | Command | Trains? |
|---|---|---|
| Core check | `python study.py check` | no |
| Unit tests | `python -m pytest tests -q -p no:cacheprovider` | no |
| Pilot | `python study.py pilot` | yes: regularized seed 0, validation split only |
| Comparisons | `python study.py experiments` | yes: refuses to run until `research/pilot-publication.json` exists |

Controller runs pilot and comparisons only after core is published. `study.py` is hash-pinned in every result (`code_sha256`), as is `research/protocol.json`; editing either after results exist is rejected by the code. `study.py` was not modified.

## Data and split
`load_digits` (1797 x 64, pixels /16, a constant, so no learned preprocessing). Stratified 60/20/20 split, `split_seed=42`: train 1078 / validation 359 / test 360, asserted disjoint and exhaustive. Test is used only by `experiments`.

## Arms (all 50 epochs, AdamW lr 1e-3, batch 64, seeds 0,1,2 for MLP arms)
| Role | Method | Definition |
|---|---|---|
| Primary treatment | `regularized` | weight_decay 0.01 |
| Baseline | `unregularized` | weight_decay 0 |
| Ablation / dose check | `sensitivity` | weight_decay 0.001 (descriptive, not a selected sweep) |
| Random control | `shuffled_labels` | decay 0.01, training labels permuted; should lose useful accuracy |
| Non-neural baseline | `logistic` | sklearn LogisticRegression C=1, max_iter 1000 |
| Trivial floor | `class_prior` | predicts most frequent training class |

Paired seeds share initialization and batch order (`torch.manual_seed(seed)`, generator seeded by `seed`), so decay is the only difference between `regularized` and `unregularized`.

## Primary metric and analysis
Mean over seeds of test acc(0.01) − acc(0), with a 10000-resample paired bootstrap (rng seed 2026) over test examples, pairing preserved across arms and seeds (`analysis.paired_effect`). The interval is conditional on the trained models (excludes training-population uncertainty). Falsification: CI wholly below zero contradicts the directional hypothesis; spanning zero is inconclusive, not equivalence.

## Added audits (post-hoc, exploratory)
`analysis.max_weight_difference` compares safetensors weights between arms (zero would indicate decay was not applied), and accuracies can be recomputed from saved `y_true`/`y_pred`. These are not in the registered protocol.

## Tests (tests/test_study.py, no training)
Split sizes/disjointness/stratification/determinism; protocol decay values and arm list; network output shape; registration hash equals protocol hash; `experiments` is blocked before pilot publication; bootstrap recovers a known 0.25 effect and a zero null, and is reproducible; weight-difference helper.

## Outputs
`results/<id>.json` (accuracy, predictions, split ids, loss history, hashes, hardware), `models/*.safetensors|npz` (reload verified bit-exact), timestamped stdout logs. Negative results are never deleted.

## Limitations
One random split without writer IDs; 3 seeds; deterministic algorithms flag set, but GPU/CPU results may differ across hardware (device recorded). Sources: sklearn load_digits, PyTorch AdamW, safetensors docs, Nanda's research-process sequence (see research/sources.json).
