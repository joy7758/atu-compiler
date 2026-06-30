#!/usr/bin/env python3
"""Check that the active Hugging Face identity matches ATU's canonical namespace."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


EXPECTED_USER = "joy7758"
DATASET_ID = "joy7758/atu-trace-1000"
LOCAL_DATASET_DIR = Path("hf_dataset/atu_trace_1000")


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def hf_command() -> list[str] | None:
    local_hf = Path(".venv/bin/hf")
    if local_hf.exists():
        return [str(local_hf)]
    hf = shutil.which("hf")
    if hf:
        return [hf]
    legacy = shutil.which("huggingface-cli")
    if legacy:
        return [legacy]
    return None


def run(args: list[str]) -> dict[str, object]:
    try:
        completed = subprocess.run(
            args,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=30,
        )
    except subprocess.TimeoutExpired as exc:
        return {
            "ok": False,
            "returncode": "timeout",
            "stdout": (exc.stdout or "").strip() if isinstance(exc.stdout, str) else "",
            "stderr": (exc.stderr or "").strip() if isinstance(exc.stderr, str) else "",
        }
    return {
        "ok": completed.returncode == 0,
        "returncode": completed.returncode,
        "stdout": completed.stdout.strip(),
        "stderr": completed.stderr.strip(),
    }


def parse_username(stdout: str) -> str | None:
    for line in stdout.splitlines():
        value = line.strip()
        if not value:
            continue
        if value.lower().startswith(("orgs:", "organizations:")):
            continue
        return value.split()[0]
    return None


def local_dataset_status() -> dict[str, object]:
    return {
        "path": str(LOCAL_DATASET_DIR),
        "exists": LOCAL_DATASET_DIR.exists(),
        "readme_present": (LOCAL_DATASET_DIR / "README.md").exists(),
        "train_present": (LOCAL_DATASET_DIR / "data" / "train.jsonl").exists(),
    }


def main() -> int:
    command = hf_command()
    payload: dict[str, object] = {
        "schema_version": "1.0",
        "project": "ATU",
        "release": "v0.2.0",
        "checked_at": utc_now(),
        "mode": "hf_canonical_identity_check",
        "canonical_dataset": DATASET_ID,
        "required_hf_user": EXPECTED_USER,
        "local_dataset": local_dataset_status(),
        "mutation": "none",
    }
    if command is None:
        payload.update(
            {
                "ok": False,
                "status": "hf_cli_not_found",
                "next_gate": "install_huggingface_hub_cli",
            }
        )
        json.dump(payload, sys.stdout, indent=2, sort_keys=True)
        sys.stdout.write("\n")
        return 69

    result = run([*command, "auth", "whoami"])
    payload["command"] = [*command, "auth", "whoami"]
    if not result["ok"]:
        payload.update(
            {
                "ok": False,
                "status": "hf_not_authenticated",
                "actual_hf_user": None,
                "stderr": result["stderr"],
                "next_gate": "hf_auth_login_as_joy7758",
            }
        )
        json.dump(payload, sys.stdout, indent=2, sort_keys=True)
        sys.stdout.write("\n")
        return 78

    actual_user = parse_username(str(result["stdout"]))
    identity_matches = actual_user == EXPECTED_USER
    payload.update(
        {
            "ok": identity_matches,
            "status": "identity_match" if identity_matches else "identity_mismatch",
            "actual_hf_user": actual_user,
            "next_gate": "upload_dataset" if identity_matches else "switch_hf_identity_to_joy7758",
        }
    )
    json.dump(payload, sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")
    return 0 if identity_matches else 78


if __name__ == "__main__":
    raise SystemExit(main())
