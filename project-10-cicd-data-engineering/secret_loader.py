import os


def get_secret(name, required=False):
    """Read a secret from an environment variable."""
    value = os.getenv(name)

    if required and not value:
        raise RuntimeError(
            f"Required secret '{name}' is not configured."
        )

    return value


def get_database_password():
    return get_secret("DB_PASSWORD")


def get_aws_access_key():
    return get_secret("AWS_ACCESS_KEY_ID")


if __name__ == "__main__":
    print("Secret loader ready. Values are intentionally not printed.")
