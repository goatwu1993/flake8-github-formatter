"""
VSO Formatters.
"""

from enum import Enum
from typing import Optional

from flake8.violation import Violation

from .base import BaseUtilsReporter


class VsoErrorLevelEnum(str, Enum):
    """
    Check https://learn.microsoft.com/en-us/azure/devops/pipelines/scripts/logging-commands?view=azure-devops&tabs=bash.
    """

    ERROR = "error"
    WARNING = "warning"


class Vso(BaseUtilsReporter):
    """GitHub formatter for Flake8."""

    reporter_prefix = "vso"
    error_format = "##vso[task.logissue type=%(error_level)s;sourcepath=%(path)s;linenumber=%(row)d;columnnumber=%(col)d;code=%(code)s;]%(text)s"

    @classmethod
    def add_options(cls, option_manager) -> None:
        option_manager.add_option(
            f"--{cls.reporter_prefix}-error-level",
            default=VsoErrorLevelEnum.ERROR.value,
            choices=[e.value for e in VsoErrorLevelEnum],
            help=f"{cls.reporter_prefix}-error-level",
        )

    @classmethod
    def parse_options(cls, option_manager) -> None:
        super().parse_options(option_manager)
        cls.error_level = getattr(option_manager, f"{cls.reporter_prefix}_error_level")

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
