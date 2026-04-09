## 2024-05-24 - Testing the get_close_matches wrapper function
**Learning:** Testing cached functions properly involves mocking the inner function to ensure that repeated calls are resolved from the cache instead of running the function again.
**Action:** When testing methods decorated with `@memoize`, patch the actual function being memoized and assert it is only called once.
