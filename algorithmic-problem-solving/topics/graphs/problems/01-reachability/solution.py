"""Shared original mechanism; inspect ../../code/graph_algorithms.py."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/"code"))
from graph_algorithms import reachable as solve
