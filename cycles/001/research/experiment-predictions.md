# Predictions recorded before `study.py experiments` (exploratory; prior Haiku/Luna results known)
- P1: regularized (wd 0.01) vs unregularized (wd 0) test-accuracy difference is ~0 (|diff| <= 0.6 pp), because lr*wd = 1e-5 per step. Falsified for the directional hypothesis only if the paired 95% bootstrap CI is wholly below 0.
- P2: sensitivity (wd 0.001) is within 0.6 pp of both; identical predictions are possible and must be checked against weight differences (bug check: decay silently unapplied).
- P3: shuffled_labels accuracy near chance (~10%), far below real-label arms (>94%). A high value would indicate leakage/bug.
- P4: logistic regression ~95-97%; class_prior ~10%. MLP arms should be comparable to logistic.
- Alternatives: no effect; decay hurts; seed noise; implementation bug (decay not applied; metric arithmetic).
