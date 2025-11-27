# Exhaustive Procedural Checklist of Python Programming Best Practices


#### 1. General Principles and Philosophies
1. Enforce DRY (Don't Repeat Yourself): Extract repeated logic into reusable functions, classes, modules, or utilities to avoid code duplication.
2. Apply KISS (Keep It Simple, Stupid): Use simple, readable solutions; avoid over-engineering or unnecessary complexity.
3. Apply YAGNI (You Ain't Gonna Need It): Never add unrequested features, abstractions, or functionality.
4. Apply SOLID principles: Ensure single responsibility per class or function; design for open extension via composition or inheritance while closed for modification; use interface segregation, dependency inversion, and Liskov substitution where appropriate.
5. Follow the Zen of Python (import this): Prioritize beautiful, explicit, simple, and readable code; errors should never pass silently unless explicitly handled; prefer flat over nested structures; sparsity over density; and one obvious way to do things.
6. Practicality beats purity: When theoretical elegance conflicts with real-world needs, choose pragmatic solutions.
7. Refuse ambiguity: Avoid guessing in unclear situations; validate inputs and document assumptions.
8. Readability counts: Always prioritize code that is easy to read and understand over clever or dense implementations.
9. Special cases aren't special enough to break rules, but be practical when needed.
10. Namespaces are great: Use modules and packages to organize code and prevent name conflicts.

#### 2. Code Style and Formatting (PEP 8 Compliance)
11. Enforce PEP 8: Limit lines to 79-99 characters (72 for docstrings/comments); use snake_case for variables/functions, CamelCase for classes; sort imports; use descriptive names.
12. Indentation: Use 4 spaces per level; never mix tabs and spaces; align continuation lines vertically or use hanging indents.
13. Blank lines: Surround top-level functions/classes with 2 blank lines; methods inside classes with 1; use sparingly for logical grouping.
14. Whitespace in expressions: Single spaces around operators (=, ==, +, etc.); no extraneous spaces inside parentheses/brackets/braces or before commas/colons/semicolons.
15. Binary operators: Break lines before operators for readability; surround with equal spaces.
16. Trailing commas: Use in lists/dicts/arguments for easier extension; required for single-element tuples.
17. String quotes: Consistent use of single or double quotes; prefer double for triple-quoted strings; use opposite inside to avoid escapes.
18. Avoid trailing whitespace: Strip it everywhere to prevent issues.
19. Format automatically: Use Black for code formatting, isort (with Black profile) for import sorting.
20. Lint and check: Use flake8 for style enforcement, mypy for type checking (strict mode), bandit for security scans.
21. Require pre-commit hooks: Enforce Black, isort, flake8, mypy, and bandit on every commit to maintain consistency.
22. Source encoding: Use UTF-8; ASCII-compatible identifiers; avoid non-ASCII unless necessary (e.g., for names/places).

#### 3. Imports
23. Place imports at the top: After docstrings, before globals/constants; group standard library, third-party, local; separate groups with blank lines.
24. Prefer absolute imports: For readability; use explicit relative only in complex packages.
25. Avoid wildcard imports (*): They pollute namespaces and obscure origins.
26. Module-level dunders: Place __all__, __version__, etc., after docstring but before other imports (except __future__).

#### 4. Naming Conventions
27. Descriptive names: Use clear, concise variable/function names reflecting usage (e.g., verbs for functions like calculate_total); avoid single-letter names like 'l', 'O', 'I'.
28. Variables/functions/methods: lowercase_with_underscores.
29. Classes: CamelCase.
30. Constants: UPPERCASE_WITH_UNDERSCORES.
31. Exceptions: CamelCase with "Error" suffix if error-related.
32. Type variables: CamelCase, short (e.g., T, Num); add _co/_contra for variance.
33. Non-public: Single leading underscore (_private_var) for internal use.
34. Name mangling: Double leading underscore (__mangled) for class attributes to avoid subclass conflicts.
35. Avoid keyword conflicts: Append trailing underscore (e.g., class_).
36. Globals: Same as functions; use __all__ to control exports.

#### 5. Documentation and Comments
37. Write docstrings: For all public modules, functions, classes, methods; use Google-style or reStructuredText for clarity.
38. One-line docstrings: Imperative phrase ending in period; triple quotes, closing on same line.
39. Multi-line docstrings: Summary line, blank line, then details; closing quotes on own line; document args, returns, exceptions, side effects.
40. Comments: Complete sentences; block comments indented to code level, starting with # ; inline comments separated by 2 spaces, used sparingly for non-obvious parts.
41. Keep comments updated: Contradictory comments are worse than none; use English.
42. Attribute docstrings: For module/class attributes, place string literal right after assignment.
43. Scripts: Use module docstring as usage message covering function, syntax, and dependencies.

#### 6. Type Hints and Static Analysis
44. Add type hints everywhere: Use typing module; avoid Any; enable strict mypy mode for full checks.
45. Function annotations: Follow PEP 484; space after colon, around -> (e.g., def func(arg: int) -> str:).

#### 7. Pythonic Idioms and Code Writing
46. Write Pythonic code: Use list/dict/set comprehensions; generator expressions; context managers (with statements); f-strings for formatting; walrus operator (:=) only where it improves clarity.
47. Use builtins efficiently: startswith/endswith over slicing; isinstance over type(); if seq/not seq over len(seq).
48. Boolean checks: if greeting (not == True); avoid comparing to True/False.
49. Returns: Consistent (all with values or all explicit None); add explicit return at end if reachable.
50. Lambdas: Prefer def for named functions (better tracebacks); use lambdas only for simple, anonymous cases.
51. Comparisons: Use is/is not for singletons like None; implement all rich methods (__eq__, etc.) for custom classes.

#### 8. Error Handling and Exceptions
52. Handle errors properly: Catch specific exceptions only; no bare except: (use except Exception:); log tracebacks.
53. Define custom exceptions: For domain-specific errors (e.g., ValueNotFoundError inheriting from Exception).
54. Raise explicitly: Use raise X from Y for chaining; don't silence errors without intent.
55. Derive from Exception: Not BaseException; add "Error" suffix for errors.
56. Minimize try blocks: Only wrap necessary code.
57. Use with for resources: Ensures cleanup via context managers.

#### 9. Testing and Refactoring
58. Follow TDD: Write unit tests before code; test every bug fix and refactor to preserve behavior.
59. Write unit tests: For functions, classes; aim for high coverage.
60. Refactor triggers: >2 duplicates, function >30 lines, nesting >3 levels; extract methods or simplify.
61. Use pytest or unittest: For test frameworks; include assertions and edge cases.

#### 10. Project Structure and Dependencies
62. Structure project: Use src/package for code; separate config, tests (unit/integration); follow modular design.
63. Use virtual environments: Isolate dependencies; lock in requirements.txt via pip freeze.
64. Scan dependencies: Use safety or similar for vulnerability checks.
65. Manage config: Via environment variables or config files; never hardcode sensitive data.

#### 11. Performance, Optimization, and Monitoring
66. Optimize judiciously: Avoid premature optimization; profile first.
67. Monitor runtime: Log start/end of long operations; track memory/CPU with psutil if needed.
68. Use efficient structures: Sets for membership; deques for queues; avoid lists for large FIFO.
69. Join strings with ''.join() over + for performance.

#### 12. Security and Maintenance
70. Secure code: Avoid eval/exec unless necessary; validate inputs; use secrets module for cryptography.
71. Design for inheritance: Make attributes non-public by default; use properties for data access.
72. Public vs. internal: Use __all__ for public APIs; underscore for internal.

This checklist covers a procedural flow: Start with principles, enforce style, document, handle errors, test, structure, and optimize. Apply iteratively during development.

### Links to Official Resources and Documentation

To confirm these industry-standard practices, refer to the following official and authoritative sources:

- PEP 8 – Style Guide for Python Code: https://peps.python.org/pep-0008/  (Core coding conventions for readability and consistency.)
- PEP 20 – The Zen of Python: https://peps.python.org/pep-0020/  (Philosophical guidelines for Python design.)
- PEP 257 – Docstring Conventions: https://peps.python.org/pep-0257/  (Standards for writing documentation strings.)
- The Hitchhiker's Guide to Python: https://docs.python-guide.org/  (Community-driven best practices handbook, covering structure, style, and more.)
- Python Official Documentation: https://www.python.org/doc/  (Includes tutorials, library references, and how-tos.)
- Google Python Style Guide: https://google.github.io/styleguide/pyguide.html  (Supplementary guide with detailed examples, often aligned with PEP 8.)

These resources are directly from python.org or endorsed community efforts, ensuring they represent official standards as of November 22, 2025.
