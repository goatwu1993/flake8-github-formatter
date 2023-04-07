"""
Formatters
"""

from flake8.formatting.default import SimpleFormatter


class GitHub(SimpleFormatter):
    """GitHub formatter for Flake8."""

    error_format = (
        "::error title=Flake8 %(code)s,file=%(path)s,"
        "line=%(row)d,col=%(col)d,endLine=%(row)d,endColumn=%(col)d"
        "::%(code)s %(text)s"
    )
