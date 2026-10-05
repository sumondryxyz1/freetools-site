#!/usr/bin/env python3
"""Build entry point.

The generator is split into part1.py, part2.py and part3.py so each file stays
small enough to upload comfortably from a phone. This runner joins them in
order and executes the result, so the build command stays `python3 build.py`.
"""
from __future__ import annotations

import pathlib

HERE = pathlib.Path(__file__).resolve().parent


def _read(name: str) -> str:
    for base in (HERE, HERE / "parts"):
        candidate = base / name
        if candidate.exists():
            return candidate.read_text(encoding="utf-8")
    raise SystemExit(f"missing {name}")


SOURCE = "".join(_read(f"part{i}.py") for i in (1, 2, 3))
exec(compile(SOURCE, str(HERE / "part1.py"), "exec"),
     {"__name__": "__main__", "__file__": str(HERE / "part1.py")})
