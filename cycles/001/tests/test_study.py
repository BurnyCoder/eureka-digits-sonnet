"""Fast tests (no training). Run: python -m pytest tests -q  (cwd = cycles/001)."""
import sys
from pathlib import Path

import numpy as np
import pytest
import torch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import analysis  # noqa: E402
import study  # noqa: E402

PROTOCOL = study.load(ROOT / 'research/protocol.json')


def test_splits_disjoint_stratified_and_sized():
    x, y, s = study.dataset(PROTOCOL)
    assert [len(s[k]) for k in ('train', 'validation', 'test')] == [1078, 359, 360]
    assert np.isfinite(x).all() and 0 <= x.min() and x.max() <= 1
    for k in s:  # stratification: every class in every split
        assert set(y[s[k]]) == set(range(10))


def test_splits_deterministic():
    _, _, a = study.dataset(PROTOCOL)
    _, _, b = study.dataset(PROTOCOL)
    assert all((a[k] == b[k]).all() for k in a)


def test_protocol_arms_and_decay_values():
    wd = PROTOCOL['weight_decay']
    assert wd['regularized'] == 0.01 and wd['unregularized'] == 0.0 and wd['sensitivity'] == 0.001
    assert set(PROTOCOL['methods']) == set(wd) | {'logistic', 'class_prior'}


def test_network_shape():
    assert study.network(PROTOCOL)(torch.zeros(3, 64)).shape == (3, 10)


def test_registration_matches_protocol_hash():
    reg = study.load(ROOT / 'research/registration.json')
    assert reg['protocol_sha256'] == study.sha(ROOT / 'research/protocol.json')


def test_experiments_blocked_before_pilot_publication(monkeypatch):
    if (ROOT / 'research/pilot-publication.json').exists():
        pytest.skip('pilot already published')
    monkeypatch.setattr(sys, 'argv', ['study.py', 'experiments'])
    with pytest.raises(RuntimeError):
        study.main()


def test_bootstrap_detects_known_effect_and_null():
    y = np.tile(np.arange(10), 36)
    good = y.copy()
    bad = y.copy(); bad[:90] = (bad[:90] + 1) % 10  # 25% errors
    eff = analysis.paired_effect(y, [good] * 3, [bad] * 3, 1000, 2026)
    assert eff['mean_effect'] == pytest.approx(0.25) and eff['ci95'][0] > 0
    null = analysis.paired_effect(y, [bad] * 3, [bad] * 3, 1000, 2026)
    assert null['mean_effect'] == 0 and null['ci95'] == [0, 0]


def test_bootstrap_reproducible():
    rng = np.random.default_rng(0)
    y = rng.integers(0, 10, 100); a = rng.integers(0, 10, (2, 100)); b = rng.integers(0, 10, (2, 100))
    assert analysis.paired_effect(y, a, b, 200, 1) == analysis.paired_effect(y, a, b, 200, 1)


def test_weight_difference():
    s = {'w': torch.ones(2)}
    assert analysis.max_weight_difference(s, s) == 0
    assert analysis.max_weight_difference(s, {'w': torch.tensor([1., 3.])}) == 2
