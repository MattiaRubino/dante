#!/usr/bin/env bash
set -euo pipefail

MIN_VERSION="2.32.0"
TESTED_VERSION="2.36.38"
AWS_BIN_DIR="${XDG_BIN_HOME:-${HOME}/.local/bin}"
AWS_DATA_DIR="${XDG_DATA_HOME:-${HOME}/.local/share/aws-cli}"
AWS_BIN="${AWS_BIN_DIR}/aws"

version_ge() {
  local left="$1"
  local right="$2"
  [[ "$(printf '%s\n%s\n' "$right" "$left" | sort -V | head -n1)" == "$right" ]]
}

if [[ ! -x "$AWS_BIN" ]]; then
  command -v curl >/dev/null 2>&1 || {
    printf 'ERROR: curl is required to install AWS CLI v2.\n' >&2
    exit 1
  }

  printf 'AWS CLI v2 not found at %s; installing with the official AWS user-local installer.\n' "$AWS_BIN"
  curl -fsSL https://awscli.amazonaws.com/v2/install.sh | bash
fi

if [[ ! -x "$AWS_BIN" ]]; then
  printf 'ERROR: AWS CLI installer completed but %s is unavailable.\n' "$AWS_BIN" >&2
  exit 1
fi

VERSION_OUTPUT="$($AWS_BIN --version 2>&1)"
VERSION="${VERSION_OUTPUT#aws-cli/}"
VERSION="${VERSION%% *}"

if ! version_ge "$VERSION" "$MIN_VERSION"; then
  printf 'ERROR: AWS CLI %s is below required minimum %s for aws login.\n' "$VERSION" "$MIN_VERSION" >&2
  exit 1
fi

printf 'AWS CLI prerequisite PASS\n'
printf '  binary          : %s\n' "$AWS_BIN"
printf '  install data    : %s\n' "$AWS_DATA_DIR"
printf '  installed       : %s\n' "$VERSION"
printf '  required minimum: %s\n' "$MIN_VERSION"
printf '  tested baseline : %s\n' "$TESTED_VERSION"

if [[ "$VERSION" != "$TESTED_VERSION" ]]; then
  printf 'NOTE: current version differs from the recorded UAT baseline; >= %s remains supported.\n' "$MIN_VERSION"
fi

printf '\nUse the absolute binary path below so a fresh shell does not depend on PATH refresh:\n'
printf '  %s login --profile dante-uat --region eu-west-3\n' "$AWS_BIN"
