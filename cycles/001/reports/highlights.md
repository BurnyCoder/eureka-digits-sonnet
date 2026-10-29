# Highlights and anomalies
- Highlight: effective per-step shrinkage lr*wd = 1e-5 (src-adamw-doc), so a null effect is the mechanistically expected outcome.
- Anomaly: both prior runs (src-prior-haiku, src-prior-luna) report identical accuracies across wd=0, 0.001, 0.01 at all seeds and a degenerate CI [0,0]. Check that decay is truly applied (compare weights and loss histories) before trusting the null.
- Limitation: load_digits is the UCI test subset without writer IDs (src-uci-digits); the random split likely mixes writers across splits.
- Limitation: 360 test examples give 0.28 pp resolution; the conditional bootstrap does not cover training randomness.
- Process caveat: prior results are known, so all conclusions are exploratory. Only the index of the Nanda sequence was read (src-nanda-sequence).
- Prior-run note: Luna reported evidence hashes broken by Git line-ending conversion; keep artifacts byte-stable (study.py asserts code and protocol hashes).
