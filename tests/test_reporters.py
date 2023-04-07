import argparse

import pytest
from flake8.violation import Violation

from flake8_github_formatter.formatters import GitHub


def _opts(**kwargs):
    kwargs.setdefault("quiet", 0),
    kwargs.setdefault("color", "never")
    kwargs.setdefault("output_file", None)
    return argparse.Namespace(**kwargs)


@pytest.fixture
def violation():
    return Violation(
        code="E501",
        filename="test/test1.py",
        line_number=1,
        column_number=2,
        text="line too long (124 > 79 characters)",
        physical_line=None,
    )


@pytest.mark.parametrize(
    "format_input, error_str",
    [
        (
            "github",
            "::error title=Flake8 E501,file=test/test1.py,line=1,col=2,endLine=1,endColumn=2::E501 line too long (124 > 79 characters)",  # noqa: E501
        ),
    ],
)
def test_make_formatter_custom(violation, format_input, error_str):
    ret = GitHub(_opts(format=format_input))
    assert ret.format(violation) == error_str
