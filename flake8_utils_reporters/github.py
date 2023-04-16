"""
GitHub Formatters.
"""

from typing import Optional

from flake8.violation import Violation

from .base import BaseUtilsReporter


class GitHub(BaseUtilsReporter):
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
