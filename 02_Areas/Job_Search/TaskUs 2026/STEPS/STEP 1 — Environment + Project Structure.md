

# [x] 1. Create the Project Folder

Open your terminal in the location where you want the project.

Run:

```
mkdir adidas-chatbot-casecd adidas-chatbot-case
```

---

# [x] 2. Initialize Git (Recommended)

```
git init
```

This is useful because:

- shows engineering discipline
- allows version tracking
- lets you rollback mistakes safely

---

# [x] 3. Create Virtual Environment

You have 2 good options:

| Option     | Recommendation     |
| ---------- | ------------------ |
| uv         | Best modern choice |
| venv + pip | Simpler fallback   |

Since you already want good practices:  
use `uv`.

---

# [x] 4. Install `uv` (If Needed)

## Windows PowerShell

```
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Verify:

```
uv --version
```

---

# [x] 5. Initialize Python Project

```
uv init
```

This creates:

- `pyproject.toml`
- initial project metadata

---

# [x] 6. Pin Python Version

```
uv python pin 3.12
```

---

# [x] 7. Create Virtual Environment

```
uv venv
```

Activate it.

## Windows

```
.venv\Scripts\activate
```

## Mac/Linux

```
source .venv/bin/activate
```

---

# [x] 8. Install ONLY the Dependencies We Actually Need

Keep it lightweight.

Run:

```
uv add pandas numpy matplotlib seaborn plotly openpyxl jupyterlab
```

These are enough for:

- Excel ingestion
- EDA
- KPI analysis
- charts
- notebook workflow

---

# [x] 9. Install Dev Dependencies

```
uv add --dev ruff mypy ipykernel
```

Why:

- Ruff → linting
- mypy → typing discipline
- ipykernel → notebook integration

Minimal and professional.

---

# [x] 10. Create the Folder Structure

Inside the project root:

```
adidas-chatbot-case/│├── data/│   ├── raw/│   └── processed/│├── notebooks/│├── src/│├── dashboards/│   ├── powerbi/│   └── react-mockup/│├── presentation/│├── exports/│├── README.md├── .gitignore└── pyproject.toml
```

---

# [x] 11. Create Folders Quickly

## Windows PowerShell

```
mkdir data, notebooks, src, dashboards, presentation, exportsmkdir data/raw, data/processedmkdir dashboards/powerbi, dashboards/react-mockup
```

---

# [x] 12. Move the Excel File

Put:

```
Business Case - Chatbot data - Raw Data.xlsx
```

inside:

```
data/raw/
```

---

# [x] 13. Create `.gitignore`

Create `.gitignore`

Add:

```
.venv/__pycache__/.ipynb_checkpoints/*.pyc.DS_Storeexports/data/processed/
```

---

# [x] 14. Create README.md

Minimal initial version:

```
# Adidas LAM Chatbot Analytics CaseAnalytics and operational optimization study for Adidas LATAM chatbot support operations.## ObjectiveAnalyze chatbot operational performance and identify opportunities to improve:- Containment rate- Resolution rate- Repeat contact reduction## Stack- Python 3.12- Pandas- Plotly- Seaborn- Jupyter- Power BI## Structure- `data/`: raw and processed datasets- `notebooks/`: EDA and KPI analysis- `src/`: reusable helper functions- `dashboards/`: Power BI and React dashboard assets- `presentation/`: final presentation materials
```

---

# 15. Expected Final Result

You should now have:

## Environment

- Python 3.12
- virtual environment active
- dependencies installed

## Structure

- clean project folders
- Excel file organized
- notebook-ready workspace

---

# 16. DO NOT Continue Yet

Before moving to STEP 2,  
show me:

1. Your folder tree
2. Your `pyproject.toml`
3. Confirmation dependencies installed correctly
4. Any installation errors if they happened

Then I’ll validate everything before we continue to:

- data ingestion
- schema inspection
- KPI reconciliation
- notebook setup

properly.