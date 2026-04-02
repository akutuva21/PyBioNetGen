## 2025-03-03 - BNG Parser Speedup
**Learning:** `test_bngexec` spawns a `perl BNG2.pl -v` subprocess every time `find_BNG_path` is called, which happens for every single model parsed. BNG model initialization was significantly slowed down (0.24s per model) by this redundant check.
**Action:** Use `@lru_cache` on `find_BNG_path` or similar subprocess-heavy path resolution functions to memoize them and avoid repeatedly testing static binaries.

## 2025-03-03 - CLI Startup Time
**Learning:** `pkg_resources` is notoriously slow to import and can add significant overhead to CLI startup time.
**Action:** Replace `from pkg_resources import packaging` with `import packaging.version` to shave off startup time.
