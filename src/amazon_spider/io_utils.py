from pathlib import Path
from typing import Iterable, List, Optional

import pandas as pd

from .types import SellerInfo


def read_url_list(
    file_path: str,
    sheet_name: Optional[str] = None,
    column: str = "url",
) -> List[str]:
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {file_path}")

    if path.suffix.lower() in {".xlsx", ".xls"}:
        df = pd.read_excel(path, sheet_name=sheet_name)
    else:
        df = pd.read_csv(path)

    if column not in df.columns:
        raise KeyError(f"Column '{column}' not found in input file. Available: {list(df.columns)}")

    urls = [str(u) for u in df[column].dropna().tolist()]
    return urls


def write_results(
    results: Iterable[SellerInfo],
    output_path: str,
    output_format: Optional[str] = None,
) -> None:
    path = Path(output_path)
    fmt = (output_format or path.suffix.lstrip(".")).lower()
    data = [r.to_dict() for r in results]
    df = pd.DataFrame(data)

    if fmt in {"xlsx", "xls"}:
        df.to_excel(path, index=False)
    elif fmt == "csv":
        df.to_csv(path, index=False)
    elif fmt == "json":
        df.to_json(path, orient="records", force_ascii=False, indent=2)
    else:
        raise ValueError(f"Unsupported output format: {fmt}")