import logging
import pandas as pd
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    datefmt='%H:%M:%S'
)
log = logging.getLogger(__name__)

BASE = Path(__file__).parent.parent.parent
DATA_PATH = BASE / 'dataset' / '2018.csv'
OUTPUT_PATH = BASE / 'dataset' / 'column_properties.csv'


def list_columns():
    log.info(f"Reading first 10,000 rows from {DATA_PATH}")
    df = pd.read_csv(DATA_PATH, nrows=10000)
    log.info(f"Inspecting {len(df.columns)} columns")
    column_info = []

    for col in df.columns:
        info = {
            'column':         col,
            'dtype':          str(df[col].dtype),
            'non_null_count': df[col].count(),
            'null_count':     df[col].isnull().sum(),
            'null_percent':   round(df[col].isnull().mean() * 100, 2),
            'unique_values':  df[col].nunique(),
            'sample_values':  str(df[col].dropna().head(3).tolist()),
        }

        if df[col].dtype in ['int64', 'float64']:
            info['min']  = df[col].min()
            info['max']  = df[col].max()
            info['mean'] = round(df[col].mean(), 2)
        else:
            info['min']  = None
            info['max']  = None
            info['mean'] = None

        log.info(f"  {col} | {info['dtype']} | nulls: {info['null_percent']}%")
        column_info.append(info)

    result = pd.DataFrame(column_info)
    result.to_csv(OUTPUT_PATH, index=False)
    log.info(f"Saved column properties to {OUTPUT_PATH}")
    print(result.to_string(index=False))
    return result


if __name__ == "__main__":
    list_columns()