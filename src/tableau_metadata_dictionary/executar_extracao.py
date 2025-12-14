from pathlib import Path
import pandas as pd

from verificar_twb_ou_twbx import verificar_twb_ou_twbx
from extracao_de_campos import get_calculated_fields


# ===============================
# Caminhos base do projeto
# ===============================
BASE_DIR = Path(__file__).resolve().parents[2]
DATA_OUTPUT_DIR = BASE_DIR / "data" / "output"
DATA_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ===============================
# Arquivo Tableau de entrada
# ===============================
url_twb = Path(r"C:\Users\User\Desktop\Portfolio_Layout01_Superstore.twbx")
xml_path = verificar_twb_ou_twbx(url_twb)


# ===============================
# Extração de campos calculados
# ===============================
prefixos = ("kpi_", "hp_", "prmt_", "filter_", "dt_", "aux_", "fmt_", "var_")
campos = get_calculated_fields(xml_path, prefixes=prefixos)


# ===============================
# Exportação do CSV
# ===============================
output_file = DATA_OUTPUT_DIR / "campos_calculados_sample.csv"

pd.DataFrame(campos).to_csv(
    output_file,
    index=False,
    encoding="utf-8"
)

print(f"Arquivo gerado com sucesso em: {output_file}")