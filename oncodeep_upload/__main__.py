#!/usr/bin/env python3
""" __main__.py

Entrypoint for oncodeep_upload
"""
import os
import subprocess
import argparse
from pathlib import Path
from .oncodeep_upload import OncoDeepUpload
from logger import Logger
import config


def arg_parse() -> dict:
    """
    Parse arguments supplied by the command line. Create argument parser, define command
    line arguments, then parse supplied command line arguments using the created
    argument parser
        :return (dict): Parsed command line attributes
    """
    info_string = "Upload a file to the OncoDEEP SFTP server"
    parser = argparse.ArgumentParser(
        description=info_string,
        usage=info_string,
    )
    parser.add_argument(
        "-R",
        "--run_identifier",
        type=str,
        help="Run identifier for the run",
        required=True,
    )
    parser.add_argument(
        "-F",
        "--file_path",
        type=lambda x: is_valid_file(parser, x),
        help="Path of file to upload",
        required=True,
    )
    parser.add_argument(
        "-H",
        "--hostname",
        type=str,
        help="Hostname for the OncoDEEP SFTP server",
        required=True,
    )
    parser.add_argument(
        "-U",
        "--username",
        type=str,
        help="Username for the OncoDEEP SFTP server",
        required=True,
    )
    parser.add_argument(
        "-P",
        "--password",
        type=str,
        help="Password for the OncoDEEP SFTP server",
        required=True,
    )
    return vars(parser.parse_args())


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


args = arg_parse()
outdir = os.path.join(os.getcwd(), "outputs")
filename = Path(args["file_path"]).stem

logfile_path = os.path.join(
    outdir, f"oncodeep_upload.{filename}.{config.TIMESTAMP}.log"
)
logger = Logger(__package__, logfile_path).logger

if not os.path.isdir(outdir):
    os.mkdir(outdir)

logger.info(f"Running oncodeep_upload {git_tag()}")

okdm_upload = OncoDeepUpload(
    args["file_path"],
    args["run_identifier"],
    args["hostname"],
    args["username"],
    args["password"],
    logger,
)
okdm_upload.upload_file()
okdm_upload.close_connection()
