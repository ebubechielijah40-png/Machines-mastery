from pathlib import Path
import shutil
import subprocess
import tempfile
B = Path(__file__).resolve().parents[1]
iv = shutil.which("iverilog")
vv = shutil.which("vvp")
flags = []
if not iv:
    iv = "/tmp/machines-tools/usr/bin/iverilog"
    flags = ["-B", "/tmp/machines-tools/usr/lib/x86_64-linux-gnu/ivl"]
if not vv:
    vv = "/tmp/machines-tools/usr/bin/vvp"
if not Path(iv).is_file() or not Path(vv).is_file():
    raise SystemExit("Icarus Verilog tools missing; simulation not validated")
with tempfile.TemporaryDirectory(prefix="mm-sv-") as temp:
    for filename, should_pass in [("register.sv", True), ("broken_priority.sv", False)]:
        out = str(Path(temp)/"sim")
        subprocess.run([iv, *flags, "-g2012", "-s", "tb", "-o", out,
                        str(B/"solutions"/filename), str(B/"tests/tb.sv")], check=True)
        run = subprocess.run([vv,out],text=True,capture_output=True)
        print(filename, run.stdout.strip())
        if should_pass and (run.returncode or "PASS: 1024" not in run.stdout):
            raise SystemExit("reference simulation failed: " + run.stderr)
        if not should_pass and (run.returncode == 0 or "transition" not in run.stdout):
            raise SystemExit("mutant not rejected by intended assertion")
print("PASS: correct RTL accepted and priority mutant rejected")
