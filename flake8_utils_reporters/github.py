"""
GitHub Formatters.
"""

from enum import Enum
from typing import Optional

from flake8.violation import Violation

from .base import BaseUtilsReporter


class GitHubErrorLevelEnum(str, Enum):
    """
    Check https://docs.github.com/en/actions/using-workflows/workflow-commands-for-github-actions.
    """

    ERROR = "error"
    NOTICE = "notice"
    DEBUG = "debug"
    WARNING = "warning"


class GitHub(BaseUtilsReporter):
    """GitHub formatter for Flake8."""

    error_format = (
        "::%(error_level)s title=Flake8 %(code)s,file=%(path)s,"
        "line=%(row)d,col=%(col)d,endLine=%(row)d,endColumn=%(col)d"
        "::%(code)s %(text)s"
    )
    git_relative_path = False

    @classmethod
    def add_options(cls, option_manager) -> None:
        super().add_options(option_manager)
        option_manager.add_option(
            "--error-level",
            default=GitHubErrorLevelEnum.ERROR.value,
            choices=[e.value for e in GitHubErrorLevelEnum],
            help=("error-level"),
        )

    @classmethod
    def parse_options(cls, option_manager) -> None:
        super().parse_options(option_manager)
        cls.error_level = option_manager.error_level

    def format(self, error: Violation) -> Optional[str]:
        """Format and write error out.

        If an output filename is specified, write formatted errors to that
        file. Otherwise, print the formatted error to standard out.
        """
        return self.error_format % {
            "error_level": self.error_level,
            "code": error.code,
            "text": error.text,
            "path": self.to_repo_relative_path(error.filename)
            if self.git_relative_path
            else error.filename,
            "row": error.line_number,
            "col": error.column_number,
        }
