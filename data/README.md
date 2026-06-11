# Data

The raw census datasets are **not** included in this repository (they are
distributed with the assessment and are not redistributed here).

To run the notebooks, place the following files in this `data/` directory:

```
data/
├── census_income_learn.csv     # training set (~199K rows)
└── census_income_test.csv      # test set (~100K rows)
```

The files have no header row; column names and ordering are defined in
[`src/utils.py`](../src/utils.py) (`COLUMN_NAMES`), taken from the dataset
metadata.

The notebooks load these via `TRAIN_PATH` / `TEST_PATH` from `src/utils.py`,
so no path changes are needed once the files are in place.
