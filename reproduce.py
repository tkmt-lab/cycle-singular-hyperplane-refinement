#!/usr/bin/env python3
"""Reproduce pinned finite checks in disposable local directories, offline."""
from pathlib import Path
import hashlib
import json
import platform
import resource
import shutil
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parent
IGNORED_MEASUREMENTS = {
    "elapsed_seconds", "maxrss_bytes", "maxrss_bytes_macos", "python"
}

def normalized(value):
    if isinstance(value, dict):
        return {k: normalized(v) for k, v in value.items()
                if k not in IGNORED_MEASUREMENTS}
    if isinstance(value, list):
        return [normalized(v) for v in value]
    return value

def limit_cpu():
    resource.setrlimit(resource.RLIMIT_CPU, (60, 60))

def main():
    if not __debug__:
        raise SystemExit("Run without -O: the pinned programs use assertions.")
    start = time.monotonic()
    provenance = json.loads((ROOT / "PROVENANCE.json").read_text())
    for item in provenance["sources"]:
        blob = (ROOT / item["snapshot_path"]).read_bytes()
        if len(blob) != item["bytes"] or hashlib.sha256(blob).hexdigest() != item["sha256"]:
            raise RuntimeError("Input snapshot mismatch: " + item["snapshot_path"])
    for copied, source in provenance["exact_copies"].items():
        if (ROOT / copied).read_bytes() != (ROOT / "inputs" / source).read_bytes():
            raise RuntimeError("Executable/baseline copy mismatch: " + copied)
    build = ROOT / "build"
    build.mkdir(exist_ok=True)
    reports = []
    for name in ("endpoint", "reviewer", "gate"):
        with tempfile.TemporaryDirectory(prefix=name + "-", dir=build) as tmp:
            script = Path(tmp) / (name + ".py")
            shutil.copyfile(ROOT / "checks" / script.name, script)
            result = subprocess.run(
                [sys.executable, "-B", str(script)], cwd=tmp,
                capture_output=True, text=True, timeout=60,
                preexec_fn=limit_cpu, check=True)
            if name == "endpoint":
                actual = json.loads((Path(tmp) / "exact-results.json").read_text())
            else:
                actual = json.loads(result.stdout)
            expected = json.loads((ROOT / "baseline" / (name + ".json")).read_text())
            if normalized(actual) != normalized(expected):
                raise RuntimeError("Exact baseline mismatch: " + name)
            reports.append({"name": name, "status": "PASS",
                            "elapsed_seconds": actual["elapsed_seconds"],
                            "data": actual})
    output = {"status": "PASS", "python": platform.python_version(),
              "input_hashes_verified": len(provenance["sources"]),
              "programs": reports,
              "elapsed_seconds": time.monotonic() - start,
              "scope": "author reproduction of finite checks; not a new independent review",
              "network_used_by_runner": False}
    destination = ROOT / "results"
    destination.mkdir(exist_ok=True)
    (destination / "reproduction.json").write_text(
        json.dumps(output, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"status": output["status"],
                      "programs": [p["name"] for p in reports],
                      "elapsed_seconds": output["elapsed_seconds"]}))

if __name__ == "__main__":
    main()
