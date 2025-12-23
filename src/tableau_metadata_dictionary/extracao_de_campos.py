from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

from lxml import etree


CALC_TOKEN_RE = re.compile(r"(Calculation_\d+)")
CALC_BRACKET_RE = re.compile(r"\[(Calculation_\d+)\]")


def get_calculated_fields(
    twb_path: Path | str,
    *,
    prefixes: Optional[Tuple[str, ...]] = None,
) -> List[Dict[str, str]]:
    """Read the XML and return the metadata of calculated fields.

    Returns
    -------
    list of dict
        Keys: **field_name**, **formula**, **datasource**.
    """

    twb_path = Path(twb_path)
    tree = etree.parse(str(twb_path))
    root = tree.getroot()

    # Helpers -----------------------------------------------------------------
    def _lname(tag: str) -> str:  
        return tag.split("}")[-1] if "}" in tag else tag

    def _iter_columns() -> Iterable[etree._Element]:
        for el in root.iter():
            if _lname(el.tag) == "column":
                yield el

    def _strip_brackets(s: str) -> str:
        s = (s or "").strip()
        if s.startswith("[") and s.endswith("]"):
            return s[1:-1]
        return s

    def _extract_calc_token(s: str) -> str | None:
        if not s:
            return None
        m = CALC_TOKEN_RE.search(str(s))
        return m.group(1) if m else None

    # -------------------------------------------------------------------------
    # 1) Pre-process: solve the issue about the use of Tableau internal ID for calculated field
    
    token_to_caption: Dict[str, str] = {}

    for col in _iter_columns():
        raw_name = col.get("name") or ""
        token = _extract_calc_token(raw_name)
        caption = col.get("caption")

        if token and caption:
            token_to_caption[token] = caption

    # -------------------------------------------------------------------------
    results: List[Dict[str, str]] = []

    for col in _iter_columns():
        calc_child = next((c for c in col if _lname(c.tag) == "calculation"), None)
        if calc_child is None:
            continue 

        raw_field_name = col.get("caption") or col.get("name")
        if not raw_field_name:
            continue

        raw_field_name = _strip_brackets(raw_field_name)

        token = _extract_calc_token(raw_field_name)
        if token and raw_field_name.startswith("Calculation_"):
            raw_field_name = token_to_caption.get(token, raw_field_name)

        field_name = raw_field_name

        if prefixes and not field_name.startswith(prefixes):
            continue

        # 2) Replace [Calculation] for [Caption] if exist
        formula = calc_child.get("formula", "") or ""

        def _repl(match: re.Match) -> str:
            t = match.group(1)
            display = token_to_caption.get(t, t)
            return f"[{display}]"

        formula = CALC_BRACKET_RE.sub(_repl, formula)

        datasource = col.get("datatype", "desconhecido")

        results.append(
            {
                "field_name": field_name,
                "formula": formula,
                "datasource": datasource,
            }
        )

    return results
