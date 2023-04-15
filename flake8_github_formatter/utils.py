from functools import lru_cache
from subprocess import CalledProcessError, check_output


@lru_cache(maxsize=1)
def get_git_root(file_path):
    """returns the absolute path of the repository root."""
    try:
        base = check_output("git rev-parse --show-toplevel", shell=True, cwd=file_path)
    except CalledProcessError:
        raise IOError("Current working directory is not a git repository")
    return base.decode("utf-8").strip()
