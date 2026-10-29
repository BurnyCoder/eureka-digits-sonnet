"""Post-run analysis helpers (no training). Protocol: research/protocol.json analysis_plan.

Paired bootstrap: https://numpy.org/doc/stable/reference/random/generator.html
"""
import numpy as np


def paired_effect(y_true, preds_a, preds_b, resamples, seed):
    """Mean over seeds of acc(a)-acc(b), with a conditional bootstrap CI over test examples.

    preds_a / preds_b: arrays (n_seeds, n_examples). One index draw per resample is shared by
    both arms and all seeds, preserving pairing. Conditions on the trained models.
    """
    y, a, b = np.asarray(y_true), np.asarray(preds_a), np.asarray(preds_b)
    hit = (a == y).astype(float) - (b == y).astype(float)  # per-seed, per-example difference
    rng = np.random.default_rng(seed)
    draws = rng.integers(0, hit.shape[1], size=(resamples, hit.shape[1]))
    boot = hit[:, draws].mean(axis=(0, 2))  # mean over seeds and resampled examples
    low, high = np.percentile(boot, [2.5, 97.5])
    per_seed = hit.mean(axis=1)
    return {'mean_effect': float(hit.mean()), 'ci95': [float(low), float(high)],
            'per_seed': per_seed.tolist(),
            'seed_std': float(per_seed.std(ddof=1)) if len(per_seed) > 1 else None}


def max_weight_difference(state_a, state_b):
    """Largest absolute parameter gap between two state dicts; 0 would mean decay had no effect."""
    return max(float((state_a[k] - state_b[k]).abs().max()) for k in state_a)
