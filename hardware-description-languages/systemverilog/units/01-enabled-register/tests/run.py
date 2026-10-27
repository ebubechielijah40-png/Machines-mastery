from pathlib import Path
import shutil
import subprocess
import tempfile
B = Path(__file__).resolve().parents[1]
iv = shutil.which("iverilog")
vv = shutil.which("vvp")
if not iv or not vv:
    raise SystemExit("Icarus Verilog tools missing from PATH; simulation not validated")
with tempfile.TemporaryDirectory(prefix="mm-sv-") as temp:
    for filename, should_pass in [("register.sv", True), ("broken_priority.sv", False)]:
        out = str(Path(temp)/"sim")
        subprocess.run([iv, "-g2012", "-s", "tb", "-o", out,
                        str(B/"solutions"/filename), str(B/"tests/tb.sv")], check=True)
        run = subprocess.run([vv,out],text=True,capture_output=True)
        print(filename, run.stdout.strip())
        if should_pass and (run.returncode or "PASS: 1024" not in run.stdout):
            raise SystemExit("reference simulation failed: " + run.stderr)
        if not should_pass and (run.returncode == 0 or "transition" not in run.stdout):
            raise SystemExit("mutant not rejected by intended assertion")
print("PASS: correct RTL accepted and priority mutant rejected")
