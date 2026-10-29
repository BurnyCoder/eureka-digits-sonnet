# Interpretation (exploratory)

This text includes disclosed [parent corrections](https://github.com/BurnyCoder/eureka-digits-sonnet/blob/main/reports/parent-review.md) after the recorded model run. The measurements and controller counters are unchanged.

## Motivation
Does AdamW weight decay (0.01 vs 0) improve held-out accuracy of a small MLP on the bundled digits data? Prior Haiku and Luna runs on this evaluation set are known (`src-prior-haiku`, `src-prior-luna`), so this run is an **exploratory engineering replication**, not confirmation.

## Context
AdamW decouples decay from the gradient update (`src-adamw-paper`; update rule in `src-adamw-doc`). Data: scikit-learn digits, 1797 x 64, 10 classes (`src-load-digits`, `src-uci-digits`). Checkpoints use safetensors (`src-safetensors-doc`). Process guidance: `src-nanda-sequence`, `src-lones-pitfalls`.

## Methods
Fixed fixture `study.py` (unchanged; hashes recorded in each result). Arms with seeds 0-2: `regularized_s*` (wd 0.01), `unregularized_s*` (wd 0), `sensitivity_s*` (wd 0.001), `shuffled_labels_s*` (control); single-seed baselines `logistic_s0`, `class_prior_s0`; pilot `pilot_regularized_s0` (validation only). Primary metric: mean paired test-accuracy difference, regularized minus unregularized, with 10000 paired bootstrap resamples (`research/protocol.json`). Predictions were recorded before the run (`research/experiment-predictions.md`). Post-hoc audit `audit-experiments`: metric recomputation, weight and loss comparison. All numbers live in `results/*.json`, `research/experiment-analysis.json` and the controller-generated `reports/metrics.json`; none are retyped here.

## Findings
- **Primary (claim-primary-null):** the paired-bootstrap interval is degenerate at zero and predictions are identical in every seed. h1 is not supported and not falsified; under the preregistered rule an interval spanning zero is inconclusive, and equivalence cannot be claimed.
- **Bug check (claim-decay-applied):** weights and training losses differ between arms, consistent with different trajectories. That observation alone does not prove correct decay implementation. The observed accuracy difference is zero.
- **Dose (claim-sensitivity):** the weaker-decay arm also matches the unregularized arm.
- **Controls (claim-controls):** shuffled labels score near chance, the class prior near chance, logistic regression slightly below the MLPs.
- **Mechanism (claim-small-decay-explanation):** the small registered per-step decay coefficient is a possible explanation for unchanged accuracy, but gradient trajectories and decision margins also matter. This is an untested hypothesis.

## Alternative explanations considered
- Unapplied decay: weight and loss differences are consistent with the intervention affecting training, but do not by themselves rule out every implementation error.
- Metric arithmetic error: saved accuracies match recomputation from saved predictions; this check does not establish the validity of the labels or the whole experiment.
- Ceiling / test-set resolution: not ruled out; the small test set limits detectable differences.
- Stronger simple baseline: logistic regression is close but lower (single seed).
- Training randomness: controlled by paired seeds, identical splits and order.

## Negative findings
No positive observed accuracy effect and no observed accuracy response across the tested decay values. No stronger-decay arm was run, so larger decay remains unexplored. These are finite-sample observations, not population equivalence claims.

## Implications
The tested decay settings did not change the observed accuracy. A confirmatory follow-up needs a prospectively amended protocol and fresh evaluation data; a larger-decay arm could be an informative probe.

## Limitations
Exploratory only (prior results known); 3 seeds; bootstrap conditions on trained models; small test set; single-seed baselines; post-hoc audit; weight differences conflate decay with run divergence; one dataset and architecture.

## Related work
Decoupled weight decay: `src-adamw-paper`. Pitfalls checklist: `src-lones-pitfalls`. Earlier executions of this study: `src-prior-haiku`, `src-prior-luna`.
