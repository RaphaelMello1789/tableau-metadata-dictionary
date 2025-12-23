"""
Exports Tableau calculated fields metadata to a CSV file.

This script resolves a Tableau `.twb` or `.twbx` file, extracts calculated
fields based on predefined name prefixes, and writes the result to a CSV
file for further analysis or documentation.
"""

from pathlib import Path
import pandas as pd

from verificar_twb_ou_twbx import verificar_twb_ou_twbx
from extracao_de_campos import get_calculated_fields


BASE_DIR = Path(__file__).resolve().parents[2]
DATA_OUTPUT_DIR = BASE_DIR / "data" / "output"
DATA_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def main() -> None:
    """
    Runs the calculated fields extraction pipeline.

    The function resolves the input Tableau file, extracts calculated fields
    that match the configured prefixes, and saves the output as a CSV file.
    """

    tableau_file = Path(
        r"C:\Users\User\Desktop\Portfolio_Layout01_Superstore.twbx"
    )

    xml_path = verificar_twb_ou_twbx(tableau_file)

    prefixes = (
        "kpi_",
        "hp_",
        "prmt_",
        "filter_",
        "dt_",
        "aux_",
        "fmt_",
        "var_",
    )

    fields = get_calculated_fields(xml_path, prefixes=prefixes)

    output_file = DATA_OUTPUT_DIR / "campos_calculados_sample.csv"

    pd.DataFrame(fields).to_csv(
        output_file,
        index=False,
        encoding="utf-8",
    )

    print(f"File successfully generated at: {output_file}")


if __name__ == "__main__":
    main()
