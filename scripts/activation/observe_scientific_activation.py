#!/usr/bin/env python3
"""Read-only observer for ATU v0.2 scientific activation gates."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


REPO = "joy7758/atu-compiler"
TAG = "v0.2.0"
HOOK_ID = "647976117"
DATASET_ID = "joy7759/atu-trace-1000"


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def run(args: list[str], timeout: int = 30) -> dict[str, object]:
    if shutil.which(args[0]) is None:
        return {
            "ok": False,
            "returncode": None,
            "stdout": "",
            "stderr": f"command not found: {args[0]}",
        }
    try:
        completed = subprocess.run(
            args,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
        )
        return {
            "ok": completed.returncode == 0,
            "returncode": completed.returncode,
            "stdout": completed.stdout.strip(),
            "stderr": completed.stderr.strip(),
        }
    except subprocess.TimeoutExpired as exc:
        return {
            "ok": False,
            "returncode": "timeout",
            "stdout": (exc.stdout or "").strip() if isinstance(exc.stdout, str) else "",
            "stderr": (exc.stderr or "").strip() if isinstance(exc.stderr, str) else "",
        }


def zenodo_search(query: str) -> dict[str, object]:
    params = urllib.parse.urlencode({"q": query, "sort": "mostrecent", "size": "5"})
    url = f"https://zenodo.org/api/records?{params}"
    last_error = ""
    for attempt in range(1, 4):
        try:
            with urllib.request.urlopen(url, timeout=30) as response:
                data = json.load(response)
            break
        except Exception as exc:  # noqa: BLE001 - observer must not fail on one flaky endpoint.
            last_error = f"{type(exc).__name__}: {exc}"
            if attempt < 3:
                time.sleep(2 * attempt)
    else:
        return {
            "ok": False,
            "query": query,
            "error": last_error,
            "total": None,
            "records": [],
        }

    hits = data.get("hits", {})
    records = [
        {
            "id": hit.get("id"),
            "doi": hit.get("doi"),
            "title": hit.get("metadata", {}).get("title"),
            "conceptdoi": hit.get("conceptdoi"),
        }
        for hit in hits.get("hits", [])
    ]
    return {
        "ok": True,
        "query": query,
        "total": hits.get("total", 0),
        "records": records,
    }


def github_release() -> dict[str, object]:
    result = run(
        [
            "gh",
            "release",
            "view",
            TAG,
            "--repo",
            REPO,
            "--json",
            "tagName,name,url,isDraft,isPrerelease,publishedAt,body",
        ]
    )
    if not result["ok"]:
        return result
    data = json.loads(str(result["stdout"]))
    data["has_retrigger_marker"] = "atu-zenodo-retrigger" in data.get("body", "")
    data.pop("body", None)
    return {"ok": True, **data}


def github_hook_deliveries() -> dict[str, object]:
    if os.environ.get("ATU_OBSERVER_SKIP_REPO_HOOK_DELIVERIES") == "1":
        return {
            "ok": None,
            "status": "skipped",
            "reason": "repo_hook_delivery_api_requires_permissions_not_available_to_github_actions_token",
        }
    result = run(
        [
            "gh",
            "api",
            f"repos/{REPO}/hooks/{HOOK_ID}/deliveries",
            "--jq",
            ".[0:10] | map({event, action, status, delivered_at})",
        ]
    )
    if not result["ok"]:
        return result
    return {"ok": True, "deliveries": json.loads(str(result["stdout"]))}


def hf_dataset_status() -> dict[str, object]:
    hf = Path(".venv/bin/hf")
    cmd = [str(hf), "datasets", "info", DATASET_ID, "--format", "json"] if hf.exists() else [
        "hf",
        "datasets",
        "info",
        DATASET_ID,
        "--format",
        "json",
    ]
    result = run(cmd)
    if not result["ok"]:
        return {
            "ok": False,
            "dataset": DATASET_ID,
            "status": "not_found_or_not_accessible",
            "stderr": result["stderr"],
        }
    return {"ok": True, "dataset": DATASET_ID, "status": "visible"}


def promptfoo_status() -> dict[str, object]:
    root = Path("evals/promptfoo")
    latest_result = None
    result_files = sorted((root / "results").glob("promptfoo-atu-v0.2.0-*.json"))
    if result_files:
        latest_path = max(result_files, key=lambda path: path.stat().st_mtime)
        try:
            data = json.loads(latest_path.read_text())
            prompt_metrics = data.get("results", {}).get("prompts", [{}])[0].get(
                "metrics", {}
            )
            latest_result = {
                "path": str(latest_path),
                "eval_id": data.get("evalId"),
                "test_pass_count": prompt_metrics.get("testPassCount"),
                "test_fail_count": prompt_metrics.get("testFailCount"),
                "test_error_count": prompt_metrics.get("testErrorCount"),
                "assert_pass_count": prompt_metrics.get("assertPassCount"),
                "assert_fail_count": prompt_metrics.get("assertFailCount"),
            }
            latest_result["passed"] = (
                latest_result["test_pass_count"] == 3
                and latest_result["test_fail_count"] == 0
                and latest_result["test_error_count"] == 0
            )
        except Exception as exc:  # noqa: BLE001 - observer should stay read-only.
            latest_result = {
                "path": str(latest_path),
                "passed": False,
                "error": f"{type(exc).__name__}: {exc}",
            }

    status = {
        "local_package": str(root),
        "node_modules_present": (root / "node_modules").exists(),
        "package_lock_present": (root / "package-lock.json").exists(),
        "config_present": (root / "promptfooconfig.yaml").exists(),
        "result_artifact_present": latest_result is not None,
        "latest_result": latest_result,
    }
    return status


def main() -> int:
    payload = {
        "schema_version": "1.0",
        "project": "ATU",
        "release": TAG,
        "checked_at": utc_now(),
        "mode": "read_only_observer",
        "github_release": github_release(),
        "github_zenodo_hook": github_hook_deliveries(),
        "zenodo": {
            "repo_query": zenodo_search('"joy7758/atu-compiler"'),
            "title_query": zenodo_search('"ATU v0.2" "Trace-to-Dataset"'),
        },
        "huggingface": hf_dataset_status(),
        "promptfoo": promptfoo_status(),
        "next_policy": "monitor_zenodo_ingestion_window_no_more_github_release_mutation_without_new_evidence",
    }
    json.dump(payload, sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
