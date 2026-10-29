# Research phase: literature and fixture review (exploratory)

**Question** (protocol.json): does AdamW weight decay 0.01 vs 0 improve held-out accuracy of a 64-128-10 ReLU MLP on sklearn digits? Prior Haiku and Luna runs on this same test set are known, so everything here is **exploratory**, not confirmatory.

## Sources (details in research/sources.json)
- AdamW: PyTorch docs [src-adamw-doc] and Loshchilov & Hutter [src-adamw-paper]. Decay is decoupled: theta <- theta - lr*wd*theta, outside Adam's moments. With lr=1e-3 and wd=0.01 each step shrinks weights by a factor of 1e-5 (arithmetic from the documented rule). Over 50 epochs x 17 batches (1078 train examples / batch 64), about 850 steps, cumulative shrinkage is roughly 0.85% of weight magnitude. This is a very weak regularizer.
- Data: load_digits [src-load-digits] is the 1797-sample UCI *test* portion [src-uci-digits] (CC BY 4.0). Writer IDs are not exposed, so the fixture's random stratified 60/20/20 split can put the same writer in train and test. Results are optimistic for "new writers" and generalize only to random examples. Dividing by the constant 16 uses no fitted statistics, so there is no preprocessing leakage.
- Serialization: safetensors API [src-safetensors-doc]; study.py usage (contiguous CPU tensors, reload, exact-equality check) matches the docs.
- Process: Nanda sequence [src-nanda-sequence] (only post titles read this phase) and Lones pitfalls [src-lones-pitfalls] as a checklist.
- Prior results [src-prior-haiku], [src-prior-luna]: regularized, unregularized and sensitivity MLPs had identical test accuracy at every seed (0.9639/0.9694/0.9694), logistic 0.9556, class-prior 0.1028, shuffled labels 0.06-0.12; paired diff 0, CI [0,0], "inconclusive".

## Fixture inspection (read study.py and protocol.json; nothing run yet)
- Split happens before fitting; disjointness and coverage are asserted; split seed 42; test is used only in `experiments`; the pilot is validation-only.
- Pairing: the same seed gives the same init and batch order (dedicated generator), so arms differ only in weight decay. shuffled_labels uses wd=0.01, so it controls for label signal, not for decay.
- The seed-0 regularized final run reuses the pilot checkpoint (code hash asserted).
- The bootstrap CI is conditional on the trained models. If predictions are identical across arms the interval is degenerate [0,0], and "inconclusive" follows from the registered rule, not from equivalence.
- Test set has 360 examples, so one example = 0.28 pp; smaller differences are below resolution.

## Predictions (recorded before any experiment)
1. P1 (main, ~65% confidence): paired mean difference is 0 or within +-0.6 pp and the CI contains or equals zero, so inconclusive. Basis: the tiny effective shrinkage above and the two prior runs.
2. P2: sensitivity (wd=0.001) is indistinguishable from the others.
3. P3: shuffled-label accuracy near chance (~0.1, +-~0.03 sampling noise on 360 examples); class-prior ~0.10; logistic ~0.95-0.96; MLP ~0.96-0.97 on test and on the validation pilot.
4. Falsifiers: a CI wholly below zero falsifies h1. A CI wholly above zero (not predicted) should first be checked for bugs. Shuffled-label accuracy well above chance would indicate leakage or a bug.

## Alternative explanations
- Null from weak decay vs null from a ceiling effect (~97% on an easy task with 360 test points).
- Identical results could be a bug (decay not applied). Cheap check: compare final weights and loss histories of regularized vs unregularized; they should differ slightly even if predictions match.
- Agreement of the prior runs reflects the same fixed code and data, not independent replication.
- Optimism from writer overlap across the random split.

## Next
Run `study.py check`, pilot, then experiments in their own phases; compare weights and histories across arms as a bug check; report the null honestly.
