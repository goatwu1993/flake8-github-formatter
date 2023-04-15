"""
Formatters.
"""
import logging
from functools import lru_cache
from pathlib import Path
from subprocess import CalledProcessError, check_output
from typing import Optional

from flake8.formatting.base import BaseFormatter
from flake8.options.manager import OptionManager
from flake8.violation import Violation

TRUSIES = ["1", "True", "true", True]
FALSIES = ["0", "False", "false", False]

logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def root(file_path):
    """returns the absolute path of the repository root."""
    try:
        base = check_output("git rev-parse --show-toplevel", shell=True, cwd=file_path)
    except CalledProcessError:
        raise IOError("Current working directory is not a git repository")
    return base.decode("utf-8").strip()


class GitHub(BaseFormatter):
    """GitHub formatter for Flake8."""

    error_format = (
        "::error title=Flake8 %(code)s,file=%(path)s,"
        "line=%(row)d,col=%(col)d,endLine=%(row)d,endColumn=%(col)d"
        "::%(code)s %(text)s"
    )
    git_relative_path = False

    def format(self, error: Violation) -> Optional[str]:
        """Format and write error out.

        If an output filename is specified, write formatted errors to that
        file. Otherwise, print the formatted error to standard out.
        """
        return self.error_format % {
            "code": error.code,
            "text": error.text,
            "path": self.to_repo_relative_path(error.filename)
            if self.git_relative_path
            else error.filename,
            "row": error.line_number,
            "col": error.column_number,
        }

    @classmethod
    def add_options(cls, option_manager: OptionManager) -> None:
        option_manager.add_option(
            "--git-relative-path",
            default="False",
            parse_from_config=True,
            help=(
                "whether to translate path to repository relative path"
                "when using --format github-format"
            ),
        )

    @classmethod
    def parse_options(cls, option_manager: OptionManager) -> None:
        if option_manager.git_relative_path in TRUSIES:
            cls.git_relative_path = True
            origin_file_path = (
                Path(".")
                if isinstance(option_manager.filename, list)
                else option_manager.filename
            )
            cls.git_root = root(origin_file_path)
        else:
            if option_manager.git_relative_path not in FALSIES:
                logger.warning(
                    "Unknown git_relative_path %s. Set to False",
                    option_manager.git_relative_path,
                )
            cls.git_relative_path = False

    @classmethod
    def to_repo_relative_path(cls, filename):
        return Path(filename).resolve().relative_to(Path(cls.git_root))
