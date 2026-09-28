"""Build and exercise the public C contract; no repository build artifacts."""
from pathlib import Path
import subprocess
import tempfile
B = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix="mm-c-") as temp:
    for flags in (["-O0"], ["-O2"], ["-O1", "-fsanitize=undefined", "-fno-sanitize-recover=all"]):
        exe = str(Path(temp) / "test")
        cmd = ["cc", "-std=c11", "-Wall", "-Wextra", "-Werror", *flags,
               str(B / "solutions/parser.c"), str(B / "tests/test_parser.c"), "-o", exe]
        subprocess.run(cmd, check=True)
        subprocess.run([exe], check=True)
        print("PASS build", " ".join(flags))
