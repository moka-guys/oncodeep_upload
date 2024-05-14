#!/usr/bin/env python3
""" __main__.py

Entrypoint for qiagen_upload
"""
import os
import argparse
from .oncodeep_upload import OncoDeepUpload
from logger import Logger
import config
import toolbox


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
        type=lambda x: toolbox.is_valid_file(parser, x),
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


args = arg_parse()
outdir = os.path.join(os.getcwd(), "outputs")
logfile_path = os.path.join(
    outdir, f"oncodeep_upload.{args['run_identifier']}.{config.TIMESTAMP}.log"
)
logger = Logger(__package__, logfile_path).logger

if not os.path.isdir(outdir):
    os.mkdir(outdir)

logger.info(f"Running oncodeep_upload {toolbox.git_tag()}")

okdm_upload = OncoDeepUpload(args['file_path'], args['run_identifier'], args['hostname'], args['username'], args['password'], logger)
okdm_upload.upload_file()
okdm_upload.close_connection()