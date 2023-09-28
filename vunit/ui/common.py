# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2014-2023, Lars Asplund lars.anders.asplund@gmail.com

"""
UI common functions
"""

from pathlib import Path
from glob import glob
from os import environ
from logging import getLogger
from typing import Iterable, Optional, List, TypeVar, Union

from ..vhdl_standard import VHDL, VHDLStandard

LOGGER = getLogger(__name__)

TEST_OUTPUT_PATH = "test_output"


def select_vhdl_standard(vhdl_standard: Optional[str] = None) -> VHDLStandard:
    """
    Select VHDL standard either from class initialization or according to environment variable VUNIT_VHDL_STANDARD
    """
    if vhdl_standard is not None:
        return VHDL.standard(vhdl_standard)

    try:
        return VHDL.standard(environ.get("VUNIT_VHDL_STANDARD", "2008"))
    except ValueError:
        LOGGER.error("Invalid standard set by VUNIT_VHDL_STANDARD environment variable")
        raise


T = TypeVar("T")


def lower_generics(generics: dict[str, T]) -> dict[str, T]:
    """
    Convert all generics names to lower case to match internal representation.
    @TODO Maybe warn in case of conflict. VHDL forbids this though so the user will notice anyway.
    """
    return dict((name.lower(), value) for name, value in generics.items())


def check_not_empty(lst: list[T], allow_empty: bool, error_msg: str) -> list[T]:
    """
    Raise ValueError if the list is empty unless allow_empty is True
    Returns the list
    """
    if (not allow_empty) and (not lst):
        raise ValueError(error_msg + ". Use allow_empty=True to avoid exception.")
    return lst


def get_checked_file_names_from_globs(pattern: Union[Iterable[str], str, Path], allow_empty: bool) -> list[str]:
    """
    Get file names from globs and check that exist
    """
    if isinstance(pattern, str):
        patterns: Iterable[str] = [pattern]
    elif isinstance(pattern, Path):
        patterns = [str(pattern)]
    else:
        patterns = pattern

    file_names: List[str] = []
    for pattern_instance in patterns:
        new_file_names = glob(str(pattern_instance), recursive=True)
        check_not_empty(
            new_file_names,
            allow_empty,
            f"Pattern {pattern_instance!r} did not match any file",
        )
        file_names += new_file_names

    return file_names
