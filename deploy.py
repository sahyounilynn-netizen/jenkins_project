"""Local deployment script for the Lab 10 Jenkins pipeline.

Copies the runnable application into a deployment directory that lives
outside the Jenkins workspace (so ``cleanWs()`` cannot delete it), runs the
deployed copy with the system Python interpreter and checks that it prints
the expected greeting.
"""

import argparse
import datetime
import os
import shutil
import subprocess  # nosec B404 - only used to run the deployed app with a fixed argument list
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent
APP_FILES = ("app.py", "README.md")
EXPECTED_OUTPUT = "Hello, World from Lynn Sahyouni!"
DEFAULT_DEPLOY_ROOT = Path.home() / "Lab10_Deploy" / "Python-CI-CD"


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="Deploy app.py to a local directory and verify it."
    )
    parser.add_argument(
        "--deploy-root", default=os.environ.get("DEPLOY_ROOT", str(DEFAULT_DEPLOY_ROOT))
    )
    parser.add_argument("--build-id", default=os.environ.get("BUILD_NUMBER", "local"))
    parser.add_argument("--commit", default=os.environ.get("GIT_COMMIT", "unknown"))
    parser.add_argument("--expected", default=EXPECTED_OUTPUT)
    parser.add_argument("--report", default=None, help="Optional file for the verification output.")
    return parser.parse_args(argv)


def base_python():
    """Interpreter outside any virtual environment.

    The deployed app therefore does not depend on the Jenkins workspace or its venv.
    """
    return getattr(sys, "_base_executable", None) or sys.executable


def copy_release(deploy_root, build_id, commit):
    """Copy the application into releases/build-<id> and refresh the 'current' directory."""
    release_dir = deploy_root / "releases" / f"build-{build_id}"
    current_dir = deploy_root / "current"
    if release_dir.exists():
        shutil.rmtree(release_dir)
    release_dir.mkdir(parents=True)
    for name in APP_FILES:
        shutil.copy2(PROJECT_DIR / name, release_dir / name)
    deployed_at = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    (release_dir / "VERSION.txt").write_text(
        f"build: {build_id}\ncommit: {commit}\ndeployed_at: {deployed_at}\n", encoding="utf-8"
    )
    if current_dir.exists():
        shutil.rmtree(current_dir)
    shutil.copytree(release_dir, current_dir)
    return release_dir, current_dir, deployed_at


def run_deployed_app(current_dir):
    """Execute the deployed copy of app.py and return (exit code, stripped stdout, stderr)."""
    command = [base_python(), str(current_dir / "app.py")]
    result = subprocess.run(  # nosec B603 - fixed argument list, no shell, trusted local file
        command, cwd=current_dir, capture_output=True, text=True, timeout=60, check=False
    )
    return result.returncode, result.stdout.strip(), result.stderr.strip(), command


def deploy(args):
    deploy_root = Path(args.deploy_root).resolve()
    release_dir, current_dir, deployed_at = copy_release(deploy_root, args.build_id, args.commit)
    returncode, output, errors, command = run_deployed_app(current_dir)
    passed = returncode == 0 and output == args.expected
    lines = [
        f"Deployment root   : {deploy_root}",
        f"Release directory : {release_dir}",
        f"Current directory : {current_dir}",
        f"Build / commit    : {args.build_id} / {args.commit}",
        f"Deployed at       : {deployed_at}",
        f"Command           : {' '.join(command)}",
        f"Exit code         : {returncode}",
        f"Actual output     : {output}",
        f"Expected output   : {args.expected}",
        f"Verification      : {'PASSED' if passed else 'FAILED'}",
    ]
    if errors:
        lines.append(f"Stderr            : {errors}")
    report = "\n".join(lines) + "\n"
    (current_dir / "deploy_verification.txt").write_text(report, encoding="utf-8")
    with open(deploy_root / "deployments.log", "a", encoding="utf-8") as history:
        history.write(report + "-" * 60 + "\n")
    if args.report:
        Path(args.report).parent.mkdir(parents=True, exist_ok=True)
        Path(args.report).write_text(report, encoding="utf-8")
    print(report, end="")
    return 0 if passed else 1


def main(argv=None):
    return deploy(parse_args(argv))


if __name__ == "__main__":
    sys.exit(main())
