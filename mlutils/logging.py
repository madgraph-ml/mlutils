import atexit
import shutil
import sys
from datetime import datetime, timedelta
from pathlib import Path

from .gitinfo import get_git_commit_hash, is_git_dirty


class Documenter:
    """
    Manages experiment output: creates a unique run folder, logs stdout/stderr,
    and handles safe saving of models, plots, and other outputs.
    """

    def __init__(self, run_name, existing_run=None, read_only=False):
        self.run_name = run_name
        script_dir = Path(__file__).resolve().parent

        if existing_run is None:
            now = datetime.now()
            while True:
                full_run_name = now.strftime("%Y%m%d_%H%M%S") + f"_{run_name}"
                self.basedir = script_dir.parent / "results" / full_run_name
                try:
                    self.basedir.mkdir(parents=True)
                    break
                except FileExistsError:
                    now += timedelta(seconds=1)
        else:
            self.basedir = Path(existing_run)

        if not read_only:
            self.tee = Tee(self.add_file("log.txt", add_run_name=False))
            atexit.register(self.close)
            self.log_git_state()

    def add_file(self, name, add_run_name=True):
        new_file = self.get_file(name, add_run_name)
        old_dir = self.basedir / "old"

        if new_file.exists():
            old_dir.mkdir(exist_ok=True)
            shutil.move(str(new_file), str(old_dir / new_file.name))

        return str(new_file)

    def get_file(self, name, add_run_name=False):
        name = Path(name)
        if add_run_name:
            name = name.with_name(f"{name.stem}_{self.run_name}{name.suffix}")
        return self.basedir / name

    def log_git_state(self):
        git_file = self.get_file("gitinfo.txt")
        with open(git_file, "w") as f:
            f.write(f"Commit: {get_git_commit_hash()}\n")
            f.write(f"Dirty: {is_git_dirty()}\n")

    def close(self):
        self.tee.close()
        self.basedir.chmod(0o755)
        for path in self.basedir.rglob("*"):
            if path.is_file():
                path.chmod(0o644)
            elif path.is_dir():
                path.chmod(0o755)


class Tee:
    def __init__(self, log_file):
        self.log_file = Path(log_file).open("w")
        self.stdout = sys.stdout
        self.stderr = sys.stderr
        sys.stdout = self
        sys.stderr = self

    def close(self):
        sys.stdout = self.stdout
        sys.stderr = self.stderr
        self.log_file.close()

    def write(self, data):
        self.log_file.write(data)
        self.stdout.write(data)

    def flush(self):
        self.log_file.flush()

    def isatty(self):
        return False
