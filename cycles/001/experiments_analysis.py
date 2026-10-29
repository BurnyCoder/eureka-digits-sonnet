"""Post-hoc exploratory audit of results/*.json (no training). Writes research/experiment-analysis.json."""
import json, numpy as np
from pathlib import Path
from safetensors.torch import load_file
from analysis import paired_effect, max_weight_difference
R = Path('results'); P = json.loads(Path('research/protocol.json').read_text(encoding='utf-8-sig'))
rec = {p.stem: json.loads(p.read_text()) for p in R.glob('*.json') if not p.stem.startswith('pilot')}
seeds = P['seeds']; y = np.array(rec['regularized_s0']['y_true'])
for r in rec.values(): assert r['y_true'] == y.tolist()
arm = lambda m: np.array([rec[f'{m}_s{s}']['y_pred'] for s in seeds])
out = {'accuracy': {}, 'recomputed_accuracy_matches': True, 'effects': {}, 'audit': {}}
for k, r in rec.items():
    out['accuracy'][k] = r['accuracy']
    out['recomputed_accuracy_matches'] &= bool(abs(np.mean(np.array(r['y_pred']) == y) - r['accuracy']) < 1e-12)
for m in ['regularized', 'unregularized', 'sensitivity', 'shuffled_labels']:
    a = [rec[f'{m}_s{s}']['accuracy'] for s in seeds]; out['accuracy'][m + '_mean'] = float(np.mean(a)); out['accuracy'][m + '_sd'] = float(np.std(a, ddof=1))
for a, b, tag in [('regularized', 'unregularized', 'primary'), ('sensitivity', 'unregularized', 'descriptive'), ('regularized', 'sensitivity', 'descriptive'), ('regularized', 'shuffled_labels', 'control')]:
    out['effects'][f'{a}-{b}'] = {**paired_effect(y, arm(a), arm(b), P['bootstrap_resamples'], P['bootstrap_seed']), 'role': tag}
sd = lambda m, s: load_file(f'models/{m}-s{s}.safetensors')
out['audit']['max_weight_diff_reg_vs_unreg'] = [max_weight_difference(sd('regularized', s), sd('unregularized', s)) for s in seeds]
out['audit']['max_weight_diff_sens_vs_unreg'] = [max_weight_difference(sd('sensitivity', s), sd('unregularized', s)) for s in seeds]
out['audit']['identical_predictions_reg_vs_unreg'] = [bool((arm('regularized')[i] == arm('unregularized')[i]).all()) for i in range(3)]
out['audit']['prediction_disagreements_reg_vs_unreg'] = [int((arm('regularized')[i] != arm('unregularized')[i]).sum()) for i in range(3)]
out['audit']['final_train_loss'] = {m: [rec[f'{m}_s{s}']['history'][-1]['train_loss'] for s in seeds] for m in ['regularized', 'unregularized', 'sensitivity']}
out['audit']['final_val_loss'] = {m: [rec[f'{m}_s{s}']['history'][-1]['validation_loss'] for s in seeds] for m in ['regularized', 'unregularized', 'sensitivity']}
out['audit']['analysis_kind'] = 'exploratory (post-hoc audit)'
Path('research/experiment-analysis.json').write_text(json.dumps(out, indent=2))
print(json.dumps(out, indent=1))
