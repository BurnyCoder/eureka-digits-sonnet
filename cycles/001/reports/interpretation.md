# Interpretation (exploratory)

## Motivation
Does AdamW weight decay (0.01 vs 0) improve held-out accuracy of a small MLP on the bundled digits data? Prior Haiku and Luna runs on this evaluation set are known (`src-prior-haiku`, `src-prior-luna`), so this run is an **exploratory engineering replication**, not confirmation.

## Context
AdamW decouples decay from the gradient update (`src-adamw-paper`; update rule in `src-adamw-doc`). Data: scikit-learn digits, 1797 x 64, 10 classes (`src-load-digits`, `src-uci-digits`). Checkpoints use safetensors (`src-safetensors-doc`). Process guidance: `src-nanda-sequence`, `src-lones-pitfalls`.

## Methods
Fixed fixture `study.py` (unchanged; hashes recorded in each result). Arms with seeds 0-2: `regularized_s*` (wd 0.01), `unregularized_s*` (wd 0), `sensitivity_s*` (wd 0.001), `shuffled_labels_s*` (control); single-seed baselines `logistic_s0`, `class_prior_s0`; pilot `pilot_regularized_s0` (validation only). Primary metric: mean paired test-accuracy difference, regularized minus unregularized, with 10000 paired bootstrap resamples (`research/protocol.json`). Predictions were recorded before the run (`research/experiment-predictions.md`). Post-hoc audit `audit-experiments`: metric recomputation, weight and loss comparison. All numbers live in `results/*.json`, `research/experiment-analysis.json` and the controller-generated `reports/metrics.json`; none are retyped here.

## Findings
- **Primary (claim-primary-null):** the paired-bootstrap interval is degenerate at zero and predictions are identical in every seed. h1 is not supported and not falsified; under the preregistered rule an interval spanning zero is inconclusive, and equivalence cannot be claimed.
- **Bug check (claim-decay-applied):** weights and training losses differ between arms, so decay is applied; its accuracy effect is nil here.
- **Dose (claim-sensitivity):** the weaker-decay arm also matches the unregularized arm.
- **Controls (claim-controls):** shuffled labels score near chance, the class prior near chance, logistic regression slightly below the MLPs.
- **Mechanism (claim-small-decay-explanation):** per-step shrinkage lr*wd is about 1e-5 at defaults, plausibly too small to change a briefly trained model. This is an untested hypothesis.

## Alternative explanations considered
- Unapplied decay: ruled out by the weight and loss audit.
- Metric arithmetic error: ruled out by recomputation from predictions.
- Ceiling / test-set resolution: not ruled out; the small test set limits detectable differences.
- Stronger simple baseline: logistic regression is close but lower (single seed).
- Training randomness: controlled by paired seeds, identical splits and order.

## Negative findings
No positive effect of decay; no dose-response over the tested range; no stronger-decay arm was run, so larger decay remains unexplored.

## Implications
In this setup the decay setting is not a useful lever. A confirmatory follow-up needs a prospectively amended protocol with a larger-decay arm and fresh evaluation data.

## Limitations
Exploratory only (prior results known); 3 seeds; bootstrap conditions on trained models; small test set; single-seed baselines; post-hoc audit; weight differences conflate decay with run divergence; one dataset and architecture.

## Related work
Decoupled weight decay: `src-adamw-paper`. Pitfalls checklist: `src-lones-pitfalls`. Earlier executions of this study: `src-prior-haiku`, `src-prior-luna`.
