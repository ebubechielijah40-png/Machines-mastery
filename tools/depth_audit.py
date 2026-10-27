#!/usr/bin/env python3
"""Compatibility entry point for the expanded content-risk inventory.

Strict by default; --report-only writes risks without calling them a quality pass.
Historical old-auditor output remains in research/quality/2026-10-22/baseline.
"""
from quality_audit import main

if __name__ == '__main__':
    raise SystemExit(main())
