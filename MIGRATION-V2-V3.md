Migrating from log21 v2 to v3
=============================

This document describes the changes required when upgrading from **log21 v2** to **log21
v3**.
Most users will only need small adjustments, but **the breaking changes below should be
reviewed first**.

Breaking Changes
----------------

### 1. Module and Package Renaming

In v3, internal modules were **renamed and normalized to lowercase**, and the package
layout was cleaned up to follow modern Python conventions.

If your code imports directly from internal modules (for example
`from log21.Colors import ...`), those imports **will break in v3** and must be updated.

This change does **not** affect public imports from `log21` itself
(e.g. `from log21 import ProgressBar`).

### Old → New Module Mapping

| v2 Module                        | v3 Module                         |
|----------------------------------|-----------------------------------|
| `log21.Argparse`                 | `log21.argparse`                  |
| `log21.Argumentify`              | `log21.argumentify`               |
| `log21.Colors`                   | `log21.colors`                    |
| `log21.CrashReporter`            | `log21.crash_reporter`            |
| `log21.FileHandler`              | `log21.file_handler`              |
| `log21.Formatters`               | `log21.formatters`                |
| `log21.Levels`                   | `log21.levels`                    |
| `log21.Logger`                   | `log21.logger`                    |
| `log21.LoggingWindow`            | `log21.logging_window`            |
| `log21.Manager`                  | `log21.manager`                   |
| `log21.PPrint`                   | `log21.pprint`                    |
| `log21.ProgressBar`              | `log21.progress_bar`              |
| `log21.StreamHandler`            | `log21.stream_handler`            |
| `log21.TreePrint`                | `log21.tree_print`                |

---

### Migration Examples

```diff
- from log21.Colors import get_color
- from log21.ProgressBar import ProgressBar
- from log21.Logger import Logger
+ from log21.colors import get_color
+ from log21.progress_bar import ProgressBar
+ from log21.logger import Logger
```

### Recommendation

Prefer importing from the public `log21` namespace whenever possible:

```python
from log21 import ProgressBar, get_colors, get_logger
```

Public imports are more stable across releases and are explicitly maintained.

### 2. Argumentify Exception Renames

Several exceptions from `argumentify` were renamed in v3 to follow a consistent
`*Error` naming convention.

These changes affect code that explicitly raises or catches these exceptions.

| v2 Exception            | v3 Exception                 |
| ----------------------- | ---------------------------- |
| `ArgumentError`         | `ArgumentError`              |
| `TooFewArguments`       | `TooFewArgumentsError`       |
| `RequiredArgument`      | `RequiredArgumentError`      |
| `IncompatibleArguments` | `IncompatibleArgumentsError` |

### Migration Example

```diff
- except log21.TooFewArguments:
+ except log21.TooFewArgumentsError:
```

```diff
- raise log21.RequiredArgument(...)
+ raise log21.RequiredArgumentError(...)
```

### 3. Crash Reporter Import Change

In v2, the crash reporter was imported via a capitalized module:

```python
from log21 import CrashReporter
```

In v3, it is exposed as a proper lowercase submodule:

```python
import log21.crash_reporter
```

If you only relied on the default reporters(`log21.console_reporter` and
`log21.file_reporter`), no change is required when using the predefined instances
exposed by `log21`.

Upgrade Checklist
-----------------

1. Upgrade the package:

   ```bash
   pip install -U log21
   ```

2. Update imports that reference renamed or capitalized modules

3. Replace renamed Argumentify exceptions (`*Arguments` → `*ArgumentsError`)

4. Verify any direct imports from internal modules

5. Run your tests

Summary
-------

* Internal modules were renamed and lowercased
* Multiple Argumentify exceptions were renamed
* Public API imports were clarified and made explicit
* Crash reporter import path changed
* No behavioral changes in logging, argument parsing, or UI components
* Most projects require minimal or no changes
