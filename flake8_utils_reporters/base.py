"""
Formatters.
"""
import logging
from functools import lru_cache
from pathlib import Path
from typing import Optional

from flake8.formatting.base import BaseFormatter
from flake8.options.manager import OptionManager
from flake8.violation import Violation

from .utils import get_git_root

TRUSIES = ["1", "True", "true", True]
FALSIES = ["0", "False", "false", False]

logger = logging.getLogger(__name__)


class BaseUtilsReporter(BaseFormatter):
    """Base Formatter for This Package."""

    def format(self, error: Violation) -> Optional[str]:
        raise NotImplementedError

    @classmethod
    @lru_cache(maxsize=1)
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
            cls.git_root = get_git_root(origin_file_path)
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
