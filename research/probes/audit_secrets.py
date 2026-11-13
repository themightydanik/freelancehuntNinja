"""Read-only heuristic scan. Never output values, hashes of values, or source lines."""
import ast
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PATTERNS = {
    "telegram_token_shape": re.compile(rb"\b\d{8,12}:[A-Za-z0-9_-]{30,50}\b"),
    "groq_token_shape": re.compile(rb"gsk_[A-Za-z0-9]{20,}"),
    "github_token_shape": re.compile(rb"(?:ghp_|github_pat_)[A-Za-z0-9_]{20,}"),
    "credential_literal": re.compile(rb'''(?im)^(?:API_TOKEN|FREELANCEHUNT_TOKEN|GROQ_API_KEY)\s*=.*(?:getenv|environ).*[, ]+["'][^"'\r\n]{16,}["']'''),
}

def git(*args):
    return subprocess.check_output(["git", "-C", str(ROOT), *args])

def main():
    baseline = git("rev-parse", "HEAD").decode().strip()
    commits = git("rev-list", "--all").decode().splitlines()
    findings = []
    blobs = {}
    # Enumerate every reachable commit tree, not only current filenames.
    for commit in commits:
        for entry in git("ls-tree", "-r", "-z", commit).split(b"\0"):
            if not entry:
                continue
            meta, path = entry.split(b"\t", 1)
            _, kind, oid = meta.split()
            if kind != b"blob":
                continue
            key = (oid, path)
            if key in blobs:
                continue
            blobs[key] = True
            content = git("cat-file", "blob", oid.decode())
            for rule, pattern in PATTERNS.items():
                matches = list(pattern.finditer(content))
                if matches:
                    findings.append({"commit_first_encountered": commit,
                                     "path": path.decode(errors="replace"),
                                     "rule": rule, "count": len(matches)})
    result = {"scope": "all blobs in all locally reachable refs; heuristic, not exhaustive",
              "baseline_head": baseline,
              "commits_scanned": len(commits), "unique_blob_path_pairs": len(blobs),
              "findings": findings, "secret_values_emitted": False}
    (ROOT / "data/security_audit.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"commits": len(commits), "finding_rows": len(findings)}))

if __name__ == "__main__":
    main()
