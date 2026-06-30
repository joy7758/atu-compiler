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


def github_hook_info() -> dict[str, object]:
    if os.environ.get("ATU_OBSERVER_SKIP_REPO_HOOK_DELIVERIES") == "1":
        return {
            "ok": None,
            "status": "skipped",
            "reason": "repo_hook_api_requires_permissions_not_available_to_github_actions_token",
        }
    result = run(
        [
            "gh",
            "api",
            f"repos/{REPO}/hooks/{HOOK_ID}",
            "--jq",
            "{active, created_at, events, name, updated_at}",
        ]
    )
    if not result["ok"]:
        return result
    return {"ok": True, **json.loads(str(result["stdout"]))}


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


def parse_github_time(value: object) -> datetime | None:
    if not isinstance(value, str) or not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def zenodo_ingestion_diagnosis(
    release: dict[str, object],
    hook: dict[str, object],
    deliveries: dict[str, object],
) -> dict[str, object]:
    release_published_at = release.get("publishedAt")
    hook_created_at = hook.get("created_at")
    if hook.get("status") == "skipped" or deliveries.get("status") == "skipped":
        return {
            "release_published_at": release_published_at,
            "hook_created_at": hook_created_at,
            "release_predates_zenodo_hook": None,
            "release_delivery_actions_seen": [],
            "has_release_published_delivery": None,
            "has_release_edited_delivery": None,
            "edited_delivery_ingested_release": False,
            "new_release_published_event_required": None,
            "status": "indeterminate_without_repo_hook_delivery_permission",
            "reason": (
                "Repository hook delivery inspection was skipped. Run the local "
                "authenticated observer to determine whether a new release/"
                "published event is required."
            ),
        }
    release_time = parse_github_time(release_published_at)
    hook_time = parse_github_time(hook_created_at)
    delivery_rows = deliveries.get("deliveries")
    if not isinstance(delivery_rows, list):
        delivery_rows = []
    delivery_actions = [
        row.get("action")
        for row in delivery_rows
        if isinstance(row, dict) and row.get("event") == "release"
    ]
    has_published_delivery = "published" in delivery_actions
    has_edited_delivery = "edited" in delivery_actions
    release_predates_hook = (
        release_time is not None and hook_time is not None and release_time < hook_time
    )
    diagnosis = {
        "release_published_at": release_published_at,
        "hook_created_at": hook_created_at,
        "release_predates_zenodo_hook": release_predates_hook,
        "release_delivery_actions_seen": delivery_actions,
        "has_release_published_delivery": has_published_delivery,
        "has_release_edited_delivery": has_edited_delivery,
        "edited_delivery_ingested_release": False,
        "new_release_published_event_required": bool(
            release_predates_hook and not has_published_delivery
        ),
    }
    if diagnosis["new_release_published_event_required"]:
        diagnosis["reason"] = (
            "v0.2.0 was published before the Zenodo hook existed, and the hook "
            "has only seen an edited release event. Zenodo UI and API still show "
            "no release ingestion."
        )
    return diagnosis


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
    if result["ok"]:
        return {"ok": True, "dataset": DATASET_ID, "status": "visible", "source": "hf_cli"}

    api_url = f"https://huggingface.co/api/datasets/{urllib.parse.quote(DATASET_ID, safe='')}"
    try:
        with urllib.request.urlopen(api_url, timeout=30) as response:
            data = json.load(response)
    except urllib.error.HTTPError as exc:
        return {
            "ok": False,
            "dataset": DATASET_ID,
            "status": "not_found_or_not_accessible",
            "source": "public_api",
            "http_status": exc.code,
            "cli_stderr": result["stderr"],
        }
    except Exception as exc:  # noqa: BLE001 - observer must not fail on one flaky endpoint.
        return {
            "ok": False,
            "dataset": DATASET_ID,
            "status": "unknown_api_error",
            "source": "public_api",
            "error": f"{type(exc).__name__}: {exc}",
            "cli_stderr": result["stderr"],
        }
    return {
        "ok": True,
        "dataset": DATASET_ID,
        "status": "visible",
        "source": "public_api",
        "sha": data.get("sha"),
        "private": data.get("private"),
        "gated": data.get("gated"),
        "disabled": data.get("disabled"),
    }


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
    release = github_release()
    hook = github_hook_info()
    deliveries = github_hook_deliveries()
    payload = {
        "schema_version": "1.0",
        "project": "ATU",
        "release": TAG,
        "checked_at": utc_now(),
        "mode": "read_only_observer",
        "github_release": release,
        "github_zenodo_hook": deliveries,
        "github_zenodo_hook_info": hook,
        "zenodo_ingestion_diagnosis": zenodo_ingestion_diagnosis(
            release, hook, deliveries
        ),
        "zenodo": {
            "repo_query": zenodo_search('"joy7758/atu-compiler"'),
            "title_query": zenodo_search('"ATU v0.2" "Trace-to-Dataset"'),
        },
        "huggingface": hf_dataset_status(),
        "promptfoo": promptfoo_status(),
        "next_policy": "new_release_published_event_requires_explicit_confirmation",
    }
    json.dump(payload, sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
