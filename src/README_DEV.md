Development setup

Install dev dependencies (recommended in a virtualenv):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -U pip
python -m pip install -r requirements-dev.txt
```

Run tests:

```powershell
python -m pytest
```

