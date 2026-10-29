# Final report (exploratory; cycle 1, Sonnet run)

Author: Libor "Burny" Burian (specification); executed by Claude Code (Sonnet). All conclusions are **exploratory**: prior Haiku and Luna results on this evaluation set are known, so nothing here is preregistered confirmation on untouched data.

Numbers are not retyped here. Per-run values live in `results/*.json`; derived tables, effects, bootstrap intervals and audits are in `research/experiment-analysis.json`, `reports/experiments.md` and `reports/paper.md`. Claims and their evidence IDs are in `research/claims.json`; the requirement checklist is `research/requirements.json`.

## What was done
Research (sources in `research/sources.json`) → preregistration (`reports/preregistration.md`) → core checks (`study.py check`, 9 tests) → one validation-only pilot (`reports/pilot.md`) → 15 test-split experiment records: regularized (wd 0.01), unregularized (wd 0), sensitivity (wd 0.001) and shuffled-label arms at seeds 0–2, plus logistic-regression and class-prior baselines → analysis (`reports/interpretation.md`) → review (`reports/review.md`). No training was repeated for repairs.

## Findings
- **Primary (h1: weight decay improves test accuracy): not supported, not falsified, equivalence not established.** Predictions of the regularized and unregularized arms are identical in every seed; the paired-bootstrap effect and its CI are degenerate at zero (`claim-primary-null`). The CI conditions on the trained models and is not a training-variance estimate.
- **Not an unapplied-decay bug (post-hoc audit):** parameters and training losses differ between decay arms while predictions agree (`claim-decay-applied`). This cannot separate the decay effect from run-to-run divergence.
- **No dose-response:** the weaker-decay arm also matched the unregularized arm (`claim-sensitivity`); only one weaker dose was tested, and no larger decay was.
- **Controls behaved as expected:** shuffled-label and class-prior arms are near chance, logistic regression is slightly below the MLPs (`claim-controls`). Shuffled-label seed 0 falls slightly under 1/10, which is within sampling noise on a 360-example test set.
- **Mechanism (untested hypothesis):** lr·wd per step is about 1e-5 at AdamW defaults, so decay barely perturbs a briefly trained small MLP (`claim-small-decay-explanation`; AdamW docs, `src-adamw-doc`).

## Predictions vs. observations
All four predictions recorded before the experiments (`research/experiment-predictions.md`) were confirmed: null primary effect, chance-level shuffled labels, MLP above class prior, decay applied (weights differ). Alternatives considered: unapplied-decay bug (ruled out by audit), data leakage (splits disjoint, shuffled control at chance), stronger simple baseline (logistic regression is below the MLPs), and a decay too weak to matter (consistent, untested).

## Reconciliation
README results table, paper, reports, claims and checklist agree with the result files; the paper's accuracy table was cross-checked against `research/experiment-analysis.json` (`recomputed_accuracy_matches: true`). The README results block is controller-generated; its "5 operational phases accepted" status line is a snapshot that the controller updates on publication. `requirements.json` marks four items `not_applicable` (README, Git/Hugging Face, environment setup, AI statement) because they are controller-owned or outside the agent's phase; the AI statement is in the paper only, not the README.

## Remaining limits
- Three seeds, one dataset (sklearn digits), one architecture; baselines are single-seed.
- Tested decay values are only 0, 0.001 and 0.01 at one learning rate and training budget; a much larger decay is the informative next probe and was not run.
- Small test set: cannot resolve small differences.
- Review did not open the interactive site in a browser or render `paper.pdf`; only two sources (AdamW docs, Nanda index) were re-fetched live in this run; the other seven (arXiv papers, sklearn, UCI, safetensors, prior-run READMEs) were not.
- This trial demonstrates one execution, not model superiority or general scientific reliability.

## Status
Cycle 1 is complete as an engineering replication with an inconclusive-to-null scientific result. No further cycle was started.
