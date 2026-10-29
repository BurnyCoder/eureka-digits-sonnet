# Review (exploratory; cycle 1, Sonnet run)

Historical model-authored review. The [parent review](../../../reports/parent-review.md) corrects its unsupported inference about sampling noise and its overstatement of the weight-difference check. This file preserves the submitted review; use the corrected interpretation and generated tables for current conclusions.

Scope: one pass over code, science, citations, reproducibility, security and presentation. Nothing was retrained; no result files were changed.

## Checks actually run
- `study.py check`: passed (1797x64 data; splits 1078/359/360).
- `pytest tests`: 8 passed, 1 skipped (the skip is the pilot-gate test, "pilot already published"; expected after the pilot ran).
- Cross-checked `reports/paper.md` accuracy table against `research/experiment-analysis.json`: values agree, and `recomputed_accuracy_matches` is true. Primary effect 0, CI [0,0], decision "inconclusive" is the same in the paper and the analysis file.
- Viewed `figures/accuracy.png` and `figures/examples.png` with the image reader. Accuracy plot: 15 labelled points, axis 0-1, color legend carried in the title (blue test, orange validation pilot); readable, no truncated axis. Examples: prediction/true-label tiles per method, first saved test records (no correctness-based selection), as the caption says.
- `cmp figures/accuracy.png site/figures/accuracy.png`: identical. Site has the same five figures as the cycle.
- Searched `.py`/`.json` for credential-like strings; only the filter ran, no `.env` or key files appear in `git status`.

## Findings
1. Science: the null result is consistent across paper, claims and interpretation. Claims are worded as "not supported / not falsified / equivalence not established", which matches the evidence (identical predictions, degenerate bootstrap CI). No overclaim found.
2. Degenerate CI: a [0,0] interval comes from identical predictions and conditions on trained models; the paper states this. It is not a variance estimate of training randomness.
3. Shuffled-label seed 0 scored 0.061, below the 0.10 chance level. With 360 test examples this is within sampling noise; not a bug.
4. Weight-difference audit (`audit-experiments`) is post hoc and cannot separate decay from run-to-run divergence. This is stated in the claim limitations.
5. The mechanism claim (lr*wd about 1e-5) is arithmetic on the documented update rule and is labelled untested.
6. Citations: claims cite result IDs and source IDs that exist in `results/*.json` and `research/sources.json`. In the research phase only two sources were re-fetched live (AdamW docs, Nanda index); the arXiv, sklearn, UCI, safetensors and prior-run README sources were not re-fetched in this run.
7. AI statement in the paper says Codex wrote the harness and fixture and Claude Code ran the cycle; README has no AI statement, per instructions.

## Not done / residual limits
- The interactive site (`site/index.html`, `site/data.json`) was not opened in a browser or rendered; I only checked that files exist, figures match, and the HTML head is well-formed. Its interactive behavior is unverified.
- `paper.pdf` was not opened or rendered; only `paper.md` was read.
- No larger-decay arm exists, so "no effect of decay" holds only for wd 0, 0.001, 0.01 at this learning rate and training budget.
- Three seeds, one dataset, one architecture, single-seed baselines; prior Haiku/Luna results known, so conclusions stay exploratory.

## Decision
No concrete failure needing a fix or an earlier-phase revisit. Continue to publish.
