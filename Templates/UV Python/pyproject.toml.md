
```toml
[tool.ruff]
line-length = 88
fix = true

[tool.ruff.lint]
select = ["E", "F", "I", "B", "UP"]
ignore = []

[tool.ruff.format]
quote-style = "double"
indent-style = "space"

[tool.mypy]
strict = true

# Paths (relativos para portabilidad)
exclude = ["tests/", "migrations/"]

# Type safety
disallow_untyped_defs = true
check_untyped_defs = true
no_implicit_optional = true

# Quality checks
warn_return_any = true
warn_unused_ignores = true

# Imports (útil en DS / ML)
ignore_missing_imports = true

# Output
pretty = true
show_error_codes = true
```

