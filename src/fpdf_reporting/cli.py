import subprocess


def lint() -> None:
    subprocess.run(["ruff", "check", ".", "--fix"])


def format() -> None:
    subprocess.run(["ruff", "format", "."])


def typecheck() -> None:
    subprocess.run(["mypy", "src"])


def coverage() -> None:
    subprocess.run(["pytest", "--cov-report=html"])
