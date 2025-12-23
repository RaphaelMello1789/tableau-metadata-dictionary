from __future__ import annotations

import logging
import zipfile
from pathlib import Path
from typing import Final

try:
    import magic  # type: ignore
except ImportError:
    magic = None  # type: ignore
    import mimetypes  # noqa: F401

__all__: Final = ["verificar_twb_ou_twbx"]


class TWBExtractionError(RuntimeError):
    """
    Raised when a `.twbx` file does not contain any valid `.twb` file.
    """


def verificar_twb_ou_twbx(path: Path | str) -> Path:
    """
    Ensures that the provided Tableau file path points to a `.twb` file.

    If the input path already refers to a `.twb` file, it is returned as-is.
    If the input path refers to a `.twbx` file, the first internal `.twb` file
    is extracted and its path is returned.

    Parameters
    ----------
    path : Path | str
        Path to a Tableau file (`.twb` or `.twbx`).

    Returns
    -------
    Path
        Path to a `.twb` file ready to be parsed.

    Raises
    ------
    FileNotFoundError
        If the provided path does not exist.
    ValueError
        If the file extension is not `.twb` or `.twbx`.
    TWBExtractionError
        If no `.twb` file is found inside a `.twbx`.
    """

    path = Path(path).expanduser().resolve()
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    if path.suffix.lower() == ".twb":
        return path

    if path.suffix.lower() != ".twbx":
        raise ValueError("File extension must be .twb or .twbx")

    is_zip = False
    if magic is not None:
        mime = magic.from_file(str(path), mime=True)
        is_zip = mime == "application/zip"
    if not is_zip:
        is_zip = zipfile.is_zipfile(path)

    if not is_zip:
        raise ValueError(f"The file {path} does not appear to be a valid .twbx")

    with zipfile.ZipFile(path) as z:
        twb_files = [n for n in z.namelist() if n.lower().endswith(".twb")]
        if not twb_files:
            raise TWBExtractionError("No .twb file found inside the .twbx")

        twb_name = twb_files[0]
        out_path = path.with_suffix(".twb")
        logging.info("Extracting %s to %s", twb_name, out_path)
        out_path.write_bytes(z.read(twb_name))
        return out_path
