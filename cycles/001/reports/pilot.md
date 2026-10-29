# Pilot report (exploratory)

**Run:** `study.py pilot` (id `pilot_regularized_s0`; record `results/pilot_regularized_s0.json`). Single run: regularized arm (AdamW, weight_decay=0.01), seed 0, scored on the **validation** split only (359 examples; train 1078 / validation 359 / test 360). Test data was not touched.

**Configuration** (from `research/protocol.json`): MLP with hidden layers 64 and 128 and 10 outputs, ReLU, AdamW lr=1e-3, batch 64, 50 epochs, split_seed 42. Device: cuda (RTX 5070 Laptop GPU), torch 2.14.1+cu130, 8.9 s. Checkpoint: `models/regularized-s0.safetensors` (sha256 `a57cb6e2...cb86cc3d`; the record states reload verification passed). Protocol, code and dataset hashes are stored in the result record. Validation predictions (`y_true`, `y_pred`, `example_ids`) and the 50-epoch loss history are in the same record.

## Predictions (made before the run, from the preregistration)
- Real-label training reaches high validation accuracy (>0.9) on this easy task. The decay effect is only measurable in later phases.
- Train and validation loss both decrease with no divergence.
- The pilot cannot say anything about the decay effect: there is no comparison arm.

## Observations
- Validation accuracy **0.9666** (347/359 correct). The count is recomputed from `y_true`/`y_pred` and matches the stored value.
- Train loss fell from 2.212 to 0.0568; validation loss fell from 2.088 to 0.1202 (epoch 50, also the minimum). The validation loss was noisy in the last epochs (0.1211 at epoch 47, 0.1233 at epoch 48) but there was no sustained rise, so no overfitting is visible within the 50-epoch budget. Both losses were still falling slowly at the end, so the model is probably undertrained rather than overfit.
- The 12 errors are: 8→1 (4 times), 2→1 (2), 5→9 (2), and one each for 0→4, 2→7, 9→8, 1→8. Class 1 is the most common wrong prediction, in 6 of 12 errors. This is a descriptive count on 12 errors, not a finding.

## Alternative explanations and checks
- Leakage: splits are disjoint, and `study.py check` and the unit tests passed in the core phase. The accuracy is plausible for this dataset and model.
- Bug (decay not applied): the pilot cannot show this. The later weight comparison between arms (see the preregistration) is needed.
- Single seed: 0.9666 has no seed-variance estimate. A binomial interval for 359 samples would be about ±1.9 points, which only covers the sampling noise of the validation set.

## Learnings
The fixture trains and saves end to end, and the predictions are reproducible from stored ids. The pilot gives no evidence for or against the decay hypothesis. The comparison phase should be run unchanged. The regularized seed-0 checkpoint is reused there; the validation pilot is the only use of this split so far. All conclusions remain exploratory because the Haiku and Luna results are known.
