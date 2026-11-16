# cJSON integration evaluation

This branch combines current upstream master with two independently tested changes:

- Original print-buffer fix: [upstream PR #1129](https://github.com/DaveGamble/cJSON/pull/1129),
  original commit `8d72ed09aa0238c5b744408f9eaeff04c3820a1c` by Koi, preserved separately.
- Bounded unescaped-string copying and native length/UTF-8 regression tests.

Baseline: `6d9f2443ab071f86e5d9b43025a40929ec41c46c`.
OpenHarmony's null-helper fix and Debian's CMake minimum-version fix are already
present in this baseline, so they were not imported again.

Validation on Codex Cloud, GCC 14.2.0, CMake 4.0.3:

- All 22 CTest targets passed; native allocator and bounded-string regressions passed.
- 3,891 independent JSON/differential cases and 1,530 protected-page cases passed.
- Native misc/string tests and a zero-buffer guard-page reproducer passed with ASan/UBSan.
- Strict C89 production compilation passed. Public header and exported symbol names
  match upstream; this is not a full cross-platform ABI audit.
- Frozen original eight-case parse/delete benchmark: 17.31% lower aggregate
  time, descriptive 95% interval 16.45–18.19%;
  held-out aggregate 13.81%. Fifteen randomized pairs per case with
  excluded warmup, pinned CPU 0, equal-weight geometric ratios, fixed regression
  and memory gates. Same VM/corpus; not new unseen data or a new optimization.

Repeat native checks from this source branch:

```sh
cmake -S . -B build -DENABLE_CJSON_UTILS=ON -DENABLE_CJSON_TEST=ON
cmake --build build --parallel 2
ctest --test-dir build --output-on-failure
```

This is an evaluation patch set, not a supported release or a comprehensive
security-fix collection. Printing correctness was tested; printing throughput,
other machines and all compiler/ABI combinations have not been benchmarked.
Existing public performance PR branches and default branches are unaffected.
AI-assisted integration and validation; borrowed authorship is retained.
