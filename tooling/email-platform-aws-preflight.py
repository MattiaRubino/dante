from __future__ import annotations

import os
import sys

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError, NoCredentialsError, ProfileNotFound

_PROFILE_ENV = "DANTE_UAT_AWS_PROFILE"
_REGION_ENV = "DANTE_UAT_SES_REGION"
_FROM_ENV = "DANTE_UAT_SES_FROM_ADDRESS"
_DEFAULT_PROFILE = "dante-uat"
_DEFAULT_REGION = "eu-west-3"


def _required_env(name: str) -> str:
    value = os.environ.get(name)
    if value is None or not value or value.strip() != value or any(
        character in value for character in "\r\n"
    ):
        raise RuntimeError(f"{name} must be set to one non-blank trimmed value")
    return value


def main() -> int:
    profile = os.environ.get(_PROFILE_ENV, _DEFAULT_PROFILE)
    region = os.environ.get(_REGION_ENV, _DEFAULT_REGION)
    from_address = _required_env(_FROM_ENV)

    try:
        session = boto3.Session(profile_name=profile, region_name=region)
        sts = session.client(
            "sts",
            config=Config(
                connect_timeout=2,
                read_timeout=5,
                retries={"mode": "standard", "total_max_attempts": 1},
            ),
        )
        ses = session.client(
            "sesv2",
            region_name=region,
            config=Config(
                connect_timeout=2,
                read_timeout=5,
                retries={"mode": "standard", "total_max_attempts": 1},
            ),
        )

        caller = sts.get_caller_identity()
        caller_arn = str(caller.get("Arn", ""))
        if caller_arn.endswith(":root"):
            print(
                "AWS PREFLIGHT FAIL: profile resolves to the AWS account root user. "
                "Root credentials are forbidden for normal DANTE local UAT. "
                "Logout this profile and authenticate as a dedicated least-privilege IAM/federated principal.",
                file=sys.stderr,
            )
            return 5

        identity = ses.get_email_identity(EmailIdentity=from_address)
    except ProfileNotFound as exc:
        print(
            f"AWS PREFLIGHT FAIL: profile {profile!r} does not exist. "
            "Run ~/.local/bin/aws login --profile dante-uat --region eu-west-3.",
            file=sys.stderr,
        )
        raise SystemExit(2) from exc
    except NoCredentialsError as exc:
        print(
            f"AWS PREFLIGHT FAIL: profile {profile!r} has no usable credentials. "
            "Run ~/.local/bin/aws login --profile dante-uat --region eu-west-3.",
            file=sys.stderr,
        )
        raise SystemExit(2) from exc
    except ClientError as exc:
        code = exc.response.get("Error", {}).get("Code", "UnknownClientError")
        print(f"AWS PREFLIGHT FAIL: {code}", file=sys.stderr)
        raise SystemExit(3) from exc

    verification = identity.get("VerificationStatus")
    if verification != "SUCCESS":
        print(
            "SES PREFLIGHT FAIL: sender identity is not verified in the selected region "
            f"(status={verification!r}).",
            file=sys.stderr,
        )
        return 4

    print("SES PREFLIGHT PASS")
    print(f"profile: {profile}")
    print(f"region: {region}")
    print(f"sender identity: {from_address}")
    print(f"verification: {verification}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
