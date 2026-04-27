
### 1. Initialize the Project with `uv`

Instead of just creating a virtual environment, we use `uv init` to create a managed project structure with a `pyproject.toml` file.



# Create and enter project directory
```powershell
mkdir django_project
cd django_project
```


# Initialize uv project

```powershell
uv init
```


# Add Django and essential production-ready dependencies

```powershell
uv add django django-environ python-dotenv ruff mypy

uv add --dev pytest pytest-django
```



- **Rationale:** `uv` handles dependency resolution much faster than `pip` and creates a lockfile (`uv.lock`) for deterministic builds.

---

### 2. Scaffold the Django Project

We use `uv run` to execute Django commands without needing to manually manage the activation state of the environment in every step.

```powershell
# Create the Django project structure

# We use 'core' as the project name and '.' to avoid nested directories

uv run django-admin startproject core .
```


---

### 3. Production Best Practices: Configuration & Security

#### A. Externalize Configuration (`.env`)

Never hardcode secrets like `SECRET_KEY` or database credentials. Create a `.env` file in the root:


```ini
# .env

DEBUG=True

SECRET_KEY=your-very-secure-secret-key

DATABASE_URL=sqlite:///db.sqlite3

ALLOWED_HOSTS=localhost,127.0.0.1
```


#### B. Modular Settings (Refactor `core/settings.py`)

Modify your `settings.py` to use `django-environ`. This allows for seamless transitions between dev, staging, and production.

```python
import environ
import os
from pathlib import Path

# Initialize environment variables

env = environ.Env(
    DEBUG=(bool, False)
)

BASE_DIR = Path(__file__).resolve().parent.parent

# Read .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

SECRET_KEY = env('SECRET_KEY')

DEBUG = env('DEBUG')

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

# Security Headers (Essential for Production)

SECURE_BROWSER_XSS_FILTER = True

SECURE_CONTENT_TYPE_NOSNIFF = True

X_FRAME_OPTIONS = 'DENY'
```


---
### 4. Static Analysis & Linting Setup

To adhere to your requirement for **Static Code Analysis**, we configure **Ruff** (the fastest Python linter/formatter) and **Mypy**.

Create a `ruff.toml` in the root:

```toml
line-length = 88

select = ["E", "F", "I", "N", "UP", "B"]

[lint]

ignore = ["D100", "D104"] # Example: ignore missing docstrings in modules/packages temporarily
```

Run linting checks:

```powershell
uv run ruff check .
```

---
### 5. Advanced Project Structure (Modular OOP)

When creating apps, follow a modular pattern. Use custom managers and service layers to keep models and views thin.

```powershell
# Create a new app

uv run python manage.py startapp users
```

**Best Practice: Type Hinting in Views**

```python

from django.http import HttpRequest, HttpResponse

from django.shortcuts import render

def index(request: HttpRequest) -> HttpResponse:

    """

    Renders the homepage.

    Args:

        request (HttpRequest): The incoming web request.

    Returns:

        HttpResponse: The rendered HTML response.

    """

    return render(request, 'index.html')
```

---

### 6. Summary of Execution Commands

To run your project daily:

1. **Start Dev Server:** `uv run python manage.py runserver`
2. **Make Migrations:** `uv run python manage.py makemigrations`
3. **Apply Migrations:** `uv run python manage.py migrate`
4. **Run Tests:** `uv run pytest`
5. **Lint Code:** `uv run ruff check . --fix`

### Why `uv` for Django?

- **Speed:** Installing dependencies is up to 10-100x faster than `pip`.
- **Single Tool:** It replaces `pip`, `venv`, `pip-tools`, and `pyenv`.
- **Reproducibility:** The `uv.lock` file ensures every developer (and your CI/CD pipeline) uses the exact same versions of every package.