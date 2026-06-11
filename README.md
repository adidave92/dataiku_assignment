# US Census Income Analysis
## Dataiku Senior Data Scientist Technical Assessment

Binary classification: predict whether an individual earns >= $50,000/year using
US Census Bureau data (~300,000 individuals, 40 features).

---

## Data Files

The raw datasets are **not** included in this repository (they ship with the
assessment and are not redistributed). Before running the notebooks, place these
files in the [`data/`](data/) directory:

```
data/
├── census_income_learn.csv     # training set
└── census_income_test.csv      # test set
```

See [`data/README.md`](data/README.md) for details. Column names/ordering are
defined in [`src/utils.py`](src/utils.py).

---

## Quick Start

### Option 1: uv (recommended -- fastest, reproducible)

```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install all dependencies from the lockfile
uv sync

# macOS only: fix LightGBM's libomp dependency
# Option A -- if you have Homebrew:
brew install libomp

# Option B -- automated download (no Homebrew needed):
uv run python -c "
import urllib.request, zstandard, zipfile, tarfile
from pathlib import Path
lib_dir = Path.home() / '.local' / 'lib'
lib_dir.mkdir(parents=True, exist_ok=True)
if not (lib_dir / 'libomp.dylib').exists():
    print('Downloading libomp...')
    urllib.request.urlretrieve(
        'https://conda.anaconda.org/conda-forge/osx-arm64/llvm-openmp-22.1.7-hc7d1edf_0.conda',
        '/tmp/llvm-openmp.conda'
    )
    with zipfile.ZipFile('/tmp/llvm-openmp.conda') as zf:
        zf.extract('pkg-llvm-openmp-22.1.7-hc7d1edf_0.tar.zst', '/tmp')
    dctx = zstandard.ZstdDecompressor()
    with open('/tmp/pkg-llvm-openmp-22.1.7-hc7d1edf_0.tar.zst','rb') as fi, open('/tmp/tmp.tar','wb') as fo:
        dctx.copy_stream(fi, fo)
    with tarfile.open('/tmp/tmp.tar') as tar:
        m = tar.getmember('lib/libomp.dylib'); m.name='libomp.dylib'; tar.extract(m, str(lib_dir))
    print('libomp installed')
else:
    print('libomp already present')
"

# Launch JupyterLab
# macOS: the DYLD_LIBRARY_PATH prefix is required for LightGBM to find libomp
DYLD_LIBRARY_PATH="$HOME/.local/lib:$DYLD_LIBRARY_PATH" uv run jupyter lab
```

### Option 2: pip + venv (no uv required)

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

pip install -r requirements.txt

# macOS: install libomp via Homebrew (required for LightGBM)
brew install libomp

DYLD_LIBRARY_PATH="$(brew --prefix libomp)/lib:$DYLD_LIBRARY_PATH" jupyter lab
```

### VS Code / Cursor users

After running `uv sync` or `pip install -r requirements.txt`, register the kernel:

```bash
# From the project root:
.venv/bin/python -m ipykernel install --user \
  --name census-income-analysis \
  --display-name "census-income-analysis (3.11)"
```

Then in VS Code: open a notebook, click the kernel selector (top right), and
choose **census-income-analysis (3.11)**.

---

## Execution Order

**Prerequisite:** place the census CSVs in [`data/`](data/) first (see
[Data Files](#data-files) above) — the notebooks will not run without them.

Run in sequence. Each stage depends on outputs from the previous.

### 1. Exploratory Data Analysis
Open `code/01_eda.ipynb` and run all cells.

**Outputs:** `outputs/figures/01_*.png` through `16_*.png`, `docs/eda_insights.md`

### 2. Feature Engineering and Modeling
Open `code/02_modeling.ipynb` and run all cells.

**Outputs:** `outputs/figures/17_*.png` through `24_*.png`,
`outputs/models/lgbm_pipeline.joblib`, `outputs/models/metrics.json`,
`docs/modeling_decisions.md`

**Note:** The Optuna hyperparameter search (60 trials) takes approximately
5-10 minutes depending on hardware.

---

## Key Results

| Model | ROC-AUC | PR-AUC |
|---|---|---|
| Logistic Regression | 0.9457 | 0.6067 |
| Random Forest | 0.9443 | 0.5966 |
| **LightGBM (tuned)** | **0.9550** | **0.6800** |

Optimal F1 threshold: 0.857 -- Recall 89.6%, Precision 31.7%, F1 0.468

---

## Project Structure

```
dataiku_assignment/
├── pyproject.toml              # uv-managed environment (source of truth)
├── requirements.txt            # pip-compatible export of the lockfile
├── uv.lock                     # pinned, fully reproducible dependency lockfile
├── README.md                   # this file
├── data/                       # place the census CSVs here (not in repo)
│   └── README.md
├── src/
│   └── utils.py                # column names, constants, shared helpers
├── code/
│   ├── 01_eda.ipynb            # exploratory data analysis
│   └── 02_modeling.ipynb       # feature engineering + modeling + evaluation
├── outputs/
│   ├── figures/                # all seaborn plots (PNG)
│   ├── models/                 # trained pipeline, preprocessor, metrics
│   └── census_data_dictionary.xlsx
└── slides/                     # presentation deck (PPTX)
```

> Note: `outputs/models/X_test_prep.npy` (a large preprocessed array) and the
> `docs/*.md` write-ups are regenerated when the notebooks run, so they are not
> committed.

---

## Key Modeling Choices

- **Instance weights** used for population-representative statistics in EDA (not in modeling)
- **ROC-AUC and PR-AUC** as primary metrics (accuracy is misleading with 93.8% class imbalance)
- **Target encoding** for high-cardinality categoricals (state, country, occupation)
- **scale_pos_weight** in LightGBM over SMOTE (preserves data integrity with stratified sample)
- **Threshold tuning** via F1 sweep rather than defaulting to 0.5
- **SHAP** for model interpretability (global + individual explanations)

---

## Troubleshooting

**LightGBM import error on macOS:** `Library not loaded: libomp.dylib` -- install
libomp via `brew install libomp` and prefix your run command with
`DYLD_LIBRARY_PATH="$(brew --prefix libomp)/lib:$DYLD_LIBRARY_PATH"`.

**Kernel not found in VS Code:** Run the `ipykernel install` command above, then
reload the VS Code window (`Cmd+Shift+P` > Developer: Reload Window).
