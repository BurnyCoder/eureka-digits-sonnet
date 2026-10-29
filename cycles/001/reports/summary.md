# All experiments

Recorded harness status: **running**; 3 operational phases accepted. Measurements below do not imply completion of unaccepted phases.

| Experiment | Method | Seed | Split | Accuracy | Seconds | Device |
|---|---|---:|---|---:|---:|---|
| pilot_regularized_s0 | regularized | 0 | validation | 0.966574 | 8.906 | cuda |

The registered primary comparison is pending; no confirmatory conclusion is available.

- **analysis_kind**: "exploratory"
- **prior_results_known**: true
- **objective**: "Replicate a known fixed study to evaluate engineering completion; do not claim new scientific confirmation."
- **question**: "Does AdamW weight decay improve held-out accuracy of a small MLP on the bundled digits data?"
- **architecture**: [64, 128, 10]
- **optimizer**: "AdamW"
- **learning_rate**: 0.001
- **batch_size**: 64
- **epochs**: 50
- **methods**: ["regularized", "unregularized", "sensitivity", "shuffled_labels", "logistic", "class_prior"]
- **seeds**: [0, 1, 2]
- **data_boundaries**: "Frozen stratified 60/20/20 train/validation/test partition. Split seed 42. Divide pixels by the documented constant 16. Pilot reports validation only. No learned preprocessing or selection uses test data. Generalization is limited to this random example split, not new writers or datasets. Prior results on this evaluation set are known. All replication observations and conclusions are exploratory; no untouched-data claim is made."
- **analysis_plan**: "Use 10000 paired bootstrap resamples of test example indices with RNG seed 2026, preserving pairing across methods and all trained seeds. This interval conditions on the trained models and does not estimate training-population uncertainty. Separately show each seed effect and its sample standard deviation. Treat other comparisons as descriptive, with no post-hoc primary selection."
- **hyperparameter_rationale**: "Small prespecified network and fixed training budget provide fast feedback on an established task. The three decay values are a descriptive local sensitivity check, not a test-selected sweep. Three seeds expose limited initialization sensitivity; they do not support broad population claims."

This is a preliminary artifact generated before final interpretation. All available outcomes are retained; a completed experiment is not evidence that the favored hypothesis is true.

## Sources

- [src-adamw-doc: PyTorch torch.optim.AdamW documentation (2.15)](https://docs.pytorch.org/docs/2.15/generated/torch.optim.AdamW.html)
- [src-adamw-paper: Loshchilov & Hutter, Decoupled Weight Decay Regularization (ICLR 2019)](https://arxiv.org/abs/1711.05101)
- [src-load-digits: scikit-learn load_digits documentation](https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_digits.html)
- [src-uci-digits: UCI Optical Recognition of Handwritten Digits (Alpaydin & Kaynak)](https://archive.ics.uci.edu/dataset/80/optical+recognition+of+handwritten+digits)
- [src-safetensors-doc: Hugging Face safetensors torch API](https://huggingface.co/docs/safetensors/en/api/torch)
- [src-nanda-sequence: Neel Nanda, research process sequence (Alignment Forum)](https://www.alignmentforum.org/s/5GT3yoYM9gRmMEKqL)
- [src-lones-pitfalls: Lones, How to avoid machine learning pitfalls: a guide for academic researchers](https://arxiv.org/abs/2108.02497)
- [src-prior-haiku: Prior run: BurnyCoder/eureka-digits-haiku](https://github.com/BurnyCoder/eureka-digits-haiku)
- [src-prior-luna: Prior run: BurnyCoder/eureka-digits-luna](https://github.com/BurnyCoder/eureka-digits-luna)
