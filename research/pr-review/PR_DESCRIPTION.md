`parse_string` already scans a bounded string literal to find its end and count escapes. For a string without escapes, it then copies the same bytes through a second scalar loop. Reuse the existing zero-escape count to copy that string with `memcpy`, then share the existing termination and item/offset updates. Escaped strings keep their existing decoder and error handling.

This targets `develop`, following `.github/CONTRIBUTING.md`. The PR contains the implementation and native regression coverage; the experiment artifacts are linked separately.

### Tests

- Add a Unity regression covering unescaped strings of lengths 0–256 without an input terminator, the same inputs truncated before the closing quote, output termination/offsets, and raw UTF-8.
- All 20 test programs present on this `develop` base finish with zero failures; one existing upstream test is ignored.
- 3,891 independent JSON/oracle and upstream-compatibility cases, plus 1,530 exact-boundary protected-page cases, pass.
- The native `parse_string` test program and protected-page checks pass under AddressSanitizer/UBSan. Production source passes strict C89 compilation with `-pedantic -Wall -Wextra -Werror`.

The native sanitizer check is reproducible from this branch:

```sh
gcc -std=c99 -O1 -g -fsanitize=address,undefined -fno-omit-frame-pointer \
    tests/parse_string.c tests/unity/src/unity.c -lm -o /tmp/parse-string-test
/tmp/parse-string-test
```

### Performance evidence

Fresh measurements against `develop` commit `1ac905d3b2359f48a0463afe8e16a080f0e1e03c` show **18.2% lower aggregate parse/delete time** across eight fixed workloads; descriptive paired-bootstrap 95% interval **17.3–19.1%**. The held-out workload aggregate improves **14.5%**.

| Workload | Paired time reduction |
|---|---:|
| Long unescaped text | 46.8% |
| Raw Unicode text | 31.1% |
| Public repository API response | 17.4% |

Short-key and number-only cases show little or no benefit. Each workload uses 15 randomized paired measurements after an excluded warmup. Results use equal-weight geometric means of paired time ratios, with 5,000 whole-round bootstrap resamples. Every workload also passes the fixed 3% upper-bound regression gate.

Environment: Codex Cloud, AMD EPYC 9V74 virtual CPU, GCC 14.2.0, generic x86-64 `-O3`, one thread pinned to CPU 0. These are shared-VM, fixed-corpus results, not a whole-application guarantee or a novelty claim.

[Raw measurements, full test logs, frozen configuration and reproduction instructions](https://github.com/skopf87/cJSON/blob/915aed0b0a498ebda2c5300e237cdd9cddbf80a0/research/pr-review/README.md). That directory preserves the separate `develop`-base validation; earlier `master` measurements elsewhere in the research branch are not substituted for it.
