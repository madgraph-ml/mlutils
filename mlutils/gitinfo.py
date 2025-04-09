import subprocess

def get_git_commit_hash():
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"]).decode("ascii").strip()
    except Exception:
        return "Unknown"


def is_git_dirty():
    try:
        status = subprocess.check_output(["git", "status", "--porcelain"]).decode("ascii").strip()
        return len(status) > 0
    except Exception:
        return False