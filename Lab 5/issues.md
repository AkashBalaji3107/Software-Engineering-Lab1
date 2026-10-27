# Static Code Analysis - Issue Documentation

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---|---|---|
| Insecure SSL Context (B501/B506) | Security (Bandit) | 57 | Used `ssl._create_unverified_context()` disabling SSL certificate verification. | Replaced with `ssl.create_default_context()` to enforce valid TLS/SSL verification. |
| Insecure XML Parsing (B318/B320) | Security (Bandit) | 47 | Standard library `xml.etree.ElementTree` is vulnerable to XML Entity Expansion and DTD attacks. | Replaced with `defusedxml.ElementTree` to prevent XML vulnerabilities. |
| Weak PRNG for Security/Policy ID (B311) | Security (Bandit) | 35 | Standard `random.randint` is pseudorandom and predictable. | Replaced with `secrets.randbelow()` for cryptographically secure pseudo-random generation. |
| Hardcoded Host Bind `0.0.0.0` (B104) | Security (Bandit) | 12 | Binding to all interfaces (`0.0.0.0`) exposes application to unexpected network interfaces. | Bound to `127.0.0.1` by default and configured via environment variable `APP_HOST`. |
| Mutable Default Argument (W0102) | Bug / Logic (Pylint) | 16 | `discounts=[]` retains modified list state across independent function calls. | Changed default parameter to `discounts=None` and created a local copy inside function body. |
| Bare `except:` Clause (W0702) | Bug / Quality (Pylint) | 53 | Catching bare `except:` intercepts system interrupts (`KeyboardInterrupt`, `SystemExit`). | Changed to catch specific exceptions `(ValueError, TypeError)`. |
| Unclosed File Resource (R1732) | Resource Leak (Pylint) | 41-43 | `open()` was used without a context manager, risking file descriptor leaks. | Wrapped file access in `with open(...) as file:` context manager with explicit UTF-8 encoding. |
| PEP 8 Function Naming (C0103 / N802) | Style (Flake8 / Pylint) | 16, 28, 34, 38 | Function names used `camelCase` (e.g., `calculatePremium`, `ageFromDob`). | Refactored all function and variable identifiers to PEP 8 compliant `snake_case`. |