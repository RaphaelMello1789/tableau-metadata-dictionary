"""
extracao_de_campos.py

Extrai metadados de **campos calculados** (calculated fields) de um arquivo
Tableau Workbook (`.twb`).

Principais diferenças em relação à primeira versão:
1. Ignora *namespaces* – muitos `.twb` não usam prefixo `t:` nos nós
   `<column>`/`<calculation>`. Assim, usamos `local-name()` para encontrar os
   elementos.
2. Filtro opcional por **prefixos** (ex.: `kpi_`, `prmt_`, …). Se passado,
   devolve apenas os campos cujo `field_name` começa com qualquer prefixo.

Uso rápido
----------
from pathlib import Path
from extracao_de_campos import get_calculated_fields

campos = get_calculated_fields(
    Path("dashboard.twb"),
    prefixes=("kpi_", "hp_", "prmt_"),
)
print(campos[:5])
"""
from __future__ import annotations

from pathlib import Path
from typing import Final, Iterable, List, Dict, Tuple, Optional

from lxml import etree

__all__: Final = ["get_calculated_fields"]


def get_calculated_fields(
    twb_path: Path | str,
    *,
    prefixes: Optional[Tuple[str, ...]] = None,
) -> List[Dict[str, str]]:
    """Percorre o XML e devolve metadados dos campos calculados.

    Parameters
    ----------
    twb_path : Path | str
        Caminho para o arquivo `.twb`.
    prefixes : tuple[str, ...] | None, default None
        Se fornecido, devolve somente os campos cujo *caption/name* começa com
        um dos prefixos.

    Returns
    -------
    list of dict
        Cada item traz chaves: **field_name**, **formula**, **datasource**.
    """

    twb_path = Path(twb_path)
    tree = etree.parse(str(twb_path))
    root = tree.getroot()

    # Helpers -----------------------------------------------------------------
    def _lname(tag: str) -> str:  # local‑name sem namespace
        return tag.split("}")[-1] if "}" in tag else tag

    def _iter_columns() -> Iterable[etree._Element]:  # noqa: WPS430
        for el in root.iter():
            if _lname(el.tag) == "column":
                yield el

    # -------------------------------------------------------------------------
    results: List[Dict[str, str]] = []

    for col in _iter_columns():
        # Verifica se possui filho <calculation>
        calc_child = next(
            (c for c in col if _lname(c.tag) == "calculation"),
            None,
        )
        if calc_child is None:
            continue  # não é campo calculado

        field_name = col.get("caption") or col.get("name")  # caption > name
        if not field_name:
            continue  # segurança extra

        # Aplica filtro de prefixos, se solicitado
        if prefixes and not field_name.startswith(prefixes):
            continue

        formula = calc_child.get("formula", "")
        datasource = col.get("datatype", "desconhecido")

        results.append(
            {
                "field_name": field_name,
                "formula": formula,
                "datasource": datasource,
            }
        )

    return results
