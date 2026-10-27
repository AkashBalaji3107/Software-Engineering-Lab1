# Lab 5: Reflection on Static Code Analysis

### 1. What is the value of static analysis in software development?
Static code analysis detects security flaws, logic traps, and style drift without needing code execution. It catches edge cases (like mutable default arguments and resource leaks) early in the development lifecycle before code hits production.

### 2. How did Pylint, Bandit, and Flake8 complement each other during this lab?
Each tool addresses a different dimension of software health:
- **Bandit** operates as a security auditor, identifying dangerous function calls, injection vulnerabilities, and weak cryptography.
- **Pylint** acts as a strict code-quality inspector, identifying logical design flaws, anti-patterns, and unhandled exceptions.
- **Flake8** enforces consistency across formatting, indentation, and standard PEP 8 naming conventions.

### 3. Which issue was the most critical to resolve and why?
The mutable default argument (`discounts=[]`) in `calculatePremium` was the most insidious business logic bug. Because default lists are instantiated once when the function is defined, each invocation appended values to the shared list, silently compounding discounts for subsequent customers. The Bandit XML and SSL vulnerabilities were equally critical from a security standpoint, as they left the application open to Man-in-the-Middle (MitM) and XML denial-of-service exploits.

### 4. How will you integrate static analysis tools into your development workflow going forward?
I will configure these linters as Git pre-commit hooks using `pre-commit` and run them automatically inside CI/CD pipelines (such as GitHub Actions) to block non-compliant code from merging.