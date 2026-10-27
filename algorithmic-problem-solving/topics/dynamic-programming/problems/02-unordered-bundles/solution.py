"""Shared reference; read prompt and derive before opening this file."""
from pathlib import Path
import importlib.util
_spec=importlib.util.spec_from_file_location("mm_dp_reference",Path(__file__).resolve().parents[2]/"code/dp.py")
_module=importlib.util.module_from_spec(_spec);_spec.loader.exec_module(_module)
solve=_module.coin_combinations
