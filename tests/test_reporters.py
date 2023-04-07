import argparse
import importlib.metadata

import pytest

from flake8.formatting import default
from flake8.plugins import finder
from flake8.plugins import reporter
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

@pytest.fixture
def reporters():
    def _plugin(name, cls):
        return finder.LoadedPlugin(
            finder.Plugin(
                "flake8",
                "123",
                importlib.metadata.EntryPoint(
                    name, f"{cls.__module__}:{cls.__name__}", "flake8.report"
                ),
            ),
            cls,
            {"options": True},
        )

    return {
        "default": _plugin("default", default.Default),
        "pylint": _plugin("pylint", default.Pylint),
        "pylint": _plugin("pylint", default.Pylint),
        "quiet-filename": _plugin("quiet-filename", default.FilenameOnly),
        "quiet-nothing": _plugin("quiet-nothing", default.Nothing),
    }



@pytest.mark.parametrize(
    "format_input, error_str",
    [
        (
            "github",
            "::error title=Flake8 E501,file=test/test1.py,line=1,col=2,endLine=1,endColumn=2::E501 line too long (124 > 79 characters)",  # noqa: E501
        ),
    ],
)
def test_make_formatter_custom(
    violation, format_input, error_str
):
    ret = GitHub(_opts(format=format_input))
    assert ret.format(violation) == error_str


