"""
src/utils/helpers.py
--------------------
Shared utility functions used across all GameZone Analytics notebooks.
Import with: from utils.helpers import load_orders, get_db_engine
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
from pathlib import Path
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load .env file for database credentials (never hardcode passwords)
load_dotenv()

# ── Paths ──────────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parents[2]
RAW_DATA_PATH = ROOT / "data" / "raw" / "gamezone-orders-data.xlsx"
PROCESSED_PATH = ROOT / "data" / "processed"
FIGURES_PATH = ROOT / "reports" / "figures"
EXCEL_OUTPUT_PATH = ROOT / "reports" / "excel_outputs"


# ── Data loading ───────────────────────────────────────────────────────────────
def load_orders(cleaned: bool = True) -> pd.DataFrame:
    """
    Load GameZone orders from the raw Excel file.

    Parameters
    ----------
    cleaned : bool
        If True (default), apply standard cleaning rules:
        - Parse datetimes
        - Standardise product names
        - Drop $0 prices
        - Fill known nulls

    Returns
    -------
    pd.DataFrame
    """
    df = pd.read_excel(RAW_DATA_PATH, sheet_name="orders")
    region = pd.read_excel(RAW_DATA_PATH, sheet_name="region")

    df = df.merge(region, on="COUNTRY_CODE", how="left")

    if cleaned:
        df = _clean_orders(df)

    return df


def _clean_orders(df: pd.DataFrame) -> pd.DataFrame:
    """Apply standard cleaning rules to raw orders DataFrame."""
    df = df.copy()

    # Parse timestamps
    df["PURCHASE_TS"] = pd.to_datetime(df["PURCHASE_TS"], errors="coerce")
    df["SHIP_TS"] = pd.to_datetime(df["SHIP_TS"], errors="coerce")

    # Fulfilment days (negative = shipped before purchase — an anomaly)
    df["FULFILMENT_DAYS"] = (df["SHIP_TS"] - df["PURCHASE_TS"]).dt.days

    # Standardise duplicate product names
    df["PRODUCT_NAME"] = df["PRODUCT_NAME"].replace(
        {"27inches 4k gaming monitor": "27in 4K gaming monitor"}
    )

    # Fill nulls with 'unknown' for categorical columns
    for col in ["MARKETING_CHANNEL", "ACCOUNT_CREATION_METHOD"]:
        df[col] = df[col].fillna("unknown")

    # Drop $0 prices (cancelled / test orders)
    df = df[df["USD_PRICE"] > 0].copy()

    # Convenience columns
    df["PURCHASE_YEAR"] = df["PURCHASE_TS"].dt.year
    df["PURCHASE_MONTH"] = df["PURCHASE_TS"].dt.month
    df["PURCHASE_YEARMONTH"] = df["PURCHASE_TS"].dt.to_period("M")

    return df.reset_index(drop=True)


# ── Database ───────────────────────────────────────────────────────────────────
def get_db_engine():
    """
    Create a SQLAlchemy engine for MySQL using credentials from .env.

    Required .env variables:
        DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME

    Returns
    -------
    sqlalchemy.engine.Engine
    """
    user = os.getenv("DB_USER", "root")
    password = os.getenv("DB_PASSWORD", "")
    host = os.getenv("DB_HOST", "127.0.0.1")
    port = os.getenv("DB_PORT", "3306")
    name = os.getenv("DB_NAME", "gamezone_analytics")

    url = f"mysql+pymysql://{user}:{password}@{host}:{port}/{name}"
    return create_engine(url)


def run_query(sql: str, engine=None) -> pd.DataFrame:
    """
    Execute a SQL query and return results as a DataFrame.

    Parameters
    ----------
    sql : str
        SQL query string.
    engine : sqlalchemy.engine.Engine, optional
        If None, calls get_db_engine() automatically.

    Returns
    -------
    pd.DataFrame
    """
    if engine is None:
        engine = get_db_engine()
    with engine.connect() as conn:
        return pd.read_sql(text(sql), conn)


# ── Plotting ───────────────────────────────────────────────────────────────────
def set_style():
    """Apply a clean, consistent style to all matplotlib/seaborn plots."""
    sns.set_theme(style="whitegrid", palette="muted", font_scale=1.1)
    plt.rcParams.update(
        {
            "figure.figsize": (12, 5),
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.titlesize": 14,
            "axes.titleweight": "medium",
            "figure.dpi": 120,
        }
    )


def save_figure(fig: plt.Figure, filename: str, tight: bool = True):
    """
    Save a matplotlib figure to reports/figures/.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
    filename : str
        e.g. 'monthly_revenue.png' — extension determines format.
    tight : bool
        Apply tight_layout before saving (default True).
    """
    FIGURES_PATH.mkdir(parents=True, exist_ok=True)
    if tight:
        fig.tight_layout()
    fig.savefig(FIGURES_PATH / filename, bbox_inches="tight")
    print(f"Figure saved → reports/figures/{filename}")
