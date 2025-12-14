"""
verificar_twb_ou_twbx.py

Função utilitária que garante que sempre teremos um caminho para um arquivo
.TWB pronto para ser parseado.

– Se o caminho recebido já for .twb, ele é simplesmente devolvido.
– Se for .twbx (um ZIP), o primeiro .twb interno é extraído para o mesmo
  diretório, mantendo o nome‑base, e esse novo caminho é devolvido.

Exemplo rápido
--------------
from pathlib import Path
from verificar_twb_ou_twbx import verificar_twb_ou_twbx

xml_path = verificar_twb_ou_twbx(Path("meu_dashboard.twbx"))
print(xml_path)  # → .../meu_dashboard.twb
"""

from __future__ import annotations

import logging
import zipfile
from pathlib import Path
from typing import Final

# Detecção MIME mais robusta (requer libmagic). Caso não exista, fazemos fallback.
try:
    import magic  # type: ignore
except ImportError:  # pragma: no cover – ambiente sem python‑magic
    magic = None  # type: ignore
    import mimetypes  # noqa: F401  # usado apenas no fallback

__all__: Final = ["verificar_twb_ou_twbx"]


class TWBExtractionError(RuntimeError):
    """Exceção lançada quando um .twbx não contém nenhum .twb válido."""


def verificar_twb_ou_twbx(path: Path | str) -> Path:
    """Transforma um `.twbx` em `.twb` (quando necessário).

    Parameters
    ----------
    path : Path | str
        Caminho para um arquivo Tableau (`.twb` ou `.twbx`).

    Returns
    -------
    Path
        Caminho para o arquivo `.twb` que deve ser usado no parsing.

    Raises
    ------
    FileNotFoundError
        Se `path` não existir.
    ValueError
        Se a extensão não for `.twb` nem `.twbx`.
    TWBExtractionError
        Se nenhum `.twb` for encontrado dentro de um `.twbx`.
    """

    # Normaliza o caminho recebido
    path = Path(path).expanduser().resolve()
    if not path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {path}")

    # Caso já seja .twb, não há nada a fazer
    if path.suffix.lower() == ".twb":
        return path

    # Só aceitamos .twbx além de .twb
    if path.suffix.lower() != ".twbx":
        raise ValueError("A extensão deve ser .twb ou .twbx")

    # ---------------------------------------------------------
    # 1) Verifica se o arquivo realmente é um ZIP
    # ---------------------------------------------------------
    is_zip = False
    if magic is not None:
        mime = magic.from_file(str(path), mime=True)
        is_zip = mime == "application/zip"
    if not is_zip:
        # Fallback simples caso magic não esteja disponível
        is_zip = zipfile.is_zipfile(path)

    if not is_zip:
        raise ValueError(f"O arquivo {path} não parece ser um .twbx válido")

    # ---------------------------------------------------------
    # 2) Procura e extrai o primeiro .twb
    # ---------------------------------------------------------
    with zipfile.ZipFile(path) as z:
        twb_files = [n for n in z.namelist() if n.lower().endswith(".twb")]
        if not twb_files:
            raise TWBExtractionError("Nenhum .twb encontrado dentro do .twbx")

        twb_name = twb_files[0]
        out_path = path.with_suffix(".twb")
        logging.info("Extraindo %s para %s", twb_name, out_path)
        out_path.write_bytes(z.read(twb_name))
        return out_path
