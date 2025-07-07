#!/usr/bin/env python3
"""Deployment update script with staging and rollback.

This script clones or pulls the latest code to a staging directory,
executes the test suites and deploys to production if all tests pass.
Two previous production versions are kept as compressed archives for
rollback purposes.
"""
import argparse
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
import tarfile

PROD_DIR = Path("/opt/nucleus-platform")
TEST_DIR = Path("/opt/nucleus-platform-test")
ACCEPT_DIR = Path("/opt/nucleus-platform-accept")
BACKUP_DIR = Path("/opt/nucleus-platform-backups")


def run(cmd, cwd=None):
    """Run a command and raise if it fails."""
    subprocess.run(cmd, cwd=cwd, check=True)


def clone_or_update(repo: str, dest: Path, branch: str = "main"):
    """Clone or pull the repository to the provided directory."""
    if dest.is_dir():
        run(["git", "fetch"], cwd=dest)
        run(["git", "checkout", branch], cwd=dest)
        run(["git", "pull"], cwd=dest)
    else:
        run(["git", "clone", "-b", branch, repo, str(dest)])


def run_tests(target: Path) -> bool:
    """Execute Python and Node test suites in the provided directory."""
    try:
        run(["pytest", "-q"], cwd=target)
        node_dir = target / "node_backend"
        if node_dir.is_dir():
            run(["npm", "test", "--silent"], cwd=node_dir)
    except subprocess.CalledProcessError:
        return False
    return True


def backup_production():
    """Archive the current production directory."""
    if not PROD_DIR.is_dir():
        return
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    archive = BACKUP_DIR / f"prod_{ts}"
    shutil.make_archive(str(archive), "gztar", PROD_DIR)
    # keep only two most recent backups
    backups = sorted(BACKUP_DIR.glob("prod_*.tar.gz"))
    while len(backups) > 2:
        backups[0].unlink()
        backups.pop(0)


def deploy_to_production():
    """Replace production with the tested acceptance build."""
    backup_production()
    if PROD_DIR.is_dir():
        shutil.rmtree(PROD_DIR)
    shutil.copytree(ACCEPT_DIR, PROD_DIR)


def rollback():
    """Restore the newest backup."""
    backups = sorted(BACKUP_DIR.glob("prod_*.tar.gz"))
    if not backups:
        print("No backups available")
        return
    latest = backups[-1]
    if PROD_DIR.is_dir():
        shutil.rmtree(PROD_DIR)
    PROD_DIR.mkdir(parents=True, exist_ok=True)
    with tarfile.open(str(latest), "r:gz") as tf:
        tf.extractall(path=PROD_DIR, filter="data")
    print(f"Rolled back to {latest.name}")


def stage(repo: str, branch: str = "main"):
    """Prepare a test build and promote to acceptance on success."""
    clone_or_update(repo, TEST_DIR, branch)
    if not run_tests(TEST_DIR):
        print("Tests failed; aborting staging")
        return
    if ACCEPT_DIR.is_dir():
        shutil.rmtree(ACCEPT_DIR)
    shutil.copytree(TEST_DIR, ACCEPT_DIR)
    print("Staged build ready for acceptance")


def main():
    parser = argparse.ArgumentParser(description="Update production instance")
    sub = parser.add_subparsers(dest="command", required=True)

    stage_p = sub.add_parser("stage", help="Clone to test and run tests")
    stage_p.add_argument("repo")
    stage_p.add_argument("--branch", default="main")

    sub.add_parser("deploy", help="Deploy accepted build to production")
    sub.add_parser("rollback", help="Rollback to previous version")

    args = parser.parse_args()

    if args.command == "stage":
        stage(args.repo, args.branch)
    elif args.command == "deploy":
        deploy_to_production()
    elif args.command == "rollback":
        rollback()


if __name__ == "__main__":
    main()
