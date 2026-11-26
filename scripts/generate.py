#!/usr/bin/env python3
"""Regenerate contract bindings with the pinned abi-typegen release."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess

def verify_artifact(artifact: dict, name: str, config: dict) -> None:
    metadata = artifact.get("rawMetadata", artifact.get("metadata"))
    if isinstance(metadata, str):
        metadata = json.loads(metadata)
    if metadata["compiler"]["version"] != config["compilerVersion"]:
        raise ValueError(f"compiler version mismatch for {name}")

    def canonical(value):
        return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)

    # Match the normalized ABI hashes in the SDKs' contracts provenance manifest.
    entries = [dict(entry) for entry in artifact["abi"]]
    for entry in entries:
        if entry.get("outputs") == []:
            entry.pop("outputs")
        if entry.get("type") in ("receive", "fallback") and entry.get("inputs") == []:
            entry.pop("inputs")
    digest = hashlib.sha256(canonical(sorted(entries, key=canonical)).encode()).hexdigest()
    if digest != config["abiSha256"][name]:
        raise ValueError(f"ABI hash mismatch for {name} at {config['contractsRevision']}")


root = Path(__file__).resolve().parents[1]
config = json.loads((root / "generation.json").read_text())
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--check", action="store_true")
args = parser.parse_args()
binary = os.environ.get("ABI_TYPEGEN", "abi-typegen")
try:
    version = subprocess.run([binary, "--version"], check=True, capture_output=True, text=True).stdout.strip()
except (OSError, subprocess.CalledProcessError) as error:
    parser.error(f"install abi-typegen {config['version']} or set ABI_TYPEGEN: {error}")
if version != f"abi-typegen {config['version']}":
    parser.error(f"abi-typegen {config['version']} is required; found {version!r}")
contracts = Path(os.environ.get("DIESIS_CONTRACTS_DIR", root / "../../diesis-core/diesis/contracts")).resolve()
artifacts = Path(os.environ.get("DIESIS_ARTIFACTS_DIR", contracts / "out"))
try:
    for name in config["contracts"]:
        matches = sorted(artifacts.rglob(f"{name}.json"))
        if len(matches) != 1:
            raise ValueError(f"expected one artifact for {name} in {artifacts}; found {len(matches)}")
        verify_artifact(json.loads(matches[0].read_text()), name, config)
except (OSError, ValueError, KeyError, TypeError) as error:
    parser.exit(1, f"artifact verification failed: {error}\n")
command = [binary, "generate", "--artifacts", str(artifacts),
           "--contracts", ",".join(config["contracts"]), "--target", config["target"],
           "--out", str(root / "generated")]
if args.check:
    command.append("--check")
subprocess.run(command, check=True)
