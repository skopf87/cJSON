# cJSON: Bulk-copy unescaped parsed strings

The implementation in `cJSON.c` exactly matches the locally verified patch against upstream `6d9f2443ab071f86e5d9b43025a40929ec41c46c`. Original lab commit: `553c85d470fcf652d7b589580ba8fa765aac5235`. The publication manifest records source SHA256 and Git blob identity.

**Independent upstream confirmation: 16.0% aggregate time reduction** on this CPU workload suite (descriptive 95% interval 14.9–17.2%). Held-out aggregate: 12.2% time reduction. These are paired geometric-mean ratios, not whole-application guarantees.

All 21 upstream Unity test programs finish with zero failures (one upstream test ignored), plus 3,891 independent JSON/compatibility cases and 1,530 protected-page cases under ASan/UBSan. Strict C89 compilation passed.

The source, datasets, evaluator, compiler flags and thresholds were frozen before implementation trials. Each validation/confirmation uses 15 randomized pairs per workload after an excluded warmup, with 5,000 paired-round bootstrap replicates. The gate requires >2% improvement separately on screen and held-out aggregates, every workload upper ratio <=1.03, and process RSS <=1.10x + 1 MiB. Screening cannot promote.

## Workloads and confirmation medians

| Workload | Split | Upstream median batch (ms) | Optimized median batch (ms) | Paired time reduction |
|---|---|---:|---:|---:|
| short-keys | screen | 176.413 | 175.149 | 1.20% |
| long-text | screen | 30.855 | 16.879 | 44.82% |
| mixed-escapes | screen | 65.667 | 56.427 | 13.02% |
| unicode | heldout | 49.579 | 35.503 | 28.32% |
| numbers | heldout | 469.655 | 471.137 | 1.73% |
| upstream-test1 | heldout | 58.709 | 55.210 | 5.29% |
| upstream-test4 | heldout | 64.028 | 57.864 | 9.15% |
| github-repo | heldout | 58.290 | 49.172 | 14.05% |

Median ratios can differ from paired geometric-mean effects. Raw observations include checksums, call counts, RSS and warmup flags. Shared-VM variability is visible; intervals describe this experiment, not all hardware. The confirmation reused the fixed held-out suite on the same VM. No new algorithmic novelty or independent-team validation is claimed.

## Reproduce

Requirements: Linux with CPU 0 available, Python 3.12+, GCC, Git and taskset. The original environment used GCC 14.2.0 and an AMD EPYC virtual CPU; complete details are in `evidence/environment.json`. No third-party Python packages are required.

```sh
python3 research/reproduce.py --prepare-only
python3 research/reproduce.py --stage validate
```

The script creates an isolated temporary workspace, clones the pinned original upstream, verifies the frozen evaluator hashes, checks that the patch reconstructs the exact published implementation, and runs the original baseline and paired validation. It leaves new results in the printed workspace and does not alter this checkout. Changing affinity, compiler flags or workloads requires recording a new protocol.

## Evidence

`evidence/results/` contains all target runs, including unsuccessful follow-ups. `evidence/experiments.csv` and `evidence/benchmark_results.csv` are filtered from the original campaign without changing measurements. `evidence/final_report.md`, novelty assessment, rejected directions and candidate/backlog summaries describe the wider 21-candidate campaign; raw evidence here covers this component. The other verified component is in the corresponding `skopf87/cJSON` or `skopf87/libcsv` research branch.

The original benchmark sources/configuration/frozen manifest are preserved exactly under `benchmarks/`, `configs/`, `fixtures/` and `framework/`. `patches/` contains the cumulative upstream patch. Existing techniques are used; novelty coverage is explicitly incomplete.
