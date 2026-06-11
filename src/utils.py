"""Shared constants and helpers for the census income analysis."""

from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
FIGURES_DIR = OUTPUTS_DIR / "figures"
MODELS_DIR = OUTPUTS_DIR / "models"
PROCESSED_DIR = OUTPUTS_DIR / "processed"
DOCS_DIR = PROJECT_ROOT / "docs"

TRAIN_PATH = DATA_DIR / "census_income_learn.csv"
TEST_PATH = DATA_DIR / "census_income_test.csv"

# ---------------------------------------------------------------------------
# Column definitions (raw CSV has no header; order from metadata)
# ---------------------------------------------------------------------------
COLUMN_NAMES = [
    "age",
    "class_of_worker",
    "detailed_industry_recode",
    "detailed_occupation_recode",
    "education",
    "wage_per_hour",
    "enroll_edu_inst",
    "marital_status",
    "major_industry_code",
    "major_occupation_code",
    "race",
    "hispanic_origin",
    "sex",
    "labor_union_member",
    "reason_for_unemployment",
    "employment_stat",
    "capital_gains",
    "capital_losses",
    "dividends_from_stocks",
    "tax_filer_status",
    "region_prev_residence",
    "state_prev_residence",
    "household_family_stat",
    "household_summary",
    "instance_weight",
    "migration_msa",
    "migration_reg",
    "migration_within_reg",
    "live_here_1yr_ago",
    "migration_sunbelt",
    "num_persons_employer",
    "family_members_under18",
    "birth_country_father",
    "birth_country_mother",
    "birth_country_self",
    "citizenship",
    "own_business_self_employed",
    "veteran_admin_questionnaire",
    "veterans_benefits",
    "weeks_worked_year",
    "year",
    "income",
]

CONTINUOUS_COLS = [
    "age",
    "wage_per_hour",
    "capital_gains",
    "capital_losses",
    "dividends_from_stocks",
    "num_persons_employer",
    "weeks_worked_year",
]

# Migration columns are structurally missing for non-movers ("Not in universe")
MIGRATION_COLS = [
    "migration_msa",
    "migration_reg",
    "migration_within_reg",
    "migration_sunbelt",
    "live_here_1yr_ago",
]

TARGET_COL = "income"
INSTANCE_WEIGHT_COL = "instance_weight"

# Education ordered from lowest to highest (for ordinal encoding)
EDUCATION_ORDER = [
    "Less than 1st grade",
    "1st 2nd 3rd or 4th grade",
    "5th or 6th grade",
    "7th and 8th grade",
    "9th grade",
    "10th grade",
    "11th grade",
    "12th grade no diploma",
    "High school graduate",
    "Some college but no degree",
    "Associates degree-occup /vocational",
    "Associates degree-academic program",
    "Bachelors degree(BA AB BS)",
    "Masters degree(MA MS MEng MEd MSW MBA)",
    "Prof school degree (MD DDS DVM LLB JD)",
    "Doctorate degree(PhD EdD)",
]

# Seaborn palette -- keys must match the string hue column values used in plots
INCOME_LABELS = {0: "< $50K", 1: ">= $50K"}
INCOME_PALETTE = {INCOME_LABELS[0]: "#4C72B0", INCOME_LABELS[1]: "#DD8452"}

# Target encoding for binary labels
TARGET_MAP = {"- 50000": 0, "50000+": 1}

# Columns to drop before modeling (non-feature or redundant)
COLS_TO_DROP = [
    INSTANCE_WEIGHT_COL,
    "detailed_industry_recode",    # redundant with major_industry_code
    "detailed_occupation_recode",  # redundant with major_occupation_code
]

# High-cardinality columns that benefit from target encoding
HIGH_CARDINALITY_COLS = [
    "household_family_stat",
    "state_prev_residence",
    "birth_country_father",
    "birth_country_mother",
    "birth_country_self",
    "major_industry_code",
    "major_occupation_code",
]

# Low-cardinality columns for one-hot encoding
LOW_CARDINALITY_COLS = [
    "class_of_worker",
    "education",
    "enroll_edu_inst",
    "marital_status",
    "race",
    "hispanic_origin",
    "sex",
    "labor_union_member",
    "reason_for_unemployment",
    "employment_stat",
    "tax_filer_status",
    "region_prev_residence",
    "household_summary",
    "migration_msa",
    "migration_reg",
    "migration_within_reg",
    "live_here_1yr_ago",
    "migration_sunbelt",
    "family_members_under18",
    "citizenship",
    "own_business_self_employed",
    "veteran_admin_questionnaire",
    "veterans_benefits",
    "year",
]

FIGURE_DPI = 150
FIGURE_SIZE_DEFAULT = (12, 6)
RANDOM_STATE = 42
