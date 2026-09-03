from __future__ import annotations

import subprocess
from pathlib import Path

import run_m05_email_phase_b as phase_b

EXPECTED_BRANCH = "feature/access-auth"

_SECTION_BY_LABEL: dict[str, tuple[str, str]] = {
    "google set-email staged state": (
        "    async def set_provider_enrollment_email(\n",
        "    async def resend_provider_enrollment_verification(\n",
    ),
    "google set-email atomic intent": (
        "    async def set_provider_enrollment_email(\n",
        "    async def resend_provider_enrollment_verification(\n",
    ),
    "google resend staged state": (
        "    async def resend_provider_enrollment_verification(\n",
        "    async def verify_provider_enrollment(\n",
    ),
    "google resend atomic intent": (
        "    async def resend_provider_enrollment_verification(\n",
        "    async def verify_provider_enrollment(\n",
    ),
    "google persistence atomic stage": (
        "    async def _persist_provider_enrollment(\n",
        "    async def _persist_link_challenge(\n",
    ),
    "apple set-email staged state": (
        "    async def set_provider_enrollment_email(\n",
        "    async def resend_provider_enrollment_verification(\n",
    ),
    "apple set-email atomic intent": (
        "    async def set_provider_enrollment_email(\n",
        "    async def resend_provider_enrollment_verification(\n",
    ),
    "apple resend staged state": (
        "    async def resend_provider_enrollment_verification(\n",
        "    async def verify_provider_enrollment(\n",
    ),
    "apple resend atomic intent": (
        "    async def resend_provider_enrollment_verification(\n",
        "    async def verify_provider_enrollment(\n",
    ),
    "apple persistence atomic stage": (
        "    async def _persist_enrollment(\n",
        "    async def _persist_link(\n",
    ),
}


def run(*args: str) -> str:
    return subprocess.check_output(args, text=True).strip()


def replace_scoped(text: str, old: str, new: str, *, label: str) -> str:
    section = _SECTION_BY_LABEL.get(label)
    if section is None:
        count = text.count(old)
        if count != 1:
            raise RuntimeError(f"{label}: expected exactly one anchor, found {count}")
        return text.replace(old, new, 1)

    start_marker, end_marker = section
    start = text.find(start_marker)
    if start < 0:
        raise RuntimeError(f"{label}: start marker not found")
    end = text.find(end_marker, start + len(start_marker))
    if end < 0:
        raise RuntimeError(f"{label}: end marker not found")
    prefix = text[:start]
    body = text[start:end]
    suffix = text[end:]
    count = body.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected one scoped anchor, found {count}")
    return prefix + body.replace(old, new, 1) + suffix


def validate_repo(root: Path) -> None:
    branch = run("git", "-C", str(root), "branch", "--show-current")
    if branch != EXPECTED_BRANCH:
        raise RuntimeError(f"expected branch {EXPECTED_BRANCH}, found {branch!r}")
    for relative, expected in phase_b.EXPECTED_HASHES.items():
        actual = run("git", "-C", str(root), "hash-object", relative)
        if actual != expected:
            raise RuntimeError(f"unexpected blob for {relative}: {actual} != {expected}")


def _tighten_nullable_provider_timestamp(text: str, *, label: str) -> str:
    old = "if row.verification_expires_at is None:\n"
    new = (
        "if row.verification_expires_at is None or row.verification_issued_at is None:\n"
    )
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected one provider timestamp guard, found {count}")
    return text.replace(old, new, 1)


def main() -> None:
    root = Path(__file__).resolve().parents[3]
    validate_repo(root)
    phase_b.replace_exact = replace_scoped

    targets = {
        relative: (root / relative).read_text()
        for relative in phase_b.EXPECTED_HASHES
    }
    google = _tighten_nullable_provider_timestamp(
        phase_b.patch_google(targets["apps/backend/src/dante/auth/provider_flow.py"]),
        label="google provider timestamp guard",
    )
    apple = _tighten_nullable_provider_timestamp(
        phase_b.patch_apple(targets["apps/backend/src/dante/auth/apple_flow.py"]),
        label="apple provider timestamp guard",
    )
    # Every transformation completes in memory before any target file is written.
    patched = {
        "apps/backend/src/dante/auth/provider_flow.py": google,
        "apps/backend/src/dante/auth/apple_flow.py": apple,
        "apps/backend/src/dante/auth/provider_flow_runtime.py": phase_b.patch_runtime(
            targets["apps/backend/src/dante/auth/provider_flow_runtime.py"]
        ),
    }
    for relative, content in patched.items():
        (root / relative).write_text(content)

    print("M05 Email Platform Phase B SAFE materialized successfully.")
    print("Google + Apple provider-enrollment intents are transactionally staged.")
    print("No commit was created.")


if __name__ == "__main__":
    main()
