#!/usr/bin/env python3
""" toolbox.py

This script contains functions used and imported across multiple modules
"""

import os
import sys
import logging
import subprocess
import json
import argparse


def is_valid_file(parser: argparse.ArgumentParser, arg: str) -> str:
    """
    Check file path is valid
        :param parser (argparse.ArgumentParser):    Holds necessary info to parse cmd
                                                    line into Python data types
        :param arg (str):                           Input argument
        :return (str):                              Input argument
    """
    if not os.path.exists(arg):
        parser.error(f"The file {arg} does not exist!")
    else:
        return arg  # Return argument


def git_tag() -> str:
    """
    Obtain git tag from current commit
        :return stdout (str):   String containing stdout,
                                with newline characters removed
    """
    filepath = os.path.dirname(os.path.realpath(__file__))
    cmd = f"git -C {filepath} describe --tags"

    proc = subprocess.Popen(
        [cmd], stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True
    )
    out, _ = proc.communicate()
    if out.decode("utf-8"):
        return out.rstrip().decode("utf-8")
    else:
        return "[unversioned]"
