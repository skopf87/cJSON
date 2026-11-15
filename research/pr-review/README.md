# cJSON PR validation against develop

Base: `1ac905d3b2359f48a0463afe8e16a080f0e1e03c` (`DaveGamble/cJSON:develop`), as required by `.github/CONTRIBUTING.md`. This is a separate protocol from the earlier master-based research; its evaluator and data are frozen in this directory.

Validation: 18.19% paired aggregate time reduction; descriptive 95% interval 17.33–19.08%. Fifteen randomized pairs across eight workloads. Both screen and held-out aggregates and every per-workload regression gate pass. This is a single validation run on the develop base; earlier master confirmations are separate evidence.

All 20 develop-base upstream Unity programs pass (one upstream test ignored), plus the new bounded-string native test, 3,891 independent compatibility/oracle cases and 1,530 protected-page cases under ASan/UBSan. The native parse-string test executable also passes under ASan/UBSan and the production source passes strict C89 with warnings as errors.

```sh
python3 research/pr-review/run.py --prepare-only
python3 research/pr-review/run.py --stage validate
```

The script requires Linux with CPU 0, GCC, Git, taskset and Python 3.12+. It clones the pinned original develop commit into an isolated directory and reuses the frozen evaluator and patch. Raw results, test output and per-workload intervals are under `evidence/results/`. The test adapter enumerates the 20 programs present on develop, while the datasets, timing harness, statistical method and thresholds match the original experiment.

Paired geometric-mean ratios are descriptive for this shared VM and fixed suite, not whole-application guarantees or a claim of algorithmic novelty. Short keys and numeric documents show little or no gain.

| Workload | Upstream median ms | Optimized median ms | Paired time reduction |
|---|---:|---:|---:|
| short-keys | 151.841 | 151.300 | -0.14% |
| long-text | 30.710 | 16.647 | 46.83% |
| mixed-escapes | 61.263 | 50.578 | 17.47% |
| unicode | 46.318 | 31.911 | 31.13% |
| numbers | 366.262 | 364.014 | 0.13% |
| upstream-test1 | 53.001 | 48.130 | 8.97% |
| upstream-test4 | 56.987 | 49.990 | 11.76% |
| github-repo | 53.685 | 44.141 | 17.36% |
